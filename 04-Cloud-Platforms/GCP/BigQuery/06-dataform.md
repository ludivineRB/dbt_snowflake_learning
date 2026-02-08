# Module 06 - Orchestration avec Dataform

## Qu'est-ce que Dataform ?

Dataform est l'outil d'orchestration SQL intégré nativement à BigQuery (racheté par Google). C'est l'équivalent GCP de **dbt**.

### Caractéristiques

| Fonctionnalité | Description |
|----------------|-------------|
| **SQLX** | SQL étendu avec Jinja-like templating |
| **Dépendances** | Gestion automatique de l'ordre d'exécution |
| **Tests** | Assertions de qualité intégrées |
| **Documentation** | Auto-générée |
| **Git** | Versionning natif |
| **Scheduling** | Planification intégrée |

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     DATAFORM                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐         │
│  │  Git Repo  │  │ Development│  │ Scheduler  │         │
│  │  (source)  │→ │ Workspace  │→ │  (cron)    │         │
│  └────────────┘  └────────────┘  └────────────┘         │
│                         │                                │
│                         ▼                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │               BIGQUERY                            │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐          │   │
│  │  │ Bronze  │→ │ Silver  │→ │  Gold   │          │   │
│  │  └─────────┘  └─────────┘  └─────────┘          │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Setup Dataform

### Créer un repository

1. Console GCP → BigQuery → Dataform
2. "Create repository"
3. Configurer :
   - **Name** : `formation-medallion`
   - **Region** : `europe-west1` (même que vos datasets)
   - **Git provider** : GitHub, GitLab, ou Google Cloud Repository

### Créer un workspace

1. Dans le repository, "Create development workspace"
2. Nommer : `dev-workspace`
3. Initialiser avec le template par défaut

### Structure du projet

```
formation-medallion/
├── definitions/           # Modèles SQL
│   ├── bronze/
│   │   └── raw_sales.sqlx
│   ├── silver/
│   │   └── clean_sales.sqlx
│   └── gold/
│       ├── agg_sales_daily.sqlx
│       └── dm_customer_360.sqlx
├── includes/             # Fonctions réutilisables
│   └── utils.js
├── dataform.json         # Configuration projet
└── package.json          # Dépendances
```

### Configuration (dataform.json)

```json
{
    "warehouse": "bigquery",
    "defaultSchema": "dataform",
    "defaultDatabase": "mon-projet",
    "defaultLocation": "EU",
    "assertionSchema": "dataform_assertions"
}
```

## Syntaxe SQLX

### Modèle simple

```sql
-- definitions/silver/clean_sales.sqlx

config {
    type: "table",
    schema: "silver",
    name: "clean_sales",
    description: "Ventes nettoyées et validées",
    tags: ["silver", "daily"]
}

SELECT
    order_id,
    SAFE.PARSE_DATE('%Y-%m-%d', order_date) as order_date,
    LOWER(TRIM(customer_email)) as customer_email,
    SAFE_CAST(total_amount AS FLOAT64) as total_amount,
    CURRENT_TIMESTAMP() as processed_at
FROM ${ref("raw_sales")}  -- Référence au modèle Bronze
WHERE
    order_id IS NOT NULL
    AND SAFE_CAST(total_amount AS FLOAT64) > 0
```

### Types de matérialisation

```sql
-- TABLE : Crée/remplace une table
config { type: "table" }

-- VIEW : Crée une vue
config { type: "view" }

-- INCREMENTAL : Ajoute uniquement les nouvelles données
config {
    type: "incremental",
    uniqueKey: ["order_id"]
}

-- OPERATIONS : Script SQL libre
config { type: "operations" }
```

### Références et dépendances

```sql
-- definitions/gold/agg_sales_daily.sqlx

config {
    type: "table",
    schema: "gold"
}

-- ${ref("table_name")} crée une dépendance automatique
SELECT
    order_date,
    COUNT(DISTINCT order_id) as order_count,
    SUM(total_amount) as revenue
FROM ${ref("clean_sales")}  -- Dépend de silver.clean_sales
GROUP BY order_date
```

### Modèle incrémental

```sql
-- definitions/silver/clean_sales_incremental.sqlx

config {
    type: "incremental",
    schema: "silver",
    uniqueKey: ["order_id"],
    tags: ["incremental"]
}

SELECT
    order_id,
    SAFE.PARSE_DATE('%Y-%m-%d', order_date) as order_date,
    LOWER(TRIM(customer_email)) as customer_email,
    SAFE_CAST(total_amount AS FLOAT64) as total_amount
FROM ${ref("raw_sales")}

${when(incremental(), `
WHERE _ingested_at > (
    SELECT MAX(processed_at) FROM ${self()}
)
`)}
```

## Tests et assertions

### Assertions de qualité

```sql
-- definitions/silver/clean_sales.sqlx

config {
    type: "table",
    schema: "silver",
    assertions: {
        uniqueKey: ["order_id"],
        nonNull: ["order_id", "order_date", "customer_email"],
        rowConditions: [
            "total_amount > 0",
            "order_date >= '2020-01-01'"
        ]
    }
}

SELECT ...
```

### Assertions personnalisées

