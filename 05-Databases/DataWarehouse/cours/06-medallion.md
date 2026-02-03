# Module 06 - Architecture Medallion

## Concept

L'architecture **Medallion** (Bronze/Silver/Gold) est un pattern de design pour organiser les données en couches progressives de qualité.

```
┌──────────────────────────────────────────────────────────┐
│                       GOLD Layer                          │
│                (Business & Analytics Ready)               │
│                                                           │
│  • Données agrégées                                      │
│  • Métriques business                                    │
│  • Hautement curées                                      │
│  • Optimisées pour la consommation                       │
└───────────────────────┬──────────────────────────────────┘
                        ↑
┌───────────────────────┴──────────────────────────────────┐
│                     SILVER Layer                          │
│                  (Cleaned & Conformed)                    │
│                                                           │
│  • Données validées                                      │
│  • Dédoublonnées                                         │
│  • Standardisées                                         │
│  • Qualité contrôlée                                     │
└───────────────────────┬──────────────────────────────────┘
                        ↑
┌───────────────────────┴──────────────────────────────────┐
│                     BRONZE Layer                          │
│                      (Raw Data)                           │
│                                                           │
│  • Données brutes (as-is)                                │
│  • Transformation minimale                               │
│  • Archive historique                                    │
│  • Immutable                                             │
└───────────────────────┬──────────────────────────────────┘
                        ↑
                   Data Sources
```

## Pourquoi cette architecture ?

### Problèmes résolus

| Problème | Solution Medallion |
|----------|-------------------|
| Données corrompues | Bronze conserve l'original |
| Traçabilité | Lineage clair entre couches |
| Qualité variable | Silver applique les règles |
| Performance BI | Gold optimisé pour requêtes |
| Coût | Bronze stockage économique |

### Bénéfices

- **Reproductibilité** : Reprocesser depuis Bronze
- **Debuggabilité** : Identifier où l'erreur survient
- **Gouvernance** : Permissions par couche
- **Agilité** : Ajouter de nouvelles transformations

## Bronze Layer (Raw)

### Objectif

Ingestion des données **brutes**, sans transformation, pour archivage historique complet.

### Caractéristiques

```
┌─────────────────────────────────────────────────────────┐
│                     BRONZE LAYER                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✓ Données "as-is" de la source                         │
│  ✓ Format : Parquet, Delta, JSON original               │
│  ✓ Aucune transformation business                       │
│  ✓ Append-only (immutable)                              │
│  ✓ Metadata : timestamp ingestion, source               │
│  ✓ Rétention longue (années)                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Exemples d'implémentation

**BigQuery**
```sql
-- Table Bronze
CREATE TABLE bronze.raw_sales (
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    source_system STRING,
    raw_data STRING  -- JSON brut
)
PARTITION BY DATE(ingestion_timestamp);

-- Ou table structurée avec colonnes sources
CREATE TABLE bronze.sales_raw (
    ingestion_timestamp TIMESTAMP,
    source_file STRING,
    order_id_raw STRING,
    amount_raw STRING,  -- Garder le type string original
    date_raw STRING,
    customer_email_raw STRING
);
```

**Snowflake**
```sql
-- Table Bronze
CREATE TABLE bronze.sales_raw (
    _ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR,
    raw_json VARIANT  -- Semi-structured
);

-- Chargement depuis Stage
COPY INTO bronze.sales_raw
FROM @my_stage/sales/
FILE_FORMAT = (TYPE = JSON);
```

## Silver Layer (Cleaned)

### Objectif

Données **nettoyées**, validées, dédupliquées et standardisées.

### Caractéristiques

```
┌─────────────────────────────────────────────────────────┐
│                     SILVER LAYER                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✓ Dédoublonnage                                        │
│  ✓ Types castés (STRING → DATE, INT, etc.)              │
│  ✓ Valeurs normalisées (UPPER, TRIM, etc.)              │
│  ✓ Nulls gérés                                          │
│  ✓ Validation des contraintes                           │
│  ✓ Enrichissement (lookups)                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Transformations typiques

