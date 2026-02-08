# 03 - Filtrage des groupes avec HAVING

[← 02 - GROUP BY](02-group-by.md) | [🏠 Accueil](../README.md) | [04 - Exercices →](04-exercices.md)

---

La clause `HAVING` est au `GROUP BY` ce que le `WHERE` est au `SELECT`. Elle permet de filtrer les résultats **après** que les calculs d'agrégation ont été effectués.

## 1. Pourquoi ne pas utiliser WHERE ?
On ne peut pas filtrer sur le résultat d'une fonction d'agrégation avec `WHERE` car celui-ci s'exécute **avant** le groupement.

### Exemple : Trouver les villes ayant plus de 2 clients
```sql
-- CORRECT
SELECT city, COUNT(*)
FROM customers
GROUP BY city
HAVING COUNT(*) > 2;

-- INCORRECT (générera une erreur)
SELECT city, COUNT(*)
FROM customers
WHERE COUNT(*) > 2
GROUP BY city;
```

---

## 2. Combiner WHERE et HAVING
On peut utiliser les deux dans la même requête.
- `WHERE` : Filtre les lignes individuelles.
- `HAVING` : Filtre les groupes calculés.

```sql
SELECT category, AVG(price)
FROM products
WHERE price < 1000          -- Filtre sur les prix unitaires
GROUP BY category
HAVING AVG(price) > 50;     -- Filtre sur la moyenne calculée
```

---

[← 02 - GROUP BY](02-group-by.md) | [🏠 Accueil](../README.md) | [04 - Exercices →](04-exercices.md)