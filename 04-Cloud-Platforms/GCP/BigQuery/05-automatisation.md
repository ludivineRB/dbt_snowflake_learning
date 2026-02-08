# Module 05 - Automatisation avec Procedures et Schedules

## Stored Procedures (Procédures stockées)

Les procédures stockées permettent d'encapsuler la logique de transformation.

### Syntaxe de base

```sql
CREATE OR REPLACE PROCEDURE dataset.nom_procedure(
    param1 TYPE,
    param2 TYPE
)
BEGIN
    -- Instructions SQL
    -- Variables
    -- Conditions
    -- Boucles
END;
```

### Procédure Bronze → Silver

```sql
CREATE OR REPLACE PROCEDURE silver.sp_transform_sales()
BEGIN
    -- Variables
    DECLARE rows_processed INT64;
    DECLARE start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP();

    -- Transformation
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
        SELECT *,
            ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _ingested_at DESC) as rn
        FROM bronze.raw_sales
    )
    WHERE rn = 1
        AND order_id IS NOT NULL
        AND SAFE_CAST(total_amount AS FLOAT64) > 0;

    -- Compter les lignes traitées
    SET rows_processed = (SELECT COUNT(*) FROM silver.clean_sales);

    -- Logger l'exécution
    INSERT INTO silver.pipeline_logs (
        procedure_name, rows_processed, start_time, end_time, status
    ) VALUES (
        'sp_transform_sales',
        rows_processed,
        start_time,
        CURRENT_TIMESTAMP(),
        'SUCCESS'
    );
END;
```

### Procédure avec paramètres

```sql
CREATE OR REPLACE PROCEDURE silver.sp_transform_sales_incremental(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    -- Transformation incrémentale
    MERGE INTO silver.clean_sales AS target
    USING (
        SELECT
            order_id,
            SAFE.PARSE_DATE('%Y-%m-%d', order_date) as order_date,
            LOWER(TRIM(customer_email)) as customer_email,
            SAFE_CAST(total_amount AS FLOAT64) as total_amount
        FROM bronze.raw_sales
        WHERE DATE(_ingested_at) BETWEEN start_date AND end_date
    ) AS source
    ON target.order_id = source.order_id
    WHEN MATCHED THEN
        UPDATE SET
            order_date = source.order_date,
            customer_email = source.customer_email,
            total_amount = source.total_amount
    WHEN NOT MATCHED THEN
        INSERT (order_id, order_date, customer_email, total_amount)
        VALUES (source.order_id, source.order_date, source.customer_email, source.total_amount);
END;
```

### Appeler une procédure

```sql
-- Sans paramètres
CALL silver.sp_transform_sales();

-- Avec paramètres
CALL silver.sp_transform_sales_incremental('2024-01-01', '2024-01-31');

-- Depuis bq CLI
bq query --use_legacy_sql=false 'CALL silver.sp_transform_sales()'
```

### Procédure avec gestion d'erreurs

```sql
CREATE OR REPLACE PROCEDURE silver.sp_transform_with_error_handling()
BEGIN
    DECLARE error_message STRING;

    BEGIN
        -- Tentative de transformation
        CREATE OR REPLACE TABLE silver.clean_sales AS
        SELECT * FROM bronze.raw_sales WHERE 1=1;

        -- Log succès
        INSERT INTO silver.pipeline_logs (procedure_name, status, message)
        VALUES ('sp_transform', 'SUCCESS', 'Completed successfully');

    EXCEPTION WHEN ERROR THEN
        -- Capturer l'erreur
        SET error_message = @@error.message;

        -- Log erreur
        INSERT INTO silver.pipeline_logs (procedure_name, status, message)
        VALUES ('sp_transform', 'ERROR', error_message);

        -- Relancer l'erreur
        RAISE USING MESSAGE = error_message;
    END;
END;
```

## Scheduled Queries (Requêtes planifiées)

Exécuter automatiquement des requêtes à intervalles réguliers.

### Créer via la Console

1. BigQuery → Query editor
2. Écrire la requête
3. Menu "Schedule" → "Create new scheduled query"
4. Configurer :
   - **Name** : `refresh_silver_sales_daily`
   - **Schedule** : `every 24 hours`
   - **Start time** : 06:00 UTC
   - **Destination** : Table ou None (pour CALL)

### Créer via SQL (Data Transfer API)

```sql
-- Note : les scheduled queries se gèrent via l'API ou la console
-- Voici le SQL qu'on peut planifier :

-- Requête à planifier : Refresh Silver → Gold
CREATE OR REPLACE TABLE gold.agg_sales_daily AS
SELECT
    order_date,
    COUNT(DISTINCT order_id) as order_count,
    SUM(total_amount) as total_revenue,
    CURRENT_TIMESTAMP() as refreshed_at
FROM silver.clean_sales
GROUP BY order_date;
```

### Créer via bq CLI

```bash
# Créer une scheduled query
bq mk --transfer_config \
    --project_id=mon-projet \
    --data_source=scheduled_query \
    --target_dataset=gold \
    --display_name='Refresh Gold Daily' \
    --schedule='every 24 hours' \
    --params='{
        "query": "CREATE OR REPLACE TABLE gold.agg_sales_daily AS SELECT order_date, COUNT(*) as orders, SUM(total_amount) as revenue FROM silver.clean_sales GROUP BY order_date",
        "destination_table_name_template": "",
        "write_disposition": "WRITE_TRUNCATE"
    }'

# Lister les scheduled queries
bq ls --transfer_config --transfer_location=EU

# Exécuter manuellement
bq mk --transfer_run \
    --run_time=2024-01-15T00:00:00Z \
    projects/mon-projet/locations/EU/transferConfigs/xxx
```

