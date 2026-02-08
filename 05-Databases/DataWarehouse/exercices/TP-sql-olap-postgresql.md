# TP : SQL OLAP avec PostgreSQL

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 3h |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Prérequis** | [Module 05 - Opérations OLAP](../cours/05-operations-olap.md), [TP ROLAP](./TP-conception-logique-rolap.md) |
| **Outils** | PostgreSQL 14+ (local ou Docker) |
| **Livrables** | Script SQL complet avec toutes les requêtes |

## Objectifs

- Maîtriser `ROLLUP`, `CUBE` et `GROUPING SETS` pour les agrégations multi-niveaux
- Utiliser les fonctions de fenêtrage (window functions) pour les analyses OLAP
- Implémenter les opérations OLAP classiques (slice, dice, roll-up, drill-down, pivot) en SQL
- Comparer les performances des différentes approches

---

## Setup : Création de l'environnement

### Option 1 : Docker (recommandé)

```bash
docker run --name pg-olap -e POSTGRES_PASSWORD=olap123 -p 5432:5432 -d postgres:16
docker exec -it pg-olap psql -U postgres
```

### Option 2 : PostgreSQL local

```bash
psql -U postgres
CREATE DATABASE olap_tp;
\c olap_tp
```

### Créer et charger les données

Exécutez le script suivant pour créer un mini Data Warehouse de ventes :

