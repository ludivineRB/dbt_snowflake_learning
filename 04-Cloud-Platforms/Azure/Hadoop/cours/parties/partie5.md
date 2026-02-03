## 🎯 Objectifs d'Apprentissage

- Découvrir Apache Hive pour requêter avec SQL
- Utiliser Apache Pig pour le scripting de données
- Comprendre HBase comme base NoSQL
- Maîtriser Sqoop pour l'import/export de données
- Explorer Flume pour la collecte de logs

## 🗺️ 1. Vue d'Ensemble de l'Écosystème

```bash
┌─────────────────────────────────────────────────────────────┐
│                  ÉCOSYSTÈME HADOOP                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INGESTION          STOCKAGE        TRAITEMENT    ANALYSE  │
│  ──────────         ────────        ──────────    ──────   │
│  Flume              HDFS            MapReduce     Hive     │
│  Sqoop              HBase           Spark         Pig      │
│  Kafka                              Tez           Impala   │
│                                                             │
│  ORCHESTRATION      COORDINATION    MONITORING             │
│  ──────────────     ────────────    ──────────             │
│  Oozie              ZooKeeper       Ambari                 │
│                                     Ganglia                │
└─────────────────────────────────────────────────────────────┘
```

| Outil | Catégorie | Description |
| --- | --- | --- |
| **Hive** | SQL/Analyse | Entrepôt de données avec interface SQL (HiveQL) |
| **Pig** | Scripting | Langage de haut niveau pour flux de données |
| **HBase** | Base NoSQL | Base de données distribuée orientée colonnes |
| **Sqoop** | Import/Export | Transfert entre Hadoop et SGBD relationnels |
| **Flume** | Ingestion | Collecte et agrégation de logs streaming |
| **Oozie** | Orchestration | Planificateur de workflows Hadoop |
| **ZooKeeper** | Coordination | Service de coordination distribuée |
| **Spark** | Traitement | Moteur de traitement in-memory rapide |

## 🐝 2. Apache Hive : SQL sur Hadoop

### Qu'est-ce que Hive ?

**Apache Hive** est un entrepôt de données construit sur Hadoop qui permet d'interroger
et d'analyser de grandes quantités de données avec **HiveQL**, un langage similaire à SQL.

#### ✅ Avantages

- Syntaxe SQL familière
- Pas besoin d'écrire du MapReduce
- Support de gros volumes
- Optimiseur de requêtes

#### ❌ Inconvénients

- Latence élevée (batch, pas temps réel)
- Pas de modification en place (INSERT only)
- Pas idéal pour les petites requêtes

### Architecture Hive

```bash
Client (Hive CLI / Beeline / JDBC)
         ↓
    Hive Server 2
         ↓
    Metastore (MySQL/PostgreSQL) ← Stocke les schémas
         ↓
    Driver (Query Compiler, Optimizer, Executor)
         ↓
    Execution Engine (MapReduce / Tez / Spark)
         ↓
    HDFS (Données)
```

### Exemple de Requêtes HiveQL

#### Créer une Table

```bash
CREATE TABLE IF NOT EXISTS employees (
    id INT,
    name STRING,
    department STRING,
    salary DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

#### Charger des Données

```bash
-- Charger depuis un fichier local
LOAD DATA LOCAL INPATH '/tmp/employees.csv' INTO TABLE employees;

-- Charger depuis HDFS
LOAD DATA INPATH '/user/data/employees.csv' INTO TABLE employees;
```

#### Requêtes SELECT

```bash
-- Sélection simple
SELECT * FROM employees WHERE salary > 50000;

-- Agrégation
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING avg_salary > 60000;

-- Jointure
SELECT e.name, d.department_name
FROM employees e
JOIN departments d ON e.department = d.dept_id;
```

#### Partitionnement

```bash
-- Table partitionnée par année
CREATE TABLE logs (
    timestamp STRING,
    level STRING,
    message STRING
)
PARTITIONED BY (year INT, month INT)
STORED AS PARQUET;

