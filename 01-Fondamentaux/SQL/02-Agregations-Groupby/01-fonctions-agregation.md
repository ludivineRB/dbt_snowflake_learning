# 01 - Fonctions d'agrégation

[← Module 01](../01-Introduction-Select/04-exercices.md) | [🏠 Accueil](../README.md) | [02 - Groupement (GROUP BY) →](02-group-by.md)

---

Les fonctions d'agrégation permettent de résumer un ensemble de données en une seule valeur statistique.

## 1. Les fonctions essentielles

- **`COUNT(*)`** : Compte le nombre total de lignes.
- **`COUNT(colonne)`** : Compte les valeurs non-nulles dans une colonne.
- **`SUM(colonne)`** : Calcule la somme totale.
- **`AVG(colonne)`** : Calcule la moyenne.
- **`MIN(colonne)`** / **`MAX(colonne)`** : Trouve la valeur la plus petite ou la plus grande.

### Exemples :
```sql
-- Nombre total de ventes (dans la table orders)
SELECT COUNT(*) FROM orders;

-- Chiffre d'affaires total
SELECT SUM(total_amount) FROM orders;

-- Prix moyen des produits
SELECT AVG(price) FROM products;
```

---

## 2. COUNT DISTINCT
Pour compter le nombre d'éléments uniques.
```sql
-- Combien de pays différents parmi nos clients ?
SELECT COUNT(DISTINCT country) FROM customers;
```

---

[← Module 01](../01-Introduction-Select/04-exercices.md) | [🏠 Accueil](../README.md) | [02 - Groupement (GROUP BY) →](02-group-by.md)