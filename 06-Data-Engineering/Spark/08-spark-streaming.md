# 08 - Spark Streaming

[← 07 - Optimisation](07-performance-optimization.md) | [🏠 Accueil](README.md) | [09 - Sujets avancés →](09-advanced-topics.md)

---

## 1. Structured Streaming

Permet de traiter des flux de données en temps réel avec la même API que le batch.

```python
# Lire depuis Kafka
df = spark.readStream 
    .format("kafka") 
    .option("subscribe", "topic1") 
    .load()
```

## 2. Windowing

```python
# Fenêtres de 10 minutes
windowed_counts = df 
    .groupBy(window(col("timestamp"), "10 minutes")) 
    .count()
```

## 3. Checkpointing

Indispensable pour la tolérance aux pannes.

```python
query = df.writeStream 
    .format("parquet") 
    .option("checkpointLocation", "/checkpoint/") 
    .start("/output/")
```

---

[← 07 - Optimisation](07-performance-optimization.md) | [🏠 Accueil](README.md) | [09 - Sujets avancés →](09-advanced-topics.md)
