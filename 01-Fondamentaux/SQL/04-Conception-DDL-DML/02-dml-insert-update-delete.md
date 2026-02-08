# 02 - DML : INSERT, UPDATE, DELETE

[← 01 - DDL](01-ddl-create-alter.md) | [🏠 Accueil](../README.md) | [03 - Exercices →](03-exercices.md)

---

Le DML (Data Manipulation Language) permet de manipuler les lignes de données.

## 1. INSERT INTO
```sql
INSERT INTO students (name, age) VALUES ('Alice', 22);
```

## 2. UPDATE
⚠️ **Ne pas oublier le WHERE !** Sans lui, toute la table est mise à jour.
```sql
UPDATE students SET age = 23 WHERE name = 'Alice';
```

## 3. DELETE
⚠️ **Ne pas oublier le WHERE !**
```sql
DELETE FROM students WHERE id = 1;
```

---

[← 01 - DDL](01-ddl-create-alter.md) | [🏠 Accueil](../README.md) | [03 - Exercices →](03-exercices.md)