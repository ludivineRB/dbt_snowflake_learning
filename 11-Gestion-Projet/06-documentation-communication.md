[← Precedent](05-faisabilite-technique-financiere.md) | [🏠 Accueil](README.md) | [Suivant →](07-accessibilite-eco-conception.md)

# Lecon 6 - Documentation et Communication

## 🎯 Objectifs

- Rediger un Document d'Architecture Technique (DAT) complet
- Documenter les pipelines, APIs et dictionnaires de donnees
- Communiquer efficacement avec les parties prenantes metier
- Mettre en place une strategie "Docs as Code" avec versionning
- Adapter la communication selon l'audience (technique vs business)

---

## 1. Documentation Technique

### 1.1 Le Document d'Architecture Technique (DAT)

Le DAT est le **document de reference** qui decrit l'architecture technique d'un projet data. Il est a la fois un outil de conception (avant le developpement) et un outil de maintenance (apres le deploiement).

#### Quand rediger un DAT ?

| Phase | Contenu du DAT |
|-------|---------------|
| **Cadrage** | Version initiale : architecture cible, choix techniques justifies |
| **Developpement** | Mise a jour : schemas detailles, configurations, decisions prises |
| **Deploiement** | Finalisation : architecture reelle, monitoring, plan de reprise |
| **Maintenance** | Mise a jour continue : evolutions, incidents majeurs, lessons learned |

#### Template de DAT pour un projet data

