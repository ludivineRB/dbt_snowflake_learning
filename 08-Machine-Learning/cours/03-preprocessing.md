# Chapitre 3 : Preprocessing – Préparer ses Données

## 🎯 Objectifs

- Nettoyer et préparer des données pour le Machine Learning
- Maîtriser les techniques d'encodage des variables catégorielles
- Comprendre la différence entre normalisation et standardisation
- Gérer les valeurs manquantes et les outliers efficacement
- Construire des pipelines de preprocessing reproductibles avec scikit-learn
- Savoir traiter les classes déséquilibrées

---

## 1. 🧠 Pourquoi le preprocessing est crucial

Le preprocessing est l'étape la plus importante (et la plus longue) d'un projet ML. La qualité de vos données détermine directement la qualité de votre modèle.

### Le principe "Garbage in, Garbage out"

```
Données sales     → Modèle sophistiqué → Résultats médiocres  ❌
Données propres   → Modèle simple      → Bons résultats       ✅
Données propres   → Modèle sophistiqué → Excellents résultats ✅✅
```

> 💡 **Conseil** : "Un bon preprocessing vaut souvent mieux qu'un modèle plus complexe. Investissez du temps dans la préparation de vos données."

### Impact sur les performances

| Aspect du preprocessing | Impact potentiel sur le score |
|------------------------|-------------------------------|
| Gestion des valeurs manquantes | +5 à +15% |
| Encodage correct des catégorielles | +5 à +20% |
| Normalisation/Standardisation | +10 à +30% (pour SVM, KNN) |
| Gestion des outliers | +2 à +10% |
| Feature engineering | +10 à +50% |

> 💡 **Conseil de pro** : "Ne sous-estimez jamais le preprocessing. Les data scientists expérimentés y consacrent 60 à 80% de leur temps."

---

## 2. 🔧 Gestion des valeurs manquantes

### 2.1 Détecter les valeurs manquantes

```python
import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("donnees.csv")

# --- Détection des valeurs manquantes ---

# Nombre de manquantes par colonne
print("=== Valeurs manquantes par colonne ===")
print(df.isnull().sum())

# Pourcentage de manquantes
print("\n=== Pourcentage de manquantes ===")
pct_manquantes = (df.isnull().sum() / len(df)) * 100
print(pct_manquantes.sort_values(ascending=False))

# Résumé visuel
print(f"\nNombre total de valeurs manquantes : {df.isnull().sum().sum()}")
print(f"Pourcentage global : {(df.isnull().sum().sum() / df.size) * 100:.2f}%")
```

```python
# Visualisation avec missingno
import missingno as msno
import matplotlib.pyplot as plt

# Matrice de manquantes
msno.matrix(df, figsize=(12, 6))
plt.title("Matrice des valeurs manquantes")
plt.show()

# Heatmap de corrélation des manquantes
# (utile pour voir si les manquantes sont liées entre colonnes)
msno.heatmap(df, figsize=(10, 6))
plt.title("Corrélation des valeurs manquantes")
plt.show()
```

### 2.2 Stratégies de traitement

| Stratégie | Quand l'utiliser | Avantage | Inconvénient |
|-----------|-----------------|----------|-------------|
| **Suppression de lignes** | Peu de manquantes (<5%) | Simple | Perte de données |
| **Suppression de colonnes** | >50% manquantes | Élimine la colonne problématique | Perte d'information |
| **Imputation par la moyenne** | Numérique, peu de manquantes | Simple, rapide | Réduit la variance |
| **Imputation par la médiane** | Numérique avec outliers | Robuste aux outliers | Réduit la variance |
| **Imputation par le mode** | Catégoriel | Adapté aux catégories | Peut biaiser |
| **Imputation KNN** | Relations entre features | Plus précis | Plus lent |
| **Imputation par constante** | Signification métier du manquant | Explicite | Ajoute une "catégorie" |

