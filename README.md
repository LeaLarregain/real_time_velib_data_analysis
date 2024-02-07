# Projet de Traitement de Données Temps Réel avec Kafka et Spark Streaming

## Description

Ce projet vise à concevoir et mettre en œuvre une pipeline de récupération et de traitement de données en temps réel pour les stations Vélib' à Paris et dans la métropole voisine. La solution utilise Apache Kafka pour la collecte initiale des données et Apache Spark Streaming pour le traitement, produisant des indicateurs spécifiques.

## Objectifs

- Collecter en temps réel les données des stations Vélib'.
- Filtrer, traiter et agréger les données pour générer des indicateurs spécifiques.
- Utiliser Apache Kafka comme système de messagerie pour la collecte initiale des données.
- Appliquer Apache Spark Streaming pour le traitement des données en temps réel.

## Configuration Requise

- Apache Kafka
- Apache Spark
- Python 3.x

Avant de commencer, assurez-vous d'avoir Apache Kafka et Apache Spark installés et configurés sur votre machine.

## Création des topics Kafka

1.**Lancement de Zookeeper**

Dans un terminal bash, exécuter la commande suivante (en remplaçant `.` par le chemin réel vers le dossier contenant votre installation Kafka):
```bash
./kafka_2.12-2.6.0/bin/zookeeper-server-start.sh ./kafka_2.12-2.6.0/config/zookeeper.properties
```

2.**Lancement de Apache Kafka**

Ouvrez un nouveau terminal bash, exécuter les deux commandes suivantes (en remplaçant `.` par le chemin réel vers le dossier contenant votre installation Kafka):
```bash
./kafka_2.12-2.6.0/bin/kafka-server-start.sh ./kafka_2.12-2.6.0/config/server.properties
```

3.**Création des deux Topics**

Ouvrez de nouveau un nouveau terminal et exécutez les commandes suivantes pour créer les topics nécessaires :
```bash
./kafka_2.12-2.6.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --
partitions 1 --topic velib-projet
./kafka_2.12-2.6.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --
partitions 1 --topic velib-projet-final-data
```

4.**Vérification des Topics**

Pour vérifier que les topics ont été créés avec succès, utilisez la commande suivante :
```bash
./kafka_2.12-2.6.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```
Vous devriez voir les noms des topics `velib-projet` et `velib-projet-final-data` répertoriés.

## Producer de données vélib pour Apache Kafka

Ce script Python se connecte à une API de données vélib, filtre les informations pour sélectionner uniquement les données de deux stations spécifiques, puis envoie ces données vers un topic Apache Kafka.

Avant d'exécuter ce script, assurez-vous d'avoir installé la bibliothèque kafka-python en utilisant la commande suivante :

```bash
pip install kafka-python
```

Tapez ensuite la commande suivante dans le terminal pour envoyer les données filtrées vers le topic Kafka `velib-projet` pour la collecte.
```bash
python producer.py
```
Le script va récupérer les données vélib en temps réel à partir de l'API, filtrer les informations pour les stations spécifiques 16107 et 32017, puis les envoyer au topic Kafka `velib-projet`.

## Traitement des Données avec Spark Streaming

Ce script Python utilise Apache Spark pour effectuer un traitement en temps réel des données vélib. Il lit les données à partir d'un topic Kafka contenant des informations sur les stations vélib, ainsi que des données supplémentaires provenant d'un fichier CSV. En fusionnant ces deux sources de données, il calcule des indicateurs essentiels, tels que le nombre de vélos disponibles par code postal.

La combinaison des données en temps réel du topic Kafka avec les données statiques du fichier CSV permet d'enrichir les informations sur les stations vélib. Par exemple, les données du fichier CSV peuvent contenir des détails comme les codes postaux des stations, ce qui est essentiel pour analyser la répartition des vélos disponibles dans différentes zones géographiques.

