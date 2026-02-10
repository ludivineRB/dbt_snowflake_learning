[← Precedent](04-objectifs-smart-priorisation-rice.md) | [🏠 Accueil](README.md) | [Suivant →](06-documentation-communication.md)

# Lecon 5 - Faisabilite Technique et Financiere

## 🎯 Objectifs

- Evaluer la faisabilite technique d'un projet data (donnees, stack, competences)
- Mener un audit de donnees structure avant le lancement
- Definir et piloter un POC (Proof of Concept)
- Calculer le TCO (Total Cost of Ownership) d'une solution data
- Estimer le ROI (Return on Investment) d'un projet data
- Realiser une analyse des risques (SWOT, matrice de risques)

---

## 1. Faisabilite Technique

### 1.1 Les 4 dimensions de la faisabilite technique

Avant de lancer un projet data, 4 dimensions doivent etre evaluees :

```
┌─────────────────────────────────────────────────┐
│              FAISABILITE TECHNIQUE               │
├──────────────┬──────────────┬──────────────┬─────┤
│   DONNEES    │    STACK     │ COMPETENCES  │ POC │
│              │  TECHNIQUE   │              │     │
│ - Dispo ?    │ - Actuelle ? │ - Equipe ?   │ 2-4 │
│ - Qualite ?  │ - Cible ?    │ - Gaps ?     │ sem │
│ - Volume ?   │ - Migration? │ - Formation? │     │
│ - Format ?   │ - Cout ?     │ - Recrutement│     │
│ - Acces ?    │              │              │     │
└──────────────┴──────────────┴──────────────┴─────┘
```

### 1.2 Audit de donnees - Checklist des 10 questions

Avant de s'engager sur un projet data, il faut repondre a ces 10 questions :

| # | Question | Ce qu'on cherche | Risque si non verifie |
|---|----------|-----------------|----------------------|
| 1 | **Les donnees existent-elles ?** | Confirmer que les sources sont identifiees | Decouvrir en plein sprint que la donnee n'existe pas |
| 2 | **Sont-elles accessibles ?** | API, base de donnees, fichier, acces reseau | Blocage de semaines pour obtenir les credentials |
| 3 | **Quel est le volume ?** | Nombre de lignes, taille en Go/To, croissance | Sous-dimensionner l'infrastructure |
| 4 | **Quel est le format ?** | CSV, JSON, Parquet, XML, API REST, SOAP | Effort de parsing et transformation sous-estime |
| 5 | **Quelle est la qualite ?** | Completude, coherence, unicite, fraicheur | Decouvertes tardives de problemes de qualite |
| 6 | **Quelle est la frequence de mise a jour ?** | Temps reel, horaire, quotidien, mensuel | SLA impossible a tenir |
| 7 | **Y a-t-il des donnees sensibles ?** | Donnees personnelles (RGPD), donnees financieres | Non-conformite reglementaire |
| 8 | **Qui est le owner de la donnee ?** | Equipe/personne responsable de la source | Pas d'interlocuteur en cas de probleme |
| 9 | **Y a-t-il un schema documente ?** | Dictionnaire de donnees, documentation API | Interpretation erronee des champs |
| 10 | **La donnee est-elle historisee ?** | Profondeur d'historique disponible | Impossible de faire des analyses temporelles |

### 1.3 Rapport d'audit de donnees - Template

```
RAPPORT D'AUDIT DE DONNEES
===========================

Source : [Nom de la source]
Date d'audit : [Date]
Auditeur : [Nom]

1. IDENTIFICATION
   - Nom de la source : CRM Salesforce
   - Type : API REST
   - Owner : Equipe Commerciale (Jean Dupont)
   - Documentation : https://developer.salesforce.com/docs

2. ACCES
   - Mode d'acces : API REST avec OAuth 2.0
   - Credentials : Demande en cours (ticket JIRA-1234)
   - Restrictions : Rate limit 100 req/min, sandbox disponible
   - Reseau : Accessible depuis le VPC production

3. VOLUMETRIE
   - Volume actuel : 2.5 millions de contacts, 800 000 opportunites
   - Croissance : +50 000 contacts/mois
   - Taille estimee : ~15 Go (JSON brut)

4. QUALITE (sur un echantillon de 10 000 enregistrements)
   - Completude : email 98%, telephone 72%, adresse 65%
   - Unicite : 3% de doublons sur le champ email
   - Coherence : 5% de dates de creation > date de modification
   - Fraicheur : derniere mise a jour < 24h pour 95% des enregistrements

5. SCHEMA
   - Nombre de tables/objets : 15 principaux
   - Documentation : Complete pour les champs standard, partielle pour les champs custom
   - Champs custom : 45 champs custom ajoutes par l'equipe commerciale

6. CONTRAINTES
   - RGPD : Oui (donnees personnelles clients)
   - Retention : 5 ans (politique interne)
   - Anonymisation : Necessaire pour l'environnement de dev/test

7. VERDICT
   - [x] Source exploitable
   - [ ] Source exploitable avec reserves (preciser)
   - [ ] Source non exploitable (preciser)

   Reserves : Completude du telephone insuffisante pour le cas d'usage
   "notification SMS". Necessite un enrichissement ou un plan B.
```

