# Chapitre 4 : Régression – Prédire des Valeurs Continues

## 🎯 Objectifs

- Comprendre et implémenter la régression linéaire simple et multiple
- Maîtriser en profondeur les métriques de régression (MSE, RMSE, MAE, R², MAPE)
- Appliquer la régularisation (Ridge, Lasso, ElasticNet) pour éviter l'overfitting
- Comprendre le Gradient Descent et la régression polynomiale
- Savoir diagnostiquer et améliorer un modèle de régression

---

## 1. 📈 La régression linéaire simple

### 1.1 Concept

La régression linéaire simple modélise la relation entre **une feature** (x) et **une target** (y) par une droite :

```
y = a * x + b

Où :
- a = pente (coefficient directeur) → l'effet de x sur y
- b = ordonnée à l'origine (intercept) → la valeur de y quand x = 0
```

L'algorithme cherche les valeurs de `a` et `b` qui **minimisent** la somme des erreurs au carré entre les prédictions et les valeurs réelles. C'est la méthode des **moindres carrés ordinaires** (OLS – Ordinary Least Squares).

### 1.2 Implémentation avec scikit-learn

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# --- Générer des données ---
np.random.seed(42)
surface = np.random.uniform(20, 150, 200)  # Surface en m²
prix = 3000 * surface + 50000 + np.random.normal(0, 30000, 200)  # Prix en €

# Créer un DataFrame
df = pd.DataFrame({'surface': surface, 'prix': prix})

# --- Préparer les données ---
X = df[['surface']]  # Features (2D obligatoire pour sklearn)
y = df['prix']       # Target

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Entraîner le modèle ---
modele = LinearRegression()
modele.fit(X_train, y_train)

# Coefficients appris
print(f"Coefficient (pente) : {modele.coef_[0]:.2f} €/m²")
print(f"Intercept : {modele.intercept_:.2f} €")
# → "Pour chaque m² supplémentaire, le prix augmente de ~3000€"

# --- Prédire ---
y_pred = modele.predict(X_test)

# --- Visualiser ---
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, alpha=0.6, label='Données réelles')
plt.plot(X_test.sort_values('surface'),
         modele.predict(X_test.sort_values('surface')),
         color='red', linewidth=2, label='Régression linéaire')
plt.xlabel('Surface (m²)')
plt.ylabel('Prix (€)')
plt.title('Régression linéaire : Prix vs Surface')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

> 💡 **Conseil** : "La régression linéaire est le modèle le plus simple et le plus interprétable. Commencez **toujours** par une régression linéaire comme baseline avant d'essayer des modèles plus complexes."

---

## 2. 📊 La régression linéaire multiple

### 2.1 Concept

La régression multiple utilise **plusieurs features** pour prédire la target :

```
y = b₀ + b₁*x₁ + b₂*x₂ + b₃*x₃ + ... + bₙ*xₙ

Où :
- b₀ = intercept
- b₁, b₂, ..., bₙ = coefficients (un par feature)
- x₁, x₂, ..., xₙ = features
```

### 2.2 Implémentation