### 2.3 Implémentation avec scikit-learn

```python
from sklearn.impute import SimpleImputer, KNNImputer

# --- Imputation par la moyenne (variables numériques) ---
imputer_mean = SimpleImputer(strategy='mean')
df_numerique_imputed = pd.DataFrame(
    imputer_mean.fit_transform(df[colonnes_numeriques]),
    columns=colonnes_numeriques
)

# --- Imputation par la médiane (si outliers) ---
imputer_median = SimpleImputer(strategy='median')
df_numerique_imputed = pd.DataFrame(
    imputer_median.fit_transform(df[colonnes_numeriques]),
    columns=colonnes_numeriques
)

# --- Imputation par le mode (variables catégorielles) ---
imputer_mode = SimpleImputer(strategy='most_frequent')
df_categoriel_imputed = pd.DataFrame(
    imputer_mode.fit_transform(df[colonnes_categorielles]),
    columns=colonnes_categorielles
)

# --- Imputation par une constante ---
imputer_const = SimpleImputer(strategy='constant', fill_value='Inconnu')
df_categoriel_imputed = pd.DataFrame(
    imputer_const.fit_transform(df[colonnes_categorielles]),
    columns=colonnes_categorielles
)

# --- Imputation KNN (plus sophistiquée) ---
imputer_knn = KNNImputer(n_neighbors=5)
df_knn_imputed = pd.DataFrame(
    imputer_knn.fit_transform(df[colonnes_numeriques]),
    columns=colonnes_numeriques
)
```

> ⚠️ **Attention** : "Ne **jamais** imputer AVANT le split train/test ! L'imputation doit être `fit` sur le train set et `transform` sur le test set. Sinon, vous avez du **data leakage** — le modèle 'voit' des informations du test set pendant l'entraînement."

```python
from sklearn.model_selection import train_test_split

# 1. Splitter D'ABORD
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Fit sur le train SEULEMENT, transform sur train ET test
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)  # fit + transform
X_test_imputed = imputer.transform(X_test)          # transform SEULEMENT
```

---

## 3. 📊 Gestion des valeurs aberrantes (outliers)

### 3.1 Détecter les outliers

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Méthode 1 : Boxplot (visuel) ---
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for i, col in enumerate(colonnes_numeriques[:4]):
    sns.boxplot(y=df[col], ax=axes[i])
    axes[i].set_title(f'{col}')
plt.suptitle("Détection des outliers par boxplot")
plt.tight_layout()
plt.show()

# --- Méthode 2 : IQR (Interquartile Range) ---
def detecter_outliers_iqr(df, colonne):
    """Détecte les outliers avec la méthode IQR"""
    Q1 = df[colonne].quantile(0.25)
    Q3 = df[colonne].quantile(0.75)
    IQR = Q3 - Q1
    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR
    outliers = df[(df[colonne] < borne_inf) | (df[colonne] > borne_sup)]
    return outliers, borne_inf, borne_sup

for col in colonnes_numeriques:
    outliers, b_inf, b_sup = detecter_outliers_iqr(df, col)
    print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")
    print(f"  Bornes: [{b_inf:.2f}, {b_sup:.2f}]")

# --- Méthode 3 : Z-Score ---
from scipy import stats

def detecter_outliers_zscore(df, colonne, seuil=3):
    """Détecte les outliers avec le Z-Score"""
    z_scores = np.abs(stats.zscore(df[colonne].dropna()))
    outliers = df[colonne].dropna()[z_scores > seuil]
    return outliers

for col in colonnes_numeriques:
    outliers = detecter_outliers_zscore(df, col)
    print(f"{col}: {len(outliers)} outliers (Z-Score > 3)")