```sql
-- ============================================
-- CRÉATION DU SCHÉMA DW
-- ============================================

CREATE SCHEMA IF NOT EXISTS dw;

-- Dimension Date
CREATE TABLE dw.dim_date (
    date_key    INTEGER PRIMARY KEY,
    date_val    DATE NOT NULL,
    jour        INTEGER NOT NULL,
    mois        INTEGER NOT NULL,
    nom_mois    VARCHAR(10) NOT NULL,
    trimestre   INTEGER NOT NULL,
    annee       INTEGER NOT NULL,
    jour_semaine VARCHAR(10) NOT NULL,
    est_weekend BOOLEAN NOT NULL
);

INSERT INTO dw.dim_date
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER,
    d,
    EXTRACT(DAY FROM d)::INTEGER,
    EXTRACT(MONTH FROM d)::INTEGER,
    TO_CHAR(d, 'TMMonth'),
    EXTRACT(QUARTER FROM d)::INTEGER,
    EXTRACT(YEAR FROM d)::INTEGER,
    TO_CHAR(d, 'TMDay'),
    EXTRACT(ISODOW FROM d) IN (6, 7)
FROM generate_series('2023-01-01'::date, '2024-12-31'::date, '1 day') d;

-- Dimension Région
CREATE TABLE dw.dim_region (
    region_key  SERIAL PRIMARY KEY,
    ville       VARCHAR(50) NOT NULL,
    region      VARCHAR(50) NOT NULL,
    pays        VARCHAR(30) NOT NULL DEFAULT 'France'
);

INSERT INTO dw.dim_region (ville, region) VALUES
    ('Paris', 'Île-de-France'),
    ('Lyon', 'Auvergne-Rhône-Alpes'),
    ('Marseille', 'PACA'),
    ('Toulouse', 'Occitanie'),
    ('Lille', 'Hauts-de-France'),
    ('Bordeaux', 'Nouvelle-Aquitaine'),
    ('Nantes', 'Pays de la Loire'),
    ('Strasbourg', 'Grand Est');

-- Dimension Produit
CREATE TABLE dw.dim_produit (
    produit_key SERIAL PRIMARY KEY,
    nom_produit VARCHAR(100) NOT NULL,
    categorie   VARCHAR(50) NOT NULL,
    sous_categorie VARCHAR(50) NOT NULL,
    marque      VARCHAR(50) NOT NULL,
    prix_unitaire NUMERIC(8,2) NOT NULL
);

INSERT INTO dw.dim_produit (nom_produit, categorie, sous_categorie, marque, prix_unitaire) VALUES
    ('Laptop Pro 15', 'Électronique', 'Ordinateurs', 'TechBrand', 1299.99),
    ('Laptop Air 13', 'Électronique', 'Ordinateurs', 'TechBrand', 999.99),
    ('Smartphone X12', 'Électronique', 'Téléphones', 'PhoneCo', 899.99),
    ('Smartphone Lite', 'Électronique', 'Téléphones', 'PhoneCo', 399.99),
    ('Tablette Tab10', 'Électronique', 'Tablettes', 'TechBrand', 599.99),
    ('Casque Audio BT', 'Électronique', 'Audio', 'SoundMax', 149.99),
    ('T-shirt Premium', 'Vêtements', 'Hauts', 'ModeFR', 39.99),
    ('Jean Slim', 'Vêtements', 'Bas', 'ModeFR', 69.99),
    ('Sneakers Urban', 'Vêtements', 'Chaussures', 'StepUp', 89.99),
    ('Veste Hiver', 'Vêtements', 'Manteaux', 'ModeFR', 159.99),
    ('Canapé 3 places', 'Maison', 'Meubles', 'HomeDeco', 799.99),
    ('Lampe Design', 'Maison', 'Éclairage', 'HomeDeco', 89.99),
    ('Machine à café', 'Maison', 'Électroménager', 'CaféPlus', 249.99),
    ('Aspirateur Robot', 'Maison', 'Électroménager', 'CleanBot', 349.99),
    ('Crème visage Bio', 'Beauté', 'Soins', 'NaturSkin', 29.99),
    ('Parfum Élégance', 'Beauté', 'Parfums', 'ScentLux', 79.99);

-- Dimension Client
CREATE TABLE dw.dim_client (
    client_key  SERIAL PRIMARY KEY,
    segment     VARCHAR(20) NOT NULL,  -- Premium, Standard, Nouveau
    tranche_age VARCHAR(20) NOT NULL   -- 18-25, 26-35, 36-50, 51+
);

INSERT INTO dw.dim_client (segment, tranche_age) VALUES
    ('Premium', '26-35'), ('Premium', '36-50'), ('Premium', '51+'),
    ('Standard', '18-25'), ('Standard', '26-35'), ('Standard', '36-50'),
    ('Standard', '51+'), ('Nouveau', '18-25'), ('Nouveau', '26-35'),
    ('Nouveau', '36-50');

-- Dimension Canal
CREATE TABLE dw.dim_canal (
    canal_key   SERIAL PRIMARY KEY,
    canal       VARCHAR(30) NOT NULL,  -- Magasin, Web, Mobile
    type_canal  VARCHAR(20) NOT NULL   -- Physique, Digital
);

INSERT INTO dw.dim_canal (canal, type_canal) VALUES
    ('Magasin', 'Physique'),
    ('Site Web', 'Digital'),
    ('Application Mobile', 'Digital');

-- ============================================
-- TABLE DE FAITS : VENTES
-- ============================================

CREATE TABLE dw.fact_ventes (
    vente_id    BIGSERIAL,
    date_key    INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    region_key  INTEGER NOT NULL REFERENCES dw.dim_region(region_key),
    produit_key INTEGER NOT NULL REFERENCES dw.dim_produit(produit_key),
    client_key  INTEGER NOT NULL REFERENCES dw.dim_client(client_key),
    canal_key   INTEGER NOT NULL REFERENCES dw.dim_canal(canal_key),
    quantite    INTEGER NOT NULL,
    montant     NUMERIC(10,2) NOT NULL,
    cout        NUMERIC(10,2) NOT NULL,
    remise_pct  NUMERIC(5,2) DEFAULT 0
);

-- ============================================
-- GÉNÉRATION DE ~5000 LIGNES DE VENTES
-- ============================================

INSERT INTO dw.fact_ventes (date_key, region_key, produit_key, client_key, canal_key, quantite, montant, cout, remise_pct)
SELECT
    TO_CHAR(
        '2023-01-01'::date + (random() * 730)::int,
        'YYYYMMDD'
    )::INTEGER as date_key,
    (1 + (random() * 7)::int) as region_key,
    (1 + (random() * 15)::int) as produit_key,
    (1 + (random() * 9)::int) as client_key,
    (1 + (random() * 2)::int) as canal_key,
    (1 + (random() * 5)::int) as quantite,
    ROUND((10 + random() * 1500)::numeric, 2) as montant,
    ROUND((5 + random() * 800)::numeric, 2) as cout,
    CASE WHEN random() < 0.3 THEN ROUND((random() * 20)::numeric, 2) ELSE 0 END as remise_pct
FROM generate_series(1, 5000);

-- Vérification
SELECT 'dim_date' as table_name, COUNT(*) as nb_rows FROM dw.dim_date
UNION ALL SELECT 'dim_region', COUNT(*) FROM dw.dim_region
UNION ALL SELECT 'dim_produit', COUNT(*) FROM dw.dim_produit
UNION ALL SELECT 'dim_client', COUNT(*) FROM dw.dim_client
UNION ALL SELECT 'dim_canal', COUNT(*) FROM dw.dim_canal
UNION ALL SELECT 'fact_ventes', COUNT(*) FROM dw.fact_ventes;
```

