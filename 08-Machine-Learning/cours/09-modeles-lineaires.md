# Chapitre 9 : Modèles Linéaires et Logiques — Les Fondamentaux

## 🎯 Objectifs

- Maîtriser en profondeur la régression linéaire (simple et multiple)
- Comprendre la régression logistique et ses différences avec la régression linéaire
- Revisiter KNN avec un regard critique (avantages, limites, curse of dimensionality)
- Comprendre ce que font `.fit()` et `.predict()` en interne pour chaque modèle
- Savoir comparer et choisir entre ces trois algorithmes fondamentaux

**Phase 3 — Semaine 9 — Les Algorithmes, enfin !**

---

## 1. 🧠 Régression linéaire (approfondissement)

### 1.1 Rappel de la formule

La régression linéaire modélise la relation entre des features (X) et une target (y) sous la forme :

```
y = b0 + b1*x1 + b2*x2 + ... + bn*xn

Où :
- b0 = intercept (ordonnée à l'origine)
- b1, b2, ..., bn = coefficients (un par feature)
- x1, x2, ..., xn = features (variables explicatives)
```

L'algorithme cherche les valeurs de `b0, b1, ..., bn` qui **minimisent** la somme des erreurs au carré (méthode des moindres carrés ordinaires — OLS).

```
Objectif : minimiser Σ(yi - ŷi)²
                     i=1..n

Où ŷi = b0 + b1*x1i + b2*x2i + ... + bn*xni
```

### 1.2 Interprétation des coefficients

Chaque coefficient représente l'**impact marginal** de la feature correspondante sur la target, **toutes les autres features étant constantes**.

```
Exemple : prédiction du prix d'un appartement

prix = 50000 + 3200 * surface + 15000 * nb_pieces - 800 * distance_metro

Interprétation :
- b0 = 50 000 € → prix de base (intercept)
- b1 = 3 200    → chaque m² supplémentaire ajoute 3 200 € au prix
- b2 = 15 000   → chaque pièce supplémentaire ajoute 15 000 €
- b3 = -800     → chaque km d'éloignement du métro retire 800 €
```

> 💡 **Conseil** : "Pour comparer l'importance relative des coefficients, il faut d'abord **standardiser** les features. Sans standardisation, un coefficient de 3200 (en m²) n'est pas comparable à un coefficient de -800 (en km)."

### 1.3 Régression linéaire simple vs multiple

