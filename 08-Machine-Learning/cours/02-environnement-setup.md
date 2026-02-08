# Chapitre 2 : Environnement et Outils

## 🎯 Objectifs

- Configurer un environnement ML complet et reproductible
- Maîtriser Jupyter Notebook pour l'expérimentation
- Savoir charger et explorer des datasets
- Réaliser une Analyse Exploratoire des Données (EDA) efficace
- Structurer un projet ML proprement

---

## 1. ⚙️ Installation de l'environnement

### 1.1 Installer uv (gestionnaire de packages moderne)

**uv** est un gestionnaire de packages Python ultra-rapide (écrit en Rust) qui remplace `pip`, `venv` et `pip-tools`. Il est **10 à 100x plus rapide** que pip.

```bash
# Installer uv (une seule fois)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Vérifier l'installation
uv --version
```

> 💡 **Conseil** : "uv est le futur de la gestion de packages Python. Il remplace pip, venv, pip-tools et même pyenv en un seul outil ultra-rapide."

### 1.2 Initialiser un projet ML

```bash
# Créer et initialiser un projet avec uv
uv init mon-projet-ml
cd mon-projet-ml

# uv crée automatiquement :
# - pyproject.toml (description du projet + dépendances)
# - .venv/ (environnement virtuel)
# - .python-version (version de Python)
```

### 1.3 Installer les packages essentiels

```bash
# Installation de tous les packages ML essentiels
uv add numpy pandas matplotlib seaborn scikit-learn jupyter ipykernel

# Optionnel mais recommandé
uv add missingno  # Visualisation des valeurs manquantes
uv add xgboost    # Algorithme de boosting performant
uv add plotly     # Visualisations interactives
```

> 💡 **Conseil de pro** : "Avec uv, pas besoin d'activer manuellement l'environnement virtuel. Utilisez `uv run python script.py` ou `uv run jupyter lab` pour exécuter dans le bon environnement automatiquement."

### 1.4 Gestion des dépendances avec `pyproject.toml`

uv gère les dépendances dans le fichier `pyproject.toml` (standard Python moderne) et génère automatiquement un `uv.lock` pour le verrouillage exact des versions :

```toml
# pyproject.toml (généré et maintenu par uv)
[project]
name = "mon-projet-ml"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "numpy>=1.26.4",
    "pandas>=2.2.0",
    "matplotlib>=3.8.2",
    "seaborn>=0.13.1",
    "scikit-learn>=1.4.0",
    "jupyter>=1.0.0",
    "ipykernel>=6.29.0",
    "missingno>=0.5.2",
]
```

```bash
# Pour reproduire l'environnement sur une autre machine
uv sync  # Installe exactement les mêmes versions grâce à uv.lock
```

> 💡 **Conseil de pro** : "Committez **toujours** votre `pyproject.toml` ET `uv.lock` dans votre dépôt Git. Un collègue peut reproduire votre environnement exact avec `uv sync`."

> ⚠️ **Attention** : "Ne pas verrouiller les versions est une source fréquente de bugs. Le code qui marche aujourd'hui peut casser demain si une bibliothèque est mise à jour avec des changements incompatibles. Le fichier `uv.lock` garantit la reproductibilité."

---

## 2. 📓 Jupyter Notebook : votre laboratoire

### 2.1 Pourquoi Jupyter pour le ML ?

Jupyter Notebook est l'outil de prédilection des data scientists pour plusieurs raisons :

| Avantage | Description |
|----------|-------------|
| **Itération rapide** | Exécuter cellule par cellule, pas besoin de relancer tout le script |
| **Visualisation inline** | Les graphiques s'affichent directement dans le notebook |
| **Documentation intégrée** | Mélanger code, texte Markdown, formules LaTeX |
| **Exploration** | Parfait pour l'EDA et l'expérimentation |
| **Partage** | Les notebooks `.ipynb` contiennent code + résultats + explications |

### 2.2 Lancer Jupyter

```bash
# Lancer Jupyter Notebook (interface classique)
jupyter notebook

# Ou Jupyter Lab (interface moderne, recommandée)
jupyter lab
```

