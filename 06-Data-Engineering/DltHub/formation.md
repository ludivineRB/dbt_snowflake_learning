## Objectifs de la formation

- Comprendre DltHub et ses avantages
- Créer des pipelines de données simples
- Utiliser les sources et destinations
- Implémenter des transformations
- Gérer le schema evolution
- Déployer en production

## 1. Introduction à DltHub

### Qu'est-ce que DltHub ?

**DltHub (Data Load Tool Hub)** est un framework Python open-source qui simplifie la création
de pipelines de données (ELT). Il permet d'extraire des données de diverses sources et de les charger dans
des destinations (data warehouses, data lakes) avec un minimum de code.

#### Philosophie de DltHub

DltHub suit une approche **ELT** (Extract, Load, Transform) plutôt que ETL.
Les transformations lourdes sont effectuées dans la destination (warehouse) plutôt que pendant le transit.

### Pourquoi DltHub ?

#### 🚀 Simplicité

Créez des pipelines en quelques lignes de Python, sans infrastructure complexe

#### 🔄 Schema Evolution

Gestion automatique des changements de schéma, pas de migrations manuelles

#### 🎯 Python-First

100% Python, intégration naturelle avec pandas, requests, etc.

#### 🔌 Connecteurs

Nombreux connecteurs vers BigQuery, Snowflake, PostgreSQL, DuckDB...

#### 📊 Data Quality

Validation automatique, détection d'anomalies, data contracts

#### ⚡ Incrémental

Support natif du loading incrémental pour économiser ressources et temps

### DltHub vs Alternatives

| Aspect | DltHub | Airbyte | Fivetran |
| --- | --- | --- | --- |
| **Type** | Librairie Python | Platform (UI + API) | SaaS |
| **Code** | Python natif | Configuration YAML | No-code |
| **Hosting** | Votre infra | Self-hosted ou Cloud | Cloud seulement |
| **Complexité** | Simple (Python) | Moyenne (Docker) | Simple (UI) |
| **Coût** | Gratuit (open source) | Gratuit + Paid | Payant |
| **Flexibilité** | Très haute (code) | Moyenne | Limitée |

### Concepts clés

| Concept | Description |
| --- | --- |
| **Source** | Origine des données (API, base de données, fichiers) |
| **Resource** | Unité de données à charger (table, endpoint API) |
| **Destination** | Où les données sont chargées (BigQuery, PostgreSQL...) |
| **Pipeline** | Configuration du flux source → destination |
| **Schema** | Structure des données, évolutif automatiquement |
| **State** | Sauvegarde de l'état pour loading incrémental |

```bash
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   SOURCE    │       │   DLTHUB     │       │ DESTINATION │
│             │       │   PIPELINE   │       │             │
│  API/DB/    │  ───→ │              │  ───→ │  BigQuery   │
│  Files      │       │  Extract     │       │  Snowflake  │
│             │       │  Validate    │       │  PostgreSQL │
│             │       │  Transform   │       │             │
└─────────────┘       └──────────────┘       └─────────────┘
                             │
                             ↓
                      ┌──────────────┐
                      │    STATE     │
                      │ (incremental)│
                      └──────────────┘
```

## 2. Installation et premier pipeline

### Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Installer dlt
pip install dlt

# Installer des destinations spécifiques
pip install "dlt[duckdb]"      # Pour DuckDB
pip install "dlt[postgres]"    # Pour PostgreSQL
pip install "dlt[bigquery]"    # Pour BigQuery
pip install "dlt[snowflake]"   # Pour Snowflake

# Vérifier l'installation
dlt --version
```

### Premier pipeline : API → DuckDB

Créons un pipeline simple qui charge des données depuis une API vers DuckDB :

```bash
"""
Premier pipeline DLT : API → DuckDB
"""
import dlt
import requests


# 1. Définir une source (function qui génère des données)
@dlt.resource(name="users", write_disposition="replace")
def get_users():
    """Récupérer des utilisateurs depuis JSONPlaceholder API"""
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    yield response.json()


# 2. Créer le pipeline
def run_pipeline():
# Configurer le pipeline
    pipeline = dlt.pipeline(
        pipeline_name="api_to_duckdb",
        destination="duckdb",
        dataset_name="demo_data"
    )

