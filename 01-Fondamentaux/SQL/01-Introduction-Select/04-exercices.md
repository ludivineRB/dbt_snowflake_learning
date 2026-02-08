# 04 - Exercices : Fondamentaux

[← 03 - Tri et Limites](03-tri-limites.md) | [🏠 Accueil](../README.md) | [Module 02 : Agrégations →](../02-Agregations-Groupby/README.md)

---

## Contexte
Pour ces exercices, utilisez les tables `customers` et `products` que vous avez importées dans le Module 00.

---

## Exercice 1 : Premiers pas
1. Écrivez une requête pour sélectionner **tous** les clients.
2. Écrivez une requête pour ne sélectionner que les colonnes `first_name`, `last_name` et `email`.

## Exercice 2 : Filtrage simple
1. Sélectionnez les clients qui habitent en **France**.
2. Sélectionnez les clients qui ont plus de **30 ans**.

## Exercice 3 : Filtrage avancé
1. Sélectionnez les clients qui habitent à **Paris** ET qui ont moins de **25 ans**.
2. Sélectionnez les clients qui habitent soit en **France**, soit en **Belgique**. (Utilisez `IN`).
3. Trouvez les clients dont l'email se termine par `@gmail.com`.

## Exercice 4 : Tri et Limites
1. Affichez les 5 clients les plus jeunes (tri par âge croissant).
2. Affichez les noms et prénoms des clients, triés par ordre alphabétique du nom de famille.

## Exercice 5 : Le piège du NULL
1. Sélectionnez les clients dont la ville n'est pas renseignée (est `NULL`).

---

## 💡 Solutions

<details>
<summary>Cliquez pour voir les solutions</summary>

### Exercice 1
```sql
-- 1.
SELECT * FROM customers;

-- 2.
SELECT first_name, last_name, email FROM customers;
```

### Exercice 2
```sql
-- 1.
SELECT * FROM customers WHERE country = 'France';

-- 2.
SELECT * FROM customers WHERE age > 30;
```

### Exercice 3
```sql
-- 1.
SELECT * FROM customers 
WHERE city = 'Paris' AND age < 25;

-- 2.
SELECT * FROM customers 
WHERE country IN ('France', 'Belgique');

-- 3.
SELECT * FROM customers 
WHERE email LIKE '%@gmail.com';
```

### Exercice 4
```sql
-- 1.
SELECT * FROM customers 
ORDER BY age ASC 
LIMIT 5;

-- 2.
SELECT first_name, last_name 
FROM customers 
ORDER BY last_name ASC;
```

### Exercice 5
```sql
-- 1.
SELECT * FROM customers 
WHERE city IS NULL;
```

</details>

---

[← 03 - Tri et Limites](03-tri-limites.md) | [🏠 Accueil](../README.md) | [Module 02 : Agrégations →](../02-Agregations-Groupby/README.md)