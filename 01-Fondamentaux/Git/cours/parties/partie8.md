## 8. Workflows et Automation

### Conventional Commits : Standardiser vos messages

**Conventional Commits** est une convention pour structurer les messages de commit
de manière cohérente. Cela facilite la génération automatique de changelogs, le versionnage
sémantique et la compréhension de l'historique.

#### Format du message

```bash
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types de commits

| Type | Description | Exemple |
| --- | --- | --- |
| `feat` | Nouvelle fonctionnalité | `feat(api): add MongoDB connector` |
| `fix` | Correction de bug | `fix(etl): handle null values in transform` |
| `docs` | Documentation uniquement | `docs(readme): update setup instructions` |
| `style` | Formatage (pas de changement de code) | `style: format with black` |
| `refactor` | Refactorisation | `refactor(db): optimize connection pooling` |
| `perf` | Amélioration de performance | `perf(query): add index on user_id` |
| `test` | Ajout ou modification de tests | `test(etl): add validation tests` |
| `build` | Build système ou dépendances | `build(deps): upgrade pandas to 2.0` |
| `ci` | Configuration CI/CD | `ci: add GitHub Actions workflow` |
| `chore` | Tâches de maintenance | `chore: update .gitignore` |

#### Scope (optionnel mais recommandé)

Le scope précise la partie du projet affectée :

- `feat(api)` : Nouvelle feature dans l'API
- `fix(etl)` : Bug fix dans le pipeline ETL
- `docs(readme)` : Modification du README
- `test(transform)` : Tests pour le module transform

#### Breaking Changes

Pour signaler un changement incompatible (breaking change), ajoutez `!` ou
`BREAKING CHANGE:` dans le footer :

```bash
# Méthode 1 : avec !
feat(api)!: change response format to JSON

# Méthode 2 : avec BREAKING CHANGE dans le footer
feat(api): change response format

BREAKING CHANGE: API now returns JSON instead of XML
```

#### Exemples concrets pour Data Engineering

```bash
# Nouvelle fonctionnalité ETL
feat(extract): add S3 data source connector

Implement S3Extractor class to pull data from AWS S3 buckets.
Supports both CSV and Parquet formats.

Closes #42

# Correction de bug
fix(transform): handle missing values in date columns

Previously, missing dates caused the pipeline to crash.
Now replaced with NULL values and logged for monitoring.

Fixes #67

# Amélioration de performance
perf(load): batch insert in chunks of 1000 rows

Improves loading speed by 3x for large datasets.

# Refactorisation
refactor(db): extract connection logic to separate module

Makes database connections reusable across extractors.

# Tests
test(validation): add data quality checks

Add tests for:
- Null value detection
- Schema validation
- Duplicate detection

# CI/CD
ci: add Docker build and push to registry

Configure GitHub Actions to:
- Build Docker image on merge to main
- Push to Docker Hub with version tag
- Run integration tests before deploy

# Documentation
docs(etl): add architecture diagram and data flow

Add Mermaid diagrams showing:
- ETL pipeline stages
- Data sources and destinations
- Error handling flow
```

#### Outils pour automatiser Conventional Commits

- **commitizen** : CLI interactive pour créer des commits conformes
- **commitlint** : Valide que vos commits respectent la convention
- **standard-version** : Génère automatiquement le CHANGELOG et les tags de version
- **semantic-release** : Automatise le versionnage et la release

#### Configuration de Commitizen

```bash
# Installation
pip install commitizen

# Initialiser dans votre projet
cz init

# Créer un commit avec l'assistant interactif
cz commit

# Exemple d'interaction :
# ? Select the type of change you are committing: feat
# ? What is the scope of this change?: etl
# ? Write a short description: add PostgreSQL extractor
# ? Provide a longer description: (press enter to skip)
# ? Are there any breaking changes?: No
# ? Does this change affect any open issues?: Yes
# ? Add issue references: closes #42

# Résultat :
# feat(etl): add PostgreSQL extractor
#
# closes #42
```

#### Configuration de Commitlint

```bash
# Installation (Node.js requis)
npm install --save-dev @commitlint/{cli,config-conventional}

