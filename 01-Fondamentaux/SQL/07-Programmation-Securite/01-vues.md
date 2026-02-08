# 01 - Les Vues (Views)

[← Module 06](../06-Performance/02-indexation.md) | [🏠 Accueil](../README.md) | [02 - Transactions et ACID →](02-transactions-acid.md)

---

Une vue est une requête SQL sauvegardée que vous pouvez interroger comme une table.

## 1. Création d'une vue
```sql
CREATE VIEW active_premium_customers AS
SELECT id, first_name, email
FROM customers
WHERE city = 'Paris';
```

## 2. Vues Matérialisées
Contrairement à une vue classique, elle stocke physiquement les données du résultat. Utile pour les calculs lourds qui ne changent pas souvent.
```sql
-- Syntaxe Postgres/DuckDB
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT EXTRACT(MONTH FROM order_date) as month, SUM(total_amount)
FROM orders
GROUP BY 1;

-- Mise à jour
REFRESH MATERIALIZED VIEW monthly_sales_summary;
```

---

[← Module 06](../06-Performance/02-indexation.md) | [🏠 Accueil](../README.md) | [02 - Transactions et ACID →](02-transactions-acid.md)