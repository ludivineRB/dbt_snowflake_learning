# Chapitre 11 : Boosting — Les Champions de Kaggle

## 🎯 Objectifs

- Comprendre l'intuition du boosting : apprendre de ses erreurs
- Maîtriser la différence fondamentale entre Random Forest et Boosting
- Comprendre le Gradient Boosting pas à pas
- Savoir utiliser XGBoost, LightGBM et CatBoost
- Comparer les trois frameworks de boosting
- Découvrir les SVM (Support Vector Machines) en aperçu
- Savoir choisir le bon algorithme selon le problème

**Phase 3 — Semaine 11**

---

## 1. 🧠 Intuition : Apprendre de ses erreurs

### 1.1 Le principe fondamental

Le boosting repose sur une idée simple et puissante : **chaque nouveau modèle se concentre sur les erreurs des modèles précédents**. Au lieu d'entraîner des modèles indépendants (comme Random Forest), on les entraîne **séquentiellement**, chacun corrigeant les faiblesses du précédent.

```
Boosting = Apprentissage séquentiel

  Modèle 1 : prédit sur tout le dataset
             → fait des erreurs sur certains exemples

  Modèle 2 : se concentre sur les ERREURS du modèle 1
             → corrige une partie des erreurs

  Modèle 3 : se concentre sur les ERREURS résiduelles (modèle 1 + 2)
             → corrige encore plus

  ...

  Modèle N : corrige les dernières erreurs subtiles

  Prédiction finale = combinaison pondérée de TOUS les modèles
```

### 1.2 Analogie : un étudiant qui révise ses erreurs

```
Examen blanc 1 :
  ✅ Algèbre → 18/20
  ✅ Géométrie → 16/20
  ❌ Probabilités → 8/20
  ❌ Statistiques → 6/20

L'étudiant intelligent ne révise pas TOUT :
  → Il se concentre sur Probabilités et Statistiques

Examen blanc 2 (après révision ciblée) :
  ✅ Algèbre → 17/20 (stable)
  ✅ Géométrie → 15/20 (stable)
  ✅ Probabilités → 14/20 (amélioré !)
  ❌ Statistiques → 10/20 (amélioré, mais encore faible)

Il continue à cibler les faiblesses restantes :
  → Révise intensément les Statistiques

Examen blanc 3 :
  ✅ Algèbre → 17/20
  ✅ Géométrie → 16/20
  ✅ Probabilités → 15/20
  ✅ Statistiques → 14/20  (enfin bon !)

C'est EXACTEMENT ce que fait le Boosting :
  → Chaque itération cible les exemples les plus difficiles
```

> 💡 **Conseil** : "Le boosting est comme un étudiant méthodique : il identifie ses faiblesses et travaille dessus en priorité. C'est pourquoi il est si efficace pour atteindre de hautes performances."

---

## 2. 📊 Différence fondamentale avec Random Forest

### 2.1 Parallèle (RF) vs séquentiel (Boosting)

```
Random Forest (Bagging) :                Boosting :

  ┌────────┐  ┌────────┐  ┌────────┐     ┌────────┐
  │ Arbre 1│  │ Arbre 2│  │ Arbre 3│     │ Arbre 1│
  └───┬────┘  └───┬────┘  └───┬────┘     └───┬────┘
      │           │           │               │ erreurs
      │           │           │               ▼
      │           │           │           ┌────────┐
      │           │           │           │ Arbre 2│
      │           │           │           └───┬────┘
      │           │           │               │ erreurs
      ▼           ▼           ▼               ▼
  ┌──────────────────────────────┐       ┌────────┐
  │   VOTE MAJORITAIRE / MOYENNE │       │ Arbre 3│
  └──────────────────────────────┘       └───┬────┘
                                              │
  Arbres indépendants, en parallèle           ▼
  → Réduit la VARIANCE                   ┌──────────────────┐
                                          │ SOMME PONDÉRÉE   │
                                          └──────────────────┘

                                          Arbres séquentiels
                                          → Réduit le BIAIS
```

### 2.2 Variance vs biais

| Concept | Random Forest (Bagging) | Boosting |
|---------|------------------------|----------|
| **Stratégie** | Modèles indépendants en parallèle | Modèles séquentiels, chacun corrige le précédent |
| **Réduit principalement** | La **variance** (instabilité) | Le **biais** (erreur systématique) |
| **Modèles de base** | Arbres profonds (haute variance) | Arbres peu profonds (haut biais) |
| **Risque d'overfitting** | Faible (les erreurs se moyennent) | Modéré à élevé (apprend le bruit) |
| **Données bruitées** | Robuste (résiste au bruit) | Sensible (peut apprendre le bruit) |
| **Performance typique** | Bonne | Excellente (si bien réglé) |
| **Facilité de tuning** | Peu de tuning nécessaire | Tuning important pour éviter l'overfitting |
| **Parallélisable** | Oui (entraînement) | Non (séquentiel par nature) |

