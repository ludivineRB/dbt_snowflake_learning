## 7. Meilleures pratiques Git pour Data Engineering

### Le fichier .gitignore

Le **.gitignore** indique à Git quels fichiers ne PAS versionner.
C'est crucial en Data Engineering pour éviter de commiter des données sensibles ou volumineuses.

```bash
# Créer un .gitignore optimisé pour Data Engineering
touch .gitignore

# Ajouter des patterns
cat >> .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/
.venv/
*.egg-info/
dist/
build/

# Jupyter Notebooks - CONFIGURATION IMPORTANTE
.ipynb_checkpoints/
# NE PAS exclure tous les *.ipynb !
# Pour nettoyer les outputs avant commit, utilisez :
# jupyter nbconvert --clear-output --inplace notebook.ipynb

# OU installez nbstripout :
# pip install nbstripout
# nbstripout --install

# Data files - NE JAMAIS VERSIONNER LES DONNÉES
*.csv
*.parquet
*.json
*.xlsx
*.xls
*.db
*.sqlite
*.sqlite3
data/
raw_data/
processed_data/
output/
*.pickle
*.pkl
*.h5
*.hdf5

# Credentials et secrets - CRITIQUE !
.env
.env.*
!.env.example
credentials.json
service-account.json
*.pem
*.key
*.p12
*.pfx
config/secrets.yaml
config/prod.yaml
.aws/credentials
.gcloud/

# Logs
*.log
logs/
airflow/logs/
*.log.*

# IDE et éditeurs
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db
*.bak

# DBT
dbt_packages/
target/
dbt_modules/
logs/
.user.yml

# Terraform
*.tfstate
*.tfstate.*
*.tfstate.backup
.terraform/
.terraform.lock.hcl
terraform.tfvars
# Mais versionner :
# !terraform.tfvars.example

# Docker
docker-compose.override.yml

# Spark
metastore_db/
spark-warehouse/
derby.log

# Airflow
airflow.db
airflow.cfg
webserver_config.py
unittests.cfg

# Kafka
.kafka/

# Great Expectations
uncommitted/

# MLflow
mlruns/
mlartifacts/

# Prefect
.prefect/
EOF
```

#### ⚠️ Notebooks Jupyter : Configuration correcte