---

## Exercice 1 : ROLLUP - Sous-totaux hiérarchiques (30 min)

`ROLLUP` produit des sous-totaux en suivant la hiérarchie des colonnes spécifiées (de droite à gauche).

### 1.1 : ROLLUP simple

Écrivez une requête qui affiche le **CA par catégorie et sous-catégorie**, avec des sous-totaux par catégorie et un total général.

```sql
-- Résultat attendu :
-- Beauté        | Parfums          | xxxxx
-- Beauté        | Soins            | xxxxx
-- Beauté        | (sous-total)     | xxxxx   ← sous-total catégorie
-- Électronique  | Audio            | xxxxx
-- Électronique  | Ordinateurs      | xxxxx
-- ...
-- (total général)|                  | xxxxx   ← total général

SELECT
    _______ as categorie,
    _______ as sous_categorie,
    SUM(v.montant) as ca
FROM dw.fact_ventes v
JOIN dw.dim_produit p ON v.produit_key = p.produit_key
GROUP BY ROLLUP(_______, _______)
ORDER BY _______;
```

### 1.2 : ROLLUP géographique

CA par **pays > région > ville** avec sous-totaux à chaque niveau.

```sql
-- À compléter : ROLLUP sur la hiérarchie géographique
```

### 1.3 : ROLLUP temporel

CA par **année > trimestre > mois** avec sous-totaux.

```sql
-- À compléter : ROLLUP sur la hiérarchie temporelle
-- Utilisez la dimension date pour les libellés (nom_mois, etc.)
```

### 1.4 : GROUPING() pour identifier les niveaux

Reprenez la requête 1.1 et ajoutez `GROUPING()` pour distinguer les lignes de détail des sous-totaux :

```sql
SELECT
    CASE WHEN GROUPING(p.categorie) = 1 THEN '*** TOTAL GÉNÉRAL ***'
         ELSE p.categorie END as categorie,
    CASE WHEN GROUPING(p.sous_categorie) = 1 THEN '** Sous-total **'
         ELSE p.sous_categorie END as sous_categorie,
    SUM(v.montant) as ca,
    GROUPING(p.categorie) as is_total_general,
    GROUPING(p.sous_categorie) as is_sous_total
FROM dw.fact_ventes v
JOIN dw.dim_produit p ON v.produit_key = p.produit_key
GROUP BY ROLLUP(p.categorie, p.sous_categorie)
ORDER BY p.categorie NULLS LAST, p.sous_categorie NULLS LAST;
```

**Question :** Quelle est la différence entre un NULL "naturel" dans les données et un NULL généré par ROLLUP ? Comment `GROUPING()` aide-t-il ?

---

## Exercice 2 : CUBE - Toutes les combinaisons (20 min)

`CUBE` génère les agrégations pour **toutes les combinaisons** possibles des colonnes spécifiées.

### 2.1 : CUBE sur 2 dimensions