```python
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np

# --- Charger les données ---
housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df['prix'] = housing.target  # Prix médian en centaines de milliers de $

print("=== Features disponibles ===")
print(df.columns.tolist())
print(f"\nShape : {df.shape}")
print(f"\nDescription :\n{df.describe()}")

# --- Préparer ---
X = df.drop('prix', axis=1)
y = df['prix']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardiser (recommandé pour interpréter les coefficients)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Entraîner ---
modele = LinearRegression()
modele.fit(X_train_scaled, y_train)

# --- Interpréter les coefficients ---
coefs = pd.DataFrame({
    'Feature': housing.feature_names,
    'Coefficient': modele.coef_
}).sort_values('Coefficient', key=abs, ascending=False)

print("\n=== Coefficients (données standardisées) ===")
print(coefs)
print(f"\nIntercept : {modele.intercept_:.4f}")

# Visualiser l'importance des features
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.barh(coefs['Feature'], coefs['Coefficient'])
plt.xlabel('Coefficient (impact sur le prix)')
plt.title('Importance des features (régression linéaire)')
plt.axvline(x=0, color='black', linestyle='--')
plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "Standardisez vos features avant de comparer les coefficients. Sans standardisation, un coefficient de 1000 pour une feature en mètres n'est pas comparable à un coefficient de 0.01 pour une feature en kilomètres."

### 2.3 Hypothèses de la régression linéaire

| Hypothèse | Description | Comment vérifier |
|-----------|-------------|-----------------|
| **Linéarité** | Relation linéaire entre X et y | Scatter plots, résidus vs prédictions |
| **Indépendance** | Les erreurs sont indépendantes | Durbin-Watson test |
| **Homoscédasticité** | Variance constante des erreurs | Résidus vs prédictions (pas de cône) |
| **Normalité des résidus** | Erreurs ≈ distribution normale | QQ-Plot, test de Shapiro-Wilk |
| **Pas de multicolinéarité** | Features pas trop corrélées entre elles | VIF (Variance Inflation Factor) |

> ⚠️ **Attention** : "En pratique, ces hypothèses sont rarement parfaitement respectées. Mais les vérifier vous aide à comprendre les limites de votre modèle et à choisir la bonne technique."

---

## 3. 📊 MÉTRIQUES DE RÉGRESSION

Les métriques sont **essentielles** pour évaluer la qualité d'un modèle de régression. Chacune a ses forces et faiblesses.

### 3.1 MSE – Mean Squared Error (Erreur Quadratique Moyenne)

**Formule** : `MSE = (1/n) * Σ(yᵢ - ŷᵢ)²`

```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_test, y_pred)
print(f"MSE : {mse:.4f}")
```

| Propriété | Détail |
|-----------|--------|
| **Interprétation** | Moyenne des erreurs au carré |
| **Unité** | Unité² (ex: €² → pas intuitif) |
| **Sensible aux outliers** | ⚠️ Oui, très (les erreurs sont au carré) |
| **Quand l'utiliser** | Quand on veut pénaliser fortement les grosses erreurs |
| **Valeur idéale** | 0 |

### 3.2 RMSE – Root Mean Squared Error (Racine de l'Erreur Quadratique Moyenne)

**Formule** : `RMSE = √MSE = √[(1/n) * Σ(yᵢ - ŷᵢ)²]`

```python
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# Ou directement :
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE : {rmse:.4f}")
```

| Propriété | Détail |
|-----------|--------|
| **Interprétation** | Erreur moyenne dans la même unité que la cible |
| **Unité** | Même unité que y (ex: € → interprétable !) |
| **Sensible aux outliers** | ⚠️ Oui (hérité du MSE) |
| **Quand l'utiliser** | Quand on veut une erreur interprétable dans l'unité cible |
| **Valeur idéale** | 0 |

> 💡 **Conseil** : "Le RMSE est souvent préféré au MSE car il est dans la **même unité** que la cible. Un RMSE de 15 000€ sur des prix d'appartements est plus parlant qu'un MSE de 225 000 000€²."

### 3.3 MAE – Mean Absolute Error (Erreur Absolue Moyenne)

**Formule** : `MAE = (1/n) * Σ|yᵢ - ŷᵢ|`

```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, y_pred)
print(f"MAE : {mae:.4f}")
```

| Propriété | Détail |
|-----------|--------|
| **Interprétation** | Erreur moyenne absolue |
| **Unité** | Même unité que y |
| **Sensible aux outliers** | ✅ Plus robuste que RMSE (pas de carré) |
| **Quand l'utiliser** | Quand on veut une mesure robuste aux outliers |
| **Valeur idéale** | 0 |

### 3.4 R² – Coefficient de détermination

**Formule** : `R² = 1 - (SS_res / SS_tot)` où `SS_res = Σ(yᵢ - ŷᵢ)²` et `SS_tot = Σ(yᵢ - ȳ)²`

```python
from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)
print(f"R² : {r2:.4f}")
# Ou directement avec le modèle :
print(f"R² (score) : {modele.score(X_test, y_test):.4f}")
```

| Propriété | Détail |
|-----------|--------|
| **Interprétation** | % de variance de y expliqué par le modèle |
| **Plage** | ]-∞, 1] (1 = parfait, 0 = prédit la moyenne, <0 = pire que la moyenne) |
| **Sans unité** | ✅ Comparable entre datasets |
| **Quand l'utiliser** | Pour une vue d'ensemble de la qualité du modèle |
| **Limite** | Peut être trompeur si peu de variance dans y |

> ⚠️ **Attention** : "Un R² de 0.99 ne veut pas dire que le modèle est parfait. Vérifiez toujours avec RMSE/MAE. Et un R² qui augmente toujours quand on ajoute des features → utilisez le **R² ajusté**."

**R² ajusté** : pénalise l'ajout de features non-informatives.

```python
def r2_ajuste(r2, n, p):
    """
    Calcule le R² ajusté
    r2 : R² classique
    n  : nombre d'observations
    p  : nombre de features
    """
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)

