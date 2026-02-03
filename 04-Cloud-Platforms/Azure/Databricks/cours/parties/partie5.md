## 🎯 Objectifs d'apprentissage

- Comprendre Delta Lake et ses avantages
- Créer et manipuler des tables Delta
- Utiliser les transactions ACID sur les données
- Exploiter le Time Travel pour l'audit et le rollback
- Optimiser et maintenir les tables Delta
- Implémenter le streaming avec Delta Lake

## 1. Introduction à Delta Lake

Delta Lake est une **couche de stockage open source** qui apporte la fiabilité des bases de données aux data lakes. C'est le fondement de l'architecture Lakehouse de Databricks.

### Problèmes des Data Lakes traditionnels

| Problème | Impact | Solution Delta Lake |
| --- | --- | --- |
| Pas de transactions ACID | Données corrompues lors d'écritures concurrentes | ✅ ACID complet |
| Lectures incohérentes | Résultats différents selon le timing | ✅ Isolation des transactions |
| Pas d'historique | Impossible de revenir en arrière | ✅ Time Travel |
| Difficile à maintenir | Petits fichiers, performances dégradées | ✅ OPTIMIZE et Z-ORDER |
| Pas de schéma enforcement | Données invalides insérées | ✅ Schema enforcement & evolution |

### Architecture Delta Lake

```bash
┌─────────────────────────────────────────────────────────────┐
│                    DELTA LAKE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            Transaction Log (_delta_log/)             │    │
│  │  • JSON files with change history                    │    │
│  │  • Versioning and ACID guarantees                    │    │
│  │  • Checkpoint files for performance                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                            │                                  │
│                            ▼                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Data Files (Parquet)                    │    │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐    │    │
│  │  │ part-1 │  │ part-2 │  │ part-3 │  │ part-4 │    │    │
│  │  │.parquet│  │.parquet│  │.parquet│  │.parquet│    │    │
│  │  └────────┘  └────────┘  └────────┘  └────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 2. Créer et manipuler des tables Delta

### Création d'une table Delta

```bash
# Méthode 1 : Depuis un DataFrame
from pyspark.sql.functions import *

data = [
    ("2024-01-01", "ProductA", 100, 1500.0),
    ("2024-01-01", "ProductB", 50, 750.0),
    ("2024-01-02", "ProductA", 120, 1800.0)
]

df = spark.createDataFrame(data, ["date", "product", "quantity", "revenue"])

# Écrire en format Delta
df.write.format("delta").mode("overwrite").save("/mnt/delta/sales")

# Méthode 2 : Créer une table managée
df.write.format("delta").mode("overwrite").saveAsTable("sales")

# Méthode 3 : Avec SQL
spark.sql("""
    CREATE TABLE IF NOT EXISTS sales_delta (
        date DATE,
        product STRING,
        quantity INT,
        revenue DOUBLE
    )
    USING DELTA
    LOCATION '/mnt/delta/sales'
""")
```

### Opérations CRUD

```bash
from delta.tables import DeltaTable

# Référence à une table Delta
delta_table = DeltaTable.forPath(spark, "/mnt/delta/sales")

# INSERT : Ajouter des données
new_data = spark.createDataFrame([
    ("2024-01-03", "ProductA", 150, 2250.0),
    ("2024-01-03", "ProductC", 80, 1200.0)
], ["date", "product", "quantity", "revenue"])

new_data.write.format("delta").mode("append").save("/mnt/delta/sales")

# UPDATE : Mettre à jour des lignes
delta_table.update(
    condition="product = 'ProductA'",
    set={"revenue": "revenue * 1.1"}  # Augmentation de 10%
)

# DELETE : Supprimer des lignes
delta_table.delete("quantity < 60")

# MERGE (UPSERT) : Insertion ou mise à jour
updates = spark.createDataFrame([
    ("2024-01-03", "ProductA", 200, 3000.0),  # Update si existe
    ("2024-01-04", "ProductD", 90, 1350.0)    # Insert si nouveau
], ["date", "product", "quantity", "revenue"])

delta_table.alias("target").merge(
    updates.alias("source"),
    "target.date = source.date AND target.product = source.product"
).whenMatchedUpdate(
    set={
        "quantity": "source.quantity",
        "revenue": "source.revenue"
    }
).whenNotMatchedInsert(
    values={
        "date": "source.date",
        "product": "source.product",
        "quantity": "source.quantity",
        "revenue": "source.revenue"
    }
).execute()
```

### Opérations avec SQL

```bash
-- UPDATE
UPDATE sales
SET revenue = revenue * 1.1
WHERE product = 'ProductA';

