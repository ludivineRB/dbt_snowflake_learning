# TP : Migration PostgreSQL vers BigQuery

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 1h |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Prérequis** | [Module 07 - PostgreSQL vs BigQuery](../cours/07-postgresql-vs-bigquery.md) |
| **Outils** | PostgreSQL (local ou Docker), Google BigQuery (free tier) |
| **Livrables** | Scripts SQL BigQuery adaptés + réponses aux questions |

## Objectifs

- Traduire des requêtes PostgreSQL en syntaxe BigQuery
- Adapter un schéma dimensionnel PostgreSQL pour BigQuery (types, partitionnement, clustering)
- Comprendre les différences de comportement (transactions, index, types)
- Optimiser les requêtes pour le modèle de facturation BigQuery

---

## Contexte

Vous avez implémenté le Data Warehouse **CinéStar** dans PostgreSQL (TP ROLAP + TP SQL OLAP). La direction décide de migrer vers **BigQuery** pour bénéficier du serverless et du scaling illimité.

Votre mission : adapter le schéma et les requêtes pour BigQuery.

---

## Partie 1 : Adaptation du schéma (20 min)

### 1.1 : Traduire le DDL

Voici le schéma PostgreSQL existant. Traduisez-le en BigQuery SQL.

**PostgreSQL (existant) :**

```sql
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,
    date            DATE NOT NULL,
    day_of_week     INTEGER,
    day_name        VARCHAR(10),
    month           INTEGER,
    month_name      VARCHAR(10),
    quarter         INTEGER,
    year            INTEGER,
    is_weekend      BOOLEAN,
    is_holiday      BOOLEAN
);

CREATE TABLE dim_cinema (
    cinema_key      SERIAL PRIMARY KEY,
    cinema_id       VARCHAR(10) NOT NULL,
    nom             VARCHAR(100),
    ville           VARCHAR(50),
    region          VARCHAR(50),
    nb_salles       INTEGER
);

CREATE TABLE dim_film (
    film_key        SERIAL PRIMARY KEY,
    film_id         VARCHAR(10) NOT NULL,
    titre           VARCHAR(200),
    genre           VARCHAR(50),
    realisateur     VARCHAR(100),
    duree_minutes   INTEGER,
    annee_sortie    INTEGER
);

CREATE TABLE fact_ventes_billets (
    date_key        INTEGER REFERENCES dim_date(date_key),
    cinema_key      INTEGER REFERENCES dim_cinema(cinema_key),
    film_key        INTEGER REFERENCES dim_film(film_key),
    nb_billets      INTEGER,
    recette         NUMERIC(10,2),
    nb_seances      INTEGER
);

CREATE INDEX idx_fact_date ON fact_ventes_billets(date_key);
CREATE INDEX idx_fact_cinema ON fact_ventes_billets(cinema_key);
```

**Exercice :** Réécrivez ce schéma en BigQuery SQL.

**Points d'attention :**
- Remplacez les types PostgreSQL par les types BigQuery (`INT64`, `STRING`, `FLOAT64`, `BOOL`)
- Supprimez les `PRIMARY KEY`, `FOREIGN KEY`, `SERIAL`, `INDEX`
- Ajoutez `PARTITION BY` et `CLUSTER BY` sur la table de faits
- Utilisez le format `project.dataset.table`

### 1.2 : Questions de réflexion

1. Pourquoi BigQuery n'a-t-il pas besoin d'index B-tree ?
2. Quelle colonne est la meilleure candidate pour le `PARTITION BY` ? Pourquoi ?
3. Quelles colonnes choisir pour le `CLUSTER BY` ? (max 4)

---

## Partie 2 : Migration des requêtes (25 min)

### 2.1 : Requêtes de base

Traduisez chaque requête PostgreSQL en BigQuery SQL.

**Requête 1 : CA par trimestre et région**

```sql
-- PostgreSQL
SELECT
    d.year,
    d.quarter,
    c.region,
    SUM(f.recette) as ca_total,
    SUM(f.nb_billets) as total_billets
FROM fact_ventes_billets f
JOIN dim_date d ON f.date_key = d.date_key
JOIN dim_cinema c ON f.cinema_key = c.cinema_key
WHERE d.year = 2024
GROUP BY d.year, d.quarter, c.region
ORDER BY d.quarter, ca_total DESC;
```

**Requête 2 : Top 5 films par recette (avec LIMIT)**

```sql
-- PostgreSQL
SELECT
    fi.titre,
    fi.genre,
    SUM(f.recette) as recette_totale,
    SUM(f.nb_billets) as total_billets,
    ROUND(SUM(f.recette) / SUM(f.nb_billets), 2) as prix_moyen_billet
FROM fact_ventes_billets f
JOIN dim_film fi ON f.film_key = fi.film_key
GROUP BY fi.titre, fi.genre
ORDER BY recette_totale DESC
LIMIT 5;
```

**Requête 3 : Évolution mensuelle avec DATE_TRUNC**

