# Chapitre 6 : Méthodes d'Ensemble – La Force du Collectif

## 🎯 Objectifs

- Comprendre le principe fondamental des méthodes d'ensemble
- Maîtriser le fonctionnement de Random Forest et ses hyperparamètres
- Comprendre la famille du Boosting : AdaBoost, Gradient Boosting, XGBoost
- Savoir interpréter les feature importances de manière fiable
- Maîtriser le tuning d'hyperparamètres avec GridSearchCV et RandomizedSearchCV
- Savoir choisir la bonne méthode d'ensemble selon le contexte

---

## 1. 🧠 Principe des méthodes d'ensemble

### 1.1 La sagesse des foules

Le principe des méthodes d'ensemble repose sur une idée simple mais puissante : **combiner plusieurs modèles faibles pour obtenir un modèle fort**. C'est le même principe que la « sagesse des foules » : si vous demandez à 1 000 personnes d'estimer le poids d'un bœuf, la moyenne des estimations sera remarquablement proche du poids réel, même si chaque estimation individuelle est imprécise.

En Machine Learning, cela se traduit par :

- Chaque modèle individuel (appelé **learner faible**) fait des erreurs
- Ces erreurs sont **différentes** d'un modèle à l'autre
- En **combinant** les prédictions, les erreurs se compensent
- Le modèle final est **plus performant** et **plus robuste** que chaque modèle individuel

### 1.2 Bagging vs Boosting

Les deux grandes familles de méthodes d'ensemble se distinguent par leur stratégie de combinaison :

| Caractéristique | **Bagging** | **Boosting** |
|---|---|---|
| Principe | Modèles en **parallèle** | Modèles en **séquence** |
| Échantillonnage | Bootstrap (avec remise) | Pondération des erreurs |
| Objectif principal | Réduire la **variance** | Réduire le **biais** |
| Risque d'overfitting | Faible | Modéré à élevé |
| Vitesse d'entraînement | Parallélisable | Séquentiel (plus lent) |
| Exemple phare | Random Forest | XGBoost, LightGBM |
| Sensibilité au bruit | Robuste | Sensible (apprend le bruit) |

> 💡 **Conseil** : "Si vos données sont bruitées (beaucoup d'outliers, labels incertains), préférez le Bagging. Si vos données sont propres et que vous cherchez la performance maximale, le Boosting sera souvent meilleur."

---

## 2. 🌲 Bagging et Random Forest

### 2.1 Bagging (Bootstrap Aggregating)

Le Bagging, inventé par Leo Breiman en 1996, suit un processus en trois étapes :

1. **Créer N échantillons bootstrap** : tirer avec remise depuis le dataset d'entraînement (chaque échantillon contient ~63% des données originales)
2. **Entraîner N modèles indépendants** : chacun sur son échantillon bootstrap
3. **Agréger les prédictions** :
   - Classification → **vote majoritaire**
   - Régression → **moyenne des prédictions**

```python
import numpy as np
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Générer des données d'exemple
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Bagging avec des arbres de décision
bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(),  # modèle de base
    n_estimators=100,                     # nombre de modèles
    max_samples=0.8,                      # 80% des données par échantillon
    max_features=0.8,                     # 80% des features par modèle
    bootstrap=True,                       # tirage avec remise
    random_state=42,
    n_jobs=-1                             # paralléliser sur tous les cœurs
)

bagging.fit(X_train, y_train)

# Évaluation
y_pred = bagging.predict(X_test)
print(f"Accuracy du Bagging : {accuracy_score(y_test, y_pred):.4f}")
```

> 💡 **Conseil** : "Le Bagging est particulièrement efficace avec des modèles instables (haute variance) comme les arbres de décision. Il n'apporte presque rien avec des modèles stables comme la régression logistique."

### 2.2 Random Forest

Random Forest est l'amélioration la plus célèbre du Bagging. L'idée clé est d'ajouter une **double source d'aléatoire** :

