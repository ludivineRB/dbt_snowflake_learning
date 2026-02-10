[← Precedent](03-methodes-agiles.md) | [🏠 Accueil](README.md) | [Suivant →](05-faisabilite-technique-financiere.md)

# Lecon 4 - Objectifs SMART et Priorisation RICE

## 🎯 Objectifs

- Maitriser la methode SMART pour definir des objectifs data mesurables
- Appliquer le framework RICE pour prioriser les projets et fonctionnalites
- Comprendre la methode MoSCoW comme complement
- Combiner SMART + RICE dans une roadmap de projet data

---

## 1. Objectifs SMART

### 1.1 Qu'est-ce que la methode SMART ?

La methode SMART est un cadre pour formuler des objectifs **clairs, mesurables et atteignables**. Chaque objectif doit repondre aux 5 criteres suivants :

| Lettre | Critere | Question a se poser |
|:------:|---------|-------------------|
| **S** | Specifique | L'objectif est-il precis et sans ambiguite ? |
| **M** | Mesurable | Peut-on mesurer l'atteinte de l'objectif avec un chiffre ou un KPI ? |
| **A** | Atteignable | L'objectif est-il realiste avec les ressources disponibles ? |
| **R** | Realiste (Relevant) | L'objectif est-il aligne avec les objectifs strategiques de l'entreprise ? |
| **T** | Temporellement defini | Y a-t-il une date limite claire ? |

### 1.2 Appliquer SMART a chaque lettre

#### S - Specifique

Un objectif specifique repond aux questions : **Quoi ? Qui ? Ou ? Comment ?**

❌ **Mauvais** : "Ameliorer la qualite des donnees"

**Pourquoi c'est mauvais** : Quelles donnees ? Quelle dimension de la qualite ? Pour qui ?

✅ **Bon** : "Reduire le taux de valeurs nulles dans la colonne `email` de la table `customers` de la base de production"

#### M - Mesurable

Un objectif mesurable contient un **KPI** et une **valeur cible**.

❌ **Mauvais** : "Reduire le taux de valeurs nulles"

**Pourquoi c'est mauvais** : De combien ? Comment sait-on que c'est atteint ?

✅ **Bon** : "Reduire le taux de valeurs nulles de 12% a moins de 1%"

#### A - Atteignable

Un objectif atteignable est **realiste** compte tenu des ressources (equipe, budget, temps, technologie).

❌ **Mauvais** : "Construire un data lakehouse complet avec ML en temps reel en 2 semaines avec 1 Data Engineer"

✅ **Bon** : "Construire le pipeline d'ingestion des 3 sources principales en 6 semaines avec 2 Data Engineers"

#### R - Realiste (Relevant)

L'objectif doit etre **aligne avec la strategie** de l'entreprise. Poser la question : "Pourquoi cet objectif est-il important pour le business ?"

❌ **Mauvais** : "Migrer de MySQL vers PostgreSQL" (si aucun probleme de performance actuel)

✅ **Bon** : "Migrer vers PostgreSQL pour supporter la montee en charge prevue de 300% du volume de commandes d'ici Q4"

#### T - Temporellement defini

Un objectif doit avoir une **date limite** ou une **echeance par etape** (milestone).

❌ **Mauvais** : "Reduire les valeurs nulles a moins de 1%"

✅ **Bon** : "Reduire les valeurs nulles a moins de 1% d'ici le 31 mars 2026"

### 1.3 Exemples complets d'objectifs SMART pour des projets data

#### Exemple 1 : Performance de pipeline

❌ **Mauvais** : "Le pipeline doit etre plus rapide"

✅ **SMART** : "Reduire le temps d'execution du pipeline ETL quotidien de 4h30 a moins de 1h30 d'ici le 15 avril 2026, en optimisant les transformations dbt et en passant a un cluster Spark de taille M."

| Critere | Verification |
|---------|-------------|
| Specifique | Pipeline ETL quotidien, optimisation dbt + Spark |
| Mesurable | De 4h30 a < 1h30 |
| Atteignable | Optimisation dbt + scale-up Spark (pas de refonte totale) |
| Realiste | Le pipeline est le goulot d'etranglement du reporting matinal |
| Temporel | 15 avril 2026 |

#### Exemple 2 : Qualite de donnees

❌ **Mauvais** : "Ameliorer la qualite des donnees clients"

✅ **SMART** : "Atteindre un taux de completude de 99% sur les 5 colonnes obligatoires de la table `customers` (nom, prenom, email, telephone, date_naissance) d'ici fin Q1 2026, en implementant des controles de saisie dans le CRM et des tests Great Expectations dans le pipeline."

