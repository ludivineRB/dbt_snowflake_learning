# Formation Data Engineer - Simplon

Bienvenue dans le repository de formation Data Engineer ! Ce dépôt contient l'ensemble des ressources pédagogiques pour le parcours Data Engineer, incluant les fondamentaux DevOps et Cloud.

## Table des matières

- [À propos](#à-propos)
- [Structure du repository](#structure-du-repository)
- [Technologies couvertes](#technologies-couvertes)
- [Prérequis](#prérequis)
- [Comment utiliser ce repository](#comment-utiliser-ce-repository)
- [Parcours d'apprentissage](#parcours-dapprentissage)
- [Contribution](#contribution)
- [Support](#support)

## À propos

Ce repository regroupe un cursus complet pour devenir Data Engineer. Il couvre l'ensemble de la chaîne de valeur de la donnée, de l'infrastructure à l'analyse, en passant par l'ingestion et la transformation.

Chaque module contient :
- Des cours théoriques
- Des exercices pratiques
- Des projets guidés (briefs)
- Des ressources complémentaires

## Structure du repository

```
formation-data-engineer/
├── 01-Fondamentaux/           # Socle technique indispensable
│   ├── Bash-Zsh/              # Ligne de commande
│   ├── Bonne pratique/        # Clean Code, Architecture, Git flow
│   ├── Git/                   # Gestion de versions
│   ├── Github/                # Collaboration
│   └── Python/                # Langage principal pour la Data
├── 02-Containerisation/       # Standardisation des environnements
│   ├── Docker/                # Création de conteneurs
│   └── Kubernetes/            # Orchestration
├── 03-Infrastructure-as-Code/ # Gestion de l'infrastructure
│   ├── Ansible/               # Gestion de configuration
│   └── Terraform/             # Provisioning d'infrastructure
├── 04-Cloud-Platforms/        # Environnements Cloud
│   ├── Azure/                 # Microsoft Azure (Databricks, Hadoop...)
│   ├── GCP/                   # Google Cloud Platform
│   └── snowflake/             # Data Warehouse Cloud
├── 05-Databases/              # Stockage des données
│   ├── DataWarehouse/         # Concepts DWH
│   └── MongoDb/               # NoSQL
├── 06-Data-Engineering/       # Cœur du métier
│   ├── Dbt/                   # Transformation (ELT)
│   ├── DltHub/                # Ingestion (EL)
│   ├── Fabric/                # Solution tout-en-un Microsoft
│   └── Spark/                 # Traitement Big Data distribué
├── 07-DevOps/                 # Industrialisation
│   ├── 01-CI-CD/              # Intégration et Déploiement Continus
│   └── 02-Monitoring/         # Surveillance (Grafana, Prometheus)
└── 99-Brief/                  # Projets fil rouge et évaluations
```

## Technologies couvertes

### 1. Fondamentaux & Développement
- **Python** : Le langage de référence pour la data (POO, Tests, Data Engineering).
- **Bash/Zsh** : Maîtrise du terminal.
- **Git/GitHub** : Versionning et travail collaboratif.
- **Bonnes Pratiques** : Clean Code, Architecture, Sécurité.

### 2. Infrastructure & Cloud
- **Docker & Kubernetes** : Déploiement d'applications conteneurisées.
- **Terraform & Ansible** : Infrastructure as Code (IaC).
- **Azure & GCP** : Plateformes Cloud majeures.

### 3. Data Engineering & Big Data
- **Spark** : Traitement de données massives.
- **Dbt** : Transformation de données (Analytics Engineering).
- **Snowflake** : Data Warehouse moderne.
- **Microsoft Fabric** : Plateforme analytique unifiée.
- **DltHub** : Pipelines d'ingestion de données légers.
- **MongoDB** : Bases de données orientées documents.

### 4. DevOps & Industrialisation
- **CI/CD** : Pipelines d'automatisation (GitHub Actions, GitLab CI).
- **Monitoring** : Prometheus, Grafana, Uptime Kuma.

## Prérequis

### Outils recommandés
- **Système** : Linux, macOS ou Windows avec WSL2.
- **Code** : VS Code avec les extensions appropriées (Python, Docker, Terraform...).
- **Conteneurs** : Docker Desktop ou Rancher Desktop.
- **Cloud** : CLI Azure, CLI Google Cloud, CLI Snowflake.

### Connaissances de base
- Compréhension de base du fonctionnement d'un ordinateur et d'un réseau.
- Notions d'algorithmique.

## Comment utiliser ce repository

1.  **Cloner le projet** :
    ```bash
    git clone <url-du-repo>
    cd formation-data-engineer
    ```

2.  **Suivre la progression** :
    Le cursus est conçu pour être suivi séquentiellement, du module `01-Fondamentaux` au module `07-DevOps`.

3.  **Réaliser les Briefs** :
    Le dossier `99-Brief/` contient des projets concrets pour valider vos acquis (ex: Pipeline NYC Taxi, Analyse Qualité de l'Eau, etc.).

## Parcours d'apprentissage suggéré

1.  **Onboarding (Semaines 1-2)**
    - Maîtriser le shell, Git et les bases de Python (`01-Fondamentaux`).

2.  **Environnement & Infra (Semaines 3-5)**
    - Comprendre Docker et Kubernetes (`02-Containerisation`).
    - Automatiser avec Terraform et Ansible (`03-Infrastructure-as-Code`).

3.  **Data Engineering Core (Semaines 6-10)**
    - Bases de données (`05-Databases`, `04-Cloud-Platforms/snowflake`).
    - Traitement distribué avec Spark (`06-Data-Engineering/Spark`).
    - Modern Data Stack avec dbt et dlt (`06-Data-Engineering`).

4.  **Cloud & Industrialisation (Semaines 11+)**
    - Déploiement sur Azure/GCP (`04-Cloud-Platforms`).
    - Mise en place de pipelines CI/CD et monitoring (`07-DevOps`).

## Contribution

Les contributions sont les bienvenues !
Veuillez suivre les bonnes pratiques définies dans `01-Fondamentaux/Bonne pratique`.

## Support

Pour toute question technique, référez-vous d'abord à la documentation officielle des outils, puis aux README spécifiques de chaque module.