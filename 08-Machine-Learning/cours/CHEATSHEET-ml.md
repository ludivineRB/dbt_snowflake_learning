# Cheatsheet Machine Learning

> Référence rapide pour le Data Engineer / Data Scientist. Gardez cette page sous la main pendant vos projets ML.

---

## 1. 🧭 Quel algorithme choisir ?

### Arbre de décision rapide

```
Données labellisées ?
├── OUI → Apprentissage supervisé
│   ├── Target numérique → RÉGRESSION
│   │   ├── Relations linéaires → LinearRegression / Ridge / Lasso
│   │   ├── Relations complexes → RandomForestRegressor / XGBRegressor
│   │   └── Peu de données → Ridge (régularisation)
│   │
│   └── Target catégorielle → CLASSIFICATION
│       ├── 2 classes, interprétable → LogisticRegression
│       ├── 2 classes, performance max → XGBClassifier / LightGBM
│       ├── Multi-classes → RandomForestClassifier / XGBClassifier
│       └── Texte / images → Deep Learning
│
└── NON → Apprentissage non-supervisé
    ├── Grouper des observations → CLUSTERING
    │   ├── Nombre de groupes connu → KMeans
    │   ├── Nombre inconnu → DBSCAN
    │   └── Hiérarchie souhaitée → AgglomerativeClustering
    │
    └── Réduire les dimensions → PCA / t-SNE / UMAP
```

### Tableau comparatif des algorithmes

| Algorithme | Type | Interprétable | Rapide | Gère le non-linéaire | Données nécessaires |
|---|---|---|---|---|---|
| LinearRegression | Régression | +++  | +++ | - | Peu |
| Ridge / Lasso | Régression | +++ | +++ | - | Peu |
| DecisionTree | Les deux | +++ | ++ | ++ | Peu |
| RandomForest | Les deux | + | ++ | +++ | Moyen |
| XGBoost | Les deux | + | ++ | +++ | Moyen |
| LogisticRegression | Classification | +++ | +++ | - | Peu |
| SVM | Les deux | + | + | ++ | Moyen |
| KNN | Les deux | ++ | - | ++ | Moyen |
| KMeans | Clustering | ++ | +++ | - | Moyen |
| DBSCAN | Clustering | + | ++ | +++ | Moyen |

> 💡 **Conseil de pro** : "En cas de doute, commencez par un Random Forest. Il marche bien dans 80% des cas, gère les features numériques et catégorielles, et ne nécessite pas de normalisation."

---

## 2. 📊 Métriques par type de problème

### Régression

| Métrique | Formule | Quand l'utiliser | Sensible aux outliers |
|---|---|---|---|
| **MAE** | mean(\|y - y_pred\|) | Erreur interprétable en unités | Non |
| **RMSE** | sqrt(mean((y - y_pred)^2)) | Pénaliser les grosses erreurs | Oui |
| **R2** | 1 - SS_res/SS_tot | Score global (0 à 1) | Oui |
| **MAPE** | mean(\|y - y_pred\|/\|y\|) * 100 | Erreur en pourcentage | Non |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
```

### Classification

| Métrique | Quand l'utiliser | Classes déséquilibrées ? |
|---|---|---|
| **Accuracy** | Classes équilibrées uniquement | NON |
| **Precision** | Coût élevé des faux positifs (spam) | OUI |
| **Recall** | Coût élevé des faux négatifs (cancer) | OUI |
| **F1-Score** | Équilibre precision/recall | OUI |
| **AUC-ROC** | Comparaison globale de modèles | OUI |

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)

# Rapport complet en une ligne
print(classification_report(y_test, y_pred))

# Métriques individuelles
f1 = f1_score(y_test, y_pred, average="weighted")
auc = roc_auc_score(y_test, model.predict_proba(X_test), multi_class="ovr")
```

> ⚠️ **Attention** : "N'utilisez JAMAIS l'accuracy seule sur des classes déséquilibrées. Un modèle qui prédit toujours la classe majoritaire aura 95% d'accuracy sur un jeu 95/5, mais sera complètement inutile."

### Clustering

| Métrique | Avec labels | Sans labels | Interprétation |
|---|---|---|---|
| **Silhouette** | Non | Oui | -1 (mauvais) à 1 (bon) |
| **Inertie** | Non | Oui | Plus bas = mieux (elbow method) |
| **ARI** | Oui | Non | 0 (aléatoire) à 1 (parfait) |
| **NMI** | Oui | Non | 0 à 1 |

```python
from sklearn.metrics import silhouette_score, adjusted_rand_score

sil = silhouette_score(X, labels_pred)
ari = adjusted_rand_score(labels_vrais, labels_pred)  # si labels disponibles
```

---

## 3. 🔧 Commandes sklearn essentielles

### Preprocessing

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

# Normalisation (moyenne=0, écart-type=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)         # fit + transform sur train
X_test_scaled = scaler.transform(X_test)          # transform SEULEMENT sur test

# Encodage one-hot
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_encoded = encoder.fit_transform(X_train[["ville", "type"]])
```

### Train/Test Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,       # 80/20
    random_state=42,     # Reproductibilité
    stratify=y           # Garder les proportions de classes
)
```