### 2.3 Tableau comparatif détaillé

| Critère | Random Forest | Gradient Boosting | XGBoost | LightGBM |
|---------|--------------|-------------------|---------|----------|
| **Principe** | Bagging | Boosting séquentiel | Boosting optimisé | Boosting ultra-rapide |
| **Arbres** | Profonds, indépendants | Peu profonds, séquentiels | Peu profonds, séquentiels | Peu profonds, séquentiels |
| **Vitesse entraînement** | Rapide (parallèle) | Lent (séquentiel) | Modérée | Rapide |
| **Vitesse prédiction** | Modérée | Modérée | Rapide | Très rapide |
| **Risque overfitting** | Faible | Modéré | Modéré (régularisation) | Modéré |
| **Gestion NaN** | Non | Non | Oui | Oui |
| **Performance** | Bonne | Très bonne | Excellente | Excellente |
| **Facilité d'usage** | Très facile | Modérée | Modérée | Modérée |

> ⚠️ **Attention** : "Le boosting est plus puissant que le bagging, mais aussi plus fragile. Un Random Forest mal réglé donnera quand même de bons résultats. Un Gradient Boosting mal réglé peut donner des résultats catastrophiques (overfitting sévère)."

---

## 3. ⚙️ Gradient Boosting expliqué pas à pas

### 3.1 L'algorithme en 4 étapes

Prenons un exemple de **régression** pour illustrer le Gradient Boosting :

```
Dataset : prédire le prix d'un appartement

Surface (m²) :  [30,  50,  70,  90,  120]
Prix réel (k€) : [90, 150, 200, 250, 350]

═══ ÉTAPE 1 : Modèle initial (la moyenne) ═══

  Prédiction initiale F₀ = moyenne(prix) = (90+150+200+250+350)/5 = 208 k€

  Prédictions : [208, 208, 208, 208, 208]
  Prix réels  : [ 90, 150, 200, 250, 350]

═══ ÉTAPE 2 : Calculer les résidus ═══

  Résidus = Prix réel - Prédiction
  Résidus : [90-208, 150-208, 200-208, 250-208, 350-208]
          = [-118,    -58,      -8,     42,     142]

  Ces résidus sont les ERREURS du modèle actuel.

═══ ÉTAPE 3 : Entraîner un arbre sur les résidus ═══

  Arbre 1 apprend à prédire les résidus à partir de la surface :
  Surface → Résidu
  30 m²   → -118
  50 m²   → -58
  70 m²   → -8
  90 m²   → +42
  120 m²  → +142

═══ ÉTAPE 4 : Mettre à jour les prédictions ═══

  F₁ = F₀ + learning_rate × Arbre1(X)

  Avec learning_rate = 0.1 :
  Nouvelles prédictions = 208 + 0.1 × [-118, -58, -8, 42, 142]
                        = [196.2, 202.2, 207.2, 212.2, 222.2]

  Nouvelles erreurs : [90-196.2, 150-202.2, 200-207.2, 250-212.2, 350-222.2]
                     = [-106.2,   -52.2,     -7.2,      37.8,     127.8]

  → Les erreurs sont plus petites ! On continue...

═══ RÉPÉTER ═══

  Étape 2 bis : résidus de F₁
  Étape 3 bis : arbre 2 sur les nouveaux résidus
  Étape 4 bis : F₂ = F₁ + 0.1 × Arbre2(X)

  ... Après 100 itérations, les résidus → ~0
```

### 3.2 Pourquoi le learning rate ?

```
Sans learning rate (= 1.0) :
  Chaque arbre corrige 100% de l'erreur d'un coup
  → Risque élevé d'overfitting (trop agressif)

Avec learning rate petit (= 0.1) :
  Chaque arbre corrige seulement 10% de l'erreur
  → Plus de pas nécessaires, mais meilleure généralisation
  → Comme marcher prudemment vers le minimum

Règle d'or :
  learning_rate ↓ = n_estimators ↑ = meilleur résultat (mais plus lent)
  learning_rate=0.01 + n_estimators=1000 > learning_rate=0.3 + n_estimators=100
```

### 3.3 Code from scratch simplifié

