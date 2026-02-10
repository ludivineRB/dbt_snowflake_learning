[← Precedent](04-modele-logique-mld.md) | [🏠 Accueil](README.md) | [Suivant →](06-outils-pratiques.md)

---

# 05 - Le Modele Physique de Donnees (MPD)

## 🎯 Objectifs de cette lecon

- Savoir transformer un MLD en scripts SQL DDL executables
- Choisir les types de donnees adaptes a chaque attribut
- Maitriser les contraintes SQL : PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK, DEFAULT
- Comprendre les strategies d'indexation (B-tree, Hash, composite)
- Connaitre les strategies de partitionnement pour les grandes tables
- Appliquer les bonnes pratiques de nommage
- Connaitre les differences entre PostgreSQL, MySQL et SQL Server

---

## 1. Du MLD au SQL DDL

### 1.1 Le DDL (Data Definition Language)

Le MPD est la traduction concrete du MLD en instructions SQL. Le DDL regroupe les commandes qui **definissent la structure** de la base :

| Commande | Role |
|----------|------|
| `CREATE TABLE` | Creer une table |
| `ALTER TABLE` | Modifier une table existante |
| `DROP TABLE` | Supprimer une table |
| `CREATE INDEX` | Creer un index |
| `CREATE SCHEMA` | Creer un schema (namespace) |

### 1.2 Ordre de creation des tables

⚠️ **Important** : les tables referencees par des cles etrangeres doivent etre creees **avant** les tables qui les referencent.

```
Ordre pour notre exemple e-commerce :

1. CATEGORIE     (pas de FK, aucune dependance)
2. CLIENT        (pas de FK, aucune dependance)
3. PRODUIT       (FK vers CATEGORIE → doit etre apres CATEGORIE)
4. COMMANDE      (FK vers CLIENT → doit etre apres CLIENT)
5. LIGNE_COMMANDE (FK vers COMMANDE et PRODUIT → doit etre en dernier)
```

Pour la suppression, c'est l'**ordre inverse** :

```sql
-- Suppression (ordre inverse de la creation)
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS produit;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS client;
```

---

## 2. Choisir les types de donnees

### 2.1 Types numeriques

| Type | Taille | Plage | Usage |
|------|--------|-------|-------|
| `SMALLINT` | 2 octets | -32 768 a 32 767 | Quantites faibles, codes |
| `INT` / `INTEGER` | 4 octets | -2.1 milliards a 2.1 milliards | Identifiants, compteurs |
| `BIGINT` | 8 octets | ± 9.2 x 10^18 | Identifiants IoT, gros volumes |
| `SERIAL` | 4 octets | Auto-incremente (PostgreSQL) | PK auto-incrementee |
| `BIGSERIAL` | 8 octets | Auto-incremente grand (PostgreSQL) | PK gros volume |
| `DECIMAL(p,s)` | Variable | Precision exacte | Montants financiers |
| `FLOAT` / `REAL` | 4 octets | Precision approchee | Mesures scientifiques |
| `DOUBLE PRECISION` | 8 octets | Precision approchee double | Calculs scientifiques |

💡 **Regle d'or** : utilisez `DECIMAL` pour tout ce qui touche a l'argent. `FLOAT` introduit des erreurs d'arrondi.

```sql
-- ❌ MAUVAIS : FLOAT pour des montants financiers
prix FLOAT  -- 19.99 peut devenir 19.990000000000002

-- ✅ CORRECT : DECIMAL pour des montants financiers
prix DECIMAL(10,2)  -- 19.99 reste 19.99
```

### 2.2 Types texte

| Type | Description | Usage |
|------|-------------|-------|
| `CHAR(n)` | Longueur fixe (padde avec des espaces) | Codes ISO (FR, US), codes fixes |
| `VARCHAR(n)` | Longueur variable, max n caracteres | Noms, emails, descriptions courtes |
| `TEXT` | Longueur illimitee | Descriptions longues, commentaires |

💡 **Conseil** : preferez `VARCHAR(n)` avec une taille adaptee. `TEXT` est pratique mais ne permet pas de valider la taille.

