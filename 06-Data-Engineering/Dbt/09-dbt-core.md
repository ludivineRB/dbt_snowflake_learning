# Chapitre 9 : dbt Core – Installation et Utilisation en Local

## 🎯 Objectifs
- Installer et configurer dbt Core en local
- Comprendre les differences entre dbt Cloud et dbt Core
- Configurer `profiles.yml` pour differents adaptateurs
- Developper un workflow dbt Core complet
- Orchestrer dbt sans dbt Cloud

## 1. dbt Cloud vs dbt Core

Jusqu'a present, nous avons travaille avec **dbt Cloud**, la version hebergee de dbt. Il existe egalement **dbt Core**, la version open-source en ligne de commande que vous installez et executez localement.

### 📊 Tableau comparatif

| Critere | dbt Core | dbt Cloud |
|---------|----------|-----------|
| **Prix** | Gratuit (open-source) | Gratuit (plan Developer) / Payant (Team, Enterprise) |
| **Installation** | Locale via `pip` | Aucune (SaaS) |
| **IDE** | Votre editeur prefere (VS Code, etc.) | IDE integre dans le navigateur |
| **CLI** | Oui, natif | Oui, via dbt Cloud CLI |
| **Scheduling** | A configurer (cron, Airflow, etc.) | Integre (Jobs, Scheduling) |
| **CI/CD** | A configurer (GitHub Actions, etc.) | Integre (Slim CI) |
| **Collaboration** | Via Git uniquement | Interface collaborative integree |
| **Documentation** | `dbt docs serve` en local | Hebergee automatiquement |
| **Logs et monitoring** | Fichiers locaux (`logs/`) | Dashboard integre |
| **Adaptateurs** | Tous disponibles | Principaux (Snowflake, BigQuery, etc.) |

### 🤔 Quand utiliser chacun ?

**dbt Core** est recommande quand :
- Vous avez besoin d'un **controle total** sur votre environnement
- Vous travaillez avec un adaptateur **non supporte** par dbt Cloud
- Votre equipe a deja un **orchestrateur** en place (Airflow, Dagster)
- Vous souhaitez **eviter les couts** de licence dbt Cloud Team/Enterprise
- Vous devez respecter des contraintes de **securite** (pas de SaaS)

**dbt Cloud** est recommande quand :
- Vous voulez un demarrage **rapide** sans configuration
- Vous avez besoin de **scheduling et CI/CD integres**
- L'equipe data est **non technique** et apprecie l'IDE web
- Vous souhaitez un **monitoring centralise**

> 💡 **Conseil** : Les deux outils utilisent le meme langage dbt (SQL + Jinja). Un projet dbt est **100% portable** entre dbt Core et dbt Cloud.

## 2. Installation de dbt Core

### 🐍 Pre-requis

- **Python** 3.9 ou superieur
- **pip** (gestionnaire de packages Python)
- **Git** installe et configure

### 2.1. Creation d'un environnement virtuel

Il est fortement recommande d'utiliser **uv** pour gerer votre environnement Python.

```bash
# Creer un dossier pour le projet
mkdir mon-projet-dbt && cd mon-projet-dbt

# Initialiser le projet avec uv
uv init

# uv cree automatiquement :
# - pyproject.toml (dependances)
# - .venv/ (environnement virtuel)
# - .python-version
```

> 💡 **Conseil** : Avec uv, pas besoin d'activer l'environnement virtuel manuellement. Utilisez `uv run dbt ...` pour executer dbt dans le bon environnement.

### 2.2. Installation de dbt Core avec un adaptateur

dbt Core s'installe separement de l'adaptateur de base de donnees. Installez **uniquement l'adaptateur dont vous avez besoin** :

```bash
# Pour PostgreSQL
uv add dbt-core dbt-postgres

# Pour BigQuery
uv add dbt-core dbt-bigquery

# Pour Snowflake
uv add dbt-core dbt-snowflake

# Pour DuckDB (leger, ideal pour l'apprentissage)
uv add dbt-core dbt-duckdb

# Pour installer plusieurs adaptateurs
uv add dbt-core dbt-postgres dbt-bigquery
```

### 2.3. Verification de l'installation

```bash
# Verifier la version installee
dbt --version
```

Vous devriez obtenir une sortie similaire a :

```
Core:
  - installed: 1.9.1
  - latest:    1.9.1 - Up to date!

Plugins:
  - postgres: 1.9.0 - Up to date!
```

### 2.4. Figer les dependances

Avec uv, les dependances sont gerees automatiquement dans `pyproject.toml` et verrouillees dans `uv.lock` :

