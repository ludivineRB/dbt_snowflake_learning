# Module 04 - Architecture Medallion dans BigQuery

## Rappel de l'architecture

```
┌─────────────────────────────────────────────────────────┐
│                    BIGQUERY PROJECT                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │                   GOLD (dataset)                   │  │
│  │  Tables agrégées, KPIs, prêtes pour BI            │  │
│  │  • gold.agg_sales_daily                           │  │
│  │  • gold.dm_customer_360                           │  │
│  │  • gold.fact_revenue                              │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ↑                               │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │                  SILVER (dataset)                  │  │
│  │  Données nettoyées, validées, typées              │  │
│  │  • silver.clean_sales                             │  │
│  │  • silver.clean_customers                         │  │
│  │  • silver.clean_products                          │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          ↑                               │
│  ┌───────────────────────┴───────────────────────────┐  │
│  │                  BRONZE (dataset)                  │  │
│  │  Données brutes, as-is de la source               │  │
│  │  • bronze.raw_sales                               │  │
│  │  • bronze.raw_customers                           │  │
│  │  • bronze.raw_products                            │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Couche Bronze : Implémentation

### Schéma Bronze

```sql
-- Table Bronze : Ventes brutes
CREATE OR REPLACE TABLE bronze.raw_sales (
    -- Métadonnées d'ingestion
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING,
    _batch_id STRING,

    -- Données sources (STRING pour préserver l'original)
    order_id STRING,
    order_date STRING,
    customer_email STRING,
    product_id STRING,
    quantity STRING,
    unit_price STRING,
    total_amount STRING,
    payment_method STRING,
    shipping_address STRING
)
PARTITION BY DATE(_ingested_at)
OPTIONS (
    description = 'Données brutes des ventes - Bronze Layer',
    labels = [("layer", "bronze"), ("source", "ecommerce")]
);
```

### Chargement Bronze

```sql
-- Ingestion depuis GCS
INSERT INTO bronze.raw_sales (
    _source_file, _batch_id,
    order_id, order_date, customer_email, product_id,
    quantity, unit_price, total_amount, payment_method, shipping_address
)
SELECT
    _FILE_NAME,
    GENERATE_UUID(),
    order_id, order_date, customer_email, product_id,
    quantity, unit_price, total_amount, payment_method, shipping_address
FROM EXTERNAL_QUERY(
    'gs://bucket/landing/sales/*.csv',
    '''SELECT * FROM sales'''
);
```

### Vérification Bronze

```sql
-- Statistiques d'ingestion
SELECT
    DATE(_ingested_at) as ingestion_date,
    _source_file,
    COUNT(*) as row_count,
    COUNT(DISTINCT order_id) as unique_orders
FROM bronze.raw_sales
GROUP BY 1, 2
ORDER BY 1 DESC;
```

## Couche Silver : Transformation

### Transformations typiques

| Transformation | Bronze (Input) | Silver (Output) |
|----------------|----------------|-----------------|
| Type casting | `"2024-01-15"` | `DATE` |
| Normalisation | `" ALICE "` | `"alice"` |
| Dédoublonnage | 3 lignes id=1 | 1 ligne id=1 |
| Filtrage | Montants négatifs | Exclus |
| Enrichissement | `country_code` | + `country_name` |

### Script Bronze → Silver

```sql
-- Transformation vers Silver
CREATE OR REPLACE TABLE silver.clean_sales AS
WITH deduplicated AS (
    -- Dédoublonnage : garder la dernière ingestion
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY _ingested_at DESC
        ) as rn
    FROM bronze.raw_sales
),
validated AS (
    SELECT
        -- Clés
        order_id,

        -- Dates - Parsing sécurisé
        SAFE.PARSE_DATE('%Y-%m-%d', order_date) as order_date,

        -- Emails - Normalisation
        LOWER(TRIM(customer_email)) as customer_email,

        -- Références
        UPPER(TRIM(product_id)) as product_id,

        -- Numériques - Cast sécurisé
        SAFE_CAST(quantity AS INT64) as quantity,
        SAFE_CAST(unit_price AS FLOAT64) as unit_price,
        SAFE_CAST(total_amount AS FLOAT64) as total_amount,

        -- Catégoriels
        UPPER(TRIM(payment_method)) as payment_method,

        -- Métadonnées
        _ingested_at as bronze_ingested_at,
        CURRENT_TIMESTAMP() as silver_processed_at

    FROM deduplicated
    WHERE rn = 1
)
SELECT *
FROM validated
WHERE
    -- Filtres de qualité
    order_id IS NOT NULL
    AND order_date IS NOT NULL
    AND SAFE_CAST(total_amount AS FLOAT64) > 0
    AND customer_email LIKE '%@%.%';
