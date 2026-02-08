# 03 - RDD Basics

[← 02 - Installation](02-installation-setup.md) | [🏠 Accueil](README.md) | [04 - DataFrames API →](04-dataframes-api.md)

---

## 1. Introduction aux RDDs

**RDD (Resilient Distributed Dataset)** est la structure de données fondamentale de Spark. C'est une collection immuable et distribuée d'objets.

## 2. Création de RDDs

```python
# À partir d'une collection
rdd = sc.parallelize([1, 2, 3, 4, 5])

# À partir d'un fichier texte
rdd = sc.textFile("data/logs.txt")
```

## 3. Transformations (Lazy)

- `map(f)` : Applique f à chaque élément.
- `filter(f)` : Garde les éléments où f est vrai.
- `flatMap(f)` : Map + aplatit.
- `reduceByKey(f)` : Réduit par clé.

## 4. Actions (Eager)

- `collect()` : Récupère tous les éléments.
- `count()` : Compte les éléments.
- `take(n)` : n premiers éléments.
- `reduce(f)` : Agrégation complète.

---

[← 02 - Installation](02-installation-setup.md) | [🏠 Accueil](README.md) | [04 - DataFrames API →](04-dataframes-api.md)