```

### 3.2 Stratégies de traitement

| Stratégie | Implémentation | Quand l'utiliser |
|-----------|---------------|-----------------|
| **Suppression** | Supprimer les lignes | Peu d'outliers, clairement erronés |
| **Capping (winsorisation)** | Remplacer par la borne IQR | Valeurs extrêmes mais pas impossibles |
| **Transformation log** | `np.log1p(x)` | Distribution très asymétrique |
| **Ne rien faire** | Garder les outliers | Informations légitimes (ex: fraude) |

```python
# --- Capping avec IQR ---
def capper_outliers(df, colonne):
    """Remplace les outliers par les bornes IQR"""
    Q1 = df[colonne].quantile(0.25)
    Q3 = df[colonne].quantile(0.75)
    IQR = Q3 - Q1
    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR
    df[colonne] = df[colonne].clip(lower=borne_inf, upper=borne_sup)
    return df

# Appliquer sur chaque colonne numérique
for col in colonnes_numeriques:
    df = capper_outliers(df, col)

# --- Transformation logarithmique ---
# Utile pour les variables avec distribution très asymétrique (ex: revenus, prix)
df['prix_log'] = np.log1p(df['prix'])  # log(1+x) pour gérer les zéros
```

> 💡 **Conseil de pro** : "Avant de supprimer un outlier, demandez-vous : est-ce une erreur de saisie ou une observation légitime ? Un achat de 50 000€ peut être un outlier statistique mais un client VIP réel."

---

## 4. 🏷️ Encodage des variables catégorielles

Les algorithmes de ML ne comprennent que les **nombres**. Il faut donc convertir les variables catégorielles en représentations numériques.

### 4.1 Types de variables catégorielles

| Type | Description | Exemple | Encodage recommandé |
|------|------------|---------|---------------------|
| **Nominale** | Pas d'ordre entre les catégories | Couleur (rouge, bleu, vert) | One-Hot Encoding |
| **Ordinale** | Ordre significatif | Taille (S, M, L, XL) | Label/Ordinal Encoding |
| **Binaire** | Deux catégories | Sexe (H, F) | Label Encoding (0/1) |

### 4.2 Label Encoding (variables ordinales)

```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

# --- LabelEncoder : pour la variable cible ---
le = LabelEncoder()
df['target_encoded'] = le.fit_transform(df['target'])
# Ex: ['chat', 'chien', 'oiseau'] → [0, 1, 2]

# Inverser l'encodage
labels_originaux = le.inverse_transform([0, 1, 2])

# --- OrdinalEncoder : pour les features ordinales ---
# Spécifier l'ORDRE des catégories
categories_ordre = [['S', 'M', 'L', 'XL', 'XXL']]
oe = OrdinalEncoder(categories=categories_ordre)
df['taille_encoded'] = oe.fit_transform(df[['taille']])
# S→0, M→1, L→2, XL→3, XXL→4
```

> ⚠️ **Attention** : "N'utilisez **jamais** le Label Encoding pour des variables nominales (sans ordre). Le modèle interpréterait un ordre artificiel entre les catégories. Par exemple, si rouge=0, bleu=1, vert=2, le modèle croirait que vert > bleu > rouge."

### 4.3 One-Hot Encoding (variables nominales)

```python
from sklearn.preprocessing import OneHotEncoder

# --- Avec pandas (simple et rapide) ---
df_encoded = pd.get_dummies(df, columns=['couleur', 'ville'], drop_first=True)
# couleur_bleu, couleur_vert (rouge est la référence avec drop_first=True)

