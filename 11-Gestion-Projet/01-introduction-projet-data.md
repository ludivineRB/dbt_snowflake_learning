[🏠 Accueil](README.md) | [Suivant →](02-cadrage-expression-besoins.md)

# Lecon 1 - Introduction aux Projets Data

## 🎯 Objectifs

- Comprendre ce qu'est un projet data et ses specificites
- Identifier les differences avec un projet logiciel classique
- Maitriser le cycle de vie d'un projet data
- Connaitre les roles cles et la matrice RACI
- Eviter les ecueils les plus courants

---

## 1. Qu'est-ce qu'un Projet Data ?

### 1.1 Definition

Un **projet data** est un projet dont l'objectif principal est de **collecter, transformer, stocker, analyser ou exploiter des donnees** pour creer de la valeur metier. Contrairement a un projet logiciel classique ou l'on construit une application avec des specifications fonctionnelles claires, un projet data implique une part significative d'**incertitude liee aux donnees elles-memes**.

### 1.2 Differences avec un projet logiciel classique

| Dimension | Projet Logiciel Classique | Projet Data |
|-----------|--------------------------|-------------|
| **Entrees** | Specifications fonctionnelles claires | Donnees brutes, qualite incertaine |
| **Sortie** | Application fonctionnelle | Pipeline, dashboard, modele ML, data warehouse |
| **Incertitude** | Faible a moyenne (on sait ce qu'on construit) | Elevee (la donnee peut ne pas exister ou etre inexploitable) |
| **Exploration** | Limitee (prototypage UI) | Essentielle (EDA, audit de donnees) |
| **Iteration** | Sprint -> Livraison | Exploration -> Experimentation -> Validation -> Livraison |
| **Critere de succes** | L'application fonctionne selon les specs | La donnee est fiable, accessible, et repond au besoin metier |
| **Maintenance** | Correction de bugs, evolution fonctionnelle | Derive des donnees, evolution des schemas, monitoring qualite |
| **Alignement metier** | Important | **Critique** (sans alignement metier, le projet n'a aucune valeur) |
| **Tests** | Tests unitaires, integration, E2E | Tests de qualite de donnees, tests de pipeline, tests de modele |
| **Documentation** | Specs fonctionnelles, API docs | Dictionnaire de donnees, lineage, catalogue |

### 1.3 Les 3 specificites fondamentales d'un projet data

**1. L'incertitude sur la qualite des donnees**

On ne sait pas toujours ce qu'on va trouver dans les donnees. Un champ "email" peut contenir des numeros de telephone. Un champ "date" peut avoir 15 formats differents. Avant de construire quoi que ce soit, il faut **auditer les donnees**.

**2. Le besoin d'exploration iterative**

Contrairement a un projet logiciel ou l'on code directement les specs, un projet data necessite une phase d'exploration : comprendre la donnee, identifier les patterns, valider les hypotheses. Cette phase est **incompressible** et doit etre prevue dans le planning.

**3. L'alignement metier permanent**

Un pipeline ETL techniquement parfait qui ne repond pas au besoin metier ne vaut rien. L'alignement avec les equipes metier doit etre **continu**, pas seulement en debut de projet.

💡 **Astuce** : La regle d'or d'un projet data est "Garbage In, Garbage Out". Si vos donnees d'entree sont de mauvaise qualite, votre sortie le sera aussi, quel que soit la sophistication de votre pipeline ou de votre modele.

---

## 2. Le Cycle de Vie d'un Projet Data

### 2.1 Vue d'ensemble

```
┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────┐
│          │    │             │    │              │    │             │    │             │    │          │
│ CADRAGE  │───>│ EXPLORATION │───>│DEVELOPPEMENT │───>│ DEPLOIEMENT │───>│ MAINTENANCE │───>│EVOLUTION │
│          │    │             │    │              │    │             │    │             │    │          │
└──────────┘    └─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘    └──────────┘
   2-4 sem         2-4 sem           4-12 sem            1-2 sem           Continue          Continue
```

### 2.2 Phase 1 : Cadrage (2-4 semaines)

**Objectif** : Definir le perimetre, les objectifs et les moyens du projet.

Activites cles :
- Entretiens avec les parties prenantes metier
- Audit preliminaire des donnees disponibles
- Expression de besoins et redaction du cahier des charges
- Evaluation de la faisabilite technique et financiere
- Decision Go/No-Go

**Livrable** : Cahier des charges valide, backlog initial

### 2.3 Phase 2 : Exploration (2-4 semaines)

**Objectif** : Comprendre les donnees et valider la faisabilite technique.

Activites cles :
- Audit detaille des sources de donnees (qualite, volume, format, acces)
- Analyse exploratoire (EDA) sur des echantillons
- Prototype / POC sur un perimetre reduit
- Identification des risques techniques
- Validation du choix de la stack technique

**Livrable** : Rapport d'audit, POC valide, architecture technique proposee

### 2.4 Phase 3 : Developpement (4-12 semaines)

**Objectif** : Construire la solution de maniere iterative.

Activites cles :
- Developpement des pipelines / modeles / dashboards par sprints
- Tests de qualite de donnees a chaque iteration
- Revues de code et revues de donnees
- Integration continue / Deploiement continu (CI/CD)
- Documentation au fil de l'eau

**Livrable** : Solution fonctionnelle, tests automatises, documentation technique

### 2.5 Phase 4 : Deploiement (1-2 semaines)

**Objectif** : Mettre en production la solution.

Activites cles :
- Deploiement sur l'environnement de production
- Configuration du monitoring et des alertes
- Formation des utilisateurs
- Tests de non-regression en production
- Plan de rollback

**Livrable** : Solution en production, monitoring operationnel, documentation utilisateur

### 2.6 Phase 5 : Maintenance (continue)

**Objectif** : Garantir le bon fonctionnement et la qualite dans le temps.

Activites cles :
- Surveillance de la qualite des donnees (drift, anomalies)
- Correction des incidents
- Optimisation des performances
- Mise a jour des dependances
- Monitoring des couts cloud

**Livrable** : Rapports de monitoring, SLA respectes

### 2.7 Phase 6 : Evolution (continue)

**Objectif** : Adapter la solution aux nouveaux besoins.

Activites cles :
- Ajout de nouvelles sources de donnees
- Evolution des transformations
- Amelioration des modeles ML (retraining, nouvelles features)
- Extension du perimetre fonctionnel

**Livrable** : Nouvelles fonctionnalites, backlog mis a jour

---

## 3. Les Roles Cles d'un Projet Data

### 3.1 Les roles techniques

| Role | Responsabilites principales | Competences cles |
|------|---------------------------|-----------------|
| **Data Engineer** | Concevoir et maintenir les pipelines de donnees, assurer la qualite et la disponibilite des donnees | Python, SQL, Spark, Airflow, Cloud (AWS/GCP/Azure), dbt |
| **Data Analyst** | Analyser les donnees pour en extraire des insights, creer des dashboards et rapports | SQL, Excel, Power BI/Tableau, statistiques descriptives |
| **Data Scientist** | Construire des modeles predictifs et des algorithmes d'apprentissage | Python, ML/DL, statistiques, feature engineering |
| **ML Engineer** | Industrialiser les modeles ML (MLOps), deployer et monitorer en production | Python, Docker, Kubernetes, MLflow, CI/CD |
| **DevOps / Platform Engineer** | Gerer l'infrastructure, la CI/CD, la securite | Terraform, Docker, Kubernetes, Cloud, monitoring |

### 3.2 Les roles fonctionnels et transverses

| Role | Responsabilites principales |
|------|---------------------------|
| **Data Product Manager** | Definir la vision produit data, prioriser le backlog, aligner les equipes techniques et metier |
| **Product Owner (PO)** | Porter la voix du client, rediger les User Stories, valider les livraisons |
| **Scrum Master** | Faciliter les ceremonies agiles, lever les blocages, ameliorer les processus |
| **DPO (Data Protection Officer)** | Garantir la conformite RGPD, valider les traitements de donnees personnelles |
| **Architecte Data** | Definir l'architecture technique globale, choix des technologies |
| **Sponsor / Commanditaire** | Fournir le budget et le support managerial, valider les orientations strategiques |

### 3.3 Matrice RACI - Exemple pour un projet data

La matrice RACI definit pour chaque activite qui est :
- **R** (Responsible) : Celui qui fait le travail
- **A** (Accountable) : Celui qui rend des comptes (un seul par activite)
- **C** (Consulted) : Celui qu'on consulte avant de decider
- **I** (Informed) : Celui qu'on informe apres la decision

| Activite | Data Engineer | Data Scientist | PO | Scrum Master | DPO | Sponsor |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|
| Expression de besoins | C | C | **R/A** | I | C | I |
| Audit des donnees | **R/A** | C | I | I | C | I |
| Architecture technique | **R/A** | C | I | I | I | I |
| Developpement pipeline | **R/A** | I | C | I | I | I |
| Developpement modele ML | C | **R/A** | C | I | I | I |
| Tests qualite de donnees | **R/A** | C | I | I | I | I |
| Validation RGPD | C | C | C | I | **R/A** | I |
| Sprint Planning | C | C | **R/A** | R | I | I |
| Retrospective | R | R | R | **R/A** | I | I |
| Decision Go/No-Go | C | C | R | I | C | **A** |
| Mise en production | **R/A** | C | I | I | I | I |
| Formation utilisateurs | C | C | **R/A** | I | I | I |

💡 **Astuce** : Une erreur courante est d'avoir plusieurs "A" (Accountable) pour une meme activite. Il ne doit y en avoir qu'un seul : c'est la personne qui prend la responsabilite finale.

---

## 4. Types de Projets Data

### 4.1 Panorama des projets data

| Type de projet | Description | Complexite | Duree typique |
|---------------|-------------|:----------:|:-------------:|
| **Pipeline ETL/ELT** | Extraire, transformer et charger des donnees d'une source a une destination | Moyenne | 4-8 semaines |
| **Data Warehouse** | Construire un entrepot de donnees centralise pour l'analyse | Elevee | 3-6 mois |
| **Dashboard / Reporting** | Creer des tableaux de bord pour le suivi d'indicateurs metier | Faible a moyenne | 2-6 semaines |
| **Modele ML** | Developper et deployer un modele d'apprentissage automatique | Elevee | 2-6 mois |
| **Data Lake** | Mettre en place un lac de donnees pour centraliser les donnees brutes | Elevee | 3-6 mois |
| **Data Catalog** | Creer un catalogue de donnees pour la gouvernance et la decouverte | Moyenne | 2-4 mois |
| **Migration de donnees** | Migrer des donnees d'un systeme legacy vers un systeme moderne | Elevee | 2-6 mois |
| **Data Quality** | Mettre en place un framework de qualite de donnees | Moyenne | 1-3 mois |

### 4.2 Exemple : Pipeline ETL pour un e-commerce

```
Sources                    Transformation              Destination
┌─────────────┐           ┌──────────────────┐        ┌──────────────┐
│ PostgreSQL   │──────────>│                  │        │              │
│ (commandes)  │           │  Airflow + dbt   │───────>│  Snowflake   │
└─────────────┘           │                  │        │  (DWH)       │
┌─────────────┐           │  - Nettoyage     │        └──────────────┘
│ API Stripe   │──────────>│  - Jointures     │               │
│ (paiements)  │           │  - Agregations   │               │
└─────────────┘           │  - Tests qualite │        ┌──────────────┐
┌─────────────┐           │                  │        │  Power BI    │
│ S3 Bucket    │──────────>│                  │───────>│  (Dashboard) │
│ (logs web)   │           └──────────────────┘        └──────────────┘
└─────────────┘
```

---

## 5. Les Ecueils Courants d'un Projet Data

### 5.1 Les 8 erreurs les plus frequentes

#### ❌ Erreur 1 : Demarrer sans audit de donnees

**Symptome** : L'equipe commence a coder un pipeline sans avoir verifie que les donnees sont disponibles, accessibles et de qualite suffisante.

**Consequence** : Decouverte en cours de developpement que 30% des donnees sont manquantes ou inexploitables. Retard de plusieurs semaines.

✅ **Solution** : Toujours commencer par un audit de donnees de 1-2 semaines. Verifier : disponibilite, qualite, volume, format, droits d'acces.

#### ❌ Erreur 2 : Pas d'alignement metier

**Symptome** : L'equipe technique construit une solution techniquement elegante mais qui ne repond pas au besoin reel du metier.

**Consequence** : Le dashboard est livre mais personne ne l'utilise. Le modele ML fait des predictions que personne ne comprend.

✅ **Solution** : Impliquer les equipes metier des le cadrage et a chaque sprint review. Valider les User Stories avec des criteres d'acceptation metier.

#### ❌ Erreur 3 : Sur-ingenierie (Over-engineering)

**Symptome** : Mettre en place un data lake avec Apache Kafka, Spark Streaming et Kubernetes pour traiter 100 lignes de CSV par jour.

**Consequence** : Couts d'infrastructure et de maintenance disproportionnes par rapport a la valeur creee.

✅ **Solution** : Commencer simple. Un script Python avec cron peut suffire. Evoluer vers une architecture plus complexe uniquement quand le besoin le justifie.

#### ❌ Erreur 4 : Ignorer la gouvernance des donnees

**Symptome** : Pas de catalogue de donnees, pas de lineage, pas de politique de retention. Personne ne sait d'ou viennent les donnees ni qui en est responsable.

**Consequence** : Incidents RGPD, duplications, incoherences entre les rapports, perte de confiance des utilisateurs.

✅ **Solution** : Definir un owner pour chaque jeu de donnees. Documenter le lineage. Mettre en place un catalogue (meme simple avec un fichier Markdown au debut).

#### ❌ Erreur 5 : Pas de tests de qualite de donnees

**Symptome** : Le pipeline tourne mais personne ne verifie que les donnees en sortie sont correctes.

**Consequence** : Des decisions metier basees sur des donnees erronees. Decouverte du probleme des semaines apres.

✅ **Solution** : Implementer des tests de qualite (Great Expectations, dbt tests) : nullite, unicite, coherence referentielle, plages de valeurs.

#### ❌ Erreur 6 : Negliger la phase de maintenance

**Symptome** : Le projet est "fini" une fois deploye. Pas de monitoring, pas d'alertes, pas de plan de maintenance.

**Consequence** : Le pipeline tombe en panne un vendredi soir. Les schemas evoluent et cassent les transformations. Les modeles derivent.

✅ **Solution** : Prevoir 20-30% du budget pour la maintenance. Mettre en place un monitoring des le deploiement.

#### ❌ Erreur 7 : Sous-estimer la complexite de l'integration

**Symptome** : "C'est facile, on n'a qu'a connecter l'API et recuperer les donnees."

**Consequence** : L'API a des rate limits, la pagination est mal documentee, les formats changent sans preavis, l'authentification expire.

✅ **Solution** : Faire un POC d'integration pour chaque source avant de s'engager sur un planning.

#### ❌ Erreur 8 : Documentation absente ou obsolete

**Symptome** : Le Data Engineer qui a construit le pipeline quitte l'equipe. Personne ne sait comment ca marche.

**Consequence** : Impossible de maintenir ou faire evoluer la solution. Il faut tout reconstruire.

✅ **Solution** : Documenter au fil de l'eau (pas a la fin). Utiliser le principe "Docs as Code" : documentation dans le meme repo que le code, revue en meme temps que le code.

### 5.2 Checklist de demarrage d'un projet data

Avant de demarrer un projet data, verifiez que vous avez :

- [ ] Identifie le sponsor et les parties prenantes metier
- [ ] Realise un audit preliminaire des donnees
- [ ] Defini des objectifs SMART
- [ ] Redige des User Stories avec des criteres d'acceptation
- [ ] Evalue la faisabilite technique (donnees, stack, competences)
- [ ] Evalue la faisabilite financiere (TCO, ROI)
- [ ] Obtenu la validation RGPD du DPO si donnees personnelles
- [ ] Defini l'architecture cible et la stack technique
- [ ] Constitue l'equipe avec les competences necessaires
- [ ] Planifie les premiers sprints

---

## 6. Synthese

### Ce qu'il faut retenir

| Concept | Point cle |
|---------|-----------|
| Specificite data | L'incertitude sur les donnees est la difference majeure avec un projet logiciel |
| Cycle de vie | 6 phases : Cadrage -> Exploration -> Dev -> Deploy -> Maintenance -> Evolution |
| Roles | Le Data Engineer est au coeur, mais le PO et le DPO sont essentiels |
| RACI | Un seul Accountable par activite, toujours |
| Ecueils | Le plus frequent : demarrer sans audit de donnees |

### Les 3 regles d'or

1. **Toujours auditer les donnees avant de coder** - C'est la phase la plus rentable du projet
2. **Aligner le technique et le metier en continu** - Pas seulement au debut du projet
3. **Commencer simple, complexifier si necessaire** - Eviter le sur-engineering

---

📝 **Exercice rapide** : Identifiez un projet data dans votre contexte professionnel ou de formation. Classez-le dans l'un des 8 types de projets data decrits dans cette lecon. Quels roles seraient necessaires ? Quels ecueils risqueriez-vous de rencontrer ?

---

[🏠 Accueil](README.md) | [Suivant →](02-cadrage-expression-besoins.md)

---

**Academy** - Formation Data Engineer
