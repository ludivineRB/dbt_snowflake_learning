# Brief — Construction d'un Data Warehouse et de Data Marts avec BigQuery

**Projet décisionnel basé sur AdventureWorks Data Warehouse (DW)**

---

## Informations générales

| Critère       | Valeur                                              |
|---------------|-----------------------------------------------------|
| Durée         | 5 jours (35 heures)                                 |
| Niveau        | Intermédiaire                                       |
| Modalité      | Individuel                                          |
| Technologies  | GCP, BigQuery, SQL                                  |
| Données       | AdventureWorks Data Warehouse (DW)                  |
| Prérequis     | SQL, concepts DW (faits / dimensions), bases BigQuery |

---

## Contexte

Vous êtes **Data Engineer** chez **AdventureWorks**, une entreprise fictive spécialisée dans la fabrication et la vente de vélos et d'accessoires.

L'entreprise met à disposition la base **AdventureWorks Data Warehouse (DW)**, déjà structurée en **schéma en étoile**, mais **non directement exploitable** pour des usages analytiques avancés (performance, KPI prêts à l'emploi, gouvernance).

Votre mission est de construire, dans **BigQuery**, une architecture décisionnelle complète permettant :

- l'import des données ;
- leur transformation et standardisation ;
- la reconstruction d'un **Core Data Warehouse** ;
- la création de **Data Marts métier** ;
- la mise à disposition d'indicateurs fiables pour la direction.

---

## Objectifs pédagogiques

À l'issue du brief, vous serez capable de :

- structurer un projet BigQuery (datasets, couches) ;
- importer des données AdventureWorks DW dans BigQuery ;
- implémenter une architecture **Staging → Core DW → Data Marts** ;
- écrire des transformations ELT performantes en SQL BigQuery ;
- écrire des requêtes OLAP avancées (ROLLUP, CUBE, window functions) ;
- optimiser les tables avec **partitionnement** et **clustering** ;
- construire des **KPI métiers** prêts pour le reporting ;
- automatiser et documenter un pipeline analytique.

---

## Données fournies

### Fichiers CSV (hébergés en ligne)

| Fichier | URL |
|---------|-----|
| FactResellerSales | <https://solliancepublicdata.blob.core.windows.net/dataengineering/dp-203/awdata/FactResellerSales.csv> |
| DimProduct | <https://solliancepublicdata.blob.core.windows.net/dataengineering/dp-203/awdata/DimProduct.csv> |
| DimReseller | <https://solliancepublicdata.blob.core.windows.net/dataengineering/dp-203/awdata/DimReseller.csv> |
| DimEmployee | <https://solliancepublicdata.blob.core.windows.net/dataengineering/dp-203/awdata/DimEmployee.csv> |
| DimGeography | <https://solliancepublicdata.blob.core.windows.net/dataengineering/dp-203/awdata/DimGeography.csv> |
| DimDate | <https://solliancepublicdata.blob.core.windows.net/dataengineering/dp-203/awdata/DimDate.csv> |

### Documentation

- Fichier **AdventureWorks_DataDescription.xlsx** (dictionnaire de données) fourni par le formateur.

> **Note :** Les CSV utilisent le séparateur **pipe `|`** (pas la virgule).

---

## Architecture cible BigQuery

```
staging   →   dw   →   marts
  |            |        |
  |            |        ├─ mart_sales
  |            |        ├─ mart_products
  |            |        └─ mart_customers
```

---

## Planning détaillé