| Transformation | Avant (Bronze) | Après (Silver) |
|----------------|----------------|----------------|
| Cast type | `"2024-01-15"` | `2024-01-15 (DATE)` |
| Normalisation | `"  PARIS  "` | `"Paris"` |
| Dédoublonnage | 3 lignes id=123 | 1 ligne id=123 |
| Nettoyage | `amount = "-5"` | Filtré ou corrigé |
| Enrichissement | `country_code = "FR"` | + `country_name = "France"` |

### Exemple BigQuery

```sql
-- Silver : Transformation depuis Bronze
CREATE OR REPLACE TABLE silver.sales_cleaned AS
SELECT DISTINCT
    -- Clés
    CAST(order_id_raw AS INT64) as order_id,

    -- Dates
    PARSE_DATE('%Y%m%d', date_raw) as order_date,

    -- Montants
    SAFE_CAST(amount_raw AS FLOAT64) as amount,

    -- Normalisation
    LOWER(TRIM(customer_email_raw)) as customer_email,
    UPPER(SUBSTR(customer_email_raw,
        STRPOS(customer_email_raw, '@') + 1)) as email_domain,

    -- Metadata
    CURRENT_TIMESTAMP() as _processed_at

FROM bronze.sales_raw
WHERE
    order_id_raw IS NOT NULL
    AND SAFE_CAST(amount_raw AS FLOAT64) > 0;
```

### Data Quality Checks

```sql
-- Assertions de qualité
SELECT
    COUNT(*) as total_rows,
    COUNT(DISTINCT order_id) as unique_orders,
    SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END) as null_amounts,
    SUM(CASE WHEN amount < 0 THEN 1 ELSE 0 END) as negative_amounts,
    MIN(order_date) as min_date,
    MAX(order_date) as max_date
FROM silver.sales_cleaned;

-- Alerter si anomalie
-- null_amounts > 0 ou negative_amounts > 0 → Investigation
```

## Gold Layer (Business)

### Objectif

Données **agrégées** et optimisées pour la consommation business (BI, ML, Reporting).

### Caractéristiques

```
┌─────────────────────────────────────────────────────────┐
│                      GOLD LAYER                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ✓ Agrégations pré-calculées                            │
│  ✓ Métriques business (KPIs)                            │
│  ✓ Dénormalisé (Star Schema)                            │
│  ✓ Optimisé pour les requêtes BI                        │
│  ✓ Dimensions conformes                                 │
│  ✓ Documentation des calculs                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Exemple BigQuery

```sql
-- Gold : Métriques par région et mois
CREATE OR REPLACE TABLE gold.sales_by_region_monthly AS
SELECT
    -- Dimensions
    DATE_TRUNC(order_date, MONTH) as month,
    c.region,
    c.segment,

    -- Métriques agrégées
    COUNT(DISTINCT s.order_id) as order_count,
    COUNT(DISTINCT s.customer_email) as unique_customers,
    SUM(s.amount) as total_revenue,
    AVG(s.amount) as avg_order_value,

    -- Métriques calculées
    SAFE_DIVIDE(SUM(s.amount), COUNT(DISTINCT s.customer_email))
        as revenue_per_customer,

    -- Metadata
    CURRENT_TIMESTAMP() as _refreshed_at

FROM silver.sales_cleaned s
LEFT JOIN silver.customers c ON s.customer_email = c.email
GROUP BY 1, 2, 3;

-- Gold : Vue Customer 360
CREATE OR REPLACE TABLE gold.customer_360 AS
SELECT
    customer_email,
    MIN(order_date) as first_order_date,
    MAX(order_date) as last_order_date,
    COUNT(*) as total_orders,
    SUM(amount) as lifetime_value,
    AVG(amount) as avg_order_value,
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as days_since_last_order,
    CASE
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) > 90 THEN 'At Risk'
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) > 30 THEN 'Cooling'
        ELSE 'Active'
    END as customer_status
