# 01 - Introduction aux Jointures

[← Module 02](../02-Agregations-Groupby/04-exercices.md) | [🏠 Accueil](../README.md) | [02 - Types de Jointures →](02-types-jointures.md)

---

Dans une base de données relationnelle, les données sont normalisées (réparties dans plusieurs tables) pour éviter les doublons.

## 1. Clé Primaire et Clé Étrangère
- **Primary Key (PK)** : Identifiant unique d'une ligne (ex: `customers.id`).
- **Foreign Key (FK)** : Colonne qui référence la PK d'une autre table (ex: `orders.customer_id`).

## 2. Le principe de la jointure
La jointure permet de lier deux tables sur une colonne commune (généralement PK = FK).

```sql
SELECT orders.id, customers.first_name, orders.total_amount
FROM orders
JOIN customers ON orders.customer_id = customers.id;
```

---

[← Module 02](../02-Agregations-Groupby/04-exercices.md) | [🏠 Accueil](../README.md) | [02 - Types de Jointures →](02-types-jointures.md)