```bash
# Les dependances sont deja dans pyproject.toml grace a `uv add`
# Pour reinstaller sur un autre poste :
uv sync
```

Exemple de `pyproject.toml` :

```toml
[project]
name = "mon-projet-dbt"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "dbt-core>=1.9.1",
    "dbt-postgres>=1.9.0",
]
```

## 3. Configuration de `profiles.yml`

Le fichier `profiles.yml` est le **point central de la configuration des connexions** en dbt Core. Il definit comment dbt se connecte a votre base de donnees.

### 3.1. Emplacement du fichier

Par defaut, dbt cherche ce fichier dans le repertoire `~/.dbt/` :

```
~/.dbt/
└── profiles.yml
```

```bash
# Creer le repertoire s'il n'existe pas
mkdir -p ~/.dbt
```

> ⚠️ **Attention** : Ne commitez **jamais** `profiles.yml` dans Git ! Ce fichier contient des informations de connexion sensibles. Il doit rester dans `~/.dbt/` ou etre reference via des variables d'environnement.

### 3.2. Structure generale

```yaml
# ~/.dbt/profiles.yml

nom_du_profil:
  target: dev           # Environnement par defaut
  outputs:
    dev:                 # Configuration de l'environnement "dev"
      type: postgres     # Type d'adaptateur
      host: localhost
      port: 5432
      user: mon_user
      password: mon_password
      dbname: ma_base
      schema: dev_schema
      threads: 4         # Nombre de modeles executes en parallele

    prod:                # Configuration de l'environnement "prod"
      type: postgres
      host: prod-server.example.com
      port: 5432
      user: dbt_prod
      password: "{{ env_var('DBT_PROD_PASSWORD') }}"
      dbname: production_db
      schema: analytics
      threads: 8
```

> 💡 **Conseil** : Le nom du profil dans `profiles.yml` doit correspondre exactement au champ `profile` dans votre `dbt_project.yml`.

### 3.3. Exemple pour PostgreSQL

```yaml
ecommerce_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: dbt_user
      password: "{{ env_var('DBT_PG_PASSWORD') }}"
      dbname: ecommerce
      schema: dbt_dev
      threads: 4
      keepalives_idle: 0
      connect_timeout: 10
      retries: 3

    prod:
      type: postgres
      host: "{{ env_var('DBT_PG_HOST') }}"
      port: 5432
      user: "{{ env_var('DBT_PG_USER') }}"
      password: "{{ env_var('DBT_PG_PASSWORD') }}"
      dbname: ecommerce
      schema: analytics
      threads: 8
```

### 3.4. Exemple pour BigQuery

```yaml
ecommerce_project:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: mon-projet-gcp-dev
      dataset: dbt_dev
      threads: 4
      timeout_seconds: 300
      location: EU
      keyfile: "{{ env_var('DBT_BQ_KEYFILE') }}"
      # Ou directement le chemin :
      # keyfile: /chemin/vers/service-account.json

    prod:
      type: bigquery
      method: service-account
      project: mon-projet-gcp-prod
      dataset: analytics
      threads: 8
      timeout_seconds: 600
      location: EU
      keyfile: "{{ env_var('DBT_BQ_KEYFILE') }}"
```

### 3.5. Exemple pour Snowflake

```yaml
ecommerce_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('DBT_SF_ACCOUNT') }}"
      user: "{{ env_var('DBT_SF_USER') }}"
      password: "{{ env_var('DBT_SF_PASSWORD') }}"
      role: transform
      database: ECOMMERCE
      warehouse: COMPUTE_WH
      schema: dbt_dev
      threads: 4

    prod:
      type: snowflake
      account: "{{ env_var('DBT_SF_ACCOUNT') }}"
      user: "{{ env_var('DBT_SF_USER') }}"
      password: "{{ env_var('DBT_SF_PASSWORD') }}"
      role: transform
      database: ECOMMERCE
      warehouse: COMPUTE_WH
      schema: analytics
      threads: 8
```

### 3.6. Variables d'environnement pour les credentials

Plutot que de stocker les mots de passe en clair, utilisez des **variables d'environnement** :

```bash
# Dans votre fichier ~/.bashrc, ~/.zshrc ou .env
export DBT_PG_PASSWORD="mon_mot_de_passe_secret"
export DBT_PG_HOST="prod-server.example.com"
export DBT_PG_USER="dbt_prod"
export DBT_BQ_KEYFILE="/chemin/vers/service-account.json"
export DBT_SF_ACCOUNT="xy12345.eu-west-1"
export DBT_SF_USER="dbt"
export DBT_SF_PASSWORD="MonMotDePasse123"
```

