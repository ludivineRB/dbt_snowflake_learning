# 02 - INNER, LEFT, RIGHT et FULL JOIN

[← 01 - Introduction](01-introduction-jointures.md) | [🏠 Accueil](../README.md) | [03 - Opérations d'Ensembles →](03-operations-ensembles.md)

---

## 1. INNER JOIN (Jointure Interne)
Retourne uniquement les lignes ayant une correspondance dans **les deux** tables. C'est le type par défaut quand vous écrivez juste `JOIN`.
```sql
SELECT c.first_name, o.id
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;
```

## 2. LEFT JOIN (Jointure Gauche)
Retourne **tous** les enregistrements de la table de gauche, et les correspondances de la table de droite (complété par des `NULL` si pas de match).
```sql
-- Tous les clients, même ceux qui n'ont jamais passé de commande
SELECT c.first_name, o.id
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id;
```

## 3. RIGHT JOIN
Retourne tous les enregistrements de la table de droite. Moins fréquent car on peut souvent inverser l'ordre des tables dans un `LEFT JOIN`.

---

[← 01 - Introduction](01-introduction-jointures.md) | [🏠 Accueil](../README.md) | [03 - Opérations d'Ensembles →](03-operations-ensembles.md)