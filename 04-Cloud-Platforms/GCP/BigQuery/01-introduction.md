# Module 01 - Introduction à BigQuery

## Qu'est-ce que BigQuery ?

BigQuery est le **Data Warehouse serverless** de Google Cloud Platform. Il permet d'analyser des pétaoctets de données en utilisant du SQL standard.

### Caractéristiques principales

| Caractéristique | Description |
|-----------------|-------------|
| **Serverless** | Aucune infrastructure à gérer |
| **Scalable** | De quelques MB à plusieurs PB |
| **SQL Standard** | ANSI SQL 2011 |
| **Temps réel** | Streaming ingestion |
| **ML intégré** | BigQuery ML |
| **Géospatial** | Fonctions GIS natives |

## Architecture BigQuery

```
┌─────────────────────────────────────────────────────────┐
│                     BIGQUERY                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   DREMEL                          │   │
│  │         (Distributed Query Engine)                │   │
│  │                                                   │   │
│  │   ┌─────────┐ ┌─────────┐ ┌─────────┐           │   │
│  │   │ Worker  │ │ Worker  │ │ Worker  │  ...      │   │
│  │   │  Node   │ │  Node   │ │  Node   │           │   │
│  │   └─────────┘ └─────────┘ └─────────┘           │   │
│  └──────────────────────────────────────────────────┘   │
│                          │                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  COLOSSUS                         │   │
│  │          (Distributed Storage)                    │   │
│  │                                                   │   │
│  │   Format Capacitor : stockage colonnes           │   │
│  │   Compression automatique                        │   │
│  │   Réplication géographique                       │   │
│  └──────────────────────────────────────────────────┘   │
│                          │                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │               JUPITER NETWORK                     │   │
│  │          (1 Petabit/s bandwidth)                  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Séparation Compute / Storage

```
       ┌────────────────┐         ┌────────────────┐
       │    COMPUTE     │         │    STORAGE     │
       │    (Slots)     │         │   (Colossus)   │
       ├────────────────┤         ├────────────────┤
       │ • À la demande │         │ • $0.02/GB/mois│
       │ • Réservation  │         │ • Long-term    │
       │ • Auto-scale   │         │   $0.01/GB     │
       └────────────────┘         └────────────────┘
              │                          │
              └──────────┬───────────────┘
                         │
                    INDÉPENDANTS
                (Scale séparément)
```

## Concepts clés

### Projet

Le conteneur principal pour toutes les ressources GCP.

```
project: mon-projet-123
├── dataset: bronze
│   ├── table: raw_sales
│   └── table: raw_customers
├── dataset: silver
│   └── table: clean_orders
└── dataset: gold
    └── table: agg_revenue
```

### Dataset

Conteneur logique pour les tables, équivalent d'un schéma SQL.

```sql
-- Créer un dataset
CREATE SCHEMA IF NOT EXISTS `mon-projet.bronze`
OPTIONS(
    location = 'EU',
    description = 'Données brutes - Bronze Layer'
);
```

### Table

Structure de stockage des données.

| Type | Description | Usage |
|------|-------------|-------|
| **Native** | Stockée dans BigQuery | Standard |
| **External** | Pointe vers GCS, Drive | Données externes |
| **View** | Requête sauvegardée | Abstraction |
| **Materialized View** | Vue pré-calculée | Performance |

### Partitionnement

Diviser une table pour réduire les données scannées.

```sql
CREATE TABLE `projet.dataset.events`
(
    event_id STRING,
    event_date DATE,
    event_type STRING,
    payload STRING
)
PARTITION BY event_date  -- Partition par date
OPTIONS(
    partition_expiration_days = 365
);
```

### Clustering

Organiser les données pour optimiser les requêtes.

```sql
CREATE TABLE `projet.dataset.events`
(
    event_id STRING,
    event_date DATE,
    event_type STRING,
    user_id STRING
)
PARTITION BY event_date
CLUSTER BY event_type, user_id;  -- Clustering
```

## Modèle de tarification

### On-demand (À la demande)

```
┌─────────────────────────────────────────────────────────┐
│                    ON-DEMAND PRICING                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Analyse : $5 par TB de données scannées                │
│                                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Exemple : SELECT * FROM table (100 GB)         │    │
│  │  Coût = 0.1 TB × $5 = $0.50                     │    │
│  └─────────────────────────────────────────────────┘    │
│                                                          │
│  Premier TB gratuit chaque mois !                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Capacity (Réservation)

Pour les charges de travail prévisibles : slots réservés.

### Stockage

| Type | Prix |
|------|------|
| Active | $0.02/GB/mois |
| Long-term (>90 jours) | $0.01/GB/mois |

## Interface BigQuery

### Console GCP

```
console.cloud.google.com → BigQuery
│
├── Explorer (sidebar gauche)
│   ├── Projects
│   ├── Datasets
│   └── Tables
│
├── Query Editor (centre)
│   └── Écrire et exécuter SQL
│
└── Results (bas)
    └── Résultats des requêtes
```

### Première requête

```sql
-- Dataset public : météo mondiale
SELECT
    name,
    state,
    country,
    AVG(prcp) as avg_precipitation
FROM `bigquery-public-data.samples.gsod`
WHERE country = 'FR'
GROUP BY name, state, country
ORDER BY avg_precipitation DESC
LIMIT 10;
```

### bq CLI

```bash
# Installer gcloud SDK puis :
bq query --use_legacy_sql=false '
SELECT COUNT(*) as total
FROM `bigquery-public-data.samples.shakespeare`'

# Lister les datasets
bq ls

# Créer un dataset
bq mk --location=EU mon_dataset
```

## SQL BigQuery : spécificités

### Types de données

| Type BigQuery | Description |
|---------------|-------------|
| `STRING` | Texte UTF-8 |
| `INT64` | Entier 64-bit |
| `FLOAT64` | Décimal |
| `NUMERIC` | Décimal précis |
| `BOOL` | Booléen |
| `DATE` | Date sans heure |
| `DATETIME` | Date + heure sans timezone |
| `TIMESTAMP` | Date + heure avec timezone |
| `ARRAY` | Liste de valeurs |
| `STRUCT` | Objet structuré |

### Fonctions utiles

```sql
-- Dates
SELECT
    CURRENT_DATE() as today,
    DATE_TRUNC(order_date, MONTH) as month,
    DATE_DIFF(CURRENT_DATE(), order_date, DAY) as days_ago,
    FORMAT_DATE('%Y-%m', order_date) as year_month;

-- Safe operations (pas d'erreur si échec)
SELECT
    SAFE_CAST('abc' AS INT64) as will_be_null,
    SAFE_DIVIDE(10, 0) as also_null;

-- Arrays
SELECT
    ARRAY_AGG(product_name) as products,
    ARRAY_LENGTH(ARRAY_AGG(product_name)) as count;

-- Structs
SELECT
    STRUCT(first_name, last_name) as name;
```

## Points clés à retenir

- BigQuery est **serverless** : pas de cluster à gérer
- Tarification au **TB scanné** (ou slots réservés)
- **Partitionnement** = moins de données scannées = moins cher
- **Clustering** = données triées = requêtes plus rapides
- **1 TB gratuit** par mois pour les requêtes
- SQL standard avec extensions (ARRAY, STRUCT, etc.)

---

**Prochain module :** [02 - Création de projet et datasets](./02-setup.md)

[Retour au sommaire](./README.md)