CA par **catégorie x canal**, avec toutes les combinaisons :

```sql
-- Résultat attendu :
-- Beauté       | Magasin           | xxxx
-- Beauté       | Site Web          | xxxx
-- Beauté       | App Mobile        | xxxx
-- Beauté       | (tous canaux)     | xxxx  ← sous-total catégorie
-- ...
-- (toutes cat) | Magasin           | xxxx  ← sous-total canal
-- (toutes cat) | (tous canaux)     | xxxx  ← total général

-- À compléter
SELECT
    _______,
    _______,
    SUM(v.montant) as ca,
    COUNT(*) as nb_transactions
FROM dw.fact_ventes v
JOIN dw.dim_produit p ON _______
JOIN dw.dim_canal c ON _______
GROUP BY CUBE(_______, _______)
ORDER BY _______;
```

### 2.2 : Comparaison ROLLUP vs CUBE

**Question :** Pour 3 colonnes (A, B, C), combien de groupes d'agrégation produit `ROLLUP(A, B, C)` ? Et `CUBE(A, B, C)` ? Listez-les.

| ROLLUP(A, B, C) | CUBE(A, B, C) |
|------------------|---------------|
| (A, B, C) | (A, B, C) |
| (A, B) | ? |
| ? | ? |
| ? | ? |
| | ? |
| | ? |
| | ? |
| | ? |

---

## Exercice 3 : GROUPING SETS - Combinaisons personnalisées (20 min)

`GROUPING SETS` permet de spécifier exactement quels regroupements on veut.

### 3.1 : Sets personnalisés

Créez une seule requête qui produit :
- CA par catégorie de produit
- CA par canal de vente
- CA par segment client
- CA total

```sql
SELECT
    p.categorie,
    c.canal,
    cl.segment,
    SUM(v.montant) as ca,
    COUNT(*) as nb_transactions
FROM dw.fact_ventes v
JOIN dw.dim_produit p ON v.produit_key = p.produit_key
JOIN dw.dim_canal c ON v.canal_key = c.canal_key
JOIN dw.dim_client cl ON v.client_key = cl.client_key
GROUP BY GROUPING SETS (
    (_______),       -- par catégorie
    (_______),       -- par canal
    (_______),       -- par segment
    ()               -- total général
);
```

### 3.2 : Rapport croisé

Créez une requête avec `GROUPING SETS` qui produit :
- CA par (catégorie, trimestre) - pour l'analyse saisonnière
- CA par (région, trimestre) - pour l'analyse géographique
- CA par trimestre seul - pour la tendance globale

---

## Exercice 4 : Fonctions de fenêtrage (Window Functions) (45 min)

Les fonctions de fenêtrage calculent des valeurs sur un ensemble de lignes **sans réduire** le nombre de lignes dans le résultat.

### 4.1 : Classement (RANK, DENSE_RANK, ROW_NUMBER)

**Top 3 produits par catégorie** (par CA) :

```sql
-- À compléter
SELECT * FROM (
    SELECT
        p.categorie,
        p.nom_produit,
        SUM(v.montant) as ca,
        RANK() OVER (
            PARTITION BY _______
            ORDER BY _______
        ) as rang
    FROM dw.fact_ventes v
    JOIN dw.dim_produit p ON v.produit_key = p.produit_key
    GROUP BY p.categorie, p.nom_produit
) ranked
WHERE rang <= 3;
```

**Question :** Quelle est la différence entre `RANK()`, `DENSE_RANK()` et `ROW_NUMBER()` quand des valeurs sont ex aequo ?

### 4.2 : Comparaison temporelle (LAG, LEAD)

**Évolution du CA mensuel** avec le delta par rapport au mois précédent :

```sql
SELECT
    d.annee,
    d.mois,
    d.nom_mois,
    SUM(v.montant) as ca_mensuel,
    LAG(SUM(v.montant)) OVER (ORDER BY d.annee, d.mois) as ca_mois_precedent,
    -- À compléter : calculez le delta en % (croissance)
    _______ as croissance_pct
FROM dw.fact_ventes v
JOIN dw.dim_date d ON v.date_key = d.date_key
GROUP BY d.annee, d.mois, d.nom_mois
ORDER BY d.annee, d.mois;
```