# Charger les données
    load_info = pipeline.run(get_users())

# Afficher les résultats
    print(f"✅ Pipeline exécuté avec succès!")
    print(f"📊 Lignes chargées: {load_info}")


if __name__ == "__main__":
    run_pipeline()
```

#### Exécuter le pipeline

```bash
python first_pipeline.py

# Résultat
✅ Pipeline exécuté avec succès!
📊 Lignes chargées: LoadInfo(...)

# Vérifier les données dans DuckDB
duckdb demo_data.duckdb

# Dans DuckDB:
SELECT * FROM users LIMIT 5;
.exit
```

#### Félicitations !

Vous venez de créer votre premier pipeline DLT en quelques lignes de code.
Les données de l'API sont maintenant stockées dans DuckDB et prêtes à être analysées.

### Structure d'un projet DLT

```bash
my_dlt_project/
├── .dlt/
│   ├── config.toml          # Configuration (credentials)
│   └── secrets.toml         # Secrets (API keys, passwords)
├── pipelines/
│   ├── api_pipeline.py
│   └── database_pipeline.py
├── requirements.txt
└── README.md
```

#### Configuration (.dlt/config.toml)

```bash
# Configuration du pipeline
[runtime]
log_level = "INFO"

# Configuration de la destination
[destination.duckdb]
credentials = "demo_data.duckdb"

[destination.postgres]
credentials = "postgresql://user:password@localhost:5432/db"
```

#### Secrets (.dlt/secrets.toml)

```bash
# Ne JAMAIS commiter ce fichier !
[sources.api]
api_key = "your-secret-api-key"

[destination.bigquery.credentials]
project_id = "my-project"
private_key = "-----BEGIN PRIVATE KEY-----\n..."
```

#### Sécurité

Ajoutez `.dlt/secrets.toml` dans votre `.gitignore` pour ne pas
commiter vos credentials par erreur !

## 3. Sources et Resources

### Qu'est-ce qu'une Resource ?

Une **resource** est une unité de données que DLT peut charger.
Elle peut être une fonction, un générateur ou un itérateur qui produit des données.

#### Resource simple

```bash
import dlt

@dlt.resource
def my_data():
    """Resource simple qui retourne une liste"""
    return [
        {"id": 1, "name": "Alice", "age": 28},
        {"id": 2, "name": "Bob", "age": 32},
        {"id": 3, "name": "Charlie", "age": 25}
    ]

# Utilisation
pipeline = dlt.pipeline(
    pipeline_name="simple",
    destination="duckdb",
    dataset_name="demo"
)

pipeline.run(my_data())
```

#### Resource avec générateur (lazy loading)

```bash
@dlt.resource
def paginated_api():
    """Resource avec pagination (lazy loading)"""
    page = 1
    while True:
        response = requests.get(f"https://api.example.com/data?page={page}")
        data = response.json()

        if not data:
            break

        yield data  # Yield permet de traiter les données par batch
        page += 1
```

### Write Disposition

Le **write\_disposition** définit comment les données sont écrites dans la destination :

| Mode | Description | Cas d'usage |
| --- | --- | --- |
| `replace` | Remplace toutes les données | Snapshots complets, petites tables |
| `append` | Ajoute les nouvelles données | Logs, événements, time-series |
| `merge` | Upsert (update ou insert) | Dimension tables, CDC |

```bash
# Replace : écrase les données
@dlt.resource(write_disposition="replace")
def full_snapshot():
    return get_all_users()

# Append : ajoute aux données existantes
@dlt.resource(write_disposition="append")
def events_log():
    return get_new_events()

# Merge : upsert basé sur primary_key
@dlt.resource(
    write_disposition="merge",
    primary_key="user_id"
)
def user_updates():
    return get_updated_users()
```

### Sources : Regrouper plusieurs Resources

Une **source** regroupe plusieurs resources liées :

```bash
import dlt

