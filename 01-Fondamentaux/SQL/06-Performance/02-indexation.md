# 02 - Indexation

[← 01 - EXPLAIN](01-analyse-requetes.md) | [🏠 Accueil](../README.md) | [Module 07 : Sécurité →](../07-Programmation-Securite/README.md)

---

Les index accélèrent les recherches mais ralentissent les écritures.

## 1. Création d'index
```sql
CREATE INDEX idx_customers_email ON customers(email);
```

## 2. Quand indexer ?
- Colonnes utilisées dans les clauses `WHERE`.
- Colonnes utilisées dans les jointures (`JOIN`).
- Colonnes utilisées pour le tri (`ORDER BY`).

## 3. Les pièges
- Ne pas indexer les colonnes à faible cardinalité (ex: Sexe, Pays si peu de pays).
- Éviter d'indexer toutes les colonnes d'une table (surcoût au stockage et à l'écriture).

---

[← 01 - EXPLAIN](01-analyse-requetes.md) | [🏠 Accueil](../README.md) | [Module 07 : Sécurité →](../07-Programmation-Securite/README.md)