```markdown
# Document d'Architecture Technique (DAT)
# [Nom du Projet]

## Informations generales
- Version : 1.0
- Date : YYYY-MM-DD
- Auteur : [Nom]
- Relecteurs : [Noms]
- Statut : Brouillon | En revue | Valide

## Table des matieres
1. Contexte et objectifs
2. Architecture generale
3. Architecture des donnees
4. Architecture applicative
5. Infrastructure et deploiement
6. Securite
7. Monitoring et observabilite
8. Plan de reprise d'activite
9. Decisions d'architecture (ADR)
10. Annexes

---

## 1. Contexte et objectifs

### 1.1 Contexte du projet
[Description du contexte metier et technique]

### 1.2 Objectifs techniques
- Objectif 1 : [ex: Ingerer 5 sources de donnees en quasi temps reel]
- Objectif 2 : [ex: Garantir une latence < 15 minutes]
- Objectif 3 : [ex: Supporter 100 utilisateurs concurrents]

### 1.3 Contraintes
- Budget : [montant]
- Delai : [date cible]
- Reglementaire : [RGPD, secteur regulemente, etc.]
- Technique : [stack existante, contraintes d'integration]

### 1.4 Perimetre
- In scope : [liste]
- Out of scope : [liste]

---

## 2. Architecture generale

### 2.1 Vue d'ensemble

[Schema d'architecture de haut niveau]

### 2.2 Composants principaux

| Composant | Role | Technologie | Justification |
|-----------|------|-------------|---------------|
| Ingestion | Extraction des sources | Airbyte | Open source, connecteurs natifs |
| Orchestration | Planification des taches | Airflow | Standard du marche, extensible |
| Transformation | Modelisation des donnees | dbt | SQL-based, tests integres, lineage |
| Stockage | Data Warehouse | Snowflake | Scalabilite, separation compute/storage |
| Visualisation | Dashboards | Power BI | Deja en place, maitrise par le metier |
| Monitoring | Surveillance | Datadog | Centralise, alertes configurables |

### 2.3 Flux de donnees

[Schema detaille des flux : sources -> ingestion -> staging ->
transformation -> serving -> visualisation]

---

## 3. Architecture des donnees

### 3.1 Sources de donnees

| Source | Type | Volume | Frequence | Format |
|--------|------|--------|-----------|--------|
| CRM | API REST | 2.5M enregistrements | Quotidien | JSON |
| ERP | Base PostgreSQL | 500 Go | Quotidien | Tables relationnelles |
| Web Analytics | API | 10M events/jour | Horaire | JSON |

### 3.2 Modele de donnees

#### Couche Bronze (Raw)
[Schema des tables brutes]

#### Couche Silver (Cleaned)
[Schema des tables nettoyees]

#### Couche Gold (Business)
[Schema du modele dimensional : faits + dimensions]

### 3.3 Dictionnaire de donnees
[Lien vers le dictionnaire de donnees complet]

### 3.4 Lineage
[Schema de lineage des donnees : source -> transformations -> destination]

---

## 4. Architecture applicative

### 4.1 Pipeline ETL/ELT
[Description detaillee de chaque pipeline]

### 4.2 APIs exposees
[Specs OpenAPI/Swagger si applicable]

### 4.3 Batch vs Streaming
[Justification du choix batch/streaming par flux]

---

## 5. Infrastructure et deploiement

### 5.1 Environnements

| Environnement | Usage | Infrastructure |
|--------------|-------|----------------|
| Dev | Developpement | AWS, t3.small, Snowflake XS |
| Staging | Tests et validation | AWS, t3.medium, Snowflake S |
| Production | Production | AWS, t3.large, Snowflake M |

### 5.2 CI/CD
[Description du pipeline CI/CD : GitHub Actions, tests, deploiement]

### 5.3 Infrastructure as Code
[Terraform, CDK, ou equivalent]

---

## 6. Securite

### 6.1 Authentification et autorisation
[IAM, RBAC, SSO]

### 6.2 Chiffrement
[At rest, in transit]

### 6.3 Conformite RGPD
[Anonymisation, pseudonymisation, retention]

---

## 7. Monitoring et observabilite

### 7.1 Metriques surveillees

| Metrique | Seuil d'alerte | Outil |
|----------|:-------------:|-------|
| Temps d'execution pipeline | > 2h | Datadog |
| Taux d'erreur pipeline | > 1% | Datadog |
| Qualite donnees (tests dbt) | Echec | Slack |
| Cout Snowflake | > 1000 EUR/jour | Snowflake alerts |

### 7.2 Alerting
[Canaux d'alerte : Slack, email, PagerDuty]

### 7.3 Logging
[Strategie de logging : niveaux, retention, centralisation]

---

## 8. Plan de reprise d'activite (PRA)

### 8.1 RTO / RPO

| Metrique | Cible |
|----------|:-----:|
| RTO (Recovery Time Objective) | 4 heures |
| RPO (Recovery Point Objective) | 24 heures |

### 8.2 Strategie de backup
[Frequence, retention, localisation]

### 8.3 Procedure de rollback
[Etapes detaillees de rollback]

---

## 9. Decisions d'architecture (ADR)

### ADR-001 : Choix de Snowflake comme Data Warehouse
- **Date** : 2026-01-15
- **Statut** : Accepte
- **Contexte** : Besoin d'un DWH scalable, separation compute/storage
- **Decision** : Snowflake plutot que BigQuery ou Redshift
- **Justification** : Multi-cloud, auto-scaling, cout previsible,
  meilleur support France
- **Consequences** : Lock-in Snowflake, necessite formation equipe

### ADR-002 : dbt plutot que procedures stockees
- **Date** : 2026-01-20
- **Statut** : Accepte
- **Contexte** : Transformations actuellement en procedures stockees SQL Server
- **Decision** : Migrer vers dbt pour les transformations
- **Justification** : Version control, tests integres, documentation auto,
  lineage
- **Consequences** : Courbe d'apprentissage, necessite refactoring

---

## 10. Annexes
- Glossaire technique
- Schema detaille de la base de donnees
- Configuration des outils
- Contacts de l'equipe
```

### 1.2 Documentation des pipelines

Chaque pipeline doit etre documente avec les informations suivantes :

| Element | Description | Exemple |
|---------|------------|---------|
| **Nom** | Identifiant unique | `pipeline_sales_daily` |
| **Description** | Ce que fait le pipeline | "Ingere les ventes quotidiennes depuis PostgreSQL et les transforme en modele dimensional dans Snowflake" |
| **Source(s)** | D'ou viennent les donnees | PostgreSQL `sales_db`, tables `orders`, `order_items` |
| **Destination** | Ou vont les donnees | Snowflake, schema `gold`, tables `fact_sales`, `dim_products` |
| **Frequence** | Quand le pipeline s'execute | Quotidien a 6h00 UTC |
| **Duree moyenne** | Temps d'execution | 45 minutes |
| **SLA** | Deadline de completion | Avant 8h00 UTC (debut de journee France) |
| **Owner** | Qui est responsable | @jean.dupont |
| **Dependances** | Autres pipelines requis | `pipeline_products_sync` doit etre termine avant |
| **Tests** | Tests de qualite associes | 12 tests dbt (unicite, nullite, coherence) |
| **Alertes** | Que se passe-t-il en cas d'echec | Slack #data-alerts + email owner |