n = len(y_test)
p = X_test.shape[1]
r2_adj = r2_ajuste(r2, n, p)
print(f"R² ajusté : {r2_adj:.4f}")
```

### 3.5 MAPE – Mean Absolute Percentage Error

**Formule** : `MAPE = (1/n) * Σ|( yᵢ - ŷᵢ) / yᵢ| * 100`

```python
from sklearn.metrics import mean_absolute_percentage_error

mape = mean_absolute_percentage_error(y_test, y_pred) * 100
print(f"MAPE : {mape:.2f}%")
```

| Propriété | Détail |
|-----------|--------|
| **Interprétation** | Erreur moyenne en pourcentage |
| **Unité** | % (très interprétable par les métiers) |
| **Quand l'utiliser** | Quand on veut communiquer l'erreur aux non-techniques |
| **Limite** | ⚠️ Problème si y contient des valeurs proches de 0 (division par ~0) |

> 💡 **Conseil de pro** : "Le MAPE est **idéal** pour communiquer avec les équipes métier. 'Notre modèle se trompe en moyenne de 8%' est beaucoup plus parlant que 'Le RMSE est de 12 345'."

### 3.6 Tableau comparatif complet des métriques

| Métrique | Formule simplifiée | Unité | Sensible outliers | Interprétable | Quand l'utiliser |
|----------|-------------------|-------|-------------------|---------------|-----------------|
| **MSE** | Moyenne(erreur²) | Unité² | ⚠️ Très | ❌ Non | Optimisation, pénaliser grosses erreurs |
| **RMSE** | √MSE | Unité | ⚠️ Oui | ✅ Oui | Métrique par défaut, erreur interprétable |
| **MAE** | Moyenne(\|erreur\|) | Unité | ✅ Robuste | ✅ Oui | Données avec outliers |
| **R²** | 1 - SS_res/SS_tot | Sans | Modéré | ✅ Oui | Vue d'ensemble, comparaison |
| **MAPE** | Moyenne(\|erreur/y\|) | % | Modéré | ✅✅ Très | Communication métier |

> 💡 **Conseil de pro** : "Toujours reporter **PLUSIEURS** métriques. R² seul peut être trompeur si les données ont peu de variance. RMSE seul ne dit rien sur la proportion d'erreur. Utilisez au minimum **R² + RMSE + MAE**."

### 3.7 Exemple complet d'évaluation

```python
import numpy as np
from sklearn.metrics import (mean_squared_error, mean_absolute_error,
                             r2_score, mean_absolute_percentage_error)