| Aspect | Régression simple | Régression multiple |
|--------|-------------------|---------------------|
| **Nombre de features** | 1 seule (y = b0 + b1*x) | Plusieurs (y = b0 + b1*x1 + ... + bn*xn) |
| **Visualisation** | Droite dans un plan 2D | Hyperplan dans un espace nD |
| **Risque de multicolinéarité** | Aucun | Oui, si features corrélées |
| **Interprétation** | Très intuitive | Plus nuancée (effet marginal) |
| **Performance typique** | Limitée | Meilleure (plus d'information) |

### 1.4 Hypothèses du modèle

La régression linéaire repose sur **5 hypothèses fondamentales**. Les connaître permet de comprendre quand le modèle est fiable et quand il ne l'est pas.

| Hypothèse | Description | Vérification | Conséquence si violée |
|-----------|-------------|-------------|----------------------|
| **Linéarité** | Relation linéaire entre X et y | Scatter plots, résidus vs prédictions | Modèle biaisé, sous-performance |
| **Homoscédasticité** | Variance constante des résidus | Résidus vs prédictions (pas de cône) | Intervalles de confiance faux |
| **Normalité des résidus** | Résidus ≈ distribution normale | QQ-Plot, test de Shapiro-Wilk | Tests statistiques non fiables |
| **Indépendance des résidus** | Pas de corrélation entre résidus | Durbin-Watson test | Sous-estimation de l'incertitude |
| **Pas de multicolinéarité** | Features non fortement corrélées | VIF > 5 = problème | Coefficients instables, ininterprétables |

```
Vérification visuelle des hypothèses :

  Résidus vs Prédictions         Résidus vs Prédictions
  (Bon modèle)                   (Problème : hétéroscédasticité)

  residus                        residus
    |  .  . .  .  .                |           . .  .
    |. .  . .  . .                 |        . .  .
    |-----.----.----→ ŷ            |    . .  .
    |.  .  .  . .                  |  . .
    | .  .  . .                    | . .
                                   |.
    → aléatoire, centré sur 0      → forme de cône = problème !
```

### 1.5 Limites de la régression linéaire

| Limite | Description | Solution |
|--------|-------------|----------|
| **Non-linéarité** | Relations courbes non captées | Régression polynomiale, arbres, XGBoost |
| **Outliers** | Très sensible aux valeurs extrêmes | Nettoyage des données, régularisation |
| **Multicolinéarité** | Features corrélées → coefficients instables | Lasso (sélection), PCA, suppression manuelle |
| **Features catégorielles** | Ne gère que le numérique | One-Hot Encoding, Target Encoding |
| **Interactions** | Ne capture pas les interactions entre features | Ajouter manuellement x1*x2, ou modèle non-linéaire |

### 1.6 Code complet : régression linéaire sur house_prices

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# --- Générer un dataset house_prices réaliste ---
np.random.seed(42)
n = 500

surface = np.random.uniform(20, 200, n)
nb_pieces = np.random.randint(1, 7, n)
distance_metro = np.random.uniform(0.1, 10, n)
etage = np.random.randint(0, 15, n)
annee_construction = np.random.randint(1960, 2024, n)

# Prix avec relation réaliste + bruit
prix = (
    50000
    + 3200 * surface
    + 15000 * nb_pieces
    - 800 * distance_metro
    + 500 * etage
    + 200 * (annee_construction - 1960)
    + np.random.normal(0, 25000, n)
)

df = pd.DataFrame({
    'surface': surface,
    'nb_pieces': nb_pieces,
    'distance_metro': distance_metro,
    'etage': etage,
    'annee_construction': annee_construction,
    'prix': prix
})

print("=== Aperçu du dataset ===")
print(df.head())
print(f"\nShape : {df.shape}")
print(f"\nStatistiques :\n{df.describe().round(2)}")

# --- Préparation ---
X = df.drop('prix', axis=1)
y = df['prix']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Entraînement ---
modele = LinearRegression()
modele.fit(X_train_scaled, y_train)

# --- Coefficients ---
print("\n=== Coefficients du modèle ===")
coefs = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': modele.coef_
}).sort_values('Coefficient', key=abs, ascending=False)
print(coefs)
print(f"\nIntercept : {modele.intercept_:.2f} €")

# --- Prédictions et évaluation ---
y_pred = modele.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n=== Évaluation ===")
print(f"RMSE : {rmse:,.0f} €")
print(f"MAE  : {mae:,.0f} €")
print(f"R²   : {r2:.4f}")
```

### 1.7 Visualisation des résidus

```python
def analyser_residus(y_true, y_pred, titre="Analyse des résidus"):
    """Analyse complète des résidus"""
    residus = y_true - y_pred

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # 1. Résidus vs Prédictions
    axes[0].scatter(y_pred, residus, alpha=0.3, s=20)
    axes[0].axhline(y=0, color='red', linestyle='--', linewidth=2)
    axes[0].set_xlabel('Prédictions (ŷ)')
    axes[0].set_ylabel('Résidus (y - ŷ)')
    axes[0].set_title('Résidus vs Prédictions')
    axes[0].grid(True, alpha=0.3)

    # 2. Distribution des résidus
    axes[1].hist(residus, bins=30, edgecolor='black', alpha=0.7)
    axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Résidus')
    axes[1].set_ylabel('Fréquence')
    axes[1].set_title('Distribution des résidus')

    # 3. QQ-Plot
    from scipy import stats
    stats.probplot(residus, dist="norm", plot=axes[2])
    axes[2].set_title('QQ-Plot (normalité)')

    plt.suptitle(titre, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Statistiques
    print(f"Résidus - Moyenne : {residus.mean():.2f} (devrait être ≈ 0)")
    print(f"Résidus - Écart-type : {residus.std():.2f}")

analyser_residus(y_test, y_pred)
```

> 💡 **Conseil** : "Tracez **toujours** les résidus après une régression linéaire. Si vous voyez une forme de courbe → la relation n'est pas linéaire. Si vous voyez un cône → hétéroscédasticité. Des résidus aléatoires centrés sur 0 = bon modèle."

### 1.8 R² et R² ajusté

Le **R²** (coefficient de détermination) mesure la proportion de variance expliquée par le modèle :

| Métrique | Formule | Interprétation |
|----------|---------|----------------|
| **R²** | 1 - SS_res / SS_tot | % de variance expliqué (0 à 1) |
| **R² ajusté** | 1 - (1-R²)(n-1)/(n-p-1) | Pénalise l'ajout de features inutiles |

```python
def r2_ajuste(r2, n, p):
    """
    R² ajusté
    n = nombre d'observations
    p = nombre de features
    """
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)