```sql
-- definitions/assertions/assert_no_orphan_orders.sqlx

config {
    type: "assertion",
    schema: "dataform_assertions"
}

-- Cette requête doit retourner 0 ligne pour passer
SELECT order_id
FROM ${ref("clean_sales")} s
LEFT JOIN ${ref("clean_customers")} c
    ON s.customer_email = c.email
WHERE c.email IS NULL
```

### Tests de fraîcheur

```sql
-- definitions/assertions/assert_fresh_data.sqlx

config {
    type: "assertion"
}

SELECT 'Data is stale' as error_message
WHERE (
    SELECT MAX(order_date)
    FROM ${ref("clean_sales")}
) < DATE_SUB(CURRENT_DATE(), INTERVAL 2 DAY)
```

## Variables et macros

### Variables de projet

```javascript
// includes/constants.js

const LOOKBACK_DAYS = 7;
const DEFAULT_COUNTRY = 'FR';

module.exports = { LOOKBACK_DAYS, DEFAULT_COUNTRY };
```

```sql
-- Utilisation dans SQLX
js {
    const { LOOKBACK_DAYS } = require("includes/constants");
}

SELECT *
FROM ${ref("clean_sales")}
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL ${LOOKBACK_DAYS} DAY)
```

### Macros réutilisables

```javascript
// includes/utils.js

function cleanEmail(column) {
    return `LOWER(TRIM(${column}))`;
}

function safeParseDate(column, format) {
    return `SAFE.PARSE_DATE('${format}', ${column})`;
}

module.exports = { cleanEmail, safeParseDate };
```

```sql
-- Utilisation
js {
    const { cleanEmail, safeParseDate } = require("includes/utils");
}

SELECT
    order_id,
    ${safeParseDate("order_date", "%Y-%m-%d")} as order_date,
    ${cleanEmail("customer_email")} as customer_email
FROM ${ref("raw_sales")}
```

## Exécution et planification

### Exécuter manuellement

Dans le workspace Dataform :
1. Sélectionner les modèles à exécuter
2. "Start Execution"
3. Choisir "Full refresh" ou "Incremental"

### Via l'API / CLI

```bash
# Installer dataform CLI (optionnel)
npm install -g @dataform/cli

# Compiler le projet
dataform compile

# Exécuter
dataform run
```

### Planification (Workflow)

1. Dataform → Repository → "Create release configuration"
2. Définir la branche Git (ex: `main`)
3. "Create workflow configuration"
4. Configurer :
   - **Schedule** : `0 6 * * *` (chaque jour à 6h)
   - **Tags** : `["daily"]` (optionnel)

## Exemple complet Medallion

### Bronze

```sql
-- definitions/bronze/raw_sales.sqlx

config {
    type: "table",
    schema: "bronze",
    description: "Données brutes des ventes"
}

SELECT
    CURRENT_TIMESTAMP() as _ingested_at,
    *
FROM EXTERNAL_QUERY(
    'gs://bucket/landing/sales/*.csv'
)
```

### Silver

```sql
-- definitions/silver/clean_sales.sqlx

config {
    type: "table",
    schema: "silver",
    description: "Ventes nettoyées",
    assertions: {
        uniqueKey: ["order_id"],
        nonNull: ["order_id", "order_date"]
    }
}

js { const { cleanEmail, safeParseDate } = require("includes/utils"); }

WITH deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY _ingested_at DESC) as rn
    FROM ${ref("raw_sales")}
)

SELECT
    order_id,
    ${safeParseDate("order_date", "%Y-%m-%d")} as order_date,
    ${cleanEmail("customer_email")} as customer_email,
    SAFE_CAST(total_amount AS FLOAT64) as total_amount
FROM deduplicated
WHERE rn = 1
    AND order_id IS NOT NULL
```

### Gold

```sql
-- definitions/gold/agg_sales_daily.sqlx

config {
    type: "table",
    schema: "gold",
    description: "Agrégation quotidienne des ventes"
}

SELECT
    order_date,
    COUNT(DISTINCT order_id) as order_count,
    COUNT(DISTINCT customer_email) as unique_customers,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as avg_order_value,
    CURRENT_TIMESTAMP() as refreshed_at
FROM ${ref("clean_sales")}
GROUP BY order_date
```

## DAG (Graphe de dépendances)

Dataform génère automatiquement le DAG :

```
raw_sales (bronze)
    │
    ▼
clean_sales (silver)
    │
    ├──────────────────┐
    ▼                  ▼
agg_sales_daily   dm_customer_360
    (gold)            (gold)
```

Visualisable dans l'interface Dataform.

## Points clés à retenir

- **Dataform** = dbt pour BigQuery (natif GCP)
- **SQLX** = SQL + configuration + templating
- **ref()** = crée les dépendances automatiquement
- **Assertions** = tests de qualité intégrés
- **Incrémental** = traitement des nouvelles données seulement
- **Scheduling** = planification via Workflow configurations
- **Git** = versionning et collaboration

---

**Prochain module :** [07 - Optimisation et bonnes pratiques](./07-optimisation.md)

[Module précédent](./05-automatisation.md) | [Retour au sommaire](./README.md)
