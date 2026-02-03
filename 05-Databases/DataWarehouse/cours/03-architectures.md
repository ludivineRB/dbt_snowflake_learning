# Module 03 - Architectures et Patterns

## Les deux écoles fondatrices

### Bill Inmon - Top-Down (Enterprise DW)

```
┌───────────────────────────────────────────────────────┐
│                  DATA SOURCES                          │
│         (ERP, CRM, Files, APIs, ...)                  │
└───────────────────────┬───────────────────────────────┘
                        │
                   ┌────▼────┐
                   │   ETL   │
                   └────┬────┘
                        │
         ┌──────────────▼──────────────┐
         │     ENTERPRISE DW           │
         │   (Normalisé 3NF)           │
         │   Source unique de vérité   │
         └──────────────┬──────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Data Mart   │ │  Data Mart   │ │  Data Mart   │
│   Finance    │ │   Ventes     │ │   Marketing  │
└──────────────┘ └──────────────┘ └──────────────┘
```

**Caractéristiques :**
- DW centralisé et normalisé (3NF)
- Data Marts dépendants du DW
- Gouvernance forte
- Vision entreprise globale

**Avantages :**
- Cohérence des données garantie
- Une seule source de vérité
- Qualité des données élevée

**Inconvénients :**
- Long à mettre en place
- Coût initial élevé
- Rigidité du modèle

### Ralph Kimball - Bottom-Up (Dimensional)

```
┌───────────────────────────────────────────────────────┐
│                  DATA SOURCES                          │
│         (ERP, CRM, Files, APIs, ...)                  │
└───────────────────────┬───────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌────────┐      ┌────────┐      ┌────────┐
   │  ETL   │      │  ETL   │      │  ETL   │
   └───┬────┘      └───┬────┘      └───┬────┘
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Data Mart   │ │  Data Mart   │ │  Data Mart   │
│   Ventes     │ │   Finance    │ │   Marketing  │
│  (Star)      │ │  (Star)      │ │  (Star)      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
           ┌────────────▼────────────┐
           │      DATA WAREHOUSE     │
           │  (Conformed Dimensions) │
           └─────────────────────────┘
```

**Caractéristiques :**
- Data Marts indépendants en Star Schema
- Dimensions conformes (partagées)
- Approche incrémentale
- Orienté business process

**Avantages :**
- Time-to-value rapide
- Coût initial modéré
- Flexibilité

**Inconvénients :**
- Risque de silos
- Cohérence à maintenir
- Dimensions à synchroniser

### Comparaison Inmon vs Kimball

| Aspect | Inmon | Kimball |
|--------|-------|---------|
| **Approche** | Top-down | Bottom-up |
| **Modèle central** | 3NF normalisé | Dimensional (Star) |
| **Data Marts** | Dépendants | Indépendants |
| **Délai initial** | Long | Court |
| **Coût initial** | Élevé | Modéré |
| **Évolutivité** | Complexe | Flexible |
| **Cas d'usage** | Grande entreprise | PME, agilité |

## Architecture moderne : Lakehouse

### Évolution des architectures

```
     2000s                2010s                2020s
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│    DW       │      │  DW + Lake  │      │  LAKEHOUSE  │
│ (Expensive) │      │  (Silos)    │      │  (Unified)  │
└─────────────┘      └─────────────┘      └─────────────┘
```

### Data Lakehouse

Le Lakehouse combine :
- **Stockage économique** du Data Lake (object storage)
- **Performance ACID** du Data Warehouse
- **Gouvernance** et qualité des données
- **Support ML** natif

