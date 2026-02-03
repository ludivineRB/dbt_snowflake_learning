## 🎯 Objectifs d'apprentissage

- Comprendre ce qu'est Azure Databricks et son rôle dans l'écosystème Azure
- Découvrir l'architecture et les composants principaux
- Identifier les cas d'usage et avantages de Databricks
- Différencier Databricks d'autres solutions Azure
- Comprendre le concept de Lakehouse Architecture

## 1. Qu'est-ce qu'Azure Databricks ?

Azure Databricks est une **plateforme d'analyse de données unifiée** basée sur Apache Spark, optimisée pour Microsoft Azure. Elle a été développée par les créateurs originaux d'Apache Spark et offre un environnement collaboratif pour les data engineers, data scientists et analystes.

#### 🚀 Rapidité

Moteur Spark optimisé jusqu'à 50 fois plus rapide que le Spark open source standard

#### 🤝 Collaboration

Notebooks partagés, commentaires en temps réel et gestion de versions intégrée

#### 🔧 Simplicité

Gestion automatisée des clusters, autoscaling et optimisations intégrées

#### 🔐 Sécurité

Intégration native avec Azure AD, encryption et conformité entreprise

### Pourquoi Databricks ?

Databricks résout plusieurs problèmes majeurs rencontrés avec Apache Spark traditionnel :

- **Complexité de configuration :** Installation et configuration simplifiées
- **Gestion des clusters :** Provisionnement et scaling automatiques
- **Performance :** Optimisations propriétaires (Photon engine, Delta Lake)
- **Collaboration :** Environnement unifié pour toutes les équipes data
- **Productivité :** Outils intégrés pour tout le cycle de vie des données

## 2. Architecture Azure Databricks

L'architecture de Databricks se compose de deux plans principaux :

| Plan | Description | Composants |
| --- | --- | --- |
| **Control Plane** | Géré par Databricks (SaaS) | • Interface utilisateur web  • Gestion des notebooks  • Orchestration des clusters  • Scheduler de jobs |
| **Data Plane** | Déployé dans votre abonnement Azure | • Clusters Spark (VMs Azure)  • DBFS (Databricks File System)  • Stockage des données  • Réseau virtuel |

#### Architecture hybride

Cette séparation entre Control Plane et Data Plane permet de combiner la simplicité d'un service managé avec le contrôle et la sécurité d'un déploiement dans votre propre infrastructure Azure.

### Composants principaux

#### Workspace

Environnement de travail contenant notebooks, bibliothèques, dashboards et configurations

#### Clusters

Ensemble de machines virtuelles (driver + workers) exécutant le code Spark

#### Notebooks

Interface interactive pour écrire du code (Python, SQL, Scala, R) et créer des visualisations

#### Jobs

Tâches automatisées et orchestrées pour exécuter des workflows de données

#### Delta Lake

Couche de stockage fiable avec transactions ACID et time travel

#### MLflow

Plateforme open source pour gérer le cycle de vie du Machine Learning

## 3. Cas d'usage Azure Databricks

### Data Engineering

Construisez des pipelines ETL/ELT robustes et scalables :

- Ingestion de données depuis diverses sources (Azure Data Lake, Event Hubs, IoT Hub)
- Transformation et nettoyage de données à grande échelle
- Création de data lakes et data lakehouses
- Streaming en temps réel avec Structured Streaming

### Data Science & Machine Learning

Développez, entraînez et déployez des modèles ML :

- Exploration et analyse de données massives
- Feature engineering distribué
- Entraînement de modèles ML/DL à grande échelle
- MLOps avec MLflow et Model Registry
- AutoML pour la sélection de modèles

### Business Intelligence & Analytics

Analysez vos données et créez des visualisations :

- Requêtes SQL interactives sur de grandes volumétries
- Dashboards et visualisations intégrées
- Connexion avec Power BI, Tableau, etc.
- Data Warehousing moderne avec Delta Lake

#### Exemple de cas d'usage : Pipeline E-commerce

Une entreprise e-commerce utilise Databricks pour :

1. **Ingestion :** Collecter les logs de navigation, transactions, et événements depuis Azure Event Hubs
2. **Transformation :** Nettoyer et enrichir les données avec informations produits et clients
3. **Analyse :** Calculer des métriques business (panier moyen, taux de conversion, churn)
4. **Machine Learning :** Créer un système de recommandation produits en temps réel
5. **Visualisation :** Dashboards Power BI pour le suivi des KPIs

## 4. Databricks vs autres solutions Azure

