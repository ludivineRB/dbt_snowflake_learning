[← Precedent](03-modele-conceptuel-mcd.md) | [🏠 Accueil](README.md) | [Suivant →](05-modele-physique-mpd.md)

---

# 04 - Le Modele Logique de Donnees (MLD)

## 🎯 Objectifs de cette lecon

- Maitriser les 5 regles de transformation MCD → MLD
- Comprendre et appliquer la normalisation (1NF, 2NF, 3NF, BCNF)
- Savoir quand et pourquoi denormaliser
- Transformer un MCD complet en MLD avec tables, cles primaires et cles etrangeres
- Lire et ecrire un schema relationnel en notation textuelle

---

## 1. Regles de transformation MCD → MLD

Le passage du MCD au MLD suit des **regles mecaniques** et non ambigues. C'est l'un des points forts de MERISE : la transformation est deterministe.

### 1.1 Regle 1 : Chaque entite devient une table

Chaque entite du MCD devient une **table** dans le MLD. L'identifiant de l'entite devient la **cle primaire (PK)** de la table. Les attributs deviennent des colonnes.

```
MCD :                                    MLD :
┌──────────────────┐                     CLIENT (
│     CLIENT       │                       id_client    PK,
├──────────────────┤        ──→            nom,
│ id_client        │                       prenom,
│ nom              │                       email,
│ prenom           │                       telephone,
│ email            │                       date_inscription
│ telephone        │                     )
│ date_inscription │
└──────────────────┘
```

### 1.2 Regle 2 : Association (x,1) - (x,n) → Cle etrangere cote (x,1)

Quand une association relie deux entites avec une cardinalite maximale de **1** d'un cote et **n** de l'autre, on ajoute une **cle etrangere (FK)** dans la table cote **(x,1)**.

La cle etrangere est l'identifiant de l'entite cote (x,n).

```
MCD :
┌──────────┐  (0,n)    PASSE    (1,1)  ┌──────────┐
│  CLIENT  │────────── [    ] ─────────│ COMMANDE │
└──────────┘                           └──────────┘

MLD :
CLIENT (                             COMMANDE (
  id_client    PK,                     id_commande     PK,
  nom,                                 date_commande,
  prenom,                              statut,
  email                                montant_total,
)                                      id_client       FK → CLIENT
                                     )

La FK id_client est ajoutee dans COMMANDE (cote 1,1)
car chaque commande est associee a 1 et 1 seul client.
```

**Explication** : on place la FK du cote (1,1) car chaque commande connait son client. L'inverse (mettre toutes les commandes dans la table client) serait absurde : un client peut avoir N commandes.

**Autre exemple** : PRODUIT (1,1) --- APPARTIENT --- (0,n) CATEGORIE

```
MLD :
PRODUIT (
  id_produit        PK,
  nom_produit,
  description,
  prix_unitaire,
  stock_disponible,
  id_categorie      FK → CATEGORIE    ← FK cote (1,1)
)
```

### 1.3 Regle 3 : Association (x,n) - (x,n) → Table de jonction

Quand une association relie deux entites avec une cardinalite maximale de **n des deux cotes** (relation N:M), on cree une **table de jonction** (aussi appelee table associative ou table pivot).

Cette table contient :
- Les cles primaires des deux entites comme **cles etrangeres**
- Ces deux FK forment ensemble la **cle primaire composee** de la table de jonction
- Les attributs de l'association (s'il y en a) deviennent des colonnes de la table de jonction

```
MCD :
┌──────────┐            CONTIENT              ┌──────────┐
│ COMMANDE │  (1,n) ┌──────────────┐  (0,n)  │ PRODUIT  │
│          │────────│ quantite     │─────────│          │
│          │        │ prix_unit_cmd│         │          │
└──────────┘        └──────────────┘         └──────────┘

MLD :

COMMANDE (                  LIGNE_COMMANDE (              PRODUIT (
  id_commande  PK,            id_commande  PK, FK,         id_produit  PK,
  date_commande,              id_produit   PK, FK,         nom_produit,
  statut,                     quantite,                    description,
  montant_total,              prix_unit_cmd                prix_unitaire,
  id_client    FK           )                              stock_disponible,
)                                                          id_categorie FK
                                                         )
```