```

### Table Silver avec partitionnement

```sql
-- Création avec partitionnement et clustering
CREATE OR REPLACE TABLE silver.clean_sales
PARTITION BY order_date
CLUSTER BY customer_email, product_id
AS
SELECT
    order_id,
    SAFE.PARSE_DATE('%Y-%m-%d', order_date) as order_date,
    LOWER(TRIM(customer_email)) as customer_email,
    UPPER(TRIM(product_id)) as product_id,
    SAFE_CAST(quantity AS INT64) as quantity,
    SAFE_CAST(unit_price AS FLOAT64) as unit_price,
    SAFE_CAST(total_amount AS FLOAT64) as total_amount,
    CURRENT_TIMESTAMP() as processed_at
FROM bronze.raw_sales
WHERE
    order_id IS NOT NULL
    AND SAFE_CAST(total_amount AS FLOAT64) > 0;
```

### Validation de qualité Silver

```sql
-- Rapport de qualité
CREATE OR REPLACE VIEW silver.vw_quality_report AS
SELECT
    'clean_sales' as table_name,
    COUNT(*) as total_rows,
    COUNT(DISTINCT order_id) as unique_orders,
    COUNTIF(order_date IS NULL) as null_dates,
    COUNTIF(customer_email IS NULL) as null_emails,
    COUNTIF(total_amount <= 0) as invalid_amounts,
    MIN(order_date) as min_date,
    MAX(order_date) as max_date,
    CURRENT_TIMESTAMP() as report_generated_at
FROM silver.clean_sales;

-- Consulter le rapport
SELECT * FROM silver.vw_quality_report;
```

## Couche Gold : Agrégation

### Métriques business

```sql
-- GOLD : Ventes par jour
CREATE OR REPLACE TABLE gold.agg_sales_daily
PARTITION BY order_date
CLUSTER BY product_id
AS
SELECT
    order_date,
    product_id,

    -- Métriques de volume
    COUNT(DISTINCT order_id) as order_count,
    COUNT(DISTINCT customer_email) as unique_customers,
    SUM(quantity) as total_quantity,

    -- Métriques financières
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    MIN(total_amount) as min_order_value,
    MAX(total_amount) as max_order_value,

    -- Métadonnées
    CURRENT_TIMESTAMP() as refreshed_at

FROM silver.clean_sales
GROUP BY order_date, product_id;
```

### Vue Customer 360

```sql
-- GOLD : Profil client complet
CREATE OR REPLACE TABLE gold.dm_customer_360 AS
SELECT
    customer_email,

    -- Premières métriques
    MIN(order_date) as first_order_date,
    MAX(order_date) as last_order_date,
    DATE_DIFF(MAX(order_date), MIN(order_date), DAY) as customer_tenure_days,

    -- Métriques d'achat
    COUNT(DISTINCT order_id) as total_orders,
    SUM(total_amount) as lifetime_value,
    AVG(total_amount) as avg_order_value,
    SUM(quantity) as total_items_purchased,

    -- Métriques de récence
    DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) as days_since_last_order,

    -- Segmentation RFM simplifiée
    CASE
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) <= 30 THEN 'Active'
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(order_date), DAY) <= 90 THEN 'At Risk'
        ELSE 'Churned'
    END as customer_status,

    -- Valeur client
    CASE
        WHEN SUM(total_amount) >= 1000 THEN 'High Value'
        WHEN SUM(total_amount) >= 500 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment,

    -- Métadonnées
    CURRENT_TIMESTAMP() as refreshed_at