```python
import numpy as np
from sklearn.tree import DecisionTreeRegressor

def gradient_boosting_simple(X, y, n_estimators=100, learning_rate=0.1, max_depth=3):
    """Gradient Boosting from scratch (version simplifiée)"""

    # Étape 1 : prédiction initiale = moyenne
    prediction = np.full(len(y), y.mean())
    arbres = []

    for i in range(n_estimators):
        # Étape 2 : calculer les résidus
        residus = y - prediction

        # Étape 3 : entraîner un arbre sur les résidus
        arbre = DecisionTreeRegressor(max_depth=max_depth)
        arbre.fit(X, residus)
        arbres.append(arbre)

        # Étape 4 : mettre à jour les prédictions
        prediction += learning_rate * arbre.predict(X)

        # Afficher la progression
        if (i + 1) % 20 == 0:
            mse = np.mean((y - prediction) ** 2)
            print(f"  Itération {i+1:>3} : MSE = {mse:.4f}")

    return arbres, y.mean()

# Exemple d'utilisation
from sklearn.datasets import make_regression
X, y = make_regression(n_samples=200, n_features=5, noise=20, random_state=42)

print("=== Gradient Boosting from scratch ===\n")
arbres, base = gradient_boosting_simple(X, y, n_estimators=100, learning_rate=0.1)

# Prédiction
def predire(X, arbres, base, learning_rate=0.1):
    prediction = np.full(X.shape[0], base)
    for arbre in arbres:
        prediction += learning_rate * arbre.predict(X)
    return prediction

y_pred = predire(X, arbres, base)
print(f"\nR² final : {1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2):.4f}")
```

> 💡 **Conseil** : "Comprendre le Gradient Boosting from scratch permet de saisir intuitivement comment fonctionne XGBoost/LightGBM. L'idée clé : chaque arbre apprend à prédire les **résidus** (erreurs) du modèle précédent."

---

## 4. 🏆 XGBoost

### 4.1 Pourquoi XGBoost est populaire

XGBoost (eXtreme Gradient Boosting) domine les compétitions de ML depuis 2014 pour plusieurs raisons :

| Avantage | Description |
|----------|-------------|
| **Régularisation intégrée** | L1 (Lasso) et L2 (Ridge) pour limiter l'overfitting |
| **Gestion des NaN** | Apprend automatiquement la direction optimale pour les valeurs manquantes |
| **Parallélisation des splits** | Bien que séquentiel au niveau des arbres, les splits sont parallélisés |
| **Pruning intelligent** | Élagage par "gain" plutôt que par profondeur fixe |
| **Cache-aware** | Optimisé pour l'utilisation du cache CPU |
| **Early stopping** | Arrêt automatique quand le score stagne |

### 4.2 Installation et API

```bash
# Installation
uv add xgboost
```

### 4.3 Code complet sur churn dataset

```python
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score,
    accuracy_score, roc_curve
)
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt

# Générer un dataset churn
X, y = make_classification(
    n_samples=5000, n_features=15, n_informative=8,
    n_redundant=3, n_clusters_per_class=2,
    weights=[0.7, 0.3],  # 30% de churn
    random_state=42
)
feature_names = [f'feature_{i}' for i in range(X.shape[1])]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Créer le modèle XGBoost
xgb_clf = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,         # petit = meilleur, mais plus lent
    max_depth=6,                # profondeur des arbres
    min_child_weight=5,         # régularisation (≈ min_samples_leaf)
    subsample=0.8,              # 80% des lignes par arbre
    colsample_bytree=0.8,      # 80% des features par arbre
    reg_alpha=0.1,              # régularisation L1
    reg_lambda=1.0,             # régularisation L2
    scale_pos_weight=2.3,       # ratio négatifs/positifs pour classes déséquilibrées
    random_state=42,
    n_jobs=-1,
    eval_metric='logloss',
    early_stopping_rounds=50    # arrêter si pas d'amélioration pendant 50 rounds
)

# Entraîner avec early stopping
xgb_clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=50
)

# Résultats
y_pred = xgb_clf.predict(X_test)
y_proba = xgb_clf.predict_proba(X_test)[:, 1]

print(f"\n=== XGBoost — Résultats ===")
print(f"Meilleur nombre d'itérations : {xgb_clf.best_iteration}")
print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
print(f"AUC-ROC   : {roc_auc_score(y_test, y_proba):.4f}")
print(f"\n{classification_report(y_test, y_pred)}")

# Feature importance
importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': xgb_clf.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(importance['Feature'][:10][::-1],
         importance['Importance'][:10][::-1],
         color='steelblue')
plt.xlabel('Importance (gain)')
plt.title('Top 10 Features — XGBoost')
plt.tight_layout()
plt.show()
```