**La table LIGNE_COMMANDE** :
- Sa PK est composee de (id_commande, id_produit) → identifie de maniere unique une ligne
- id_commande est FK vers COMMANDE
- id_produit est FK vers PRODUIT
- quantite et prix_unit_cmd sont les attributs de l'association

### 1.4 Regle 4 : Association (x,1) - (x,1) → Fusion ou FK

Quand les deux cotes ont une cardinalite maximale de **1** (relation 1:1), deux options :

**Option A : Cle etrangere** (prefere quand les entites sont distinctes)

```
MCD :
┌──────────┐  (1,1)   POSSEDE   (0,1)  ┌──────────┐
│ EMPLOYE  │────────── [    ] ──────────│  BADGE   │
└──────────┘                            └──────────┘

MLD (Option A) :
EMPLOYE (                    BADGE (
  id_employe  PK,              id_badge       PK,
  nom,                         code_acces,
  poste                        date_emission,
)                              id_employe     FK UNIQUE → EMPLOYE
                             )
```

La contrainte **UNIQUE** sur la FK garantit la relation 1:1.

**Option B : Fusion des tables** (quand les entites sont conceptuellement proches)

```
MLD (Option B) :
EMPLOYE (
  id_employe    PK,
  nom,
  poste,
  code_badge,        ← Attributs du badge integres dans EMPLOYE
  date_emission_badge
)
```

💡 **Quand fusionner ?** Quand les deux entites ont le meme cycle de vie (creees et supprimees en meme temps) et que la separation n'apporte pas de valeur.

### 1.5 Regle 5 : Association ternaire → Table de jonction a 3 FK

Une association ternaire se transforme comme une N:M, mais avec **3 cles etrangeres**.

```
MCD :
ENSEIGNANT (0,n) ─── ENSEIGNE ─── MATIERE (1,n)
                       │
                     SALLE (0,n)

MLD :
ENSEIGNEMENT (
  id_enseignant   PK, FK → ENSEIGNANT,
  id_matiere      PK, FK → MATIERE,
  id_salle        PK, FK → SALLE,
  jour,
  heure_debut
)
```

### 1.6 Tableau recapitulatif des regles

| Regle | Cardinalites | Transformation |
|-------|-------------|----------------|
| R1 | - | Entite → Table, Identifiant → PK |
| R2 | (x,1) -- (x,n) | FK dans la table cote (x,1) |
| R3 | (x,n) -- (x,n) | Table de jonction avec PK composee |
| R4 | (x,1) -- (x,1) | FK (avec UNIQUE) ou fusion |
| R5 | Ternaire | Table de jonction a 3+ FK |

---

## 2. La normalisation

### 2.1 Pourquoi normaliser ?

La normalisation est un processus qui **elimine les redondances** et les **anomalies** dans un schema relationnel. Sans normalisation, on risque :

- **Anomalie d'insertion** : impossible d'ajouter une donnee sans en ajouter une autre
- **Anomalie de mise a jour** : modifier une donnee oblige a la modifier partout
- **Anomalie de suppression** : supprimer une donnee entraine la perte d'une autre

### 2.2 Premiere Forme Normale (1NF)

**Regle** : Tous les attributs contiennent des **valeurs atomiques** (pas de listes, pas de groupes repetitifs).