### 1.4 Evaluation de la stack technique

| Dimension | Questions | Exemple de reponse |
|-----------|----------|-------------------|
| **Infra actuelle** | Que possede-t-on deja ? | AWS (S3, RDS, EC2), pas de solution d'orchestration |
| **Infra cible** | De quoi a-t-on besoin ? | + Airflow (orchestration), + dbt (transformation), + Snowflake (DWH) |
| **Gap** | Qu'est-ce qui manque ? | Airflow et Snowflake a provisionner |
| **Migration** | Faut-il migrer l'existant ? | Oui, migrer les 15 rapports SQL Server vers Snowflake |
| **Integration** | La nouvelle stack s'integre-t-elle ? | Oui, Airflow peut orchestrer dbt et Snowflake |
| **Scalabilite** | La stack tient-elle a x10 du volume ? | Snowflake oui (auto-scaling), Airflow a verifier |

### 1.5 Evaluation des competences

| Technologie requise | Niveau de l'equipe | Gap | Action |
|--------------------|--------------------|-----|--------|
| Python | Expert | Aucun | - |
| SQL | Expert | Aucun | - |
| Airflow | Intermediaire | A renforcer | Formation 2 jours |
| dbt | Debutant | Fort | Formation 3 jours + pair programming |
| Snowflake | Aucune experience | Critique | Formation 5 jours + accompagnement consultant |
| Terraform | Intermediaire | Faible | Auto-formation |

### 1.6 POC (Proof of Concept)

#### Qu'est-ce qu'un POC ?

Un POC est une **experimentation a perimetre reduit** qui vise a valider la faisabilite technique d'un projet avant de s'engager sur le developpement complet.

#### Regles du POC

