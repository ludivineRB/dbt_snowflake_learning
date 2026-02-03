## 🎯 Objectifs d'apprentissage

- Comprendre l'architecture et les concepts d'Apache Spark
- Maîtriser les DataFrames et Datasets
- Effectuer des transformations et actions sur les données
- Utiliser Spark SQL pour requêter les données
- Optimiser les performances des requêtes

## 1. Architecture Apache Spark

### Concepts fondamentaux

```bash
┌─────────────────────────────────────────────────────────────┐
│                   ARCHITECTURE SPARK                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐                                            │
│  │   Driver     │   (Master Node)                            │
│  │   Program    │   • SparkContext                           │
│  │              │   • Planification des tâches               │
│  └──────┬───────┘   • Distribution du code                   │
│         │                                                     │
│         │                                                     │
│    ┌────▼─────────────────────────────────┐                  │
│    │      Cluster Manager                 │                  │
│    │  (YARN / Mesos / Kubernetes / Local) │                  │
│    └────┬──────────────┬──────────────────┘                  │
│         │              │                                      │
│    ┌────▼────┐    ┌───▼─────┐    ┌─────────┐                │
│    │ Worker  │    │ Worker  │    │ Worker  │                │
│    │ Node 1  │    │ Node 2  │    │ Node 3  │                │
│    │         │    │         │    │         │                │
│    │ ┌─────┐ │    │ ┌─────┐ │    │ ┌─────┐ │                │
│    │ │Task │ │    │ │Task │ │    │ │Task │ │                │
│    │ └─────┘ │    │ └─────┘ │    │ └─────┘ │                │
│    │ ┌─────┐ │    │ ┌─────┐ │    │ ┌─────┐ │                │
│    │ │Task │ │    │ │Task │ │    │ │Task │ │                │
│    │ └─────┘ │    │ └─────┘ │    │ └─────┘ │                │
│    └─────────┘    └─────────┘    └─────────┘                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

| Composant | Rôle | Responsabilités |
| --- | --- | --- |
| **Driver** | Nœud maître | • Exécute le code utilisateur  • Crée le SparkContext  • Planifie les tâches |
| **Cluster Manager** | Gestionnaire de ressources | • Alloue les ressources  • Gère les workers  • Monitore la santé du cluster |
| **Workers** | Nœuds de calcul | • Exécutent les tâches  • Stockent les données en cache  • Renvoient les résultats |
| **Executors** | Processus sur workers | • Exécutent le code  • Gèrent le cache  • Communiquent avec driver |

## 2. DataFrames et Datasets

### Qu'est-ce qu'un DataFrame ?

Un DataFrame est une collection distribuée de données organisée en colonnes nommées, similaire à une table SQL ou un DataFrame pandas, mais optimisé pour le traitement distribué.

### Création de DataFrames

```bash
# 1. Depuis une collection Python
data = [
    ("Alice", 34, "Engineering"),
    ("Bob", 45, "Sales"),
    ("Charlie", 29, "Marketing")
]
df = spark.createDataFrame(data, ["name", "age", "department"])
df.show()

# 2. Depuis un fichier CSV
df_csv = spark.read.csv(
    "/path/to/data.csv",
    header=True,
    inferSchema=True
)

# 3. Depuis un fichier Parquet
df_parquet = spark.read.parquet("/path/to/data.parquet")

# 4. Depuis une table Delta
df_delta = spark.read.format("delta").load("/path/to/delta-table")

# 5. Depuis JSON
df_json = spark.read.json("/path/to/data.json")

# 6. Depuis une requête SQL
df_sql = spark.sql("SELECT * FROM my_table WHERE age > 30")
```

### Schéma des DataFrames

```bash
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Définir un schéma explicitement
schema = StructType([
    StructField("name", StringType(), nullable=False),
    StructField("age", IntegerType(), nullable=True),
    StructField("department", StringType(), nullable=True)
])

# Créer DataFrame avec schéma
df = spark.createDataFrame(data, schema=schema)

# Afficher le schéma
df.printSchema()
# root
#  |-- name: string (nullable = false)
#  |-- age: integer (nullable = true)
#  |-- department: string (nullable = true)

# Obtenir le schéma sous forme de DDL
print(df.schema.simpleString())
```

## 3. Transformations et Actions

Spark utilise deux types d'opérations :

#### Transformations (Lazy)

Créent un nouveau DataFrame sans exécution immédiate

- select(), filter(), groupBy()
- join(), orderBy(), distinct()
- withColumn(), drop()

#### Actions (Eager)

Déclenchent l'exécution et retournent un résultat

- show(), count(), collect()
- take(), first(), head()
- write.save(), foreach()

### Transformations courantes

```bash
from pyspark.sql.functions import col, lit, when, avg, sum, count

# SELECT : Sélectionner des colonnes
df_select = df.select("name", "age")
df_select = df.select(col("name"), col("age") + 1)

# FILTER / WHERE : Filtrer les lignes
df_filtered = df.filter(col("age") > 30)
df_filtered = df.where("age > 30 AND department = 'Engineering'")