1. **Échantillons bootstrap** (comme le Bagging classique)
2. **Sélection aléatoire de features** à chaque split de chaque arbre

Cette double randomisation rend les arbres plus **décorrélés** entre eux, ce qui améliore la qualité de l'agrégation.

#### Hyperparamètres clés

| Hyperparamètre | Description | Valeur par défaut | Conseil de tuning |
|---|---|---|---|
| `n_estimators` | Nombre d'arbres | 100 | 100-1000, plus = mieux (mais plus lent) |
| `max_depth` | Profondeur max des arbres | None (illimitée) | 10-30, ou None |
| `min_samples_split` | Échantillons min pour splitter | 2 | 2-20 |
| `min_samples_leaf` | Échantillons min par feuille | 1 | 1-10 |
| `max_features` | Features à considérer par split | 'sqrt' | 'sqrt', 'log2', 0.3-0.8 |
| `class_weight` | Poids des classes | None | 'balanced' si classes déséquilibrées |
| `n_jobs` | Parallélisation | 1 | -1 (tous les cœurs) |

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import pandas as pd

# Créer et entraîner le Random Forest
rf = RandomForestClassifier(
    n_estimators=200,        # 200 arbres
    max_depth=20,            # profondeur max de 20
    min_samples_split=5,     # au moins 5 échantillons pour splitter
    min_samples_leaf=2,      # au moins 2 échantillons par feuille
    max_features='sqrt',     # racine carrée du nombre de features
    class_weight='balanced', # gestion des classes déséquilibrées
    random_state=42,
    n_jobs=-1                # utiliser tous les cœurs
)

rf.fit(X_train, y_train)

# Prédictions
y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

# Rapport de classification complet
print("=== Rapport de classification ===")
print(classification_report(y_test, y_pred))

# AUC-ROC
auc = roc_auc_score(y_test, y_proba)
print(f"AUC-ROC : {auc:.4f}")

# Score OOB (Out-Of-Bag) - estimation gratuite de la performance
rf_oob = RandomForestClassifier(
    n_estimators=200,
    oob_score=True,      # activer le score OOB
    random_state=42,
    n_jobs=-1
)
rf_oob.fit(X_train, y_train)
print(f"Score OOB : {rf_oob.oob_score_:.4f}")
```

> 💡 **Conseil de pro** : "Random Forest est souvent le meilleur premier modèle à essayer : peu de tuning nécessaire, gère les non-linéarités, résistant à l'overfitting, et fournit des feature importances gratuitement. C'est votre couteau suisse du ML."

> 💡 **Conseil** : "Commencez avec 100 arbres et augmentez si le score continue de monter. Au-delà de 500 arbres, le gain marginal est généralement négligeable. Vérifiez avec le score OOB."

#### Feature Importance avec Random Forest

Random Forest calcule automatiquement l'importance de chaque feature :

```python
import matplotlib.pyplot as plt

# Récupérer les importances
importances = rf.feature_importances_
feature_names = [f"feature_{i}" for i in range(X.shape[1])]

# Créer un DataFrame trié
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)

# Visualiser les top 10 features
plt.figure(figsize=(10, 6))
plt.barh(
    importance_df['feature'][:10][::-1],
    importance_df['importance'][:10][::-1]
)
plt.xlabel('Importance (Gini)')
plt.title('Top 10 Features les plus importantes (Random Forest)')
plt.tight_layout()
plt.show()
```

> ⚠️ **Attention** : "Les feature importances basées sur l'impureté (Gini) ont un biais connu : elles surestiment l'importance des features à haute cardinalité (beaucoup de valeurs uniques). Préférez la permutation importance pour des résultats fiables (voir section 6)."

---

## 3. ⚡ Boosting

### 3.1 AdaBoost (Adaptive Boosting)

AdaBoost, créé par Freund et Schapire en 1997, est le premier algorithme de Boosting à avoir connu un succès pratique.

**Principe :**

1. Entraîner un premier modèle faible (souvent un arbre à 1 niveau = « decision stump »)
2. Identifier les **échantillons mal classés**
3. **Augmenter le poids** de ces échantillons pour le prochain modèle
4. Entraîner un nouveau modèle qui se concentre sur les erreurs
5. Répéter N fois
6. Combiner les modèles avec des **poids proportionnels à leur performance**

```python
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

