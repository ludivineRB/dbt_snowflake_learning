# Module 03 - Chargement des données

## Méthodes d'ingestion

BigQuery offre plusieurs méthodes pour charger des données :

```
┌─────────────────────────────────────────────────────────┐
│                MÉTHODES D'INGESTION                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  BATCH (volumes importants)                             │
│  ├── Cloud Storage → BigQuery                           │
│  ├── Upload local                                       │
│  └── BigQuery Data Transfer                             │
│                                                          │
│  STREAMING (temps réel)                                 │
│  ├── Streaming API                                      │
│  └── Dataflow                                           │
│                                                          │
│  EXTERNE (sans chargement)                              │
│  └── Tables externes sur GCS                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Chargement depuis Cloud Storage

### Formats supportés

| Format | Extension | Usage |
|--------|-----------|-------|
| CSV | `.csv` | Données tabulaires simples |
| JSON | `.json`, `.jsonl` | Données semi-structurées |
| Avro | `.avro` | Schéma intégré |
| Parquet | `.parquet` | Optimisé colonnes |
| ORC | `.orc` | Hadoop ecosystem |

### Préparer les données

Exemple de fichier `sales.csv` :

```csv
order_id,order_date,customer_email,product_id,quantity,unit_price,total_amount
ORD001,2024-01-15,alice@email.com,PROD001,2,29.99,59.98
ORD002,2024-01-15,bob@email.com,PROD002,1,149.99,149.99
ORD003,2024-01-16,alice@email.com,PROD003,3,19.99,59.97
```

### Upload vers Cloud Storage

```bash
# Upload d'un fichier
gsutil cp sales.csv gs://formation-bigquery-dwh-data/landing/sales/

# Upload de plusieurs fichiers
gsutil -m cp *.csv gs://formation-bigquery-dwh-data/landing/sales/

# Vérifier
gsutil ls gs://formation-bigquery-dwh-data/landing/sales/
```

### Chargement via SQL (LOAD DATA)

```sql
-- Charger un CSV depuis GCS
LOAD DATA OVERWRITE bronze.raw_sales
FROM FILES (
    format = 'CSV',
    uris = ['gs://formation-bigquery-dwh-data/landing/sales/*.csv'],
    skip_leading_rows = 1
);

-- Charger avec schéma explicite
LOAD DATA OVERWRITE bronze.raw_sales (
    order_id STRING,
    order_date STRING,
    customer_email STRING,
    product_id STRING,
    quantity INT64,
    unit_price FLOAT64,
    total_amount FLOAT64
)
FROM FILES (
    format = 'CSV',
    uris = ['gs://formation-bigquery-dwh-data/landing/sales/*.csv'],
    skip_leading_rows = 1
);
```

### Chargement via bq CLI

```bash
# Charger un CSV
bq load \
    --source_format=CSV \
    --skip_leading_rows=1 \
    --autodetect \
    bronze.raw_sales \
    gs://formation-bigquery-dwh-data/landing/sales/sales.csv

# Charger avec schéma JSON
echo '[
    {"name": "order_id", "type": "STRING"},
    {"name": "order_date", "type": "STRING"},
    {"name": "customer_email", "type": "STRING"},
    {"name": "product_id", "type": "STRING"},
    {"name": "quantity", "type": "INTEGER"},
    {"name": "unit_price", "type": "FLOAT"},
    {"name": "total_amount", "type": "FLOAT"}
]' > schema.json

bq load \
    --source_format=CSV \
    --skip_leading_rows=1 \
    --schema=schema.json \
    bronze.raw_sales \
    gs://formation-bigquery-dwh-data/landing/sales/*.csv
```

## Tables externes

Interroger des fichiers GCS **sans les charger** dans BigQuery.

### Créer une table externe

```sql
-- Table externe sur CSV
CREATE OR REPLACE EXTERNAL TABLE bronze.ext_sales
OPTIONS (
    format = 'CSV',
    uris = ['gs://formation-bigquery-dwh-data/landing/sales/*.csv'],
    skip_leading_rows = 1
);

-- Requêter directement
SELECT * FROM bronze.ext_sales LIMIT 10;
```

### Avantages / Inconvénients

| Aspect | Table native | Table externe |
|--------|-------------|---------------|
| **Performance** | Optimisée | Plus lente |
| **Coût stockage** | Payant | Gratuit (GCS seul) |
| **Coût requête** | Normal | Normal |
| **Fraîcheur** | Snapshot | Temps réel |
| **Usage** | Production | Exploration |

## Chargement JSON

### JSON Lines (JSONL)

Fichier `events.jsonl` :
```json
{"event_id": "E001", "timestamp": "2024-01-15T10:30:00Z", "type": "click", "data": {"page": "/home"}}
{"event_id": "E002", "timestamp": "2024-01-15T10:31:00Z", "type": "purchase", "data": {"product": "PROD001"}}
```

### Charger du JSON

```sql
-- Charger JSONL
LOAD DATA OVERWRITE bronze.raw_events
FROM FILES (
    format = 'JSON',
    uris = ['gs://formation-bigquery-dwh-data/landing/events/*.jsonl']
);

