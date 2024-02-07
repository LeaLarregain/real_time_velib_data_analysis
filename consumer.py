import os
os.environ["SPARK_HOME"] = "/workspaces/real_time_velib_data_analysis/spark-3.2.3-bin-hadoop2.7"
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /workspaces/real_time_velib_data_analysis/spark-streaming-kafka-0-10-assembly_2.12-3.2.3.jar pyspark-shell'
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
import findspark
findspark.init()
from pyspark.sql import SparkSession
import pyspark.sql.functions as pysqlf
import pyspark.sql.types as pysqlt

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.3',
    'org.apache.kafka:kafka-clients:3.2.3'
]

# Création de la session Spark
spark = (SparkSession.builder
   .config("spark.jars.packages", ",".join(packages))
   .config("spark.sql.repl.eagerEval.enabled", True)
   .getOrCreate()
)

if __name__ == "__main__":
    # Initier spark
    spark = (SparkSession
             .builder
             .appName("velib-project")
             .master("local[1]")
             .config("spark.sql.shuffle.partitions", 1)
             .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.3")
             .getOrCreate()
             )

    # Lire les données temps réel depuis le topic Kafka
    kafka_df = (spark
                .readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", "localhost:9092")
                .option("subscribe", "velib-projet")
                .option("startingOffsets", "earliest")
                .load()
                )

    # Charger les données du fichier CSV des stations
    station_info_df = spark \
        .read \
        .csv("stations_information.csv", header=True)

    # Convertir les données JSON en colonnes structurées
    schema = pysqlt.StructType([
        pysqlt.StructField("stationCode", pysqlt.StringType()),
        pysqlt.StructField("num_bikes_available", pysqlt.IntegerType()),
        pysqlt.StructField("numBikesAvailable", pysqlt.IntegerType()),
        pysqlt.StructField("num_bikes_available_types", pysqlt.ArrayType(pysqlt.MapType(pysqlt.StringType(), pysqlt.IntegerType()))),
        pysqlt.StructField("num_docks_available", pysqlt.IntegerType()),
        pysqlt.StructField("numDocksAvailable", pysqlt.IntegerType()),
        pysqlt.StructField("is_installed", pysqlt.IntegerType()),
        pysqlt.StructField("is_returning", pysqlt.IntegerType()),
        pysqlt.StructField("is_renting", pysqlt.IntegerType()),
        pysqlt.StructField("last_reported", pysqlt.TimestampType())
    ])

    kafka_df = (kafka_df
                .select(pysqlf.from_json(pysqlf.col("value").cast("string"), schema).alias("value"))
                .select("value.*")  # Sélectionner les colonnes structurées
                )

    # Joindre les données de Kafka avec les données des stations pour obtenir les codes postaux
    joined_df = kafka_df.join(station_info_df, kafka_df["stationCode"] == station_info_df["stationCode"], "inner")

    # Calculer les indicateurs par code postal
    indicators_df = (joined_df
                     .groupBy("postcode")
                     .agg(pysqlf.sum("num_bikes_available").alias("total_bikes"),
                          pysqlf.sum("num_bikes_available").alias("total_mechanical_bikes"),
                          pysqlf.sum("numBikesAvailable").alias("total_electric_bikes"))
                     .withColumn("timestamp", pysqlf.current_timestamp())
                     .select("timestamp", "postcode", "total_bikes", "total_mechanical_bikes", "total_electric_bikes")
                     )

    # Afficher les indicateurs en streaming dans la console
    query = (indicators_df
             .writeStream
             .outputMode("update")
             .format("console")
             .start()
             )

    query.awaitTermination()