### 4.3 : Cumul (Running Total)

**CA cumulé** par mois pour chaque année :

```sql
SELECT
    d.annee,
    d.mois,
    SUM(v.montant) as ca_mensuel,
    SUM(SUM(v.montant)) OVER (
        PARTITION BY _______
        ORDER BY _______
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) as ca_cumule
FROM dw.fact_ventes v
JOIN dw.dim_date d ON v.date_key = d.date_key
GROUP BY d.annee, d.mois
ORDER BY d.annee, d.mois;
```

### 4.4 : Moyenne mobile

**Moyenne mobile sur 3 mois** du CA :

```sql
SELECT
    d.annee,
    d.mois,
    SUM(v.montant) as ca_mensuel,
    AVG(SUM(v.montant)) OVER (
        ORDER BY d.annee, d.mois
        ROWS BETWEEN _______ AND _______
    ) as moyenne_mobile_3m
FROM dw.fact_ventes v
JOIN dw.dim_date d ON v.date_key = d.date_key
GROUP BY d.annee, d.mois
ORDER BY d.annee, d.mois;
```

### 4.5 : Part du total (Percent of Total)

**Part de chaque catégorie** dans le CA total par trimestre :

```sql
SELECT
    d.trimestre,
    d.annee,
    p.categorie,
    SUM(v.montant) as ca,
    -- CA total du trimestre (fenêtre sans ORDER BY)
    SUM(SUM(v.montant)) OVER (
        PARTITION BY _______
    ) as ca_total_trimestre,
    -- Pourcentage
    ROUND(
        SUM(v.montant) * 100.0 /
        SUM(SUM(v.montant)) OVER (PARTITION BY _______),
        2
    ) as pct_du_total
FROM dw.fact_ventes v
JOIN dw.dim_date d ON v.date_key = d.date_key
JOIN dw.dim_produit p ON v.produit_key = p.produit_key
GROUP BY d.annee, d.trimestre, p.categorie
ORDER BY d.annee, d.trimestre, ca DESC;
```

### 4.6 : NTILE - Segmentation en quartiles

**Segmenter les villes** en 4 groupes selon leur CA :

```sql
SELECT
    r.ville,
    SUM(v.montant) as ca_total,
    NTILE(4) OVER (ORDER BY SUM(v.montant) DESC) as quartile
    -- 1 = top performers, 4 = bottom performers
FROM dw.fact_ventes v
JOIN dw.dim_region r ON v.region_key = r.region_key
GROUP BY r.ville;
```

---

## Exercice 5 : Opérations OLAP en SQL (30 min)

### 5.1 : Slice

**Slice** sur la dimension Temps : CA par catégorie et région, uniquement pour le T1 2024.

```sql
-- À compléter
```

### 5.2 : Dice

**Dice** sur 3 dimensions : CA pour les catégories (Électronique, Vêtements), les canaux (Web, Mobile), en 2024.

```sql
-- À compléter
```

### 5.3 : Roll-up

Écrivez 3 requêtes montrant un roll-up progressif :
1. CA par ville, mois
2. CA par région, trimestre (roll-up géo + temps)
3. CA par pays, année (roll-up encore plus haut)

### 5.4 : Drill-down

À partir du CA annuel total, écrivez 3 requêtes de drill-down :
1. CA par trimestre
2. CA par trimestre et catégorie
3. CA par trimestre, catégorie et sous-catégorie

### 5.5 : Pivot

**Pivot** : Affichez le CA avec les **trimestres en colonnes** et les **catégories en lignes**.