# --- Avec sklearn (recommandé pour les pipelines) ---
ohe = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
encoded = ohe.fit_transform(df[['couleur', 'ville']])
colonnes_ohe = ohe.get_feature_names_out(['couleur', 'ville'])
df_ohe = pd.DataFrame(encoded, columns=colonnes_ohe)
```

### 4.4 Tableau comparatif des encodages

| Critère | Label Encoding | One-Hot Encoding |
|---------|---------------|-----------------|
| **Type de variable** | Ordinale | Nominale |
| **Nombre de colonnes** | 1 (même colonne) | N-1 nouvelles colonnes |
| **Ordre implicite** | Oui (attention !) | Non |
| **Risque** | Faux ordre pour le nominale | Explosion dimensionnelle |
| **Compatible avec** | Arbres de décision | Tous les algorithmes |
| **Nombre de catégories** | Illimité | Limité (<50 idéalement) |

> 💡 **Conseil de pro** : "Attention au One-Hot Encoding avec trop de catégories (>50). Vous créez autant de colonnes que de catégories, ce qui peut mener à la **curse of dimensionality**. Dans ce cas, considérez le Target Encoding ou le Feature Hashing."

> 💡 **Conseil** : "Utilisez `drop='first'` dans le One-Hot Encoding pour éviter la multicolinéarité (le piège de la variable factice). Si vous avez 3 couleurs, 2 colonnes suffisent — la 3ème est implicite."

---

## 5. 📐 Normalisation et Standardisation

### 5.1 Pourquoi mettre à l'échelle ?

Certains algorithmes sont sensibles à l'**échelle** des features. Si une feature va de 0 à 1 000 000 et une autre de 0 à 1, la première dominera.

| Algorithme | Sensible à l'échelle ? | Scaling nécessaire ? |
|-----------|----------------------|---------------------|
| Régression linéaire | Partiellement | Recommandé |
| Régression logistique | Oui | Oui |
| SVM | **Très sensible** | **Obligatoire** |
| KNN | **Très sensible** | **Obligatoire** |
| Arbres de décision | Non | Non |
| Random Forest | Non | Non |
| Gradient Boosting | Non | Non |
| Réseaux de neurones | **Très sensible** | **Obligatoire** |

> 💡 **Conseil** : "SVM et KNN sont **très sensibles** à l'échelle des features. Toujours normaliser avant d'utiliser ces algorithmes. Les arbres de décision, eux, s'en moquent."

### 5.2 StandardScaler (Standardisation / Z-Score)

Centre les données à moyenne 0 et écart-type 1.

**Formule** : `z = (x - moyenne) / écart-type`

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Fit sur le train, transform sur train ET test
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Vérification
print(f"Moyenne après scaling : {X_train_scaled.mean(axis=0)}")   # ≈ 0
print(f"Écart-type après scaling : {X_train_scaled.std(axis=0)}") # ≈ 1
```

### 5.3 MinMaxScaler (Normalisation Min-Max)

Ramène les données dans l'intervalle [0, 1].

**Formule** : `x_norm = (x - min) / (max - min)`

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()  # Par défaut [0, 1]
# Ou : MinMaxScaler(feature_range=(0, 10)) pour [0, 10]

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Vérification
print(f"Min après scaling : {X_train_scaled.min(axis=0)}")  # 0
print(f"Max après scaling : {X_train_scaled.max(axis=0)}")  # 1
```

### 5.4 RobustScaler (Robuste aux outliers)

Utilise la médiane et l'IQR au lieu de la moyenne et l'écart-type.

**Formule** : `x_robust = (x - médiane) / IQR`

```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 5.5 Tableau comparatif des scalers

| Scaler | Formule | Résultat | Sensible outliers | Quand l'utiliser |
|--------|---------|---------|-------------------|-----------------|
| **StandardScaler** | `(x-μ)/σ` | Moyenne=0, Std=1 | Oui | Cas général, distribution ~normale |
| **MinMaxScaler** | `(x-min)/(max-min)` | Valeurs dans [0,1] | **Très sensible** | Quand on veut des bornes fixes |
| **RobustScaler** | `(x-médiane)/IQR` | Centré sur médiane | **Robuste** | Données avec beaucoup d'outliers |

> 💡 **Conseil de pro** : "En cas de doute, commencez par `StandardScaler`. Si vos données ont beaucoup d'outliers, passez à `RobustScaler`. Utilisez `MinMaxScaler` uniquement si vous avez besoin de valeurs dans [0, 1]."