@dlt.source
def my_api_source(api_key: str):
    """Source qui regroupe plusieurs endpoints"""

    @dlt.resource(write_disposition="replace")
    def users():
        """Récupérer les utilisateurs"""
        response = requests.get(
            "https://api.example.com/users",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        yield response.json()

    @dlt.resource(write_disposition="append")
    def orders():
        """Récupérer les commandes"""
        response = requests.get(
            "https://api.example.com/orders",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        yield response.json()

    @dlt.resource(write_disposition="merge", primary_key="product_id")
    def products():
        """Récupérer les produits"""
        response = requests.get(
            "https://api.example.com/products",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        yield response.json()

# Retourner toutes les resources
    return users(), orders(), products()


# Utilisation
pipeline = dlt.pipeline(
    pipeline_name="ecommerce",
    destination="duckdb",
    dataset_name="ecommerce_data"
)

# Charger toutes les resources de la source
load_info = pipeline.run(my_api_source(api_key="secret-key"))

# Ou charger une seule resource
source = my_api_source(api_key="secret-key")
load_info = pipeline.run(source.users)
```

### Loading incrémental

Le **loading incrémental** permet de ne charger que les nouvelles données :

```bash
from datetime import datetime, timedelta
import dlt

@dlt.resource(
    write_disposition="append",
    primary_key="order_id"
)
def orders_incremental(
    last_timestamp=dlt.sources.incremental("created_at")
):
    """
    Charger seulement les commandes récentes
    DLT sauvegarde automatiquement le dernier timestamp
    """

# Si c'est la première exécution, prendre les 7 derniers jours
    if last_timestamp.start_value is None:
        last_timestamp.start_value = datetime.now() - timedelta(days=7)

# Requêter l'API avec le timestamp
    response = requests.get(
        "https://api.example.com/orders",
        params={"since": last_timestamp.start_value.isoformat()}
    )

    orders = response.json()

# DLT met à jour automatiquement le timestamp
# basé sur la colonne "created_at"
    yield orders


# Première exécution : charge les 7 derniers jours
pipeline.run(orders_incremental())

# Deuxième exécution : charge seulement les nouvelles données
pipeline.run(orders_incremental())
```

#### State Management

DLT sauvegarde automatiquement l'état (timestamps, cursors) dans la destination.
Vous n'avez pas besoin de gérer manuellement le tracking des données déjà chargées.

### Transformer les données

```bash
@dlt.resource
def users_transformed():
    """Resource avec transformation des données"""
    raw_data = requests.get("https://api.example.com/users").json()

# Transformer chaque enregistrement
    for user in raw_data:
        yield {
            "user_id": user["id"],
            "full_name": f"{user['first_name']} {user['last_name']}",
            "email": user["email"].lower(),
            "age": user["age"],
            "is_active": user.get("status") == "active",
            "created_at": datetime.fromisoformat(user["created_at"]),
# Ajouter des champs calculés
            "age_group": "young" if user["age"] < 30 else "senior",
            "loaded_at": datetime.now()
        }
```

### Best Practices pour les Resources

- Utilisez des générateurs (yield) pour les grandes quantités de données
- Ajoutez un primary\_key pour les merge operations
- Utilisez le loading incrémental pour économiser API calls
- Ajoutez des champs de métadonnées (loaded\_at, source, etc.)
- Gérez les erreurs avec try-except
- Loggez les opérations importantes

## 4. Destinations et configuration

### Destinations supportées

#### 🦆 DuckDB

Base de données analytique locale, parfait pour le dev et tests

#### 🐘 PostgreSQL

Base de données relationnelle classique

#### ☁️ BigQuery

Data warehouse Google Cloud, serverless et scalable

#### ❄️ Snowflake

Data warehouse cloud leader du marché

#### 🔷 Azure Synapse

Data warehouse Microsoft Azure

#### 🪣 Parquet/CSV

Export vers fichiers pour data lakes

### Configuration DuckDB

```bash
import dlt

# Méthode 1 : Configuration inline
pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination="duckdb",
    dataset_name="my_dataset"
)

# Méthode 2 : Configuration via credentials
pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination=dlt.destinations.duckdb("my_data.duckdb"),
    dataset_name="my_dataset"
)
```

### Configuration PostgreSQL

```bash
import dlt

# Configuration PostgreSQL
pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination=dlt.destinations.postgres(
        "postgresql://user:password@localhost:5432/mydb"
    ),
    dataset_name="analytics"
)

