# Module 02 - Création de projet et datasets

## Création d'un compte GCP

### Étape 1 : Créer un compte Google Cloud

1. Aller sur [cloud.google.com](https://cloud.google.com)
2. Cliquer sur "Get started for free"
3. Se connecter avec un compte Google
4. Accepter les conditions
5. Entrer les informations de facturation (carte requise mais pas débitée)

### Free Tier et crédits

```
┌─────────────────────────────────────────────────────────┐
│                  GCP FREE TIER                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  BigQuery (permanent) :                                 │
│  ├── 1 TB de requêtes / mois                           │
│  └── 10 GB de stockage / mois                          │
│                                                          │
│  Cloud Storage (permanent) :                            │
│  └── 5 GB de stockage                                   │
│                                                          │
│  Nouveaux comptes :                                     │
│  └── $300 de crédits valables 90 jours                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Création d'un projet

### Via la Console

1. Console GCP → Sélecteur de projet (en haut)
2. "Nouveau projet"
3. Remplir :
   - **Nom** : `formation-bigquery-dwh`
   - **ID** : Généré automatiquement (unique)
   - **Organisation** : Aucune (compte personnel)
4. Créer

### Via gcloud CLI

```bash
# Installer gcloud si nécessaire
# https://cloud.google.com/sdk/docs/install

# Authentification
gcloud auth login

# Créer le projet
gcloud projects create formation-bigquery-dwh \
    --name="Formation BigQuery DWH"

# Définir le projet par défaut
gcloud config set project formation-bigquery-dwh

# Activer l'API BigQuery
gcloud services enable bigquery.googleapis.com
```

## Création des datasets

### Structure Medallion

On va créer 3 datasets correspondant aux couches :

```
formation-bigquery-dwh
├── bronze    -- Données brutes
├── silver    -- Données nettoyées
└── gold      -- Données agrégées
```

### Via la Console BigQuery

1. Console GCP → BigQuery
2. Dans l'Explorer, cliquer sur les 3 points à côté du projet
3. "Create dataset"
4. Remplir :
   - **Dataset ID** : `bronze`
   - **Location** : `EU` (multi-region Europe)
   - **Default table expiration** : Jamais
5. Répéter pour `silver` et `gold`

### Via SQL

```sql
-- Dataset Bronze
CREATE SCHEMA IF NOT EXISTS `formation-bigquery-dwh.bronze`
OPTIONS(
    location = 'EU',
    description = 'Données brutes - Couche Bronze',
    labels = [("layer", "bronze"), ("env", "formation")]
);

-- Dataset Silver
CREATE SCHEMA IF NOT EXISTS `formation-bigquery-dwh.silver`
OPTIONS(
    location = 'EU',
    description = 'Données nettoyées - Couche Silver',
    labels = [("layer", "silver"), ("env", "formation")]
);

-- Dataset Gold
CREATE SCHEMA IF NOT EXISTS `formation-bigquery-dwh.gold`
OPTIONS(
    location = 'EU',
    description = 'Données agrégées - Couche Gold',
    labels = [("layer", "gold"), ("env", "formation")]
);

-- Vérifier la création
SELECT schema_name, location, creation_time
FROM `formation-bigquery-dwh.INFORMATION_SCHEMA.SCHEMATA`;
```

### Via bq CLI

```bash
# Créer les datasets
bq mk --location=EU --description="Bronze Layer" bronze
bq mk --location=EU --description="Silver Layer" silver
bq mk --location=EU --description="Gold Layer" gold

# Vérifier
bq ls
```

## Configuration du stockage (Cloud Storage)

Pour stocker les fichiers sources avant ingestion.

### Créer un bucket

```bash
# Créer un bucket (nom unique global)
gsutil mb -l EU gs://formation-bigquery-dwh-data/

# Structure recommandée
gsutil mkdir gs://formation-bigquery-dwh-data/landing/
gsutil mkdir gs://formation-bigquery-dwh-data/archive/
gsutil mkdir gs://formation-bigquery-dwh-data/rejected/
```

### Structure du bucket

```
gs://formation-bigquery-dwh-data/
├── landing/           -- Fichiers à ingérer
│   ├── sales/
│   ├── customers/
│   └── products/
├── archive/           -- Fichiers traités
└── rejected/          -- Fichiers en erreur
```

## Permissions et IAM

### Rôles BigQuery principaux

| Rôle | Description |
|------|-------------|
| `roles/bigquery.admin` | Accès complet |
| `roles/bigquery.dataEditor` | Lecture + écriture tables |
| `roles/bigquery.dataViewer` | Lecture seule |
| `roles/bigquery.jobUser` | Exécuter des requêtes |
| `roles/bigquery.user` | Lister datasets + créer jobs |

### Exemple : ajouter un utilisateur

```bash
# Donner accès en lecture au dataset gold
gcloud projects add-iam-policy-binding formation-bigquery-dwh \
    --member="user:analyste@example.com" \
    --role="roles/bigquery.dataViewer"
```

### Permissions niveau dataset

```sql
-- Accorder SELECT sur un dataset
GRANT `roles/bigquery.dataViewer`
ON SCHEMA `formation-bigquery-dwh.gold`
TO "user:analyste@example.com";
```

## Configuration du projet

### Quotas et limites

Vérifier les quotas dans la console :
- Console → IAM & Admin → Quotas

Limites importantes :
- Taille max d'une requête : 12 MB
- Résultat max : 10 GB (sans destination)
- Tables externes : 10 000 par dataset

### Paramètres recommandés

```sql
-- Activer le cache des résultats (par défaut)
-- Les requêtes identiques dans les 24h sont gratuites

-- Définir une limite de bytes par requête (protection coûts)
-- Console → BigQuery → Project Settings → Maximum bytes billed
```

## Vérification de l'environnement

### Script de validation

```sql
-- 1. Vérifier les datasets
SELECT
    catalog_name as project,
    schema_name as dataset,
    location
FROM `INFORMATION_SCHEMA.SCHEMATA`
ORDER BY schema_name;

-- 2. Tester une requête (dataset public)
SELECT
    word,
    SUM(word_count) as total
FROM `bigquery-public-data.samples.shakespeare`
GROUP BY word
ORDER BY total DESC
LIMIT 5;

-- 3. Créer une table de test
CREATE OR REPLACE TABLE `bronze.test_connection` AS
SELECT
    CURRENT_TIMESTAMP() as created_at,
    'Connection test successful' as message;

SELECT * FROM `bronze.test_connection`;

-- 4. Nettoyer
DROP TABLE IF EXISTS `bronze.test_connection`;
```

### Checklist

- [ ] Projet GCP créé
- [ ] API BigQuery activée
- [ ] 3 datasets créés (bronze, silver, gold)
- [ ] Bucket Cloud Storage créé
- [ ] Permissions configurées
- [ ] Requête de test réussie

## Points clés à retenir

- Toujours choisir la **même région** pour datasets et buckets
- **Labels** pour organiser et suivre les coûts
- **Free Tier** : 1 TB requêtes + 10 GB stockage gratuits
- **Permissions** au niveau projet, dataset ou table
- Structure **Medallion** : 3 datasets distincts

---

**Prochain module :** [03 - Chargement des données](./03-ingestion.md)

[Module précédent](./01-introduction.md) | [Retour au sommaire](./README.md)