def evaluer_regression(y_true, y_pred, nom_modele="Modèle"):
    """Évalue un modèle de régression avec toutes les métriques"""
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100

    print(f"=== Évaluation : {nom_modele} ===")
    print(f"MSE  : {mse:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"MAE  : {mae:.4f}")
    print(f"R²   : {r2:.4f}")
    print(f"MAPE : {mape:.2f}%")
    print()

    return {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'R2': r2, 'MAPE': mape}

# Utilisation
resultats = evaluer_regression(y_test, y_pred, "Régression Linéaire")
```

---

## 4. ⚙️ Le Gradient Descent (Descente de Gradient)

### 4.1 Intuition

Imaginez que vous êtes au sommet d'une montagne, **les yeux bandés**, et vous voulez descendre au point le plus bas. Vous tâtez le sol autour de vous et faites un pas dans la direction de la plus forte descente. C'est le **Gradient Descent**.

```
  Fonction de coût (erreur)
       │
  High │  ●  Début (paramètres aléatoires)
       │   ╲
       │    ╲
       │     ●  Pas 1
       │      ╲
       │       ●  Pas 2
       │        ╲
       │         ● Minimum (paramètres optimaux)
       └──────────────────── Paramètre
```

### 4.2 Le Learning Rate

Le **learning rate** (taux d'apprentissage) contrôle la taille des pas :

| Learning Rate | Comportement | Résultat |
|--------------|-------------|---------|
| **Trop grand** | Grands pas → saute par-dessus le minimum | ❌ Diverge, ne converge jamais |
| **Trop petit** | Petits pas → avance très lentement | ⚠️ Converge, mais trop lent |
| **Optimal** | Pas adaptés | ✅ Converge rapidement |

> 💡 **Conseil** : "Un bon learning rate est généralement entre 0.001 et 0.1. Commencez par 0.01 et ajustez."

### 4.3 Variantes du Gradient Descent

| Variante | Données utilisées par pas | Vitesse | Stabilité |
|----------|--------------------------|---------|-----------|
| **Batch GD** | Toutes les données | Lent | Stable |
| **Stochastic GD (SGD)** | Un échantillon | Rapide | Bruyant |
| **Mini-batch GD** | Un sous-ensemble (32-256) | Bon compromis | Bon compromis |

```python
from sklearn.linear_model import SGDRegressor

# Régression avec Stochastic Gradient Descent
sgd_reg = SGDRegressor(
    max_iter=1000,
    learning_rate='adaptive',  # Adapte le learning rate
    eta0=0.01,                 # Learning rate initial
    random_state=42
)
sgd_reg.fit(X_train_scaled, y_train)
y_pred_sgd = sgd_reg.predict(X_test_scaled)

evaluer_regression(y_test, y_pred_sgd, "SGD Regressor")
```

---

## 5. 🔄 Régression polynomiale

### 5.1 Quand la relation n'est pas linéaire

Si la relation entre X et y n'est pas une droite, on peut utiliser des **features polynomiales** :

```
Linéaire      : y = b₀ + b₁*x
Polynomiale 2 : y = b₀ + b₁*x + b₂*x²
Polynomiale 3 : y = b₀ + b₁*x + b₂*x² + b₃*x³
```

### 5.2 Implémentation

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# Générer des données non-linéaires
np.random.seed(42)
X = np.sort(np.random.uniform(0, 10, 100)).reshape(-1, 1)
y = 2 * X.ravel()**2 - 5 * X.ravel() + 10 + np.random.normal(0, 10, 100)

# Comparer différents degrés
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
degres = [1, 2, 5]

for ax, degree in zip(axes, degres):
    # Pipeline : features polynomiales + régression linéaire
    pipeline = Pipeline([
        ('poly', PolynomialFeatures(degree=degree)),
        ('regression', LinearRegression())
    ])
    pipeline.fit(X, y)

    # Prédictions
    X_plot = np.linspace(0, 10, 300).reshape(-1, 1)
    y_plot = pipeline.predict(X_plot)

    # Visualiser
    ax.scatter(X, y, alpha=0.5, label='Données')
    ax.plot(X_plot, y_plot, color='red', linewidth=2, label=f'Degré {degree}')
    ax.set_title(f'Polynôme de degré {degree}\nR² = {pipeline.score(X, y):.4f}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

> ⚠️ **Attention** : "Un degré polynomial trop élevé = **overfitting garanti**. Le modèle colle parfaitement aux données d'entraînement mais généralise très mal. Un degré 2 ou 3 est souvent suffisant."

> 💡 **Conseil de pro** : "Si vous avez besoin d'un degré supérieur à 3, c'est probablement un signe qu'il faut utiliser un modèle non-linéaire (Random Forest, XGBoost) plutôt que de la régression polynomiale."

---

## 6. 🛡️ Régularisation

La régularisation ajoute une **pénalité** aux coefficients pour empêcher l'overfitting. Elle force le modèle à rester simple.

### 6.1 Ridge (Régularisation L2)

**Principe** : pénalise la **somme des carrés** des coefficients.

**Fonction de coût** : `MSE + α * Σ(bᵢ²)`

```python
from sklearn.linear_model import Ridge

# Le paramètre alpha contrôle la force de la régularisation
# alpha = 0 → régression linéaire classique
# alpha ↑  → coefficients plus petits (plus de régularisation)

ridge = Ridge(alpha=1.0)
ridge.fit(X_train_scaled, y_train)
y_pred_ridge = ridge.predict(X_test_scaled)

evaluer_regression(y_test, y_pred_ridge, "Ridge (alpha=1.0)")

# --- Comparer différentes valeurs d'alpha ---
alphas = [0.01, 0.1, 1, 10, 100]
for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_scaled, y_train)
    y_pred = ridge.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    print(f"Alpha = {alpha:>6} → R² = {r2:.4f}")