```sql
-- Pivot avec CASE WHEN (méthode standard)
SELECT
    p.categorie,
    SUM(CASE WHEN d.trimestre = 1 THEN v.montant ELSE 0 END) as "T1",
    SUM(CASE WHEN d.trimestre = 2 THEN v.montant ELSE 0 END) as "T2",
    SUM(CASE WHEN d.trimestre = 3 THEN v.montant ELSE 0 END) as "T3",
    SUM(CASE WHEN d.trimestre = 4 THEN v.montant ELSE 0 END) as "T4",
    SUM(v.montant) as "Total"
FROM dw.fact_ventes v
JOIN dw.dim_date d ON v.date_key = d.date_key
JOIN dw.dim_produit p ON v.produit_key = p.produit_key
WHERE d.annee = 2024
GROUP BY p.categorie
ORDER BY "Total" DESC;
```

**Bonus :** Faites le même pivot avec les **canaux en colonnes** et les **régions en lignes**.

---

## Exercice 6 : Vues matérialisées (15 min)

Les vues matérialisées pré-calculent et stockent les résultats. C'est une forme de MOLAP dans PostgreSQL.

### 6.1 : Créer une vue matérialisée

```sql
-- Vue matérialisée : CA mensuel par catégorie et région
CREATE MATERIALIZED VIEW dw.mv_ca_mensuel AS
SELECT
    d.annee,
    d.mois,
    d.nom_mois,
    r.region,
    p.categorie,
    SUM(v.montant) as ca,
    COUNT(*) as nb_transactions,
    AVG(v.montant) as panier_moyen
FROM dw.fact_ventes v
JOIN dw.dim_date d ON v.date_key = d.date_key
JOIN dw.dim_region r ON v.region_key = r.region_key
JOIN dw.dim_produit p ON v.produit_key = p.produit_key
GROUP BY d.annee, d.mois, d.nom_mois, r.region, p.categorie;

-- Index pour la performance
CREATE INDEX idx_mv_annee_mois ON dw.mv_ca_mensuel(annee, mois);
```

### 6.2 : Requêter la vue matérialisée

Écrivez une requête sur `dw.mv_ca_mensuel` qui fait un ROLLUP par région et catégorie.

### 6.3 : Rafraîchir

```sql
-- Après insertion de nouvelles données
REFRESH MATERIALIZED VIEW dw.mv_ca_mensuel;

-- Rafraîchissement concurrent (sans bloquer les lectures)
REFRESH MATERIALIZED VIEW CONCURRENTLY dw.mv_ca_mensuel;
-- Nécessite un UNIQUE INDEX sur la vue
```

**Question :** Quel est l'avantage d'une vue matérialisée par rapport à une vue normale ? Quel est l'inconvénient ?

---

## Exercice 7 : Requête de synthèse (15 min)

Écrivez **une seule requête** qui produit un rapport de direction complet :

- CA par trimestre et par catégorie (2024)
- Avec le CA du même trimestre en 2023 (pour comparaison)
- Le taux de croissance en %
- Le rang de chaque catégorie par trimestre
- La part de chaque catégorie dans le total du trimestre

**Indice :** Combinez un `GROUP BY` avec `LAG()` (ou un self-join sur l'année), `RANK()` et une window function pour le pourcentage.

```sql
-- Requête de synthèse à écrire
-- Résultat attendu :
-- trim | categorie    | ca_2024 | ca_2023 | croiss_% | rang | part_%
-- T1   | Électronique | xxx     | xxx     | +xx%     | 1    | xx%
-- T1   | Maison       | xxx     | xxx     | +xx%     | 2    | xx%
-- ...
```

---

## Livrables attendus

1. **Script SQL complet** avec toutes les requêtes (setup + exercices 1 à 7)
2. **Réponses aux questions** intégrées dans les exercices (en commentaires SQL ou document séparé)
3. **Captures d'écran** des résultats des requêtes clés (exercices 5.5, 6.1, 7)

---

## Pour aller plus loin

- Comparez le temps d'exécution d'une requête avec et sans vue matérialisée (`EXPLAIN ANALYZE`)
- Testez l'extension `tablefunc` de PostgreSQL pour faire des pivots avec `crosstab()`
- Explorez `FILTER (WHERE ...)` comme alternative à `CASE WHEN` dans les agrégations

---

[Retour au sommaire](../cours/README.md)