# WITH COLUMN : Ajouter ou modifier une colonne
df_with_senior = df.withColumn(
    "is_senior",
    when(col("age") >= 40, lit("Yes")).otherwise(lit("No"))
)

df_with_salary = df.withColumn("estimated_salary", col("age") * 1000)

# DROP : Supprimer des colonnes
df_dropped = df.drop("department")

# DISTINCT : Valeurs uniques
df_unique = df.select("department").distinct()

# ORDER BY : Trier
df_sorted = df.orderBy(col("age").desc())

# LIMIT : Limiter le nombre de lignes
df_limited = df.limit(10)
```

### Agrégations

```bash
from pyspark.sql.functions import avg, sum, count, min, max, stddev

# Agrégations simples
df.select(
    avg("age").alias("avg_age"),
    min("age").alias("min_age"),
    max("age").alias("max_age")
).show()

# GROUP BY
df_grouped = df.groupBy("department").agg(
    count("*").alias("employee_count"),
    avg("age").alias("avg_age"),
    min("age").alias("youngest"),
    max("age").alias("oldest")
)
df_grouped.show()

# Multiple groupBy
df.groupBy("department", "is_senior").agg(
    count("*").alias("count")
).show()
```

### Jointures

```bash
# Créer deux DataFrames
employees = spark.createDataFrame([
    (1, "Alice", "Engineering"),
    (2, "Bob", "Sales"),
    (3, "Charlie", "Engineering")
], ["emp_id", "name", "dept"])

salaries = spark.createDataFrame([
    (1, 95000),
    (2, 85000),
    (3, 78000)
], ["emp_id", "salary"])

# INNER JOIN
df_inner = employees.join(salaries, on="emp_id", how="inner")
df_inner.show()

# LEFT JOIN
df_left = employees.join(salaries, on="emp_id", how="left")

# RIGHT JOIN
df_right = employees.join(salaries, on="emp_id", how="right")

# FULL OUTER JOIN
df_full = employees.join(salaries, on="emp_id", how="outer")

# JOIN avec conditions multiples
departments = spark.createDataFrame([
    ("Engineering", "Building A"),
    ("Sales", "Building B")
], ["dept_name", "location"])

df_complex_join = employees.join(
    departments,
    employees.dept == departments.dept_name,
    how="left"
).drop("dept_name")
df_complex_join.show()
```

## 4. Spark SQL

### Créer des vues temporaires

```bash
# Créer une vue temporaire globale
df.createOrReplaceGlobalTempView("employees_global")

# Créer une vue temporaire locale (session)
df.createOrReplaceTempView("employees")

# Requêter avec SQL
result = spark.sql("""
    SELECT
        department,
        COUNT(*) as employee_count,
        AVG(age) as avg_age,
        MIN(age) as youngest,
        MAX(age) as oldest
    FROM employees
    GROUP BY department
    ORDER BY employee_count DESC
""")
result.show()
```

### Requêtes SQL avancées

```bash
%sql
-- Window functions
SELECT
  name,
  age,
  department,
  AVG(age) OVER (PARTITION BY department) as dept_avg_age,
  RANK() OVER (PARTITION BY department ORDER BY age DESC) as age_rank
FROM employees;

-- CTEs (Common Table Expressions)
WITH dept_stats AS (
  SELECT
    department,
    AVG(age) as avg_age,
    COUNT(*) as emp_count
  FROM employees
  GROUP BY department
)
SELECT
  e.name,
  e.age,
  e.department,
  ds.avg_age,
  ds.emp_count
FROM employees e
JOIN dept_stats ds ON e.department = ds.department
WHERE e.age > ds.avg_age;

-- Sous-requêtes
SELECT *
FROM employees
WHERE age > (SELECT AVG(age) FROM employees);
```

### Fonctions SQL utiles

```bash
from pyspark.sql.functions import *

df_advanced = df.select(
# Fonctions de chaîne
    upper(col("name")).alias("name_upper"),
    lower(col("name")).alias("name_lower"),
    length(col("name")).alias("name_length"),
    concat(col("name"), lit(" - "), col("department")).alias("full_desc"),

# Fonctions de date
    current_date().alias("today"),
    current_timestamp().alias("now"),
    date_add(current_date(), 7).alias("next_week"),

# Fonctions conditionnelles
    when(col("age") >= 40, "Senior")
    .when(col("age") >= 30, "Mid")
    .otherwise("Junior").alias("seniority"),

# Fonctions mathématiques
    round(col("age") / 10, 2).alias("age_decades"),
    abs(col("age") - 35).alias("distance_from_35")
)
df_advanced.show(truncate=False)
```

## 5. Optimisation des performances

### Catalyst Optimizer

Spark utilise Catalyst, un optimiseur de requêtes qui réorganise automatiquement vos opérations pour de meilleures performances.

```bash
# Voir le plan d'exécution logique
df.explain(mode="simple")

# Plan d'exécution détaillé
df.explain(mode="extended")