n = len(y_test)
p = X_test.shape[1]

print(f"R²         : {r2:.4f}")
print(f"R² ajusté  : {r2_ajuste(r2, n, p):.4f}")
```

> ⚠️ **Attention** : "Le R² augmente **toujours** quand on ajoute une nouvelle feature, même si elle est inutile. C'est pourquoi il faut utiliser le R² ajusté qui pénalise la complexité. Si R² ajusté << R², vous avez trop de features."

---

## 2. 📊 Régression logistique

### 2.1 Ce n'est PAS une régression !

Malgré son nom trompeur, la régression logistique est un algorithme de **classification**. Le nom vient du fait qu'elle utilise une **fonction logistique** (sigmoïde) pour transformer une régression linéaire en probabilité.

```
Pourquoi ce nom trompeur ?

1. On calcule d'abord une valeur linéaire :   z = b0 + b1*x1 + b2*x2 + ...
2. Puis on la transforme en probabilité :       P(y=1) = σ(z) = 1 / (1 + e^(-z))

La partie "régression" fait référence à l'étape 1 (linéaire).
La partie "logistique" fait référence à l'étape 2 (sigmoïde).
Le résultat final est une CLASSIFICATION (classe 0 ou 1).
```

### 2.2 La fonction sigmoïde

La fonction sigmoïde transforme n'importe quel nombre réel en une valeur entre 0 et 1, ce qui en fait une probabilité :

```
           σ(z) = 1 / (1 + e^(-z))

  Probabilité
  P(y=1)
    1.0 |                          ___________
        |                       __/
    0.8 |                     _/
        |                   _/
    0.6 |                  /
        |                 /
    0.5 |- - - - - - - -/- - - - - - - seuil par défaut
        |              /
    0.4 |             /
        |           _/
    0.2 |         _/
        |      __/
    0.0 |_____/
        +-------+-------+-------+-------→  z
       -6      -3       0       3       6

  Si z >> 0 → σ(z) ≈ 1 → classe 1
  Si z << 0 → σ(z) ≈ 0 → classe 0
  Si z = 0  → σ(z) = 0.5 → frontière de décision
```

```python
import numpy as np
import matplotlib.pyplot as plt

# Visualiser la sigmoïde
z = np.linspace(-8, 8, 200)
sigmoid = 1 / (1 + np.exp(-z))

plt.figure(figsize=(10, 6))
plt.plot(z, sigmoid, 'b-', linewidth=2, label='σ(z) = 1/(1+e^(-z))')
plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Seuil = 0.5')
plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
plt.fill_between(z, sigmoid, 0.5, where=(sigmoid >= 0.5),
                 alpha=0.1, color='green', label='Classe 1')
plt.fill_between(z, sigmoid, 0.5, where=(sigmoid < 0.5),
                 alpha=0.1, color='red', label='Classe 0')
