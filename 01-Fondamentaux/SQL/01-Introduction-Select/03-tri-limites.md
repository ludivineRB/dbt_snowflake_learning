# 03 - Tri et Limitation

[← 02 - WHERE](02-filtrage-where.md) | [🏠 Accueil](../README.md) | [04 - Exercices →](04-exercices.md)

---

## 1. Trier les résultats (ORDER BY)

Par défaut, SQL ne garantit aucun ordre. On utilise `ORDER BY`.
- `ASC` : Croissant (par défaut).
- `DESC` : Décroissant.

```sql
SELECT product_name, price 
FROM products 
ORDER BY price DESC;
```

On peut trier sur plusieurs colonnes :
```sql
SELECT last_name, first_name 
FROM employees 
ORDER BY last_name ASC, first_name ASC;
```

---

## 2. Limiter les résultats (LIMIT)

Utile pour la pagination ou pour avoir un aperçu des données.

```sql
SELECT * FROM logs 
ORDER BY created_at DESC 
LIMIT 10;
```
*(Récupère les 10 entrées les plus récentes)*

---

## 3. Décalage (OFFSET)

Permet de sauter un certain nombre de lignes (utilisé pour la pagination).

```sql
-- Récupérer les résultats du 11ème au 20ème
SELECT * FROM products 
ORDER BY id 
LIMIT 10 OFFSET 10;
```

---

[← 02 - WHERE](02-filtrage-where.md) | [🏠 Accueil](../README.md) | [04 - Exercices →](04-exercices.md)