-- Insérer dans une partition
INSERT INTO TABLE logs PARTITION (year=2025, month=1)
SELECT timestamp, level, message FROM raw_logs
WHERE year(timestamp) = 2025 AND month(timestamp) = 1;
```

#### Bonnes Pratiques Hive

- Utiliser le partitionnement pour les grandes tables
- Préférer les formats colonnaires (Parquet, ORC) pour les performances
- Utiliser Tez ou Spark au lieu de MapReduce comme moteur
- Analyser les tables pour optimiser les requêtes (`ANALYZE TABLE`)

## 🐷 3. Apache Pig : Scripting de Données

### Qu'est-ce que Pig ?

**Apache Pig** est une plateforme pour analyser de grandes données avec
**Pig Latin**, un langage de haut niveau orienté flux de données.

#### Quand utiliser Pig plutôt que Hive ?

- **Pig :** Transformations complexes, ETL, traitement semi-structuré
- **Hive :** Requêtes SQL classiques, reporting, analyses SQL

### Exemple de Script Pig Latin

#### WordCount en Pig

```bash
-- Charger les données
lines = LOAD '/user/data/input.txt' AS (line:chararray);

-- Découper en mots
words = FOREACH lines GENERATE FLATTEN(TOKENIZE(line)) AS word;

-- Grouper par mot
grouped = GROUP words BY word;

-- Compter
word_counts = FOREACH grouped GENERATE group AS word, COUNT(words) AS count;

-- Trier par compte décroissant
sorted = ORDER word_counts BY count DESC;

-- Stocker le résultat
STORE sorted INTO '/user/data/output' USING PigStorage(',');
```

#### Filtrage et Transformation

```bash
-- Charger les logs
logs = LOAD '/logs/access.log' USING PigStorage(' ')
       AS (ip:chararray, timestamp:chararray, method:chararray,
           url:chararray, status:int, bytes:int);

-- Filtrer les erreurs 404
errors = FILTER logs BY status == 404;

-- Extraire l'IP et l'URL
result = FOREACH errors GENERATE ip, url;

-- Grouper par URL
grouped = GROUP result BY url;

-- Compter les erreurs par URL
error_counts = FOREACH grouped GENERATE group AS url, COUNT(result) AS count;

-- Stocker
STORE error_counts INTO '/output/404_errors';
```

#### Jointure en Pig

```bash
-- Charger deux datasets
users = LOAD '/data/users' AS (user_id:int, name:chararray);
orders = LOAD '/data/orders' AS (order_id:int, user_id:int, amount:double);

-- Jointure
joined = JOIN users BY user_id, orders BY user_id;

-- Stocker
STORE joined INTO '/output/user_orders';
```

### Exécuter un Script Pig

```bash
# Mode local (pour tester)
pig -x local script.pig

# Mode MapReduce
pig -x mapreduce script.pig

# Mode interactif (Grunt shell)
pig
```

## 🗄️ 4. Apache HBase : Base de Données NoSQL

### Qu'est-ce que HBase ?

**Apache HBase** est une base de données NoSQL distribuée, orientée colonnes,
construite sur HDFS. Inspirée de Google BigTable.

### Caractéristiques

#### 📈 Scalabilité

Supporte des milliards de lignes et millions de colonnes

#### ⚡ Accès Rapide

Lecture/écriture en temps réel (millisecondes)

#### 🔑 Clé-Valeur

Accès par clé primaire (row key)

#### 📊 Orienté Colonnes

Stockage en familles de colonnes

### Modèle de Données

```bash
Table
  ├─ Row Key (clé unique)
  └─ Column Families
       ├─ Family 1
       │    ├─ Column 1:1 (avec timestamp)
       │    └─ Column 1:2
       └─ Family 2
            └─ Column 2:1
```

### Commandes HBase Shell

#### Créer et Gérer des Tables

```bash
# Lancer HBase shell
hbase shell

# Créer une table avec deux familles de colonnes
create 'users', 'profile', 'contacts'

# Lister les tables
list

# Décrire une table
describe 'users'

# Désactiver et supprimer une table
disable 'users'
drop 'users'
```

#### Insérer et Lire des Données

```bash
# Insérer des données
put 'users', 'user1', 'profile:name', 'Alice'
put 'users', 'user1', 'profile:age', '30'
put 'users', 'user1', 'contacts:email', 'alice@example.com'

# Lire une ligne
get 'users', 'user1'

# Lire une colonne spécifique
get 'users', 'user1', 'profile:name'

# Scanner toute la table
scan 'users'

# Scanner avec filtre
scan 'users', {FILTER => "ValueFilter(=, 'binary:Alice')"}