```sql
-- ✅ Bonnes pratiques de dimensionnement
nom             VARCHAR(100),    -- Un nom depasse rarement 100 caracteres
email           VARCHAR(255),    -- Standard RFC 5321
code_postal     CHAR(5),         -- Toujours 5 caracteres en France
description     TEXT,            -- Longueur imprevisible
statut          VARCHAR(20),     -- Valeurs enumerees courtes
```

### 2.3 Types date et heure

| Type | Contenu | Exemple | Usage |
|------|---------|---------|-------|
| `DATE` | Date seule | 2024-01-15 | Date de naissance, date d'embauche |
| `TIME` | Heure seule | 14:30:00 | Horaires |
| `TIMESTAMP` | Date + heure | 2024-01-15 14:30:00 | Horodatage d'evenements |
| `TIMESTAMP WITH TIME ZONE` | Date + heure + fuseau | 2024-01-15 14:30:00+01 | Systemes multi-fuseaux |
| `INTERVAL` | Duree | 3 hours 30 minutes | Calculs de durees |

💡 **Pour le Data Engineer** : utilisez TOUJOURS `TIMESTAMP WITH TIME ZONE` pour les horodatages dans un contexte distribue (pipelines multi-regions, IoT). Les problemes de fuseaux horaires sont la cause n°1 de bugs dans les pipelines de donnees.

```sql
-- ❌ Sans fuseau horaire : ambiguite si les serveurs sont dans des fuseaux differents
date_mesure TIMESTAMP  -- 14:30:00 = heure de Paris ? De New York ?

-- ✅ Avec fuseau horaire : pas d'ambiguite
date_mesure TIMESTAMP WITH TIME ZONE  -- 14:30:00+01:00 = Paris, sans ambiguite
```

### 2.4 Types booleens et autres

| Type | Description | Usage |
|------|-------------|-------|
| `BOOLEAN` | TRUE / FALSE / NULL | Flags, indicateurs |
| `UUID` | Identifiant universellement unique | PK distribuees, API |
| `JSON` / `JSONB` | Donnees semi-structurees | Metadonnees, config (PostgreSQL) |
| `BYTEA` | Donnees binaires | Fichiers (preferer le stockage externe) |
| `ENUM` | Valeur parmi une liste | Statuts, types (MySQL) |

---

## 3. Les contraintes SQL

### 3.1 PRIMARY KEY

La cle primaire identifie de maniere unique chaque ligne. Elle implique automatiquement NOT NULL et UNIQUE.

```sql
-- PK simple
CREATE TABLE client (
    id_client SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);

-- PK composee
CREATE TABLE ligne_commande (
    id_commande INT,
    id_produit INT,
    quantite INT NOT NULL,
    PRIMARY KEY (id_commande, id_produit)
);
```

### 3.2 FOREIGN KEY

La cle etrangere assure l'**integrite referentielle** : on ne peut pas referencer une ligne qui n'existe pas.

```sql
CREATE TABLE commande (
    id_commande SERIAL PRIMARY KEY,
    date_commande TIMESTAMP NOT NULL DEFAULT NOW(),
    statut VARCHAR(20) NOT NULL DEFAULT 'en_attente',
    montant_total DECIMAL(10,2) NOT NULL,
    id_client INT NOT NULL,

    -- Cle etrangere avec actions en cascade
    CONSTRAINT fk_commande_client
        FOREIGN KEY (id_client)
        REFERENCES client(id_client)
        ON DELETE RESTRICT      -- Empeche la suppression d'un client ayant des commandes
        ON UPDATE CASCADE       -- Met a jour la FK si l'id_client change
);
```

**Actions de reference :**

| Action | Comportement |
|--------|-------------|
| `CASCADE` | Supprime/modifie automatiquement les lignes dependantes |
| `RESTRICT` | Empeche la suppression/modification si des dependances existent |
| `SET NULL` | Met la FK a NULL (si autorise) |
| `SET DEFAULT` | Met la FK a sa valeur par defaut |
| `NO ACTION` | Similaire a RESTRICT (verification differee possible) |

💡 **Bonne pratique** : utilisez `RESTRICT` par defaut pour les FK. `CASCADE` est dangereux car une suppression peut se propager en chaine.

### 3.3 NOT NULL

Empeche les valeurs NULL. A utiliser pour tous les champs obligatoires.