```
❌ Table NON en 1NF :

| id_client | nom    | telephones              |
|-----------|--------|-------------------------|
| 1         | Dupont | 0601020304, 0501020304  |  ← Liste de valeurs !
| 2         | Martin | 0701020304              |

❌ Autre violation de 1NF (groupes repetitifs) :

| id_commande | produit_1 | qte_1 | produit_2 | qte_2 | produit_3 | qte_3 |
|------------|-----------|-------|-----------|-------|-----------|-------|
| 1          | Clavier   | 2     | Souris    | 1     | NULL      | NULL  |


✅ Table en 1NF (valeurs atomiques) :

TELEPHONE :
| id_telephone | id_client | numero     |
|-------------|-----------|------------|
| 1           | 1         | 0601020304 |
| 2           | 1         | 0501020304 |
| 3           | 2         | 0701020304 |

LIGNE_COMMANDE :
| id_commande | id_produit | quantite |
|------------|-----------|----------|
| 1          | 1         | 2        |
| 1          | 2         | 1        |
```

**En resume** : chaque cellule contient UNE seule valeur. Pas de listes, pas de colonnes repetees.

### 2.3 Deuxieme Forme Normale (2NF)

**Prerequis** : la table doit etre en 1NF.

**Regle** : Tous les attributs non-cle dependent de la **totalite** de la cle primaire (pas de **dependance partielle**).

⚠️ La 2NF ne concerne que les tables avec une **cle primaire composee**.

```
❌ Table NON en 2NF :

LIGNE_COMMANDE :
| id_commande (PK) | id_produit (PK) | quantite | nom_produit    |
|------------------|-----------------|----------|----------------|
| 1                | 101             | 2        | Clavier USB    |
| 1                | 102             | 1        | Souris optique |
| 2                | 101             | 3        | Clavier USB    |

Probleme : nom_produit depend SEULEMENT de id_produit, pas de la cle complete
           (id_commande, id_produit).
           → Dependance partielle ! → "Clavier USB" est repete inutilement.


✅ Tables en 2NF :

LIGNE_COMMANDE :                         PRODUIT :
| id_commande | id_produit | quantite |  | id_produit | nom_produit    |
|------------|-----------|----------|  |-----------|----------------|
| 1          | 101       | 2        |  | 101       | Clavier USB    |
| 1          | 102       | 1        |  | 102       | Souris optique |
| 2          | 101       | 3        |
```

**En resume** : chaque attribut non-cle depend de TOUTE la cle, pas d'une partie seulement.

### 2.4 Troisieme Forme Normale (3NF)

**Prerequis** : la table doit etre en 2NF.

**Regle** : Aucun attribut non-cle ne depend d'un **autre attribut non-cle** (pas de **dependance transitive**).

```
❌ Table NON en 3NF :

CLIENT :
| id_client (PK) | nom    | code_postal | ville       |
|----------------|--------|-------------|-------------|
| 1              | Dupont | 75001       | Paris       |
| 2              | Martin | 75001       | Paris       |
| 3              | Durand | 69001       | Lyon        |

Probleme : ville depend de code_postal, qui n'est pas la PK.
           id_client → code_postal → ville
           C'est une dependance transitive !
           → "Paris" est repete pour chaque client du 75001.


✅ Tables en 3NF :

CLIENT :                                 VILLE :
| id_client | nom    | code_postal |    | code_postal | ville  |
|-----------|--------|-------------|    |-------------|--------|
| 1         | Dupont | 75001       |    | 75001       | Paris  |
| 2         | Martin | 75001       |    | 69001       | Lyon   |
| 3         | Durand | 69001       |
```

**En resume** : aucun attribut non-cle ne determine un autre attribut non-cle.

### 2.5 Forme Normale de Boyce-Codd (BCNF)

**Prerequis** : la table doit etre en 3NF.

