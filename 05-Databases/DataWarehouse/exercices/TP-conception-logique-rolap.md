# TP : Conception logique ROLAP

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 2h |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Prérequis** | [TD Conception conceptuelle](./TD-conception-conceptuelle.md), [Module 05 - Opérations OLAP](../cours/05-operations-olap.md) |
| **Outils** | PostgreSQL (local ou Docker) |
| **Livrables** | Scripts SQL DDL + DML + réponses aux questions |

## Objectifs

- Traduire un modèle conceptuel (étoile) en schéma logique ROLAP (tables SQL)
- Créer les tables dans PostgreSQL avec les types et contraintes appropriés
- Charger des données de test
- Valider le modèle avec des requêtes analytiques
- Comprendre les choix d'implémentation ROLAP

---

## Contexte

Vous reprenez le cas **CinéStar** du TD précédent. Votre modèle conceptuel est validé par la direction. Il faut maintenant l'implémenter dans PostgreSQL en approche **ROLAP** (les données restent dans des tables relationnelles, les agrégations sont calculées en SQL à la volée).

## Partie 1 : Création du schéma (45 min)

### 1.1 : Créer la base et les schémas

```sql
-- Créer la base de données
CREATE DATABASE cinestar_dw;

-- Se connecter à la base
\c cinestar_dw

-- Créer les schémas pour organiser les tables
CREATE SCHEMA dim;    -- Tables de dimensions
CREATE SCHEMA fact;   -- Tables de faits
CREATE SCHEMA staging; -- Zone temporaire pour le chargement
```

### 1.2 : Créer la dimension Date

La dimension Date est pré-fournie. Exécutez ce script :

```sql
CREATE TABLE dim.date (
    date_key        INTEGER PRIMARY KEY,       -- Format YYYYMMDD
    date_complete   DATE NOT NULL UNIQUE,
    jour            INTEGER NOT NULL,
    jour_semaine    VARCHAR(10) NOT NULL,       -- Lundi, Mardi...
    num_jour_semaine INTEGER NOT NULL,          -- 1=Lundi, 7=Dimanche
    est_weekend     BOOLEAN NOT NULL,
    semaine         INTEGER NOT NULL,
    mois            INTEGER NOT NULL,
    nom_mois        VARCHAR(10) NOT NULL,
    trimestre       INTEGER NOT NULL,
    annee           INTEGER NOT NULL,
    est_vacances    BOOLEAN DEFAULT FALSE,
    est_ferie       BOOLEAN DEFAULT FALSE
);

-- Générer les dates pour 2022-2025
INSERT INTO dim.date
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INTEGER as date_key,
    d as date_complete,
    EXTRACT(DAY FROM d)::INTEGER as jour,
    TO_CHAR(d, 'TMDay') as jour_semaine,
    EXTRACT(ISODOW FROM d)::INTEGER as num_jour_semaine,
    EXTRACT(ISODOW FROM d) IN (6, 7) as est_weekend,
    EXTRACT(WEEK FROM d)::INTEGER as semaine,
    EXTRACT(MONTH FROM d)::INTEGER as mois,
    TO_CHAR(d, 'TMMonth') as nom_mois,
    EXTRACT(QUARTER FROM d)::INTEGER as trimestre,
    EXTRACT(YEAR FROM d)::INTEGER as annee,
    FALSE as est_vacances,
    FALSE as est_ferie
FROM generate_series('2022-01-01'::date, '2025-12-31'::date, '1 day') as d;
```

### 1.3 : Créer la dimension Heure

```sql
CREATE TABLE dim.heure (
    heure_key       INTEGER PRIMARY KEY,     -- Format HHMM (0800, 1430...)
    heure           INTEGER NOT NULL,        -- 0-23
    minute          INTEGER NOT NULL,        -- 0, 15, 30, 45
    tranche_horaire VARCHAR(20) NOT NULL,    -- "Matinée", "Après-midi", "Soirée"
    est_heure_creuse BOOLEAN NOT NULL
);
```

**Exercice :** Insérez les créneaux horaires de séances (de 10h00 à 23h00, par tranche de 30 min). Définissez les tranches :
- 10h-14h → "Matinée"
- 14h-18h → "Après-midi"
- 18h-23h → "Soirée"

Heures creuses : Matinée en semaine.

### 1.4 : Créer les autres dimensions

**Exercice :** Créez les tables suivantes avec les types PostgreSQL appropriés, les clés surrogate, les clés naturelles et les contraintes.

**DIM_CINEMA :**

