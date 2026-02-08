# Projet Final : Data Engineer Junior
## Sujet : Pipeline ETL E-Commerce (Bronze to Gold)

### 📝 Scénario
Vous travaillez pour un site e-commerce qui souhaite centraliser ses données de ventes et de clients pour faire de l'analyse décisionnelle.

### 🏗️ Architecture Attendue
1.  **Ingestion** : Script Python récupérant des données (API ou CSV source).
2.  **Stockage Bronze** : Données brutes stockées dans un Data Lake ou une table Raw.
3.  **Transformation (Silver)** : Nettoyage via SQL ou Spark (gestion des doublons, types de données, valeurs nulles).
4.  **Modélisation (Gold)** : Création d'un schéma en étoile (Table de Faits + Dimensions).
5.  **Industrialisation** : Le tout doit être packagé dans un container Docker.

### ✅ Critères de Validation
- [ ] Historique Git propre (Conventional Commits).
- [ ] Présence d'un fichier `docker-compose.yml` pour lancer la stack.
- [ ] Code Python respectant les standards PEP8.
- [ ] README détaillant comment lancer le pipeline.