# AdaBoost avec des stumps (arbres à 1 niveau)
ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),  # stump
    n_estimators=200,
    learning_rate=0.1,     # contribution de chaque modèle
    random_state=42
)

ada.fit(X_train, y_train)

y_pred_ada = ada.predict(X_test)
y_proba_ada = ada.predict_proba(X_test)[:, 1]

print(f"Accuracy AdaBoost : {accuracy_score(y_test, y_pred_ada):.4f}")
print(f"AUC-ROC AdaBoost  : {roc_auc_score(y_test, y_proba_ada):.4f}")
```

> ⚠️ **Attention** : "AdaBoost est très sensible aux outliers et au bruit. Comme il augmente le poids des échantillons mal classés, un outlier aberrant aura un impact disproportionné sur le modèle."

### 3.2 Gradient Boosting

Le Gradient Boosting est une généralisation du Boosting qui utilise la **descente de gradient** pour optimiser n'importe quelle fonction de perte.

**Principe simplifié :**

1. Initialiser avec une prédiction constante (moyenne pour régression, log-odds pour classification)
2. Calculer les **résidus** (erreurs) du modèle actuel
3. Entraîner un nouvel arbre pour **prédire les résidus**
4. Ajouter ce nouvel arbre au modèle (pondéré par le learning rate)
5. Répéter N fois

Chaque arbre corrige un peu les erreurs des arbres précédents, comme un sculpteur qui affine progressivement son œuvre.

```python
from sklearn.ensemble import GradientBoostingClassifier

# Gradient Boosting
gb = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,     # taux d'apprentissage
    max_depth=3,           # arbres peu profonds (stumps améliorés)
    min_samples_split=5,
    min_samples_leaf=2,
    subsample=0.8,         # sous-échantillonnage stochastique
    random_state=42
)

gb.fit(X_train, y_train)

y_pred_gb = gb.predict(X_test)
y_proba_gb = gb.predict_proba(X_test)[:, 1]

print(f"Accuracy Gradient Boosting : {accuracy_score(y_test, y_pred_gb):.4f}")
print(f"AUC-ROC Gradient Boosting  : {roc_auc_score(y_test, y_proba_gb):.4f}")
```

#### Hyperparamètres clés du Gradient Boosting

| Hyperparamètre | Rôle | Valeur typique | Impact |
|---|---|---|---|
| `learning_rate` | Contribution de chaque arbre | 0.01 - 0.3 | Plus petit = plus robuste mais plus lent |
| `n_estimators` | Nombre d'arbres | 100 - 5000 | Plus = mieux (avec early stopping) |
| `max_depth` | Profondeur des arbres | 3 - 8 | Plus profond = plus complexe |
| `subsample` | Fraction des données par arbre | 0.7 - 0.9 | < 1.0 réduit l'overfitting |
| `min_samples_leaf` | Échantillons min par feuille | 1 - 50 | Plus grand = plus régularisé |

> ⚠️ **Attention** : "Learning rate et n_estimators sont intimement liés : un learning rate petit (0.01) nécessite beaucoup plus d'arbres (1000+) pour converger. La règle : small LR + many trees = meilleur résultat mais entraînement plus lent. Utilisez toujours l'early stopping pour trouver le bon nombre d'arbres."

> 💡 **Conseil** : "Pour le Gradient Boosting sklearn, commencez avec learning_rate=0.1, max_depth=3, n_estimators=200. Puis ajustez le learning_rate vers le bas et augmentez n_estimators proportionnellement."

---

## 4. 🏆 XGBoost – Le champion des compétitions

### 4.1 Pourquoi XGBoost domine

XGBoost (eXtreme Gradient Boosting) est une implémentation optimisée du Gradient Boosting créée par Tianqi Chen en 2014. Il domine les compétitions Kaggle depuis des années pour plusieurs raisons :

- **Régularisation intégrée** (L1 et L2) pour éviter l'overfitting
- **Gestion native des valeurs manquantes**
- **Parallélisation** au niveau des splits (pas des arbres)
- **Pruning intelligent** des arbres (contrairement au Gradient Boosting classique qui fait du pré-pruning)
- **Cache-aware access** pour des performances CPU optimales
- **Out-of-core computing** pour les datasets très volumineux

### 4.2 Installation et usage de base

```python
# Installation
# uv add xgboost

