# 01 - Installation des outils

[🏠 Accueil](../README.md) | [02 - Création de la BDD →](02-creation-bdd-import.md)

---

Pour pratiquer le SQL, vous avez besoin de deux choses :
1. **Un moteur de base de données (SGBD)** : Celui qui exécute vos requêtes.
2. **Un client SQL (GUI)** : L'interface pour écrire vos requêtes et voir les résultats.

## 1. Le choix du SGBD : DuckDB

Pour ce cours, nous recommandons **DuckDB**. 
- **Pourquoi ?** C'est un SGBD analytique (OLAP) ultra-rapide, qui ne nécessite aucune installation de serveur complexe. C'est le "SQLite du Big Data".
- **Installation** : 
  - Sur macOS : `brew install duckdb`
  - Sur Windows/Linux : Téléchargez l'exécutable sur [duckdb.org](https://duckdb.org/).
  - *Note : DBeaver peut aussi le gérer automatiquement.*

---

## 2. Le client SQL : DBeaver

DBeaver est l'outil universel pour les Data Engineers. Il permet de se connecter à n'importe quelle base (Postgres, MySQL, Snowflake, DuckDB, etc.).

### Installation de DBeaver
1. Allez sur [dbeaver.io](https://dbeaver.io/download/).
2. Téléchargez la version **Community Edition** (Gratuite).
3. Installez et lancez l'application.

---

## 3. Alternative : Docker (PostgreSQL)

Si vous préférez utiliser un serveur plus traditionnel comme PostgreSQL, le plus simple est d'utiliser Docker :

```bash
docker run --name formation-sql -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

Vous pourrez ensuite vous y connecter via DBeaver avec :
- **Host** : `localhost`
- **Port** : `5432`
- **User** : `postgres`
- **Password** : `password`

---

[🏠 Accueil](../README.md) | [02 - Création de la BDD →](02-creation-bdd-import.md)