> ⚠️ **Attention** : "Comme pour l'imputation, le scaler doit être `fit` sur le **train set uniquement** et `transform` sur le train ET le test set. Sinon = data leakage."

---

## 6. ✂️ Train / Test / Validation Split

### 6.1 Pourquoi splitter ?

Le but du ML est la **généralisation** — bien performer sur des données jamais vues. Le split permet de simuler cette situation.

```
Dataset complet (100%)
    │
    ├── Training set (80%) → Entraîner le modèle
    │
    └── Test set (20%) → Évaluer la généralisation
```

### 6.2 Implémentation

```python
from sklearn.model_selection import train_test_split

# Split classique 80/20
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 20% pour le test
    random_state=42,     # Reproductibilité
    shuffle=True         # Mélanger les données (par défaut)
)

print(f"Training set : {X_train.shape[0]} échantillons ({X_train.shape[0]/len(X)*100:.0f}%)")
print(f"Test set : {X_test.shape[0]} échantillons ({X_test.shape[0]/len(X)*100:.0f}%)")
```

### 6.3 Stratification (classes déséquilibrées)

```python
# SANS stratification → les proportions de classes peuvent être différentes
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Train: 70% classe 0, 30% classe 1 (aléatoire)

# AVEC stratification → les proportions sont conservées
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,          # Conserver les proportions de classes
    random_state=42
)
# Train: 65% classe 0, 35% classe 1 (comme le dataset original)

# Vérifier les proportions
print("Proportions dans le train set :")
print(pd.Series(y_train).value_counts(normalize=True))
print("\nProportions dans le test set :")
print(pd.Series(y_test).value_counts(normalize=True))
```

> ⚠️ **Attention** : "**TOUJOURS** splitter **AVANT** le preprocessing pour éviter le data leakage. L'ordre correct est : split → fit preprocessing sur train → transform train et test → entraîner le modèle."

### 6.4 Train / Validation / Test Split

Pour le tuning d'hyperparamètres, on ajoute un **validation set** :

```
Dataset complet (100%)
    │
    ├── Training set (60%) → Entraîner le modèle
    │
    ├── Validation set (20%) → Tuner les hyperparamètres
    │
    └── Test set (20%) → Évaluation finale (UNE SEULE FOIS)
```

```python
# Méthode : deux splits successifs
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.25, random_state=42, stratify=y_train_val
)
# 0.25 * 0.8 = 0.2 → 60% train, 20% val, 20% test

print(f"Train : {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"Validation : {len(X_val)} ({len(X_val)/len(X)*100:.0f}%)")
print(f"Test : {len(X_test)} ({len(X_test)/len(X)*100:.0f}%)")
```

> 💡 **Conseil de pro** : "Le **test set** ne doit être utilisé qu'**UNE SEULE FOIS** — pour l'évaluation finale. Si vous l'utilisez plusieurs fois pour ajuster votre modèle, vous faites du data leakage indirect."

---

## 7. 🔗 Pipelines scikit-learn

Les pipelines sont la façon **professionnelle** de construire un workflow de preprocessing. Ils garantissent la reproductibilité et évitent le data leakage.

### 7.1 Pipeline simple

```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# Pipeline avec noms explicites
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

# Ou version raccourcie (noms automatiques)
pipeline = make_pipeline(
    SimpleImputer(strategy='mean'),
    StandardScaler(),
    LogisticRegression()
)

# Utilisation : une seule ligne pour tout le workflow
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
score = pipeline.score(X_test, y_test)
print(f"Score : {score:.4f}")
```

### 7.2 ColumnTransformer (traitement différencié)

En pratique, les colonnes numériques et catégorielles nécessitent des traitements différents :

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Identifier les types de colonnes
colonnes_numeriques = ['age', 'revenu', 'score_credit']
colonnes_categorielles = ['ville', 'profession', 'statut_marital']