import xgboost as xgb
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Créer le modèle XGBoost
xgb_clf = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    min_child_weight=5,      # équivalent de min_samples_leaf
    subsample=0.8,           # sous-échantillonnage des lignes
    colsample_bytree=0.8,    # sous-échantillonnage des colonnes
    reg_alpha=0.1,           # régularisation L1
    reg_lambda=1.0,          # régularisation L2
    scale_pos_weight=1,      # pour classes déséquilibrées
    random_state=42,
    n_jobs=-1,
    eval_metric='logloss'    # métrique d'évaluation
)

# Entraîner avec early stopping
xgb_clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],  # données de validation
    verbose=50                     # afficher toutes les 50 itérations
)

# Prédictions
y_pred_xgb = xgb_clf.predict(X_test)
y_proba_xgb = xgb_clf.predict_proba(X_test)[:, 1]

print(f"Accuracy XGBoost : {accuracy_score(y_test, y_pred_xgb):.4f}")
print(f"AUC-ROC XGBoost  : {roc_auc_score(y_test, y_proba_xgb):.4f}")
print("\n", classification_report(y_test, y_pred_xgb))
```

### 4.3 Early Stopping – L'arme anti-overfitting

L'early stopping est une technique cruciale : on arrête l'entraînement quand la performance sur le set de validation ne s'améliore plus.

```python
# XGBoost avec early stopping
xgb_es = xgb.XGBClassifier(
    n_estimators=2000,          # mettre un nombre élevé
    learning_rate=0.01,         # learning rate petit
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1,
    early_stopping_rounds=50    # arrêter si pas d'amélioration pendant 50 rounds
)

xgb_es.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=100
)