```

| Propriété | Détail |
|-----------|--------|
| **Effet** | Réduit les coefficients (les pousse vers 0) mais ne les met jamais exactement à 0 |
| **Quand l'utiliser** | Quand toutes les features sont potentiellement utiles |
| **Hyperparamètre** | `alpha` : plus il est grand, plus la régularisation est forte |

### 6.2 Lasso (Régularisation L1)

**Principe** : pénalise la **somme des valeurs absolues** des coefficients.

**Fonction de coût** : `MSE + α * Σ|bᵢ|`

```python
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train_scaled, y_train)
y_pred_lasso = lasso.predict(X_test_scaled)

evaluer_regression(y_test, y_pred_lasso, "Lasso (alpha=0.1)")

# Lasso peut mettre des coefficients à ZÉRO → sélection de features
print("\n=== Coefficients Lasso ===")
for name, coef in zip(housing.feature_names, lasso.coef_):
    marqueur = " ← ÉLIMINÉ" if coef == 0 else ""
    print(f"  {name:>15} : {coef:>10.4f}{marqueur}")

n_zero = sum(lasso.coef_ == 0)
print(f"\nFeatures éliminées : {n_zero}/{len(lasso.coef_)}")
```

| Propriété | Détail |
|-----------|--------|
| **Effet** | Peut mettre des coefficients **exactement à 0** → sélection automatique de features |
| **Quand l'utiliser** | Quand on suspecte que certaines features sont inutiles |
| **Hyperparamètre** | `alpha` : plus il est grand, plus de features sont éliminées |

### 6.3 ElasticNet (L1 + L2)

**Principe** : combine Ridge et Lasso.

**Fonction de coût** : `MSE + α * (l1_ratio * Σ|bᵢ| + (1-l1_ratio) * Σbᵢ²)`

```python
from sklearn.linear_model import ElasticNet

elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)  # 50% L1 + 50% L2
elastic.fit(X_train_scaled, y_train)
y_pred_elastic = elastic.predict(X_test_scaled)

evaluer_regression(y_test, y_pred_elastic, "ElasticNet")
```

### 6.4 Tableau comparatif de la régularisation

| Modèle | Pénalité | Sélection de features | Quand l'utiliser |
|--------|---------|----------------------|-----------------|
| **Linéaire** | Aucune | Non | Baseline, peu de features |
| **Ridge (L2)** | Σ(bᵢ²) | Non (réduit, ne supprime pas) | Cas général, toutes features utiles |
| **Lasso (L1)** | Σ\|bᵢ\| | Oui (met des coefs à 0) | Features inutiles suspectées |
| **ElasticNet** | L1 + L2 | Partiellement | Beaucoup de features corrélées |

> 💡 **Conseil de pro** : "Commencez **toujours** par Ridge. Si vous suspectez que certaines features sont inutiles, passez à Lasso. Si vos features sont très corrélées entre elles, ElasticNet est un bon compromis."

### 6.5 Trouver le meilleur alpha avec Cross-Validation

```python
from sklearn.linear_model import RidgeCV, LassoCV