### 2.3 Raccourcis essentiels

| Raccourci | Action | Mode |
|-----------|--------|------|
| `Shift + Enter` | Exécuter la cellule et passer à la suivante | Édition |
| `Ctrl + Enter` | Exécuter la cellule sans avancer | Édition |
| `A` | Insérer une cellule au-dessus | Commande |
| `B` | Insérer une cellule en-dessous | Commande |
| `DD` | Supprimer la cellule | Commande |
| `M` | Convertir en Markdown | Commande |
| `Y` | Convertir en Code | Commande |
| `Esc` | Passer en mode commande | Édition |
| `Enter` | Passer en mode édition | Commande |
| `Tab` | Autocomplétion | Édition |
| `Shift + Tab` | Afficher la documentation | Édition |

> 💡 **Conseil** : "Utilisez des cellules **Markdown** pour documenter vos hypothèses, vos observations et vos décisions. Un notebook bien documenté est un notebook réutilisable."

### 2.4 Bonnes pratiques Jupyter

```python
# Toujours commencer un notebook avec ces imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration pour de jolis graphiques
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# Afficher toutes les colonnes dans pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)

# Afficher les graphiques inline
%matplotlib inline

# Recharger automatiquement les modules modifiés
%load_ext autoreload
%autoreload 2
```

> 💡 **Conseil de pro** : "Créez un template de notebook avec ces imports et configurations. Vous gagnerez du temps à chaque nouveau projet."

### 2.5 Extensions utiles

| Extension | Utilité |
|-----------|---------|
| **Table of Contents** | Navigation dans les longs notebooks |
| **Variable Inspector** | Voir les variables en mémoire |
| **ExecuteTime** | Temps d'exécution de chaque cellule |
| **Collapsible Headings** | Plier/déplier des sections |
| **Nbextensions** | Collection d'extensions (Jupyter Notebook classique) |

---

## 3. 📊 Les datasets de démonstration

### 3.1 Datasets intégrés à scikit-learn

scikit-learn inclut des datasets classiques, parfaits pour apprendre :

```python
from sklearn import datasets

# --- Datasets pour la CLASSIFICATION ---

# Iris : classification de fleurs (3 classes, 4 features)
iris = datasets.load_iris()
X_iris, y_iris = iris.data, iris.target
print(f"Iris - Shape: {X_iris.shape}, Classes: {iris.target_names}")

# Digits : reconnaissance de chiffres manuscrits (10 classes, 64 features)
digits = datasets.load_digits()
X_digits, y_digits = digits.data, digits.target
print(f"Digits - Shape: {X_digits.shape}, Classes: {np.unique(y_digits)}")

# Breast Cancer : classification tumeur bénigne/maligne (2 classes, 30 features)
cancer = datasets.load_breast_cancer()
X_cancer, y_cancer = cancer.data, cancer.target
print(f"Cancer - Shape: {X_cancer.shape}, Classes: {cancer.target_names}")

# --- Datasets pour la RÉGRESSION ---

# California Housing : prédire le prix médian des maisons
housing = datasets.fetch_california_housing()
X_housing, y_housing = housing.data, housing.target
print(f"Housing - Shape: {X_housing.shape}, Target: prix médian")

# Diabetes : prédire la progression du diabète
diabetes = datasets.load_diabetes()
X_diabetes, y_diabetes = diabetes.data, diabetes.target
print(f"Diabetes - Shape: {X_diabetes.shape}")
```

### 3.2 Générer des datasets synthétiques

```python
from sklearn.datasets import make_classification, make_regression, make_blobs

# Générer un dataset de classification
X_classif, y_classif = make_classification(
    n_samples=1000,        # Nombre d'échantillons
    n_features=10,         # Nombre de features
    n_informative=5,       # Features réellement informatives
    n_redundant=2,         # Features redondantes
    n_classes=2,           # Nombre de classes
    random_state=42        # Reproductibilité
)

# Générer un dataset de régression
X_reg, y_reg = make_regression(
    n_samples=1000,
    n_features=5,
    noise=10,              # Niveau de bruit
    random_state=42
)

# Générer des clusters (pour le non-supervisé)
X_blobs, y_blobs = make_blobs(
    n_samples=500,
    centers=4,             # Nombre de clusters
    cluster_std=1.0,       # Écart-type des clusters
    random_state=42
)
```