# Voir combien d'arbres ont été utilisés
print(f"Meilleur nombre d'itérations : {xgb_es.best_iteration}")
print(f"Meilleur score : {xgb_es.best_score:.4f}")
```

> 💡 **Conseil de pro** : "Utilisez early_stopping_rounds=50 pour éviter l'overfitting automatiquement. Mettez n_estimators à une valeur très élevée (2000-5000) et laissez l'early stopping trouver le bon moment pour s'arrêter."

### 4.4 Hyperparamètres XGBoost clés

| Hyperparamètre | Description | Valeur recommandée | Impact |
|---|---|---|---|
| `learning_rate` (eta) | Taux d'apprentissage | 0.01 - 0.1 | Contrôle la vitesse de convergence |
| `n_estimators` | Nombre d'arbres | 500 - 5000 (avec early stop) | Plus = plus lent |
| `max_depth` | Profondeur max | 3 - 10 | Plus = plus complexe |
| `min_child_weight` | Poids min par feuille | 1 - 10 | Régularisation |
| `subsample` | % lignes par arbre | 0.6 - 0.9 | Réduction de variance |
| `colsample_bytree` | % features par arbre | 0.6 - 0.9 | Réduction de variance |
| `reg_alpha` | Régularisation L1 | 0 - 1 | Sparsité des features |
| `reg_lambda` | Régularisation L2 | 0 - 10 | Lissage des poids |
| `gamma` | Min loss reduction pour split | 0 - 5 | Contrôle la complexité |
| `scale_pos_weight` | Ratio classes | n_négatifs / n_positifs | Classes déséquilibrées |

> 💡 **Conseil** : "Pour un premier essai XGBoost, utilisez ces valeurs : learning_rate=0.1, max_depth=6, subsample=0.8, colsample_bytree=0.8. Puis activez l'early stopping et réduisez le learning_rate."

---

## 5. 📊 Comparaison des performances

### 5.1 Table comparative des méthodes d'ensemble

| Algorithme | Complexité d'entraînement | Interprétabilité | Performance typique | Vitesse d'inférence | Gestion des NaN |
|---|---|---|---|---|---|
| **Random Forest** | ⭐⭐ Moyenne | ⭐⭐⭐ Bonne | ⭐⭐⭐ Bonne | ⭐⭐⭐ Rapide | Non |
| **AdaBoost** | ⭐⭐ Moyenne | ⭐⭐ Moyenne | ⭐⭐ Correcte | ⭐⭐⭐ Rapide | Non |
| **Gradient Boosting** | ⭐⭐⭐ Élevée | ⭐⭐ Moyenne | ⭐⭐⭐⭐ Très bonne | ⭐⭐ Moyenne | Non |
| **XGBoost** | ⭐⭐⭐ Élevée | ⭐⭐ Moyenne | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐ Rapide | Oui |
| **LightGBM** | ⭐⭐ Moyenne | ⭐⭐ Moyenne | ⭐⭐⭐⭐⭐ Excellente | ⭐⭐⭐⭐ Très rapide | Oui |

### 5.2 Quand utiliser quoi ?

| Situation | Algorithme recommandé | Justification |
|---|---|---|
| Première exploration | Random Forest | Robuste, peu de tuning |
| Performance maximale | XGBoost / LightGBM | Meilleurs scores Kaggle |
| Besoin d'interprétabilité | Random Forest | Feature importances intuitives |
| Dataset très volumineux (>1M lignes) | LightGBM | Rapide, efficace en mémoire |
| Données bruitées | Random Forest | Résistant à l'overfitting |
| Données propres + features bien construites | XGBoost | Tire le meilleur parti des données |
| Séries temporelles | Gradient Boosting / XGBoost | Avec feature engineering temporel |
| Domaine réglementé (médical, finance) | Random Forest | Interprétabilité + robustesse |

> 💡 **Conseil** : "Si vous devez expliquer votre modèle à un métier ou un régulateur (médical, finance, assurance), préférez Random Forest. Si seule la performance compte (compétitions, ad ranking), foncez sur XGBoost ou LightGBM."

### 5.3 Benchmark comparatif

```python
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)
from sklearn.model_selection import cross_val_score
import xgboost as xgb
import time

# Définir les modèles à comparer
modeles = {
    'Random Forest': RandomForestClassifier(
        n_estimators=200, random_state=42, n_jobs=-1
    ),
    'AdaBoost': AdaBoostClassifier(
        n_estimators=200, learning_rate=0.1, random_state=42
    ),
    'Gradient Boosting': GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.1, max_depth=3, random_state=42
    ),
    'XGBoost': xgb.XGBClassifier(
        n_estimators=200, learning_rate=0.1, max_depth=6,
        random_state=42, n_jobs=-1, eval_metric='logloss'
    )
}

# Comparer avec cross-validation
resultats = {}
for nom, modele in modeles.items():
    debut = time.time()
    scores = cross_val_score(modele, X_train, y_train, cv=5, scoring='roc_auc')
    duree = time.time() - debut
    resultats[nom] = {
        'AUC moyenne': f"{scores.mean():.4f}",
        'Écart-type': f"{scores.std():.4f}",
        'Temps (s)': f"{duree:.1f}"
    }