#### Exemple 3 : Precision d'un modele ML

❌ **Mauvais** : "Le modele de churn doit etre meilleur"

✅ **SMART** : "Ameliorer le recall du modele de prediction de churn de 0.65 a 0.80 sur le jeu de test, d'ici le 30 juin 2026, en ajoutant 10 nouvelles features comportementales et en testant au moins 3 algorithmes differents (XGBoost, LightGBM, Neural Net)."

#### Exemple 4 : Adoption d'un dashboard

❌ **Mauvais** : "Les gens doivent utiliser le dashboard"

✅ **SMART** : "Atteindre 50 utilisateurs actifs hebdomadaires sur le dashboard de ventes (contre 12 aujourd'hui) d'ici le 30 septembre 2026, en formant les 80 commerciaux, en ajoutant les 3 KPIs les plus demandes, et en envoyant un rapport automatique hebdomadaire par email."

#### Exemple 5 : Reduction des couts

❌ **Mauvais** : "Reduire les couts cloud"

✅ **SMART** : "Reduire la facture mensuelle Snowflake de 15 000EUR a moins de 9 000EUR d'ici le 31 decembre 2025, en optimisant les requetes (elimination des full scans), en implementant l'auto-suspend des warehouses, et en archivant les donnees de plus de 2 ans vers S3 Glacier."

### 1.4 Exercice de reformulation

| # | ❌ Objectif flou | ✅ Objectif SMART |
|---|-----------------|-------------------|
| 1 | "Mettre en place un data lake" | "Deployer un data lake S3 + Delta Lake capable d'ingerer les 5 sources principales (CRM, ERP, Web Analytics, Support, Facturation) avec un rafraichissement quotidien, d'ici le 30 juin 2026" |
| 2 | "Automatiser les rapports" | "Automatiser les 3 rapports mensuels du service financier (P&L, tresorerie, budget) via Airflow + dbt, reduisant le temps de production de 3 jours a 2 heures, d'ici fin Q2 2026" |
| 3 | "Faire du machine learning" | "Deployer un modele de recommendation produit atteignant un taux de clic de 5% (contre 2% actuellement) sur la page d'accueil du site e-commerce, d'ici le 31 mars 2026" |

---

## 2. Framework RICE

### 2.1 Qu'est-ce que RICE ?

RICE est un framework de **priorisation** developpe par Intercom. Il permet de comparer objectivement des projets ou fonctionnalites en leur attribuant un **score numerique**.

### 2.2 Les 4 composantes

#### R - Reach (Portee)

**Question** : Combien d'utilisateurs ou de processus sont impactes par cette fonctionnalite sur une periode donnee ?

| Exemples | Reach |
|----------|:-----:|
| Nouvelle colonne dans un rapport utilise par 5 analystes | 5 |
| Pipeline alimentant un dashboard utilise par 200 commerciaux | 200 |
| API de donnees consommee par 3 applications internes | 3 (applications) ou 1500 (utilisateurs finaux) |
| Migration de base de donnees impactant toute l'entreprise | 500 |

💡 **Astuce** : Definissez une **unite de mesure** commune pour le Reach (utilisateurs par trimestre, processus impactes, etc.) et gardez-la constante pour toutes les comparaisons.

#### I - Impact (Impact)

**Question** : Quel est l'impact sur chaque utilisateur/processus atteint ?

L'impact est evalue sur une **echelle predeterminee** :

| Score | Niveau | Description |
|:-----:|--------|------------|
| 3 | Massif | Change fondamentalement la facon de travailler |
| 2 | Eleve | Amelioration significative, gain de temps majeur |
| 1 | Moyen | Amelioration notable mais non transformative |
| 0.5 | Faible | Amelioration mineure, confort |
| 0.25 | Minimal | Presque pas d'impact perceptible |

#### C - Confidence (Confiance)

**Question** : A quel point sommes-nous surs de nos estimations de Reach et Impact ?

| Score | Niveau | Situation |
|:-----:|--------|----------|
| 100% | Haute | Donnees solides, benchmark, feedback utilisateur confirme |
| 80% | Moyenne | Estimation basee sur l'experience, quelques donnees |
| 50% | Faible | Intuition, peu de donnees, beaucoup d'inconnues |

💡 **Astuce** : La Confidence est le critere le plus souvent neglige. C'est pourtant le plus utile : il **penalise les projets dont on ne sait pas grand-chose** et favorise ceux que l'on comprend bien.

#### E - Effort (Effort)

**Question** : Combien de temps-personne ce projet necessite-t-il ?