**NE PAS exclure tous les \*.ipynb !** Les notebooks contiennent du code qu'on veut versionner.
Le problème, ce sont les *outputs* (résultats d'exécution) qui peuvent être volumineux.

**Solution recommandée :**

```bash
# Option 1 : nbstripout (RECOMMANDÉ)
# Installer nbstripout
pip install nbstripout

# Installer le hook Git qui nettoie automatiquement les outputs
nbstripout --install

# Maintenant, à chaque commit, les outputs seront automatiquement retirés !

# Option 2 : Nettoyer manuellement avant commit
jupyter nbconvert --clear-output --inplace mon_notebook.ipynb
git add mon_notebook.ipynb
git commit -m "feat: Add data exploration notebook"

# Option 3 : Configuration Git globale avec nbstripout
# Dans .git/config ou ~/.gitconfig
git config filter.nbstripout.clean 'nbstripout'
git config filter.nbstripout.smudge cat
git config filter.nbstripout.required true

# Puis dans .gitattributes :
echo "*.ipynb filter=nbstripout" >> .gitattributes
git add .gitattributes
git commit -m "chore: Configure nbstripout for Jupyter notebooks"
```

#### 🚨 Ne JAMAIS commiter

- **Données brutes ou transformées** : Utilisez S3, GCS, Azure Blob ou un data lake
- **Credentials et secrets** : API keys, mots de passe, tokens, certificats
- **Fichiers volumineux** : Utilisez Git LFS ou un système de stockage externe
- **Données personnelles (RGPD/GDPR)** : Respectez les réglementations
- **Fichiers binaires générés** : .pyc, .class, executables
- **Dépendances** : node\_modules/, venv/, packages (utilisez requirements.txt)

### Versionner quoi dans un projet Data ?

#### ✅ À versionner

- Code Python/SQL des pipelines
- Configuration DBT
- Scripts ETL/ELT
- Notebooks Jupyter (**sans outputs**)
- Schémas de données (Avro, Protobuf)
- Documentation (README, wiki)
- Tests unitaires et d'intégration
- IaC (Terraform, CloudFormation)
- Docker et docker-compose
- DAGs Airflow/Prefect
- Fichiers de config (YAML, TOML)
- Scripts de migration de DB
- Fichiers d'exemple (.env.example)

#### ❌ À NE PAS versionner

- Datasets (.csv, .parquet, .json)
- Credentials et secrets
- Fichiers de cache
- Modèles ML entraînés (>10MB)
- Logs applicatifs
- Bases de données locales
- Fichiers temporaires
- Dossiers de build
- Outputs de notebooks
- Fichiers IDE personnels
- Environnements virtuels
- Artefacts de compilation

### Stratégie de branches pour Data Engineering

```bash
main (production) ─────●──────●──────●──────▶
                        ↑      ↑      ↑
                        │      │      │
develop ────●────●──────┴──●───┴──●───┴──────▶
            ↑    ↑         ↑      ↑
            │    │         │      │
feature/    │    │         │      │
etl-sales ──┴────┘         │      │
                            │      │
feature/                    │      │
dbt-models ─────────────────┴──────┘
```

- **main** : Code déployé en production (toujours stable, protégé)
- **develop** : Code en cours de développement (branche d'intégration)
- **feature/\*** : Nouvelles fonctionnalités (ex: feature/mongodb-connector)
- **fix/\*** : Corrections de bugs non urgents
- **hotfix/\*** : Corrections urgentes en production
- **release/\*** : Préparation des releases

### Messages de commit pour Data Engineering

#### Convention Conventional Commits

`<type>(<scope>): <description>`

| Type | Usage | Exemple |
| --- | --- | --- |
| feat | Nouvelle fonctionnalité | feat(etl): Add MongoDB data extractor |
| fix | Correction de bug | fix(pipeline): Handle null values in transformation |
| perf | Amélioration de performance | perf(query): Optimize PostgreSQL aggregation query |
| refactor | Refactorisation | refactor(dbt): Restructure models directory |
| docs | Documentation | docs(readme): Add setup instructions for Airflow |
| test | Ajout de tests | test(etl): Add unit tests for data validation |
| chore | Maintenance | chore(deps): Update pandas to 2.0.0 |
| ci | CI/CD | ci: Add GitHub Actions for automated tests |
| build | Build system | build: Update Docker base image to Python 3.11 |

#### ✅ Exemples de bons messages de commit

- `feat(etl): Add incremental load for customer dimension`
- `fix(dbt): Correct date partition logic in sales_daily model`
- `perf(spark): Optimize join strategy reducing runtime by 40%`
- `docs(airflow): Document DAG parameters and retry policy`
- `test(pipeline): Add integration tests for S3 to Snowflake flow`

### Git Hooks pour automatiser les vérifications

Les **hooks** sont des scripts exécutés automatiquement à certains moments
(avant commit, avant push, etc.).

#### Utiliser pre-commit framework (RECOMMANDÉ)

```bash
# Installer pre-commit
pip install pre-commit

# Créer .pre-commit-config.yaml pour Data Engineering
cat > .pre-commit-config.yaml << 'EOF'
repos:
# Hooks standards
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=1000']  # Bloque fichiers > 1MB
      - id: detect-private-key  # Détecte les clés privées
      - id: check-merge-conflict
      - id: mixed-line-ending

# Python formatting
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

# Python linting
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']

# SQL formatting
  - repo: https://github.com/sqlfluff/sqlfluff
    rev: 3.0.0
    hooks:
      - id: sqlfluff-lint
      - id: sqlfluff-fix

# Jupyter notebooks
  - repo: https://github.com/nbQA-dev/nbQA
    rev: 1.7.1
    hooks:
      - id: nbqa-black
      - id: nbqa-flake8

# Nettoyer outputs notebooks (IMPORTANT!)
  - repo: https://github.com/kynan/nbstripout
    rev: 0.6.1
    hooks:
      - id: nbstripout
        files: "\\.ipynb$"

# Sécurité - Détecter secrets
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

# YAML linting
  - repo: https://github.com/adrienverge/yamllint
    rev: v1.33.0
    hooks:
      - id: yamllint

# Terraform
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
EOF

# Installer les hooks
pre-commit install

# Lancer sur tous les fichiers
pre-commit run --all-files

# Les hooks s'exécuteront automatiquement à chaque commit!
```

### Git LFS pour les fichiers volumineux

**Git Large File Storage (LFS)** permet de versionner des fichiers volumineux
sans alourdir le dépôt. Utile pour les petits datasets d'exemple ou modèles ML.

```bash
# Installer Git LFS
# macOS
brew install git-lfs
# Ubuntu
sudo apt-get install git-lfs
# Windows : télécharger depuis https://git-lfs.github.com

# Initialiser Git LFS dans le repo
git lfs install

# Tracker les fichiers parquet (datasets exemples)
git lfs track "*.parquet"
git lfs track "data/samples/*.csv"

# Tracker les modèles ML
git lfs track "models/*.pkl"
git lfs track "models/*.h5"
git lfs track "*.joblib"

# Le fichier .gitattributes est créé automatiquement
cat .gitattributes
# *.parquet filter=lfs diff=lfs merge=lfs -text
# models/*.pkl filter=lfs diff=lfs merge=lfs -text

# Commiter normalement
git add .gitattributes
git add data/samples/example.parquet
git commit -m "feat: Add sample data with Git LFS"
git push

# Voir les fichiers LFS
git lfs ls-files

# Cloner un repo avec LFS
git clone
# Les fichiers LFS sont téléchargés automatiquement
```

#### Quand utiliser Git LFS ?

- ✅ Datasets d'exemple de petite taille (< 100MB)
- ✅ Modèles ML de référence
- ✅ Fichiers de documentation (PDF, images)
- ❌ Gros datasets de production (utilisez S3/GCS)
- ❌ Données sensibles (ne jamais versionner)

### Gérer les secrets avec Git

```bash
# Créer un fichier .env.example (à versionner)
cat > .env.example << 'EOF'
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydatabase
DB_USER=your_username
DB_PASSWORD=your_password

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# API Keys
OPENAI_API_KEY=your_api_key
EOF

# Copier et remplir avec les vraies valeurs (NE PAS VERSIONNER)
cp .env.example .env

# Vérifier que .env est dans .gitignore
grep ".env" .gitignore

# Utiliser des outils de gestion de secrets
# Option 1 : AWS Secrets Manager
# Option 2 : HashiCorp Vault
# Option 3 : Azure Key Vault
# Option 4 : Variables d'environnement CI/CD
```

### 💡 Points clés à retenir

- Configurez un .gitignore complet DÈS LE DÉBUT du projet
- Utilisez nbstripout pour nettoyer automatiquement les notebooks
- NE JAMAIS commiter de credentials ou données sensibles
- Adoptez Conventional Commits pour des messages clairs
- Mettez en place pre-commit hooks pour automatiser les vérifications
- Utilisez Git LFS uniquement pour petits fichiers d'exemple
- Stockez les vrais datasets dans S3/GCS/Azure Blob
- Versionnez le code, pas les données
- Documentez votre workflow dans le README
- Protégez la branche main avec branch protection rules

#### ✅ Partie 7 terminée !

Félicitations ! Vous maîtrisez maintenant les meilleures pratiques Git pour le Data Engineering.
Passez à la Partie 8 pour découvrir les workflows professionnels avec Conventional Commits et Docker !

[Partie 8 : Workflows →](partie8.md)
[🎯 Faire les exercices](../exercices.md)