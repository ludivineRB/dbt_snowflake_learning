# 02 - Groupement des données (GROUP BY)

[← 01 - Agrégations](01-fonctions-agregation.md) | [🏠 Accueil](../README.md) | [03 - Filtrage (HAVING) →](03-having.md)

---

Le `GROUP BY` permet de segmenter les données selon une ou plusieurs colonnes pour leur appliquer des calculs d'agrégation.

## 1. Syntaxe de base

```sql
SELECT colonne, COUNT(*)
FROM table
GROUP BY colonne;
```

### Exemple : Nombre de clients par ville
```sql
SELECT city, COUNT(*) AS nb_customers
FROM customers
GROUP BY city;
```

---

## 2. La règle d'or

⚠️ **Toute colonne présente dans le `SELECT` qui n'est pas une fonction d'agrégation DOIT être présente dans la clause `GROUP BY`.**

### Exemple (Incorrect) :
```sql
-- Erreur : la colonne 'first_name' n'est pas groupée
SELECT city, first_name, COUNT(*) 
FROM customers 
GROUP BY city; 
```

---

## 3. Groupements multiples
On peut grouper par plusieurs colonnes.
```sql
-- Chiffre d'affaires par pays et par ville
SELECT 
    country,
    city,
    COUNT(*) AS nb_customers
FROM customers
GROUP BY country, city;
```

---

[← 01 - Agrégations](01-fonctions-agregation.md) | [🏠 Accueil](../README.md) | [03 - Filtrage (HAVING) →](03-having.md)