### 1.3 Dictionnaire de donnees

Le dictionnaire de donnees decrit chaque table et chaque colonne du data warehouse.

#### Template

| Table | Colonne | Type | Nullable | Description | Exemple | Source |
|-------|---------|------|:--------:|-------------|---------|--------|
| `fact_sales` | `sale_id` | BIGINT | Non | Identifiant unique de la vente | 123456 | PostgreSQL `orders.id` |
| `fact_sales` | `sale_date` | DATE | Non | Date de la vente | 2026-01-15 | PostgreSQL `orders.created_at` |
| `fact_sales` | `customer_id` | BIGINT | Non | FK vers `dim_customers` | 789 | PostgreSQL `orders.customer_id` |
| `fact_sales` | `product_id` | BIGINT | Non | FK vers `dim_products` | 456 | PostgreSQL `order_items.product_id` |
| `fact_sales` | `quantity` | INT | Non | Nombre d'unites vendues | 3 | PostgreSQL `order_items.quantity` |
| `fact_sales` | `amount_ht` | DECIMAL(10,2) | Non | Montant HT en euros | 149.99 | Calcule : `quantity * unit_price` |
| `fact_sales` | `amount_ttc` | DECIMAL(10,2) | Non | Montant TTC en euros | 179.99 | Calcule : `amount_ht * (1 + tva_rate)` |

💡 **Astuce** : Le dictionnaire de donnees doit etre **genere automatiquement** autant que possible (dbt docs, Great Expectations, ou un script maison). La documentation manuelle devient obsolete tres rapidement.

### 1.4 Documentation des APIs

Pour les APIs exposees par le projet data, utilisez le standard **OpenAPI/Swagger** :

```yaml
openapi: 3.0.0
info:
  title: API Data Ventes
  version: 1.0.0
  description: API REST pour acceder aux donnees de ventes agrégées

paths:
  /api/v1/sales/daily:
    get:
      summary: Ventes quotidiennes
      description: Retourne les ventes agrégées par jour
      parameters:
        - name: start_date
          in: query
          required: true
          schema:
            type: string
            format: date
          example: "2026-01-01"
        - name: end_date
          in: query
          required: true
          schema:
            type: string
            format: date
          example: "2026-01-31"
        - name: region
          in: query
          required: false
          schema:
            type: string
          example: "Ile-de-France"
      responses:
        '200':
          description: Liste des ventes quotidiennes
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    date:
                      type: string
                      format: date
                    total_sales:
                      type: number
                    total_orders:
                      type: integer
        '400':
          description: Parametres invalides
        '500':
          description: Erreur serveur
```

### 1.5 Standards README pour les repos data

Chaque repo data doit avoir un README structure :

```markdown
# [Nom du Projet]

> [Description en 1-2 phrases]

## Quick Start
[Comment lancer le projet en 3 commandes max]

## Architecture
[Schema simplifie + lien vers le DAT]

## Structure du repo
[Arborescence des dossiers principaux]

## Pre-requis
[Python, Docker, credentials necessaires]

## Installation
[Etapes detaillees]

## Usage
[Commandes principales]

## Tests
[Comment lancer les tests]

## Deploiement
[Comment deployer]

## Monitoring
[Ou voir les dashboards de monitoring]

## Contributing
[Comment contribuer : branches, PR, code review]

## Equipe
[Contacts]
```

---

## 2. Communication avec le Metier

### 2.1 Traduire le technique en business

L'une des competences les plus importantes d'un Data Engineer est de **traduire** les concepts techniques en langage business compris par les parties prenantes non-techniques.

