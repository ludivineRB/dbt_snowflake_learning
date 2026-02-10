[← Precedent](02-cadrage-expression-besoins.md) | [🏠 Accueil](README.md) | [Suivant →](04-objectifs-smart-priorisation-rice.md)

# Lecon 3 - Methodes Agiles pour les Projets Data

## 🎯 Objectifs

- Comprendre pourquoi les methodes agiles sont adaptees aux projets data
- Maitriser le framework Scrum et son adaptation au contexte data
- Savoir utiliser Kanban pour les activites de maintenance et support
- Connaitre les principaux outils de gestion de projet agile
- Savoir choisir entre Scrum et Kanban selon le contexte

---

## 1. Pourquoi l'Agile pour les Projets Data ?

### 1.1 Les limites du cycle en V pour la data

Le cycle en V (ou Waterfall) suppose que l'on peut **definir tous les besoins en amont**, puis les developper, puis les tester. Cette approche fonctionne mal pour les projets data car :

| Probleme | Explication |
|----------|------------|
| **Incertitude sur les donnees** | On ne sait pas ce qu'on va trouver dans les donnees avant de les explorer |
| **Besoins evolutifs** | Le metier decouvre de nouveaux besoins en voyant les premiers resultats |
| **Experimentation necessaire** | Un modele ML necessite des iterations : features, algorithmes, hyperparametres |
| **Feedback rapide** | Un dashboard doit etre valide visuellement par les utilisateurs tres tot |
| **Risque technique** | L'integration avec des sources externes peut reveler des problemes imprevus |

### 1.2 Les 4 valeurs Agile appliquees a la data

| Valeur Agile | Application Data |
|--------------|-----------------|
| **Individus et interactions** > processus et outils | Les echanges Data Engineer / Metier sont plus importants que la documentation exhaustive |
| **Solution fonctionnelle** > documentation exhaustive | Un pipeline qui tourne et produit des donnees fiables > un DAT de 100 pages |
| **Collaboration avec le client** > negociation contractuelle | Revue de sprint avec le metier toutes les 2 semaines |
| **Adaptation au changement** > suivi d'un plan | Les schemas de donnees changent, les besoins evoluent, il faut s'adapter |

### 1.3 Le concept de "Data Sprint"

Un Data Sprint est une adaptation du sprint classique qui integre les specificites de la data :

```
SPRINT CLASSIQUE              DATA SPRINT
================              ===========
Planning                      Planning + Revue des sources de donnees
Developpement                 Exploration / Developpement
Tests                         Tests fonctionnels + Tests de qualite donnees
Review                        Review + Demo sur donnees reelles
Retro                         Retro + Bilan qualite donnees
```