plt.xlabel('z = b0 + b1*x1 + b2*x2 + ...', fontsize=12)
plt.ylabel('P(y = 1)', fontsize=12)
plt.title('La fonction sigmoïde', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.ylim(-0.05, 1.05)
plt.show()
```

### 2.3 De la régression linéaire à la logistique

Le lien mathématique entre les deux est clair :

```
Régression linéaire :
    y = b0 + b1*x1 + b2*x2 + ...    → valeur continue (prix, température...)

Régression logistique :
    z = b0 + b1*x1 + b2*x2 + ...    → valeur linéaire (identique !)
    P(y=1) = σ(z) = 1 / (1 + e^(-z)) → probabilité [0, 1]
    classe = 1 si P(y=1) ≥ 0.5, sinon 0 → classification binaire

La seule différence : on applique la sigmoïde à la sortie linéaire.
```

### 2.4 Probabilités vs classes

| Concept | Description | Exemple |
|---------|-------------|---------|
| **Probabilité** | P(y=1) entre 0 et 1 | P(churn) = 0.78 |
| **Classe prédite** | 0 ou 1 (selon le seuil) | churn = 1 (car 0.78 > 0.5) |
| **Seuil (threshold)** | Frontière de décision | Par défaut 0.5, ajustable |

> 💡 **Conseil** : "Utiliser les probabilités (`.predict_proba()`) est souvent plus utile que les classes brutes (`.predict()`). Cela permet d'ajuster le seuil selon le contexte métier, de prioriser les cas les plus confiants, et de calculer l'AUC-ROC."

### 2.5 Interprétation des coefficients : Odds Ratio

En régression logistique, les coefficients s'interprètent via l'**odds ratio** :

```
Odds(y=1) = P(y=1) / P(y=0) = P(y=1) / (1 - P(y=1))

log(Odds) = b0 + b1*x1 + b2*x2 + ...    (log-odds = valeur linéaire)

Odds Ratio pour la feature xi = e^(bi)

Interprétation :
- OR = 1   → pas d'effet
- OR > 1   → augmente la probabilité de la classe 1
- OR < 1   → diminue la probabilité de la classe 1
- OR = 2.5 → chaque unité de xi multiplie les odds par 2.5
```

```python
import numpy as np

# Exemple d'interprétation
coefficients = {
    'nb_appels_support': 0.35,
    'anciennete_mois': -0.08,
    'montant_mensuel': 0.02,
    'contrat_mensuel': 1.20,
}

print("=== Odds Ratios (Régression Logistique - Churn) ===\n")
for feature, coef in coefficients.items():
    odds_ratio = np.exp(coef)
    if odds_ratio > 1:
        effet = f"multiplie les odds de churn par {odds_ratio:.2f}"
    else:
        effet = f"divise les odds de churn par {1/odds_ratio:.2f}"
    print(f"{feature:>25} : coef={coef:>6.2f} → OR={odds_ratio:.2f} → {effet}")
```

### 2.6 Code complet : classification binaire sur churn

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt

# --- Générer un dataset churn réaliste ---
np.random.seed(42)
n = 1000

anciennete = np.random.exponential(24, n)  # mois
montant_mensuel = np.random.uniform(20, 120, n)
nb_appels_support = np.random.poisson(2, n)
contrat_mensuel = np.random.binomial(1, 0.4, n)
satisfaction = np.random.uniform(1, 10, n)

# Probabilité de churn basée sur les features
z = (
    -2.0
    + 0.35 * nb_appels_support
    - 0.04 * anciennete
    + 0.02 * montant_mensuel
    + 1.2 * contrat_mensuel
    - 0.3 * satisfaction
)
prob_churn = 1 / (1 + np.exp(-z))
churn = (np.random.random(n) < prob_churn).astype(int)

df = pd.DataFrame({
    'anciennete': anciennete,
    'montant_mensuel': montant_mensuel,
    'nb_appels_support': nb_appels_support,
    'contrat_mensuel': contrat_mensuel,
    'satisfaction': satisfaction,
    'churn': churn
})

print(f"=== Distribution du churn ===")
print(df['churn'].value_counts(normalize=True).round(3))

# --- Préparation ---
X = df.drop('churn', axis=1)
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Entraînement ---
log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train_scaled, y_train)

# --- Coefficients et Odds Ratios ---
print("\n=== Coefficients et Odds Ratios ===")
coefs_df = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': log_reg.coef_[0],
    'Odds_Ratio': np.exp(log_reg.coef_[0])
}).sort_values('Coefficient', key=abs, ascending=False)
print(coefs_df.round(4))

# --- Prédictions ---
y_pred = log_reg.predict(X_test_scaled)
y_proba = log_reg.predict_proba(X_test_scaled)[:, 1]

# --- Évaluation ---
print("\n=== Rapport de classification ===")
print(classification_report(y_test, y_pred))
print(f"AUC-ROC : {roc_auc_score(y_test, y_proba):.4f}")

# --- Courbe ROC ---
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, 'b-', linewidth=2,
         label=f'ROC (AUC = {roc_auc_score(y_test, y_proba):.3f})')
plt.plot([0, 1], [0, 1], 'r--', label='Aléatoire')
plt.xlabel('Taux de faux positifs (FPR)')
plt.ylabel('Taux de vrais positifs (TPR)')
plt.title('Courbe ROC — Régression Logistique (Churn)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 2.7 predict vs predict_proba

```python
# predict() → classe prédite (0 ou 1)
y_pred = log_reg.predict(X_test_scaled)
print("predict() :", y_pred[:10])
# → [0, 1, 0, 0, 1, 1, 0, 0, 1, 0]

# predict_proba() → probabilités pour chaque classe
y_proba = log_reg.predict_proba(X_test_scaled)
print("predict_proba() :")
print(y_proba[:5])
# → [[0.82, 0.18],   ← 82% classe 0, 18% classe 1
#     [0.23, 0.77],   ← 23% classe 0, 77% classe 1
#     [0.91, 0.09],
#     [0.65, 0.35],
#     [0.12, 0.88]]

# Récupérer uniquement la probabilité de la classe positive
y_proba_positive = log_reg.predict_proba(X_test_scaled)[:, 1]
print("P(churn=1) :", y_proba_positive[:5].round(3))

# Ajuster le seuil de décision
seuil = 0.3  # plus agressif pour détecter le churn
y_pred_custom = (y_proba_positive >= seuil).astype(int)
print(f"\nSeuil 0.5 → {y_pred.sum()} churns détectés")
print(f"Seuil 0.3 → {y_pred_custom.sum()} churns détectés")
```

> ⚠️ **Attention** : "Le seuil par défaut de 0.5 n'est pas toujours optimal. En détection de churn, on préfère souvent un seuil plus bas (0.3-0.4) pour détecter plus de churners, quitte à avoir plus de faux positifs. Le bon seuil dépend du **coût métier** des erreurs."

---

## 3. 🔍 KNN revisité

### 3.1 Rappel du principe

K-Nearest Neighbors (KNN) est un algorithme **non paramétrique** : il ne fait aucune hypothèse sur la distribution des données. Pour prédire, il cherche les K voisins les plus proches et fait un vote (classification) ou une moyenne (régression).

```
Prédiction pour un nouveau point (⭐) avec K=3 :

    Classe A : ●
    Classe B : ▲
    Nouveau  : ⭐

        ●
    ●       ▲
        ⭐          ▲
    ●       ●
        ▲       ▲

    Les 3 plus proches voisins de ⭐ : ● ● ▲
    Vote majoritaire : 2 × ● vs 1 × ▲
    Prédiction : classe ● (A)
```

### 3.2 Avantages et inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| Très simple à comprendre | Lent en prédiction (O(n) par prédiction) |
| Aucune hypothèse sur les données | Très sensible au scaling des features |
| Non paramétrique | Curse of dimensionality (>20 features) |
| Pas de phase d'entraînement | Pas de modèle interprétable |
| Fonctionne en classification ET régression | Sensible au bruit et aux outliers |
| Capte des frontières non linéaires | Mauvais avec des features catégorielles |

### 3.3 La malédiction de la dimensionnalité (Curse of Dimensionality)

```
En haute dimension, les distances entre points deviennent presque identiques :

  Dimension 1 (1D) :  ●──────●──●──────●     → distances variées, voisins clairs

  Dimension 100 (100D) :
  Toutes les distances convergent vers une même valeur
  → "tous les points sont aussi loin les uns des autres"
  → KNN ne sait plus qui est vraiment "proche"

  Règle empirique :
  - KNN fonctionne bien jusqu'à ~20 features
  - Au-delà, les performances se dégradent
  - Solution : réduction de dimension (PCA) avant KNN
```

> ⚠️ **Attention** : "KNN est l'algorithme le plus affecté par la malédiction de la dimensionnalité. Si vous avez plus de 20-30 features, privilégiez un Random Forest ou une régression logistique."

### 3.4 KNN pour la régression

KNN n'est pas limité à la classification — il peut aussi faire de la régression en calculant la **moyenne** (ou la moyenne pondérée) des valeurs des K voisins :

```python
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# KNN en régression
knn_reg = KNeighborsRegressor(n_neighbors=5, weights='distance')
knn_reg.fit(X_train_scaled, y_train)
y_pred_knn = knn_reg.predict(X_test_scaled)

rmse = np.sqrt(mean_squared_error(y_test, y_pred_knn))
r2 = r2_score(y_test, y_pred_knn)
print(f"KNN Régression (K=5) : RMSE={rmse:.2f}, R²={r2:.4f}")

# KNN en classification
knn_clf = KNeighborsClassifier(n_neighbors=5, weights='distance')
knn_clf.fit(X_train_scaled, y_train)
y_pred_knn_clf = knn_clf.predict(X_test_scaled)
```

### 3.5 Choisir K optimal : la méthode du coude (Elbow Method)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import numpy as np

# Tester différentes valeurs de K
k_values = range(1, 31)
scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k, weights='distance')
    score = cross_val_score(knn, X_train_scaled, y_train, cv=5,
                            scoring='accuracy').mean()
    scores.append(score)

# Trouver le K optimal
best_k = k_values[np.argmax(scores)]
best_score = max(scores)
print(f"Meilleur K : {best_k} (accuracy = {best_score:.4f})")

# Visualiser
plt.figure(figsize=(10, 6))
plt.plot(k_values, scores, 'bo-', linewidth=2)
plt.axvline(x=best_k, color='red', linestyle='--',
            label=f'K optimal = {best_k}')
plt.xlabel('K (nombre de voisins)', fontsize=12)
plt.ylabel('Accuracy (cross-validation)', fontsize=12)
plt.title('Choix de K — Méthode du coude', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(k_values)
plt.show()
```

> 💡 **Conseil** : "Commencez avec K=5 ou K=√n (racine carrée du nombre d'échantillons). Utilisez toujours un nombre impair pour K en classification binaire afin d'éviter les égalités."

### 3.6 L'importance cruciale du scaling pour KNN

```python
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Sans scaling
knn_no_scale = KNeighborsClassifier(n_neighbors=5)
knn_no_scale.fit(X_train, y_train)
score_no_scale = accuracy_score(y_test, knn_no_scale.predict(X_test))

# Avec scaling
knn_scaled = KNeighborsClassifier(n_neighbors=5)
knn_scaled.fit(X_train_scaled, y_train)
score_scaled = accuracy_score(y_test, knn_scaled.predict(X_test_scaled))

print(f"KNN sans scaling : {score_no_scale:.4f}")
print(f"KNN avec scaling : {score_scaled:.4f}")
print(f"Différence       : +{score_scaled - score_no_scale:.4f}")
```

> ⚠️ **Attention** : "Le scaling est **obligatoire** pour KNN. Sans scaling, une feature en mètres (0-200) dominera une feature en km (0-10), faussant complètement le calcul des distances."

---

## 4. ⚙️ Comprendre .fit() et .predict()

### 4.1 Que se passe-t-il en interne ?

Chaque algorithme a un comportement différent lors de l'entraînement (`.fit()`) et de la prédiction (`.predict()`) :

```
┌─────────────────────────────────────────────────────────────────┐
│                    RÉGRESSION LINÉAIRE                          │
├─────────────────────────────────────────────────────────────────┤
│ .fit(X, y)                                                      │
│   → Calcule les coefficients b0, b1, ..., bn                   │
│   → Méthode : moindres carrés (OLS) ou gradient descent        │
│   → Stocke : coef_, intercept_                                  │
│   → Temps : rapide (O(np²) avec n samples, p features)         │
│                                                                  │
│ .predict(X)                                                      │
│   → Calcule y = b0 + b1*x1 + ... + bn*xn                      │
│   → Simple multiplication matrice-vecteur                        │
│   → Temps : très rapide (O(np))                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    RÉGRESSION LOGISTIQUE                        │
├─────────────────────────────────────────────────────────────────┤
│ .fit(X, y)                                                      │
│   → Optimise les coefficients par gradient descent              │
│   → Minimise la log-loss (cross-entropy)                        │
│   → Stocke : coef_, intercept_                                  │
│   → Temps : modéré (itératif, dépend de max_iter)              │
│                                                                  │
│ .predict(X)                                                      │
│   → Calcule z = b0 + b1*x1 + ... + bn*xn                      │
│   → Applique σ(z) pour obtenir les probabilités                 │
│   → Applique le seuil (0.5) pour obtenir les classes            │
│   → Temps : très rapide                                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                           KNN                                    │
├─────────────────────────────────────────────────────────────────┤
│ .fit(X, y)                                                      │
│   → Stocke simplement les données en mémoire                    │
│   → Aucun calcul !                                              │
│   → Temps : quasi-instantané                                    │
│                                                                  │
│ .predict(X)                                                      │
│   → Pour CHAQUE nouveau point :                                  │
│       1. Calcule la distance avec TOUS les points d'entraînement│
│       2. Trie pour trouver les K plus proches                    │
│       3. Vote majoritaire (classif) ou moyenne (régression)      │
│   → Temps : LENT (O(n*d) par prédiction, n=training size)      │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Lazy Learner vs Eager Learner

| Caractéristique | Lazy Learner (KNN) | Eager Learner (Régression) |
|-----------------|-------------------|---------------------------|
| **Entraînement (.fit)** | Instantané (juste stocker) | Calcul des paramètres |
| **Prédiction (.predict)** | Lent (calcul à chaque fois) | Rapide (appliquer la formule) |
| **Mémoire** | Stocke tout le dataset | Stocke seulement les paramètres |
| **Adaptabilité** | S'adapte à de nouvelles données | Doit réentraîner |
| **Interprétabilité** | Aucun modèle explicite | Coefficients interprétables |

```python
import time

# --- Comparer les temps de fit et predict ---
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

modeles = {
    'Régression Linéaire': LinearRegression(),
    'Régression Logistique': LogisticRegression(max_iter=1000),
    'KNN (K=5)': KNeighborsClassifier(n_neighbors=5),
}

print("=== Comparaison des temps (fit vs predict) ===\n")
for nom, modele in modeles.items():
    # Temps de fit
    start = time.time()
    modele.fit(X_train_scaled, y_train)
    temps_fit = time.time() - start

    # Temps de predict
    start = time.time()
    for _ in range(100):  # Répéter 100 fois pour mieux mesurer
        modele.predict(X_test_scaled)
    temps_predict = (time.time() - start) / 100

    print(f"{nom:>25} : fit={temps_fit*1000:.1f}ms, predict={temps_predict*1000:.2f}ms")
```

> 💡 **Conseil** : "En production, le temps de prédiction est souvent plus important que le temps d'entraînement. Un modèle linéaire qui prédit en 0.01ms est préférable à un KNN qui met 50ms, surtout si vous traitez des millions de requêtes par jour."

### 4.3 Que stocke chaque modèle après .fit() ?

```python
# Régression linéaire → stocke les coefficients
lin_reg = LinearRegression()
lin_reg.fit(X_train_scaled, y_train)
print("Régression Linéaire stocke :")
print(f"  coef_      : {lin_reg.coef_}")
print(f"  intercept_ : {lin_reg.intercept_}")
print(f"  → Total : {len(lin_reg.coef_) + 1} paramètres\n")

# Régression logistique → stocke les coefficients
log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train_scaled, y_train)
print("Régression Logistique stocke :")
print(f"  coef_      : {log_reg.coef_[0]}")
print(f"  intercept_ : {log_reg.intercept_}")
print(f"  classes_   : {log_reg.classes_}")
print(f"  → Total : {len(log_reg.coef_[0]) + 1} paramètres\n")

