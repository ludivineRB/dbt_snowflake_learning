# 01 - Les CTE (Common Table Expressions)

[← Module 04](../04-Conception-DDL-DML/03-exercices.md) | [🏠 Accueil](../README.md) | [02 - Fonctions de Fenêtrage →](02-window-functions.md)

---

Les CTE permettent de définir des tables temporaires pour rendre vos requêtes plus lisibles et modulaires.

## 1. Syntaxe avec WITH
```sql
WITH customer_orders AS (
    SELECT customer_id, COUNT(*) as nb_orders
    FROM orders
    GROUP BY customer_id
)
SELECT c.first_name, co.nb_orders
FROM customers c
JOIN customer_orders co ON c.id = co.customer_id;
```

## 2. Avantages
- **Lisibilité** : Évite les sous-requêtes imbriquées difficiles à lire.
- **Réutilisation** : On peut appeler la même CTE plusieurs fois dans la même requête.

---

[← Module 04](../04-Conception-DDL-DML/03-exercices.md) | [🏠 Accueil](../README.md) | [02 - Fonctions de Fenêtrage →](02-window-functions.md)