# 04 - Exercices : Jointures

[← 03 - Ensembles](03-operations-ensembles.md) | [🏠 Accueil](../README.md) | [Module 04 : DDL/DML →](../04-Conception-DDL-DML/README.md)

---

## Exercice 1 : INNER JOIN
1. Affichez le nom et prénom du client ainsi que la date de chaque commande qu'il a passée.
2. Affichez les noms des produits vendus dans la commande n°1 (utilisez `order_items` et `products`).

## Exercice 2 : LEFT JOIN
1. Listez tous les clients et le montant de leurs commandes. Ceux qui n'ont rien commandé doivent apparaître avec un montant `NULL`.
2. Identifiez les clients qui n'ont **jamais** passé de commande (astuce: utilisez `LEFT JOIN` et cherchez où l'id de la commande est `NULL`).

---

## 💡 Solutions

<details>
<summary>Voir les solutions</summary>

```sql
-- Ex 1.1
SELECT c.first_name, c.last_name, o.order_date
FROM customers c
JOIN orders o ON c.id = o.customer_id;

-- Ex 1.2
SELECT p.name
FROM order_items oi
JOIN products p ON oi.product_id = p.id
WHERE oi.order_id = 1;

-- Ex 2.1
SELECT c.first_name, o.total_amount
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;

-- Ex 2.2
SELECT c.first_name, c.last_name
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL;
```
</details>

---

[← 03 - Ensembles](03-operations-ensembles.md) | [🏠 Accueil](../README.md) | [Module 04 : DDL/DML →](../04-Conception-DDL-DML/README.md)