L'effort est exprime en **personne-semaines** ou **personne-mois**. Il inclut le developpement, les tests, la documentation et le deploiement.

| Exemples | Effort |
|----------|:------:|
| Ajouter une colonne dans un rapport existant | 0.5 personne-semaine |
| Nouveau pipeline ETL pour une source | 2 personne-semaines |
| Data Warehouse complet (modelisation + pipelines + dashboards) | 20 personne-semaines |
| Modele ML de bout en bout (feature engineering -> deploiement) | 12 personne-semaines |

### 2.3 La Formule RICE

```
                 Reach  x  Impact  x  Confidence
RICE Score  =  ──────────────────────────────────
                          Effort
```

**Plus le score est eleve, plus la priorite est haute.**

### 2.4 Exemple Complet : Prioriser 5 Projets Data

#### Contexte
Une entreprise e-commerce a 5 projets data candidats pour le prochain trimestre. L'equipe dispose de 2 Data Engineers et 1 Data Scientist (soit ~36 personne-semaines disponibles).

#### Evaluation

| # | Projet | Reach | Impact | Confidence | Effort (p-s) | RICE Score |
|---|--------|:-----:|:------:|:----------:|:------------:|:----------:|
| A | Pipeline temps reel des commandes | 200 utilisateurs | 3 (Massif) | 80% | 8 | **60.0** |
| B | Dashboard de suivi des stocks | 50 utilisateurs | 2 (Eleve) | 100% | 4 | **25.0** |
| C | Modele de prediction de churn | 10 000 clients | 1 (Moyen) | 50% | 12 | **416.7** |
| D | Migration du DWH vers Snowflake | 80 utilisateurs | 2 (Eleve) | 80% | 16 | **8.0** |
| E | Catalogue de donnees | 30 utilisateurs | 0.5 (Faible) | 100% | 3 | **5.0** |

#### Calcul detaille

```
Projet A : (200 x 3 x 0.80) / 8  = 480 / 8   = 60.0
Projet B : (50 x 2 x 1.00) / 4   = 100 / 4   = 25.0
Projet C : (10000 x 1 x 0.50) / 12 = 5000 / 12 = 416.7
Projet D : (80 x 2 x 0.80) / 16  = 128 / 16  = 8.0
Projet E : (30 x 0.5 x 1.00) / 3 = 15 / 3    = 5.0
```

#### Classement et recommandation

| Rang | Projet | RICE Score | Decision |
|:----:|--------|:----------:|----------|
| 1 | C - Modele de prediction de churn | 416.7 | **Priorite 1** - Mais attention : confidence a 50%. Faire un spike de 2 semaines d'abord. |
| 2 | A - Pipeline temps reel | 60.0 | **Priorite 2** - Haute confiance, fort impact |
| 3 | B - Dashboard stocks | 25.0 | **Priorite 3** - Rapide a livrer (4 semaines), bonne confiance |
| 4 | D - Migration DWH | 8.0 | **Report au trimestre suivant** - Effort important, impact differe |
| 5 | E - Catalogue de donnees | 5.0 | **Report** - Important mais impact faible a court terme |

💡 **Astuce** : Le projet C a le score le plus eleve grace a son Reach enorme (10 000 clients), mais sa confiance est basse (50%). La bonne strategie est de commencer par un **Spike Sprint** de 2 semaines pour valider la faisabilite avant de s'engager sur les 12 semaines completes.

### 2.5 Limites du framework RICE

| Limite | Mitigation |
|--------|-----------|
| Le Reach peut etre manipule en changeant l'unite de mesure | Definir une convention fixe pour toute l'equipe |
| L'Impact est subjectif | Utiliser des criteres objectifs quand possible (temps gagne, erreurs evitees) |
| La Confidence est souvent surestimee | Etre honnete. Quand on doute, mettre 50% |
| Ne prend pas en compte les dependances | Ajouter une colonne "Dependances" au tableau |
| Ne prend pas en compte l'urgence | Combiner avec MoSCoW pour les elements urgents |

---

## 3. Methode MoSCoW

### 3.1 Les 4 categories

| Categorie | Definition | Repartition cible |
|-----------|-----------|:-----------------:|
| **Must have** | Indispensable. Sans ca, le projet n'a pas de sens. | ~60% de l'effort |
| **Should have** | Important. Apporte beaucoup de valeur mais on peut vivre sans temporairement. | ~20% de l'effort |
| **Could have** | Souhaitable. Ameliore l'experience mais n'est pas bloquant. | ~15% de l'effort |
| **Won't have** (this time) | Hors perimetre pour cette version. Sera reconsidere plus tard. | ~5% (documentation) |

