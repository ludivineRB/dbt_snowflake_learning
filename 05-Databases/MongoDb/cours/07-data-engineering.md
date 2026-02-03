## Objectifs du module

- Creer des pipelines ETL avec Python
- Utiliser Change Streams pour le temps reel
- Implementer des transactions ACID
- Configurer des backups automatises

## Cas d'usage courants

#### Data Lake / Staging

Stocker des donnees brutes semi-structurees avant transformation (JSON logs, API responses)

#### Analytics Real-time

Agregations rapides sur des donnees en temps reel avec le framework d'agregation

#### API Backend

Base de donnees pour des APIs REST ou GraphQL avec donnees flexibles

#### IoT & Sensors

Stocker des millions de mesures de capteurs avec le bucket pattern

#### Search & Catalog

Moteur de recherche avec full-text search et Atlas Search

#### Content Management

CMS avec schema flexible pour differents types de contenu

### Pipeline ETL avec MongoDB

```bash
"""
ETL Pipeline: Extract from API -> Transform -> Load to MongoDB
"""
from pymongo import MongoClient
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBPipeline:
    def __init__(self, connection_string, database_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        logger.info(f"Connecte a MongoDB: {database_name}")

    def extract_from_api(self, api_url):
        """Extract data from REST API"""
        logger.info(f"Extraction depuis {api_url}")
        response = requests.get(api_url)
        data = response.json()
        logger.info(f"{len(data)} enregistrements extraits")
        return data

    def transform_data(self, raw_data):
        """Transform and clean data"""
        logger.info("Transformation des donnees")
        transformed = []

        for item in raw_data:
# Nettoyage et enrichissement
            cleaned = {
                "name": item.get("name", "").strip(),
                "email": item.get("email", "").lower(),
                "age": int(item.get("age", 0)),
                "status": "active",
                "created_at": datetime.utcnow(),
                "metadata": {
                    "source": "api",
                    "version": "1.0"
                }
            }
            transformed.append(cleaned)

        logger.info(f"{len(transformed)} enregistrements transformes")
        return transformed

    def load_to_mongodb(self, data, collection_name):
        """Load data into MongoDB collection"""
        logger.info(f"Chargement dans la collection {collection_name}")
        collection = self.db[collection_name]

# Bulk insert
        if data:
            result = collection.insert_many(data)
            logger.info(f"{len(result.inserted_ids)} documents inseres")
            return result.inserted_ids
        else:
            logger.warning("Aucune donnee a charger")
            return []

    def run_pipeline(self, api_url, collection_name):
        """Execute full ETL pipeline"""
        logger.info("Demarrage du pipeline ETL")

        try:
# Extract
            raw_data = self.extract_from_api(api_url)

# Transform
            transformed_data = self.transform_data(raw_data)

# Load
            self.load_to_mongodb(transformed_data, collection_name)

            logger.info("Pipeline ETL termine avec succes")

        except Exception as e:
            logger.error(f"Erreur dans le pipeline: {e}")
            raise

        finally:
            self.client.close()


# Utilisation
if __name__ == "__main__":
    pipeline = MongoDBPipeline(
        connection_string="mongodb://localhost:27017/",
        database_name="data_engineering"
    )

    pipeline.run_pipeline(
        api_url="https://jsonplaceholder.typicode.com/users",
        collection_name="users"
    )
```

## Change Streams : Donnees en temps reel

Les **Change Streams** permettent de surveiller les modifications sur une collection
en temps reel (inserts, updates, deletes).

```bash
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# Ouvrir un change stream
with collection.watch() as stream:
    print("Surveillance des changements...")
    for change in stream:
        print(f"Changement detecte: {change['operationType']}")
        print(f"Document: {change.get('fullDocument')}")

# Traiter le changement
        if change['operationType'] == 'insert':
            print("Nouveau document insere")
        elif change['operationType'] == 'update':
            print("Document mis a jour")
        elif change['operationType'] == 'delete':
            print("Document supprime")
```

**Cas d'usage :** Synchronisation temps reel, notifications, audit logs, replication

#### Prerequis pour Change Streams

Les Change Streams necessitent un replica set MongoDB (disponible par defaut sur MongoDB Atlas).
Pour un usage local, configurez un replica set ou utilisez MongoDB 4.2+ en mode standalone avec replication.