FROM silver.sales_cleaned
GROUP BY customer_email;
```

## Implémentation par plateforme

### BigQuery

```
project_id
├── dataset_bronze      -- raw_*
├── dataset_silver      -- cleaned_*, validated_*
└── dataset_gold        -- dm_*, fact_*, dim_*, agg_*
```

### Snowflake

```
database
├── schema_bronze       -- RAW_*
├── schema_silver       -- CLEAN_*
└── schema_gold         -- DIM_*, FACT_*, AGG_*
```

### Databricks / Fabric

```
Workspace
├── Lakehouse_Bronze
├── Lakehouse_Silver
└── Lakehouse_Gold
```

## Orchestration des transformations

### Option 1 : Scheduled Queries (BigQuery)

```sql
-- Requête planifiée : Bronze → Silver (chaque heure)
-- Configuration : Schedule every 1 hour

INSERT INTO silver.sales_cleaned
SELECT DISTINCT ...
FROM bronze.sales_raw
WHERE ingestion_timestamp >
    (SELECT MAX(_processed_at) FROM silver.sales_cleaned);
```

### Option 2 : Stored Procedures

```sql
-- BigQuery : Procédure stockée
CREATE OR REPLACE PROCEDURE silver.sp_transform_sales()
BEGIN
    -- Transformation Bronze → Silver
    CREATE OR REPLACE TABLE silver.sales_cleaned AS
    SELECT ...
    FROM bronze.sales_raw;

    -- Log
    INSERT INTO logs.pipeline_runs VALUES (
        CURRENT_TIMESTAMP(),
        'silver.sp_transform_sales',
        'SUCCESS'
    );
END;

-- Appel
CALL silver.sp_transform_sales();
```

### Option 3 : Dataform / dbt

```sql
-- models/silver/sales_cleaned.sql (dbt/Dataform)
{{ config(
    materialized='table',
    partition_by={'field': 'order_date', 'data_type': 'date'}
) }}

SELECT DISTINCT
    CAST(order_id_raw AS INT64) as order_id,
    PARSE_DATE('%Y%m%d', date_raw) as order_date,
    SAFE_CAST(amount_raw AS FLOAT64) as amount
FROM {{ ref('bronze_sales_raw') }}
WHERE order_id_raw IS NOT NULL
```

## Bonnes pratiques

### Nommage

| Couche | Convention | Exemple |
|--------|------------|---------|
| Bronze | `raw_*`, `bronze_*` | `raw_sales_2024` |
| Silver | `clean_*`, `validated_*` | `clean_orders` |
| Gold | `dm_*`, `agg_*`, `fact_*` | `agg_sales_daily` |

### Metadata

Toujours inclure :
```sql
-- Bronze
_ingested_at TIMESTAMP
_source_file STRING
_source_system STRING

-- Silver
_processed_at TIMESTAMP
_data_quality_score FLOAT64

-- Gold
_refreshed_at TIMESTAMP
_grain STRING  -- 'daily', 'monthly'
```

### Tests

```sql
-- Test Bronze : données arrivent
SELECT COUNT(*) FROM bronze.sales_raw
WHERE DATE(ingestion_timestamp) = CURRENT_DATE();
-- Attendu : > 0

-- Test Silver : pas de doublons
SELECT order_id, COUNT(*)
FROM silver.sales_cleaned
GROUP BY 1 HAVING COUNT(*) > 1;
-- Attendu : 0 lignes

-- Test Gold : cohérence
SELECT ABS(
    (SELECT SUM(amount) FROM silver.sales_cleaned) -
    (SELECT SUM(total_revenue) FROM gold.sales_daily)
);
-- Attendu : < 0.01 (arrondi)
```

## Points clés à retenir

- **Bronze** = données brutes, immutables, archivage long terme
- **Silver** = nettoyées, validées, dédupliquées, types corrects
- **Gold** = agrégées, dénormalisées, prêtes pour BI/ML
- Chaque couche a un objectif distinct
- Automatiser les transformations (dbt, Dataform, Procedures)
- Tester la qualité à chaque couche
- Documenter les transformations business

---

[Module précédent](./05-technologies-cloud.md) | [Retour au sommaire](./README.md)

## Pour aller plus loin

- [Brief pratique : BigQuery Medallion](../../../99-Brief/BigQuery-Medallion/)
- [Cours GCP BigQuery](../../../04-Cloud-Platforms/GCP/BigQuery/)