**Regle** : Tout **determinant** (attribut dont d'autres attributs dependent fonctionnellement) est une **cle candidate**.

La BCNF est plus stricte que la 3NF. En pratique, les violations sont rares.

```
❌ Table NON en BCNF :

ENSEIGNEMENT :
| etudiant (PK) | matiere (PK) | enseignant |
|--------------|-------------|------------|
| Alice        | Maths       | Prof_A     |
| Bob          | Maths       | Prof_A     |
| Alice        | Physique    | Prof_B     |

Regle metier : un enseignant n'enseigne qu'une seule matiere.
→ enseignant → matiere (enseignant est un determinant)
→ Mais enseignant n'est PAS une cle candidate !
→ Violation de BCNF.


✅ Solution BCNF :

INSCRIPTION :                           AFFECTATION :
| etudiant | enseignant |               | enseignant | matiere  |
|----------|-----------|               |-----------|----------|
| Alice    | Prof_A    |               | Prof_A    | Maths    |
| Bob      | Prof_A    |               | Prof_B    | Physique |
| Alice    | Prof_B    |
```

### 2.6 Resume des formes normales

```
┌──────────┐
│   1NF    │  Valeurs atomiques, pas de groupes repetitifs
├──────────┤
│   2NF    │  + Pas de dependance partielle (cle composee)
├──────────┤
│   3NF    │  + Pas de dependance transitive
├──────────┤
│  BCNF    │  + Tout determinant est une cle candidate
└──────────┘

Chaque niveau inclut le precedent :
1NF ⊂ 2NF ⊂ 3NF ⊂ BCNF
```

**En pratique** : visez la **3NF** pour les bases operationnelles (OLTP). La BCNF est un bonus rarement necessaire.

---

## 3. La denormalisation

### 3.1 Quand denormaliser ?

La normalisation optimise pour l'**ecriture** (pas de redondance, pas d'anomalie). Mais parfois, on sacrifie la normalisation pour la **lecture** (performance des requetes).

| Contexte | Normaliser (3NF) | Denormaliser |
|----------|-----------------|--------------|
| **OLTP** (transactionnel) | ✅ Oui | ❌ Non |
| **OLAP** (analytique) | ❌ Non | ✅ Oui |
| **Data Warehouse** | ❌ Non | ✅ Oui (schemas en etoile) |
| **Cache / Lecture intensive** | ❌ Non | ✅ Oui |
| **Faible volume** | ✅ Oui | ❌ Inutile |
| **Fort volume en lecture** | Possiblement non | ✅ Oui |

### 3.2 Techniques de denormalisation

**1. Ajout de colonnes redondantes**

```sql
-- 3NF : il faut une jointure pour avoir le nom du client sur une commande
SELECT c.nom, co.date_commande
FROM commande co
JOIN client c ON c.id_client = co.id_client;

-- Denormalise : on ajoute le nom directement dans commande
-- Plus rapide en lecture, mais il faut maintenir la coherence
ALTER TABLE commande ADD COLUMN nom_client VARCHAR(100);
```

**2. Tables pre-agregees**

```sql
-- 3NF : calculer le CA par mois necessite un GROUP BY couteux
SELECT DATE_TRUNC('month', date_commande) AS mois, SUM(montant_total)
FROM commande
GROUP BY 1;

-- Denormalise : une table materialisee
CREATE TABLE ca_mensuel (
    mois        DATE PRIMARY KEY,
    total_ca    DECIMAL(15,2),
    nb_commandes INT
);
```

**3. Schemas en etoile (Data Warehouse)**

```
                        ┌──────────────┐
                        │  DIM_CLIENT  │
                        └──────┬───────┘
                               │
┌──────────────┐      ┌───────▼────────┐      ┌──────────────┐
│  DIM_PRODUIT │──────│  FAIT_VENTE    │──────│  DIM_DATE    │
└──────────────┘      └───────┬────────┘      └──────────────┘
                               │
                        ┌──────▼───────┐
                        │ DIM_MAGASIN  │
                        └──────────────┘
```

💡 **Pour le Data Engineer** : vous alternerez entre normalisation (bases operationnelles, staging) et denormalisation (Data Warehouse, cubes OLAP). Savoir faire les deux est essentiel.

