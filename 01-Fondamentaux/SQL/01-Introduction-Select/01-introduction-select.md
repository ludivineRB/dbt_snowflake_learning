# 01 - Introduction et SELECT

[← Précédent](../00-Preparation-Environnement/02-creation-bdd-import.md) | [🏠 Accueil](../README.md) | [02 - Filtrage avec WHERE →](02-filtrage-where.md)

---

## 1. Qu'est-ce qu'une base de données relationnelle (SGBDR) ?

Une base de données relationnelle stocke des données dans des **tables** (semblables à des feuilles Excel), qui sont reliées entre elles par des relations logiques. Le SQL (Structured Query Language) est le langage standard pour interagir avec ces bases.

### Concepts clés :
- **Table** : Une entité (ex: `Clients`, `Produits`).
- **Colonne (Champ)** : Un attribut de l'entité (ex: `email`, `nom`).
- **Ligne (Enregistrement)** : Une entrée unique dans la table.

---

## 2. La clause SELECT

C'est la commande de base pour extraire des données.

### Sélectionner toutes les colonnes
On utilise l'astérisque `*`.
```sql
SELECT * FROM employees;
```
*💡 Conseil : En production, évitez le `SELECT *` pour limiter la bande passante et améliorer les performances.*

### Sélectionner des colonnes précises
```sql
SELECT first_name, last_name, email 
FROM employees;
```

### Utiliser des Alias (AS)
Permet de renommer temporairement une colonne pour le résultat de la requête.
```sql
SELECT first_name AS prenom, last_name AS nom
FROM employees;
```

### Éliminer les doublons (DISTINCT)
```sql
SELECT DISTINCT city 
FROM customers;
```
*(Affiche la liste unique des villes présentes dans la table)*

---

[← Précédent](../00-Preparation-Environnement/02-creation-bdd-import.md) | [🏠 Accueil](../README.md) | [02 - Filtrage avec WHERE →](02-filtrage-where.md)