# --- Preprocessing pour les colonnes numériques ---
preprocessor_numerique = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# --- Preprocessing pour les colonnes catégorielles ---
preprocessor_categoriel = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
])

# --- Combiner les deux avec ColumnTransformer ---
preprocessor = ColumnTransformer([
    ('num', preprocessor_numerique, colonnes_numeriques),
    ('cat', preprocessor_categoriel, colonnes_categorielles)
])

# --- Pipeline complet : preprocessing + modèle ---
pipeline_complet = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Utilisation
pipeline_complet.fit(X_train, y_train)
predictions = pipeline_complet.predict(X_test)
score = pipeline_complet.score(X_test, y_test)
print(f"Score du pipeline complet : {score:.4f}")
```

### 7.3 Avantages des pipelines

| Avantage | Description |
|----------|-------------|
| **Pas de data leakage** | Le `fit` est automatiquement sur le train set |
| **Reproductibilité** | Tout le workflow en un objet |
| **Compatible GridSearch** | Tuner les hyperparamètres du preprocessing ET du modèle |
| **Déployable** | Sauvegarder un seul objet `pipeline.joblib` |
| **Lisible** | Le code est clair et structuré |

> 💡 **Conseil de pro** : "**Toujours** utiliser des pipelines en production. Cela évite le data leakage, rend le code reproductible et facilite le déploiement. Un pipeline = un objet qui fait tout."

### 7.4 Pipeline avec GridSearchCV

```python
from sklearn.model_selection import GridSearchCV

# Définir les hyperparamètres à tester
# Notez la syntaxe : 'étape__paramètre'
param_grid = {
    'preprocessor__num__imputer__strategy': ['mean', 'median'],
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [5, 10, None]
}

# GridSearch sur le pipeline complet
grid_search = GridSearchCV(
    pipeline_complet,
    param_grid,
    cv=5,                # 5-fold cross-validation
    scoring='f1',        # Métrique d'optimisation
    n_jobs=-1,           # Paralléliser
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"Meilleurs paramètres : {grid_search.best_params_}")
print(f"Meilleur score (F1) : {grid_search.best_score_:.4f}")

# Évaluer sur le test set
score_test = grid_search.score(X_test, y_test)
print(f"Score sur le test set : {score_test:.4f}")
```

---

## 8. ⚖️ Gestion des classes déséquilibrées

### 8.1 Le problème

Quand une classe est beaucoup plus fréquente que l'autre, le modèle a tendance à toujours prédire la classe majoritaire.

```python
# Exemple : 95% classe 0, 5% classe 1
print(pd.Series(y_train).value_counts())
# 0    9500
# 1     500

# Un modèle qui prédit TOUJOURS 0 a 95% d'accuracy → mais il est INUTILE !
```

> ⚠️ **Attention** : "Avec des classes déséquilibrées, ne **JAMAIS** regarder l'accuracy seule. Un modèle 'stupide' qui prédit toujours la classe majoritaire aura une accuracy élevée mais ne détectera jamais la classe minoritaire."

### 8.2 Solutions

| Solution | Description | Quand l'utiliser |
|----------|-------------|-----------------|
| **class_weight='balanced'** | Donne plus de poids à la classe minoritaire | Premier réflexe, simple |
| **SMOTE** | Crée des échantillons synthétiques de la classe minoritaire | Peu de données minoritaires |
| **Undersampling** | Réduit la classe majoritaire | Beaucoup de données |
| **Seuil ajusté** | Modifier le seuil de décision (pas 0.5) | Ajustement fin |
| **Métriques adaptées** | F1, AUC-ROC au lieu de l'accuracy | Toujours |

```python
# --- Solution 1 : class_weight='balanced' ---
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# La plupart des classifieurs sklearn supportent class_weight
modele = LogisticRegression(class_weight='balanced', random_state=42)
modele.fit(X_train, y_train)

