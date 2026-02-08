# 04 - Exercices : Agrégations

[← 03 - HAVING](03-having.md) | [🏠 Accueil](../README.md) | [Module 03 : Jointures →](../03-Jointures/README.md)

---

## Contexte
Utilisez les tables `orders` et `products`.

---

## Exercice 1 : Fonctions de base
1. Quel est le montant total de toutes les ventes (`total_amount` dans `orders`) ?
2. Quel est le prix du produit le plus cher ?
3. Combien de produits différents avons-nous en stock ?

## Exercice 2 : Groupements simples
1. Calculez le prix moyen des produits par catégorie.
2. Comptez le nombre de clients par pays.

## Exercice 3 : Filtrage avec HAVING
1. Listez les catégories qui ont un prix moyen supérieur à 100.
2. Affichez les pays qui ont plus de 3 clients.

---

## 💡 Solutions

<details>
<summary>Cliquez pour voir les solutions</summary>

### Exercice 1
```sql
-- 1.
SELECT SUM(total_amount) FROM orders;

-- 2.
SELECT MAX(price) FROM products;

-- 3.
SELECT COUNT(*) FROM products;
```

### Exercice 2
```sql
-- 1.
SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category;

-- 2.
SELECT country, COUNT(*) AS nb_customers
FROM customers
GROUP BY country;
```

### Exercice 3
```sql
-- 1.
SELECT category, AVG(price)
FROM products
GROUP BY category
HAVING AVG(price) > 100;

-- 2.
SELECT country, COUNT(*)
FROM customers
GROUP BY country
HAVING COUNT(*) > 3;
```

</details>

---

[← 03 - HAVING](03-having.md) | [🏠 Accueil](../README.md) | [Module 03 : Jointures →](../03-Jointures/README.md)