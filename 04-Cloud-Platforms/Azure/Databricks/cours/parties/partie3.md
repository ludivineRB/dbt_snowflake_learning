## 🎯 Objectifs d'apprentissage

- Créer et organiser des notebooks Databricks
- Utiliser Python, SQL, Scala et R dans les notebooks
- Maîtriser les magic commands
- Créer des visualisations de données interactives
- Collaborer efficacement avec les widgets et le partage

## 1. Introduction aux notebooks Databricks

Les notebooks Databricks sont des documents interactifs qui combinent code, visualisations et texte narratif. Ils supportent plusieurs langages dans un même notebook.

### Création d'un notebook

#### Créer votre premier notebook

1. Dans la barre latérale, cliquez sur `Workspace`
2. Naviguez vers votre dossier utilisateur
3. Clic droit → `Create` → `Notebook`
4. Nommez-le "Mon Premier Notebook"
5. Choisissez le langage par défaut : **Python**
6. Sélectionnez un cluster (ou créez-en un)

### Structure d'un notebook

#### Cellules de code

Exécutent du code Python, SQL, Scala ou R

#### Cellules Markdown

Documentation formatée avec titres, listes, images

#### Visualisations

Graphiques intégrés générés à partir des résultats

#### Widgets

Paramètres interactifs pour l'utilisateur

## 2. Langages supportés

### Python (PySpark)

Le langage le plus populaire pour Data Science et Machine Learning sur Databricks.

```bash
# Exemple Python dans un notebook Databricks
# Créer un DataFrame depuis une liste
data = [
    ("Alice", 34, "Data Engineer"),
    ("Bob", 45, "Data Scientist"),
    ("Charlie", 29, "ML Engineer")
]

df = spark.createDataFrame(data, ["name", "age", "role"])

# Afficher le contenu
display(df)

# Opérations sur le DataFrame
df_filtered = df.filter(df.age > 30)
display(df_filtered)

# Statistiques descriptives
df.describe().show()
```

### SQL

Pour les requêtes et analyses de données avec une syntaxe SQL familière.

```bash
-- Utiliser SQL dans une cellule
-- Créer une table temporaire
CREATE OR REPLACE TEMP VIEW employees AS
SELECT * FROM VALUES
  ('Alice', 34, 'Data Engineer', 95000),
  ('Bob', 45, 'Data Scientist', 105000),
  ('Charlie', 29, 'ML Engineer', 98000)
AS (name, age, role, salary);

-- Requête d'analyse
SELECT
  role,
  AVG(salary) as avg_salary,
  COUNT(*) as count
FROM employees
GROUP BY role
ORDER BY avg_salary DESC;
```

### Scala

Langage natif de Spark, offrant les meilleures performances.

```bash
// Exemple Scala
val data = Seq(
  ("Alice", 34, "Data Engineer"),
  ("Bob", 45, "Data Scientist"),
  ("Charlie", 29, "ML Engineer")
)

val df = data.toDF("name", "age", "role")
display(df)

// Transformations typées
case class Employee(name: String, age: Int, role: String)
val ds = df.as[Employee]
val seniors = ds.filter(_.age > 30)
display(seniors)
```

### R

Pour les statisticiens et analystes préférant R.

```bash
# Exemple R avec SparkR
library(SparkR)

df <- createDataFrame(data.frame(
  name = c("Alice", "Bob", "Charlie"),
  age = c(34, 45, 29),
  role = c("Data Engineer", "Data Scientist", "ML Engineer")
))

display(df)

# Utiliser ggplot2 pour visualisation
library(ggplot2)
local_df <- collect(df)
ggplot(local_df, aes(x=name, y=age)) +
  geom_bar(stat="identity", fill="steelblue")
```

## 3. Magic Commands

Les magic commands permettent de mélanger plusieurs langages dans un même notebook.