### 4.4 Hyperparamètres clés

| Hyperparamètre | Description | Plage recommandée | Impact |
|----------------|-------------|-------------------|--------|
| `learning_rate` (eta) | Contribution de chaque arbre | 0.01 - 0.1 | Plus petit = plus robuste, plus lent |
| `n_estimators` | Nombre d'arbres | 500-5000 (avec early stop) | Utiliser early stopping |
| `max_depth` | Profondeur des arbres | 3-10 | Plus profond = plus complexe |
| `min_child_weight` | Poids min par feuille | 1-10 | Régularisation |
| `subsample` | % lignes par arbre | 0.6-0.9 | Réduction de variance |
| `colsample_bytree` | % features par arbre | 0.6-0.9 | Diversité des arbres |
| `reg_alpha` | Régularisation L1 | 0-1 | Sparsité |
| `reg_lambda` | Régularisation L2 | 0-10 | Lissage |
| `gamma` | Min gain pour split | 0-5 | Complexité |
| `scale_pos_weight` | Ratio classes | n_neg / n_pos | Classes déséquilibrées |

> 💡 **Conseil** : "Recette XGBoost qui marche : learning_rate=0.05, max_depth=6, subsample=0.8, colsample_bytree=0.8, n_estimators=2000 avec early_stopping_rounds=50. Laissez l'early stopping trouver le bon nombre d'arbres."

---

## 5. ⚡ LightGBM

### 5.1 Différence avec XGBoost

La différence principale est dans la **stratégie de croissance des arbres** :

```
XGBoost : Level-wise (croissance par niveau)
─────────────────────────────────────────────

  Niveau 0 :       ┌────────┐
                    │  Noeud │
                    └───┬────┘
                   ╱         ╲
  Niveau 1 : ┌────────┐  ┌────────┐     ← TOUS les noeuds du niveau 1
              │ Noeud  │  │ Noeud  │        sont développés avant
              └───┬────┘  └───┬────┘        de passer au niveau 2
             ╱    ╲      ╱    ╲
  Niveau 2 : ...  ...  ...  ...          ← puis tous ceux du niveau 2

  → Arbres équilibrés, mais développe des branches inutiles


LightGBM : Leaf-wise (croissance par feuille)
──────────────────────────────────────────────

  Étape 1 :        ┌────────┐
                    │  Noeud │
                    └───┬────┘
                   ╱         ╲
  Étape 2 :  ┌────────┐  [feuille]     ← Développe SEULEMENT
              │ Noeud  │                   la feuille avec le
              └───┬────┘                   plus grand gain
             ╱         ╲
  Étape 3 : [feuille]  ┌────────┐
                        │ Noeud  │      ← Puis la suivante
                        └───┬────┘
                       ╱         ╲
                     ...        ...

  → Arbres déséquilibrés, mais plus efficaces (moins de splits inutiles)
  → Plus rapide, même performance ou meilleure
```

| Critère | XGBoost | LightGBM |
|---------|---------|----------|
| **Croissance** | Level-wise (par niveau) | Leaf-wise (par feuille) |
| **Vitesse** | Modérée | 2-10x plus rapide |
| **Mémoire** | Modérée | Plus efficace |
| **Grands datasets** | Correct | Excellent (>1M lignes) |
| **Catégorielles** | Encoding nécessaire | Gestion native |
| **Risque overfitting** | Modéré | Légèrement plus élevé |
| **Maturité** | Très mature | Mature |

### 5.2 Code complet LightGBM

```python
import lightgbm as lgb
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score

# Créer le modèle LightGBM
lgb_clf = lgb.LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=-1,              # -1 = illimité (leaf-wise gère la profondeur)
    num_leaves=31,             # paramètre clé de LightGBM (2^max_depth - 1)
    min_child_samples=20,      # min échantillons par feuille
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    n_jobs=-1,
    verbose=-1                 # silencieux
)

# Entraîner avec early stopping
lgb_clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    callbacks=[
        lgb.early_stopping(50, verbose=True),
        lgb.log_evaluation(50)
    ]
)

# Résultats
y_pred_lgb = lgb_clf.predict(X_test)
y_proba_lgb = lgb_clf.predict_proba(X_test)[:, 1]

print(f"\n=== LightGBM — Résultats ===")
print(f"Meilleur nombre d'itérations : {lgb_clf.best_iteration_}")
print(f"Accuracy  : {accuracy_score(y_test, y_pred_lgb):.4f}")
print(f"AUC-ROC   : {roc_auc_score(y_test, y_proba_lgb):.4f}")
```