# Ou via .dlt/secrets.toml:
# [destination.postgres.credentials]
# database = "mydb"
# username = "user"
# password = "password"
# host = "localhost"
# port = 5432

pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination="postgres",
    dataset_name="analytics"
)
```

### Configuration BigQuery

```bash
import dlt

# Configuration BigQuery
pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination="bigquery",
    dataset_name="analytics"
)

# Fichier .dlt/secrets.toml :
# [destination.bigquery.credentials]
# project_id = "my-gcp-project"
# private_key = "-----BEGIN PRIVATE KEY-----\n..."
# client_email = "service-account@project.iam.gserviceaccount.com"

# Ou utiliser GOOGLE_APPLICATION_CREDENTIALS
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
```

### Configuration Snowflake

```bash
import dlt

# Fichier .dlt/secrets.toml :
# [destination.snowflake.credentials]
# database = "MY_DATABASE"
# username = "MY_USER"
# password = "MY_PASSWORD"
# host = "account.snowflakecomputing.com"
# warehouse = "MY_WAREHOUSE"
# role = "MY_ROLE"

pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination="snowflake",
    dataset_name="analytics"
)
```

### Export vers fichiers (Data Lake)

```bash
import dlt

# Export vers Parquet
pipeline = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination=dlt.destinations.filesystem("/data/lake"),
    dataset_name="raw_data"
)

# Configuration dans .dlt/config.toml :
# [destination.filesystem]
# bucket_url = "s3://my-bucket/data"  # S3
# # ou
# bucket_url = "gs://my-bucket/data"  # GCS
# # ou
# bucket_url = "az://my-container/data"  # Azure Blob

# Layout des fichiers :
# /data/lake/
#   ├── users/
#   │   ├── 2024-01-15_001.parquet
#   │   └── 2024-01-16_001.parquet
#   └── orders/
#       └── 2024-01-15_001.parquet
```

#### Environnements multiples

Utilisez différents fichiers de configuration pour dev, staging et production :

- `.dlt/config.dev.toml`
- `.dlt/config.staging.toml`
- `.dlt/config.prod.toml`

## 5. Schémas et validation des données

### Schema Evolution automatique

DLT gère automatiquement l'évolution du schéma. Si de nouvelles colonnes apparaissent,
elles sont ajoutées automatiquement sans casser le pipeline.

```bash
# Première exécution : 3 colonnes
data_v1 = [
    {"id": 1, "name": "Alice", "age": 28}
]
pipeline.run(data_v1, table_name="users")

# Deuxième exécution : nouvelle colonne "email"
# DLT ajoute automatiquement la colonne
data_v2 = [
    {"id": 2, "name": "Bob", "age": 32, "email": "bob@example.com"}
]
pipeline.run(data_v2, table_name="users")

# Résultat dans la table :
# id | name  | age | email
# 1  | Alice | 28  | NULL
# 2  | Bob   | 32  | bob@example.com
```

### Définir un schéma explicite

```bash
from dlt.common.schema import TColumnSchema

@dlt.resource(
    columns={
        "user_id": {
            "data_type": "bigint",
            "nullable": False,
            "primary_key": True
        },
        "email": {
            "data_type": "text",
            "nullable": False,
            "unique": True
        },
        "age": {
            "data_type": "bigint",
            "nullable": True
        },
        "created_at": {
            "data_type": "timestamp",
            "nullable": False
        }
    }
)
def users_with_schema():
    """Resource avec schéma explicite"""
    return get_users_data()
```

### Validation des données

```bash
import dlt
from dlt.common.typing import TDataItem

@dlt.resource
def validated_users():
    """Resource avec validation custom"""
    raw_data = get_raw_users()

    for user in raw_data:
# Validation manuelle
        if not user.get("email") or "@" not in user["email"]:
            print(f"⚠️ Email invalide pour user {user.get('id')}")
            continue  # Skip cet enregistrement

        if user.get("age") and user["age"] < 0:
            print(f"⚠️ Age négatif pour user {user.get('id')}")
            user["age"] = None  # Corriger la donnée

        yield user


# Ou utiliser Pydantic pour la validation
from pydantic import BaseModel, EmailStr, validator