-- Avec schéma (semi-structuré)
CREATE TABLE bronze.raw_events (
    event_id STRING,
    timestamp TIMESTAMP,
    type STRING,
    data JSON  -- Colonne JSON native
);

LOAD DATA INTO bronze.raw_events
FROM FILES (
    format = 'JSON',
    uris = ['gs://formation-bigquery-dwh-data/landing/events/*.jsonl']
);
```

### Extraire des champs JSON

```sql
-- Accéder aux champs JSON
SELECT
    event_id,
    timestamp,
    type,
    JSON_VALUE(data, '$.page') as page,
    JSON_VALUE(data, '$.product') as product
FROM bronze.raw_events;
```

## Streaming (temps réel)

Pour les données en continu (IoT, logs, etc.).

### Via l'API

```python
from google.cloud import bigquery

client = bigquery.Client()
table_id = "projet.bronze.events_stream"

rows = [
    {"event_id": "E003", "timestamp": "2024-01-15T10:35:00Z", "type": "view"},
    {"event_id": "E004", "timestamp": "2024-01-15T10:36:00Z", "type": "click"}
]

errors = client.insert_rows_json(table_id, rows)
if errors:
    print(f"Erreurs: {errors}")
```

### Considérations streaming

- Coût : $0.05 par 200 MB (après 2 TB gratuits/mois)
- Buffer : données visibles après quelques secondes
- Pas de mise à jour : insert uniquement
- Usage : IoT, logs, événements temps réel

## Data Transfer Service

Service géré pour les transferts récurrents depuis :
- Google Ads
- Google Analytics
- YouTube
- Amazon S3
- Teradata, Redshift (migration)

### Créer un transfert

Console → BigQuery → Data Transfers → Create Transfer

## Bonnes pratiques d'ingestion Bronze

### Pattern recommandé

```sql
-- 1. Table Bronze avec métadonnées
CREATE TABLE bronze.raw_sales (
    -- Métadonnées d'ingestion
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    _source_file STRING,

    -- Colonnes sources (STRING pour préserver l'original)
    order_id STRING,
    order_date STRING,
    customer_email STRING,
    product_id STRING,
    quantity STRING,
    unit_price STRING,
    total_amount STRING
)
PARTITION BY DATE(_ingested_at);

-- 2. Charger avec métadonnées
INSERT INTO bronze.raw_sales
(_source_file, order_id, order_date, customer_email, product_id, quantity, unit_price, total_amount)
SELECT
    _FILE_NAME as _source_file,
    *
FROM bronze.ext_sales_temp;
```

### Gestion des erreurs

```sql
-- Configurer un répertoire pour les lignes rejetées
LOAD DATA OVERWRITE bronze.raw_sales
FROM FILES (
    format = 'CSV',
    uris = ['gs://bucket/landing/sales/*.csv']
)
WITH CONNECTION `project.region.connection`
OPTIONS (
    max_bad_records = 100  -- Tolérer jusqu'à 100 erreurs
);
```

## Exercice pratique

### 1. Créer les fichiers sources

Créez un fichier `customers.csv` :
```csv
customer_id,email,first_name,last_name,country,created_at
CUST001,alice@email.com,Alice,Martin,FR,2023-06-15
CUST002,bob@email.com,Bob,Dupont,FR,2023-08-22
CUST003,carol@email.com,Carol,Smith,UK,2024-01-10
```

### 2. Uploader et charger

```bash
# Upload
gsutil cp customers.csv gs://formation-bigquery-dwh-data/landing/customers/

# Charger
bq load --autodetect bronze.raw_customers \
    gs://formation-bigquery-dwh-data/landing/customers/customers.csv
```

### 3. Vérifier

```sql
SELECT * FROM bronze.raw_customers;
```

## Points clés à retenir

- **Batch** : Cloud Storage → BigQuery (recommandé pour volumes)
- **Tables externes** : requêter GCS sans chargement (exploration)
- **Streaming** : temps réel, coût plus élevé
- **Bronze** : garder les données brutes en STRING
- Toujours ajouter des **métadonnées d'ingestion**
- **Partitionner** par date d'ingestion

---

**Prochain module :** [04 - Architecture Medallion dans BigQuery](./04-medallion.md)

[Module précédent](./02-setup.md) | [Retour au sommaire](./README.md)