Dans `profiles.yml`, referencez-les avec la syntaxe Jinja :

```yaml
password: "{{ env_var('DBT_PG_PASSWORD') }}"
```

> 💡 **Conseil** : Vous pouvez aussi utiliser un fichier `.env` avec un outil comme `direnv` ou `python-dotenv` pour charger automatiquement les variables d'environnement par projet.

### 3.7. Changer de target (environnement)

```bash
# Utiliser l'environnement par defaut (dev)
dbt run

# Utiliser un environnement specifique
dbt run --target prod

# Verifier quel profil est utilise
dbt debug
```

## 4. Initialisation d'un projet dbt Core

### 4.1. Commande `dbt init`

```bash
# Initialiser un nouveau projet
dbt init mon_projet
```

dbt vous posera quelques questions :

```
Which database would you like to use?
[1] postgres
[2] bigquery
[3] snowflake

Enter a number: 1
```

### 4.2. Structure generee

```
mon_projet/
├── dbt_project.yml          # Configuration principale du projet
├── README.md                # Documentation du projet
├── models/                  # Dossier des modeles SQL
│   └── example/             # Modeles d'exemple (a supprimer)
│       ├── my_first_dbt_model.sql
│       ├── my_second_dbt_model.sql
│       └── schema.yml
├── analyses/                # Analyses ad-hoc
├── tests/                   # Tests personnalises (singular tests)
├── seeds/                   # Fichiers CSV statiques
├── snapshots/               # Historisation des donnees (SCD)
├── macros/                  # Fonctions Jinja reutilisables
└── target/                  # Fichiers compiles (genere automatiquement)
```

### 4.3. Configuration de `dbt_project.yml`

Editez le fichier `dbt_project.yml` pour l'adapter a votre projet :

```yaml
name: 'ecommerce'
version: '1.0.0'
config-version: 2

# Le profil doit correspondre a celui de profiles.yml
profile: 'ecommerce_project'

# Repertoires
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

# Configuration des modeles par repertoire
models:
  ecommerce:
    staging:
      +materialized: view
      +schema: staging

    intermediate:
      +materialized: ephemeral

    marts:
      +materialized: table
      +schema: marts

# Configuration des seeds
seeds:
  ecommerce:
    +schema: seeds
```

### 4.4. Fichier `packages.yml` pour les dependances

Creez un fichier `packages.yml` a la racine du projet pour gerer les packages externes :

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.3.0

  - package: calogica/dbt_expectations
    version: 0.10.4

  - package: dbt-labs/codegen
    version: 0.12.1
```

Installez les packages :

```bash
dbt deps
```

## 5. Workflow de developpement local

Voici l'enchainement typique des commandes pour developper avec dbt Core.

### 5.1. Verifier la connexion

```bash
# Diagnostiquer la configuration et la connexion
dbt debug
```

Sortie attendue :

```
All checks passed!
```

Si une erreur apparait, verifiez :
1. Que `profiles.yml` existe dans `~/.dbt/`
2. Que le nom du profil correspond a `dbt_project.yml`
3. Que les credentials sont corrects
4. Que la base de donnees est accessible

### 5.2. Installer les dependances

```bash
# Installer les packages definis dans packages.yml
dbt deps
```

### 5.3. Charger les seeds

```bash
# Charger tous les fichiers CSV dans la base de donnees
dbt seed

# Charger un seed specifique
dbt seed --select countries

# Recharger en ecrasant les donnees existantes
dbt seed --full-refresh
```

### 5.4. Executer les modeles

```bash
# Executer tous les modeles
dbt run

# Executer un modele specifique
dbt run --select stg_customers

# Executer un modele et toutes ses dependances amont
dbt run --select +fct_orders

# Executer un modele et tous ses descendants
dbt run --select stg_customers+

# Executer tous les modeles d'un repertoire
dbt run --select staging.*
```

### 5.5. Lancer les tests

```bash
# Executer tous les tests
dbt test

# Tester un modele specifique
dbt test --select stg_customers

# Tester uniquement les tests unitaires
dbt test --select test_type:unit
```

### 5.6. Pipeline complet avec `dbt build`

```bash
# Executer seed + run + test dans le bon ordre
dbt build

# Build d'un sous-ensemble
dbt build --select +fct_orders+

# Build avec full refresh (recrée tout)
dbt build --full-refresh
```

### 5.7. Generer et consulter la documentation

```bash
# Generer la documentation
dbt docs generate