### 3.2 Exemple : Dashboard de ventes

| Fonctionnalite | Categorie | Justification |
|---------------|-----------|--------------|
| Affichage du CA en temps reel | **Must** | Besoin principal du sponsor |
| Filtres par region et produit | **Must** | Besoin exprime par tous les utilisateurs |
| Comparaison N-1 | **Must** | Indispensable pour l'analyse |
| Export CSV/Excel | **Should** | Demande par 80% des utilisateurs mais workaround possible |
| Alertes automatiques par email | **Should** | Utile mais peut etre fait manuellement au debut |
| Vue cartographique des ventes | **Could** | Joli mais pas indispensable |
| Prediction des ventes (ML) | **Won't** | Trop complexe pour la v1, prevu en v2 |

💡 **Astuce** : La categorie "Won't have" ne signifie pas "jamais". Elle signifie "pas cette fois-ci". Documenter les "Won't have" est important pour ne pas les oublier et les reconsiderer dans les versions suivantes.

---

## 4. Combiner SMART + RICE dans une Roadmap Data

### 4.1 Le processus en 4 etapes

```
Etape 1              Etape 2              Etape 3              Etape 4
IDENTIFIER            PRIORISER            PLANIFIER            MESURER
les objectifs         avec RICE            la roadmap           avec SMART
│                     │                    │                    │
│ Lister tous les     │ Scorer chaque      │ Placer les         │ Definir des
│ projets/features    │ projet avec        │ projets dans       │ objectifs SMART
│ candidats           │ RICE + MoSCoW      │ le calendrier      │ pour chaque
│                     │                    │ trimestriel        │ projet retenu
▼                     ▼                    ▼                    ▼
```

### 4.2 Template de Roadmap Trimestrielle

| Trimestre | Projet | RICE | Categorie | Objectif SMART | Equipe |
|-----------|--------|:----:|:---------:|---------------|--------|
| Q1 2026 | Modele de churn (Spike) | 417 | Must | Valider la faisabilite du modele (recall > 0.60 sur donnees test) en 2 semaines | DS + DE1 |
| Q1 2026 | Pipeline temps reel | 60 | Must | Pipeline en production avec latence < 15 min d'ici le 31 mars | DE1 + DE2 |
| Q1 2026 | Dashboard stocks | 25 | Should | 50 utilisateurs actifs hebdomadaires d'ici fin mars | DA |
| Q2 2026 | Modele de churn (Dev) | 417 | Must | Recall > 0.80 en production d'ici le 30 juin | DS + DE1 |
| Q2 2026 | Migration DWH | 8 | Should | Migration des 10 tables principales d'ici le 30 juin | DE1 + DE2 |
| Q3 2026 | Catalogue de donnees | 5 | Could | 100% des tables du DWH documentees d'ici le 30 sept | DA + DE2 |

### 4.3 Communication de la roadmap

La roadmap doit etre presentee differemment selon l'audience :

| Audience | Format | Contenu |
|----------|--------|---------|
| Direction / Sponsor | 1 slide PowerPoint | 3-5 projets majeurs, impact business, timeline |
| Product Owner / Metier | Tableau detaille | Tous les projets, priorite, objectifs SMART, echeanges |
| Equipe technique | Board Jira/GitHub | Epics, stories, estimation, sprint planning |

---

## 5. Synthese

| Concept | Point cle |
|---------|-----------|
| SMART | 5 criteres pour des objectifs clairs : Specifique, Mesurable, Atteignable, Realiste, Temporel |
| RICE | Score = (Reach x Impact x Confidence) / Effort |
| MoSCoW | Must / Should / Could / Won't pour categoriser les fonctionnalites |
| Combinaison | RICE pour prioriser, SMART pour definir les objectifs de chaque projet retenu |
| Roadmap | Planification trimestrielle combinant priorisation et objectifs mesurables |

### Les 3 regles d'or

1. **Un objectif non mesurable n'est pas un objectif** - Si vous ne pouvez pas le chiffrer, reformulez-le
2. **Priorisez par les donnees, pas par le HiPPO** (Highest Paid Person's Opinion) - RICE objectivise la decision
3. **Revisez la priorisation regulierement** - Tous les trimestres, les Reach, Impact et Confidence evoluent

---

📝 **Exercice** : Vous avez 4 projets data candidats pour le prochain trimestre. Definissez un objectif SMART pour chacun, estimez leur score RICE, et proposez un ordre de realisation.

---

[← Precedent](03-methodes-agiles.md) | [🏠 Accueil](README.md) | [Suivant →](05-faisabilite-technique-financiere.md)

---

**Academy** - Formation Data Engineer
