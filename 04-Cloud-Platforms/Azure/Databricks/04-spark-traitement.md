# 04 - Apache Spark et traitement de données

[← 03 - Notebooks](03-notebooks-langages.md) | [🏠 Accueil](README.md) | [05 - Delta Lake et gestion des données →](05-delta-lake.md)

---

## 🎯 Objectifs d'apprentissage

- Comprendre l'architecture et les concepts d'Apache Spark
- Maîtriser les DataFrames et Datasets
- Effectuer des transformations et actions sur les données
- Utiliser Spark SQL pour requêter les données
- Optimiser les performances des requêtes

## 1. Architecture Apache Spark

Spark distribue le calcul sur plusieurs nœuds (Driver + Workers).

## 2. DataFrames et Datasets

Un DataFrame est une collection distribuée de données organisée en colonnes nommées.

```python
# Création depuis CSV
df_csv = spark.read.csv(
    "/path/to/data.csv",
    header=True,
    inferSchema=True
)
```

## 3. Transformations et Actions

- **Transformations (Lazy)** : select(), filter(), groupBy()
- **Actions (Eager)** : show(), count(), collect()

## 4. Spark SQL

```python
df.createOrReplaceTempView("employees")
result = spark.sql("SELECT * FROM employees WHERE age > 30")
```

## 5. Optimisation des performances

- **Partitionnement**
- **Mise en cache** (cache(), persist())
- **Broadcast Join**

---

[← 03 - Notebooks](03-notebooks-langages.md) | [🏠 Accueil](README.md) | [05 - Delta Lake et gestion des données →](05-delta-lake.md)