# Servir la documentation dans le navigateur
dbt docs serve
# Ouvre automatiquement http://localhost:8080
```

### 📊 Resume du workflow

```
dbt debug          → Verifier la connexion
    ↓
dbt deps           → Installer les packages
    ↓
dbt seed           → Charger les CSV de reference
    ↓
dbt run            → Executer les modeles SQL
    ↓
dbt test           → Valider la qualite des donnees
    ↓
dbt docs generate  → Generer la documentation
dbt docs serve     → Consulter la documentation
```

> 💡 **Conseil** : En developpement, preferez `dbt run --select mon_modele` pour iterer rapidement sur un seul modele plutot que d'executer tout le projet a chaque modification.

## 6. Exemple complet avec PostgreSQL

Nous allons construire un **pipeline e-commerce complet** avec dbt Core et PostgreSQL.

### 6.1. Lancer PostgreSQL avec Docker

Creez un fichier `docker-compose.yml` a la racine du projet :

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: dbt_postgres
    environment:
      POSTGRES_USER: dbt_user
      POSTGRES_PASSWORD: dbt_password
      POSTGRES_DB: ecommerce
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d

volumes:
  postgres_data:
```

Demarrez le conteneur :

```bash
docker compose up -d
```

### 6.2. Donnees sources (seeds)

Creez les fichiers CSV dans le dossier `seeds/` :

**`seeds/raw_customers.csv`** :
```csv
customer_id,first_name,last_name,email,created_at,country
1,Marie,Dupont,marie.dupont@email.fr,2023-01-15,France
2,Jean,Martin,jean.martin@email.fr,2023-02-20,France
3,Sophie,Bernard,sophie.b@email.be,2023-03-10,Belgique
4,Lucas,Mueller,lucas.m@email.de,2023-04-05,Allemagne
5,Emma,Rossi,emma.r@email.it,2023-05-18,Italie
```

**`seeds/raw_products.csv`** :
```csv
product_id,product_name,category,unit_price
101,T-shirt Classique,Vetements,19.99
102,Jean Slim,Vetements,49.99
103,Baskets Running,Chaussures,89.99
104,Sac a dos,Accessoires,34.99
105,Casquette Sport,Accessoires,14.99
```

**`seeds/raw_orders.csv`** :
```csv
order_id,customer_id,order_date,status,total_amount
1001,1,2024-01-10,completed,69.98
1002,2,2024-01-15,completed,89.99
1003,1,2024-02-01,completed,49.98
1004,3,2024-02-14,completed,124.98
1005,4,2024-03-01,shipped,34.99
1006,5,2024-03-15,completed,109.98
1007,1,2024-04-02,completed,19.99
1008,2,2024-04-20,cancelled,49.99
```

**`seeds/raw_order_items.csv`** :
```csv
order_item_id,order_id,product_id,quantity,unit_price
1,1001,101,2,19.99
2,1001,105,2,14.99
3,1002,103,1,89.99
4,1003,102,1,49.99
5,1004,103,1,89.99
6,1004,104,1,34.99
7,1005,104,1,34.99
8,1006,102,1,49.99
9,1006,101,3,19.99
10,1007,101,1,19.99
11,1008,102,1,49.99
```

### 6.3. Configuration de `profiles.yml`

```yaml
# ~/.dbt/profiles.yml

ecommerce_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: dbt_user
      password: dbt_password
      dbname: ecommerce
      schema: public
      threads: 4
```

### 6.4. Definition des sources

Creez le fichier `models/staging/sources.yml` :

```yaml
version: 2

sources:
  - name: raw
    description: "Donnees brutes e-commerce chargees via dbt seed"
    schema: seeds
    tables:
      - name: raw_customers
        description: "Table brute des clients"
        columns:
          - name: customer_id
            description: "Identifiant unique du client"
            tests:
              - unique
              - not_null

      - name: raw_orders
        description: "Table brute des commandes"
        columns:
          - name: order_id
            description: "Identifiant unique de la commande"
            tests:
              - unique
              - not_null
          - name: customer_id
            tests:
              - not_null
              - relationships:
                  to: source('raw', 'raw_customers')
                  field: customer_id

      - name: raw_order_items
        description: "Table brute des lignes de commande"
        columns:
          - name: order_item_id
            tests:
              - unique
              - not_null

      - name: raw_products
        description: "Table brute des produits"
        columns:
          - name: product_id
            tests:
              - unique
              - not_null
```

### 6.5. Modeles staging

**`models/staging/stg_customers.sql`** :

