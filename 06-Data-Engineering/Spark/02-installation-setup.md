# 02 - Installation et Setup

[← 01 - Introduction](01-introduction.md) | [🏠 Accueil](README.md) | [03 - RDD Basics →](03-rdd-basics.md)

---

## 1. Options d'installation

| Option | Difficulté | Recommandé pour |
|--------|------------|-----------------|
| **pip install pyspark** | ⭐ | Débutants, prototypage rapide |
| **Docker** | ⭐⭐ | Développement, reproductibilité |
| **Installation manuelle** | ⭐⭐⭐ | Production, personnalisation |
| **Databricks** | ⭐ | Cloud, collaboration |

## 2. Installation locale

### Prérequis
**Java 8 ou 11** (requis) et **Python 3.7+**.

### Option 1 : pip install
```bash
pip install pyspark
```

## 3. Docker (Recommandé)

Utilisation de l'image `bitnami/spark` ou `jupyter/pyspark-notebook`.

## 4. Premier programme Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder 
    .appName("HelloSpark") 
    .master("local[*]") 
    .getOrCreate()

data = [("Alice", 25), ("Bob", 30)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()
```

---

[← 01 - Introduction](01-introduction.md) | [🏠 Accueil](README.md) | [03 - RDD Basics →](03-rdd-basics.md)