```
Jour 1 : Veille + Découverte (7h)
├── Partie 0 — Veille : Concepts DW, OLAP, BigQuery
│   ├── TD : Conception conceptuelle d'un DW
│   └── TP : Conception logique ROLAP + requêtes OLAP SQL
└── Partie 1 — Découverte et modélisation AdventureWorks

Jour 2 : Import & Core DW (7h)
├── Partie 2 — Import des données & couche Staging
└── Partie 3 — Transformations & Core Data Warehouse (début)

Jour 3 : Core DW & Data Marts (7h)
├── Partie 3 — Core DW (fin)
└── Partie 4 — Data Marts & KPI métier (début)

Jour 4 : Data Marts & Requêtes OLAP (7h)
├── Partie 4 — Data Marts (fin) + requêtes OLAP avancées
└── Partie 5 — Optimisation & automatisation (début)

Jour 5 : Finalisation (7h)
├── Partie 5 — Automatisation, monitoring, documentation
└── Rendu des livrables
```

---

## Partie 0 — Veille : Concepts DW, OLAP et BigQuery

Cette phase de veille pose les bases conceptuelles nécessaires à la conception et à l'implémentation du Data Warehouse AdventureWorks dans BigQuery.

**Fichier détaillé :** [Partie0.md](./Partie0.md)

---

### 1. Concepts du Data Warehouse

* **Informatique décisionnelle**
  Analyse des données pour l'aide à la décision.

* **Entrepôt de données (DW)**
  Base orientée analyse, intégrée, historisée et non volatile.