# Ridge avec cross-validation automatique
ridge_cv = RidgeCV(alphas=[0.01, 0.1, 1, 10, 100], cv=5)
ridge_cv.fit(X_train_scaled, y_train)
print(f"Meilleur alpha (Ridge) : {ridge_cv.alpha_}")
print(f"R² test : {ridge_cv.score(X_test_scaled, y_test):.4f}")

# Lasso avec cross-validation automatique
lasso_cv = LassoCV(alphas=[0.001, 0.01, 0.1, 1], cv=5)
lasso_cv.fit(X_train_scaled, y_train)
print(f"Meilleur alpha (Lasso) : {lasso_cv.alpha_}")
print(f"R² test : {lasso_cv.score(X_test_scaled, y_test):.4f}")
```

---

## 7. 📈 Comment améliorer son modèle de régression

### 7.1 Checklist d'amélioration

| Étape | Action | Comment |
|-------|--------|---------|
| 1️⃣ | **Plus de données ?** | Courbes d'apprentissage |
| 2️⃣ | **Meilleures features ?** | Feature engineering, interactions |
| 3️⃣ | **Outliers ?** | Vérifier et traiter les valeurs aberrantes |
| 4️⃣ | **Régularisation ?** | Ridge, Lasso, ElasticNet |
| 5️⃣ | **Non-linéarité ?** | Polynomiale, ou modèle non-linéaire |
| 6️⃣ | **Modèle plus complexe ?** | Random Forest, XGBoost |

### 7.2 Courbes d'apprentissage (Learning Curves)

Les courbes d'apprentissage permettent de diagnostiquer l'**overfitting** et l'**underfitting** :

```python
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

def tracer_courbes_apprentissage(modele, X, y, titre="Courbes d'apprentissage"):
    """Trace les courbes d'apprentissage pour diagnostiquer over/underfitting"""
    train_sizes, train_scores, val_scores = learning_curve(
        modele, X, y,
        train_sizes=np.linspace(0.1, 1.0, 10),
        cv=5,
        scoring='r2',
        n_jobs=-1
    )

    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)

    plt.figure(figsize=(10, 6))
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='orange')
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Score entraînement')
    plt.plot(train_sizes, val_mean, 'o-', color='orange', label='Score validation')
    plt.xlabel("Nombre d'échantillons d'entraînement")
    plt.ylabel('R² Score')
    plt.title(titre)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.show()

# Utilisation
tracer_courbes_apprentissage(LinearRegression(), X_train_scaled, y_train)
```

**Interprétation** :

| Diagnostic | Train score | Val score | Écart | Action |
|-----------|------------|----------|-------|--------|
| **Underfitting** | Bas | Bas | Faible | Modèle plus complexe, plus de features |
| **Overfitting** | Haut | Bas | **Grand** | Régularisation, plus de données, simplifier |
| **Bon modèle** | Haut | Haut | Faible | Continuer ! |

### 7.3 Analyse des résidus

Les **résidus** (erreurs) = y_vrai - y_prédit. Analyser les résidus permet de vérifier que le modèle a bien capturé tous les patterns.

```python
def analyser_residus(y_true, y_pred, titre="Analyse des résidus"):
    """Analyse complète des résidus d'un modèle de régression"""
    residus = y_true - y_pred

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Résidus vs Prédictions
    axes[0].scatter(y_pred, residus, alpha=0.3)
    axes[0].axhline(y=0, color='red', linestyle='--')
    axes[0].set_xlabel('Prédictions')
    axes[0].set_ylabel('Résidus')
    axes[0].set_title('Résidus vs Prédictions')

    # 2. Distribution des résidus
    axes[1].hist(residus, bins=30, edgecolor='black')
    axes[1].axvline(x=0, color='red', linestyle='--')
    axes[1].set_xlabel('Résidus')
    axes[1].set_ylabel('Fréquence')
    axes[1].set_title('Distribution des résidus')

    # 3. QQ-Plot (normalité des résidus)
    from scipy import stats
    stats.probplot(residus, dist="norm", plot=axes[2])
    axes[2].set_title('QQ-Plot des résidus')

    plt.suptitle(titre)
    plt.tight_layout()
    plt.show()

    # Statistiques des résidus
    print(f"Résidus - Moyenne : {residus.mean():.4f} (devrait être ≈ 0)")
    print(f"Résidus - Écart-type : {residus.std():.4f}")
    print(f"Résidus - Médiane : {np.median(residus):.4f}")