### 5.3 Gestion native des catégorielles

L'un des grands avantages de LightGBM est la gestion **native** des variables catégorielles, sans besoin de One-Hot Encoding :

```python
import lightgbm as lgb
import pandas as pd

# Exemple avec des catégorielles
df = pd.DataFrame({
    'ville': ['Paris', 'Lyon', 'Paris', 'Marseille', 'Lyon', 'Paris'],
    'contrat': ['mensuel', 'annuel', 'mensuel', 'annuel', 'mensuel', 'annuel'],
    'montant': [50, 30, 60, 25, 45, 35],
    'churn': [1, 0, 1, 0, 1, 0]
})

# Convertir en category (LightGBM les gère automatiquement)
df['ville'] = df['ville'].astype('category')
df['contrat'] = df['contrat'].astype('category')

X = df.drop('churn', axis=1)
y = df['churn']

# LightGBM gère nativement les catégorielles
lgb_model = lgb.LGBMClassifier(n_estimators=100, verbose=-1)
lgb_model.fit(X, y, categorical_feature=['ville', 'contrat'])
# Pas besoin de One-Hot Encoding !
```

> 💡 **Conseil** : "LightGBM est le meilleur choix quand vous avez un grand dataset (>100k lignes) ou beaucoup de variables catégorielles. Il est souvent 2-10x plus rapide que XGBoost avec des performances similaires ou meilleures."

---

## 6. 🐱 CatBoost

### 6.1 Spécialisé catégorielles

CatBoost (Categorical Boosting) a été développé par Yandex avec un focus sur les **variables catégorielles** et la réduction de l'overfitting.

| Caractéristique | Description |
|----------------|-------------|
| **Ordered Boosting** | Technique anti-overfitting unique qui évite le target leakage |
| **Catégorielles natives** | Meilleure gestion que XGBoost, comparable à LightGBM |
| **Target Encoding** | Encoding intelligent intégré (ordered target statistics) |
| **Symmetric Trees** | Arbres symétriques par défaut = prédiction très rapide |
| **GPU natif** | Excellente accélération GPU |

### 6.2 Ordered Boosting

```
Problème classique du boosting :
  Le modèle à l'itération t est entraîné sur des résidus calculés
  avec les MÊMES données → risque de target leakage → overfitting

Ordered Boosting (CatBoost) :
  Pour chaque échantillon, les résidus sont calculés uniquement
  avec les modèles entraînés sur les échantillons PRÉCÉDENTS
  (dans un ordre aléatoire) → pas de fuite d'information → moins d'overfitting
```

### 6.3 Code rapide CatBoost

```python
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

# Créer le modèle CatBoost
cat_clf = CatBoostClassifier(
    iterations=500,               # = n_estimators
    learning_rate=0.05,
    depth=6,                      # = max_depth
    l2_leaf_reg=3,                # régularisation L2
    random_seed=42,
    verbose=100,                  # afficher toutes les 100 itérations
    eval_metric='AUC',
    early_stopping_rounds=50
)

# Entraîner
cat_clf.fit(
    X_train, y_train,
    eval_set=(X_test, y_test),
    verbose=100
)

# Résultats
y_pred_cat = cat_clf.predict(X_test)
y_proba_cat = cat_clf.predict_proba(X_test)[:, 1]

print(f"\n=== CatBoost — Résultats ===")
print(f"Accuracy  : {accuracy_score(y_test, y_pred_cat):.4f}")
print(f"AUC-ROC   : {roc_auc_score(y_test, y_proba_cat):.4f}")
```

> 💡 **Conseil** : "CatBoost est excellent quand vous avez beaucoup de variables catégorielles et peu de temps pour le preprocessing. Il gère tout automatiquement et l'ordered boosting réduit naturellement l'overfitting."

---

## 7. 📋 Comparaison XGBoost vs LightGBM vs CatBoost

### 7.1 Tableau comparatif

| Critère | XGBoost | LightGBM | CatBoost |
|---------|---------|----------|----------|
| **Développeur** | Tianqi Chen (2014) | Microsoft (2017) | Yandex (2017) |
| **Stratégie de croissance** | Level-wise | Leaf-wise | Symmetric trees |
| **Vitesse entraînement** | Modérée | Rapide | Modérée |
| **Vitesse prédiction** | Rapide | Très rapide | Très rapide |
| **Gestion des NaN** | Oui (apprise) | Oui | Oui |
| **Catégorielles natives** | Non (encoding requis) | Oui (basique) | Oui (excellente) |
| **Régularisation** | L1 + L2 | L1 + L2 | L2 + Ordered Boosting |
| **GPU** | Oui | Oui | Oui (excellent) |
| **Datasets volumineux** | Correct | Excellent | Correct |
| **Facilité d'utilisation** | Modérée | Modérée | Facile (peu de tuning) |
| **Communauté** | Très large | Large | Croissante |
| **API sklearn** | Oui | Oui | Oui |

