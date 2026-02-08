# 02 - Création de la BDD et Import des données

[← 01 - Installation](01-installation-outils.md) | [🏠 Accueil](../README.md) | [Module 01 : Fondamentaux →](../01-Introduction-Select/README.md)

---

## 1. Créer une base de données avec DuckDB dans DBeaver

1. Ouvrez **DBeaver**.
2. Cliquez sur **Nouvelle Connexion** (l'icône de prise électrique en haut à gauche).
3. Recherchez **DuckDB** dans la liste et cliquez sur Suivant.
4. Dans le champ "Path", cliquez sur "Open" et choisissez un emplacement sur votre ordinateur pour enregistrer votre fichier de base de données (ex: `formation_sql.db`).
5. Cliquez sur **Terminer**. DBeaver vous proposera peut-être de télécharger les pilotes (drivers), acceptez.

---

## 2. Importer les données de pratique

Nous allons importer les fichiers CSV situés dans le dossier `data/` de ce cours.

### Via SQL (La méthode rapide avec DuckDB)
Ouvrez un éditeur SQL dans DBeaver et exécutez ces commandes :

```sql
-- Création de la table customers et import du CSV
CREATE TABLE customers AS 
SELECT * FROM read_csv_auto('../data/customers.csv');

-- Création de la table products
CREATE TABLE products AS 
SELECT * FROM read_csv_auto('../data/products.csv');

-- Création de la table orders
CREATE TABLE orders AS 
SELECT * FROM read_csv_auto('../data/orders.csv');

-- Création de la table order_items
CREATE TABLE order_items AS 
SELECT * FROM read_csv_auto('../data/order_items.csv');
```
*Note : Vérifiez bien le chemin vers vos fichiers CSV.*

### Via l'interface DBeaver (Méthode graphique)
1. Faites un clic droit sur votre connexion DuckDB > **Import Data**.
2. Choisissez **CSV**.
3. Sélectionnez votre fichier (ex: `customers.csv`).
4. Suivez l'assistant jusqu'à la fin.

---

## 3. Vérifier l'importation

Lancez une première requête pour vérifier que tout fonctionne :

```sql
SELECT * FROM customers LIMIT 5;
```

Si vous voyez vos données, bravo ! Votre environnement est prêt.

---

[← 01 - Installation](01-installation-outils.md) | [🏠 Accueil](../README.md) | [Module 01 : Fondamentaux →](../01-Introduction-Select/README.md)