```sql
with source as (
    select * from {{ source('raw', 'raw_customers') }}
),

renamed as (
    select
        customer_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as full_name,
        lower(trim(email)) as email,
        cast(created_at as date) as created_at,
        trim(country) as country
    from source
)

select * from renamed
```

**`models/staging/stg_orders.sql`** :

```sql
with source as (
    select * from {{ source('raw', 'raw_orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        cast(order_date as date) as order_date,
        lower(trim(status)) as status,
        cast(total_amount as numeric(10, 2)) as total_amount
    from source
)

select * from renamed
```

**`models/staging/stg_products.sql`** :

```sql
with source as (
    select * from {{ source('raw', 'raw_products') }}
),

renamed as (
    select
        product_id,
        trim(product_name) as product_name,
        trim(category) as category,
        cast(unit_price as numeric(10, 2)) as unit_price
    from source
)

select * from renamed
```

**`models/staging/stg_order_items.sql`** :

```sql
with source as (
    select * from {{ source('raw', 'raw_order_items') }}
),

renamed as (
    select
        order_item_id,
        order_id,
        product_id,
        quantity,
        cast(unit_price as numeric(10, 2)) as unit_price,
        cast(quantity * unit_price as numeric(10, 2)) as line_total
    from source
)

select * from renamed
```

### 6.6. Modele intermediaire

**`models/intermediate/int_order_items.sql`** :

```sql
{{
    config(
        materialized='ephemeral'
    )
}}

-- Enrichissement des lignes de commande avec les informations produit
with order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

enriched as (
    select
        oi.order_item_id,
        oi.order_id,
        oi.product_id,
        p.product_name,
        p.category,
        oi.quantity,
        oi.unit_price,
        oi.line_total
    from order_items oi
    inner join products p
        on oi.product_id = p.product_id
)

select * from enriched
```

### 6.7. Modeles marts

**`models/marts/fct_orders.sql`** :

```sql
{{
    config(
        materialized='table'
    )
}}

-- Table de faits des commandes
with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('int_order_items') }}
),

order_items_agg as (
    select
        order_id,
        count(*) as nb_items,
        sum(quantity) as total_quantity,
        sum(line_total) as calculated_total,
        count(distinct product_id) as nb_distinct_products,
        count(distinct category) as nb_distinct_categories
    from order_items
    group by order_id
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        o.status,
        o.total_amount,
        oia.nb_items,
        oia.total_quantity,
        oia.calculated_total,
        oia.nb_distinct_products,
        oia.nb_distinct_categories
    from orders o
    left join order_items_agg oia
        on o.order_id = oia.order_id
)

select * from final
```

**`models/marts/dim_customers.sql`** :

```sql
{{
    config(
        materialized='table'
    )
}}

-- Dimension clients enrichie avec les metriques de commandes
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('fct_orders') }}
),

customer_orders as (
    select
        customer_id,
        count(order_id) as nb_orders,
        sum(case when status = 'completed' then total_amount else 0 end) as lifetime_value,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        avg(total_amount) as avg_order_amount
    from orders
    where status != 'cancelled'
    group by customer_id
),

final as (
    select
        c.customer_id,
        c.full_name,
        c.email,
        c.country,
        c.created_at,
        coalesce(co.nb_orders, 0) as nb_orders,
        coalesce(co.lifetime_value, 0) as lifetime_value,
        co.first_order_date,
        co.last_order_date,
        coalesce(co.avg_order_amount, 0) as avg_order_amount,
        case
            when co.nb_orders is null then 'Prospect'
            when co.nb_orders = 1 then 'Nouveau'
            when co.nb_orders between 2 and 4 then 'Regulier'
            else 'Fidele'
        end as customer_segment
    from customers c
    left join customer_orders co
        on c.customer_id = co.customer_id
)

select * from final
```

**`models/marts/dim_products.sql`** :

```sql
{{
    config(
        materialized='table'
    )
}}

-- Dimension produits enrichie avec les metriques de ventes
with products as (
    select * from {{ ref('stg_products') }}
),

order_items as (
    select * from {{ ref('int_order_items') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

-- Ne compter que les commandes non annulees
valid_order_items as (
    select oi.*
    from order_items oi
    inner join orders o
        on oi.order_id = o.order_id
    where o.status != 'cancelled'
),

product_sales as (
    select
        product_id,
        count(distinct order_id) as nb_orders,
        sum(quantity) as total_quantity_sold,
        sum(line_total) as total_revenue
    from valid_order_items
    group by product_id
),

final as (
    select
        p.product_id,
        p.product_name,
        p.category,
        p.unit_price,
        coalesce(ps.nb_orders, 0) as nb_orders,
        coalesce(ps.total_quantity_sold, 0) as total_quantity_sold,
        coalesce(ps.total_revenue, 0) as total_revenue,
        case
            when ps.total_revenue is null then 'Aucune vente'
            when ps.total_revenue < 50 then 'Faible'
            when ps.total_revenue < 200 then 'Moyen'
            else 'Fort'
        end as sales_performance
    from products p
    left join product_sales ps
        on p.product_id = ps.product_id
)

select * from final
```