class UserModel(BaseModel):
    """Modèle Pydantic pour validation"""
    user_id: int
    email: EmailStr
    age: int

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v


@dlt.resource
def users_pydantic():
    """Validation avec Pydantic"""
    raw_data = get_raw_users()

    for user in raw_data:
        try:
# Valider avec Pydantic
            validated = UserModel(**user)
            yield validated.dict()
        except Exception as e:
            print(f"❌ Validation error: {e}")
# Logger ou rejeter
```

### Data Contracts

Les **data contracts** permettent de définir des règles strictes sur les données :

```bash
@dlt.resource(
    columns={
        "user_id": {"data_type": "bigint", "nullable": False},
        "email": {"data_type": "text", "nullable": False}
    },
    schema_contract={
        "tables": "evolve",      # Nouvelles tables autorisées
        "columns": "freeze",     # Nouvelles colonnes interdites
        "data_type": "freeze"    # Changement de type interdit
    }
)
def strict_users():
    """
    Schema contract strict :
    - Nouvelles colonnes = erreur
    - Changement de type = erreur
    """
    return get_users()
```

#### Attention

Les data contracts stricts peuvent casser vos pipelines si l'API source change.
Utilisez-les seulement quand vous contrôlez la source ou avez des SLAs stricts.

## 6. Patterns avancés et production

### Pipeline complet production-ready

```bash
"""
Pipeline production-ready avec gestion d'erreurs et monitoring
"""
import dlt
import requests
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dlt.source
def ecommerce_source(api_key: str, base_url: str):
    """Source e-commerce complète"""

    @dlt.resource(
        write_disposition="merge",
        primary_key="user_id",
        merge_key="user_id"
    )
    def users():
        """Utilisateurs avec upsert"""
        try:
            logger.info("📥 Fetching users...")
            response = requests.get(
                f"{base_url}/users",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            logger.info(f"✅ Fetched {len(data)} users")

# Enrichir avec métadonnées
            for user in data:
                user["_loaded_at"] = datetime.now()
                user["_source"] = "api"
                yield user

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching users: {e}")
            raise

    @dlt.resource(
        write_disposition="append",
        primary_key="order_id"
    )
    def orders(last_date=dlt.sources.incremental("created_at")):
        """Commandes avec loading incrémental"""
        try:
            logger.info(f"📥 Fetching orders since {last_date.start_value}...")

            params = {}
            if last_date.start_value:
                params["since"] = last_date.start_value.isoformat()

            response = requests.get(
                f"{base_url}/orders",
                headers={"Authorization": f"Bearer {api_key}"},
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            logger.info(f"✅ Fetched {len(data)} orders")

            for order in data:
                order["_loaded_at"] = datetime.now()
                yield order

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching orders: {e}")
            raise

    return users(), orders()


def run_pipeline():
    """Exécuter le pipeline avec monitoring"""
    logger.info("🚀 Starting pipeline...")

# Créer le pipeline
    pipeline = dlt.pipeline(
        pipeline_name="ecommerce_prod",
        destination="bigquery",
        dataset_name="analytics"
    )

    try:
# Récupérer credentials depuis les secrets
        api_key = dlt.secrets.value["sources.ecommerce.api_key"]
        base_url = dlt.config.value["sources.ecommerce.base_url"]

# Exécuter le pipeline
        source = ecommerce_source(api_key=api_key, base_url=base_url)
        load_info = pipeline.run(source)

# Logger les résultats
        logger.info("✅ Pipeline completed successfully!")
        logger.info(f"📊 Load info: {load_info}")

# Vérifier les erreurs
        if load_info.has_failed_jobs:
            logger.error("❌ Some jobs failed!")
            for job in load_info.load_packages[0].jobs["failed_jobs"]:
                logger.error(f"Failed job: {job}")
            raise Exception("Pipeline had failed jobs")

        return load_info

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
# Envoyer une alerte (Slack, email, etc.)
        send_alert(f"Pipeline failed: {e}")
        raise


def send_alert(message: str):
    """Envoyer une alerte en cas d'erreur"""
# Slack webhook
    webhook_url = dlt.secrets.value.get("alerts.slack_webhook")
    if webhook_url:
        requests.post(webhook_url, json={"text": message})


if __name__ == "__main__":
    run_pipeline()
```

### Déploiement avec Airflow

```bash
"""
DAG Airflow pour exécuter un pipeline DLT
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import dlt


def run_dlt_pipeline():
    """Fonction appelée par Airflow"""
    pipeline = dlt.pipeline(
        pipeline_name="ecommerce",
        destination="bigquery",
        dataset_name="analytics"
    )

# Importer votre source
    from pipelines.ecommerce import ecommerce_source

    api_key = dlt.secrets.value["sources.ecommerce.api_key"]
    source = ecommerce_source(api_key=api_key)

    load_info = pipeline.run(source)

    if load_info.has_failed_jobs:
        raise Exception("Pipeline had failed jobs")


# Définir le DAG
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'dlt_ecommerce_pipeline',
    default_args=default_args,
    description='Load ecommerce data with DLT',
    schedule_interval='@hourly',  # Toutes les heures
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['dlt', 'ecommerce']
) as dag:

    run_pipeline_task = PythonOperator(
        task_id='run_dlt_pipeline',
        python_callable=run_dlt_pipeline
    )
```

### Tests unitaires

```bash
"""
Tests pour les pipelines DLT
"""
import pytest
import dlt


def test_users_resource():
    """Tester la resource users"""
    from pipelines.ecommerce import ecommerce_source

# Mock API
    api_key = "test-key"
    base_url = "https://api.test.com"

    source = ecommerce_source(api_key=api_key, base_url=base_url)

# Tester avec DuckDB (destination de test)
    pipeline = dlt.pipeline(
        pipeline_name="test_pipeline",
        destination="duckdb",
        dataset_name="test_data",
        full_refresh=True  # Nettoyer entre chaque test
    )

    load_info = pipeline.run(source.users)

    assert not load_info.has_failed_jobs, "Pipeline should not have failed jobs"

# Vérifier les données chargées
    with pipeline.sql_client() as client:
        result = client.execute_sql("SELECT COUNT(*) as count FROM users")
        count = result[0][0]
        assert count > 0, "Should have loaded users"


def test_schema_validation():
    """Tester la validation du schéma"""
    from pipelines.ecommerce import users_resource

# Données de test
    test_data = [
        {"user_id": 1, "email": "test@example.com", "age": 25},
        {"user_id": 2, "email": "invalid-email", "age": -5}  # Invalide
    ]

# Vérifier que les données invalides sont rejetées
# ... votre logique de test
```

### Checklist Production

- Gestion d'erreurs complète (try-except)
- Logging détaillé de toutes les opérations
- Alertes en cas d'échec (Slack, email)
- Loading incrémental pour économiser ressources
- Monitoring des métriques (lignes chargées, durée)
- Tests unitaires et d'intégration
- Documentation du pipeline
- Secrets sécurisés (jamais en dur dans le code)
- Retries automatiques sur erreurs transitoires
- CI/CD pour déploiement automatique

## 📚 Ressources et liens utiles

[**Documentation officielle DLT**

Documentation complète, guides et références](https://dlthub.com/docs)
[**DLT sur GitHub**

Code source, issues et contributions](https://github.com/dlt-hub/dlt)
[**Exemples de pipelines**

Exemples prêts à l'emploi pour différentes sources](https://dlthub.com/docs/examples)
[**API Reference**

Documentation détaillée de l'API DLT](https://dlthub.com/docs/reference)
[**Blog DLT**

Articles, tutorials et best practices](https://dlthub.com/docs/blog)
[**Discord Community**

Aide, discussions et support communautaire](https://discord.gg/dlthub)

#### Prochaines étapes

Maintenant que vous maîtrisez DLT, explorez :

- **Sources vérifiées** : Utilisez les sources pré-construites (GitHub, Stripe, etc.)
- **dbt integration** : Transformez vos données avec dbt après le load
- **Orchestration** : Déployez avec Airflow, Dagster ou Prefect
- **Monitoring** : Intégrez avec DataDog, Prometheus pour le monitoring
- **Data Quality** : Ajoutez Great Expectations pour la validation
- **Reverse ETL** : Chargez des données depuis votre warehouse vers des apps