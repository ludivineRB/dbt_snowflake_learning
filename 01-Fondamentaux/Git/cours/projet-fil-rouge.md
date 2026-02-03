## 🎯 Objectifs du projet

- Créer un pipeline ETL complet avec Git dès le début
- Appliquer les stratégies de branches (Git Flow)
- Gérer des features en parallèle
- Résoudre des conflits réalistes
- Collaborer (simulation)
- Configurer pre-commit hooks
- Déployer une "release" en production

## 📋 Contexte du projet

### Scenario

Vous êtes Data Engineer chez **DataMart Inc.** et devez créer un pipeline ETL
pour analyser les données de ventes. Le pipeline doit :

- Extraire des données depuis une API et une base PostgreSQL
- Transformer et nettoyer les données
- Charger dans un Data Warehouse (Snowflake simulé)
- Générer des rapports automatiques

Vous travaillerez avec Git pour gérer le code, les branches et les déploiements.

```bash
Architecture du Pipeline :

┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   API REST  │────────▶│   Extract    │────────▶│   Raw Data  │
│  (Orders)   │         │   Module     │         │   (JSON)    │
└─────────────┘         └──────────────┘         └─────────────┘
                                                         │
┌─────────────┐         ┌──────────────┐                │
│ PostgreSQL  │────────▶│   Extract    │────────────────┤
│ (Customers) │         │   Module     │                │
└─────────────┘         └──────────────┘                ▼
                                                  ┌─────────────┐
                                                  │  Transform  │
                                                  │   Module    │
                                                  └─────────────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │    Load     │
                                                  │   Module    │
                                                  └─────────────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │  Snowflake  │
                                                  │     DWH     │
                                                  └─────────────┘
```

## Phase 1 : Initialisation du projet (10 min)

#### Étape 1.1 : Créer le projet et initialiser Git

```bash
# Créer la structure du projet
mkdir sales-etl-pipeline
cd sales-etl-pipeline

# Initialiser Git
git init
git config user.name "Votre Nom"
git config user.email "votre@email.com"

# Créer la structure de dossiers
mkdir -p src/{extract,transform,load} tests data/{raw,processed} config docs

# Créer la structure
tree -L 2
# sales-etl-pipeline/
# ├── src/
# │   ├── extract/
# │   ├── transform/
# │   └── load/
# ├── tests/
# ├── data/
# │   ├── raw/
# │   └── processed/
# ├── config/
# └── docs/
```

#### Étape 1.2 : Créer le .gitignore et README

```bash
# Créer .gitignore pour Data Engineering
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
venv/
.venv/
*.egg-info/

# Données - NE JAMAIS VERSIONNER
data/raw/*
data/processed/*
*.csv
*.parquet
*.json
!data/raw/.gitkeep
!data/processed/.gitkeep

# Credentials
.env
.env.*
!.env.example
config/secrets.yaml
credentials.json

# IDE
.vscode/
.idea/
.DS_Store

# Logs
logs/
*.log

# Jupyter
.ipynb_checkpoints/

# Tests
.pytest_cache/
.coverage
htmlcov/
EOF

# Créer les fichiers .gitkeep pour versionner les dossiers vides
touch data/raw/.gitkeep
touch data/processed/.gitkeep

# Créer README.md
cat > README.md << 'EOF'
# Sales ETL Pipeline

Pipeline ETL pour analyser les données de ventes de DataMart Inc.

## Architecture

- **Extract** : Extraction depuis API REST et PostgreSQL
- **Transform** : Nettoyage et enrichissement des données
- **Load** : Chargement dans Snowflake Data Warehouse

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Copier `.env.example` vers `.env` et remplir les credentials.

## Utilisation

```bash
python src/main.py --date 2024-01-01
```

## Tests

```bash
pytest tests/
```

## Auteur

DataMart Inc. - Data Engineering Team
EOF

# Créer requirements.txt
cat > requirements.txt << 'EOF'
pandas==2.1.0
psycopg2-binary==2.9.9
requests==2.31.0
python-dotenv==1.0.0
pyyaml==6.0.1
pytest==7.4.3
EOF

# Créer .env.example
cat > .env.example << 'EOF'
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sales_db
DB_USER=your_username
DB_PASSWORD=your_password

# API Configuration
API_URL=https://api.example.com/orders
API_KEY=your_api_key

# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=ANALYTICS
SNOWFLAKE_SCHEMA=SALES
EOF

# Premier commit
git add .
git commit -m "chore: Initial project structure with configuration"
```

