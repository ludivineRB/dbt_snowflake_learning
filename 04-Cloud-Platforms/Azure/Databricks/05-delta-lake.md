# 05 - Delta Lake et gestion des données

[← 04 - Spark](04-spark-traitement.md) | [🏠 Accueil](README.md) | [06 - Workflows et orchestration →](06-workflows-orchestration.md)

---

## 🎯 Objectifs d'apprentissage

- Comprendre Delta Lake et ses avantages
- Créer et manipuler des tables Delta
- Utiliser les transactions ACID sur les données
- Exploiter le Time Travel pour l'audit et le rollback
- Optimiser et maintenir les tables Delta

## 1. Introduction à Delta Lake

Delta Lake apporte la fiabilité des bases de données aux data lakes.

## 2. Créer et manipuler des tables Delta

```python
# Écrire en format Delta
df.write.format("delta").mode("overwrite").save("/mnt/delta/sales")
```

## 3. Time Travel

```sql
SELECT * FROM sales VERSION AS OF 5;
```

## 4. Optimisation et maintenance

- **OPTIMIZE** : Compacter les fichiers.
- **Z-ORDER** : Clustering multi-dimensionnel.
- **VACUUM** : Nettoyer les anciens fichiers.

---

[← 04 - Spark](04-spark-traitement.md) | [🏠 Accueil](README.md) | [06 - Workflows et orchestration →](06-workflows-orchestration.md)