| Regle | Detail |
|-------|--------|
| **Duree maximale** | 2-4 semaines (au-dela, c'est du developpement deguise) |
| **Perimetre reduit** | 1 source, 1 transformation, 1 sortie (pas tout le projet) |
| **Criteres de succes definis a l'avance** | "Le POC est reussi si..." |
| **Pas de code production** | Le code du POC est jetable. Ne pas essayer de le reutiliser. |
| **Decision binaire a la fin** | Go ou No-Go. Pas de "on continue a explorer". |

#### Template de cadrage POC

```
CADRAGE POC
===========

Nom : POC Pipeline Temps Reel Commandes
Duree : 2 semaines (du 10 au 21 mars 2026)
Equipe : 1 Data Engineer (temps plein)

OBJECTIF
--------
Valider que nous pouvons ingerer les commandes depuis l'API
e-commerce en temps quasi-reel (< 15 minutes de latence)
et les stocker dans Snowflake pour le reporting.

PERIMETRE
---------
- 1 source : API e-commerce (endpoint /orders)
- 1 transformation : nettoyage + deduplication
- 1 destination : table raw_orders dans Snowflake

HORS PERIMETRE
--------------
- Les autres sources (clients, produits, stocks)
- Les transformations metier (modele dimensional)
- Le dashboard
- Les tests de qualite automatises

CRITERES DE SUCCES
------------------
1. Le pipeline ingere les commandes des dernieres 24h sans erreur
2. La latence entre une commande passee et sa disponibilite dans
   Snowflake est < 15 minutes
3. Le taux de perte de donnees est < 0.1%
4. Le pipeline est idempotent (re-execution sans duplication)

CRITERES D'ECHEC
----------------
1. L'API ne supporte pas le volume de requetes necessaire
2. La latence est > 30 minutes malgre optimisation
3. Les credentials ne sont pas obtenus dans la premiere semaine

DECISION
--------
- GO : Tous les criteres de succes sont atteints
- NO-GO : Un ou plusieurs criteres d'echec sont atteints
- GO AVEC RESERVES : Criteres partiellement atteints, plan
  d'action identifie
```

### 1.7 Decision Go/No-Go

La decision Go/No-Go est formalisee dans une **matrice de decision** :

| Critere | Poids | Score (1-5) | Score pondere |
|---------|:-----:|:-----------:|:-------------:|
| Donnees disponibles et de qualite suffisante | 30% | 4 | 1.2 |
| Stack technique adaptee ou adaptable | 20% | 3 | 0.6 |
| Competences disponibles (equipe + formation) | 20% | 3 | 0.6 |
| POC concluant | 20% | 4 | 0.8 |
| Alignement metier confirme | 10% | 5 | 0.5 |
| **TOTAL** | **100%** | | **3.7 / 5** |

**Seuils de decision** :
- Score >= 3.5 : **GO** - Le projet est lance
- Score entre 2.5 et 3.5 : **GO avec reserves** - Plan d'action sur les points faibles
- Score < 2.5 : **NO-GO** - Le projet est reporte ou abandonne

---

## 2. Faisabilite Financiere

### 2.1 TCO (Total Cost of Ownership)

Le TCO represente le **cout total de possession** d'une solution sur sa duree de vie. Il inclut non seulement les couts directs (infrastructure) mais aussi les couts indirects (equipe, formation, maintenance).

#### Categories de couts

| Categorie | Exemples | Frequence |
|-----------|---------|-----------|
| **Infrastructure Cloud** | Compute (EC2, VMs), Stockage (S3, Blob), Reseau | Mensuel |
| **Licences et outils** | Snowflake, Databricks, Tableau, Jira, dbt Cloud | Mensuel/Annuel |
| **Ressources humaines** | Salaires equipe data, consultants externes | Mensuel |
| **Formation** | Formations techniques, certifications | Ponctuel |
| **Mise en place initiale** | Developpement initial, migration, configuration | Ponctuel |
| **Maintenance** | Corrections, evolutions mineures, monitoring | Mensuel |
| **Support** | Support editeur, support interne | Mensuel/Annuel |

#### Exemple : TCO d'un Data Pipeline (Airflow + Snowflake + dbt)

**Hypotheses** : Pipeline ETL quotidien, 5 sources, 50 Go de donnees, equipe de 2 Data Engineers.

| Poste de cout | Cout mensuel | Cout annuel |
|--------------|:------------:|:-----------:|
| **Infrastructure** | | |
| Snowflake (XS warehouse, 8h/jour) | 800 EUR | 9 600 EUR |
| Airflow sur EC2 (t3.large, 24/7) | 150 EUR | 1 800 EUR |
| S3 (stockage 500 Go + transferts) | 50 EUR | 600 EUR |
| **Licences** | | |
| dbt Cloud (Team, 2 users) | 200 EUR | 2 400 EUR |
| Monitoring (Datadog, 2 hosts) | 80 EUR | 960 EUR |
| **Ressources humaines** | | |
| 2 Data Engineers (salaire charge) | 14 000 EUR | 168 000 EUR |
| **Formation** | | |
| Formation Snowflake (2 personnes) | - | 3 000 EUR |
| Formation dbt (2 personnes) | - | 2 000 EUR |
| **Mise en place initiale** (amortie sur 3 ans) | | |
| Developpement initial (3 mois, 2 DE) | 7 000 EUR | 84 000 EUR* |
| | | |
| **TOTAL (annee 1)** | **~22 280 EUR** | **~272 360 EUR** |
| **TOTAL (annee 2+)** | **~15 280 EUR** | **~183 360 EUR** |

*Le developpement initial de 84 000 EUR est un cout unique la premiere annee.

💡 **Astuce** : Le poste de cout le plus eleve est presque toujours les **ressources humaines** (60-80% du TCO). L'optimisation de l'infrastructure est importante mais ne change pas fondamentalement le cout total.

### 2.2 ROI (Return on Investment)

#### Formule

```
              Gains generes - Cout total (TCO)
ROI (%) = ────────────────────────────────────── x 100
                      Cout total (TCO)
```

#### Types de gains pour un projet data

| Type de gain | Exemples | Comment mesurer |
|-------------|---------|----------------|
| **Gain de temps** | Automatisation de rapports manuels | Heures economisees x cout horaire |
| **Reduction d'erreurs** | Moins d'erreurs de saisie ou de calcul | Cout moyen d'une erreur x nombre d'erreurs evitees |
| **Augmentation de revenus** | Meilleure conversion grace aux recommandations | Revenu additionnel attribuable au projet |
| **Reduction de couts** | Optimisation des achats grace a l'analyse predictive | Economies realisees |
| **Evitement de pertes** | Detection de fraude, prevention du churn | Pertes evitees |
| **Conformite** | Eviter des amendes RGPD | Montant des amendes potentielles |

#### Exemple : ROI d'un Modele de Prediction de Churn

**Contexte** : Un operateur telecom perd 5% de ses clients chaque mois (churn). Un client rapporte en moyenne 50 EUR/mois. L'entreprise a 100 000 clients.

**Situation actuelle (sans modele)** :
- Churn mensuel : 5 000 clients
- Perte mensuelle : 5 000 x 50 EUR = 250 000 EUR/mois
- Perte annuelle : 3 000 000 EUR

**Situation cible (avec modele)** :
- Le modele identifie 80% des churners potentiels (recall = 0.80)
- Les actions de retention (offre speciale, appel commercial) retiennent 30% des churners identifies
- Clients sauves par mois : 5 000 x 0.80 x 0.30 = 1 200 clients
- Revenu sauve par mois : 1 200 x 50 EUR = 60 000 EUR
- Revenu sauve par an : 720 000 EUR

**Cout du modele** :
- Cout de retention (offres speciales) : 10 EUR/client cible x 4 000 cibles/mois = 40 000 EUR/mois = 480 000 EUR/an
- Cout du projet data (TCO annee 1) : 200 000 EUR
- **Cout total annee 1 : 680 000 EUR**

**Calcul du ROI** :

```
ROI = (720 000 - 680 000) / 680 000 x 100 = 5.9% (annee 1)
ROI = (720 000 - 480 000) / 480 000 x 100 = 50.0% (annee 2+)
```

Le projet est **rentable des la premiere annee** et fortement rentable a partir de la deuxieme annee.

### 2.3 Presenter le business case

| Element | Contenu |
|---------|---------|
| **Probleme** | Churn de 5%/mois = perte de 3M EUR/an |
| **Solution** | Modele ML de prediction de churn + actions de retention |
| **Investissement** | 200 000 EUR (annee 1) + 480 000 EUR (retention) |
| **Gains** | 720 000 EUR de revenu sauve par an |
| **ROI** | 5.9% annee 1, 50% annee 2+ |
| **Payback period** | 11 mois |
| **Risques** | Recall du modele inferieur aux attentes, cout de retention plus eleve |

---

## 3. Analyse des Risques

### 3.1 Analyse SWOT pour un projet data

L'analyse SWOT (Strengths, Weaknesses, Opportunities, Threats) est un outil strategique pour evaluer un projet.

#### Exemple : Projet de migration vers le cloud

| | **Positif** | **Negatif** |
|---|:---:|:---:|
| **Interne** | **Forces (Strengths)** | **Faiblesses (Weaknesses)** |
| | Equipe technique competente | Pas d'experience cloud |
| | Donnees bien documentees | Budget limite |
| | Sponsor engage | Legacy code mal maintenu |
| | Stack moderne (Python, dbt) | Pas de DBA cloud |
| **Externe** | **Opportunites (Opportunities)** | **Menaces (Threats)** |
| | Reduction des couts infra (-40%) | Dependance a un fournisseur cloud |
| | Scalabilite automatique | Risque de hausse des prix cloud |
| | Acces a de nouveaux services (ML) | Reglementation sur la localisation des donnees |
| | Concurrents deja migres | Penurie de talents cloud |

### 3.2 Matrice de risques (Probabilite x Impact)

#### Identification des risques

| # | Risque | Categorie |
|---|--------|-----------|
| R1 | Les donnees source sont de mauvaise qualite | Technique |
| R2 | L'equipe ne maitrise pas la stack cible | Competences |
| R3 | Le budget est depasse | Financier |
| R4 | Le sponsor change ou quitte l'entreprise | Organisationnel |
| R5 | Non-conformite RGPD decouverte tardivement | Reglementaire |
| R6 | Performance insuffisante en production | Technique |
| R7 | Resistance au changement des utilisateurs | Humain |
| R8 | Defaillance d'un fournisseur cloud | Technique |

#### Evaluation des risques

```
IMPACT
  ^
5 │           R5
  │      R3        R1
4 │
  │ R8        R2
3 │                     R6
  │      R7
2 │                R4
  │
1 │
  └──────────────────────> PROBABILITE
  1    2    3    4    5
```

| Risque | Probabilite (1-5) | Impact (1-5) | Score | Niveau |
|--------|:-----------------:|:------------:|:-----:|:------:|
| R1 - Qualite donnees | 4 | 5 | 20 | **Critique** |
| R5 - Non-conformite RGPD | 2 | 5 | 10 | **Eleve** |
| R3 - Depassement budget | 3 | 4 | 12 | **Eleve** |
| R2 - Manque competences | 3 | 3 | 9 | **Moyen** |
| R6 - Performance | 4 | 3 | 12 | **Eleve** |
| R7 - Resistance changement | 2 | 2 | 4 | **Faible** |
| R4 - Changement sponsor | 3 | 2 | 6 | **Moyen** |
| R8 - Defaillance cloud | 1 | 3 | 3 | **Faible** |

**Echelle** :
- Score >= 15 : **Critique** - Action immediate obligatoire
- Score 10-14 : **Eleve** - Plan de mitigation a definir
- Score 5-9 : **Moyen** - A surveiller
- Score < 5 : **Faible** - Accepter le risque

### 3.3 Strategies de mitigation

| Risque | Strategie | Action concrete |
|--------|-----------|----------------|
| R1 - Qualite donnees (Critique) | **Reduire** | Audit de donnees en semaine 1. Tests de qualite automatises. Budget pour le nettoyage. |
| R5 - RGPD (Eleve) | **Eviter** | Impliquer le DPO des le cadrage. Audit RGPD avant le developpement. |
| R3 - Budget (Eleve) | **Transferer** | Prevoir une marge de 20%. Revue budgetaire mensuelle. |
| R2 - Competences (Moyen) | **Reduire** | Formation planifiee en amont. Accompagnement par un consultant. |
| R6 - Performance (Eleve) | **Reduire** | POC de performance. Tests de charge en staging. Plan de scalabilite. |
| R7 - Resistance (Faible) | **Accepter** | Communication et formation. Champions utilisateurs. |
| R4 - Sponsor (Moyen) | **Reduire** | Impliquer plusieurs decideurs. Documenter les decisions. |
| R8 - Cloud (Faible) | **Accepter** | Multi-AZ. Backup cross-region. |

### 3.4 Registre des risques - Template

| # | Risque | Prob. | Impact | Score | Strategie | Action | Responsable | Statut |
|---|--------|:-----:|:------:|:-----:|-----------|--------|-------------|:------:|
| R1 | Qualite donnees | 4 | 5 | 20 | Reduire | Audit semaine 1 | DE1 | En cours |
| R5 | RGPD | 2 | 5 | 10 | Eviter | Audit DPO | DPO | A faire |
| R3 | Budget | 3 | 4 | 12 | Transferer | Marge 20% | PM | Fait |
| ... | | | | | | | | |

---

## 4. Synthese

| Concept | Point cle |
|---------|-----------|
| Audit de donnees | 10 questions a poser AVANT de commencer le projet |
| POC | 2-4 semaines max, criteres de succes definis, code jetable |
| Go/No-Go | Matrice de decision ponderee, seuil a 3.5/5 |
| TCO | 60-80% du cout = ressources humaines, pas l'infra |
| ROI | Gains generes - Couts / Couts. Inclure les gains indirects. |
| SWOT | Forces/Faiblesses (interne) + Opportunites/Menaces (externe) |
| Matrice de risques | Probabilite x Impact. Score >= 15 = action immediate |

### Les 3 regles d'or

1. **Pas de projet sans audit de donnees** - 2 semaines d'audit peuvent economiser 6 mois de developpement
2. **Le TCO inclut les gens** - N'optimisez pas que l'infrastructure
3. **Tout risque critique doit avoir un plan de mitigation** - Pas d'option "on verra"

---

📝 **Exercice** : Estimez le TCO sur 3 ans et le ROI d'un projet d'automatisation de reporting (3 rapports mensuels produits manuellement en 3 jours par un analyste). Identifiez les 5 risques principaux et proposez des strategies de mitigation.

---

[← Precedent](04-objectifs-smart-priorisation-rice.md) | [🏠 Accueil](README.md) | [Suivant →](06-documentation-communication.md)

---

**Academy** - Formation Data Engineer