| Critère | Azure Databricks | Azure Synapse Analytics | HDInsight |
| --- | --- | --- | --- |
| **Focus principal** | Lakehouse unifié pour Data + ML | Data Warehousing & Analytics | Clusters Big Data open source |
| **Facilité d'utilisation** | ⭐⭐⭐⭐⭐ Très simple | ⭐⭐⭐⭐ Simple | ⭐⭐ Complexe |
| **Performance Spark** | ⭐⭐⭐⭐⭐ Optimisé (Photon) | ⭐⭐⭐⭐ Standard | ⭐⭐⭐ Standard |
| **Machine Learning** | ⭐⭐⭐⭐⭐ MLflow intégré | ⭐⭐⭐ Azure ML intégration | ⭐⭐ Configuration manuelle |
| **Collaboration** | ⭐⭐⭐⭐⭐ Notebooks avancés | ⭐⭐⭐⭐ Notebooks | ⭐⭐ Basique |
| **Coût** | Premium (mais optimisé) | Variable selon usage | Moins cher (mais + complexe) |
| **Meilleur pour** | Data Engineering + ML unifié | Analytics SQL, BI | Infrastructure Big Data custom |

#### Quand choisir Databricks ?

- Projets combinant Data Engineering et Machine Learning
- Besoin de performance Spark maximale
- Équipes mixtes (Data Engineers, Data Scientists, Analysts)
- Architecture Lakehouse moderne
- Streaming en temps réel avec batch processing

## 5. Lakehouse Architecture

Databricks a popularisé le concept de **Lakehouse**, qui combine les avantages des Data Lakes et Data Warehouses.

| Approche | Avantages | Inconvénients |
| --- | --- | --- |
| **Data Warehouse** | • Performance SQL excellente  • Transactions ACID  • Schéma structuré | • Coût élevé  • Données structurées uniquement  • Pas de ML natif |
| **Data Lake** | • Stockage peu coûteux  • Tous types de données  • Scalabilité illimitée | • Performance queries faible  • Pas de transactions  • "Data swamp" risk |
| **Lakehouse** | • Combine les deux approches  • ACID + performance SQL  • ML + BI sur mêmes données  • Stockage économique | • Concept relativement récent  • Nécessite Delta Lake |

### Composants du Lakehouse

```bash
┌─────────────────────────────────────────────────────────────┐
│                    LAKEHOUSE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌────────────┐ │
│  │   Sources    │ ───▶ │  Bronze      │ ───▶ │   Silver   │ │
│  │   de données │      │  (Raw)       │      │  (Cleaned) │ │
│  └──────────────┘      └──────────────┘      └────────────┘ │
│       │                       │                      │        │
│       │                       ▼                      ▼        │
│       │              ┌─────────────────────────────────┐      │
│       │              │     Delta Lake Storage         │      │
│       │              │  (ACID, Time Travel, Schema)   │      │
│       │              └─────────────────────────────────┘      │
│       │                              │                        │
│       ▼                              ▼                        │
│  ┌────────────┐              ┌──────────────┐                │
│  │   Gold     │◀──────────── │  Compute     │                │
│  │ (Curated)  │              │  (Spark)     │                │
│  └────────────┘              └──────────────┘                │
│       │                                                       │
│       ├──────────────┬──────────────┬────────────────┐       │
│       ▼              ▼              ▼                ▼       │
│   ┌──────┐      ┌────────┐    ┌────────┐      ┌────────┐   │
│   │  BI  │      │   ML   │    │ Apps   │      │ Users  │   │
│   └──────┘      └────────┘    └────────┘      └────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Médaillons Bronze-Silver-Gold

#### 🥉 Bronze

**Données brutes**

- Ingestion sans transformation
- Format original préservé
- Historique complet

#### 🥈 Silver

**Données nettoyées**

- Validation et nettoyage
- Déduplication
- Standardisation

#### 🥇 Gold

**Données business**

- Agrégations
- Métriques business
- Prêt pour BI/ML

### 📌 Points clés à retenir

- Azure Databricks est une plateforme unifiée pour Data Engineering, Science et Analytics
- Architecture en deux plans : Control Plane (managé) et Data Plane (votre Azure)
- Optimisations propriétaires rendant Spark jusqu'à 50x plus rapide
- Lakehouse Architecture combine avantages Data Lake + Data Warehouse
- Delta Lake apporte ACID transactions et time travel aux données
- Solution idéale pour projets nécessitant Data + ML sur mêmes données

#### Prochaine étape

Maintenant que vous comprenez ce qu'est Azure Databricks, passons à la **Partie 2** pour apprendre à créer et configurer votre premier workspace !