# 05 - Spark SQL

[← 04 - DataFrames](04-dataframes-api.md) | [🏠 Accueil](README.md) | [06 - ETL Pipelines →](06-etl-pipelines.md)

---

## 1. Catalog et Tables

**Spark SQL** permet d'utiliser SQL sur des données structurées.

```python
# Créer une temporary view
df.createOrReplaceTempView("users")

# Utiliser SQL
result = spark.sql("SELECT * FROM users WHERE age > 25")
```

## 2. Window Functions

Effectuent des calculs sur une fenêtre de lignes.

```sql
SELECT
    name,
    salary,
    RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rank
FROM employees;
```

## 3. User Defined Functions (UDF)

```python
@udf(returnType=StringType())
def upper_case(s):
    return s.upper() if s else None
```

---

[← 04 - DataFrames](04-dataframes-api.md) | [🏠 Accueil](README.md) | [06 - ETL Pipelines →](06-etl-pipelines.md)
