# 03 - Opérations d'Ensembles (UNION, INTERSECT)

[← 02 - Types de Jointures](02-types-jointures.md) | [🏠 Accueil](../README.md) | [04 - Exercices →](04-exercices.md)

---

Contrairement aux jointures qui ajoutent des **colonnes**, les opérations d'ensembles ajoutent des **lignes**.

## 1. UNION et UNION ALL
Combine les résultats de deux requêtes.
- `UNION` : Supprime les doublons (plus lent).
- `UNION ALL` : Garde tous les résultats (plus rapide).

```sql
SELECT city FROM customers
UNION
SELECT city FROM suppliers;
```

## 2. INTERSECT et EXCEPT
- `INTERSECT` : Éléments présents dans les deux résultats.
- `EXCEPT` : Éléments de la première requête absents de la deuxième.

---

[← 02 - Types de Jointures](02-types-jointures.md) | [🏠 Accueil](../README.md) | [04 - Exercices →](04-exercices.md)