| Jargon technique | Traduction business |
|-----------------|-------------------|
| "Le pipeline ETL a echoue" | "Les donnees du rapport ne sont pas a jour ce matin" |
| "Il y a un drift dans le modele ML" | "Les predictions sont moins fiables qu'avant, il faut reajuster" |
| "On a un probleme de cardinalite sur la jointure" | "Certaines lignes du rapport sont dupliquees" |
| "Le warehouse Snowflake est sous-dimensionne" | "Le rapport met trop de temps a se charger aux heures de pointe" |
| "Il faut implementer un CDC pour le temps reel" | "On va pouvoir afficher les donnees en quasi temps reel" |
| "Les tests dbt echouent sur la table customers" | "On a detecte un probleme de qualite sur les donnees clients" |
| "On va passer d'un batch quotidien a du micro-batch" | "Les donnees seront mises a jour toutes les 15 minutes au lieu d'une fois par jour" |

### 2.2 Templates de presentation

#### Executive Summary (pour la Direction)

```
EXECUTIVE SUMMARY - [Nom du Projet]
Date : [Date]
Statut : 🟢 En bonne voie / 🟡 A risque / 🔴 En difficulte

AVANCEMENT
- Sprint 4/8 termine
- 60% des fonctionnalites livrees
- Budget consomme : 55% (en ligne avec le planning)

REALISATIONS DE LA PERIODE
- Pipeline de ventes en production (objectif atteint)
- Dashboard v1 livre et valide par l'equipe commerciale
- 3 tests de qualite automatises deployes

PROCHAINES ETAPES
- Sprint 5 : Pipeline stocks + modele dimensional
- Sprint 6 : Dashboard v2 avec filtres avances

RISQUES ET ALERTES
- 🟡 Acces a l'API ERP en attente (impact potentiel : 1 semaine de retard)
- 🟢 Tous les autres risques sous controle

DECISION DEMANDEE
- Aucune decision requise cette semaine
```

#### Demo Sprint Review (pour le PO et le metier)

**Structure recommandee** :
1. **Rappel du Sprint Goal** (2 min)
2. **Demo en live sur donnees reelles** (15 min)
3. **Metriques de qualite** (5 min) : "Voici la qualite des donnees qui alimentent ce que vous venez de voir"
4. **Feedback** (10 min) : Questions, ajustements, nouvelles idees
5. **Preview du prochain sprint** (3 min)

#### Retrospective (pour l'equipe)

| Colonne | Questions |
|---------|----------|
| **Ce qui a bien fonctionne** | Qu'est-ce qu'on doit continuer a faire ? |
| **Ce qui peut etre ameliore** | Qu'est-ce qui nous a ralentis ou frustres ? |
| **Actions** | Quelles actions concretes pour le prochain sprint ? |

### 2.3 Reporting et frequence de communication

| Audience | Format | Frequence | Contenu |
|----------|--------|-----------|---------|
| Direction / Sponsor | Executive Summary (1 page) | Mensuel ou bimensuel | Avancement, budget, risques, decisions |
| PO / Metier | Sprint Review + Demo | Toutes les 2 semaines | Fonctionnalites livrees, feedback |
| Equipe technique | Daily Standup | Quotidien | Blocages, avancement, coordination |
| Equipe technique | Retrospective | Toutes les 2 semaines | Amelioration continue |
| DSI / Architecture | Comite technique | Mensuel | Architecture, performance, securite |
| DPO | Point conformite | Mensuel | Donnees personnelles, traitements, audits |

### 2.4 Gestion des parties prenantes

| Type de partie prenante | Ce qu'elle veut savoir | Ce qu'il ne faut PAS faire |
|------------------------|----------------------|--------------------------|
| **Sponsor** | "Est-ce dans les temps et le budget ?" | Noyer dans les details techniques |
| **PO** | "Les fonctionnalites correspondent-elles aux besoins ?" | Parler de l'infrastructure |
| **Utilisateur final** | "Comment ca marche ? C'est fiable ?" | Utiliser du jargon technique |
| **DSI** | "Est-ce securise, scalable, maintenable ?" | Minimiser les risques techniques |
| **DPO** | "Est-ce conforme au RGPD ?" | Ignorer les donnees personnelles |

---

## 3. Version Control pour la Documentation

### 3.1 Docs as Code

Le principe "Docs as Code" consiste a traiter la documentation comme du code :

