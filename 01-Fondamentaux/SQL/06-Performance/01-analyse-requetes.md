# 01 - Analyse des requêtes (EXPLAIN)

[← Module 05](../05-Fonctions-Avancees/03-exercices.md) | [🏠 Accueil](../README.md) | [02 - Indexation →](02-indexation.md)

---

Pour optimiser une requête, il faut d'abord comprendre comment le moteur de base de données l'exécute.

## 1. EXPLAIN et EXPLAIN ANALYZE
- `EXPLAIN` : Affiche le plan d'exécution prévu.
- `EXPLAIN ANALYZE` : Exécute réellement la requête et affiche les statistiques réelles.

```sql
EXPLAIN ANALYZE SELECT * FROM customers WHERE email = 'jean.dupont@email.com';
```

## 2. Seq Scan vs Index Scan
- **Seq Scan** : Lecture de toute la table (lent sur des millions de lignes).
- **Index Scan** : Utilisation d'un index pour un accès quasi-instantané.

---

[← Module 05](../05-Fonctions-Avancees/03-exercices.md) | [🏠 Accueil](../README.md) | [02 - Indexation →](02-indexation.md)