# KNN → stocke TOUT le dataset
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
print("KNN stocke :")
print(f"  _fit_X shape : {knn._fit_X.shape}")
print(f"  _y shape     : {knn._y.shape}")
print(f"  → Total : {knn._fit_X.size + knn._y.size} valeurs en mémoire !")
```

---

## 5. 📋 Tableau comparatif des 3 modèles

### 5.1 Comparaison générale

| Critère | Régression Linéaire | Régression Logistique | KNN |
|---------|--------------------|-----------------------|-----|
| **Type de problème** | Régression | Classification | Les deux |
| **Sortie** | Valeur continue | Probabilité / Classe | Valeur / Classe |
| **Hypothèses** | Linéarité, normalité résidus | Linéarité du log-odds | Aucune |
| **Paramétrique** | Oui | Oui | Non |
| **Interprétabilité** | Excellente (coefficients) | Bonne (odds ratios) | Faible |
| **Scaling nécessaire** | Non (sauf comparaison coefs) | Recommandé | Obligatoire |
| **Gère la non-linéarité** | Non | Non | Oui |
| **Vitesse fit** | Rapide | Modérée | Instantanée |
| **Vitesse predict** | Très rapide | Très rapide | Lente |
| **Sensible aux outliers** | Très | Modérément | Oui |
| **Gère les features catégorielles** | Après encoding | Après encoding | Difficilement |
| **Nombre de features élevé** | Correct | Bon | Mauvais (curse of dim.) |

### 5.2 Quand utiliser quoi ?

| Situation | Modèle recommandé | Justification |
|-----------|-------------------|---------------|
| Prédire un prix, une durée | Régression Linéaire | Valeur continue, interprétable |
| Classifier spam/non-spam | Régression Logistique | Classification binaire, probabilités |
| Peu de features, relations complexes | KNN | Non-paramétrique, frontières non-linéaires |
| Besoin d'explicabilité métier | Régression (Lin. ou Log.) | Coefficients interprétables |
| Production à grande échelle | Régression (Lin. ou Log.) | Prédiction ultra-rapide |
| Exploration rapide / baseline | KNN ou Régression | Simple, rapide à implémenter |
| > 50 features | Régression Logistique | KNN souffre de la dimensionnalité |
| Dataset > 100k lignes | Régression (Lin. ou Log.) | KNN trop lent en prédiction |

### 5.3 Code de comparaison complète

```python
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score
import pandas as pd
import time