# Créer le fichier de configuration
echo "module.exports = {extends: ['@commitlint/config-conventional']};" > commitlint.config.js

# Ajouter un hook Git pour valider les commits
npm install --save-dev husky
npx husky install
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'

# Maintenant, les commits non conformes seront rejetés :
git commit -m "bad message"
# ❌ ERREUR : subject may not be empty [subject-empty]
```

### Git + Docker : Workflow de Conteneurisation

L'intégration de Git avec Docker permet de versionner non seulement le code,
mais aussi l'environnement d'exécution complet. Voici les meilleures pratiques.

#### Structure de projet recommandée

```bash
projet-data-pipeline/
├── .git/
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── src/
│   ├── extract/
│   ├── transform/
│   └── load/
├── tests/
├── config/
│   ├── dev.yaml
│   └── prod.yaml
└── scripts/
    ├── build.sh
    └── deploy.sh
```

#### Dockerfile pour un projet ETL Python

```bash
# Dockerfile
FROM python:3.11-slim

# Metadata
LABEL maintainer="votre.email@example.com"
LABEL version="1.0"
LABEL description="ETL Pipeline for Sales Data"

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Create non-root user for security
RUN useradd -m -u 1000 etluser && \
    chown -R etluser:etluser /app

USER etluser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the ETL pipeline
CMD ["python", "src/main.py"]
```

#### .dockerignore

Évitez de copier des fichiers inutiles dans l'image Docker :

```bash
# .dockerignore

# Git
.git
.gitignore
.gitattributes

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
.venv
venv/
ENV/
env/

# Testing
.pytest_cache
.coverage
htmlcov/
.tox/

# IDE
.vscode
.idea
*.swp
*.swo

# Documentation
*.md
docs/

# Data (ne jamais inclure dans l'image)
data/
*.csv
*.parquet
*.json
*.xlsx

# Logs
*.log
logs/

# Docker
docker-compose.yml
Dockerfile
.dockerignore

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile
```

#### docker-compose.yml pour développement local

```bash
# docker-compose.yml
version: '3.8'

services:
  etl-pipeline:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: sales-etl
    volumes:
# Mount source code for development (hot reload)
      - ./src:/app/src
      - ./config:/app/config
# Mount data directory
      - ./data:/app/data
    environment:
      - APP_ENV=development
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=sales
      - DB_USER=etluser
      - DB_PASSWORD=etlpass
    depends_on:
      - postgres
    networks:
      - etl-network

  postgres:
    image: postgres:15-alpine
    container_name: sales-db
    environment:
      - POSTGRES_USER=etluser
      - POSTGRES_PASSWORD=etlpass
      - POSTGRES_DB=sales
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - etl-network

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
    networks:
      - etl-network

volumes:
  postgres-data:

networks:
  etl-network:
    driver: bridge
```

#### Workflow Git + Docker

```bash
# 1. Développement local avec hot reload
git checkout -b feature/add-validation

# Lancer l'environnement de développement
docker-compose up -d

# Les changements dans src/ sont immédiatement reflétés
# car le volume est monté

# 2. Tester vos modifications
docker-compose exec etl-pipeline python -m pytest tests/

# 3. Commiter avec Conventional Commits
git add src/validation.py tests/test_validation.py
git commit -m "feat(validation): add data quality checks

Implement validation rules for:
- Email format
- Date ranges
- Required fields

Closes #42"

# 4. Créer une image Docker taggée avec le commit hash
git push origin feature/add-validation

# 5. Build et tag de l'image pour production
docker build -t myregistry/sales-etl:latest .
docker build -t myregistry/sales-etl:$(git rev-parse --short HEAD) .

# 6. Tester l'image en environnement de staging
docker run --rm \
  -e APP_ENV=staging \
  -e DB_HOST=staging-db.example.com \
  myregistry/sales-etl:$(git rev-parse --short HEAD)

# 7. Si OK, merger et déployer
git checkout main
git merge feature/add-validation
git tag -a v1.2.0 -m "Release 1.2.0: Add data validation"
git push origin main --tags