# Afficher les résultats
resultats_df = pd.DataFrame(resultats).T
print(resultats_df)
```

---

## 6. 🔍 Feature Importance – Comprendre vos modèles

### 6.1 Impurity-based importance (Gini / Entropy)

C'est la méthode par défaut de Random Forest et Gradient Boosting. Elle mesure la diminution totale de l'impureté apportée par chaque feature à travers tous les arbres.

```python
# Feature importance par impureté (méthode par défaut)
importances_gini = rf.feature_importances_

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance_gini': importances_gini
}).sort_values('importance_gini', ascending=False)

print("Top 10 features (impureté) :")
print(importance_df.head(10))
```

> ⚠️ **Attention** : "L'importance par impureté est **biaisée** en faveur des features numériques à haute cardinalité et des features corrélées. Une feature aléatoire avec beaucoup de valeurs uniques peut apparaître comme « importante » alors qu'elle ne l'est pas."

### 6.2 Permutation Importance (plus fiable)

La permutation importance mesure la **chute de performance** quand on mélange aléatoirement les valeurs d'une feature. Si le score chute beaucoup, la feature est importante.

```python
from sklearn.inspection import permutation_importance

# Calculer la permutation importance sur le set de test
perm_importance = permutation_importance(
    rf, X_test, y_test,
    n_repeats=10,        # répéter 10 fois pour stabilité
    random_state=42,
    n_jobs=-1,
    scoring='roc_auc'    # métrique utilisée
)

# Créer un DataFrame
perm_df = pd.DataFrame({
    'feature': feature_names,
    'importance_mean': perm_importance.importances_mean,
    'importance_std': perm_importance.importances_std
}).sort_values('importance_mean', ascending=False)

print("Top 10 features (permutation) :")
print(perm_df.head(10))

# Visualisation avec barres d'erreur
plt.figure(figsize=(10, 6))
top_10 = perm_df.head(10)[::-1]  # inverser pour affichage horizontal
plt.barh(
    top_10['feature'],
    top_10['importance_mean'],
    xerr=top_10['importance_std'],
    color='steelblue'
)
plt.xlabel('Diminution moyenne du score AUC-ROC')
plt.title('Permutation Importance (Top 10)')
plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "Ne faites JAMAIS confiance aux feature importances par impureté seules. Utilisez TOUJOURS la permutation importance pour valider. Les deux méthodes devraient globalement s'accorder sur les features les plus importantes."

### 6.3 SHAP Values – L'état de l'art pour l'interprétabilité

SHAP (SHapley Additive exPlanations) est basé sur la théorie des jeux et fournit une explication **locale** pour chaque prédiction.

```python
# Installation : uv add shap
import shap

# Créer un explainer SHAP pour le modèle XGBoost
explainer = shap.TreeExplainer(xgb_clf)
shap_values = explainer.shap_values(X_test)

# Graphique global : importance des features
shap.summary_plot(shap_values, X_test, feature_names=feature_names)

# Graphique pour une prédiction individuelle
shap.force_plot(
    explainer.expected_value,
    shap_values[0],           # première observation
    X_test[0],
    feature_names=feature_names
)

# Dependence plot : relation feature <-> impact
shap.dependence_plot("feature_0", shap_values, X_test, feature_names=feature_names)
```

> 💡 **Conseil de pro** : "SHAP est LA référence pour l'interprétabilité. Il vous dit non seulement quelles features sont importantes, mais COMMENT elles influencent chaque prédiction. Indispensable pour les domaines réglementés."

### 6.4 Comparaison des méthodes d'importance

| Méthode | Fiabilité | Vitesse | Scope | Cas d'usage |
|---|---|---|---|---|
| Impurity-based | ⭐⭐ Moyenne | ⭐⭐⭐⭐ Très rapide | Global | Exploration rapide |
| Permutation | ⭐⭐⭐⭐ Bonne | ⭐⭐ Moyenne | Global | Validation, sélection |
| SHAP | ⭐⭐⭐⭐⭐ Excellente | ⭐ Lente | Global + Local | Production, réglementé |

---

## 7. 📈 Tuning avec GridSearchCV et RandomizedSearchCV