### 6.8. Tests et documentation

Creez le fichier `models/marts/schema.yml` :

```yaml
version: 2

models:
  - name: fct_orders
    description: "Table de faits des commandes enrichie avec les agregations par commande"
    columns:
      - name: order_id
        description: "Identifiant unique de la commande"
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "Identifiant du client"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: status
        description: "Statut de la commande"
        tests:
          - accepted_values:
              values: ['completed', 'shipped', 'cancelled', 'pending']
      - name: total_amount
        description: "Montant total de la commande"
        tests:
          - not_null

  - name: dim_customers
    description: "Dimension clients avec metriques de commandes et segmentation"
    columns:
      - name: customer_id
        description: "Identifiant unique du client"
        tests:
          - unique
          - not_null
      - name: email
        description: "Adresse e-mail du client (en minuscules)"
        tests:
          - unique
          - not_null
      - name: customer_segment
        description: "Segment client base sur le nombre de commandes"
        tests:
          - accepted_values:
              values: ['Prospect', 'Nouveau', 'Regulier', 'Fidele']

  - name: dim_products
    description: "Dimension produits avec metriques de ventes"
    columns:
      - name: product_id
        description: "Identifiant unique du produit"
        tests:
          - unique
          - not_null
      - name: unit_price
        description: "Prix unitaire du produit"
        tests:
          - not_null
```

### 6.9. Execution du pipeline

```bash
# 1. Verifier la connexion
dbt debug

# 2. Installer les packages
dbt deps

# 3. Charger les seeds
dbt seed

# 4. Executer tout le pipeline (seed + run + test)
dbt build

# 5. Generer et consulter la documentation
dbt docs generate && dbt docs serve
```

## 7. Exemple avec BigQuery

### 7.1. Configuration du service account

Pour utiliser dbt avec BigQuery, vous devez creer un **service account** GCP :

1. Rendez-vous dans la [console GCP](https://console.cloud.google.com)
2. Allez dans **IAM & Admin** → **Service Accounts**
3. Cliquez **Create Service Account**
4. Donnez-lui un nom : `dbt-service-account`
5. Attribuez les roles :
   - `BigQuery Data Editor`
   - `BigQuery Job User`
6. Creez une cle JSON et telecharger-la

```bash
# Placez la cle dans un endroit securise
mkdir -p ~/.gcp
mv ~/Downloads/mon-projet-gcp-xxxxx.json ~/.gcp/dbt-service-account.json

# Definissez la variable d'environnement
export DBT_BQ_KEYFILE="$HOME/.gcp/dbt-service-account.json"
```

### 7.2. Configuration `profiles.yml` pour BigQuery

```yaml
ecommerce_project:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: mon-projet-gcp
      dataset: dbt_dev
      threads: 4
      timeout_seconds: 300
      location: EU
      keyfile: "{{ env_var('DBT_BQ_KEYFILE') }}"
      priority: interactive
      retries: 3
```

### 7.3. Differences cles avec l'adaptateur PostgreSQL

| Aspect | PostgreSQL | BigQuery |
|--------|-----------|----------|
| **Schema** | `schema` | `dataset` |
| **Authentification** | user/password | Service account (keyfile) |
| **Types de donnees** | `VARCHAR`, `INTEGER` | `STRING`, `INT64` |
| **Materialisation** | Tables standard | Tables + vues materialisees |
| **Partitionnement** | Natif PostgreSQL | `partition_by` dans config |
| **Clustering** | Index | `cluster_by` dans config |
| **Couts** | Infrastructure fixe | Pay-per-query |

### 7.4. Configuration specifique BigQuery dans les modeles

```sql
{{
    config(
        materialized='table',
        partition_by={
            "field": "order_date",
            "data_type": "date",
            "granularity": "month"
        },
        cluster_by=["status", "customer_id"]
    )
}}

select * from {{ ref('stg_orders') }}
```

## 8. Orchestration sans dbt Cloud

Quand vous utilisez dbt Core, le scheduling et le CI/CD sont a votre charge. Voici les principales options.

### 8.1. Cron jobs (simple)

Pour une execution quotidienne basique :

```bash
# Editer la crontab
crontab -e

# Executer dbt build tous les jours a 6h00
0 6 * * * cd /chemin/vers/mon-projet-dbt && uv run dbt build --target prod >> /var/log/dbt/daily_run.log 2>&1
```

> ⚠️ **Attention** : Les cron jobs ne gerent pas les erreurs de maniere sophistiquee. Preferez un orchestrateur pour la production.

### 8.2. Apache Airflow

Airflow est l'orchestrateur le plus populaire pour les pipelines dbt en production.

#### Avec BashOperator

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_daily_pipeline',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    catchup=False,
    tags=['dbt', 'ecommerce'],
) as dag:

    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command='cd /opt/dbt/ecommerce && dbt deps',
    )

    dbt_seed = BashOperator(
        task_id='dbt_seed',
        bash_command='cd /opt/dbt/ecommerce && dbt seed --target prod',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/dbt/ecommerce && dbt run --target prod',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/dbt/ecommerce && dbt test --target prod',
    )

    dbt_docs = BashOperator(
        task_id='dbt_docs_generate',
        bash_command='cd /opt/dbt/ecommerce && dbt docs generate --target prod',
    )

    dbt_deps >> dbt_seed >> dbt_run >> dbt_test >> dbt_docs