> 💡 **Conseil** : "Les datasets synthétiques sont parfaits pour **comprendre** un algorithme car vous contrôlez les paramètres. Utilisez-les avant de passer à des données réelles."

### 3.3 Charger ses propres données

```python
# Depuis un fichier CSV
df = pd.read_csv("donnees.csv")

# Depuis un fichier Excel
df = pd.read_excel("donnees.xlsx", sheet_name="Feuille1")

# Depuis une base de données SQL
import sqlite3
conn = sqlite3.connect("base.db")
df = pd.read_sql("SELECT * FROM clients", conn)

# Depuis une URL
url = "https://raw.githubusercontent.com/datasets/iris/master/data/iris.csv"
df = pd.read_csv(url)
```

### 3.4 Tableau récapitulatif des datasets sklearn

| Dataset | Type | Samples | Features | Classes | Difficulté |
|---------|------|---------|----------|---------|------------|
| `load_iris` | Classification | 150 | 4 | 3 | ⭐ |
| `load_digits` | Classification | 1 797 | 64 | 10 | ⭐⭐ |
| `load_breast_cancer` | Classification | 569 | 30 | 2 | ⭐⭐ |
| `load_diabetes` | Régression | 442 | 10 | - | ⭐⭐ |
| `fetch_california_housing` | Régression | 20 640 | 8 | - | ⭐⭐⭐ |
| `make_classification` | Classification | Configurable | Configurable | Configurable | Variable |
| `make_regression` | Régression | Configurable | Configurable | - | Variable |

---

## 4. 🔍 Exploration de données (EDA)

L'Analyse Exploratoire des Données (EDA) est l'étape la plus importante avant toute modélisation.

> 💡 **Conseil de pro** : "Toujours visualiser vos données AVANT de modéliser. L'EDA permet de détecter des problèmes (valeurs manquantes, outliers, déséquilibres) et de formuler des hypothèses."

### 4.1 Vue d'ensemble du dataset

```python
import pandas as pd
import numpy as np

# Charger le dataset
df = pd.read_csv("donnees.csv")

# --- Informations générales ---
print("=== FORME DU DATASET ===")
print(f"Nombre de lignes : {df.shape[0]}")
print(f"Nombre de colonnes : {df.shape[1]}")

print("\n=== TYPES DE DONNÉES ===")
print(df.dtypes)

print("\n=== INFORMATIONS COMPLÈTES ===")
df.info()

print("\n=== PREMIÈRES LIGNES ===")
df.head(10)
```

### 4.2 Statistiques descriptives

```python
# Statistiques des variables numériques
print("=== STATISTIQUES NUMÉRIQUES ===")
print(df.describe())

# Statistiques des variables catégorielles
print("\n=== STATISTIQUES CATÉGORIELLES ===")
print(df.describe(include='object'))

# Distribution de la variable cible
print("\n=== DISTRIBUTION DE LA CIBLE ===")
print(df['target'].value_counts())
print(f"\nPourcentages :")
print(df['target'].value_counts(normalize=True) * 100)
```

### 4.3 Valeurs manquantes

```python
# Compter les valeurs manquantes
print("=== VALEURS MANQUANTES ===")
missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({'Manquantes': missing, 'Pourcentage': missing_pct})
print(missing_df[missing_df['Manquantes'] > 0].sort_values('Pourcentage', ascending=False))

# Visualisation avec missingno
import missingno as msno
msno.matrix(df, figsize=(12, 6))
plt.title("Matrice des valeurs manquantes")
plt.show()
```

> ⚠️ **Attention** : "Des valeurs manquantes supérieures à 50% sur une colonne sont souvent un signal pour la supprimer. Entre 5% et 50%, l'imputation est généralement appropriée."