### 7.1 GridSearchCV – Recherche exhaustive

GridSearchCV teste **toutes les combinaisons** possibles des hyperparamètres spécifiés. Idéal pour un espace de recherche restreint.

```python
from sklearn.model_selection import GridSearchCV

# Définir la grille d'hyperparamètres
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

# Attention : 3 x 4 x 3 x 3 x 2 = 216 combinaisons x 5 folds = 1080 entraînements !
print(f"Nombre de combinaisons : {3*4*3*3*2}")

# GridSearchCV
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid=param_grid,
    cv=5,                    # 5-fold cross-validation
    scoring='roc_auc',       # métrique à optimiser
    n_jobs=-1,               # paralléliser
    verbose=1,               # afficher la progression
    return_train_score=True  # pour diagnostiquer l'overfitting
)

grid_search.fit(X_train, y_train)

# Résultats
print(f"\nMeilleurs hyperparamètres : {grid_search.best_params_}")
print(f"Meilleur score AUC-ROC (CV) : {grid_search.best_score_:.4f}")

# Score sur le test set avec le meilleur modèle
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)
y_proba_best = best_model.predict_proba(X_test)[:, 1]
print(f"Score AUC-ROC (test) : {roc_auc_score(y_test, y_proba_best):.4f}")

# Analyser les résultats
resultats_cv = pd.DataFrame(grid_search.cv_results_)
print("\nTop 5 combinaisons :")
print(resultats_cv.nlargest(5, 'mean_test_score')[
    ['params', 'mean_test_score', 'std_test_score', 'mean_train_score']
])
```

> ⚠️ **Attention** : "GridSearchCV est exhaustif et donc très lent. Avec 5 hyperparamètres à 4 valeurs chacun, vous avez 4^5 = 1024 combinaisons. Avec 5-fold CV, cela fait 5120 entraînements de modèle. Réfléchissez avant de lancer !"

### 7.2 RandomizedSearchCV – Recherche aléatoire

RandomizedSearchCV tire des combinaisons **au hasard** dans des distributions d'hyperparamètres. Beaucoup plus efficace pour de grands espaces de recherche.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# Définir des distributions (pas juste des listes)
param_distributions = {
    'n_estimators': randint(100, 1000),          # entier entre 100 et 1000
    'max_depth': randint(3, 30),                  # entier entre 3 et 30
    'min_samples_split': randint(2, 20),          # entier entre 2 et 20
    'min_samples_leaf': randint(1, 10),           # entier entre 1 et 10
    'max_features': uniform(0.1, 0.9),            # flottant entre 0.1 et 1.0
}

# RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=RandomForestClassifier(random_state=42, n_jobs=-1),
    param_distributions=param_distributions,
    n_iter=100,              # 100 combinaisons aléatoires (au lieu de milliers)
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1,
    random_state=42,
    return_train_score=True
)

random_search.fit(X_train, y_train)

print(f"Meilleurs hyperparamètres : {random_search.best_params_}")
print(f"Meilleur score AUC-ROC (CV) : {random_search.best_score_:.4f}")
```

> 💡 **Conseil** : "Commencez TOUJOURS par RandomizedSearchCV pour explorer largement l'espace des hyperparamètres, puis affinez avec GridSearchCV autour des meilleures valeurs trouvées. C'est la stratégie la plus efficace."

### 7.3 Stratégie optimale de tuning

```python
# Étape 1 : Exploration large avec RandomizedSearchCV
# (voir code ci-dessus)

# Étape 2 : Affinage ciblé avec GridSearchCV
# Basé sur les meilleurs paramètres trouvés : ex. max_depth=15, n_estimators=400
param_grid_fin = {
    'n_estimators': [350, 400, 450],        # autour de 400
    'max_depth': [12, 15, 18],              # autour de 15
    'min_samples_split': [3, 5, 7],         # autour de 5
    'min_samples_leaf': [1, 2, 3],          # autour de 2
}

