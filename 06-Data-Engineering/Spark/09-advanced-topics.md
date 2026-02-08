# 09 - Sujets avancés

[← 08 - Streaming](08-spark-streaming.md) | [🏠 Accueil](README.md) | [10 - Production →](10-production-deployment.md)

---

## 1. Machine Learning avec MLlib

```python
from pyspark.ml.classification import RandomForestClassifier
rf = RandomForestClassifier(labelCol="label")
model = rf.fit(training_data)
```

## 2. Delta Lake

Ajoute des transactions ACID sur Data Lakes.

```python
# Écrire en Delta
df.write.format("delta").save("/data/delta-table")

# Time Travel
df = spark.read.format("delta").option("versionAsOf", 5).load("/path")
```

## 3. Pandas UDF

Utilise Apache Arrow pour des performances 10-100x plus rapides que les UDF standards.

---

[← 08 - Streaming](08-spark-streaming.md) | [🏠 Accueil](README.md) | [10 - Production →](10-production-deployment.md)