```python
# Charger les données du fichier CSV des stations
station_info_df = spark \
    .read \
    .csv("stations_information.csv", header=True)

# Joindre les données de Kafka avec les données des stations pour obtenir les codes postaux
joined_df = kafka_df.join(station_info_df, kafka_df["stationCode"] == station_info_df["stationCode"], "inner")
```
Pour exécuter le script, utilisez la commande suivante :

```bash
python consumer.py
```

Le script Spark va lire les données vélib en temps réel à partir du topic Kafka `velib-projet`, les traiter pour calculer des indicateurs, et afficher les résultats en streaming dans la console. De plus, il envoie les résultats vers le topic Kafka `velib-projet-final-data` pour un traitement ultérieur.


----------------------------------------------------------------------------------------------------------------------------------
<font color="#62B3F5" size="15"><b><i>ENGLISH VERSION</i></b></font>


# Real-Time Data Processing Project with Kafka and Spark Streaming

## Description

This project aims to design and implement a real-time data retrieval and processing pipeline for Vélib' stations in Paris and the neighboring metropolis. The solution uses Apache Kafka for initial data collection and Apache Spark Streaming for processing, producing specific indicators.

## Objectives
- Collect real-time data from Vélib' stations.
- Filter, process, and aggregate data to generate specific indicators.
- Use Apache Kafka as a messaging system for initial data collection.
- Apply Apache Spark Streaming for real-time data processing.

## Required Setup

- Apache Kafka
- Apache Spark
- Python 3.x

Before you begin, make sure to have Apache Kafka and Apache Spark installed and configured on your machine.

## Creating Kafka Topics

1.**Launching Zookeeper**

In a bash terminal, execute the following command (replacing . with the actual path to the directory containing your Kafka installation):
```bash
./kafka_2.12-2.6.0/bin/zookeeper-server-start.sh ./kafka_2.12-2.6.0/config/zookeeper.properties
```
2.**Launching Apache Kafka**

Open a new bash terminal and execute the following two commands (replacing . with the actual path to the directory containing your Kafka installation):
```bash
./kafka_2.12-2.6.0/bin/kafka-server-start.sh ./kafka_2.12-2.6.0/config/server.properties
```

3.**Creating the Two Topics**

Open another new terminal and execute the following commands to create the necessary topics:
```bash
./kafka_2.12-2.6.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --
partitions 1 --topic velib-projet
./kafka_2.12-2.6.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --
partitions 1 --topic velib-projet-final-data
```

4.**Verifying the Topics**

To verify that the topics have been successfully created, use the following command:
```bash
./kafka_2.12-2.6.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```
You should see the names of the `velib-projet` and `velib-projet-final-data` topics listed.

## Vélib' Data Producer for Apache Kafka

This Python script connects to a Vélib' data API, filters the information to select only data from two specific stations, and then sends this data to an Apache Kafka topic.
```bash
python producer.py
```
The script retrieves real-time Vélib' data from the API, filters it for the specific stations 16107 and 32017, and then sends it to the Kafka topic `velib-projet` for collection.

## Data Processing with Spark Streaming

This Python script leverages Apache Spark to perform real-time processing of Velib data. It reads data from a Kafka topic containing information about Velib stations, as well as additional data from a CSV file. By merging these two data sources, it calculates essential indicators, such as the number of available bikes per postal code.

Combining real-time data from the Kafka topic with static data from the CSV file enriches the information about Velib stations. For example, the CSV file data may contain details such as station postal codes, which are essential for analyzing the distribution of available bikes across different geographic areas.

```python
# Charger les données du fichier CSV des stations
station_info_df = spark \
    .read \
    .csv("stations_information.csv", header=True)

# Joindre les données de Kafka avec les données des stations pour obtenir les codes postaux
joined_df = kafka_df.join(station_info_df, kafka_df["stationCode"] == station_info_df["stationCode"], "inner")
```
To execute the script, use the following command:

```bash
python consumer.py
```
The Spark script reads Velib data in real-time from the Kafka topic `velib-projet`, processes it to calculate indicators, and displays the results in streaming on the console. Additionally, it sends the results to the Kafka topic `velib-projet-final-data` for further processing.