```sql
CREATE TABLE dim.cinema (
    cinema_key      SERIAL PRIMARY KEY,
    cinema_id       VARCHAR(10) NOT NULL,    -- Clé naturelle
    nom             VARCHAR(100) NOT NULL,
    ville           VARCHAR(50) NOT NULL,
    region          VARCHAR(50) NOT NULL,
    nb_salles       INTEGER NOT NULL,
    type_salle_principal VARCHAR(20),        -- Standard, IMAX, Premium
    -- SCD Type 1 : on écrase
    directeur       VARCHAR(100),
    -- Metadata
    date_chargement TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**A vous de créer :**

- `dim.film` - avec : film_key (SERIAL PK), film_id, titre, realisateur, genre, duree_min, pays_origine, distributeur, date_sortie, classification, budget_millions
- `dim.client` - avec SCD Type 2 (valid_from, valid_to, is_current) : client_key, client_id, nom, prenom, ville, region, carte_fidelite, segment (Fidèle/Occasionnel/Nouveau)
- `dim.tarif` - avec : tarif_key (PK), type_tarif (Plein/Réduit/Étudiant/Senior/Enfant), canal_achat (Guichet/Web/Appli), description

### 1.5 : Créer la table de faits

**Exercice :** Créez la table `fact.billetterie` avec :

- Toutes les FK vers les dimensions (avec REFERENCES)
- Les mesures : prix_paye (NUMERIC), nb_billets (INTEGER, toujours 1 au grain billet), nb_places_salle (INTEGER, pour le taux de remplissage)
- Pensez au partitionnement PostgreSQL

```sql
-- Structure à compléter
CREATE TABLE fact.billetterie (
    billet_id       BIGSERIAL,
    -- FK dimensions (à compléter)
    date_key        INTEGER NOT NULL REFERENCES dim.date(date_key),
    __________      _______ NOT NULL REFERENCES dim._______(___________),
    __________      _______ NOT NULL REFERENCES dim._______(___________),
    __________      _______ NOT NULL REFERENCES dim._______(___________),
    __________      _______ NOT NULL REFERENCES dim._______(___________),
    -- Mesures (à compléter)
    prix_paye       NUMERIC(8,2) NOT NULL,
    __________      ___________,
    __________      ___________
) PARTITION BY RANGE (date_key);

-- Créer les partitions par année
CREATE TABLE fact.billetterie_2022 PARTITION OF fact.billetterie
    FOR VALUES FROM (20220101) TO (20230101);
CREATE TABLE fact.billetterie_2023 PARTITION OF fact.billetterie
    FOR VALUES FROM (20230101) TO (20240101);
CREATE TABLE fact.billetterie_2024 PARTITION OF fact.billetterie
    FOR VALUES FROM (20240101) TO (20250101);
```

---

## Partie 2 : Chargement des données de test (30 min)

### 2.1 : Données de référence

Insérez des données de test dans les dimensions :

```sql
-- Cinémas (5 cinémas pour le test)
INSERT INTO dim.cinema (cinema_id, nom, ville, region, nb_salles, type_salle_principal, directeur)
VALUES
    ('CIN001', 'CinéStar Opéra', 'Paris', 'Île-de-France', 12, 'IMAX', 'Marie Laurent'),
    ('CIN002', 'CinéStar Bellecour', 'Lyon', 'Auvergne-Rhône-Alpes', 8, 'Standard', 'Jean Dupont'),
    ('CIN003', 'CinéStar Vieux-Port', 'Marseille', 'PACA', 10, 'Premium', 'Sophie Martin'),
    ('CIN004', 'CinéStar Capitole', 'Toulouse', 'Occitanie', 6, 'Standard', 'Pierre Moreau'),
    ('CIN005', 'CinéStar République', 'Paris', 'Île-de-France', 8, '3D', 'Anne Petit');

-- Films (10 films)
-- EXERCICE : Insérez 10 films variés (genres, pays, distributeurs différents)
-- Incluez au moins : 1 film d'action, 1 comédie, 1 drame, 1 animation, 1 SF

-- Clients (20 clients)
-- EXERCICE : Insérez 20 clients avec des profils variés
-- (villes différentes, avec/sans carte fidélité, segments variés)

-- Tarifs
INSERT INTO dim.tarif (tarif_key, type_tarif, canal_achat, description)
VALUES
    (1, 'Plein', 'Guichet', 'Tarif plein guichet'),
    (2, 'Plein', 'Web', 'Tarif plein en ligne'),
    (3, 'Plein', 'Appli', 'Tarif plein application'),
    (4, 'Réduit', 'Guichet', 'Tarif réduit guichet'),
    (5, 'Réduit', 'Web', 'Tarif réduit en ligne'),
    (6, 'Étudiant', 'Guichet', 'Tarif étudiant guichet'),
    (7, 'Étudiant', 'Web', 'Tarif étudiant en ligne'),
    (8, 'Senior', 'Guichet', 'Tarif senior guichet'),
    (9, 'Enfant', 'Guichet', 'Tarif enfant guichet'),
    (10, 'Enfant', 'Web', 'Tarif enfant en ligne');