grid_fin = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42, n_jobs=-1),
    param_grid=param_grid_fin,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1
)

grid_fin.fit(X_train, y_train)
print(f"Score final affiné : {grid_fin.best_score_:.4f}")
```

> 💡 **Conseil de pro** : "Le tuning des hyperparamètres donne généralement 2-5% d'amélioration. Le feature engineering en donne 10-30%. Ne passez pas des heures à tuner si vos features sont médiocres."

---

## 8. 🧠 Techniques avancées

### 8.1 Voting Classifier

Combiner plusieurs algorithmes différents pour un vote final :

```python
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression

# Combiner plusieurs modèles différents
voting = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=200, random_state=42)),
        ('gb', GradientBoostingClassifier(n_estimators=200, random_state=42)),
        ('lr', LogisticRegression(max_iter=1000, random_state=42))
    ],
    voting='soft',   # utiliser les probabilités (meilleur que 'hard')
    n_jobs=-1
)

voting.fit(X_train, y_train)
y_proba_voting = voting.predict_proba(X_test)[:, 1]
print(f"AUC-ROC Voting : {roc_auc_score(y_test, y_proba_voting):.4f}")
```

### 8.2 Stacking

Le stacking utilise un **méta-modèle** pour combiner les prédictions des modèles de base :

```python
from sklearn.ensemble import StackingClassifier

# Stacking : modèles de base + méta-modèle
stacking = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=200, random_state=42)),
        ('gb', GradientBoostingClassifier(n_estimators=200, random_state=42)),
        ('xgb', xgb.XGBClassifier(n_estimators=200, random_state=42, eval_metric='logloss'))
    ],
    final_estimator=LogisticRegression(max_iter=1000),  # méta-modèle
    cv=5,            # cross-validation pour les prédictions intermédiaires
    n_jobs=-1
)

stacking.fit(X_train, y_train)
y_proba_stack = stacking.predict_proba(X_test)[:, 1]
print(f"AUC-ROC Stacking : {roc_auc_score(y_test, y_proba_stack):.4f}")
```

> 💡 **Conseil** : "Le stacking est souvent la méthode la plus performante, mais aussi la plus complexe et la plus lente. Réservez-le pour les compétitions ou les cas où chaque 0.1% compte."

---

## 🎯 Points clés à retenir

1. **Les méthodes d'ensemble** combinent plusieurs modèles faibles pour créer un modèle fort
2. **Bagging** (Random Forest) réduit la variance → robuste, peu de tuning
3. **Boosting** (Gradient Boosting, XGBoost) réduit le biais → performances maximales
4. **Random Forest** est le meilleur premier choix : robuste, interprétable, rapide
5. **XGBoost** avec early stopping est l'arme ultime pour la performance
6. **Feature importance** : toujours vérifier avec la permutation importance, pas seulement Gini
7. **SHAP** est l'état de l'art pour l'interprétabilité
8. **RandomizedSearchCV** d'abord, puis **GridSearchCV** pour affiner
9. Le **tuning** donne 2-5%, le **feature engineering** donne 10-30%
10. **Voting** et **Stacking** pour aller encore plus loin

## ✅ Checklist de validation

- [ ] Je sais expliquer la différence entre Bagging et Boosting
- [ ] Je sais entraîner un Random Forest et interpréter ses feature importances
- [ ] Je comprends le principe du Gradient Boosting (résidus)
- [ ] Je sais utiliser XGBoost avec early stopping
- [ ] Je connais les hyperparamètres clés de chaque algorithme
- [ ] Je sais utiliser la permutation importance et SHAP
- [ ] Je maîtrise GridSearchCV et RandomizedSearchCV
- [ ] Je sais choisir entre Random Forest et XGBoost selon le contexte
- [ ] Je comprends le Voting et le Stacking

---

[⬅️ Chapitre 5 : SVM et KNN](05-svm-knn.md) | [➡️ Chapitre 7 : Clustering](07-clustering.md)
