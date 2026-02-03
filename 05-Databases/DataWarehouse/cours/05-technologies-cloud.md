# Module 05 - Technologies Cloud Data Warehouse

## Vue d'ensemble du marché

Les Data Warehouses cloud ont révolutionné l'analytique en offrant :
- Scalabilité élastique
- Paiement à l'usage
- Zéro infrastructure à gérer
- Performance optimisée

### Les leaders du marché

```
┌─────────────────────────────────────────────────────────┐
│                 CLOUD DATA WAREHOUSES                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │ Snowflake  │  │ BigQuery   │  │  Redshift  │         │
│  │   (Multi)  │  │   (GCP)    │  │   (AWS)    │         │
│  └────────────┘  └────────────┘  └────────────┘         │
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │  Synapse   │  │ Databricks │  │  Firebolt  │         │
│  │  (Azure)   │  │   (Multi)  │  │   (Multi)  │         │
│  └────────────┘  └────────────┘  └────────────┘         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Snowflake

### Architecture unique

```
┌─────────────────────────────────────────────────────────┐
│                    CLOUD SERVICES                        │
│    (Authentification, Metadata, Optimiseur, Sécurité)   │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Warehouse   │    │  Warehouse   │    │  Warehouse   │
│    XS        │    │     M        │    │     XL       │
│  (Compute)   │    │  (Compute)   │    │  (Compute)   │
└──────────────┘    └──────────────┘    └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                   ┌────────▼────────┐
                   │   STORAGE       │
                   │  (S3/Azure/GCS) │
                   │  Séparé & Mutu- │
                   │  alisé          │
                   └─────────────────┘
```

### Caractéristiques clés

| Fonctionnalité | Description |
|----------------|-------------|
| **Multi-cloud** | AWS, Azure, GCP |
| **Separation of concerns** | Compute et Storage indépendants |
| **Zero-copy cloning** | Clone instantané sans duplication |
| **Time Travel** | Accès aux données passées (jusqu'à 90j) |
| **Data Sharing** | Partage sans copie entre comptes |
| **Semi-structured** | JSON, Avro, Parquet natifs |

### Tarification

```
Coût Total = Compute (Credits) + Storage (TB/mois)
                │                      │
                ▼                      ▼
         Usage réel              $23-40/TB/mois
         (par seconde)           selon région
```

### Exemple SQL Snowflake

```sql
-- Créer un warehouse
CREATE WAREHOUSE analytics_wh
WITH WAREHOUSE_SIZE = 'MEDIUM'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE;

-- Time Travel
SELECT * FROM sales
AT(TIMESTAMP => '2024-01-15 10:00:00'::TIMESTAMP);

-- Clone sans copie
CREATE TABLE sales_backup CLONE sales;
```

## Google BigQuery

### Architecture serverless

```
┌─────────────────────────────────────────────────────────┐
│                     BIGQUERY                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │              DREMEL (Query Engine)               │    │
│  │        Exécution distribuée, massive, SQL        │    │
│  └─────────────────────────────────────────────────┘    │
│                          │                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │           COLOSSUS (Distributed Storage)         │    │
│  │         Format Capacitor (colonnes optimisé)     │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │                JUPITER NETWORK                   │    │
│  │              1 Petabit/s bandwidth               │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Caractéristiques clés

| Fonctionnalité | Description |
|----------------|-------------|
| **Serverless** | Aucune infrastructure à gérer |
| **Auto-scaling** | Scaling automatique illimité |
| **SQL Standard** | SQL ANSI-2011 |
| **BigQuery ML** | ML directement en SQL |
| **Streaming** | Ingestion temps réel |
| **GIS** | Données géospatiales natives |
| **BI Engine** | Cache en mémoire pour BI |

### Tarification

```
┌─────────────────────────────────────────────────────────┐
│                 MODÈLES DE TARIFICATION                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ON-DEMAND (À la requête)                               │
│  ├── $5 / TB de données scannées                        │
│  ├── 1 TB gratuit / mois                                │
│  └── Idéal pour charges variables                       │
│                                                          │
│  CAPACITY (Réservation)                                 │
│  ├── Slots réservés (unités de calcul)                  │
│  ├── Prix prévisible                                    │
│  └── Idéal pour charges constantes                      │
│                                                          │
│  STORAGE                                                │
│  ├── $0.02 / GB / mois (Active)                         │
│  └── $0.01 / GB / mois (Long-term, > 90 jours)          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Exemple SQL BigQuery

```sql
-- Requête simple avec coût contrôlé
SELECT
    region,
    DATE_TRUNC(order_date, MONTH) as month,
    SUM(amount) as revenue
FROM `project.dataset.orders`
WHERE order_date >= '2024-01-01'
GROUP BY region, month;

-- BigQuery ML : Créer un modèle
CREATE OR REPLACE MODEL `project.dataset.churn_model`
OPTIONS(model_type='LOGISTIC_REG') AS
SELECT
    customer_segment,
    total_purchases,
    days_since_last_order,
    churned