---

## 4. MLD complet : exemple E-commerce

Appliquons les regles de transformation au MCD de la lecon 03.

### 4.1 Application des regles

| Association MCD | Cardinalites | Regle appliquee | Resultat MLD |
|----------------|-------------|-----------------|--------------|
| CLIENT - PASSE - COMMANDE | (0,n) -- (1,1) | R2 | FK id_client dans COMMANDE |
| COMMANDE - CONTIENT - PRODUIT | (1,n) -- (0,n) | R3 | Table LIGNE_COMMANDE |
| CATEGORIE - APPARTIENT - PRODUIT | (0,n) -- (1,1) | R2 | FK id_categorie dans PRODUIT |

### 4.2 Schema relationnel (notation textuelle)

```
CLIENT (
    id_client           PK,
    nom                 VARCHAR(100)    NOT NULL,
    prenom              VARCHAR(100)    NOT NULL,
    email               VARCHAR(255)    NOT NULL UNIQUE,
    telephone           VARCHAR(20),
    date_inscription    TIMESTAMP       NOT NULL
)

CATEGORIE (
    id_categorie         PK,
    nom_categorie        VARCHAR(100)    NOT NULL,
    description_categorie TEXT
)

PRODUIT (
    id_produit           PK,
    nom_produit          VARCHAR(200)    NOT NULL,
    description          TEXT,
    prix_unitaire        DECIMAL(10,2)   NOT NULL,
    stock_disponible     INT             NOT NULL,
    #id_categorie        FK → CATEGORIE  NOT NULL
)

COMMANDE (
    id_commande          PK,
    date_commande        TIMESTAMP       NOT NULL,
    statut               VARCHAR(20)     NOT NULL,
    montant_total        DECIMAL(10,2)   NOT NULL,
    #id_client           FK → CLIENT     NOT NULL
)

LIGNE_COMMANDE (
    #id_commande         PK, FK → COMMANDE,
    #id_produit          PK, FK → PRODUIT,
    quantite             INT             NOT NULL,
    prix_unitaire_cmd    DECIMAL(10,2)   NOT NULL
)
```

**Legende** :
- `PK` = Cle Primaire
- `FK` = Cle Etrangere (prefixee par `#` en notation MERISE)
- `NOT NULL` = Obligatoire
- `UNIQUE` = Valeur unique dans la table

### 4.3 Diagramme du MLD

```
┌─────────────────────────────┐
│          CLIENT             │
├─────────────────────────────┤
│ PK  id_client          INT  │
│     nom           VARCHAR   │
│     prenom        VARCHAR   │
│     email         VARCHAR   │  UNIQUE
│     telephone     VARCHAR   │
│     date_inscription TIMESTAMP│
└──────────────┬──────────────┘
               │ 1
               │
               │ *
┌──────────────▼──────────────┐         ┌─────────────────────────────┐
│         COMMANDE            │         │        CATEGORIE            │
├─────────────────────────────┤         ├─────────────────────────────┤
│ PK  id_commande        INT  │         │ PK  id_categorie       INT  │
│     date_commande TIMESTAMP │         │     nom_categorie  VARCHAR  │
│     statut         VARCHAR  │         │     description_cat  TEXT   │
│     montant_total  DECIMAL  │         └──────────────┬──────────────┘
│ FK  id_client          INT  │─ ─ ─ ┐                │ 1
└──────────────┬──────────────┘      │                │
               │ 1                    │                │ *
               │                      │  ┌─────────────▼──────────────┐
               │ *                    │  │          PRODUIT            │
┌──────────────▼──────────────┐      │  ├─────────────────────────────┤
│      LIGNE_COMMANDE         │      │  │ PK  id_produit         INT  │
├─────────────────────────────┤      │  │     nom_produit    VARCHAR  │
│ PK,FK id_commande      INT  │──────┘  │     description       TEXT  │
│ PK,FK id_produit       INT  │─────────│     prix_unitaire  DECIMAL  │
│       quantite         INT  │         │     stock_disponible   INT  │
│       prix_unitaire_cmd DEC │         │ FK  id_categorie       INT  │
└─────────────────────────────┘         └─────────────────────────────┘
```

