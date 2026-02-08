# 06 - ETL Pipelines

[← 05 - Spark SQL](05-spark-sql.md) | [🏠 Accueil](README.md) | [07 - Optimisation →](07-performance-optimization.md)

---

## 1. Extract (Lecture)

```python
df = spark.read.parquet("s3://bucket/data.parquet")
```

## 2. Transform (Nettoyage et Enrichissement)

- `dropna()`, `fillna()`
- `dropDuplicates()`
- Joins pour enrichissement.

## 3. Load (Écriture)

```python
# Parquet partitionné
df.write 
    .mode("overwrite") 
    .partitionBy("year", "month") 
    .parquet("output/data")
```

## 4. Formats recommandés
- **Parquet** : Analytics, Data Lake (columnar).
- **Avro** : Streaming, évolution de schéma.

---

[← 05 - Spark SQL](05-spark-sql.md) | [🏠 Accueil](README.md) | [07 - Optimisation →](07-performance-optimization.md)