## Transactions ACID

Depuis MongoDB 4.0, les **transactions multi-documents** sont supportees pour garantir
la coherence des donnees (ACID : Atomicity, Consistency, Isolation, Durability).

```bash
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']

# Demarrer une session
with client.start_session() as session:
# Demarrer une transaction
    with session.start_transaction():
        try:
# Operation 1 : Debiter le compte A
            db.accounts.update_one(
                {"account_id": "A"},
                {"$inc": {"balance": -100}},
                session=session
            )

# Operation 2 : Crediter le compte B
            db.accounts.update_one(
                {"account_id": "B"},
                {"$inc": {"balance": 100}},
                session=session
            )

# Tout s'est bien passe, commit
            print("Transaction reussie")

        except Exception as e:
# En cas d'erreur, rollback automatique
            print(f"Transaction echouee: {e}")
            raise
```

#### Quand utiliser les transactions ?

- Operations critiques necessitant l'atomicite (virements bancaires, commandes)
- Modifications sur plusieurs collections qui doivent reussir ou echouer ensemble
- Pas besoin si vous utilisez embedded documents (atomicite par defaut)

## Backup et Restore

### mongodump et mongorestore

```bash
# Backup d'une base de donnees
mongodump --uri="mongodb://localhost:27017/mydb" --out=/backup/

# Backup avec compression
mongodump --uri="mongodb://localhost:27017/mydb" --gzip --out=/backup/

# Backup d'une collection specifique
mongodump --db=mydb --collection=users --out=/backup/

# Restore
mongorestore --uri="mongodb://localhost:27017/" /backup/

# Restore avec drop des collections existantes
mongorestore --uri="mongodb://localhost:27017/" --drop /backup/
```

### Backup automatise avec Python

```bash
import subprocess
from datetime import datetime
import os

def backup_mongodb(database_name, backup_dir):
    """Backup automatique de MongoDB"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(backup_dir, f"backup_{timestamp}")

    command = [
        "mongodump",
        f"--uri=mongodb://localhost:27017/{database_name}",
        f"--out={output_dir}",
        "--gzip"
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Backup reussi: {output_dir}")
        return output_dir
    except subprocess.CalledProcessError as e:
        print(f"Erreur backup: {e}")
        raise

# Utilisation
backup_mongodb("mydb", "/backups/mongodb")
```

#### Bonnes pratiques de backup

- Backups reguliers automatises (cron, scheduler)
- Stockage des backups sur un systeme distant (S3, etc.)
- Tester regulierement la restauration
- Conserver plusieurs versions de backups

## Integration avec l'ecosysteme Data

### MongoDB avec Apache Airflow

```bash
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pymongo import MongoClient

def extract_and_load():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['analytics']
    collection = db['daily_stats']

# Votre logique ETL ici
    data = {"date": datetime.utcnow(), "total": 1000}
    collection.insert_one(data)

    client.close()

dag = DAG(
    'mongodb_etl',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
)

task = PythonOperator(
    task_id='extract_load',
    python_callable=extract_and_load,
    dag=dag
)
```

### MongoDB avec Pandas

```bash
import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
collection = db['users']

# MongoDB vers DataFrame
cursor = collection.find({"age": {"$gt": 25}})
df = pd.DataFrame(list(cursor))

# Analyse avec Pandas
print(df.describe())
print(df.groupby('department')['age'].mean())

# DataFrame vers MongoDB
new_data = pd.DataFrame({
    "name": ["Alice", "Bob"],
    "age": [28, 32]
})

collection.insert_many(new_data.to_dict('records'))
```

### Best Practices Data Engineering avec MongoDB

- Utilisez des index adaptes pour vos requetes frequentes
- Privilegiez l'agregation pipeline pour l'analytics
- Implementez des Change Streams pour la synchronisation temps reel
- Mettez en place des backups automatiques reguliers
- Surveillez les performances avec MongoDB Atlas ou Ops Manager
- Utilisez le bucket pattern pour les time-series data
- Configurez la replication pour la haute disponibilite
- Documentez votre schema meme s'il est flexible

[Module 6: Modelisation](06-modelisation.md)
[Retour a l'accueil](index.md)