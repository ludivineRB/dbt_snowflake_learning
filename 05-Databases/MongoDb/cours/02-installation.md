## Objectifs du module

- Installer MongoDB avec Docker
- Configurer docker-compose pour MongoDB
- Se connecter avec mongosh
- Utiliser PyMongo avec Python

## Installation de MongoDB

### Option 1 : Installation locale

```bash
# macOS avec Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod

# Verifier l'installation
mongosh --version
```

### Option 2 : Docker (recommande pour le developpement)

Docker permet une installation rapide et isolee de MongoDB, ideale pour le developpement.

#### Lancer MongoDB avec Docker

```bash
# Lancer MongoDB avec Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:7.0

# Se connecter au shell MongoDB
docker exec -it mongodb mongosh -u admin -p password
```

#### Configuration avec docker-compose

Pour un environnement plus complet avec Mongo Express (interface web), creez un fichier `docker-compose.yml` :

```bash
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb_dev
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: mydb
    volumes:
      - mongodb_data:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js
    restart: unless-stopped

  mongo-express:
    image: mongo-express:latest
    container_name: mongo_express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: password
      ME_CONFIG_MONGODB_URL: mongodb://admin:password@mongodb:27017/
      ME_CONFIG_BASICAUTH: false
    depends_on:
      - mongodb
    restart: unless-stopped

volumes:
  mongodb_data:
```

```bash
# Demarrer avec docker-compose
docker-compose up -d

# Acceder a Mongo Express (UI web)
# http://localhost:8081

# Arreter les services
docker-compose down
```

### Option 3 : MongoDB Atlas (Cloud gratuit)

MongoDB Atlas offre un cluster gratuit (M0) dans le cloud :

1. Allez sur [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Creez un compte gratuit
3. Creez un cluster (M0 - Free Tier)
4. Configurez l'acces reseau (Allow Access from Anywhere pour le dev)
5. Creez un utilisateur de base de donnees
6. Recuperez la connection string

#### Connection String MongoDB

Format local : `mongodb://[username:password@]host[:port]/[database]`

Format Atlas : `mongodb+srv://username:password@cluster.mongodb.net/database`

## Se connecter a MongoDB

### Avec mongosh (MongoDB Shell)

```bash
# Connexion locale
mongosh

# Avec authentification
mongosh mongodb://localhost:27017 -u admin -p password

# MongoDB Atlas
mongosh "mongodb+srv://cluster0.xxxxx.mongodb.net/mydb" --username admin

# Voir les bases de donnees
show dbs

# Utiliser une base de donnees
use mydb

# Voir les collections
show collections

# Afficher la base courante
db

# Quitter
exit
```

### Avec Python (PyMongo)

#### Installation de PyMongo

```bash
# Installation avec pip
pip install pymongo

# Avec support DNS pour Atlas
pip install "pymongo[srv]"
```

#### Connexion avec PyMongo

```bash
from pymongo import MongoClient
from datetime import datetime

# Connexion locale
client = MongoClient('mongodb://localhost:27017/')

# Avec authentification
client = MongoClient(
    'mongodb://localhost:27017/',
    username='admin',
    password='password'
)

# MongoDB Atlas
client = MongoClient(
    'mongodb+srv://admin:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority'
)

# Selectionner une base de donnees
db = client['mydb']

# Selectionner une collection
collection = db['users']

# Tester la connexion
try:
    client.admin.command('ping')
    print("Connexion reussie a MongoDB!")
except Exception as e:
    print(f"Erreur de connexion: {e}")

# Obtenir des informations sur le serveur
server_info = client.server_info()
print(f"Version MongoDB: {server_info['version']}")

# Lister les bases de donnees
print("Bases de donnees:", client.list_database_names())

# Lister les collections
print("Collections:", db.list_collection_names())

# Fermer la connexion
client.close()
```

#### Bonnes pratiques de connexion

- Utilisez des variables d'environnement pour les credentials
- Fermez toujours les connexions apres utilisation
- Utilisez un connection pool pour les applications en production
- Configurez des timeouts pour eviter les blocages

### Points cles a retenir

- Docker est la methode la plus simple pour installer MongoDB en dev
- docker-compose permet de configurer MongoDB + Mongo Express facilement
- mongosh est le shell interactif pour MongoDB
- PyMongo est le driver Python officiel pour MongoDB
- MongoDB Atlas offre un cluster gratuit dans le cloud

[Module 1: Introduction](01-introduction.md)
[Module 3: Operations CRUD](03-crud.md)