```sql
-- Coherence avec le dictionnaire de donnees :
-- Si "Obligatoire = Oui" → NOT NULL
-- Si "Obligatoire = Non" → pas de NOT NULL (ou explicitement NULL)

nom         VARCHAR(100)  NOT NULL,   -- Obligatoire
telephone   VARCHAR(20),              -- Facultatif (NULL autorise)
```

### 3.4 UNIQUE

Empeche les doublons sur une ou plusieurs colonnes.

```sql
-- UNIQUE simple
email VARCHAR(255) NOT NULL UNIQUE,

-- UNIQUE composee (combinaison unique)
CONSTRAINT uk_capteur_zone UNIQUE (numero_serie, id_zone)
```

### 3.5 CHECK

Valide qu'une valeur respecte une condition.

```sql
-- Exemples de CHECK
statut VARCHAR(20) NOT NULL
    CHECK (statut IN ('en_attente', 'validee', 'expediee', 'livree', 'annulee')),

prix_unitaire DECIMAL(10,2) NOT NULL
    CHECK (prix_unitaire > 0),

quantite INT NOT NULL
    CHECK (quantite >= 1),

date_fin DATE
    CHECK (date_fin > date_debut),

-- CHECK avec nom de contrainte (recommande)
CONSTRAINT chk_commande_montant CHECK (montant_total >= 0)
```

### 3.6 DEFAULT

Definit une valeur par defaut si aucune n'est specifiee lors de l'insertion.

```sql
date_inscription    TIMESTAMP   NOT NULL DEFAULT NOW(),
statut              VARCHAR(20) NOT NULL DEFAULT 'en_attente',
est_actif           BOOLEAN     NOT NULL DEFAULT TRUE,
stock_disponible    INT         NOT NULL DEFAULT 0,
pays                VARCHAR(50) NOT NULL DEFAULT 'France'
```

---

## 4. Les index

### 4.1 Pourquoi indexer ?

Un index accelere les recherches en creant une structure de donnees optimisee (comme l'index d'un livre). Sans index, le SGBD doit scanner **toutes les lignes** (full table scan).

```
Sans index : Rechercher "Dupont" parmi 1 million de clients → scan de 1M lignes
Avec index : Rechercher "Dupont" parmi 1 million de clients → ~20 operations (B-tree)
```

### 4.2 Types d'index

| Type | Structure | Usage | Ideal pour |
|------|-----------|-------|-----------|
| **B-tree** | Arbre equilibre | Par defaut | `=`, `<`, `>`, `BETWEEN`, `ORDER BY` |
| **Hash** | Table de hachage | Egalite stricte | `=` uniquement |
| **GIN** | Generalised Inverted | Recherche plein texte | `LIKE '%mot%'`, JSON, arrays |
| **BRIN** | Block Range | Donnees physiquement ordonnees | Series temporelles, logs |
| **GiST** | Generalised Search Tree | Donnees spatiales | PostGIS, geometrie |

### 4.3 Quand creer un index ?

✅ **Indexez** :
- Les colonnes utilisees dans les `WHERE` frequents
- Les colonnes utilisees dans les `JOIN` (les FK)
- Les colonnes utilisees dans les `ORDER BY` frequents
- Les colonnes avec une haute cardinalite (beaucoup de valeurs distinctes)

❌ **N'indexez PAS** :
- Les petites tables (< 1000 lignes)
- Les colonnes avec peu de valeurs distinctes (booleen, statut avec 3 valeurs)
- Les tables en ecriture intensive (chaque INSERT met a jour les index)

### 4.4 Exemples de creation d'index

```sql
-- Index simple (B-tree par defaut)
CREATE INDEX idx_client_email ON client(email);

-- Index composite (pour les requetes filtrant sur plusieurs colonnes)
CREATE INDEX idx_commande_client_date ON commande(id_client, date_commande);

-- Index unique (combine index + contrainte d'unicite)
CREATE UNIQUE INDEX idx_client_email_unique ON client(email);

-- Index partiel (indexe seulement un sous-ensemble de lignes)
CREATE INDEX idx_commande_en_attente
    ON commande(date_commande)
    WHERE statut = 'en_attente';

-- Index BRIN pour les series temporelles (IoT)
CREATE INDEX idx_mesure_date_brin
    ON mesure USING BRIN(date_mesure);

-- Index pour la recherche plein texte (PostgreSQL)
CREATE INDEX idx_produit_nom_gin
    ON produit USING GIN(to_tsvector('french', nom_produit));
```