```
┌─────────────────────────────────────────────────────────┐
│                     LAKEHOUSE                            │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │          Unified Metadata Layer                  │   │
│  │    (Unity Catalog / Iceberg / Hive Metastore)   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │    SQL       │  │   Python     │  │     ML       │  │
│  │   Engine     │  │   Spark      │  │   Training   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Delta Lake / Apache Iceberg              │   │
│  │     (ACID Transactions, Time Travel, Schema)     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Object Storage (S3, GCS, ADLS)         │   │
│  │              (Parquet, ORC, Delta)               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Implémentations Lakehouse

| Plateforme | Format de table | Métadonnées |
|------------|-----------------|-------------|
| **Databricks** | Delta Lake | Unity Catalog |
| **AWS** | Iceberg / Delta | Glue Catalog |
| **GCP** | BigLake | BigQuery |
| **Azure** | Delta Lake | Purview |
| **Snowflake** | Iceberg | Propriétaire |

## Architecture en couches (Layers)

### Architecture 3 couches classique

```
┌──────────────────────────────────────────────────────┐
│                  PRESENTATION                         │
│           (BI Tools, Dashboards, Reports)            │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│                  DATA WAREHOUSE                       │
│               (Agrégations, KPIs)                    │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│                   STAGING                             │
│           (Données brutes, nettoyage)                │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│                    SOURCES                            │
│          (ERP, CRM, APIs, Files, ...)                │
└──────────────────────────────────────────────────────┘
```

### Architecture Lambda

Pour le traitement temps réel + batch :

```
                    ┌─────────────────┐
                    │     SOURCES     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              │              ▼
     ┌────────────────┐      │      ┌────────────────┐
     │  SPEED LAYER   │      │      │  BATCH LAYER   │
     │   (Streaming)  │      │      │   (ETL daily)  │
     │  Kafka/Flink   │      │      │  Spark/Airflow │
     └───────┬────────┘      │      └───────┬────────┘
             │               │              │
             │        ┌──────▼──────┐       │
             │        │SERVING LAYER│       │
             └───────►│  (Combined) │◄──────┘
                      └──────┬──────┘
                             │
                      ┌──────▼──────┐
                      │   QUERIES   │
                      └─────────────┘
```

### Architecture Kappa

Simplification : tout est stream.

```
┌───────────────────────────────────────────────────────┐
│                     SOURCES                            │
└───────────────────────┬───────────────────────────────┘
                        │
                ┌───────▼───────┐
                │  EVENT STREAM │
                │    (Kafka)    │
                └───────┬───────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Real-   │   │ Batch   │   │  ML     │
    │ time    │   │ (micro) │   │ Scoring │
    └────┬────┘   └────┬────┘   └────┬────┘
         │             │              │
         └─────────────┼──────────────┘
                       │
               ┌───────▼───────┐
               │    SERVING    │
               └───────────────┘
```

## Patterns de chargement

### Full Load (Rechargement complet)

```sql
-- Truncate + Insert
TRUNCATE TABLE dim_products;

INSERT INTO dim_products
SELECT * FROM staging.products;
```

**Quand l'utiliser :**
- Tables de référence petites
- Données source sans historique
- Reconstruction nécessaire

### Incremental Load (Chargement incrémental)

```sql
-- Merge / Upsert
MERGE INTO dim_products target
USING staging.products source
ON target.product_id = source.product_id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;
```

**Quand l'utiliser :**
- Tables volumineuses
- Changements fréquents
- Performance critique

### Change Data Capture (CDC)

Capture les changements en temps réel depuis la source.

```
┌────────────┐    ┌─────────┐    ┌────────────┐
│   Source   │───►│   CDC   │───►│  Target    │
│    DB      │    │ (Debezium)   │    DW      │
└────────────┘    └─────────┘    └────────────┘
```

**Outils CDC :**
- Debezium
- Oracle GoldenGate
- AWS DMS
- Airbyte

## Points clés à retenir

- **Inmon** : DW centralisé normalisé, puis Data Marts
- **Kimball** : Data Marts dimensionnels, puis consolidation
- **Lakehouse** : Fusion DW + Data Lake avec ACID
- **Lambda** : Batch + Real-time en parallèle
- **Kappa** : Tout en streaming
- **CDC** : Capture des changements temps réel

---

**Prochain module :** [04 - Modélisation dimensionnelle](./04-modelisation.md)

[Module précédent](./02-oltp-vs-olap.md) | [Retour au sommaire](./README.md)