# Comparaison sur un problème de classification
modeles_clf = {
    'Régression Logistique': LogisticRegression(max_iter=1000, random_state=42),
    'KNN (K=3)': KNeighborsClassifier(n_neighbors=3),
    'KNN (K=5)': KNeighborsClassifier(n_neighbors=5),
    'KNN (K=11)': KNeighborsClassifier(n_neighbors=11),
}

resultats = []
for nom, modele in modeles_clf.items():
    start = time.time()
    scores = cross_val_score(modele, X_train_scaled, y_train,
                             cv=5, scoring='roc_auc')
    duree = time.time() - start

    resultats.append({
        'Modèle': nom,
        'AUC-ROC (CV)': f"{scores.mean():.4f} ± {scores.std():.4f}",
        'Temps (s)': f"{duree:.2f}",
    })

df_resultats = pd.DataFrame(resultats)
print("=== Comparaison des modèles ===")
print(df_resultats.to_string(index=False))
```

---

## 🎯 Points clés à retenir

1. **La régression linéaire** modélise y = b0 + b1*x1 + ... — chaque coefficient est l'impact marginal d'une feature sur la target
2. **Les 5 hypothèses** de la régression linéaire (linéarité, homoscédasticité, normalité des résidus, indépendance, pas de multicolinéarité) doivent être vérifiées
3. **La régression logistique** n'est PAS une régression — c'est une classification qui applique la sigmoïde à une combinaison linéaire
4. **predict_proba** est souvent plus utile que predict — il donne les probabilités et permet d'ajuster le seuil
5. **Les odds ratios** (e^coefficient) permettent d'interpréter l'impact de chaque feature en régression logistique
6. **KNN** est simple et non-paramétrique, mais lent en prédiction et sensible à la dimensionnalité
7. **Le scaling est obligatoire** pour KNN (distances) et recommandé pour la régression logistique
8. **KNN est un lazy learner** : fit est instantané mais predict est lent (calcul des distances à chaque fois)
9. **Les régressions sont des eager learners** : fit calcule les paramètres, predict les applique très rapidement
10. **Commencer simple** : régression linéaire/logistique comme baseline, puis complexifier si nécessaire

---

## ✅ Checklist de validation

- [ ] Je sais implémenter et interpréter une régression linéaire simple et multiple
- [ ] Je connais les 5 hypothèses de la régression linéaire et sais les vérifier
- [ ] Je sais analyser les résidus et en tirer des conclusions
- [ ] Je comprends la différence entre R² et R² ajusté
- [ ] Je sais que la régression logistique est un modèle de classification, pas de régression
- [ ] Je sais dessiner et expliquer la fonction sigmoïde
- [ ] Je sais utiliser predict_proba et ajuster le seuil de décision
- [ ] Je sais interpréter les coefficients via les odds ratios
- [ ] Je connais les avantages et limites de KNN (curse of dimensionality, scaling obligatoire)
- [ ] Je sais choisir K optimal avec la méthode du coude
- [ ] Je comprends la différence entre lazy learner (KNN) et eager learner (régression)
- [ ] Je sais quel modèle choisir selon le contexte (taille des données, interprétabilité, production)

---

**Précédent** : [Chapitre 8 : Évaluation et Métriques](08-evaluation-metriques.md)

**Suivant** : [Chapitre 10 : Arbres de Décision et Forêts Aléatoires](10-arbres-forets.md)