-- DELETE
DELETE FROM sales
WHERE quantity < 60;

-- MERGE (UPSERT)
MERGE INTO sales AS target
USING updates AS source
ON target.date = source.date AND target.product = source.product
WHEN MATCHED THEN
  UPDATE SET
    target.quantity = source.quantity,
    target.revenue = source.revenue
WHEN NOT MATCHED THEN
  INSERT (date, product, quantity, revenue)
  VALUES (source.date, source.product, source.quantity, source.revenue);
```

## 3. Time Travel

Delta Lake conserve l'historique complet des modifications, permettant de voyager dans le temps pour auditer ou restaurer des données.

```bash
# Lire une version spécifique
df_v0 = spark.read.format("delta").option("versionAsOf", 0).load("/mnt/delta/sales")
df_v5 = spark.read.format("delta").option("versionAsOf", 5).load("/mnt/delta/sales")

# Lire à une date spécifique
df_yesterday = spark.read.format("delta") \
    .option("timestampAsOf", "2024-01-15") \
    .load("/mnt/delta/sales")

# Voir l'historique des versions
delta_table = DeltaTable.forPath(spark, "/mnt/delta/sales")
display(delta_table.history())

# Informations affichées :
# - version
# - timestamp
# - operation (WRITE, UPDATE, DELETE, MERGE)
# - operationParameters
# - readVersion, isolationLevel
```

```bash
-- SQL Time Travel
SELECT * FROM sales VERSION AS OF 5;

SELECT * FROM sales TIMESTAMP AS OF '2024-01-15';

-- Voir l'historique
DESCRIBE HISTORY sales;

-- Restaurer une version précédente
RESTORE TABLE sales TO VERSION AS OF 3;

-- Ou à une date
RESTORE TABLE sales TO TIMESTAMP AS OF '2024-01-15';
```

#### Cas d'usage Time Travel

- **Audit :** Voir qui a modifié quoi et quand
- **Rollback :** Revenir à une version stable après une erreur
- **Comparaison :** Analyser l'évolution des données dans le temps
- **Reproducibilité :** Re-exécuter des analyses sur des données historiques

## 4. Optimisation et maintenance

### OPTIMIZE : Compacter les fichiers

Au fil du temps, les écritures créent de nombreux petits fichiers, dégradant les performances de lecture.

```bash
# Compacter les fichiers d'une table
delta_table.optimize().executeCompaction()

# Ou avec SQL
spark.sql("OPTIMIZE sales")

# Optimiser seulement certaines partitions
spark.sql("OPTIMIZE sales WHERE date >= '2024-01-01'")
```

### Z-ORDER : Clustering multi-dimensionnel

Z-ORDER co-localise les données souvent filtrées ensemble, améliorant drastiquement les performances.

```bash
# Z-ORDER sur colonnes fréquemment filtrées
delta_table.optimize().executeZOrderBy("product", "date")

# SQL
spark.sql("OPTIMIZE sales ZORDER BY (product, date)")
```

#### Quand utiliser Z-ORDER ?

Utilisez Z-ORDER sur les colonnes fréquemment utilisées dans les clauses WHERE. Typiquement 2-4 colonnes max.

### VACUUM : Nettoyer les anciens fichiers

VACUUM supprime les fichiers de données obsolètes (marqués comme supprimés mais physiquement présents).

```bash
# Par défaut, conserve 7 jours d'historique
delta_table.vacuum()

# Conserver 30 jours
delta_table.vacuum(retentionHours=30*24)

# SQL
spark.sql("VACUUM sales")
spark.sql("VACUUM sales RETAIN 720 HOURS")  # 30 jours

# Mode DRY RUN pour voir ce qui serait supprimé
spark.sql("VACUUM sales DRY RUN")
```

#### Attention avec VACUUM

Une fois VACUUM exécuté, le Time Travel avant la période de rétention ne fonctionnera plus. Assurez-vous de ne pas avoir besoin de ces versions !

### Auto Optimize (Databricks)

```bash
-- Activer l'optimisation automatique
ALTER TABLE sales SET TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
);

-- optimizeWrite : Combine petits fichiers lors de l'écriture
-- autoCompact : Compacte automatiquement après écritures
```

## 5. Schema Management

### Schema Enforcement

```bash
# Delta Lake valide automatiquement le schéma
bad_data = spark.createDataFrame([
    ("2024-01-05", "ProductE", "invalid", 1500.0)  # quantity doit être INT
], ["date", "product", "quantity", "revenue"])