# Utilisation
analyser_residus(y_test, y_pred)
```

> 💡 **Conseil** : "Tracez **TOUJOURS** les résidus. Des patterns dans les résidus (courbe, cône, clusters) indiquent que le modèle n'a pas capturé toute l'information. Un bon modèle a des résidus **aléatoires et centrés sur 0**."

### 7.4 Comparaison de plusieurs modèles

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import pandas as pd

# Définir les modèles à comparer
modeles = {
    'Linéaire': LinearRegression(),
    'Ridge (α=1)': Ridge(alpha=1.0),
    'Ridge (α=10)': Ridge(alpha=10.0),
    'Lasso (α=0.1)': Lasso(alpha=0.1),
    'Polynomiale (deg=2)': Pipeline([
        ('poly', PolynomialFeatures(degree=2)),
        ('reg', LinearRegression())
    ])
}

# Entraîner et évaluer chaque modèle
resultats = []
for nom, modele in modeles.items():
    modele.fit(X_train_scaled, y_train)
    y_pred = modele.predict(X_test_scaled)

    resultats.append({
        'Modèle': nom,
        'R²': r2_score(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'MAE': mean_absolute_error(y_test, y_pred)
    })

# Afficher le tableau comparatif
df_resultats = pd.DataFrame(resultats).sort_values('R²', ascending=False)
print("=== Comparaison des modèles de régression ===")
print(df_resultats.to_string(index=False))
```

> 💡 **Conseil de pro** : "Comparez **toujours** plusieurs modèles avec les **mêmes métriques** et le **même split** de données. C'est la seule façon de faire une comparaison juste."

---

## 🎯 Points clés à retenir

1. **Commencez simple** : régression linéaire comme baseline
2. **Métriques multiples** : toujours reporter R², RMSE, MAE (au minimum)
3. **RMSE** est souvent la métrique par défaut — même unité que la cible
4. **MAPE** est idéale pour communiquer avec les métiers (erreur en %)
5. **R² seul peut être trompeur** — toujours vérifier avec d'autres métriques
6. **Régularisation** : Ridge par défaut, Lasso pour la sélection de features
7. **Learning curves** : diagnostic overfitting/underfitting
8. **Résidus** : toujours les analyser — des patterns = modèle incomplet
9. **Standardiser** les features pour comparer les coefficients
10. **Ne pas oublier** : le preprocessing (chapitre 3) est souvent plus impactant que le choix du modèle

---

## ✅ Checklist de validation

- [ ] Je sais implémenter une régression linéaire simple et multiple avec sklearn
- [ ] Je sais interpréter les coefficients d'une régression
- [ ] Je connais et sais calculer MSE, RMSE, MAE, R² et MAPE
- [ ] Je sais quand utiliser chaque métrique selon le contexte
- [ ] Je comprends le Gradient Descent et le rôle du learning rate
- [ ] Je sais implémenter une régression polynomiale avec PolynomialFeatures
- [ ] Je comprends la régularisation et sais choisir entre Ridge, Lasso et ElasticNet
- [ ] Je sais tracer et interpréter les courbes d'apprentissage
- [ ] Je sais analyser les résidus d'un modèle de régression
- [ ] Je sais comparer plusieurs modèles avec les mêmes métriques

---

**Précédent** : [Chapitre 3 : Preprocessing – Préparer ses Données](03-preprocessing.md)

**Suivant** : [Chapitre 5 : Classification – Prédire des Catégories](05-classification.md)