FROM silver.clean_sales
GROUP BY customer_email;
```

### Tendances temporelles

```sql
-- GOLD : Tendances mensuelles
CREATE OR REPLACE TABLE gold.agg_monthly_trends AS
SELECT
    DATE_TRUNC(order_date, MONTH) as month,
    EXTRACT(YEAR FROM order_date) as year,
    FORMAT_DATE('%Y-%m', order_date) as year_month,

    -- Volume
    COUNT(DISTINCT order_id) as orders,
    COUNT(DISTINCT customer_email) as customers,

    -- Revenue
    SUM(total_amount) as revenue,

    -- Comparaison M-1
    LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC(order_date, MONTH)) as prev_month_revenue,
    SAFE_DIVIDE(
        SUM(total_amount) - LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC(order_date, MONTH)),
        LAG(SUM(total_amount)) OVER (ORDER BY DATE_TRUNC(order_date, MONTH))
    ) * 100 as revenue_growth_pct,

    CURRENT_TIMESTAMP() as refreshed_at

FROM silver.clean_sales
GROUP BY 1, 2, 3
ORDER BY 1;
```

## Pipeline complet

### Script de refresh end-to-end

```sql
-- SCRIPT : Refresh complet Bronze → Silver → Gold

-- Étape 1 : Charger Bronze (supposé fait par ingestion externe)
-- LOAD DATA INTO bronze.raw_sales FROM FILES (...)

-- Étape 2 : Refresh Silver
CREATE OR REPLACE TABLE silver.clean_sales
PARTITION BY order_date
CLUSTER BY customer_email
AS
SELECT
    order_id,
    SAFE.PARSE_DATE('%Y-%m-%d', order_date) as order_date,
    LOWER(TRIM(customer_email)) as customer_email,
    UPPER(TRIM(product_id)) as product_id,
    SAFE_CAST(quantity AS INT64) as quantity,
    SAFE_CAST(total_amount AS FLOAT64) as total_amount,
    CURRENT_TIMESTAMP() as processed_at
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _ingested_at DESC) as rn
    FROM bronze.raw_sales
)
WHERE rn = 1 AND order_id IS NOT NULL;

-- Étape 3 : Refresh Gold - Sales Daily
CREATE OR REPLACE TABLE gold.agg_sales_daily AS
SELECT
    order_date,
    COUNT(DISTINCT order_id) as orders,
    SUM(total_amount) as revenue,
    CURRENT_TIMESTAMP() as refreshed_at
FROM silver.clean_sales
GROUP BY order_date;

-- Étape 4 : Refresh Gold - Customer 360
CREATE OR REPLACE TABLE gold.dm_customer_360 AS
SELECT
    customer_email,
    COUNT(*) as total_orders,
    SUM(total_amount) as lifetime_value,
    MAX(order_date) as last_order,
    CURRENT_TIMESTAMP() as refreshed_at
FROM silver.clean_sales
GROUP BY customer_email;

-- Log de fin
SELECT 'Pipeline completed' as status, CURRENT_TIMESTAMP() as completed_at;
```

## Points clés à retenir

- **Bronze** : données brutes, STRING, métadonnées d'ingestion
- **Silver** : types corrects, dédoublonné, validé, partitionné
- **Gold** : agrégé, orienté business, optimisé pour BI
- Utiliser **SAFE_CAST** et **SAFE.** pour éviter les erreurs
- **Partitionner** par date, **Clusterer** par colonnes filtrées
- Toujours **vérifier la qualité** entre les couches

---

**Prochain module :** [05 - Automatisation avec Procedures et Schedules](./05-automatisation.md)

[Module précédent](./03-ingestion.md) | [Retour au sommaire](./README.md)
