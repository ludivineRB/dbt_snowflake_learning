# 02 - Fonctions de Fenêtrage (Window Functions)

[← 01 - CTEs](01-ctes-with.md) | [🏠 Accueil](../README.md) | [03 - Exercices →](03-exercices.md)

---

Les Window Functions effectuent un calcul sur un ensemble de lignes liées à la ligne actuelle, sans les regrouper (contrairement au `GROUP BY`).

## 1. RANK() et DENSE_RANK()
```sql
-- Classer les produits par prix dans chaque catégorie
SELECT 
    name, price, category,
    RANK() OVER (PARTITION BY category ORDER BY price DESC) as rank
FROM products;
```

## 2. LAG() et LEAD()
Accéder à la ligne précédente ou suivante.
```sql
-- Comparer le montant d'une commande avec la précédente
SELECT 
    id, order_date, total_amount,
    LAG(total_amount) OVER (ORDER BY order_date) as prev_amount
FROM orders;
```

## 3. Sommes cumulées
```sql
SELECT 
    order_date, total_amount,
    SUM(total_amount) OVER (ORDER BY order_date) as running_total
FROM orders;
```

---

[← 01 - CTEs](01-ctes-with.md) | [🏠 Accueil](../README.md) | [03 - Exercices →](03-exercices.md)