### 4.4 Visualisations clés

```python
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Distributions des variables numériques ---
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
for i, col in enumerate(df.select_dtypes(include=[np.number]).columns[:6]):
    ax = axes[i // 3, i % 3]
    df[col].hist(bins=30, ax=ax, edgecolor='black')
    ax.set_title(f'Distribution de {col}')
plt.tight_layout()
plt.show()

# --- 2. Boxplots pour détecter les outliers ---
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, col in enumerate(df.select_dtypes(include=[np.number]).columns[:4]):
    sns.boxplot(y=df[col], ax=axes[i])
    axes[i].set_title(f'Boxplot de {col}')
plt.tight_layout()
plt.show()

# --- 3. Matrice de corrélation ---
plt.figure(figsize=(12, 8))
corr_matrix = df.select_dtypes(include=[np.number]).corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
            fmt='.2f', linewidths=0.5)
plt.title("Matrice de corrélation")
plt.tight_layout()
plt.show()

# --- 4. Scatter plots des features les plus corrélées ---
# Trouver les paires les plus corrélées avec la cible
if 'target' in df.columns:
    correlations = df.corr()['target'].drop('target').abs().sort_values(ascending=False)
    top_features = correlations.head(4).index

    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    for i, feat in enumerate(top_features):
        axes[i].scatter(df[feat], df['target'], alpha=0.3)
        axes[i].set_xlabel(feat)
        axes[i].set_ylabel('target')
        axes[i].set_title(f'Corrélation: {correlations[feat]:.2f}')
    plt.tight_layout()
    plt.show()

# --- 5. Distribution de la target (classification) ---
plt.figure(figsize=(8, 5))
sns.countplot(x='target', data=df)
plt.title("Distribution des classes")
plt.xlabel("Classe")
plt.ylabel("Nombre d'échantillons")
plt.show()
```

### 4.5 Checklist EDA

| Vérification | Code | Objectif |
|-------------|------|----------|
| Forme du dataset | `df.shape` | Combien de lignes/colonnes ? |
| Types de données | `df.dtypes` | Numérique vs catégoriel |
| Valeurs manquantes | `df.isnull().sum()` | Colonnes à imputer/supprimer |
| Statistiques | `df.describe()` | Moyennes, écarts-types, min/max |
| Distribution cible | `df['target'].value_counts()` | Classes déséquilibrées ? |
| Corrélations | `df.corr()` | Features liées entre elles ? |
| Outliers | Boxplots, IQR | Valeurs extrêmes à traiter ? |
| Distributions | Histogrammes | Normalité, asymétrie ? |

> 💡 **Conseil de pro** : "Documentez chaque observation de votre EDA dans des cellules Markdown. 'La colonne X a 15% de manquantes', 'La target est déséquilibrée 80/20', etc. Ce journal vous sera utile lors de la modélisation."

---

## 5. 📁 Structure d'un projet ML

### 5.1 Arborescence recommandée

```
mon-projet-ml/
│
├── data/                   # Données
│   ├── raw/                # Données brutes (jamais modifiées)
│   ├── processed/          # Données nettoyées/transformées
│   └── external/           # Données de sources externes
│
├── notebooks/              # Notebooks d'exploration
│   ├── 01-eda.ipynb        # Analyse exploratoire
│   ├── 02-preprocessing.ipynb
│   ├── 03-modeling.ipynb
│   └── 04-evaluation.ipynb
│
├── src/                    # Code source réutilisable
│   ├── __init__.py
│   ├── preprocessing.py    # Fonctions de preprocessing
│   ├── features.py         # Feature engineering
│   ├── models.py           # Entraînement des modèles
│   └── evaluation.py       # Fonctions d'évaluation
│
├── models/                 # Modèles sauvegardés (.pkl, .joblib)
│   └── model_v1.joblib
│
├── tests/                  # Tests unitaires
│   ├── test_preprocessing.py
│   └── test_models.py
│
├── reports/                # Rapports et visualisations
│   └── figures/
│
├── pyproject.toml          # Dépendances Python (géré par uv)
├── .gitignore              # Fichiers à exclure de Git
└── README.md               # Description du projet
```

