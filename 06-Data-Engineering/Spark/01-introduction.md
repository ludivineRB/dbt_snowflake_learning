# 01 - Introduction à Apache Spark

[🏠 Accueil](README.md) | [02 - Installation et Setup →](02-installation-setup.md)

---

## 1. Qu'est-ce qu'Apache Spark ?

**Apache Spark** est un moteur d'analyse unifié pour le traitement de données à grande échelle, avec des modules intégrés pour le streaming, SQL, le machine learning et le traitement de graphes.

### Caractéristiques principales

**Vitesse**
- Traitement en mémoire (RAM) plutôt que disque
- Jusqu'à 100x plus rapide que Hadoop MapReduce

**Facilité d'utilisation**
- APIs dans plusieurs langages : Python, Scala, Java, R, SQL
- API haut niveau (DataFrame) similaire à Pandas/SQL

**Évolutivité**
- Du laptop (mode local) aux clusters de milliers de machines
- Support de multiples gestionnaires de cluster (YARN, Kubernetes, Mesos)

## 2. Architecture de Spark

### Composants principaux

**Driver Program**
- Point d'entrée de l'application Spark
- Crée le SparkContext/SparkSession
- Distribue les tâches aux executors

**Cluster Manager**
- Alloue les ressources (CPU, mémoire)
- Types : Standalone, YARN, Kubernetes

**Executors**
- Processus qui exécutent les tâches
- Stockent les données en cache
- Retournent les résultats au driver

## 3. Concepts clés

### RDD (Resilient Distributed Dataset)
API de bas niveau, collection distribuée immuable.

### DataFrame
API haut niveau, optimisée, similaire à Pandas ou table SQL.

### Lazy Evaluation
Les transformations ne sont pas exécutées immédiatement. Spark ne calcule que quand une action est appelée.

---

[🏠 Accueil](README.md) | [02 - Installation et Setup →](02-installation-setup.md)
