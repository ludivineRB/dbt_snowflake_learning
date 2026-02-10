# Exercices dbt

## 🎯 Objectifs
Mettre en pratique les concepts appris dans les chapitres precedents a travers des exercices progressifs couvrant la modelisation, les tests, les modeles incrementaux, les macros et un pipeline complet avec dbt Core.

---

## Exercice 1 : Modelisation staging et marts (⏱ 30 min)

### 📊 Niveau : Intermediaire

### 📝 Contexte

Vous disposez d'un jeu de donnees e-commerce brut compose de 4 tables :
- `raw_customers` (customer_id, first_name, last_name, email, created_at, country)
- `raw_orders` (order_id, customer_id, order_date, status, total_amount)
- `raw_order_items` (order_item_id, order_id, product_id, quantity, unit_price)
- `raw_products` (product_id, product_name, category, unit_price)

### 🎯 Objectifs de l'exercice

1. Creer les **modeles staging** avec le prefixe `stg_` pour chaque table source
2. Creer une **table de faits** `fct_orders` qui agrege les informations de commandes
3. Creer les **tables de dimensions** `dim_customers` et `dim_products`
4. Configurer les **materialisations** appropriees

### 📋 Consignes

#### Staging models (`models/staging/`)

Pour chaque table source, creer un modele staging qui :
- Renomme les colonnes si necessaire (nommage coherent)
- Nettoie les donnees (trim, lower pour les emails, cast des types)
- Est materialise en **view**

#### Table de faits (`models/marts/fct_orders.sql`)

La table `fct_orders` doit contenir :
- Les informations de base de la commande (order_id, customer_id, order_date, status)
- Le montant total de la commande
- Le nombre de lignes de commande
- La quantite totale d'articles
- Le nombre de produits distincts

Configuration : **materialized = table**

#### Tables de dimensions

**`dim_customers`** doit contenir :
- Informations du client
- Nombre total de commandes
- Montant total depense (lifetime value)
- Date de premiere et derniere commande

**`dim_products`** doit contenir :
- Informations du produit
- Nombre de commandes contenant ce produit
- Quantite totale vendue
- Revenu total genere

### ✅ Resultats attendus

```
models/
├── staging/
│   ├── stg_customers.sql       # view
│   ├── stg_orders.sql          # view
│   ├── stg_products.sql        # view
│   └── stg_order_items.sql     # view
└── marts/
    ├── fct_orders.sql          # table
    ├── dim_customers.sql       # table
    └── dim_products.sql        # table
```

Toutes les commandes suivantes doivent s'executer sans erreur :

```bash
dbt run
dbt test  # (si des tests existent deja)
```

### 💡 Indices

- Utilisez des CTEs (Common Table Expressions) pour structurer vos requetes
- La fonction `{{ source('raw', 'raw_customers') }}` reference une source
- La fonction `{{ ref('stg_customers') }}` reference un autre modele dbt
- Pensez a utiliser `coalesce()` pour gerer les valeurs nulles dans les agregations
- Configurez la materialisation avec `{{ config(materialized='table') }}`

---

## Exercice 2 : Tests et documentation (⏱ 30 min)

### 📊 Niveau : Intermediaire

### 📝 Contexte

Vous partez des modeles crees dans l'exercice 1 et devez ajouter une couche de **qualite de donnees** et de **documentation**.

### 🎯 Objectifs de l'exercice

1. Ajouter des **tests generiques** (unique, not_null, accepted_values, relationships)
2. Creer un **test personnalise** (singular test)
3. Documenter tous les modeles et colonnes dans `schema.yml`

### 📋 Consignes

#### Tests generiques dans `models/marts/schema.yml`

Ajoutez les tests suivants :

| Modele | Colonne | Tests |
|--------|---------|-------|
| `fct_orders` | `order_id` | `unique`, `not_null` |
| `fct_orders` | `customer_id` | `not_null`, `relationships` vers `dim_customers` |
| `fct_orders` | `status` | `accepted_values` : completed, shipped, cancelled, pending |
| `fct_orders` | `total_amount` | `not_null` |
| `dim_customers` | `customer_id` | `unique`, `not_null` |
| `dim_customers` | `email` | `unique`, `not_null` |
| `dim_products` | `product_id` | `unique`, `not_null` |
| `dim_products` | `unit_price` | `not_null` |