💡 **Pour le Data Engineer** : sur les tables de mesures IoT avec des millions de lignes, l'index BRIN sur la colonne `date_mesure` est extremement efficace car les donnees arrivent chronologiquement.

### 4.5 Index composite : l'ordre compte

```sql
-- Cet index est efficace pour :
CREATE INDEX idx_commande_client_date ON commande(id_client, date_commande);

-- ✅ WHERE id_client = 42
-- ✅ WHERE id_client = 42 AND date_commande > '2024-01-01'
-- ❌ WHERE date_commande > '2024-01-01'  (colonne pas en premier)

-- Regle : l'index est utilisable pour les colonnes de GAUCHE a DROITE
```

---

## 5. Le partitionnement

### 5.1 Pourquoi partitionner ?

Le partitionnement divise une grande table en **sous-tables** (partitions) plus petites et plus faciles a gerer.

| Avantage | Description |
|----------|-------------|
| **Performance** | Les requetes ne scannent que les partitions pertinentes |
| **Maintenance** | On peut archiver/supprimer une partition entiere (pas de DELETE massif) |
| **Stockage** | Chaque partition peut etre sur un disque different |
| **Parallelisme** | Les partitions peuvent etre traitees en parallele |

### 5.2 Strategies de partitionnement

**Par intervalle (RANGE)** - Le plus courant pour les series temporelles :

```sql
-- Partitionnement par mois (PostgreSQL)
CREATE TABLE mesure (
    id_mesure       BIGSERIAL,
    id_capteur      INT NOT NULL,
    valeur_mesuree  DECIMAL(10,4) NOT NULL,
    date_mesure     TIMESTAMP WITH TIME ZONE NOT NULL,
    est_valide      BOOLEAN NOT NULL DEFAULT TRUE
) PARTITION BY RANGE (date_mesure);

-- Creation des partitions mensuelles
CREATE TABLE mesure_2024_01 PARTITION OF mesure
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE mesure_2024_02 PARTITION OF mesure
    FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

CREATE TABLE mesure_2024_03 PARTITION OF mesure
    FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');
-- etc.
```

**Par liste (LIST)** - Pour des valeurs discretes :

```sql
-- Partitionnement par region
CREATE TABLE commande (
    id_commande     SERIAL,
    id_client       INT NOT NULL,
    date_commande   TIMESTAMP NOT NULL,
    region          VARCHAR(20) NOT NULL
) PARTITION BY LIST (region);

CREATE TABLE commande_europe PARTITION OF commande
    FOR VALUES IN ('FR', 'DE', 'ES', 'IT', 'UK');

CREATE TABLE commande_amerique PARTITION OF commande
    FOR VALUES IN ('US', 'CA', 'BR', 'MX');

CREATE TABLE commande_asie PARTITION OF commande
    FOR VALUES IN ('CN', 'JP', 'KR', 'IN');
```

**Par hachage (HASH)** - Pour distribuer uniformement :

```sql
-- Partitionnement par hash (distribution uniforme)
CREATE TABLE log_evenement (
    id_event    BIGSERIAL,
    id_user     INT NOT NULL,
    action      VARCHAR(100) NOT NULL,
    date_event  TIMESTAMP NOT NULL
) PARTITION BY HASH (id_user);

CREATE TABLE log_evenement_0 PARTITION OF log_evenement
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE log_evenement_1 PARTITION OF log_evenement
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE log_evenement_2 PARTITION OF log_evenement
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE log_evenement_3 PARTITION OF log_evenement
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

---

## 6. Scripts SQL complets : exemple E-commerce

### 6.1 Creation du schema

```sql
-- =============================================================
-- MPD - Plateforme E-commerce
-- SGBD : PostgreSQL 15+
-- Date : 2024
-- Auteur : Formation Data Engineer
-- =============================================================

-- Schema dedie (bonne pratique)
CREATE SCHEMA IF NOT EXISTS ecommerce;
SET search_path TO ecommerce;