### 7.2 Quand utiliser lequel ?

| Situation | Recommandation | Justification |
|-----------|---------------|---------------|
| Premier essai / défaut | **XGBoost** | Le plus documenté, communauté la plus large |
| Grand dataset (>1M lignes) | **LightGBM** | 2-10x plus rapide |
| Beaucoup de catégorielles | **CatBoost** | Gestion native optimale |
| Compétition Kaggle | **LightGBM** ou **XGBoost** | Performances top, flexibilité de tuning |
| Production (inférence rapide) | **LightGBM** ou **CatBoost** | Prédiction ultra-rapide |
| Peu de temps pour le tuning | **CatBoost** | Bons résultats out-of-the-box |
| Données bruitées | **CatBoost** | Ordered boosting réduit l'overfitting |

### 7.3 Benchmark rapide

```python
import time
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score

# Paramètres communs
params_communs = {
    'n_estimators': 300,
    'learning_rate': 0.05,
    'max_depth': 6,
    'random_state': 42,
}

modeles = {
    'XGBoost': xgb.XGBClassifier(
        **{k: v for k, v in params_communs.items()},
        n_jobs=-1, eval_metric='logloss', verbosity=0
    ),
    'LightGBM': lgb.LGBMClassifier(
        **{k: v for k, v in params_communs.items()},
        n_jobs=-1, verbose=-1
    ),
    'CatBoost': CatBoostClassifier(
        iterations=params_communs['n_estimators'],
        learning_rate=params_communs['learning_rate'],
        depth=params_communs['max_depth'],
        random_seed=params_communs['random_state'],
        verbose=0
    ),
}

print("=== Benchmark XGBoost vs LightGBM vs CatBoost ===\n")
print(f"{'Modèle':>12} {'AUC-ROC':>10} {'Temps fit (s)':>15} {'Temps predict (ms)':>20}")
print(f"{'─'*60}")

for nom, modele in modeles.items():
    # Temps de fit
    start = time.time()
    modele.fit(X_train, y_train)
    temps_fit = time.time() - start

    # Temps de predict
    start = time.time()
    for _ in range(100):
        y_proba = modele.predict_proba(X_test)[:, 1]
    temps_predict = (time.time() - start) / 100 * 1000

    # Score
    auc = roc_auc_score(y_test, y_proba)

    print(f"{nom:>12} {auc:>10.4f} {temps_fit:>15.2f} {temps_predict:>20.2f}")
```

---

## 8. 🎯 Bonus : SVM (aperçu)

### 8.1 Trouver la meilleure frontière

Les **Support Vector Machines** (SVM) cherchent l'hyperplan qui sépare les classes avec la **marge maximale** :

```
Mauvaise frontière :              Bonne frontière (SVM) :

  ● ●  ● / ▲ ▲                    ●  ●  ● │ ▲  ▲
  ●  ● /  ▲  ▲ ▲                  ●  ● ●  │  ▲ ▲ ▲
  ● ● / ▲  ▲  ▲                   ● ●  ●  │ ▲  ▲ ▲
                                       ↑←marge→↑
  La frontière est proche             La frontière maximise
  de certains points                  la distance aux points
  → instable, peu robuste            les plus proches (supports)
                                      → stable, bonne généralisation
```

### 8.2 Concept de marge maximale

```
            Support vectors (les points les plus proches)
                    ↓           ↓
  ●  ●  ●    ●    ‖     │     ‖    ▲    ▲  ▲  ▲
  ●  ● ●    ●     ‖     │     ‖   ▲  ▲    ▲
  ●  ●  ●  ●      ‖     │     ‖     ▲  ▲  ▲
                   ‖     │     ‖
                   ← marge →  ← marge →
                    ↑
              hyperplan de séparation

  L'objectif du SVM : maximiser la marge totale
  Seuls les "support vectors" (points sur la marge) influencent la frontière
```

### 8.3 Le Kernel Trick (intuition)

Quand les données ne sont pas linéairement séparables, le **kernel trick** projette les données dans un espace de dimension supérieure où elles deviennent séparables :