FROM `project.dataset.customer_features`;

-- Prédiction
SELECT *
FROM ML.PREDICT(MODEL `project.dataset.churn_model`,
    (SELECT * FROM `project.dataset.new_customers`));
```

## Amazon Redshift

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    REDSHIFT CLUSTER                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   LEADER NODE                     │   │
│  │      (Query planning, Results aggregation)        │   │
│  └──────────────────────────────────────────────────┘   │
│                          │                               │
│         ┌────────────────┼────────────────┐             │
│         ▼                ▼                ▼             │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐      │
│  │  Compute   │   │  Compute   │   │  Compute   │      │
│  │   Node 1   │   │   Node 2   │   │   Node N   │      │
│  │  (Slices)  │   │  (Slices)  │   │  (Slices)  │      │
│  └────────────┘   └────────────┘   └────────────┘      │
│                                                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   REDSHIFT SPECTRUM   │
              │   (Query S3 direct)   │
              └───────────────────────┘
```

### Caractéristiques clés

| Fonctionnalité | Description |
|----------------|-------------|
| **Columnar** | Stockage orienté colonnes |
| **MPP** | Massively Parallel Processing |
| **Spectrum** | Requêtes sur S3 sans chargement |
| **ML** | Intégration SageMaker |
| **Federated** | Requêtes vers RDS, Aurora |
| **Serverless** | Option sans gestion de cluster |

### Exemple SQL Redshift

```sql
-- Distribution et Sort Keys
CREATE TABLE fact_sales (
    sale_id BIGINT,
    product_id INT,
    customer_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
DISTSTYLE KEY
DISTKEY (product_id)
SORTKEY (sale_date);

-- Requête avec Spectrum (S3)
SELECT
    s.region,
    SUM(s.amount) as total
FROM spectrum.external_sales s
JOIN public.dim_product p ON s.product_id = p.product_id
GROUP BY s.region;
```

## Azure Synapse Analytics

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  SYNAPSE WORKSPACE                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │ Dedicated  │  │ Serverless │  │   Spark    │         │
│  │ SQL Pool   │  │ SQL Pool   │  │   Pool     │         │
│  │ (DWU)      │  │ (On-demand)│  │            │         │
│  └────────────┘  └────────────┘  └────────────┘         │
│         │               │               │                │
│         └───────────────┼───────────────┘                │
│                         │                                │
│              ┌──────────▼──────────┐                    │
│              │   DATA LAKE (ADLS)  │                    │
│              │   (Parquet, Delta)  │                    │
│              └─────────────────────┘                    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              SYNAPSE LINK                         │   │
│  │   (Real-time sync : CosmosDB, SQL, Dataverse)    │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Caractéristiques clés

| Fonctionnalité | Description |
|----------------|-------------|
| **Unified** | SQL + Spark + Pipelines |
| **Serverless** | SQL on-demand sur Data Lake |
| **Power BI** | Intégration native |
| **Synapse Link** | Sync temps réel |
| **Dedicated** | Performance garantie (DWU) |

## Comparaison globale

| Critère | Snowflake | BigQuery | Redshift | Synapse |
|---------|-----------|----------|----------|---------|
| **Serverless** | Partiel | Natif | Option | Partiel |
| **Multi-cloud** | Oui | Non | Non | Non |
| **Pricing** | Credits | TB scanné | Noeud/h | DWU |
| **ML intégré** | Snowpark | BQ ML | SageMaker | Azure ML |
| **Streaming** | Snowpipe | Natif | Kinesis | Event Hub |
| **Écosystème** | Indépendant | Google | AWS | Microsoft |

## Choisir la bonne solution

```
┌─────────────────────────────────────────────────────────┐
│              ARBRE DE DÉCISION                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Multi-cloud requis ?                                   │
│       │                                                  │
│       ├── OUI → SNOWFLAKE                               │
│       │                                                  │
│       └── NON → Quel cloud principal ?                  │
│                   │                                      │
│                   ├── GCP → BIGQUERY                    │
│                   │     (Serverless, ML, Analytics)     │
│                   │                                      │
│                   ├── AWS → REDSHIFT                    │
│                   │     (Écosystème AWS, Spectrum)      │
│                   │                                      │
│                   └── Azure → SYNAPSE                   │
│                         (Power BI, Microsoft stack)     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Points clés à retenir

- **Snowflake** : Multi-cloud, séparation compute/storage, data sharing
- **BigQuery** : Serverless pur, pricing au TB scanné, ML intégré
- **Redshift** : Écosystème AWS, Spectrum pour S3, MPP traditionnel
- **Synapse** : Unified analytics, intégration Microsoft, hybrid

---

**Prochain module :** [06 - Architecture Medallion](./06-medallion.md)

[Module précédent](./04-modelisation.md) | [Retour au sommaire](./README.md)