#### Test personnalise : `tests/assert_no_negative_order_total.sql`

Creez un test singular qui verifie qu'**aucune commande n'a un montant total negatif**. Le test echoue si des lignes sont retournees.

```sql
-- Le test echoue si cette requete retourne des lignes
select
    order_id,
    total_amount
from {{ ref('fct_orders') }}
where total_amount < 0
```

#### Documentation dans `schema.yml`

Chaque modele doit avoir :
- Une `description` claire en francais
- Chaque colonne doit avoir une `description`

### ✅ Resultats attendus

```bash
# Tous les tests doivent passer
dbt test

# Sortie attendue :
# Completed successfully
# Done. PASS=X WARN=0 ERROR=0 SKIP=0 TOTAL=X
```

### 💡 Indices

- Le format d'un test `relationships` est :
  ```yaml
  - relationships:
      to: ref('dim_customers')
      field: customer_id
  ```
- Un test singular retourne les lignes **en erreur**. Si la requete retourne 0 ligne, le test passe.
- Pensez a `dbt test --select fct_orders` pour tester un modele specifique

---

## Exercice 3 : Modele incremental (⏱ 45 min)

### 📊 Niveau : Avance

### 📝 Contexte

Votre table de commandes grandit de jour en jour. Pour eviter de recalculer les agregations sur l'ensemble des donnees a chaque execution, vous devez creer un modele **incremental**.

### 🎯 Objectifs de l'exercice

1. Creer un modele incremental `mart_daily_orders` qui agregue les commandes **par jour**
2. Gerer les **donnees tardives** (late-arriving data) avec un lookback de 3 jours
3. Configurer une **cle unique** pour eviter les doublons
4. Comparer les performances entre full-refresh et incremental

### 📋 Consignes

#### Modele `models/marts/mart_daily_orders.sql`

Creez un modele incremental avec les specifications suivantes :