```
En 1D : pas séparable                En 2D (après kernel) : séparable !

  ▲ ▲ ● ● ● ▲ ▲                          ▲           ▲
  ──────────────── x                      │ ▲       ▲ │
                                          │   ● ● ●   │
  Impossible de séparer                   │  ●  ●  ●  │
  ● et ▲ avec une droite                  │   ● ● ●   │
                                          │ ▲       ▲ │
  φ(x) = x² transforme :                 ▲           ▲
  ▲ à x=1,7 → x²=1,49                        ↑ x²
  ● à x=3,4,5 → x²=9,16,25             On peut séparer
                                         avec un cercle !
```

```python
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# SVM avec kernel RBF (le plus courant)
svm = SVC(
    kernel='rbf',        # Radial Basis Function (gaussien)
    C=1.0,               # paramètre de régularisation
    gamma='scale',       # paramètre du kernel RBF
    probability=True,    # activer predict_proba (plus lent)
    random_state=42
)

svm.fit(X_train, y_train)

y_pred_svm = svm.predict(X_test)
print(f"SVM Accuracy : {accuracy_score(y_test, y_pred_svm):.4f}")
print(classification_report(y_test, y_pred_svm))
```

### 8.4 Quand utiliser SVM

| Situation | SVM adapté ? | Justification |
|-----------|-------------|---------------|
| Peu de données (<10k) | Oui | SVM excelle en petit dataset |
| Haute dimension | Oui | Gère bien les features > échantillons |
| Grand dataset (>100k) | Non | Trop lent (O(n²) à O(n³)) |
| Besoin d'interprétabilité | Non | Modèle "boîte noire" |
| Classification d'images (classique) | Oui | Kernel RBF performant |
| Classification de texte | Oui | SVM linéaire excellent |
| Régression | Possible | SVR existe, mais moins utilisé |

> ⚠️ **Attention** : "Le SVM est un excellent algorithme, mais il est dépassé par XGBoost/LightGBM sur la plupart des problèmes tabulaires. Il reste pertinent pour les petits datasets et les données textuelles avec peu de preprocessing."

---

## 9. 📋 Guide de choix final : Quel algorithme pour quel problème ?

### 9.1 Tableau de synthèse

| Critère | Rég. Linéaire | Rég. Logistique | KNN | Arbre | Random Forest | XGBoost/LightGBM | SVM |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Régression** | Oui | Non | Oui | Oui | Oui | Oui | Oui |
| **Classification** | Non | Oui | Oui | Oui | Oui | Oui | Oui |
| **Interprétabilité** | Excellente | Bonne | Faible | Excellente | Bonne | Moyenne | Faible |
| **Performance** | Faible-Moyenne | Moyenne | Moyenne | Moyenne | Bonne | Excellente | Bonne |
| **Scaling nécessaire** | Non* | Oui | Oui | Non | Non | Non | Oui |
| **Gère non-linéarité** | Non | Non | Oui | Oui | Oui | Oui | Oui (kernel) |
| **Données > 100k** | Oui | Oui | Non | Oui | Oui | Oui | Non |
| **Peu de données** | Oui | Oui | Oui | Risqué | Oui | Risqué | Oui |
| **Sensible outliers** | Très | Peu | Oui | Peu | Peu | Peu | Oui |
| **Facilité tuning** | Facile | Facile | Moyen | Moyen | Facile | Complexe | Complexe |

*Scaling recommandé pour comparer les coefficients

### 9.2 Arbre de décision : quel algorithme choisir ?

```
                      ┌──────────────────────────┐
                      │  Mon problème est...      │
                      └────────────┬─────────────┘
                              ╱         ╲
               Régression  ╱               ╲  Classification
                         ╱                   ╲
            ┌──────────────────┐    ┌──────────────────┐
            │ Besoin            │    │ Besoin            │
            │ d'interprétabilité│    │ d'interprétabilité│
            │ maximale ?        │    │ maximale ?        │
            └────────┬─────────┘    └────────┬─────────┘
                ╱         ╲             ╱         ╲
          Oui ╱             ╲ Non Oui ╱             ╲ Non
            ╱                 ╲     ╱                 ╲
  ┌────────────────┐ ┌──────────┐ ┌────────────────┐ ┌──────────┐
  │ Rég. Linéaire  │ │ Combien  │ │ Rég. Logistique│ │ Combien  │
  │ (baseline)     │ │ de       │ │ (baseline)     │ │ de       │
  │                │ │ données ?│ │                │ │ données ?│
  └────────────────┘ └────┬─────┘ └────────────────┘ └────┬─────┘
                      ╱       ╲                       ╱       ╲
                 <10k ╱         ╲ >10k           <10k ╱         ╲ >10k
                    ╱             ╲                 ╱             ╲
          ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
          │ Random Forest│ │ LightGBM /   │ │ Random Forest│ │ LightGBM /   │
          │ ou SVM       │ │ XGBoost      │ │ ou SVM       │ │ XGBoost      │
          └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

### 9.3 Stratégie recommandée pour tout projet ML

```python
# STRATÉGIE EN 4 ÉTAPES