| Magic Command | Description | Exemple |
| --- | --- | --- |
| `%python` | Exécuter du code Python | Notebook par défaut SQL |
| `%sql` | Exécuter une requête SQL | Requêtes dans notebook Python |
| `%scala` | Exécuter du code Scala | Librairies Scala spécifiques |
| `%r` | Exécuter du code R | Analyses statistiques R |
| `%md` | Cellule Markdown | Documentation |
| `%sh` | Exécuter des commandes shell | Vérifier l'environnement |
| `%fs` | Commandes filesystem (DBFS) | Lister/copier des fichiers |
| `%run` | Exécuter un autre notebook | Modularisation du code |

### Exemples d'utilisation

```bash
# Cellule 1 : Python par défaut
data = [("Paris", 2.2), ("Lyon", 0.5), ("Marseille", 0.9)]
cities_df = spark.createDataFrame(data, ["city", "population_millions"])
cities_df.createOrReplaceTempView("cities")
```

```bash
-- Cellule 2 : Utiliser SQL sur les données Python
%sql
SELECT
  city,
  population_millions,
  ROUND(population_millions * 1000000) as population
FROM cities
ORDER BY population_millions DESC
```

```bash
%md
### Cellule 3 : Documentation Markdown

Les **trois plus grandes villes** de France :
1. Paris
2. Marseille
3. Lyon

*Données de population en millions d'habitants*
```

```bash
%sh
# Cellule 4 : Commandes shell
echo "Python version:"
python --version
echo "Spark version:"
spark-submit --version | head -1
```

```bash
%fs
# Cellule 5 : Opérations filesystem
ls /databricks-datasets/
```

## 4. Visualisations de données

Databricks offre des visualisations intégrées puissantes avec la fonction `display()`.

### Visualisations automatiques

```bash
# Créer des données de ventes
sales_data = [
    ("2024-01", "Produit A", 15000),
    ("2024-01", "Produit B", 12000),
    ("2024-02", "Produit A", 18000),
    ("2024-02", "Produit B", 14000),
    ("2024-03", "Produit A", 22000),
    ("2024-03", "Produit B", 16000)
]

sales_df = spark.createDataFrame(sales_data, ["month", "product", "revenue"])

# La fonction display() génère automatiquement des visualisations
display(sales_df)
```

#### Types de graphiques disponibles

- **Bar Chart :** Comparaisons catégorielles
- **Line Chart :** Évolutions temporelles
- **Pie Chart :** Proportions
- **Scatter Plot :** Corrélations
- **Map :** Données géospatiales
- **Box Plot :** Distributions statistiques

### Visualisations avec bibliothèques Python

```bash
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Convertir en Pandas pour visualisation
pandas_df = sales_df.toPandas()

# Créer un graphique avec matplotlib
plt.figure(figsize=(10, 6))
for product in pandas_df['product'].unique():
    data = pandas_df[pandas_df['product'] == product]
    plt.plot(data['month'], data['revenue'], marker='o', label=product)

plt.xlabel('Mois')
plt.ylabel('Revenu (€)')
plt.title('Évolution des revenus par produit')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Afficher dans Databricks
display(plt.gcf())
```

```bash
# Visualisation Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=pandas_df, x='month', y='revenue', hue='product', ax=ax)
ax.set_title('Comparaison des revenus')
ax.set_xlabel('Mois')
ax.set_ylabel('Revenu (€)')
plt.xticks(rotation=45)
display(fig)
```

## 5. Widgets et paramétrage

Les widgets permettent de créer des notebooks paramétrables et interactifs.

### Types de widgets

| Type | Fonction | Cas d'usage |
| --- | --- | --- |
| `text` | Champ de texte | Saisie de chemins, noms |
| `dropdown` | Liste déroulante | Sélection parmi options |
| `combobox` | Combinaison dropdown + texte | Options + saisie libre |
| `multiselect` | Sélection multiple | Filtres multiples |

### Création et utilisation de widgets

