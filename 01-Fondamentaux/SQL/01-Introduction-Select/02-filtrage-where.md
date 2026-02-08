# 02 - Filtrage des données avec WHERE

[← 01 - SELECT](01-introduction-select.md) | [🏠 Accueil](../README.md) | [03 - Tri et Limites →](03-tri-limites.md)

---

La clause `WHERE` permet de restreindre les résultats aux lignes qui respectent une condition précise.

## 1. Opérateurs de comparaison
- `=` : Égal à
- `<>` ou `!=` : Différent de
- `>` / `<` : Supérieur / Inférieur
- `>=` / `<=` : Supérieur ou égal / Inférieur ou égal

```sql
SELECT * FROM products WHERE price > 100;
```

---

## 2. Opérateurs Logiques (AND, OR, NOT)

### AND (ET) : Toutes les conditions doivent être vraies.
```sql
SELECT * FROM employees 
WHERE department = 'IT' AND salary > 50000;
```

### OR (OU) : Au moins une condition doit être vraie.
```sql
SELECT * FROM products 
WHERE color = 'Red' OR color = 'Blue';
```

---

## 3. Filtrage avancé

### IN : Pour une liste de valeurs
```sql
SELECT * FROM customers 
WHERE country IN ('France', 'Belgique', 'Suisse');
```

### BETWEEN : Pour une plage de valeurs
```sql
SELECT * FROM orders 
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';
```

### LIKE : Pour la recherche textuelle (Pattern matching)
- `%` : Remplace n'importe quel nombre de caractères.
- `_` : Remplace un seul caractère.

```sql
SELECT * FROM users WHERE email LIKE '%@gmail.com';
```

---

## 4. Gestion des NULL
Le `NULL` représente l'absence de valeur. On ne peut pas utiliser `=` avec lui.

```sql
-- CORRECT
SELECT * FROM tasks WHERE completion_date IS NULL;

-- INCORRECT
SELECT * FROM tasks WHERE completion_date = NULL;
```

---

[← 01 - SELECT](01-introduction-select.md) | [🏠 Accueil](../README.md) | [03 - Tri et Limites →](03-tri-limites.md)