### Pipeline avec procédures planifiées

```sql
-- Procédure complète à planifier
CREATE OR REPLACE PROCEDURE gold.sp_refresh_all_gold()
BEGIN
    -- Refresh table 1
    CREATE OR REPLACE TABLE gold.agg_sales_daily AS
    SELECT order_date, COUNT(*) as orders, SUM(total_amount) as revenue
    FROM silver.clean_sales
    GROUP BY order_date;

    -- Refresh table 2
    CREATE OR REPLACE TABLE gold.dm_customer_360 AS
    SELECT
        customer_email,
        COUNT(*) as orders,
        SUM(total_amount) as ltv
    FROM silver.clean_sales
    GROUP BY customer_email;

    -- Log
    INSERT INTO gold.refresh_log (table_name, refreshed_at)
    VALUES ('all_gold_tables', CURRENT_TIMESTAMP());
END;

-- Planifier : CALL gold.sp_refresh_all_gold()
```

## Table de logs

### Créer une table de logs

```sql
CREATE TABLE IF NOT EXISTS silver.pipeline_logs (
    log_id STRING DEFAULT GENERATE_UUID(),
    procedure_name STRING,
    rows_processed INT64,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_seconds FLOAT64,
    status STRING,
    message STRING,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(created_at);
```

### Utiliser dans les procédures

```sql
CREATE OR REPLACE PROCEDURE silver.sp_logged_transform()
BEGIN
    DECLARE start_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP();
    DECLARE row_count INT64;

    -- Transformation
    CREATE OR REPLACE TABLE silver.clean_sales AS
    SELECT * FROM bronze.raw_sales;

    SET row_count = @@row_count;

    -- Log
    INSERT INTO silver.pipeline_logs (
        procedure_name, rows_processed, start_time, end_time,
        duration_seconds, status
    ) VALUES (
        'sp_logged_transform',
        row_count,
        start_ts,
        CURRENT_TIMESTAMP(),
        TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), start_ts, SECOND),
        'SUCCESS'
    );
END;
```

### Monitoring

```sql
-- Dernières exécutions
SELECT
    procedure_name,
    status,
    rows_processed,
    duration_seconds,
    created_at
FROM silver.pipeline_logs
ORDER BY created_at DESC
LIMIT 20;

-- Alertes sur erreurs
SELECT *
FROM silver.pipeline_logs
WHERE status = 'ERROR'
    AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR);
```

## Orchestration multi-étapes

### Pipeline séquentiel

```sql
CREATE OR REPLACE PROCEDURE pipeline.sp_run_full_etl()
BEGIN
    -- Étape 1 : Bronze → Silver (Sales)
    CALL silver.sp_transform_sales();

    -- Étape 2 : Bronze → Silver (Customers)
    CALL silver.sp_transform_customers();

    -- Étape 3 : Silver → Gold (Agrégations)
    CALL gold.sp_refresh_aggregates();

    -- Étape 4 : Silver → Gold (Customer 360)
    CALL gold.sp_refresh_customer_360();

    -- Log final
    INSERT INTO pipeline.execution_log (pipeline_name, status)
    VALUES ('full_etl', 'COMPLETED');
END;

-- Planifier cette procédure unique
-- Schedule : CALL pipeline.sp_run_full_etl()
```

### Dépendances avec vérification

```sql
CREATE OR REPLACE PROCEDURE pipeline.sp_safe_etl()
BEGIN
    DECLARE silver_ready BOOL DEFAULT FALSE;

    -- Vérifier que Bronze a des données récentes
    SET silver_ready = (
        SELECT COUNT(*) > 0
        FROM bronze.raw_sales
        WHERE DATE(_ingested_at) = CURRENT_DATE()
    );

    IF NOT silver_ready THEN
        RAISE USING MESSAGE = 'No fresh Bronze data for today';
    END IF;

    -- Continuer le pipeline
    CALL silver.sp_transform_sales();
    CALL gold.sp_refresh_all();
END;
```

## Bonnes pratiques

### 1. Nommage

```
sp_<layer>_<action>_<table>

Exemples :
- sp_transform_sales      (Bronze → Silver)
- sp_refresh_daily_agg    (Silver → Gold)
- sp_run_full_pipeline    (Orchestration)
```

### 2. Idempotence

```sql
-- MAUVAIS : INSERT qui duplique
INSERT INTO silver.clean_sales SELECT ...

-- BON : CREATE OR REPLACE (idempotent)
CREATE OR REPLACE TABLE silver.clean_sales AS SELECT ...

-- BON : MERGE (idempotent)
MERGE INTO silver.clean_sales AS target USING ... WHEN MATCHED THEN UPDATE ...
```

### 3. Logging systématique

Toujours logger :
- Début/fin d'exécution
- Nombre de lignes traitées
- Statut (SUCCESS/ERROR)
- Message d'erreur le cas échéant

### 4. Alerting

```sql
-- Vue pour alertes
CREATE VIEW pipeline.vw_failed_jobs AS
SELECT *
FROM pipeline.execution_log
WHERE status = 'ERROR'
    AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
```

## Points clés à retenir

- **Stored Procedures** : encapsulent la logique, paramètres, gestion erreurs
- **Scheduled Queries** : exécution automatique à intervalles réguliers
- **Logging** : traçabilité et debugging
- **Idempotence** : CREATE OR REPLACE ou MERGE
- **Orchestration** : procédure maître qui appelle les autres
- **Monitoring** : tables de logs + vues d'alertes

---

**Prochain module :** [06 - Orchestration avec Dataform](./06-dataform.md)

[Module précédent](./04-medallion.md) | [Retour au sommaire](./README.md)