| Configuration | Valeur |
|---------------|--------|
| **Materialisation** | `incremental` |
| **Cle unique** | `order_date` |
| **Strategie** | `delete+insert` (ou `merge` selon l'adaptateur) |

Le modele doit calculer pour chaque jour :
- `order_date` : la date du jour
- `nb_orders` : nombre de commandes
- `nb_completed` : nombre de commandes completees
- `nb_cancelled` : nombre de commandes annulees
- `total_revenue` : somme des montants (commandes completees uniquement)
- `avg_order_value` : montant moyen par commande
- `nb_unique_customers` : nombre de clients distincts

#### Gestion du mode incremental

En mode incremental, le modele doit :
- Traiter les donnees des **3 derniers jours** (lookback) pour capturer les donnees tardives
- Utiliser `{{ this }}` pour referencer la table existante

```sql
{% if is_incremental() %}
    where order_date >= (
        select max(order_date) - interval '3 days'
        from {{ this }}
    )
{% endif %}
```

#### Tests de comparaison

1. Executez le modele en mode **full-refresh** :
   ```bash
   dbt run --select mart_daily_orders --full-refresh
   ```

2. Ajoutez de nouvelles donnees dans le seed (quelques commandes supplementaires)

3. Executez en mode **incremental** :
   ```bash
   dbt run --select mart_daily_orders
   ```

4. Verifiez que les resultats sont **identiques** entre incremental et full-refresh

### ✅ Resultats attendus

```bash
# Premiere execution (full refresh automatique)
dbt run --select mart_daily_orders
# → Cree la table complete

# Execution incrementale
dbt run --select mart_daily_orders
# → Ne traite que les 3 derniers jours

# Full refresh pour comparaison
dbt run --select mart_daily_orders --full-refresh
# → Recree la table entiere
```

### 💡 Indices

- La macro `{{ config(materialized='incremental', unique_key='order_date') }}` definit le modele comme incremental
- `is_incremental()` retourne `true` uniquement quand la table existe deja ET que `--full-refresh` n'est pas utilise
- Pour PostgreSQL, la strategie par defaut est `delete+insert` sur la `unique_key`
- Le lookback de 3 jours permet de gerer les commandes dont le statut change apres la date initiale

---

## Exercice 4 : Macros et packages (⏱ 30 min)

### 📊 Niveau : Avance

### 📝 Contexte

Pour rendre votre projet plus maintenable et reutilisable, vous devez creer des **macros** personnalisees et utiliser des **packages** de la communaute dbt.

### 🎯 Objectifs de l'exercice

1. Creer une macro `generate_surrogate_key()`
2. Creer une macro `clean_string()`
3. Installer et utiliser le package `dbt-utils`
4. Creer un **test generique** base sur une macro

### 📋 Consignes

#### Macro 1 : `macros/generate_surrogate_key.sql`

Creez une macro qui genere une **cle de substitution** (surrogate key) a partir d'une ou plusieurs colonnes en utilisant un hash MD5 :

```sql
{% macro generate_surrogate_key(columns) %}
    md5(
        {%- for column in columns %}
            coalesce(cast({{ column }} as varchar), '_null_')
            {%- if not loop.last %} || '-' || {% endif -%}
        {%- endfor %}
    )
{% endmacro %}
```

Utilisez cette macro dans un modele :

```sql
select
    {{ generate_surrogate_key(['order_id', 'product_id']) }} as order_item_key,
    *
from {{ ref('stg_order_items') }}
```

#### Macro 2 : `macros/clean_string.sql`

Creez une macro qui nettoie une chaine de caracteres :
- Supprime les espaces en debut et fin (`trim`)
- Convertit en minuscules (`lower`)
- Remplace les caracteres speciaux courants

```sql
{% macro clean_string(column_name) %}
    lower(
        trim(
            regexp_replace(
                {{ column_name }},
                '[^a-zA-Z0-9\s\-@.]',
                '',
                'g'
            )
        )
    )
{% endmacro %}
```

#### Package dbt-utils

1. Creez ou mettez a jour `packages.yml` :

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.3.0
```

2. Installez les packages :

```bash
dbt deps
```

3. Utilisez les macros suivantes de dbt-utils dans vos modeles ou tests :
   - `{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }}` (comparez avec votre macro)
   - `{{ dbt_utils.pivot(...) }}` ou `{{ dbt_utils.unpivot(...) }}`
   - `dbt_utils.unique_combination_of_columns` (dans les tests)

#### Test generique : `macros/test_positive_value.sql`

Creez un test generique reutilisable qui verifie qu'une colonne ne contient que des **valeurs positives** :

```sql
{% test positive_value(model, column_name) %}

select
    {{ column_name }}
from {{ model }}
where {{ column_name }} < 0

{% endtest %}
```

Utilisez ce test dans `schema.yml` :

```yaml
columns:
  - name: total_amount
    tests:
      - positive_value
```

### ✅ Resultats attendus

```bash
# Le projet compile sans erreur
dbt compile

# Les modeles s'executent
dbt run

# Les tests passent (y compris le test generique)
dbt test
```

### 💡 Indices

- Une macro se definit avec `{% macro nom_macro(params) %} ... {% endmacro %}`
- Un test generique est une macro nommee `test_nom_du_test` dans le dossier `macros/`
- `dbt deps` doit etre execute apres chaque modification de `packages.yml`
- La macro `dbt_utils.generate_surrogate_key` existe deja dans le package — comparez son implementation avec la votre

---

## Exercice 5 : Pipeline dbt Core complet (⏱ 60 min)

### 📊 Niveau : Avance

### 📝 Contexte

Vous devez construire un **pipeline dbt complet depuis zero** en utilisant dbt Core avec PostgreSQL. Cet exercice integre tous les concepts vus dans les chapitres precedents.

### 🎯 Objectifs de l'exercice

1. Initialiser un projet dbt Core
2. Configurer la connexion PostgreSQL (Docker)
3. Charger des donnees de reference (seeds)
4. Creer une architecture **staging → intermediate → mart**
5. Ajouter des tests de qualite
6. Generer la documentation
7. Creer un Makefile pour automatiser les commandes

### 📋 Consignes

#### Etape 1 : Infrastructure (10 min)

1. Creez un dossier pour le projet
2. Creez un `docker-compose.yml` avec PostgreSQL 16
3. Demarrez le conteneur : `docker compose up -d`
4. Creez un environnement virtuel Python et installez dbt-core + dbt-postgres
5. Initialisez le projet avec `dbt init`

#### Etape 2 : Configuration (10 min)

1. Configurez `~/.dbt/profiles.yml` pour se connecter a PostgreSQL local
2. Verifiez avec `dbt debug`
3. Editez `dbt_project.yml` avec la structure staging / intermediate / marts

#### Etape 3 : Donnees (10 min)

1. Creez les fichiers CSV dans `seeds/` :
   - `raw_customers.csv` (au moins 5 clients)
   - `raw_orders.csv` (au moins 8 commandes)
   - `raw_order_items.csv` (au moins 10 lignes)
   - `raw_products.csv` (au moins 5 produits)
2. Chargez les seeds : `dbt seed`

#### Etape 4 : Modeles (15 min)

Creez les modeles suivants :

```
models/
├── staging/
│   ├── sources.yml
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   ├── stg_products.sql
│   └── stg_order_items.sql
├── intermediate/
│   └── int_order_items.sql         # Jointure order_items + products
└── marts/
    ├── schema.yml
    ├── fct_orders.sql              # Table de faits commandes
    ├── dim_customers.sql           # Dimension clients + lifetime value
    └── dim_products.sql            # Dimension produits + metriques ventes