# Supprimer une cellule
delete 'users', 'user1', 'profile:age'
```

### Cas d'Usage HBase

| Domaine | Cas d'Usage |
| --- | --- |
| Réseaux Sociaux | Profils utilisateurs, fils d'actualité, messages |
| IoT | Stockage de séries temporelles de capteurs |
| Finance | Historique de transactions en temps réel |
| E-commerce | Catalogue produits, historique des commandes |

## 🔄 5. Apache Sqoop : Import/Export de Données

### Qu'est-ce que Sqoop ?

**Apache Sqoop** (SQL to Hadoop) est un outil pour transférer des données
entre Hadoop et des bases de données relationnelles (MySQL, PostgreSQL, Oracle, etc.).

### Commandes Principales

#### Import depuis SGBD vers HDFS

```bash
# Importer une table entière
sqoop import \
  --connect jdbc:mysql://localhost/mydb \
  --username root \
  --password mypassword \
  --table employees \
  --target-dir /user/hadoop/employees

# Importer avec une requête WHERE
sqoop import \
  --connect jdbc:mysql://localhost/mydb \
  --username root \
  --password mypassword \
  --table employees \
  --where "department = 'IT'" \
  --target-dir /user/hadoop/it_employees

# Importer toutes les tables d'une base
sqoop import-all-tables \
  --connect jdbc:mysql://localhost/mydb \
  --username root \
  --password mypassword \
  --warehouse-dir /user/hadoop/warehouse
```

#### Export depuis HDFS vers SGBD

```bash
# Exporter vers une table MySQL
sqoop export \
  --connect jdbc:mysql://localhost/mydb \
  --username root \
  --password mypassword \
  --table employees_export \
  --export-dir /user/hadoop/employees_processed
```

#### Import Incrémental

```bash
# Import incrémental basé sur une colonne d'ID
sqoop import \
  --connect jdbc:mysql://localhost/mydb \
  --username root \
  --password mypassword \
  --table orders \
  --incremental append \
  --check-column order_id \
  --last-value 1000 \
  --target-dir /user/hadoop/orders
```

#### Import Direct vers Hive

```bash
sqoop import \
  --connect jdbc:mysql://localhost/mydb \
  --username root \
  --password mypassword \
  --table employees \
  --hive-import \
  --hive-table employees \
  --create-hive-table
```

## 📡 6. Apache Flume : Collecte de Logs

### Qu'est-ce que Flume ?

**Apache Flume** est un service distribué pour collecter, agréger et déplacer
efficacement de grandes quantités de données de logs vers HDFS.

### Architecture Flume

```bash
Source → Channel → Sink

Exemples:
- Source : Netcat, Exec, Avro, Kafka
- Channel : Memory, File, JDBC
- Sink : HDFS, HBase, Logger, Avro
```

### Exemple de Configuration

```bash
# flume-conf.properties

# Définir les composants
agent1.sources = source1
agent1.channels = channel1
agent1.sinks = sink1

# Configurer la source (écoute sur un port)
agent1.sources.source1.type = netcat
agent1.sources.source1.bind = localhost
agent1.sources.source1.port = 44444

# Configurer le channel (mémoire)
agent1.channels.channel1.type = memory
agent1.channels.channel1.capacity = 1000
agent1.channels.channel1.transactionCapacity = 100

# Configurer le sink (HDFS)
agent1.sinks.sink1.type = hdfs
agent1.sinks.sink1.hdfs.path = /user/flume/events/%Y-%m-%d
agent1.sinks.sink1.hdfs.fileType = DataStream
agent1.sinks.sink1.hdfs.rollInterval = 60
agent1.sinks.sink1.hdfs.rollSize = 0
agent1.sinks.sink1.hdfs.rollCount = 0

# Relier les composants
agent1.sources.source1.channels = channel1
agent1.sinks.sink1.channel = channel1
```

#### Lancer Flume

```bash
flume-ng agent \
  --conf-file flume-conf.properties \
  --name agent1 \
  -Dflume.root.logger=INFO,console
```

## 📝 Résumé de la Partie 5

### Points Clés à Retenir

- **Hive** : SQL sur Hadoop, idéal pour analyses et reporting
- **Pig** : Scripting pour ETL et transformations complexes
- **HBase** : Base NoSQL temps réel sur HDFS
- **Sqoop** : Import/Export entre Hadoop et SGBD relationnels
- **Flume** : Ingestion de logs en streaming vers HDFS
- L'écosystème Hadoop est riche et chaque outil a son cas d'usage spécifique
- Ces outils peuvent être combinés pour créer des pipelines Big Data complets

#### ✅ Prêt pour la Suite ?

Vous connaissez maintenant l'écosystème Hadoop ! Dans la dernière partie, nous verrons comment **installer et configurer** un cluster Hadoop.