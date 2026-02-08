# 04 - DataFrames API

[← 03 - RDD Basics](03-rdd-basics.md) | [🏠 Accueil](README.md) | [05 - Spark SQL →](05-spark-sql.md)

---

## 1. Introduction aux DataFrames

Un **DataFrame** est une collection distribuée de données organisées en colonnes nommées.

## 2. Création de DataFrames

```python
# Depuis CSV
df = spark.read.csv("data.csv", header=True, inferSchema=True)

# Depuis Parquet
df = spark.read.parquet("data.parquet")
```

## 3. Sélection et Filtrage

```python
df.select("name", "age").filter(col("age") > 25).show()
```

## 4. Agrégations

```python
df.groupBy("city").agg(avg("age").alias("avg_age")).show()
```

## 5. Joins

```python
result = df1.join(df2, "id", "inner")
```

---

[← 03 - RDD Basics](03-rdd-basics.md) | [🏠 Accueil](README.md) | [05 - Spark SQL →](05-spark-sql.md)