```sql
-- PostgreSQL
SELECT
    DATE_TRUNC('month', d.date) as mois,
    SUM(f.recette) as ca_mensuel,
    SUM(f.nb_billets) as billets_mensuels
FROM fact_ventes_billets f
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY DATE_TRUNC('month', d.date)
ORDER BY mois;
```

### 2.2 : Fonctions fenêtres

**Requête 4 : Classement des cinémas avec RANK et cumul**

```sql
-- PostgreSQL
SELECT
    c.nom as cinema,
    c.region,
    SUM(f.recette) as ca_total,
    RANK() OVER (ORDER BY SUM(f.recette) DESC) as rang,
    SUM(SUM(f.recette)) OVER (ORDER BY SUM(f.recette) DESC) as ca_cumule
FROM fact_ventes_billets f
JOIN dim_cinema c ON f.cinema_key = c.cinema_key
GROUP BY c.nom, c.region;
```

**Requête 5 : Croissance mois par mois avec LAG**

```sql
-- PostgreSQL
SELECT
    DATE_TRUNC('month', d.date) as mois,
    SUM(f.recette) as ca,
    LAG(SUM(f.recette)) OVER (ORDER BY DATE_TRUNC('month', d.date)) as ca_mois_precedent,
    ROUND(
        (SUM(f.recette) - LAG(SUM(f.recette)) OVER (ORDER BY DATE_TRUNC('month', d.date)))
        / LAG(SUM(f.recette)) OVER (ORDER BY DATE_TRUNC('month', d.date)) * 100,
        2
    ) as croissance_pct
FROM fact_ventes_billets f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY DATE_TRUNC('month', d.date)
ORDER BY mois;
```

### 2.3 : Syntaxe spécifique

**Requête 6 : Génération de séries de dates**

```sql
-- PostgreSQL
SELECT generate_series('2024-01-01'::date, '2024-12-31'::date, '1 month'::interval) as mois;
```

**Requête 7 : ROLLUP avec COALESCE et cast**

```sql
-- PostgreSQL
SELECT
    COALESCE(c.region, 'TOTAL') as region,
    COALESCE(fi.genre, 'TOTAL') as genre,
    SUM(f.recette)::INTEGER as ca_total
FROM fact_ventes_billets f
JOIN dim_cinema c ON f.cinema_key = c.cinema_key
JOIN dim_film fi ON f.film_key = fi.film_key
GROUP BY ROLLUP(c.region, fi.genre);
```

---

## Partie 3 : Optimisation BigQuery (15 min)

### 3.1 : Analyse des coûts

Pour chaque requête ci-dessous, estimez le coût BigQuery (on-demand à $5/TB) et proposez une optimisation :

**Requête A (non optimisée) :**
```sql
SELECT *
FROM `project.dataset.fact_ventes_billets`
WHERE CAST(date_key AS STRING) LIKE '2024%';
```

**Questions :**
1. Pourquoi cette requête est-elle coûteuse ?
2. Réécrivez-la pour minimiser les TB scannés

**Requête B (non optimisée) :**
```sql
SELECT
    c.region,
    SUM(f.recette)
FROM `project.dataset.fact_ventes_billets` f
JOIN `project.dataset.dim_cinema` c ON f.cinema_key = c.cinema_key
GROUP BY c.region;
```

**Questions :**
3. Cette requête scanne-t-elle toutes les colonnes de `fact_ventes_billets` ? Pourquoi ?
4. La table est partitionnée par date. Est-ce utile ici ? Comment améliorer ?

### 3.2 : Comparaison de coûts

Estimez le coût mensuel d'exploitation du DW CinéStar sur BigQuery :
- **Stockage** : 50 GB de données (30 GB actives, 20 GB long-term)
- **Requêtes** : 200 requêtes/jour, scannant en moyenne 2 GB chacune

**Questions :**
5. Calculez le coût mensuel estimé (stockage + requêtes on-demand)
6. À partir de quel volume de requêtes quotidien serait-il rentable de passer en capacity pricing (100 slots à ~$2000/mois) ?

---

## Récapitulatif des différences rencontrées

À compléter au fur et à mesure du TP :

| Élément | PostgreSQL | BigQuery |
|---------|------------|----------|
| Types entiers | `INTEGER`, `SERIAL` | ? |
| Types texte | `VARCHAR(n)` | ? |
| Types décimaux | `NUMERIC(10,2)` | ? |
| Référence table | `schema.table` | ? |
| Date truncation | `DATE_TRUNC('month', col)` | ? |
| Type casting | `col::TYPE` | ? |
| Série de dates | `generate_series(...)` | ? |
| Index | `CREATE INDEX ...` | ? |
| Partitionnement | `PARTITION BY RANGE(...)` | ? |

---

## Pour aller plus loin

- Essayez de charger des données CSV dans BigQuery via la console
- Explorez `INFORMATION_SCHEMA` pour voir les métadonnées de vos tables
- Testez `SAFE_CAST` vs `CAST` sur des données mal formatées
- Comparez le temps d'exécution d'une même requête avec et sans filtre de partition