### 4.4 Verification de la normalisation

**1NF** : ✅ Toutes les valeurs sont atomiques, pas de groupes repetitifs.

**2NF** : ✅ Dans LIGNE_COMMANDE (PK composee), `quantite` et `prix_unitaire_cmd` dependent de la cle complete (id_commande, id_produit), pas d'une partie seulement.

**3NF** : ✅ Aucun attribut non-cle ne determine un autre attribut non-cle. Par exemple, `nom_categorie` n'est pas dans PRODUIT (il est dans CATEGORIE, liee par FK).

---

## 5. Verification du MLD

### 5.1 Checklist de verification

Apres avoir produit votre MLD, verifiez systematiquement :

- ✅ Chaque entite du MCD a sa table dans le MLD
- ✅ Chaque identifiant est devenu une PK
- ✅ Les associations (x,1)-(x,n) ont genere une FK cote (x,1)
- ✅ Les associations (x,n)-(x,n) ont genere une table de jonction
- ✅ Les attributs d'association sont dans la table de jonction
- ✅ Aucune donnee n'est dupliquee sans raison
- ✅ Les NOT NULL sont coherents avec les cardinalites minimales
  - Cardinalite min = 1 → FK NOT NULL
  - Cardinalite min = 0 → FK peut etre NULL

### 5.2 Lien cardinalites → contraintes

| Cardinalite MERISE | Contrainte MLD |
|--------------------|----------------|
| (1,1) | FK NOT NULL |
| (0,1) | FK NULLABLE (ou UNIQUE si max=1) |
| (1,n) | Au moins 1 ligne dans la table de jonction (contrainte applicative) |
| (0,n) | Aucune contrainte supplementaire |

---

## 6. Resume

| Concept | A retenir |
|---------|-----------|
| Regle 1 | Entite → Table, Identifiant → PK |
| Regle 2 | Association (x,1)-(x,n) → FK cote (x,1) |
| Regle 3 | Association (x,n)-(x,n) → Table de jonction (PK composee) |
| Regle 4 | Association (x,1)-(x,1) → FK + UNIQUE ou fusion |
| Regle 5 | Ternaire → Table de jonction a 3 FK |
| 1NF | Valeurs atomiques, pas de groupes repetitifs |
| 2NF | Pas de dependance partielle (cle composee) |
| 3NF | Pas de dependance transitive |
| BCNF | Tout determinant est une cle candidate |
| Denormalisation | Sacrifier la normalisation pour la performance en lecture |

---

## 📝 Auto-evaluation

1. Transformez le MCD suivant en MLD :
   - AUTEUR (0,n) --- ECRIT --- (1,n) LIVRE
   - LIVRE (0,n) --- EMPRUNTE --- (0,n) ADHERENT (avec date_emprunt, date_retour)

2. La table suivante est-elle en 3NF ? Justifiez.
   ```
   COMMANDE (id_commande, date, id_client, nom_client, email_client, montant)
   ```

3. Quelle regle de transformation appliqueriez-vous pour une association (0,1)-(0,1) ? Pourquoi ?

4. Dans un contexte Data Warehouse, pourquoi denormaliseriez-vous la table COMMANDE en y ajoutant le nom du client ?

5. Une table LIGNE_COMMANDE avec les colonnes (id_commande PK, id_produit PK, quantite, nom_produit) est-elle en 2NF ? Pourquoi ?

---

[← Precedent](03-modele-conceptuel-mcd.md) | [🏠 Accueil](README.md) | [Suivant →](05-modele-physique-mpd.md)

---

**Academy** - Formation Data Engineer