# Étape 1 : BASELINE SIMPLE (5 minutes)
# → Régression linéaire ou logistique
from sklearn.linear_model import LogisticRegression
baseline = LogisticRegression(max_iter=1000)
baseline.fit(X_train, y_train)
print(f"Baseline : {baseline.score(X_test, y_test):.4f}")

# Étape 2 : RANDOM FOREST (10 minutes)
# → Bon résultat avec peu de tuning
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
print(f"Random Forest : {rf.score(X_test, y_test):.4f}")

# Étape 3 : BOOSTING (30 minutes)
# → Performance maximale
import lightgbm as lgb
lgbm = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, verbose=-1)
lgbm.fit(X_train, y_train,
         eval_set=[(X_test, y_test)],
         callbacks=[lgb.early_stopping(50, verbose=False)])
print(f"LightGBM : {lgbm.score(X_test, y_test):.4f}")

# Étape 4 : TUNING (si nécessaire, 1-2 heures)
# → Optimiser les hyperparamètres du meilleur modèle
# → Voir chapitres précédents pour GridSearchCV / RandomizedSearchCV
```

> 💡 **Conseil** : "Ne passez pas directement à XGBoost. Commencez **toujours** par une baseline simple (régression logistique), puis Random Forest, puis boosting. Si la baseline suffit, pas besoin de complexifier. La différence entre RF et XGBoost n'est souvent que de 1-3%."

> ⚠️ **Attention** : "L'algorithme ne fait pas tout. Un bon feature engineering avec une régression logistique battra souvent un XGBoost mal entraîné sur des features brutes. Investissez dans la compréhension de vos données avant le choix de l'algorithme."

---

## 🎯 Points clés à retenir

1. **Le boosting apprend de ses erreurs** : chaque arbre corrige les erreurs des précédents (apprentissage séquentiel)
2. **Random Forest réduit la variance** (modèles indépendants), le **boosting réduit le biais** (modèles séquentiels)
3. **Le Gradient Boosting** entraîne des arbres successifs sur les **résidus** (erreurs) du modèle courant
4. **Le learning rate** contrôle l'agressivité de chaque correction — plus petit = meilleur résultat mais plus lent
5. **XGBoost** est la référence : régularisation L1/L2, gestion des NaN, early stopping, parallélisation des splits
6. **LightGBM** est 2-10x plus rapide grâce à la croissance leaf-wise — idéal pour les grands datasets
7. **CatBoost** excelle sur les données catégorielles et réduit l'overfitting avec l'ordered boosting
8. **L'early stopping** est indispensable pour le boosting : mettez n_estimators très haut et laissez l'algorithme s'arrêter seul
9. **Les SVM** restent pertinents pour les petits datasets et les données textuelles, mais sont dépassés par le boosting sur les données tabulaires
10. **Stratégie universelle** : baseline simple puis Random Forest puis LightGBM/XGBoost — ne jamais sauter les étapes

---

## ✅ Checklist de validation

- [ ] Je sais expliquer l'intuition du boosting (apprendre de ses erreurs, séquentiel)
- [ ] Je connais la différence fondamentale entre Random Forest (variance) et Boosting (biais)
- [ ] Je sais expliquer le Gradient Boosting pas à pas (résidus, learning rate, accumulation)
- [ ] Je sais implémenter XGBoost avec early stopping
- [ ] Je connais les hyperparamètres clés de XGBoost (learning_rate, max_depth, subsample, reg_alpha/lambda)
- [ ] Je sais quand utiliser LightGBM plutôt que XGBoost (grands datasets, vitesse)
- [ ] Je comprends la différence level-wise vs leaf-wise
- [ ] Je sais que CatBoost excelle sur les catégorielles et réduit l'overfitting naturellement
- [ ] Je connais les bases des SVM (marge maximale, kernel trick)
- [ ] Je sais choisir le bon algorithme selon le contexte (taille des données, interprétabilité, performance)
- [ ] Je maîtrise la stratégie en 4 étapes : baseline → RF → Boosting → Tuning

---

**Précédent** : [Chapitre 10 : Arbres de Décision et Forêts Aléatoires](10-arbres-forets.md)

**Suivant** : [Chapitre 12 : Réduction de Dimension et Clustering Avancé](12-dimension-clustering.md)