-- =============================================================
-- TABLE : categorie
-- Description : Categories de produits
-- =============================================================
CREATE TABLE categorie (
    id_categorie        SERIAL          PRIMARY KEY,
    nom_categorie       VARCHAR(100)    NOT NULL,
    description_categorie TEXT,
    date_creation       TIMESTAMP       NOT NULL DEFAULT NOW(),

    -- Contraintes
    CONSTRAINT uk_categorie_nom UNIQUE (nom_categorie)
);

COMMENT ON TABLE categorie IS 'Categories de produits du catalogue';
COMMENT ON COLUMN categorie.nom_categorie IS 'Nom unique de la categorie';

-- =============================================================
-- TABLE : client
-- Description : Clients inscrits sur la plateforme
-- =============================================================
CREATE TABLE client (
    id_client           SERIAL          PRIMARY KEY,
    nom                 VARCHAR(100)    NOT NULL,
    prenom              VARCHAR(100)    NOT NULL,
    email               VARCHAR(255)    NOT NULL,
    telephone           VARCHAR(20),
    date_inscription    TIMESTAMP       NOT NULL DEFAULT NOW(),
    est_actif           BOOLEAN         NOT NULL DEFAULT TRUE,

    -- Contraintes
    CONSTRAINT uk_client_email UNIQUE (email),
    CONSTRAINT chk_client_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

COMMENT ON TABLE client IS 'Clients inscrits sur la plateforme e-commerce';
COMMENT ON COLUMN client.email IS 'Adresse email unique du client';
COMMENT ON COLUMN client.est_actif IS 'Indique si le compte client est actif';

-- =============================================================
-- TABLE : produit
-- Description : Catalogue de produits
-- =============================================================
CREATE TABLE produit (
    id_produit          SERIAL          PRIMARY KEY,
    nom_produit         VARCHAR(200)    NOT NULL,
    description         TEXT,
    prix_unitaire       DECIMAL(10,2)   NOT NULL,
    stock_disponible    INT             NOT NULL DEFAULT 0,
    date_creation       TIMESTAMP       NOT NULL DEFAULT NOW(),
    est_actif           BOOLEAN         NOT NULL DEFAULT TRUE,
    id_categorie        INT             NOT NULL,

    -- Contraintes
    CONSTRAINT fk_produit_categorie
        FOREIGN KEY (id_categorie)
        REFERENCES categorie(id_categorie)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_produit_prix CHECK (prix_unitaire > 0),
    CONSTRAINT chk_produit_stock CHECK (stock_disponible >= 0)
);

COMMENT ON TABLE produit IS 'Catalogue des produits disponibles';
COMMENT ON COLUMN produit.prix_unitaire IS 'Prix unitaire HT courant du produit';
COMMENT ON COLUMN produit.stock_disponible IS 'Quantite disponible en stock';

-- =============================================================
-- TABLE : commande
-- Description : Commandes passees par les clients
-- =============================================================
CREATE TABLE commande (
    id_commande         SERIAL          PRIMARY KEY,
    date_commande       TIMESTAMP       NOT NULL DEFAULT NOW(),
    statut              VARCHAR(20)     NOT NULL DEFAULT 'en_attente',
    montant_total       DECIMAL(10,2)   NOT NULL,
    id_client           INT             NOT NULL,

    -- Contraintes
    CONSTRAINT fk_commande_client
        FOREIGN KEY (id_client)
        REFERENCES client(id_client)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_commande_statut
        CHECK (statut IN ('en_attente', 'validee', 'expediee', 'livree', 'annulee')),
    CONSTRAINT chk_commande_montant CHECK (montant_total >= 0)
);

COMMENT ON TABLE commande IS 'Commandes passees par les clients';
COMMENT ON COLUMN commande.statut IS 'Etat de la commande : en_attente, validee, expediee, livree, annulee';

-- =============================================================
-- TABLE : ligne_commande
-- Description : Detail des produits dans chaque commande
-- =============================================================
CREATE TABLE ligne_commande (
    id_commande         INT             NOT NULL,
    id_produit          INT             NOT NULL,
    quantite            INT             NOT NULL,
    prix_unitaire_cmd   DECIMAL(10,2)   NOT NULL,

    -- Cle primaire composee
    PRIMARY KEY (id_commande, id_produit),

    -- Cles etrangeres
    CONSTRAINT fk_ligne_commande
        FOREIGN KEY (id_commande)
        REFERENCES commande(id_commande)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_ligne_produit
        FOREIGN KEY (id_produit)
        REFERENCES produit(id_produit)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    -- Contraintes de validation
    CONSTRAINT chk_ligne_quantite CHECK (quantite >= 1),
    CONSTRAINT chk_ligne_prix CHECK (prix_unitaire_cmd > 0)
);

COMMENT ON TABLE ligne_commande IS 'Lignes de detail des commandes (table de jonction)';
COMMENT ON COLUMN ligne_commande.prix_unitaire_cmd IS 'Prix unitaire fige au moment de la commande';
```

### 6.2 Creation des index

```sql
-- =============================================================
-- INDEX
-- =============================================================

-- Recherche de clients par nom (recherche frequente)
CREATE INDEX idx_client_nom ON client(nom, prenom);

-- Recherche de commandes par client (jointure frequente)
CREATE INDEX idx_commande_client ON commande(id_client);

-- Recherche de commandes par date (filtrage temporel)
CREATE INDEX idx_commande_date ON commande(date_commande DESC);

-- Recherche de commandes par statut (filtrage)
CREATE INDEX idx_commande_statut ON commande(statut)
    WHERE statut IN ('en_attente', 'validee', 'expediee');

-- Recherche de produits par categorie (jointure)
CREATE INDEX idx_produit_categorie ON produit(id_categorie);

-- Recherche de produits par nom (recherche full-text)
CREATE INDEX idx_produit_nom ON produit(nom_produit);

-- Recherche de lignes par produit (statistiques produit)
CREATE INDEX idx_ligne_produit ON ligne_commande(id_produit);
```

### 6.3 Modifications avec ALTER TABLE

```sql
-- =============================================================
-- ALTER TABLE : exemples de modifications apres creation
-- =============================================================

-- Ajouter une colonne
ALTER TABLE client
    ADD COLUMN adresse_livraison TEXT;

-- Ajouter une contrainte
ALTER TABLE produit
    ADD CONSTRAINT chk_produit_nom_longueur
    CHECK (LENGTH(nom_produit) >= 2);

-- Modifier le type d'une colonne
ALTER TABLE commande
    ALTER COLUMN montant_total TYPE DECIMAL(12,2);

-- Renommer une colonne
ALTER TABLE produit
    RENAME COLUMN description TO description_produit;

-- Ajouter une valeur par defaut
ALTER TABLE client
    ALTER COLUMN est_actif SET DEFAULT TRUE;

-- Supprimer une contrainte
ALTER TABLE produit
    DROP CONSTRAINT chk_produit_nom_longueur;

-- Ajouter une cle etrangere apres creation
ALTER TABLE commande
    ADD CONSTRAINT fk_commande_adresse
    FOREIGN KEY (id_adresse) REFERENCES adresse(id_adresse);
```

---

## 7. Bonnes pratiques de nommage

### 7.1 Conventions recommandees

| Element | Convention | Exemple |
|---------|-----------|---------|
| Table | snake_case, singulier | `client`, `ligne_commande` |
| Colonne | snake_case | `date_inscription`, `nom_produit` |
| Cle primaire | `id_` + nom table | `id_client`, `id_commande` |
| Cle etrangere | Meme nom que la PK referencee | `id_client` dans `commande` |
| Contrainte PK | `pk_` + table | `pk_client` |
| Contrainte FK | `fk_` + table_source + `_` + table_cible | `fk_commande_client` |
| Contrainte UNIQUE | `uk_` + table + `_` + colonne | `uk_client_email` |
| Contrainte CHECK | `chk_` + table + `_` + description | `chk_commande_statut` |
| Index | `idx_` + table + `_` + colonnes | `idx_commande_date` |
| Schema | snake_case | `ecommerce`, `iot_data` |

### 7.2 Regles generales

- ✅ Utiliser **snake_case** partout (pas de camelCase, pas de MAJUSCULES)
- ✅ Noms en **anglais ou francais**, mais ne pas melanger
- ✅ Noms **explicites et descriptifs** (`date_inscription` plutot que `dt_insc`)
- ✅ **Prefixer** les contraintes et index avec leur type
- ✅ **Singulier** pour les noms de tables (`client` pas `clients`)
- ❌ Eviter les mots reserves SQL (`user`, `order`, `table`, `select`)
- ❌ Eviter les abbreviations obscures (`clt` pour client)
- ❌ Eviter les espaces et caracteres speciaux

---

## 8. Comparaison PostgreSQL vs MySQL vs SQL Server

### 8.1 Differences principales

| Fonctionnalite | PostgreSQL | MySQL | SQL Server |
|----------------|-----------|-------|------------|
| **Auto-increment** | `SERIAL` / `GENERATED ALWAYS` | `AUTO_INCREMENT` | `IDENTITY(1,1)` |
| **Booleen** | `BOOLEAN` (natif) | `BOOLEAN` (alias TINYINT) | `BIT` |
| **UUID** | `UUID` (natif) | `CHAR(36)` | `UNIQUEIDENTIFIER` |
| **JSON** | `JSON` / `JSONB` | `JSON` | `NVARCHAR(MAX)` |
| **Schemas** | Oui (natif) | Non (= database) | Oui (natif) |
| **Partitionnement** | Declaratif (natif) | Oui | Oui |
| **CHECK contrainte** | Oui (appliquee) | Oui (depuis 8.0.16) | Oui |
| **Sequences** | Oui | Non | Oui |
| **CTE recursive** | Oui | Oui (depuis 8.0) | Oui |
| **Licence** | Open source (PostgreSQL) | Open source (GPL) | Proprietaire |
| **Prix** | Gratuit | Gratuit (Community) | Payant (sauf Express) |

### 8.2 Exemples de syntaxe comparee

```sql
-- Auto-increment
-- PostgreSQL :
CREATE TABLE client (id_client SERIAL PRIMARY KEY);
-- ou (standard SQL)
CREATE TABLE client (id_client INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY);

-- MySQL :
CREATE TABLE client (id_client INT AUTO_INCREMENT PRIMARY KEY);

-- SQL Server :
CREATE TABLE client (id_client INT IDENTITY(1,1) PRIMARY KEY);
```

```sql
-- Timestamp avec fuseau horaire
-- PostgreSQL :
date_mesure TIMESTAMP WITH TIME ZONE DEFAULT NOW()

-- MySQL :
date_mesure DATETIME DEFAULT CURRENT_TIMESTAMP

-- SQL Server :
date_mesure DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
```

💡 **Pour le Data Engineer** : PostgreSQL est le choix recommande pour la plupart des projets Data. Il est gratuit, complet, performant, et supporte nativement les types avances (JSON, arrays, hstore, PostGIS).

---

## 9. Resume

| Concept | A retenir |
|---------|-----------|
| DDL | CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX |
| Ordre de creation | Tables referencees en premier, dependantes en dernier |
| DECIMAL vs FLOAT | DECIMAL pour l'argent, FLOAT pour la science |
| TIMESTAMP WITH TZ | Toujours pour les systemes distribues |
| PRIMARY KEY | Identifie chaque ligne de maniere unique |
| FOREIGN KEY | Garantit l'integrite referentielle |
| CHECK | Valide les valeurs selon une condition |
| Index B-tree | Par defaut, efficace pour =, <, >, BETWEEN, ORDER BY |
| Index BRIN | Ideal pour les series temporelles (IoT, logs) |
| Partitionnement | Par RANGE (dates), LIST (regions), HASH (distribution) |
| Nommage | snake_case, prefixes (fk_, idx_, chk_, uk_) |

---

## 📝 Auto-evaluation

1. Ecrivez le CREATE TABLE pour la table MESURE du systeme IoT (avec PK, FK, contraintes).
2. Pourquoi utiliser `DECIMAL(10,2)` plutot que `FLOAT` pour un prix ?
3. Quel type d'index utiliseriez-vous pour une table de logs avec 100 millions de lignes filtrees par date ?
4. Dans quel ordre creeriez-vous les tables pour le schema IoT (capteur, zone, mesure, alerte) ?
5. Ecrivez un `ALTER TABLE` pour ajouter une contrainte CHECK sur le champ `severite` de la table alerte.

---

[← Precedent](04-modele-logique-mld.md) | [🏠 Accueil](README.md) | [Suivant →](06-outils-pratiques.md)

---

**Academy** - Formation Data Engineer
