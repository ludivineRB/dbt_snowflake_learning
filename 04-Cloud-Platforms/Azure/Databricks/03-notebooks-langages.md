# 03 - Notebooks et langages

[← 02 - Configuration](02-configuration-workspace.md) | [🏠 Accueil](README.md) | [04 - Apache Spark et traitement de données →](04-spark-traitement.md)

---

## 🎯 Objectifs d'apprentissage

- Créer et organiser des notebooks Databricks
- Utiliser Python, SQL, Scala et R dans les notebooks
- Maîtriser les magic commands
- Créer des visualisations de données interactives
- Collaborer efficacement avec les widgets et le partage

## 1. Introduction aux notebooks Databricks

Les notebooks Databricks sont des documents interactifs qui combinent code, visualisations et texte narratif. Ils supportent plusieurs langages dans un même notebook.

## 2. Langages supportés

### Python (PySpark)
Le langage le plus populaire pour Data Science et Machine Learning sur Databricks.

### SQL
Pour les requêtes et analyses de données avec une syntaxe SQL familière.

### Scala
Langage natif de Spark, offrant les meilleures performances.

### R
Pour les statisticiens et analystes préférant R.

## 3. Magic Commands

Les magic commands permettent de mélanger plusieurs langages dans un même notebook.

| Magic Command | Description |
| --- | --- |
| `%python` | Exécuter du code Python |
| `%sql` | Exécuter une requête SQL |
| `%scala` | Exécuter du code Scala |
| `%r` | Exécuter du code R |
| `%md` | Cellule Markdown |
| `%sh` | Exécuter des commandes shell |
| `%fs` | Commandes filesystem (DBFS) |
| `%run` | Exécuter un autre notebook |

## 4. Visualisations de données

Databricks offre des visualisations intégrées puissantes avec la fonction `display()`.

## 5. Widgets et paramétrage

Les widgets permettent de créer des notebooks paramétrables et interactifs.

---

[← 02 - Configuration](02-configuration-workspace.md) | [🏠 Accueil](README.md) | [04 - Apache Spark et traitement de données →](04-spark-traitement.md)