# Ou avec Random Forest
modele_rf = RandomForestClassifier(class_weight='balanced', random_state=42)

# --- Solution 2 : SMOTE (sur-échantillonnage synthétique) ---
# uv add imbalanced-learn
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"Avant SMOTE : {pd.Series(y_train).value_counts().to_dict()}")
print(f"Après SMOTE : {pd.Series(y_train_resampled).value_counts().to_dict()}")
# Avant : {0: 9500, 1: 500}
# Après : {0: 9500, 1: 9500}

# --- Solution 3 : Undersampling ---
from imblearn.under_sampling import RandomUnderSampler

undersampler = RandomUnderSampler(random_state=42)
X_train_resampled, y_train_resampled = undersampler.fit_resample(X_train, y_train)
```

> ⚠️ **Attention** : "SMOTE ne doit **jamais** être appliqué sur le test set. On rééquilibre uniquement le **train set**."

### 8.3 Impact sur les métriques

```python
from sklearn.metrics import classification_report, f1_score, roc_auc_score

# Comparer les métriques avec et sans class_weight
modele_sans = LogisticRegression(random_state=42)
modele_avec = LogisticRegression(class_weight='balanced', random_state=42)

modele_sans.fit(X_train, y_train)
modele_avec.fit(X_train, y_train)

print("=== SANS class_weight ===")
print(classification_report(y_test, modele_sans.predict(X_test)))

print("=== AVEC class_weight='balanced' ===")
print(classification_report(y_test, modele_avec.predict(X_test)))
```

> 💡 **Conseil de pro** : "Avec des classes déséquilibrées, utilisez le **F1-Score** ou l'**AUC-ROC** comme métrique principale. L'accuracy est trompeuse et peut vous donner une fausse impression de performance."

---

## 🎯 Points clés à retenir

1. **"Garbage in, Garbage out"** : la qualité des données détermine la qualité du modèle
2. **Valeurs manquantes** : détecter d'abord, choisir la stratégie d'imputation ensuite (mean, median, mode, KNN)
3. **Outliers** : détecter (boxplot, IQR, Z-Score), puis décider (supprimer, capper, transformer)
4. **Encodage** : One-Hot pour le nominal, Ordinal pour l'ordinal, **jamais** de Label Encoding pour le nominal
5. **Scaling** : StandardScaler par défaut, RobustScaler si outliers, MinMaxScaler si besoin de bornes
6. **Split AVANT preprocessing** : c'est la règle d'or pour éviter le data leakage
7. **Pipelines sklearn** : utilisez-les toujours — reproductibilité, pas de leakage, déployable
8. **Classes déséquilibrées** : class_weight='balanced', SMOTE, et surtout les bonnes métriques (F1, AUC)
9. **Fit sur train, transform sur train et test** : ne jamais fit sur le test set
10. **ColumnTransformer** : traitement différencié pour colonnes numériques et catégorielles

---

## ✅ Checklist de validation

- [ ] Je sais détecter les valeurs manquantes et choisir une stratégie d'imputation
- [ ] Je sais détecter et traiter les outliers (IQR, Z-Score, capping)
- [ ] Je connais la différence entre Label Encoding et One-Hot Encoding
- [ ] Je sais quand utiliser StandardScaler, MinMaxScaler et RobustScaler
- [ ] Je sais splitter mes données AVANT le preprocessing
- [ ] Je maîtrise `train_test_split` avec stratification
- [ ] Je sais construire un pipeline sklearn avec ColumnTransformer
- [ ] Je comprends le data leakage et comment l'éviter
- [ ] Je sais gérer les classes déséquilibrées (class_weight, SMOTE)
- [ ] Je sais combiner Pipeline + GridSearchCV pour le tuning

---

**Précédent** : [Chapitre 2 : Environnement et Outils](02-environnement-setup.md)

**Suivant** : [Chapitre 4 : Régression – Prédire des Valeurs Continues](04-regression.md)