```bash
# Créer un widget dropdown pour sélectionner un pays
dbutils.widgets.dropdown("country", "France", ["France", "Allemagne", "Espagne", "Italie"])

# Créer un widget texte pour la date
dbutils.widgets.text("start_date", "2024-01-01")

# Créer un widget multiselect pour les catégories
dbutils.widgets.multiselect("categories", "Electronics", ["Electronics", "Clothing", "Food", "Books"])

# Récupérer les valeurs des widgets
selected_country = dbutils.widgets.get("country")
start_date = dbutils.widgets.get("start_date")
selected_categories = dbutils.widgets.get("categories")

print(f"Analyse pour {selected_country} à partir du {start_date}")
print(f"Catégories : {selected_categories}")

# Utiliser dans une requête
df = spark.sql(f"""
    SELECT * FROM sales
    WHERE country = '{selected_country}'
    AND date >= '{start_date}'
""")

display(df)

# Supprimer un widget
# dbutils.widgets.remove("country")

# Supprimer tous les widgets
# dbutils.widgets.removeAll()
```

#### Exercice pratique : Dashboard paramétré

Créez un notebook qui :

1. Crée un widget dropdown pour sélectionner un produit
2. Crée un widget texte pour spécifier un seuil de revenu
3. Filtre les données selon ces paramètres
4. Affiche un graphique des résultats

## 6. Collaboration et partage

### Fonctionnalités collaboratives

#### Édition multi-utilisateurs

Plusieurs personnes peuvent travailler simultanément sur un notebook

#### Commentaires

Ajoutez des commentaires sur des cellules spécifiques pour discussion

#### Contrôle de version

Historique des révisions intégré avec Git integration

#### Permissions

Contrôle d'accès granulaire (lecture, édition, exécution)

### Partage d'un notebook

#### Partager avec votre équipe

1. Ouvrez le notebook à partager
2. Cliquez sur `Share` en haut à droite
3. Ajoutez des utilisateurs ou groupes
4. Définissez les permissions :
   - **Can Read :** Lecture seule
   - **Can Run :** Lecture + exécution
   - **Can Edit :** Lecture + édition + exécution
5. Cliquez sur `Add`

### Intégration Git

```bash
# Configuration Git dans Databricks
# 1. Dans User Settings → Git Integration
# 2. Connectez votre compte GitHub/GitLab/Azure DevOps

# Cloner un repository
# Workspace → Add → Repo → Clone from Git
# URL: https://github.com/your-org/your-repo.git

# Les notebooks sont synchronisés avec le repo
# Commits et push depuis l'interface Databricks
```

### Export et partage de résultats

```bash
# Exporter un notebook en différents formats
# File → Export → DBC Archive (Databricks format)
# File → Export → Source File (.py, .scala, .r, .sql)
# File → Export → HTML
# File → Export → Jupyter Notebook (.ipynb)

# Partager les résultats via un dashboard
# Dans une cellule de visualisation :
# Cliquez sur "Add to Dashboard"
# Créez un nouveau dashboard ou ajoutez à un existant
```

## 7. Bonnes pratiques

### 💡 Recommandations

- **Organisation :** Structurez vos notebooks avec des sections Markdown claires
- **Nommage :** Utilisez des noms descriptifs (ex: "ETL\_Sales\_Daily" pas "Notebook1")
- **Modularité :** Utilisez %run pour réutiliser du code commun
- **Documentation :** Commentez votre code et utilisez des cellules Markdown
- **Performance :** Évitez de charger trop de données avec display(), limitez avec .limit()
- **Widgets :** Rendez vos notebooks paramétrables pour la réutilisation
- **Version Control :** Intégrez Git pour historique et collaboration
- **Nettoyage :** Supprimez les widgets avec removeAll() à la fin si nécessaire

#### Erreurs courantes à éviter

- Oublier de détacher le notebook avant de supprimer un cluster
- Utiliser `collect()` sur de très grandes DataFrames (risque OutOfMemory)
- Ne pas nettoyer les tables temporaires (créent du clutter)
- Hardcoder des chemins au lieu d'utiliser des widgets

### 📌 Points clés à retenir

- Notebooks supportent Python, SQL, Scala et R dans un même document
- Magic commands (%sql, %python, %md, %fs, %run) pour mélanger les langages
- display() génère des visualisations interactives automatiques
- Widgets créent des notebooks paramétrables et réutilisables
- Collaboration en temps réel avec commentaires et permissions
- Intégration Git pour version control professionnel

#### Prochaine étape

Vous maîtrisez les notebooks ! Dans la **Partie 4**, plongez dans Apache Spark et le traitement distribué de données.