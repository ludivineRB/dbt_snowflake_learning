# 01 - DDL : CREATE, ALTER, DROP

[← Module 03](../03-Jointures/04-exercices.md) | [🏠 Accueil](../README.md) | [02 - DML : INSERT, UPDATE, DELETE →](02-dml-insert-update-delete.md)

---

Le DDL (Data Definition Language) permet de définir la structure de la base.

## 1. CREATE TABLE
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT CHECK (age > 0)
);
```

## 2. ALTER TABLE
```sql
-- Ajouter une colonne
ALTER TABLE students ADD COLUMN email VARCHAR(255);
```

## 3. DROP TABLE
```sql
-- Supprimer une table
DROP TABLE IF EXISTS students;
```

---

[← Module 03](../03-Jointures/04-exercices.md) | [🏠 Accueil](../README.md) | [02 - DML : INSERT, UPDATE, DELETE →](02-dml-insert-update-delete.md)