```

### 8.3. GitHub Actions pour CI/CD

Creez le fichier `.github/workflows/dbt_ci.yml` :

```yaml
name: dbt CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

env:
  DBT_PROFILES_DIR: ./
  DBT_PG_HOST: localhost
  DBT_PG_USER: dbt_user
  DBT_PG_PASSWORD: dbt_password

jobs:
  dbt-ci:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: dbt_user
          POSTGRES_PASSWORD: dbt_password
          POSTGRES_DB: ecommerce
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Installation de Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Installation de uv
        uses: astral-sh/setup-uv@v4

      - name: Installation des dependances
        run: |
          uv sync
          uv run dbt deps

      - name: Verification de la connexion
        run: dbt debug

      - name: Chargement des seeds
        run: dbt seed

      - name: Execution des modeles
        run: dbt run

      - name: Execution des tests
        run: dbt test

      - name: Generation de la documentation
        run: dbt docs generate
```

Pour que ce workflow fonctionne, creez un fichier `profiles.yml` a la racine du projet (uniquement pour la CI, avec des variables d'environnement) :

```yaml
# profiles.yml (a la racine, pour CI uniquement)
ecommerce_project:
  target: ci
  outputs:
    ci:
      type: postgres
      host: "{{ env_var('DBT_PG_HOST') }}"
      port: 5432
      user: "{{ env_var('DBT_PG_USER') }}"
      password: "{{ env_var('DBT_PG_PASSWORD') }}"
      dbname: ecommerce
      schema: ci_test
      threads: 4
```

> ⚠️ **Attention** : Ce `profiles.yml` de CI est different de votre `~/.dbt/profiles.yml` local. Il utilise uniquement des variables d'environnement et un schema dedie `ci_test`.

### 8.4. Makefile pour les commandes courantes

Creez un `Makefile` a la racine du projet pour simplifier les commandes :

```makefile
.PHONY: setup run test build docs clean fresh lint

# Configuration initiale
setup:
	uv sync
	uv run dbt deps
	uv run dbt debug

# Charger les seeds
seed:
	dbt seed

# Executer les modeles
run:
	dbt run

# Lancer les tests
test:
	dbt test

# Pipeline complet (seed + run + test)
build:
	dbt build

# Generer et servir la documentation
docs:
	dbt docs generate
	dbt docs serve

# Full refresh de tous les modeles
fresh:
	dbt build --full-refresh

# Nettoyer les fichiers generes
clean:
	dbt clean
	rm -rf target/ dbt_packages/ logs/

# Linter SQL avec sqlfluff (si installe)
lint:
	sqlfluff lint models/ --dialect postgres

# Demarrer PostgreSQL avec Docker
db-up:
	docker compose up -d

# Arreter PostgreSQL
db-down:
	docker compose down

# Pipeline complet depuis zero
all: db-up setup seed build docs
```

Utilisation :

```bash
# Premiere mise en place
make all

# Developpement quotidien
make build

# Generer la documentation
make docs

# Nettoyer et repartir de zero
make clean fresh
```

## 9. Bonnes pratiques dbt Core

### 9.1. Fichier `.gitignore`

Creez un `.gitignore` adapte a dbt :

```gitignore
# dbt
target/
dbt_packages/
logs/
dbt_modules/