# 8. Push vers le registry Docker
docker push myregistry/sales-etl:latest
docker push myregistry/sales-etl:v1.2.0
```

#### Scripts d'automatisation

Créez des scripts pour automatiser le workflow :

```bash
#!/bin/bash
# scripts/build.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔨 Building Docker image...${NC}"

# Get Git info
GIT_COMMIT=$(git rev-parse --short HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
VERSION=$(git describe --tags --always)

# Build args
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# Build image
docker build \
  --build-arg GIT_COMMIT=$GIT_COMMIT \
  --build-arg VERSION=$VERSION \
  --build-arg BUILD_DATE=$BUILD_DATE \
  -t myregistry/sales-etl:$VERSION \
  -t myregistry/sales-etl:latest \
  .

echo -e "${GREEN}✅ Build successful!${NC}"
echo "   📦 Images:"
echo "      - myregistry/sales-etl:$VERSION"
echo "      - myregistry/sales-etl:latest"
echo "   🔖 Git commit: $GIT_COMMIT"
echo "   🌿 Git branch: $GIT_BRANCH"
```

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

ENV=${1:-dev}
VERSION=${2:-latest}

echo "🚀 Deploying version $VERSION to $ENV environment..."

# Pull latest image
docker pull myregistry/sales-etl:$VERSION

# Stop and remove old container
docker stop sales-etl-$ENV || true
docker rm sales-etl-$ENV || true

# Run new container
docker run -d \
  --name sales-etl-$ENV \
  --restart unless-stopped \
  -e APP_ENV=$ENV \
  --env-file .env.$ENV \
  myregistry/sales-etl:$VERSION

echo "✅ Deployment successful!"
docker logs -f sales-etl-$ENV
```

#### GitHub Actions pour CI/CD

```bash
# .github/workflows/docker-build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main, develop]
    tags:
      - 'v*'
  pull_request:
    branches: [main]

env:
  REGISTRY: docker.io
  IMAGE_NAME: myusername/sales-etl

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to Docker Hub
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run tests
        run: |
          docker run --rm ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }} \
            python -m pytest tests/
```

#### Bonnes pratiques Git + Docker

- ✅ Versionnez le Dockerfile et docker-compose.yml
- ✅ Utilisez .dockerignore pour réduire la taille de l'image
- ✅ Taggez vos images avec le commit hash ou la version Git
- ✅ Ne jamais commiter de secrets dans le Dockerfile
- ✅ Utilisez des variables d'environnement pour la configuration
- ✅ Créez des images multi-stage pour optimiser la taille
- ❌ Ne jamais inclure de données dans l'image Docker
- ❌ Ne jamais commiter les fichiers .env avec des secrets

#### Exemple complet : Dockerfile multi-stage

```bash
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Add metadata
ARG VERSION=dev
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.revision=$GIT_COMMIT
LABEL org.opencontainers.image.created=$BUILD_DATE

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application
COPY src/ ./src/
COPY config/ ./config/

# Create non-root user
RUN useradd -m -u 1000 etluser && \
    chown -R etluser:etluser /app

USER etluser

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Store Git info in env
ENV VERSION=$VERSION
ENV GIT_COMMIT=$GIT_COMMIT
ENV BUILD_DATE=$BUILD_DATE

CMD ["python", "src/main.py"]
```

### Résumé des workflows

### 🎯 Points clés

- **Conventional Commits** : Structure vos messages pour automatiser changelog et versionnage
- **Commitizen** : Assistant interactif pour créer des commits conformes
- **Commitlint** : Valide automatiquement vos commits avec Git hooks
- **Docker + Git** : Versionnez code ET environnement ensemble
- **Tagging** : Liez les versions Git aux tags Docker pour traçabilité
- **CI/CD** : Automatisez build, test et déploiement avec GitHub Actions
- **Multi-stage builds** : Optimisez la taille des images Docker
- **Scripts** : Automatisez les tâches répétitives

#### ✅ Partie 8 terminée !

Vous maîtrisez maintenant les workflows professionnels avec Conventional Commits et
l'intégration Git + Docker. Vous êtes prêt pour les exercices pratiques !

[🎯 Faire les exercices](../exercices.md)
[🚀 Projet fil rouge](../projet-fil-rouge.md)