# Plan d'exécution formaté
df.explain(mode="formatted")

# Coût estimé
df.explain(mode="cost")
```

### Partitionnement

```bash
# Vérifier le nombre de partitions
print(f"Nombre de partitions : {df.rdd.getNumPartitions()}")

# Repartitionner (shuffle)
df_repartitioned = df.repartition(10)
df_by_dept = df.repartition(10, "department")

# Coalesce (pas de shuffle, réduction uniquement)
df_coalesced = df.coalesce(5)

# Optimal : partition par colonne fréquemment filtrée
df_optimized = df.repartition("department")
```

### Mise en cache

```bash
# Cache en mémoire
df.cache()  # ou df.persist()

# Utiliser le DataFrame mis en cache
df.count()  # Premier accès : calcul et mise en cache
df.filter(col("age") > 30).count()  # Réutilise le cache

# Retirer du cache
df.unpersist()

# Cache avec niveau de stockage personnalisé
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)
```

### Bonnes pratiques d'optimisation

#### Filtrage précoce

Filtrez les données le plus tôt possible pour réduire le volume traité

```bash
# Bon
df.filter(col("age") > 30) \
  .select("name", "dept") \
  .groupBy("dept").count()

# Moins bon
df.groupBy("dept").count() \
  .filter(col("count") > 10)
```

#### Éviter collect()

collect() ramène toutes les données au driver, risque d'OutOfMemory

```bash
# Dangereux sur big data
# all_data = df.collect()

# Préférer
df.show(20)
df.take(10)
df.limit(100).toPandas()
```

#### Broadcast Join

Pour joindre une petite table avec une grande

```bash
from pyspark.sql.functions import broadcast

# Broadcast automatique si < 10MB
df_large.join(
    broadcast(df_small),
    on="key"
)
```

#### Adaptive Query Execution

Active par défaut dans Spark 3.x, optimise dynamiquement

```bash
spark.conf.set(
  "spark.sql.adaptive.enabled",
  "true"
)
```

#### Fonctionnalités spécifiques Databricks

- **Photon Engine :** Moteur vectorisé C++ jusqu'à 4x plus rapide (Premium tier)
- **Auto Optimize :** Optimisation automatique des tables Delta
- **Adaptive Query Execution :** Activé par défaut
- **Dynamic File Pruning :** Réduit les fichiers lus lors des jointures

## 6. Exemple pratique complet

```bash
# Scénario : Analyse de ventes e-commerce

# 1. Charger les données
orders = spark.read.parquet("/mnt/data/orders/")
customers = spark.read.parquet("/mnt/data/customers/")
products = spark.read.parquet("/mnt/data/products/")

# 2. Créer des vues pour SQL
orders.createOrReplaceTempView("orders")
customers.createOrReplaceTempView("customers")
products.createOrReplaceTempView("products")

# 3. Analyse avec PySpark
from pyspark.sql.functions import *

# Jointure enrichie
enriched_orders = orders \
    .join(customers, on="customer_id", how="left") \
    .join(products, on="product_id", how="left") \
    .withColumn("order_date", to_date(col("timestamp"))) \
    .withColumn("revenue", col("quantity") * col("unit_price"))

# Agrégation par produit et mois
monthly_sales = enriched_orders \
    .withColumn("month", date_trunc("month", col("order_date"))) \
    .groupBy("month", "product_name", "category") \
    .agg(
        sum("revenue").alias("total_revenue"),
        sum("quantity").alias("total_quantity"),
        count("order_id").alias("order_count"),
        countDistinct("customer_id").alias("unique_customers")
    ) \
    .orderBy(col("month").desc(), col("total_revenue").desc())

# 4. Ou avec SQL
result = spark.sql("""
    SELECT
        DATE_TRUNC('month', o.order_date) as month,
        p.product_name,
        p.category,
        SUM(o.quantity * o.unit_price) as total_revenue,
        SUM(o.quantity) as total_quantity,
        COUNT(o.order_id) as order_count,
        COUNT(DISTINCT o.customer_id) as unique_customers
    FROM orders o
    LEFT JOIN products p ON o.product_id = p.product_id
    GROUP BY month, p.product_name, p.category
    ORDER BY month DESC, total_revenue DESC
""")

# 5. Sauvegarder les résultats
result.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("month") \
    .save("/mnt/analytics/monthly_sales")

# 6. Afficher les insights
display(result.limit(20))
```

### 📌 Points clés à retenir

- Spark distribue le calcul sur plusieurs nœuds (Driver + Workers)
- DataFrames sont des collections distribuées avec schéma
- Transformations (lazy) vs Actions (eager) - comprenez la différence
- Spark SQL permet de requêter avec syntaxe SQL standard
- Catalyst optimizer optimise automatiquement vos requêtes
- Cache les DataFrames réutilisés, partitionnez intelligemment
- Évitez collect() sur de gros volumes, privilégiez show()/take()

#### Prochaine étape

Vous maîtrisez Spark ! Dans la **Partie 5**, découvrez Delta Lake pour des données fiables et performantes.