* **Modélisation décisionnelle**

  * tables de faits (mesures) ;
  * tables de dimensions (axes d'analyse) ;
  * schémas en **étoile** / **flocon**.

**TD associé** : conception conceptuelle d'un Data Warehouse (identification des faits, dimensions et mesures)

---

### 2. OLAP et implantation des Data Warehouses

#### Approches d'implantation

* **ROLAP** : basé sur des bases relationnelles et SQL ;
* **MOLAP** : basé sur des cubes multidimensionnels ;
* **HOLAP** : approche hybride.

#### Opérations OLAP principales

* **Slice** : sélection sur une dimension ;
* **Dice** : sélection multidimensionnelle ;
* **Roll-up** : agrégation (jour → mois → année) ;
* **Drill-down** : descente dans le détail ;
* **Pivot** : changement d'axe d'analyse.

#### Requêtes OLAP SQL

* jointures faits / dimensions ;
* agrégations (`SUM`, `COUNT`, `AVG`) ;
* `ROLLUP`, `CUBE`, `GROUPING SETS` ;
* window functions (`LAG`, `RANK`, `SUM() OVER`).

**TP associé** : Modélisation et conception logique ROLAP d'un ED, requêtes OLAP SQL (PostgreSQL)

---

### 3. Introduction à BigQuery

* **BigQuery** : Data Warehouse cloud **serverless** (GCP) ;
* moteur SQL analytique massivement parallèle ;
* séparation stockage / calcul ;
* scalabilité automatique.

#### Bonnes pratiques clés

* organisation des données par **datasets** ;
* tables volumineuses optimisées par :

  * **partitionnement** (souvent temporel) ;
  * **clustering** (colonnes fréquemment filtrées) ;
* approche **ELT** privilégiée en environnement Cloud.

---

## Partie 1 — Découverte, cadrage et modélisation

**Fichier détaillé :** [Partie1_apprenants.md](./Partie1_apprenants.md)

### Objectifs

* comprendre les données AdventureWorks DW ;
* définir l'architecture BigQuery ;
* concevoir le modèle cible.

### Travaux

* analyse de FactResellerSales (événement métier, mesures, clés) ;
* classification des mesures (FLOW / VPU / STOCK) ;
* détermination de la granularité du fait ;
* analyse des dimensions (attributs, axes d'analyse) ;
* formulation de KPI métier ;
* conception du schéma en étoile cible.

### Livrables

* schéma cible (DW + Data Marts) ;
* liste des KPI par Data Mart.

---

## Partie 2 — Import des données & couche Staging

**Fichier détaillé :** [Partie2_apprenants.md](./Partie2_apprenants.md)

### Objectifs

* charger les données dans BigQuery ;
* mettre en place une zone brute contrôlée.

### Travaux

* création du projet GCP et des datasets (`staging`, `dw`, `marts`, `meta`) ;
* création d'un bucket Cloud Storage ;
* import des 6 tables CSV dans BigQuery ;
* ajout de métadonnées (`_ingested_at`, `_source_file`) ;
* contrôles qualité (comptages, NULLs, doublons, intégrité référentielle).

### Livrables

* tables `staging.*` ;
* requêtes de contrôle qualité ;
* table `meta.pipeline_logs`.

---

## Partie 3 — Transformations & Core Data Warehouse

**Fichier détaillé :** [Partie3_apprenants.md](./Partie3_apprenants.md)

### Objectifs

* construire un DW propre et cohérent.

### Travaux

* création des 5 dimensions nettoyées (`dw.dim_*`) ;
* création de la table de faits (`dw.fact_reseller_sales`) ;
* transformations : standardisation, filtrage, calculs (margin) ;
* optimisation : partitionnement (dates) + clustering ;
* validation : cohérence staging vs dw, requêtes de test.

### Livrables

* tables `dw.*` ;
* scripts SQL ELT documentés ;
* résultats des contrôles.

---

## Partie 4 — Data Marts & KPI métier

**Fichier détaillé :** [Partie4_apprenants.md](./Partie4_apprenants.md)

### Objectifs

* créer des tables orientées usage et performance ;
* écrire des requêtes OLAP avancées.

### Data Marts attendus

#### `mart_sales`

* CA total, quantité vendue, marge, panier moyen, nombre de commandes ;
* agrégations : jour / mois / année / pays / type revendeur ;
* requêtes OLAP : ROLLUP, CUBE, LAG, cumul.

#### `mart_products`

* CA par produit, marge, classement, contribution au CA ;
* analyse Pareto (80/20).

#### `mart_customers`

* CA par revendeur, LTV, fréquence, récence ;
* segmentation (Active / At Risk / Churned) ;
* 7 requêtes KPI pour la direction.

### Livrables

* tables `marts.*` ;
* requêtes KPI validées avec résultats et interprétation.

---

## Partie 5 — Optimisation, automatisation & documentation

**Fichier détaillé :** [Partie5_apprenants.md](./Partie5_apprenants.md)

### Objectifs

* rendre le pipeline exploitable et maintenable.

### Travaux

* audit du partitionnement et du clustering ;
* création de 3 Stored Procedures (refresh DW, refresh Marts, pipeline complet) ;
* planification avec Scheduled Queries ;
* vues de monitoring ;
* documentation finale (README).

### Livrables

* pipeline automatisé ;
* README (architecture, tables, KPI, exécution) ;
* vues de monitoring fonctionnelles.

---

## Livrables finaux

* scripts SQL BigQuery complets (staging → dw → marts) ;
* tables DW & Data Marts fonctionnelles ;
* requêtes OLAP (ROLLUP, CUBE, window functions) ;
* KPI métiers avec résultats et interprétation ;
* pipeline automatisé (Stored Procedures + Scheduled Queries) ;
* documentation complète (README).

---

## Critères d'évaluation

| Partie | Thème | Points |
|--------|-------|--------|
| **Partie 1** | Découverte, cadrage, modélisation | **20** |
| **Partie 2** | Import & Staging | **20** |
| **Partie 3** | Core Data Warehouse | **30** |
| **Partie 4** | Data Marts & KPI | **35** |
| **Partie 5** | Optimisation & automatisation | **15** |
| **TOTAL** | | **120** |

**Note sur 20 :** Total / 6

Le détail des critères par partie est disponible dans les fichiers formateur correspondants.

---

## Ressources

* [Cours Data Warehouse](../cours/)
* [Cours BigQuery](../../../04-Cloud-Platforms/GCP/BigQuery/cours/)
* [Documentation BigQuery](https://cloud.google.com/bigquery/docs)
* [BigQuery SQL Reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
