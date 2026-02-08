# 07 - Optimisation des performances

[← 06 - ETL Pipelines](06-etl-pipelines.md) | [🏠 Accueil](README.md) | [08 - Spark Streaming →](08-spark-streaming.md)

---

## 1. Partitionnement

```python
# Repartitionner (shuffle)
df = df.repartition(100)

# Coalesce (réduction sans shuffle)
df = df.coalesce(10)
```

## 2. Caching

```python
df.cache() # En mémoire
df.persist(StorageLevel.MEMORY_AND_DISK)
```

## 3. Broadcast Join

Pour les petites tables jointes à des grandes.

```python
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "id")
```

## 4. Adaptive Query Execution (AQE)
Active par défaut dans Spark 3.x, optimise dynamiquement les partitions après shuffle.

---

[← 06 - ETL Pipelines](06-etl-pipelines.md) | [🏠 Accueil](README.md) | [08 - Spark Streaming →](08-spark-streaming.md)