```

#### Etape 5 : Tests (10 min)

1. Ajoutez des tests generiques dans `schema.yml` :
   - `unique` et `not_null` sur les cles primaires
   - `relationships` entre les tables
   - `accepted_values` sur le champ `status`
2. Creez au moins 1 test singular dans `tests/`

#### Etape 6 : Documentation et livraison (5 min)

1. Ajoutez des descriptions sur tous les modeles et colonnes dans `schema.yml`
2. Generez la documentation : `dbt docs generate`
3. Consultez-la : `dbt docs serve`

#### Etape 7 : Makefile

Creez un `Makefile` avec les commandes suivantes :

| Commande | Action |
|----------|--------|
| `make setup` | Installe dbt et les packages, verifie la connexion |
| `make run` | Execute `dbt run` |
| `make test` | Execute `dbt test` |
| `make build` | Execute `dbt build` (seed + run + test) |
| `make docs` | Genere et sert la documentation |
| `make clean` | Nettoie target/, dbt_packages/, logs/ |
| `make fresh` | Full refresh complet |
| `make db-up` | Demarre PostgreSQL avec Docker |
| `make db-down` | Arrete PostgreSQL |

### ✅ Resultats attendus

```bash
# Le pipeline complet s'execute sans erreur
make build

# Sortie attendue :
# dbt build
# Running with dbt=1.9.x
# ...
# Completed successfully
# Done. PASS=XX WARN=0 ERROR=0 SKIP=0 TOTAL=XX
```

```bash
# La documentation est accessible
make docs
# → Ouvre http://localhost:8080 avec le graphe de lignee complet
```

### 💡 Indices

- Commencez par les seeds et le staging avant les marts
- Utilisez `dbt build` pour tout executer dans le bon ordre (seeds → modeles → tests)
- Si un test echoue, utilisez `dbt test --select nom_du_test` pour le relancer individuellement
- La documentation est generee a partir des descriptions dans `schema.yml`
- Dans le Makefile, chaque commande est precedee d'une **tabulation** (pas d'espaces)

### 📋 Grille d'auto-evaluation

| Critere | Points |
|---------|--------|
| PostgreSQL accessible via Docker | /2 |
| dbt Core installe et configure | /2 |
| Seeds charges (4 tables) | /2 |
| Modeles staging (4 modeles, view) | /3 |
| Modele intermediaire (ephemeral) | /2 |
| Modeles marts (3 modeles, table) | /3 |
| Tests generiques (unique, not_null, relationships, accepted_values) | /2 |
| Test singular personnalise | /1 |
| Documentation avec descriptions | /1 |
| Makefile fonctionnel | /2 |
| **Total** | **/20** |

---

**Etape precedente** : [Chapitre 9 - dbt Core](09-dbt-core.md)
**Prochaine etape** : [Brief - Pipeline dbt pour l'Analyse des Ventes](11-brief.md)