💡 **Astuce** : Prevoyez des **Spike Sprints** (sprints d'exploration) en debut de projet. Un Spike Sprint est un sprint dedie a l'exploration et au prototypage, sans engagement de livraison fonctionnelle. Il sert a reduire l'incertitude.

---

## 2. Scrum pour les Projets Data

### 2.1 Les 3 Roles Scrum

#### Product Owner (PO)

| Aspect | Description |
|--------|------------|
| **Qui** | Responsable metier ou Data Product Manager |
| **Responsabilites** | Definir et prioriser le backlog, rediger les User Stories, valider les livraisons |
| **Specificite data** | Doit comprendre suffisamment la data pour valider la qualite des donnees, pas seulement les fonctionnalites |
| **Erreur courante** | Un PO qui ne regarde que le dashboard final sans verifier que les donnees sous-jacentes sont fiables |

#### Scrum Master

| Aspect | Description |
|--------|------------|
| **Qui** | Facilitateur (peut etre un membre de l'equipe en rotation) |
| **Responsabilites** | Faciliter les ceremonies, lever les blocages, proteger l'equipe |
| **Specificite data** | Doit comprendre que les blocages data (acces aux sources, qualite) sont souvent les plus critiques |
| **Erreur courante** | Ignorer les blocages d'acces aux donnees car "c'est technique" |

#### Equipe de Developpement

| Aspect | Description |
|--------|------------|
| **Qui** | Data Engineers, Data Scientists, Data Analysts (3-9 personnes) |
| **Responsabilites** | Estimer, developper, tester, deployer |
| **Specificite data** | Equipe pluridisciplinaire : les competences data engineering, data science et analyse sont complementaires |
| **Erreur courante** | Separer les Data Engineers et Data Scientists dans des equipes differentes |

### 2.2 Les 5 Ceremonies Scrum

#### Sprint Planning (Planification de Sprint)

| Element | Detail |
|---------|--------|
| **Duree** | 2-4 heures pour un sprint de 2 semaines |
| **Participants** | PO + Equipe + Scrum Master |
| **Objectif** | Definir le Sprint Goal et selectionner les stories du sprint |
| **Adaptation data** | Inclure l'estimation de la complexite des donnees, pas seulement du code |

**Deroulement** :
1. Le PO presente les stories prioritaires du backlog
2. L'equipe discute et clarifie chaque story
3. L'equipe estime l'effort (points de complexite ou t-shirt sizing)
4. L'equipe s'engage sur un ensemble de stories (Sprint Backlog)
5. Le Sprint Goal est formule

**Points de vigilance pour la data** :
- Estimer le temps d'acces aux donnees (permissions, API keys, VPN)
- Prevoir du temps pour les tests de qualite de donnees
- Identifier les dependances avec d'autres equipes (DevOps, DBA, Securite)

#### Daily Standup (Melee Quotidienne)

| Element | Detail |
|---------|--------|
| **Duree** | 15 minutes maximum |
| **Participants** | Equipe + Scrum Master |
| **Format** | Chaque membre repond a 3 questions |

Les 3 questions :
1. **Qu'ai-je fait hier ?** (Ex : "J'ai developpe la transformation de la table clients")
2. **Que vais-je faire aujourd'hui ?** (Ex : "Je vais ecrire les tests de qualite pour cette table")
3. **Y a-t-il des blocages ?** (Ex : "J'attends toujours les credentials pour l'API Salesforce")

💡 **Astuce** : Dans les equipes data, les blocages les plus frequents sont lies a l'**acces aux donnees**. Le Scrum Master doit les escalader immediatement car ils peuvent bloquer tout le sprint.

#### Sprint Review (Revue de Sprint)

| Element | Detail |
|---------|--------|
| **Duree** | 1-2 heures |
| **Participants** | PO + Equipe + Parties prenantes metier |
| **Objectif** | Montrer ce qui a ete accompli, recueillir le feedback |

**Adaptation data** :
- Demontrer sur des **donnees reelles** (pas des donnees de test fictives)
- Montrer les **metriques de qualite** des donnees (taux de completude, coherence)
- Presenter les resultats du modele ML sur des cas concrets du metier
- Eviter les termes techniques : parler de resultats metier, pas d'architecture

#### Sprint Retrospective (Retrospective)

| Element | Detail |
|---------|--------|
| **Duree** | 1-1.5 heures |
| **Participants** | Equipe + Scrum Master (sans le PO) |
| **Objectif** | Ameliorer les processus de l'equipe |

**Format classique** : 3 colonnes

```
┌──────────────────┬──────────────────┬──────────────────┐
│   Ce qui a bien  │  Ce qui peut     │   Actions        │
│   fonctionne     │  etre ameliore   │   concretes      │
├──────────────────┼──────────────────┼──────────────────┤
│ Tests de qualite │ Acces aux        │ Demander les     │
│ catches des      │ donnees trop     │ credentials 1    │
│ bugs avant       │ lent (2j pour    │ semaine avant    │
│ la review        │ obtenir les      │ le sprint        │
│                  │ credentials)     │                  │
├──────────────────┼──────────────────┼──────────────────┤
│ Bonne collab     │ Documentation    │ Integrer la      │
│ avec l'equipe    │ pas a jour       │ doc dans la DoD  │
│ metier           │                  │ de chaque story  │
├──────────────────┼──────────────────┼──────────────────┤
│ CI/CD pipeline   │ Pas assez de     │ Ajouter des      │
│ stable           │ tests sur les    │ tests dbt dans   │
│                  │ donnees          │ le pipeline CI   │
└──────────────────┴──────────────────┴──────────────────┘
```

#### Refinement (Affinage du Backlog)

| Element | Detail |
|---------|--------|
| **Duree** | 1 heure par semaine |
| **Participants** | PO + Equipe (ou sous-groupe) |
| **Objectif** | Clarifier et estimer les stories futures |

**Specificite data** : Le refinement est crucial pour identifier en avance les **besoins d'acces aux donnees** et les **risques de qualite**. Cela permet de debloquer les pre-requis avant le sprint.

### 2.3 Les 3 Artefacts Scrum

#### Product Backlog

Liste priorisee de toutes les fonctionnalites du produit data. Chaque element est une User Story.

**Exemple de Product Backlog pour un projet de Data Warehouse** :

| Priorite | Epic | User Story | Points |
|:--------:|------|-----------|:------:|
| 1 | Ingestion | Pipeline d'ingestion des donnees de ventes depuis PostgreSQL | 8 |
| 2 | Ingestion | Pipeline d'ingestion des donnees clients depuis le CRM | 5 |
| 3 | Transformation | Modele dimensional des ventes (fait + dimensions) | 13 |
| 4 | Qualite | Tests de qualite sur les donnees de ventes | 5 |
| 5 | Dashboard | Dashboard CA par region et par produit | 8 |
| 6 | Ingestion | Pipeline d'ingestion des donnees de stocks depuis l'ERP | 8 |
| 7 | Transformation | Modele dimensional des stocks | 8 |
| 8 | Alerting | Alertes en cas d'anomalie sur les donnees | 3 |

#### Sprint Backlog

Sous-ensemble du Product Backlog selectionne pour le sprint en cours, avec les taches techniques associees.

#### Increment

La somme de tous les elements du Product Backlog termines pendant le sprint et les sprints precedents. Chaque increment doit etre **potentiellement livrable**.

### 2.4 Duree de Sprint recommandee

| Duree | Quand l'utiliser |
|:-----:|-----------------|
| **1 semaine** | Phase d'exploration / POC : iterations rapides pour valider les hypotheses |
| **2 semaines** | Phase de developpement : standard recommande pour les projets data |
| **3 semaines** | Projets avec forte dependance externe : permet d'absorber les delais d'acces |
| **4 semaines** | Rarement recommande : trop long pour le feedback |

💡 **Astuce** : Commencez par des sprints de 2 semaines. Ajustez si necessaire apres 3-4 sprints en fonction des retros.

---

## 3. Kanban pour les Projets Data

### 3.1 Quand utiliser Kanban ?

Kanban est preferable a Scrum dans les situations suivantes :

| Situation | Pourquoi Kanban |
|-----------|----------------|
| **Maintenance de pipelines** | Les incidents arrivent de maniere imprevue, pas dans des sprints |
| **Support data** | Les demandes metier ad-hoc ne se planifient pas |
| **Flux continu** | Les nouvelles sources de donnees arrivent regulierement |
| **Petite equipe (1-2 personnes)** | Scrum est trop ceremonieux pour une personne seule |
| **Activites operationnelles** | Monitoring, correction de drift, mise a jour de modeles |

### 3.2 Structure du Board Kanban

```
┌────────────┬──────────────┬────────────┬───────────┬──────────┐
│  BACKLOG   │  A FAIRE     │ EN COURS   │  REVUE    │   DONE   │
│            │  (To Do)     │ (In Prog.) │ (Review)  │          │
│  (illimite)│  (max 5)     │  (max 3)   │ (max 2)   │          │
├────────────┼──────────────┼────────────┼───────────┼──────────┤
│            │              │            │           │          │
│ Ajouter    │ Corriger le  │ Pipeline   │ Tests de  │ Pipeline │
│ source     │ mapping des  │ ingestion  │ qualite   │ clients  │
│ MongoDB    │ dates dans   │ factures   │ sur table │ deploye  │
│            │ table        │            │ ventes    │          │
│ Optimiser  │ produits     │ Debug      │           │ Dashboard│
│ requete    │              │ alerte     │           │ CA v2    │
│ rapport    │ Mettre a     │ faux       │           │ livre    │
│ mensuel    │ jour la doc  │ positif    │           │          │
│            │ du pipeline  │            │           │          │
│ ...        │ ventes       │            │           │          │
│            │              │            │           │          │
└────────────┴──────────────┴────────────┴───────────┴──────────┘
                  WIP: 5        WIP: 3      WIP: 2
```

### 3.3 WIP Limits (Limites de Travail en Cours)

Les WIP limits (Work In Progress) sont la **regle la plus importante** du Kanban. Elles limitent le nombre d'elements dans chaque colonne.

**Pourquoi c'est essentiel** :
- Evite le multi-tache (le multi-tache reduit la productivite de 20-40%)
- Force a terminer avant de commencer quelque chose de nouveau
- Revele les goulots d'etranglement (si une colonne est toujours pleine)
- Ameliore le temps de cycle (temps entre le debut et la fin d'une tache)

**Regle de base** : WIP limit = nombre de personnes dans l'equipe pour cette etape (+ 1 pour le buffer).

### 3.4 Metriques Kanban

| Metrique | Definition | Objectif |
|----------|-----------|---------|
| **Lead Time** | Temps total entre la demande et la livraison | Reduire (ideal < 1 semaine) |
| **Cycle Time** | Temps entre le debut du travail et la livraison | Reduire (ideal < 3 jours) |
| **Throughput** | Nombre d'elements livres par semaine | Stabiliser et augmenter |
| **WIP** | Nombre d'elements en cours a un instant T | Maintenir sous la limite |

---

## 4. Outils de Gestion de Projet Agile

### 4.1 Comparaison des outils

| Outil | Type | Points forts | Limites | Prix |
|-------|------|-------------|---------|------|
| **Jira** | Complet | Scrum + Kanban, epics, sprints, reporting avance, integrations | Complexe a configurer, courbe d'apprentissage | Gratuit (10 users) puis ~7$/user/mois |
| **Trello** | Simple | Kanban visuel, intuitif, prise en main rapide | Limite pour Scrum pur, pas de sprints natifs | Gratuit puis ~5$/user/mois |
| **GitHub Projects** | Integre | Integre au code, issues et PRs, automatisations | Moins riche que Jira en reporting | Gratuit avec GitHub |
| **Azure DevOps Boards** | Complet | Scrum + Kanban, integre a Azure, CI/CD | Ecosysteme Microsoft, moins flexible | Gratuit (5 users) puis ~6$/user/mois |
| **Linear** | Moderne | UX moderne, rapide, cycle tracking | Moins d'integrations, recent | A partir de 8$/user/mois |
| **Notion** | Flexible | Tout-en-un (docs + boards + bases), flexible | Pas optimise pour Scrum pur | Gratuit puis ~8$/user/mois |

### 4.2 Jira - Configuration pour un projet data

**Structure recommandee** :

```
PROJET DATA WAREHOUSE
│
├── Epic: Ingestion des donnees
│   ├── Story: Pipeline PostgreSQL -> Staging
│   ├── Story: Pipeline CRM -> Staging
│   └── Story: Pipeline ERP -> Staging
│
├── Epic: Transformation et modelisation
│   ├── Story: Modele dimensional ventes
│   ├── Story: Modele dimensional clients
│   └── Story: Tests de qualite dbt
│
├── Epic: Restitution / Dashboard
│   ├── Story: Dashboard CA
│   ├── Story: Dashboard Stocks
│   └── Story: Export CSV/Excel
│
├── Epic: Monitoring et Alerting
│   ├── Story: Alertes qualite donnees
│   └── Story: Dashboard de monitoring pipeline
│
└── Epic: Documentation
    ├── Story: DAT
    ├── Story: Dictionnaire de donnees
    └── Story: Guide utilisateur dashboard
```

### 4.3 GitHub Projects - Ideal pour les equipes data

GitHub Projects est particulierement adapte aux equipes data car il permet de lier directement les issues aux Pull Requests et au code.

**Workflow recommande** :
1. Creer une issue pour chaque User Story
2. Creer une branche depuis l'issue (`feature/pipeline-ventes`)
3. Developper et ouvrir une PR
4. Code review + validation des tests de qualite
5. Merge et deplacement automatique de l'issue vers "Done"

---

## 5. Comparaison Scrum vs Kanban pour les Projets Data

### 5.1 Tableau comparatif

| Critere | Scrum | Kanban |
|---------|-------|--------|
| **Cadence** | Sprints fixes (2 semaines) | Flux continu |
| **Roles** | PO, Scrum Master, Equipe | Pas de roles imposes |
| **Ceremonies** | 5 ceremonies obligatoires | Stand-up uniquement (optionnel) |
| **Planification** | Par sprint | A la demande |
| **Engagement** | Sprint Goal + stories selectionnees | Pas d'engagement formel |
| **Changement** | En principe, pas de changement en cours de sprint | Changement a tout moment |
| **Metriques** | Velocite (points/sprint) | Lead time, cycle time, throughput |
| **Board** | Reset a chaque sprint | Continu (jamais reset) |
| **WIP Limits** | Implicites (capacite du sprint) | Explicites et obligatoires |
| **Ideal pour** | Nouveau projet, phase de construction | Maintenance, support, operations |

### 5.2 Recommandation par phase de projet

| Phase du projet | Methode recommandee | Pourquoi |
|----------------|:-------------------:|---------|
| Cadrage | Ni l'un ni l'autre | Workshop + entretiens |
| Exploration / POC | Scrum (sprints courts d'1 semaine) | Iterations rapides avec feedback |
| Developpement | Scrum (sprints de 2 semaines) | Engagement et ceremonies structurees |
| Deploiement | Kanban | Flux de taches techniques a executer |
| Maintenance | Kanban | Incidents et demandes imprevisibles |
| Evolution | Scrum ou Scrumban | Depand de la taille des evolutions |

### 5.3 Scrumban : le meilleur des deux mondes ?

Scrumban combine :
- Les **ceremonies** de Scrum (Planning, Review, Retro)
- Les **WIP limits** et le flux continu de Kanban
- La **flexibilite** : pas de sprint fixe, mais des points de synchronisation reguliers

C'est souvent la methode la plus pragmatique pour les equipes data matures qui sont a la fois en construction de nouveaux pipelines et en maintenance de l'existant.

---

## 6. Cas Pratique : Organisation d'un Sprint Data

### 6.1 Contexte

Equipe de 5 personnes (2 Data Engineers, 1 Data Scientist, 1 Data Analyst, 1 PO). Sprint de 2 semaines. Projet : Data Warehouse de ventes.

### 6.2 Sprint Planning

**Sprint Goal** : "Livrer le pipeline d'ingestion des ventes et le premier draft du modele dimensional"

| Story | Responsable | Estimation | Priorite |
|-------|------------|:----------:|:--------:|
| Pipeline ingestion ventes PostgreSQL -> Staging | DE1 | 5 pts | 1 |
| Tests de qualite sur les donnees de ventes | DE2 | 3 pts | 2 |
| Modele dimensional ventes (schema + dbt) | DE1 + DE2 | 8 pts | 3 |
| EDA sur les donnees clients pour le modele ML | DS | 5 pts | 4 |
| Maquette du dashboard CA | DA | 3 pts | 5 |
| **Total** | | **24 pts** | |

**Capacite de l'equipe** : 5 personnes x 2 semaines x ~6 pts/personne = ~30 pts. On prend 24 pts (marge de 20% pour les imprevus).

### 6.3 Daily Standup - Exemple Jour 5

```
DE1: "Hier j'ai termine l'extraction PostgreSQL. Aujourd'hui je
      commence le chargement dans Staging. Pas de blocage."

DE2: "Hier j'ai ecrit 5 tests dbt sur les donnees de ventes. 2 tests
      echouent : il y a des doublons sur order_id. Aujourd'hui je
      vais investiguer la source du probleme. Blocage potentiel si
      c'est un bug dans la source."

DS:  "Hier j'ai fait l'EDA sur les donnees clients. Bonne nouvelle :
      les features sont exploitables. Mauvaise nouvelle : 15% de
      valeurs manquantes sur le revenu. Aujourd'hui je vais tester
      differentes strategies d'imputation. Pas de blocage."

DA:  "Hier j'ai termine la maquette du dashboard. Aujourd'hui je la
      presente au PO pour validation. Pas de blocage."

PO:  "Je suis disponible cet apres-midi pour la revue de maquette."
```

---

## 7. Synthese

| Concept | Point cle |
|---------|-----------|
| Agile et Data | L'incertitude sur les donnees rend l'Agile indispensable |
| Scrum | Ideal pour la phase de construction : cadre, ceremonies, engagement |
| Kanban | Ideal pour la maintenance : flux continu, WIP limits |
| Data Sprint | Sprint classique + revue des sources + tests de qualite donnees |
| Spike Sprint | Sprint d'exploration sans engagement de livraison |
| Outils | Jira (complet), GitHub Projects (integre au code), Trello (simple) |

---

📝 **Exercice** : Vous etes Scrum Master d'une equipe de 4 Data Engineers. Organisez le premier sprint d'un projet de migration de base de donnees on-premise vers le cloud. Definissez le Sprint Goal, selectionnez 4-5 stories, estimez-les, et simulez le Daily Standup du jour 3.

---

[← Precedent](02-cadrage-expression-besoins.md) | [🏠 Accueil](README.md) | [Suivant →](04-objectifs-smart-priorisation-rice.md)

---

**Academy** - Formation Data Engineer