| Principe | Application |
|----------|------------|
| **Versionne** | Documentation dans le meme repo Git que le code |
| **Revise** | Pull Request pour les modifications de documentation |
| **Automatise** | Generation automatique (dbt docs, Swagger, MkDocs) |
| **Testee** | Linting Markdown, verification des liens morts |
| **Deployee** | Publication automatique sur un site statique (GitHub Pages, MkDocs) |

### 3.2 Structure de documentation dans un repo

```
mon-projet-data/
├── README.md                    # Quick start et overview
├── docs/
│   ├── architecture/
│   │   ├── DAT.md              # Document d'Architecture Technique
│   │   ├── ADR/                # Architecture Decision Records
│   │   │   ├── 001-choix-dwh.md
│   │   │   ├── 002-choix-orchestrateur.md
│   │   │   └── template.md
│   │   └── diagrams/           # Schemas d'architecture
│   │       ├── architecture-overview.png
│   │       └── data-flow.png
│   ├── data-dictionary/
│   │   ├── bronze.md           # Tables brutes
│   │   ├── silver.md           # Tables nettoyees
│   │   └── gold.md             # Tables metier
│   ├── runbooks/
│   │   ├── incident-pipeline.md
│   │   ├── rollback-procedure.md
│   │   └── monitoring-guide.md
│   └── onboarding/
│       ├── setup-local.md
│       └── conventions.md
├── CHANGELOG.md                 # Historique des changements
├── CONTRIBUTING.md              # Guide de contribution
├── dbt/
│   └── (les docs dbt sont generees automatiquement)
└── ...
```

### 3.3 Changelog - Format recommande

Le changelog documente les changements notables du projet dans un format lisible par les humains :

```markdown
# Changelog

## [1.3.0] - 2026-02-01
### Ajoute
- Pipeline d'ingestion des donnees de stocks depuis l'ERP
- 5 nouveaux tests de qualite sur la table `dim_products`

### Modifie
- Optimisation du pipeline de ventes : temps reduit de 45min a 22min
- Mise a jour du modele dimensional : ajout de la dimension `region`

### Corrige
- Correction du doublon sur `customer_id` dans `fact_sales`
- Fix de l'alerte faux positif sur le monitoring du weekend

### Supprime
- Suppression de la vue `legacy_sales_report` (depreciated depuis v1.1)

## [1.2.0] - 2026-01-15
### Ajoute
- Dashboard de ventes v2 avec filtres par region
- Export CSV/Excel depuis le dashboard
...
```

### 3.4 Documentation automatisee

| Outil | Ce qu'il genere | Quand l'utiliser |
|-------|----------------|-----------------|
| **dbt docs** | Documentation des modeles dbt, lineage, tests | Projet utilisant dbt |
| **Swagger / OpenAPI** | Documentation d'API interactive | API REST |
| **MkDocs** | Site de documentation statique depuis Markdown | Documentation de projet |
| **Great Expectations** | Rapports de qualite de donnees | Monitoring qualite |
| **Sphinx** | Documentation Python generee depuis les docstrings | Bibliotheques Python |
| **dbdiagram.io** | Schemas de base de donnees | Modelisation |

---

## 4. Synthese

| Concept | Point cle |
|---------|-----------|
| DAT | Document de reference vivant, pas un livrable final |
| Documentation pipeline | Source, transformation, destination, SLA, owner |
| Dictionnaire de donnees | Generer automatiquement autant que possible |
| Communication metier | Traduire le technique en business, adapter le format a l'audience |
| Docs as Code | Documentation versionnee, revisee, automatisee, deployee |
| Changelog | Historique lisible des changements notables |

### Les 3 regles d'or

1. **Documentation = code** - Elle doit etre versionnee, revisee et maintenue
2. **Automatiser avant de documenter** - Les docs manuelles deviennent obsoletes
3. **Adapter le message a l'audience** - Le sponsor ne veut pas voir un schema de base de donnees

---

📝 **Exercice** : Pour un projet de pipeline ETL (3 sources, 1 data warehouse, 1 dashboard), redigez le squelette d'un DAT (sections 1-3 avec le contenu principal) et preparez un Executive Summary d'une page pour le sponsor.

---

[← Precedent](05-faisabilite-technique-financiere.md) | [🏠 Accueil](README.md) | [Suivant →](07-accessibilite-eco-conception.md)

---

**Academy** - Formation Data Engineer