# Environnement Python
.venv/
__pycache__/
*.pyc

# IDE
.vscode/
.idea/

# Variables d'environnement
.env
.env.local

# Ne JAMAIS commiter profiles.yml personnel
# (sauf le profiles.yml de CI avec env vars uniquement)
# profiles.yml

# OS
.DS_Store
Thumbs.db
```

### 9.2. Securite de `profiles.yml`

Regles imperatives :
1. **Ne jamais commiter** `~/.dbt/profiles.yml` dans Git
2. Utiliser des **variables d'environnement** pour les credentials
3. Avoir un `profiles.yml` de CI separe avec uniquement des `env_var()`
4. Verifier que `.gitignore` exclut bien les fichiers sensibles

### 9.3. Pre-commit hooks avec sqlfluff

Installez sqlfluff pour verifier la qualite du SQL automatiquement :

```bash
uv add sqlfluff sqlfluff-templater-dbt pre-commit
```

Creez `.sqlfluff` a la racine du projet :

```ini
[sqlfluff]
templater = dbt
dialect = postgres
max_line_length = 120
indent_unit = space

[sqlfluff:indentation]
tab_space_size = 4

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.identifiers]
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.functions]
capitalisation_policy = lower
```

Creez `.pre-commit-config.yaml` :

```yaml
repos:
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.2.5
    hooks:
      - id: sqlfluff-lint
        additional_dependencies:
          - sqlfluff-templater-dbt
          - dbt-postgres
      - id: sqlfluff-fix
        additional_dependencies:
          - sqlfluff-templater-dbt
          - dbt-postgres
```

Installez les hooks :

```bash
pre-commit install
```

### 9.4. Conventions de structure du projet

```
mon_projet_dbt/
├── models/
│   ├── staging/          # stg_  : nettoyage des sources
│   │   ├── sources.yml
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   └── stg_products.sql
│   ├── intermediate/     # int_  : logique metier intermediaire
│   │   └── int_order_items.sql
│   └── marts/            # fct_  / dim_  : tables finales
│       ├── schema.yml
│       ├── fct_orders.sql
│       ├── dim_customers.sql
│       └── dim_products.sql
├── seeds/                # Donnees de reference (CSV)
├── snapshots/            # SCD Type 2
├── tests/                # Tests personnalises
├── macros/               # Fonctions reutilisables
├── analyses/             # Requetes ad-hoc
├── dbt_project.yml
├── packages.yml
├── docker-compose.yml
├── Makefile
├── .gitignore
├── .sqlfluff
└── .pre-commit-config.yaml
```

| Prefixe | Couche | Materialisation | Objectif |
|---------|--------|-----------------|----------|
| `stg_` | Staging | View | Nettoyage, renommage, typage |
| `int_` | Intermediate | Ephemeral | Jointures, logique metier |
| `fct_` | Marts | Table | Tables de faits |
| `dim_` | Marts | Table | Tables de dimensions |
| `mart_` | Marts | Table | Agregations metier |

## 🎯 Points cles a retenir

1. **dbt Core est gratuit** et open-source, ideal pour les equipes ayant des contraintes de budget ou de securite
2. **`profiles.yml`** centralise la configuration des connexions — ne le commitez jamais avec des mots de passe
3. **Les environnements virtuels** Python sont indispensables pour isoler les dependances
4. **`dbt build`** est la commande principale qui enchaine seed, run et test dans le bon ordre
5. **L'orchestration** doit etre mise en place separement (Airflow, GitHub Actions, cron)
6. **Le projet est portable** : un meme projet fonctionne avec dbt Core et dbt Cloud

## ✅ Checklist de validation

- [ ] Python 3.9+ et pip sont installes
- [ ] Un environnement virtuel est cree et active
- [ ] dbt Core et l'adaptateur sont installes (`dbt --version`)
- [ ] `profiles.yml` est configure dans `~/.dbt/`
- [ ] `dbt debug` retourne "All checks passed!"
- [ ] Un projet est initialise avec `dbt init`
- [ ] `dbt_project.yml` est configure correctement
- [ ] Les seeds sont charges avec `dbt seed`
- [ ] Les modeles s'executent sans erreur avec `dbt run`
- [ ] Les tests passent avec `dbt test`
- [ ] La documentation est accessible via `dbt docs serve`
- [ ] `.gitignore` exclut `target/`, `dbt_packages/` et `logs/`
- [ ] Les credentials utilisent des variables d'environnement

---

**Etape precedente** : [Chapitre 8 - Variables DBT](08-variables.md)
**Prochaine etape** : [Exercices dbt](10-exercices.md)
