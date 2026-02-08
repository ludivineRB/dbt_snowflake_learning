# 02 - Transactions et ACID

[← 01 - Vues](01-vues.md) | [🏠 Accueil](../README.md) | [Module 08 : Projet Fil Rouge →](../08-Projet-Fil-Rouge/README.md)

---

Les transactions garantissent que plusieurs opérations sont traitées comme une seule unité atomique.

## 1. Propriétés ACID
- **A**tomicity : Tout ou rien.
- **C**onsistency : Cohérence des données.
- **I**solation : Les transactions ne s'interfèrent pas.
- **D**urability : Persistance après validation.

## 2. Syntaxe
```sql
BEGIN;

UPDATE orders SET total_amount = total_amount - 10 WHERE id = 1;
-- Imaginons une erreur ici
INSERT INTO logs (message) VALUES ('Remise appliquée');

COMMIT; -- Valide les changements
-- OU
ROLLBACK; -- Annule tout si un problème est survenu
```

---

[← 01 - Vues](01-vues.md) | [🏠 Accueil](../README.md) | [Module 08 : Projet Fil Rouge →](../08-Projet-Fil-Rouge/README.md)