#### ✅ Checkpoint Phase 1

Vous devriez avoir :

- ✓ Dépôt Git initialisé
- ✓ Structure de dossiers créée
- ✓ .gitignore configuré
- ✓ README.md documenté
- ✓ Premier commit réalisé

**Vérification :** `git log --oneline` devrait montrer 1 commit

## Phase 2 : Développement des modules (25 min)

#### Stratégie de branches

Nous allons utiliser **Git Flow** :

- `main` : Production (vide pour l'instant)
- `develop` : Intégration
- `feature/*` : Développement des fonctionnalités

#### Étape 2.1 : Créer la branche develop

```bash
# Renommer main si nécessaire
git branch -M main

# Créer develop depuis main
git checkout -b develop

# La branche develop sera notre branche d'intégration
```

#### Étape 2.2 : Feature 1 - Module d'extraction

```bash
# Créer branche feature
git checkout -b feature/extract-module

# Créer le module d'extraction API
cat > src/extract/api_extractor.py << 'EOF'
"""Module d'extraction depuis API REST"""
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class APIExtractor:
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.api_key = os.getenv('API_KEY')

    def extract_orders(self, date: str) -> list:
        """Extrait les commandes pour une date donnée"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {'date': date}

        try:
            response = requests.get(
                f"{self.api_url}/orders",
                headers=headers,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error extracting orders: {e}")
            return []

    def save_raw_data(self, data: list, filename: str):
        """Sauvegarde les données brutes"""
        output_path = f"data/raw/{filename}"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} records to {output_path}")

if __name__ == "__main__":
    extractor = APIExtractor()
    orders = extractor.extract_orders("2024-01-01")
    extractor.save_raw_data(orders, "orders_2024-01-01.json")
EOF

# Créer le module d'extraction DB
cat > src/extract/db_extractor.py << 'EOF'
"""Module d'extraction depuis PostgreSQL"""
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class DBExtractor:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }

    def extract_customers(self) -> pd.DataFrame:
        """Extrait la table customers"""
        query = """
        SELECT
            customer_id,
            customer_name,
            email,
            country,
            created_at
        FROM customers
        WHERE active = true
        """

        try:
            conn = psycopg2.connect(**self.conn_params)
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error extracting customers: {e}")
            return pd.DataFrame()

    def save_to_parquet(self, df: pd.DataFrame, filename: str):
        """Sauvegarde en format Parquet"""
        output_path = f"data/raw/{filename}"
        df.to_parquet(output_path, index=False)
        print(f"Saved {len(df)} customers to {output_path}")

if __name__ == "__main__":
    extractor = DBExtractor()
    customers = extractor.extract_customers()
    extractor.save_to_parquet(customers, "customers.parquet")
EOF

# Créer __init__.py
touch src/extract/__init__.py

# Commiter
git add src/extract/
git commit -m "feat(extract): Add API and DB extraction modules

- Add APIExtractor for orders from REST API
- Add DBExtractor for customers from PostgreSQL
- Support JSON and Parquet output formats"

# Merger dans develop
git checkout develop
git merge --no-ff feature/extract-module -m "Merge feature/extract-module into develop"

# Supprimer la branche feature
git branch -d feature/extract-module
```

#### Étape 2.3 : Feature 2 - Module de transformation (en parallèle)

**Simulation :** Un autre développeur travaille sur la transformation pendant que vous faisiez l'extraction.

```bash
# Créer branche depuis develop
git checkout develop
git checkout -b feature/transform-module

# Créer le module de transformation
cat > src/transform/data_transformer.py << 'EOF'
"""Module de transformation et nettoyage des données"""
import pandas as pd
import json
from datetime import datetime

class DataTransformer:
    def __init__(self):
        pass

    def transform_orders(self, orders_file: str) -> pd.DataFrame:
        """Transforme les données de commandes"""
        with open(orders_file, 'r') as f:
            orders = json.load(f)

        df = pd.DataFrame(orders)

# Nettoyage
        df = df.dropna(subset=['order_id', 'customer_id'])

# Conversion des types
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['amount'] = df['amount'].astype(float)

# Ajout de colonnes calculées
        df['year'] = df['order_date'].dt.year
        df['month'] = df['order_date'].dt.month
        df['quarter'] = df['order_date'].dt.quarter

        return df

    def transform_customers(self, customers_file: str) -> pd.DataFrame:
        """Transforme les données clients"""
        df = pd.read_parquet(customers_file)

# Nettoyage des emails
        df['email'] = df['email'].str.lower().str.strip()

# Suppression des doublons
        df = df.drop_duplicates(subset=['customer_id'])

        return df

    def join_data(self, orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Joint orders et customers"""
        result = orders_df.merge(
            customers_df,
            on='customer_id',
            how='left'
        )
        return result

    def save_transformed_data(self, df: pd.DataFrame, filename: str):
        """Sauvegarde les données transformées"""
        output_path = f"data/processed/{filename}"
        df.to_parquet(output_path, index=False)
        print(f"Saved {len(df)} transformed records to {output_path}")

if __name__ == "__main__":
    transformer = DataTransformer()

# Transform
    orders_df = transformer.transform_orders("data/raw/orders_2024-01-01.json")
    customers_df = transformer.transform_customers("data/raw/customers.parquet")

# Join
    final_df = transformer.join_data(orders_df, customers_df)

# Save
    transformer.save_transformed_data(final_df, "sales_enriched_2024-01-01.parquet")
EOF

touch src/transform/__init__.py

# Commiter
git add src/transform/
git commit -m "feat(transform): Add data transformation module

- Clean and validate orders data
- Enrich with customer information
- Add calculated columns (year, month, quarter)
- Join orders with customers"

# Merger dans develop
git checkout develop
git merge --no-ff feature/transform-module -m "Merge feature/transform-module into develop"
git branch -d feature/transform-module
```

#### Étape 2.4 : Feature 3 - Module de chargement

```bash
# Créer branche
git checkout develop
git checkout -b feature/load-module

# Créer le module de chargement
cat > src/load/snowflake_loader.py << 'EOF'
"""Module de chargement dans Snowflake"""
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class SnowflakeLoader:
    def __init__(self):
# Simulation: En réalité on utiliserait snowflake-connector-python
        self.account = os.getenv('SNOWFLAKE_ACCOUNT')
        self.warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
        self.database = os.getenv('SNOWFLAKE_DATABASE')
        self.schema = os.getenv('SNOWFLAKE_SCHEMA')

    def load_to_snowflake(self, df: pd.DataFrame, table_name: str):
        """Charge les données dans Snowflake"""
# Simulation du chargement
        print(f"Connecting to Snowflake: {self.account}")
        print(f"Target: {self.database}.{self.schema}.{table_name}")
        print(f"Loading {len(df)} records...")

# En production, on ferait:
# conn = snowflake.connector.connect(...)
# cursor = conn.cursor()
# df.to_sql(table_name, con=conn, if_exists='append')

        print(f"✅ Successfully loaded {len(df)} records to {table_name}")

    def validate_load(self, table_name: str) -> dict:
        """Valide le chargement"""
# Simulation
        return {
            'status': 'success',
            'table': table_name,
            'row_count': 1000,
            'load_time': '2.5s'
        }

if __name__ == "__main__":
    loader = SnowflakeLoader()

# Charger les données
    df = pd.read_parquet("data/processed/sales_enriched_2024-01-01.parquet")
    loader.load_to_snowflake(df, "FACT_SALES")

# Valider
    result = loader.validate_load("FACT_SALES")
    print(f"Validation: {result}")
EOF

touch src/load/__init__.py

# Commiter
git add src/load/
git commit -m "feat(load): Add Snowflake loading module

- Connect to Snowflake DWH
- Load transformed data to FACT_SALES table
- Validate successful load"

# Merger dans develop
git checkout develop
git merge --no-ff feature/load-module -m "Merge feature/load-module into develop"
git branch -d feature/load-module
```

#### ✅ Checkpoint Phase 2

Vérifiez votre progression :

```bash
# Visualiser l'historique
git log --oneline --graph --all --decorate

# Devrait montrer:
# * merge feature/load-module
# * commit load module
# * merge feature/transform-module
# * commit transform module
# * merge feature/extract-module
# * commit extract module
# * initial commit
```

## Phase 3 : Orchestration et Tests (15 min)

#### Étape 3.1 : Créer le fichier principal main.py

```bash
# Sur develop
git checkout develop

# Créer main.py
cat > src/main.py << 'EOF'
"""Pipeline ETL principal"""
import argparse
from datetime import datetime
from extract.api_extractor import APIExtractor
from extract.db_extractor import DBExtractor
from transform.data_transformer import DataTransformer
from load.snowflake_loader import SnowflakeLoader

def run_etl_pipeline(date: str):
    """Exécute le pipeline ETL complet"""
    print(f"🚀 Starting ETL Pipeline for {date}")
    print("=" * 50)

# Extract
    print("\n📥 Step 1: Extraction")
    api_extractor = APIExtractor()
    orders = api_extractor.extract_orders(date)
    api_extractor.save_raw_data(orders, f"orders_{date}.json")

    db_extractor = DBExtractor()
    customers = db_extractor.extract_customers()
    db_extractor.save_to_parquet(customers, "customers.parquet")

# Transform
    print("\n🔄 Step 2: Transformation")
    transformer = DataTransformer()
    orders_df = transformer.transform_orders(f"data/raw/orders_{date}.json")
    customers_df = transformer.transform_customers("data/raw/customers.parquet")
    final_df = transformer.join_data(orders_df, customers_df)
    transformer.save_transformed_data(final_df, f"sales_enriched_{date}.parquet")

# Load
    print("\n📤 Step 3: Loading")
    loader = SnowflakeLoader()
    loader.load_to_snowflake(final_df, "FACT_SALES")
    result = loader.validate_load("FACT_SALES")

    print("\n✅ Pipeline completed successfully!")
    print(f"   - Extracted: {len(orders)} orders, {len(customers)} customers")
    print(f"   - Transformed: {len(final_df)} enriched records")
    print(f"   - Loaded: {result['row_count']} records to Snowflake")
    print("=" * 50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Sales ETL Pipeline')
    parser.add_argument('--date', type=str, required=True, help='Date (YYYY-MM-DD)')
    args = parser.parse_args()

    run_etl_pipeline(args.date)
EOF

# Commiter
git add src/main.py
git commit -m "feat: Add main ETL orchestration pipeline

- Orchestrate Extract, Transform, Load steps
- Add command-line interface with argparse
- Add logging and progress tracking"
```

#### Étape 3.2 : Ajouter des tests (nouvelle branche)

```bash
# Créer branche test
git checkout -b feature/add-tests

# Créer tests
cat > tests/test_transformer.py << 'EOF'
"""Tests pour le module de transformation"""
import pytest
import pandas as pd
import sys
sys.path.insert(0, 'src')
from transform.data_transformer import DataTransformer

def test_transform_orders_removes_nulls():
    transformer = DataTransformer()
# TODO: Implémenter le test
    assert True

def test_join_data_correct_columns():
    transformer = DataTransformer()
# TODO: Implémenter le test
    assert True
EOF

cat > tests/__init__.py << 'EOF'
EOF

# Commiter
git add tests/
git commit -m "test: Add unit tests for transformer module"

# Merger dans develop
git checkout develop
git merge feature/add-tests -m "Merge feature/add-tests into develop"
git branch -d feature/add-tests
```

#### Étape 3.3 : Configurer pre-commit hooks

```bash
# Créer .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88']
EOF

# Installer pre-commit (simulation - normalement: pip install pre-commit && pre-commit install)
git add .pre-commit-config.yaml
git commit -m "chore: Configure pre-commit hooks for code quality"
```

## Phase 4 : Hotfix et Release (10 min)

#### 🚨 Scénario : Bug en production !

Un bug critique a été détecté dans le module d'extraction.
Vous devez créer un **hotfix** urgent.

#### Étape 4.1 : Hotfix depuis main

```bash
# D'abord, merger develop dans main pour avoir une base
git checkout main
git merge develop -m "Merge develop into main for initial release"

# Créer branche hotfix
git checkout -b hotfix/fix-api-timeout

# Corriger le bug
cat > src/extract/api_extractor.py << 'EOF'
"""Module d'extraction depuis API REST"""
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class APIExtractor:
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.api_key = os.getenv('API_KEY')
        self.timeout = 30  # FIX: Ajout du timeout

    def extract_orders(self, date: str) -> list:
        """Extrait les commandes pour une date donnée"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {'date': date}

        try:
            response = requests.get(
                f"{self.api_url}/orders",
                headers=headers,
                params=params,
                timeout=self.timeout  # FIX: Ajout du timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:  # FIX: Gestion timeout
            print(f"Error: API timeout after {self.timeout}s")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error extracting orders: {e}")
            return []

    def save_raw_data(self, data: list, filename: str):
        """Sauvegarde les données brutes"""
        output_path = f"data/raw/{filename}"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} records to {output_path}")

if __name__ == "__main__":
    extractor = APIExtractor()
    orders = extractor.extract_orders("2024-01-01")
    extractor.save_raw_data(orders, "orders_2024-01-01.json")
EOF

# Commiter le fix
git add src/extract/api_extractor.py
git commit -m "fix(extract): Add timeout handling for API requests

- Add 30s timeout to prevent hanging
- Add specific timeout exception handling
- Fixes production issue #42"

# Merger dans main
git checkout main
git merge hotfix/fix-api-timeout -m "Merge hotfix/fix-api-timeout into main"

# IMPORTANT: Reporter le fix dans develop aussi
git checkout develop
git merge hotfix/fix-api-timeout -m "Merge hotfix/fix-api-timeout into develop"

# Supprimer la branche hotfix
git branch -d hotfix/fix-api-timeout
```

#### Étape 4.2 : Créer une release avec tag

```bash
# Sur main
git checkout main

# Créer un tag pour la version 1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0

Features:
- Complete ETL pipeline (Extract, Transform, Load)
- API and Database extraction
- Data transformation and enrichment
- Snowflake loading
- Unit tests
- Pre-commit hooks

Fixes:
- API timeout handling (hotfix #42)"

# Voir tous les tags
git tag -l

# Voir les détails du tag
git show v1.0.0
```

#### ✅ Checkpoint Final

Visualisez votre magnifique historique Git :

```bash
# Visualiser tout l'historique
git log --oneline --graph --all --decorate

# Voir les différences entre versions
git diff v1.0.0 develop

# Voir les branches
git branch -a

# Voir les tags
git tag -l
```

## Phase 5 : Pousser vers GitHub (Optionnel - 5 min)

#### Étape 5.1 : Créer un repo GitHub et pousser

```bash
# 1. Créer un repo sur GitHub: sales-etl-pipeline

# 2. Ajouter le remote
git remote add origin https://github.com/VOTRE_USERNAME/sales-etl-pipeline.git

# 3. Pousser toutes les branches
git push -u origin main
git push -u origin develop

# 4. Pousser les tags
git push --tags

# 5. Créer une Pull Request sur GitHub
# - De develop vers main
# - Ajouter description détaillée
# - Merger après review (simulation)
```

### 🎓 Récapitulatif : Ce que vous avez appris

- ✅ Initialiser un projet Data Engineering avec Git
- ✅ Configurer un .gitignore adapté à la Data
- ✅ Utiliser Git Flow (main, develop, feature, hotfix)
- ✅ Créer et merger des branches feature
- ✅ Gérer un hotfix urgent en production
- ✅ Créer des tags pour les releases
- ✅ Configurer des pre-commit hooks
- ✅ Documenter avec README et commits clairs
- ✅ Organiser un pipeline ETL complet
- ✅ Visualiser l'historique avec git log

```bash
Votre workflow final :

main ────────●───────────────●────────▶ (v1.0.0)
              ↑               ↑
              │               │ hotfix
              │               ●
              │              /
develop ──●───┴───●───●───●─────────────▶
          ↑       ↑   ↑   ↑
          │       │   │   │
feature/  │       │   │   │
extract ──┴───────┘   │   │
                      │   │
feature/              │   │
transform ────────────┴───┘
                          │
feature/                  │
load ─────────────────────┘
```

#### 🎉 Projet terminé ! Félicitations !

Vous avez réussi à créer un pipeline ETL complet en utilisant Git de manière professionnelle.
Vous êtes maintenant prêt à appliquer ces compétences sur vos projets réels !

#### 📚 Pour aller plus loin :

- Ajoutez des tests unitaires complets avec pytest
- Intégrez GitHub Actions pour le CI/CD
- Ajoutez un DAG Airflow pour l'orchestration
- Implémentez la connexion réelle à Snowflake
- Ajoutez des métriques et monitoring

[← Retour à l'accueil du cours](index.md)