### 5.2 Convention de nommage

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Fichiers Python | snake_case | `data_preprocessing.py` |
| Notebooks | Numérotés + descriptif | `01-exploration-donnees.ipynb` |
| Variables | snake_case | `train_data`, `n_features` |
| Classes | PascalCase | `DataPreprocessor` |
| Constantes | UPPER_SNAKE_CASE | `RANDOM_STATE = 42` |
| Modèles sauvegardés | Version + date | `model_v2_2024-01-15.joblib` |

### 5.3 Bonnes pratiques de reproductibilité

```python
# 1. TOUJOURS fixer le random_state
RANDOM_STATE = 42

# Partout dans le code :
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE
)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=RANDOM_STATE)

# 2. Sauvegarder les modèles
import joblib
joblib.dump(model, 'models/model_v1.joblib')
model_charge = joblib.load('models/model_v1.joblib')

# 3. Logger les résultats
resultats = {
    'modele': 'RandomForest',
    'parametres': model.get_params(),
    'accuracy_test': 0.95,
    'f1_test': 0.93,
    'date': '2024-01-15'
}
```

> 💡 **Conseil de pro** : "Un projet ML reproductible doit permettre à n'importe qui de cloner le dépôt, installer les dépendances et obtenir **les mêmes résultats**. Le `random_state` et le `uv.lock` sont vos meilleurs alliés."

### 5.4 Fichier `.gitignore` pour un projet ML

```gitignore
# Environnement virtuel
.venv/
.env

# Données volumineuses
data/raw/*.csv
data/raw/*.parquet
*.h5

# Modèles volumineux
models/*.pkl
models/*.joblib

# Jupyter checkpoints
.ipynb_checkpoints/

# Python cache
__pycache__/
*.pyc

# OS
.DS_Store
Thumbs.db
```

> ⚠️ **Attention** : "Ne versionnez **jamais** de fichiers de données volumineux dans Git. Utilisez Git LFS, DVC ou stockez-les sur un bucket cloud (S3, GCS)."

---

## 🎯 Points clés à retenir

1. **Environnement virtuel** obligatoire pour chaque projet (`uv init` + `pyproject.toml`)
2. **Jupyter Notebook** est l'outil idéal pour l'exploration et l'expérimentation
3. **scikit-learn** fournit des datasets de démo parfaits pour apprendre
4. **L'EDA** est une étape **non-négociable** avant toute modélisation
5. **Visualisez** toujours vos données : distributions, corrélations, outliers, manquantes
6. **Structurez** votre projet avec une arborescence claire et des conventions de nommage
7. **Reproductibilité** : `random_state`, `uv.lock`, sauvegarde des modèles
8. **Documentez** vos observations dans les notebooks (cellules Markdown)

---

## ✅ Checklist de validation

- [ ] J'ai créé un environnement virtuel pour mon projet ML
- [ ] J'ai installé numpy, pandas, matplotlib, seaborn, scikit-learn et jupyter
- [ ] J'ai un `pyproject.toml` et un `uv.lock` dans mon projet
- [ ] Je maîtrise les raccourcis de base de Jupyter Notebook
- [ ] Je sais charger un dataset sklearn (`load_iris`, `load_breast_cancer`, etc.)
- [ ] Je sais charger mes propres données (CSV, Excel, SQL)
- [ ] Je sais réaliser une EDA complète : shape, types, manquantes, statistiques, visualisations
- [ ] Je sais créer une matrice de corrélation avec seaborn
- [ ] Mon projet suit une arborescence propre (data/, notebooks/, src/, models/)
- [ ] J'ai un `.gitignore` adapté à un projet ML

---

**Précédent** : [Chapitre 1 : Introduction au Machine Learning](01-introduction-ml.md)

**Suivant** : [Chapitre 3 : Preprocessing – Préparer ses Données](03-preprocessing.md)