```

### 2.2 : Générer des faits de test

**Exercice :** Écrivez une requête INSERT qui génère ~1000 lignes de billets de test en croisant aléatoirement les dimensions existantes.

**Indice :** Utilisez `generate_series`, `random()` et des sous-requêtes pour piocher aléatoirement dans les dimensions.

```sql
-- Aide : génération de données aléatoires en PostgreSQL
INSERT INTO fact.billetterie (date_key, heure_key, cinema_key, film_key, client_key, tarif_key, prix_paye, nb_places_salle)
SELECT
    -- Date aléatoire en 2024
    TO_CHAR('2024-01-01'::date + (random() * 365)::int, 'YYYYMMDD')::INTEGER,
    -- Heure : à compléter
    ___,
    -- Cinema : à compléter (aléatoire parmi les existants)
    ___,
    -- Film : à compléter
    ___,
    -- Client : à compléter
    ___,
    -- Tarif : à compléter
    ___,
    -- Prix : entre 5€ et 15€
    ROUND((5 + random() * 10)::numeric, 2),
    -- Nb places salle : selon le cinéma (simplification)
    200
FROM generate_series(1, 1000);
```

---

## Partie 3 : Validation par les requêtes (45 min)

Validez votre modèle en écrivant les requêtes qui répondent aux questions business.

### 3.1 : Requêtes de base

**Exercice :** Écrivez les requêtes SQL pour :

1. **CA par cinéma et par mois** (avec le nom du mois)

```sql
-- À compléter
SELECT
    c.nom as cinema,
    d.nom_mois,
    d.annee,
    SUM(f.prix_paye) as chiffre_affaires,
    COUNT(*) as nb_billets
FROM fact.billetterie f
JOIN dim.cinema c ON f.cinema_key = c.cinema_key
JOIN dim.date d ON f.date_key = d.date_key
GROUP BY ______
ORDER BY ______;
```

2. **Taux de remplissage moyen par cinéma**

```sql
-- Indice : taux = nb_billets_vendus / nb_places_salle pour une séance
-- Simplification : on considère que chaque combinaison (date, heure, cinema, film)
-- est une séance distincte
-- À compléter
```

3. **Top 5 films par chiffre d'affaires**

4. **Répartition des tarifs** (pourcentage de chaque type)

5. **CA par canal d'achat** (guichet, web, appli)

### 3.2 : Requêtes avec opérations OLAP

**Exercice :** Utilisez les fonctions OLAP de PostgreSQL :

6. **CA avec sous-totaux** par région et cinéma (utiliser `ROLLUP`)

```sql
SELECT
    COALESCE(c.region, 'TOTAL') as region,
    COALESCE(c.nom, 'Sous-total') as cinema,
    SUM(f.prix_paye) as ca
FROM fact.billetterie f
JOIN dim.cinema c ON f.cinema_key = c.cinema_key
GROUP BY ROLLUP(c.region, c.nom)
ORDER BY c.region NULLS LAST, c.nom NULLS LAST;
```

7. **Toutes les combinaisons** région x trimestre (utiliser `CUBE`)

8. **Analyse par GROUPING SETS** : CA par (genre film), par (type tarif), et total

### 3.3 : Requêtes avec fonctions fenêtres

9. **Classement des cinémas** par CA mensuel (utiliser `RANK()`)

```sql
SELECT
    c.nom as cinema,
    d.mois,
    SUM(f.prix_paye) as ca_mensuel,
    RANK() OVER (PARTITION BY d.mois ORDER BY SUM(f.prix_paye) DESC) as rang
FROM fact.billetterie f
JOIN dim.cinema c ON f.cinema_key = c.cinema_key
JOIN dim.date d ON f.date_key = d.date_key
WHERE d.annee = 2024
GROUP BY c.nom, d.mois;
```

10. **Évolution du CA** mois par mois avec le delta vs mois précédent (utiliser `LAG()`)

11. **Cumul du CA** par cinéma au fil des mois (utiliser `SUM() OVER`)

12. **Part de chaque cinéma** dans le CA total mensuel en % (utiliser `SUM() OVER ()`)

---

## Partie 4 : Réflexion sur le modèle (15 min)

Répondez à ces questions :

1. Pourquoi utilise-t-on des **clés surrogate** (SERIAL) plutôt que les clés naturelles (cinema_id, film_id) dans la table de faits ?

2. Quel est l'avantage du **partitionnement** de la table de faits par date_key ?

3. Si CinéStar veut analyser les ventes de **confiserie au bar**, comment adapteriez-vous le modèle ? (nouvelle table de faits ? nouvelle dimension ?)

4. Pourquoi cette implémentation est-elle qualifiée de **ROLAP** et non MOLAP ?

---

## Livrables attendus

1. **Scripts DDL** complets (CREATE TABLE) pour toutes les tables
2. **Scripts DML** d'insertion des données de test
3. **12 requêtes SQL** répondant aux questions 1-12
4. **Réponses** aux 4 questions de réflexion (Partie 4)

---

[Retour au sommaire](../cours/README.md)