### Cross-Validation

```python
from sklearn.model_selection import cross_val_score, GridSearchCV

# Validation croisée rapide
scores = cross_val_score(model, X, y, cv=5, scoring="f1_weighted")
print(f"F1 moyen : {scores.mean():.4f} (+/- {scores.std():.4f})")

# Grid Search avec cross-validation
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 10, None],
}
grid = GridSearchCV(model, param_grid, cv=5, scoring="f1_weighted", n_jobs=-1)
grid.fit(X_train, y_train)
print(f"Meilleurs paramètres : {grid.best_params_}")
```

---

## 4. 🏗️ Template de Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Définir les colonnes
colonnes_num = ["age", "revenu", "nb_achats"]
colonnes_cat = ["ville", "type_contrat"]

# Pipeline numérique : imputation + normalisation
pipeline_num = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Pipeline catégoriel : imputation + encodage
pipeline_cat = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# Combiner les deux
preprocessor = ColumnTransformer([
    ("num", pipeline_num, colonnes_num),
    ("cat", pipeline_cat, colonnes_cat)
])

# Pipeline complet : preprocessing + modèle
pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Entraîner (le pipeline gère tout)
pipeline.fit(X_train, y_train)

# Prédire (données brutes, pas besoin de prétraiter)
y_pred = pipeline.predict(X_test)

# Sauvegarder le pipeline complet
import joblib
joblib.dump(pipeline, "model/pipeline_complet.joblib")
```

> 💡 **Conseil de pro** : "Sauvegardez TOUJOURS le pipeline complet (preprocessing + modèle), jamais le modèle seul. En production, vous passez des données brutes et le pipeline fait tout le travail."

---

## 5. 🚀 Checklist avant mise en production

### Qualité des données

- [ ] Pas de data leakage (le test set est vraiment isolé)
- [ ] Valeurs manquantes traitées dans le pipeline
- [ ] Outliers identifiés et gérés
- [ ] Features cohérentes entre train et production

### Modèle

- [ ] Métrique principale choisie ET justifiée
- [ ] Cross-validation effectuée (pas juste un train/test split)
- [ ] Hyperparamètres optimisés (GridSearch ou RandomSearch)
- [ ] Pas d'overfitting (écart train/test < 5%)
- [ ] Performance comparée à une baseline simple

### Déploiement

- [ ] Pipeline complet sauvegardé (preprocessing + modèle)
- [ ] API avec endpoint `/predict` et `/health`
- [ ] Validation des entrées (Pydantic)
- [ ] Tests unitaires + tests de performance du modèle
- [ ] Docker image construite et testée
- [ ] CI/CD configuré

### Monitoring

- [ ] Logging des prédictions activé
- [ ] Détection du data drift configurée
- [ ] Alertes en place (confiance basse, drift)
- [ ] Procédure de rollback documentée

---

## 6. 🐛 Erreurs courantes et solutions

| Erreur | Symptôme | Solution |
|---|---|---|
| **Data leakage** | Accuracy 99% sur test, nulle en prod | Séparer train/test AVANT tout preprocessing |
| **Overfitting** | Train=99%, Test=70% | Régularisation, plus de données, cross-validation |
| **Underfitting** | Train=60%, Test=58% | Modèle plus complexe, meilleur feature engineering |
| **Classes déséquilibrées** | Accuracy haute, recall bas | SMOTE, class_weight="balanced", F1 comme métrique |
| **Features non normalisées** | SVM/KNN marchent mal | StandardScaler dans le pipeline |
| **Categorical non encodé** | Erreur sklearn | OneHotEncoder dans le pipeline |
| **fit sur le test set** | Résultats optimistes | fit_transform sur train, transform sur test |
| **random_state oublié** | Résultats non reproductibles | Toujours fixer random_state=42 |
| **Pipeline incomplet** | Bug en production | Sauvegarder le pipeline complet (pas le modèle seul) |
| **Pas de baseline** | Impossible d'évaluer la valeur ajoutée | Comparer à DummyClassifier/DummyRegressor |

> 💡 **Conseil de pro** : "Si votre modèle a une accuracy suspectemement haute (>99%), cherchez du data leakage. C'est l'erreur la plus fréquente et la plus dangereuse en ML."

---

## 7. 📝 Commandes uv essentielles

```bash
# Initialiser un projet ML
uv init mon-projet-ml
cd mon-projet-ml

# Ajouter les dépendances ML courantes
uv add scikit-learn pandas numpy matplotlib seaborn
uv add xgboost lightgbm                          # Boosting
uv add mlflow                                     # Experiment tracking
uv add fastapi uvicorn                            # API
uv add joblib                                     # Sérialisation

# Ajouter des dépendances de développement
uv add --dev pytest ruff ipykernel jupyter

# Exécuter un script
uv run python src/train.py

# Lancer les tests
uv run pytest tests/ -v

# Lancer MLflow
uv run mlflow ui --port 5000

# Lancer l'API
uv run uvicorn app.main:app --reload --port 8000
```

---

[⬅️ Chapitre 10 : MLOps](10-mlops-production.md) | [🏠 Sommaire](../../README.md)