# Ceci échouera avec AnalysisException
try:
    bad_data.write.format("delta").mode("append").save("/mnt/delta/sales")
except Exception as e:
    print(f"Erreur : {e}")
```

### Schema Evolution

```bash
# Ajouter de nouvelles colonnes automatiquement
new_schema_data = spark.createDataFrame([
    ("2024-01-05", "ProductE", 100, 1500.0, "France")
], ["date", "product", "quantity", "revenue", "country"])

# Activer l'évolution du schéma
new_schema_data.write \
    .format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .save("/mnt/delta/sales")

# Ou définir comme propriété de table
spark.sql("""
    ALTER TABLE sales SET TBLPROPERTIES (
        'delta.autoMerge.mergeSchema' = 'true'
    )
""")
```

### Modifier le schéma

```bash
-- Ajouter une colonne
ALTER TABLE sales ADD COLUMN region STRING;

-- Renommer une colonne
ALTER TABLE sales RENAME COLUMN product TO product_name;

-- Modifier le type (si compatible)
ALTER TABLE sales ALTER COLUMN quantity TYPE BIGINT;

-- Modifier un commentaire
ALTER TABLE sales ALTER COLUMN revenue COMMENT 'Revenue in EUR';
```

## 6. Streaming avec Delta Lake

Delta Lake est parfait pour le streaming grâce à son support des lectures et écritures continues.

### Écriture en streaming

```bash
# Source de streaming (exemple : Kafka, Event Hubs)
stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sales-topic") \
    .load()

# Parser les données JSON
from pyspark.sql.types import *

schema = StructType([
    StructField("date", StringType()),
    StructField("product", StringType()),
    StructField("quantity", IntegerType()),
    StructField("revenue", DoubleType())
])

parsed_stream = stream_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Écrire en Delta en mode streaming
query = parsed_stream.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/checkpoints/sales") \
    .start("/mnt/delta/sales_stream")

query.awaitTermination()
```

### Lecture en streaming

```bash
# Lire une table Delta en mode streaming
stream_read = spark.readStream \
    .format("delta") \
    .load("/mnt/delta/sales_stream")

# Agrégations en temps réel
real_time_stats = stream_read \
    .groupBy(
        window(col("timestamp"), "10 minutes"),
        col("product")
    ).agg(
        sum("revenue").alias("total_revenue"),
        count("*").alias("transaction_count")
    )

# Afficher les résultats
query = real_time_stats.writeStream \
    .format("console") \
    .outputMode("update") \
    .start()
```

### Change Data Feed (CDC)

```bash
-- Activer Change Data Feed
ALTER TABLE sales SET TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true'
);
```

```bash
# Lire les changements depuis une version
changes_df = spark.read \
    .format("delta") \
    .option("readChangeData", "true") \
    .option("startingVersion", 5) \
    .load("/mnt/delta/sales")

# Colonnes ajoutées : _change_type, _commit_version, _commit_timestamp
# _change_type : insert, update_preimage, update_postimage, delete
display(changes_df)

# Utiliser en streaming pour capturer les changements en temps réel
change_stream = spark.readStream \
    .format("delta") \
    .option("readChangeData", "true") \
    .option("startingVersion", 10) \
    .load("/mnt/delta/sales")
```

## 7. Bonnes pratiques Delta Lake

#### Partitionnement

- Partitionner par date/région pour filtres fréquents
- Éviter trop de partitions (<1000)
- Chaque partition : minimum 1 GB de données

#### Optimisation

- OPTIMIZE régulièrement (daily/weekly)
- Z-ORDER sur colonnes de filtre
- Auto Optimize activé en production

#### Maintenance

- VACUUM après rétention appropriée
- Monitor la taille du transaction log
- Checkpoints automatiques (tous les 10 commits)

#### Sécurité

- Activer audit logs
- Utiliser table ACLs
- Change Data Feed pour compliance

### 📌 Points clés à retenir

- Delta Lake apporte ACID, Time Travel et performance aux data lakes
- Transactions ACID garantissent la cohérence des données
- Time Travel permet audit, rollback et reproducibilité
- OPTIMIZE et Z-ORDER améliorent drastiquement les performances
- VACUUM nettoie les fichiers mais supprime l'historique ancien
- Schema enforcement + evolution = données fiables et flexibles
- Parfaitement adapté au streaming avec checkpointing et exactly-once

#### Prochaine étape

Vous maîtrisez Delta Lake ! Dans la **Partie 6**, apprenez à orchestrer vos pipelines avec Databricks Workflows.