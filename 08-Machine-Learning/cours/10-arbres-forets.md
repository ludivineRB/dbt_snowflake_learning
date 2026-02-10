# Chapitre 10 : Arbres de Décision et Forêts Aléatoires

## 🎯 Objectifs

- Comprendre intuitivement les arbres de décision comme un raisonnement humain
- Maîtriser l'algorithme CART (Gini, entropie, critères d'arrêt)
- Visualiser et comprendre l'overfitting des arbres profonds
- Connaître les techniques d'élagage (pruning)
- Comprendre le Random Forest comme une intelligence collective
- Savoir comparer les performances selon le nombre d'arbres
- Maîtriser les hyperparamètres clés du Random Forest

**Phase 3 — Semaine 10**

---

## 1. 🧠 Arbre de décision = Reproduire un raisonnement humain

### 1.1 L'intuition

Un arbre de décision fonctionne exactement comme un raisonnement humain : une série de **questions successives** qui mènent à une **décision finale**. Chaque question porte sur une feature et divise les données en sous-groupes de plus en plus homogènes.

### 1.2 Exemple quotidien : "Est-ce que je prends un parapluie ?"

```
                    ┌─────────────────────┐
                    │  Il pleut dehors ?   │
                    └──────────┬──────────┘
                          ╱         ╲
                    Oui ╱             ╲ Non
                      ╱                 ╲
           ┌──────────────┐    ┌──────────────────┐
           │ 🌂 PARAPLUIE │    │ Ciel couvert ?    │
           └──────────────┘    └────────┬─────────┘
                                   ╱         ╲
                             Oui ╱             ╲ Non
                               ╱                 ╲
                  ┌───────────────────┐   ┌───────────────────┐
                  │ Prévisions pluie? │   │ 🚫 PAS DE         │
                  └────────┬──────────┘   │    PARAPLUIE       │
                      ╱         ╲         └───────────────────┘
                Oui ╱             ╲ Non
                  ╱                 ╲
     ┌──────────────┐    ┌──────────────────┐
     │ 🌂 PARAPLUIE │    │ 🚫 PAS DE         │
     └──────────────┘    │    PARAPLUIE       │
                         └──────────────────┘
```

### 1.3 Application au Machine Learning

En ML, l'arbre de décision fait exactement pareil, mais avec des **données numériques** et des **seuils automatiques** :

```
Exemple : Prédire si un client va churner

                    ┌───────────────────────────┐
                    │ ancienneté < 6 mois ?      │
                    └─────────────┬─────────────┘
                            ╱           ╲
                      Oui ╱               ╲ Non
                        ╱                   ╲
          ┌──────────────────────┐  ┌───────────────────────┐
          │ nb_appels_support    │  │ montant_mensuel        │
          │ >= 3 ?               │  │ > 80€ ?                │
          └──────────┬───────────┘  └──────────┬────────────┘
                ╱         ╲               ╱         ╲
          Oui ╱             ╲ Non   Oui ╱             ╲ Non
            ╱                 ╲       ╱                 ╲
    ┌──────────┐    ┌──────────┐ ┌──────────┐    ┌──────────┐
    │ CHURN    │    │ PAS      │ │ CHURN    │    │ PAS      │
    │ (85%)    │    │ CHURN    │ │ (60%)    │    │ CHURN    │
    └──────────┘    │ (70%)    │ └──────────┘    │ (90%)    │
                    └──────────┘                  └──────────┘
```

> 💡 **Conseil** : "L'arbre de décision est l'un des rares modèles de ML que vous pouvez montrer directement à un non-technique. 'Si ancienneté < 6 mois ET appels_support >= 3, alors le client va churner' — c'est limpide."

---

## 2. 📊 Construction d'un arbre (algorithme CART simplifié)

### 2.1 Questions successives (splits)

L'algorithme CART (Classification And Regression Trees) construit l'arbre en posant des questions de la forme :

```
"feature X est-elle < seuil S ?"

Exemples de splits possibles :
- "surface < 50 m² ?"
- "âge < 35 ans ?"
- "revenu < 30000€ ?"
- "contrat_mensuel == 1 ?"
```

Pour **chaque feature** et **chaque valeur possible**, l'algorithme teste le split et choisit celui qui sépare le mieux les classes.

### 2.2 Comment choisir la meilleure question ?

```
L'algorithme évalue TOUS les splits possibles et garde le meilleur :

Données initiales : [🔴🔴🔴🔵🔵🔵🔵🔵]  (3 rouges, 5 bleus)

Split 1 : "âge < 25 ?"
  Gauche : [🔴🔴🔵🔵]     → mélangé (impur)
  Droite : [🔴🔵🔵🔵]     → mélangé (impur)
  → Split médiocre

Split 2 : "revenu < 30k ?"
  Gauche : [🔴🔴🔴🔵]     → presque pur
  Droite : [🔵🔵🔵🔵]     → pur !
  → Bon split ! ✅

L'algorithme choisit le split qui maximise la "pureté" des sous-groupes.
```

### 2.3 Indice de Gini

L'indice de Gini mesure l'**impureté** d'un noeud. Un Gini de 0 signifie que le noeud est pur (une seule classe).

**Formule** : `Gini = 1 - Σ(pi²)` où pi est la proportion de chaque classe

#### Calcul pas à pas

```
Exemple : un noeud contient 40 clients churn et 60 clients non-churn

  p(churn)     = 40/100 = 0.40
  p(non-churn) = 60/100 = 0.60

  Gini = 1 - (0.40² + 0.60²)
       = 1 - (0.16 + 0.36)
       = 1 - 0.52
       = 0.48    → assez impur (mélangé)

Noeud pur (100% churn) :
  Gini = 1 - (1.0²) = 0.0    → parfaitement pur ✅

Noeud maximalement impur (50/50) :
  Gini = 1 - (0.5² + 0.5²) = 0.5   → mélange maximal ❌
```

#### Visualisation de l'indice de Gini

```
  Gini
  0.50 |         ●
       |       ●   ●
  0.40 |     ●       ●
       |   ●           ●
  0.30 | ●               ●
       |●                 ●
  0.20 |                    ●
       |●                     ●
  0.10 | ●                      ●
       |  ●                       ●
  0.00 |●───────────────────────────●
       +──────────────────────────────→ p(classe 1)
       0    0.2   0.4   0.5   0.8   1.0

  Maximum à p=0.5 (50/50) → plus grande incertitude
  Minimum à p=0 ou p=1   → certitude totale
```

```python
import numpy as np
import matplotlib.pyplot as plt

# Visualiser l'indice de Gini
p = np.linspace(0, 1, 100)
gini = 1 - p**2 - (1 - p)**2

plt.figure(figsize=(8, 5))
plt.plot(p, gini, 'b-', linewidth=2, label='Gini = 1 - p² - (1-p)²')
plt.xlabel('p (proportion de la classe 1)', fontsize=12)
plt.ylabel('Indice de Gini', fontsize=12)
plt.title('Indice de Gini en fonction de la proportion', fontsize=14)
plt.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Maximum (p=0.5)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 2.4 Entropie (comparaison avec Gini)

L'**entropie** est une autre mesure d'impureté, issue de la théorie de l'information :

**Formule** : `Entropie = -Σ(pi * log2(pi))`

| Critère | Gini | Entropie |
|---------|------|----------|
| **Formule** | 1 - Σ(pi²) | -Σ(pi * log2(pi)) |
| **Plage** | [0, 0.5] (binaire) | [0, 1] (binaire) |
| **Interprétation** | Probabilité de mauvaise classification | Quantité d'information / désordre |
| **Vitesse** | Plus rapide (pas de logarithme) | Plus lent |
| **Performances** | Très similaires à l'entropie | Très similaires au Gini |
| **Par défaut sklearn** | Oui (`criterion='gini'`) | Non (`criterion='entropy'`) |

> 💡 **Conseil** : "En pratique, Gini et Entropie donnent des résultats quasiment identiques dans 95% des cas. Restez avec Gini (le défaut de sklearn) sauf raison spécifique."

### 2.5 Critères d'arrêt

L'arbre pourrait continuer à se diviser jusqu'à ce que chaque feuille contienne un seul échantillon. Les critères d'arrêt empêchent cela :

| Critère | Paramètre sklearn | Description | Valeur typique |
|---------|-------------------|-------------|----------------|
| **Profondeur maximale** | `max_depth` | Limite le nombre de niveaux | 3-20 |
| **Échantillons min pour split** | `min_samples_split` | Nombre min pour diviser un noeud | 2-20 |
| **Échantillons min par feuille** | `min_samples_leaf` | Nombre min dans une feuille | 1-10 |
| **Nombre max de feuilles** | `max_leaf_nodes` | Limite le nombre total de feuilles | None ou 10-100 |
| **Réduction min d'impureté** | `min_impurity_decrease` | Split seulement si gain suffisant | 0.0 |

```python
from sklearn.tree import DecisionTreeClassifier

# Arbre avec critères d'arrêt
arbre = DecisionTreeClassifier(
    max_depth=5,               # maximum 5 niveaux
    min_samples_split=10,      # au moins 10 échantillons pour diviser
    min_samples_leaf=5,        # au moins 5 échantillons par feuille
    criterion='gini',          # critère de pureté
    random_state=42
)
```

---

## 3. 🔍 Overfitting illustré visuellement

### 3.1 Arbre profond = apprendre par cœur

Un arbre sans limite de profondeur va créer des feuilles pour **chaque observation** du dataset d'entraînement. Il apprend par cœur les données, y compris le bruit.

```
Arbre profond (depth=20) :                Arbre élagué (depth=3) :

Données d'entraînement :                  Données d'entraînement :
  Score train = 100% 🎯                     Score train = 88% 📊
  Score test  = 72%  😰                     Score test  = 85% 😊

         ┌─┐                                     ┌────────┐
       ╱     ╲                                  ╱          ╲
     ┌─┐     ┌─┐                           ┌────┐      ┌────┐
    ╱   ╲   ╱   ╲                         ╱      ╲    ╱      ╲
  ┌─┐ ┌─┐ ┌─┐ ┌─┐                      ┌──┐  ┌──┐ ┌──┐  ┌──┐
  ... ... ... ...                       │A │  │B │ │B │  │A │
  (des centaines de feuilles)           └──┘  └──┘ └──┘  └──┘
  → Mémorise chaque exemple              → Généralise les patterns
  → Mauvais sur de nouvelles données      → Bon sur de nouvelles données
```

### 3.2 Comparaison depth=3 vs depth=20

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np

# Générer des données
X, y = make_classification(
    n_samples=500, n_features=10, n_informative=5,
    n_redundant=3, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Arbre profond (overfitting)
arbre_profond = DecisionTreeClassifier(max_depth=20, random_state=42)
arbre_profond.fit(X_train, y_train)

# Arbre élagué (bon)
arbre_elague = DecisionTreeClassifier(max_depth=3, random_state=42)
arbre_elague.fit(X_train, y_train)

# Comparer les scores
print("=== Comparaison depth=3 vs depth=20 ===\n")
print(f"{'':>20} {'Train':>10} {'Test':>10} {'Écart':>10}")
print(f"{'─'*50}")

score_train_profond = arbre_profond.score(X_train, y_train)
score_test_profond = arbre_profond.score(X_test, y_test)
print(f"{'Arbre profond (20)':>20} {score_train_profond:>10.4f} "
      f"{score_test_profond:>10.4f} {score_train_profond - score_test_profond:>10.4f}")

score_train_elague = arbre_elague.score(X_train, y_train)
score_test_elague = arbre_elague.score(X_test, y_test)
print(f"{'Arbre élagué (3)':>20} {score_train_elague:>10.4f} "
      f"{score_test_elague:>10.4f} {score_train_elague - score_test_elague:>10.4f}")

# Visualiser la courbe de profondeur vs score
depths = range(1, 25)
train_scores = []
test_scores = []

for d in depths:
    arbre = DecisionTreeClassifier(max_depth=d, random_state=42)
    arbre.fit(X_train, y_train)
    train_scores.append(arbre.score(X_train, y_train))
    test_scores.append(arbre.score(X_test, y_test))

plt.figure(figsize=(10, 6))
plt.plot(depths, train_scores, 'b-o', label='Score entraînement', linewidth=2)
plt.plot(depths, test_scores, 'r-o', label='Score test', linewidth=2)
plt.axvline(x=depths[np.argmax(test_scores)], color='green', linestyle='--',
            label=f'Profondeur optimale = {depths[np.argmax(test_scores)]}')
plt.xlabel('Profondeur de l\'arbre (max_depth)', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.title('Overfitting : Train vs Test selon la profondeur', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.show()
```

### 3.3 Élagage : pré-pruning vs post-pruning

| Technique | Description | Comment | Avantages |
|-----------|-------------|---------|-----------|
| **Pré-pruning** | Limiter la croissance PENDANT la construction | max_depth, min_samples_split, min_samples_leaf | Rapide, simple |
| **Post-pruning** | Construire l'arbre complet, puis COUPER les branches inutiles | `ccp_alpha` (cost-complexity pruning) | Explore plus de splits |

```python
# Pré-pruning : limiter dès la construction
arbre_pre = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
arbre_pre.fit(X_train, y_train)
print(f"Pré-pruning : accuracy test = {arbre_pre.score(X_test, y_test):.4f}")

# Post-pruning avec ccp_alpha (Cost Complexity Pruning)
# Étape 1 : trouver le meilleur alpha
path = DecisionTreeClassifier(random_state=42).cost_complexity_pruning_path(
    X_train, y_train
)
ccp_alphas = path.ccp_alphas

# Étape 2 : tester chaque alpha
train_scores_ccp = []
test_scores_ccp = []

for alpha in ccp_alphas:
    arbre = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42)
    arbre.fit(X_train, y_train)
    train_scores_ccp.append(arbre.score(X_train, y_train))
    test_scores_ccp.append(arbre.score(X_test, y_test))

# Visualiser
plt.figure(figsize=(10, 6))
plt.plot(ccp_alphas, train_scores_ccp, 'b-', label='Train', linewidth=2)
plt.plot(ccp_alphas, test_scores_ccp, 'r-', label='Test', linewidth=2)
plt.xlabel('Alpha (complexité du pruning)', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.title('Post-pruning : Accuracy vs alpha', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.show()

best_alpha = ccp_alphas[np.argmax(test_scores_ccp)]
print(f"Meilleur alpha : {best_alpha:.6f}")
print(f"Post-pruning : accuracy test = {max(test_scores_ccp):.4f}")
```

> 💡 **Conseil** : "En pratique, le pré-pruning (max_depth, min_samples) suffit dans la majorité des cas. Le post-pruning (ccp_alpha) est utile quand vous voulez une optimisation plus fine."

---

## 4. 📋 Avantages et inconvénients des arbres de décision

| Avantages | Inconvénients |
|-----------|---------------|
| Très interprétable (visualisable) | Forte tendance à l'overfitting |
| Pas besoin de normalisation/scaling | Instable (petite variation des données → arbre très différent) |
| Gère les features numériques ET catégorielles | Frontières de décision uniquement parallèles aux axes |
| Feature importance native | Performance inférieure aux ensembles (RF, XGBoost) |
| Rapide à entraîner et prédire | Sensible au déséquilibre des classes |
| Gère les relations non-linéaires | Bias vers les features à haute cardinalité |
| Pas de besoin de données standardisées | Un seul arbre est rarement suffisant en pratique |
| Gère les valeurs manquantes (certaines implémentations) | Crée des frontières en escalier |

### Pas besoin de normalisation !

```
Pourquoi les arbres n'ont pas besoin de scaling ?

Les arbres posent des questions du type "feature < seuil ?"
→ Seul l'ORDRE des valeurs compte, pas leur échelle

Exemple :
  "surface < 50 m²" et "surface < 50000 cm²" donnent le MÊME split
  Le résultat est identique que les données soient en m², cm² ou pieds²

C'est un avantage MAJEUR par rapport à KNN et régression logistique
qui dépendent des distances/amplitudes.
```

### Feature importance native

```python
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import matplotlib.pyplot as plt

# Entraîner un arbre
arbre = DecisionTreeClassifier(max_depth=5, random_state=42)
arbre.fit(X_train, y_train)

# Feature importance (basée sur la réduction de Gini)
feature_names = [f'feature_{i}' for i in range(X_train.shape[1])]
importances = pd.DataFrame({
    'Feature': feature_names,
    'Importance': arbre.feature_importances_
}).sort_values('Importance', ascending=False)

print("=== Feature Importance (Arbre de Décision) ===")
print(importances)

# Visualiser
plt.figure(figsize=(10, 5))
plt.barh(importances['Feature'][::-1], importances['Importance'][::-1])
plt.xlabel('Importance (réduction de Gini)')
plt.title('Importance des features — Arbre de Décision')
plt.tight_layout()
plt.show()
```

### Visualiser un arbre

```python
from sklearn.tree import export_text, plot_tree

# Affichage texte
print(export_text(arbre, feature_names=feature_names, max_depth=3))

# Affichage graphique
plt.figure(figsize=(20, 10))
plot_tree(
    arbre,
    feature_names=feature_names,
    class_names=['Non-Churn', 'Churn'],
    filled=True,          # colorer selon la classe majoritaire
    rounded=True,
    max_depth=3,          # limiter l'affichage à 3 niveaux
    fontsize=10
)
plt.title('Arbre de Décision (3 premiers niveaux)', fontsize=16)
plt.tight_layout()
plt.show()
```

---

## 5. 🌲 Random Forest = Intelligence collective

### 5.1 La métaphore du jury

```
Un seul juge (1 arbre de décision) :
  → Peut avoir des préjugés (biais)
  → Peut se tromper sur des cas complexes
  → Son jugement est instable

Un jury de 100 juges (Random Forest) :
  → Chaque juge a un parcours différent (données bootstrap)
  → Chaque juge voit des aspects différents (features aléatoires)
  → Le verdict final = vote majoritaire
  → Les erreurs individuelles se compensent
  → Jugement final plus juste et plus stable ✅
```

### 5.2 Bagging expliqué pas à pas

```
Dataset original : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

Étape 1 : Créer N échantillons bootstrap (tirage avec remise)
──────────────────────────────────────────────────────────────
  Échantillon 1 : [2, 5, 5, 8, 1, 9, 3, 7, 2, 6]  ← certains doublés, certains absents
  Échantillon 2 : [1, 1, 4, 6, 8, 3, 10, 7, 9, 4]
  Échantillon 3 : [3, 7, 2, 10, 5, 5, 8, 1, 6, 9]
  ...
  Échantillon N : [...]

Étape 2 : Entraîner un arbre sur chaque échantillon
──────────────────────────────────────────────────────
  Arbre 1 ← Échantillon 1  (+ features aléatoires à chaque split)
  Arbre 2 ← Échantillon 2  (+ features aléatoires à chaque split)
  Arbre 3 ← Échantillon 3  (+ features aléatoires à chaque split)
  ...

Étape 3 : Agréger les prédictions
──────────────────────────────────
  Nouveau client X :
    Arbre 1 prédit : CHURN
    Arbre 2 prédit : PAS CHURN
    Arbre 3 prédit : CHURN
    ...
    Arbre 100 prédit : CHURN

    Vote : 67 CHURN vs 33 PAS CHURN
    → Prédiction finale : CHURN (67% de confiance)
```

### 5.3 Bootstrap sampling (tirage avec remise)

```python
import numpy as np

# Illustration du bootstrap
np.random.seed(42)
donnees = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

print("Dataset original :", donnees)
print()

for i in range(3):
    bootstrap = np.random.choice(donnees, size=len(donnees), replace=True)
    absents = set(donnees) - set(bootstrap)
    pct_unique = len(set(bootstrap)) / len(donnees) * 100
    print(f"Bootstrap {i+1} : {bootstrap}")
    print(f"  Absents : {absents} ({100-pct_unique:.0f}% des données)")
    print(f"  Uniques : {pct_unique:.0f}%")
    print()

# En théorie, ~63.2% des données sont présentes dans chaque bootstrap
# Les ~36.8% restantes sont les données OOB (Out-Of-Bag)
print("Théorie : ~63.2% des données dans chaque bootstrap")
print("→ les ~36.8% restantes servent de validation gratuite (OOB)")
```

### 5.4 Agrégation des votes

| Type de problème | Méthode d'agrégation | Description |
|-----------------|---------------------|-------------|
| **Classification** | Vote majoritaire | La classe la plus votée gagne |
| **Classification (proba)** | Moyenne des probabilités | Moyenne des predict_proba de chaque arbre |
| **Régression** | Moyenne | Moyenne des prédictions de chaque arbre |

### 5.5 Out-of-bag score (OOB)

Le score OOB est une **estimation gratuite** de la performance du modèle, sans avoir besoin d'un set de validation séparé :

```
Pour chaque arbre, ~36.8% des données n'ont PAS été utilisées (OOB).
On peut les utiliser pour évaluer cet arbre.
En agrégeant sur tous les arbres, on obtient le score OOB.

Avantages :
  ✅ Pas besoin de set de validation séparé
  ✅ Estimation non biaisée de la performance
  ✅ Gratuit (calculé pendant l'entraînement)
```

```python
from sklearn.ensemble import RandomForestClassifier

# Activer le score OOB
rf_oob = RandomForestClassifier(
    n_estimators=200,
    oob_score=True,        # activer le score OOB
    random_state=42,
    n_jobs=-1
)
rf_oob.fit(X_train, y_train)

print(f"Score OOB      : {rf_oob.oob_score_:.4f}")
print(f"Score test     : {rf_oob.score(X_test, y_test):.4f}")
print(f"→ OOB ≈ test score (validation gratuite !)")
```

### 5.6 Implémentation sklearn complète

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import pandas as pd

# Créer et entraîner le Random Forest
rf = RandomForestClassifier(
    n_estimators=200,         # 200 arbres
    max_depth=15,             # profondeur max de chaque arbre
    min_samples_split=5,      # au moins 5 échantillons pour splitter
    min_samples_leaf=2,       # au moins 2 par feuille
    max_features='sqrt',      # racine carrée du nombre de features par split
    oob_score=True,           # score Out-Of-Bag
    class_weight='balanced',  # gestion des classes déséquilibrées
    random_state=42,
    n_jobs=-1                 # tous les coeurs
)

rf.fit(X_train, y_train)

# Évaluation
y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

print("=== Random Forest — Résultats ===\n")
print(classification_report(y_test, y_pred))
print(f"AUC-ROC   : {roc_auc_score(y_test, y_proba):.4f}")
print(f"Score OOB : {rf.oob_score_:.4f}")
```

### 5.7 Feature importance avec Random Forest

```python
import pandas as pd
import matplotlib.pyplot as plt

# Importance par impureté (Gini) — attention aux biais !
importances = pd.DataFrame({
    'Feature': feature_names,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

print("=== Feature Importance (Gini) ===")
print(importances.head(10))

# Visualiser
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Gini importance
top_n = importances.head(10)[::-1]
axes[0].barh(top_n['Feature'], top_n['Importance'], color='steelblue')
axes[0].set_xlabel('Importance (Gini)')
axes[0].set_title('Feature Importance — Impureté (Gini)')

# Permutation importance (plus fiable)
from sklearn.inspection import permutation_importance

perm_imp = permutation_importance(rf, X_test, y_test,
                                   n_repeats=10, random_state=42,
                                   n_jobs=-1)
perm_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': perm_imp.importances_mean
}).sort_values('Importance', ascending=False)

top_perm = perm_df.head(10)[::-1]
axes[1].barh(top_perm['Feature'], top_perm['Importance'], color='coral')
axes[1].set_xlabel('Diminution du score')
axes[1].set_title('Feature Importance — Permutation')

plt.suptitle('Comparaison des méthodes d\'importance', fontsize=14)
plt.tight_layout()
plt.show()
```

> ⚠️ **Attention** : "L'importance par Gini surestime les features à haute cardinalité. Préférez **toujours** la permutation importance pour des résultats fiables."

---

## 6. 🧪 TP : Comparer 1 arbre vs 10 vs 100 vs 500 arbres

### 6.1 Code complet

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import time

# Générer un dataset
X, y = make_classification(
    n_samples=2000, n_features=20, n_informative=10,
    n_redundant=5, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Tester différents nombres d'arbres
n_arbres_list = [1, 5, 10, 25, 50, 100, 200, 500]
resultats = []

for n_arbres in n_arbres_list:
    start = time.time()

    if n_arbres == 1:
        # Un seul arbre de décision
        modele = DecisionTreeClassifier(random_state=42)
    else:
        modele = RandomForestClassifier(
            n_estimators=n_arbres,
            random_state=42,
            n_jobs=-1
        )

    # Cross-validation
    scores = cross_val_score(modele, X_train, y_train, cv=5, scoring='accuracy')

    # Score test
    modele.fit(X_train, y_train)
    score_test = modele.score(X_test, y_test)

    duree = time.time() - start

    resultats.append({
        'n_arbres': n_arbres,
        'cv_mean': scores.mean(),
        'cv_std': scores.std(),
        'test_score': score_test,
        'temps': duree
    })

    print(f"n_arbres={n_arbres:>3} : "
          f"CV={scores.mean():.4f}±{scores.std():.4f}, "
          f"Test={score_test:.4f}, "
          f"Temps={duree:.2f}s")

# Visualiser
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Score vs nombre d'arbres
n_arbres = [r['n_arbres'] for r in resultats]
cv_means = [r['cv_mean'] for r in resultats]
cv_stds = [r['cv_std'] for r in resultats]
test_scores = [r['test_score'] for r in resultats]

axes[0].errorbar(n_arbres, cv_means, yerr=cv_stds, fmt='bo-',
                 linewidth=2, capsize=5, label='CV Score (±std)')
axes[0].plot(n_arbres, test_scores, 'rs-', linewidth=2, label='Test Score')
axes[0].set_xlabel('Nombre d\'arbres', fontsize=12)
axes[0].set_ylabel('Accuracy', fontsize=12)
axes[0].set_title('Performance vs Nombre d\'arbres', fontsize=14)
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)
axes[0].set_xscale('log')

# Temps vs nombre d'arbres
temps = [r['temps'] for r in resultats]
axes[1].plot(n_arbres, temps, 'go-', linewidth=2)
axes[1].set_xlabel('Nombre d\'arbres', fontsize=12)
axes[1].set_ylabel('Temps (secondes)', fontsize=12)
axes[1].set_title('Temps d\'entraînement vs Nombre d\'arbres', fontsize=14)
axes[1].grid(True, alpha=0.3)
axes[1].set_xscale('log')

plt.suptitle('Impact du nombre d\'arbres sur Random Forest', fontsize=16)
plt.tight_layout()
plt.show()
```

### 6.2 Observations typiques

```
Résultats typiques :

  n_arbres=  1 : CV=0.8420±0.0215, Test=0.8350   ← arbre seul, instable
  n_arbres=  5 : CV=0.8780±0.0180, Test=0.8750   ← déjà une amélioration nette
  n_arbres= 10 : CV=0.8920±0.0120, Test=0.8900   ← gain significatif
  n_arbres= 25 : CV=0.9040±0.0090, Test=0.9050   ← encore mieux
  n_arbres= 50 : CV=0.9100±0.0075, Test=0.9100   ← le gain ralentit
  n_arbres=100 : CV=0.9120±0.0060, Test=0.9150   ← gain marginal
  n_arbres=200 : CV=0.9130±0.0055, Test=0.9150   ← quasi-plateau
  n_arbres=500 : CV=0.9135±0.0050, Test=0.9175   ← gain négligeable

Conclusions :
  ✅ Passer de 1 à 50 arbres : gain majeur
  ⚠️ Passer de 50 à 500 : gain marginal, temps ×10
  → 100-200 arbres est souvent le sweet spot
```

> 💡 **Conseil** : "En production, choisissez le nombre d'arbres au-delà duquel le gain de performance est négligeable. 100-200 arbres suffisent dans 90% des cas. Au-delà de 500, le temps de calcul augmente mais le score stagne."

---

## 7. 🔧 Hyperparamètres importants de Random Forest

### 7.1 Les paramètres clés

| Hyperparamètre | Description | Valeur par défaut | Plage recommandée | Impact principal |
|----------------|-------------|-------------------|-------------------|-----------------|
| `n_estimators` | Nombre d'arbres | 100 | 100-500 | Plus = mieux (mais plus lent) |
| `max_depth` | Profondeur max | None (illimitée) | 5-30 ou None | Contrôle la complexité |
| `max_features` | Features par split | 'sqrt' | 'sqrt', 'log2', 0.3-0.8 | Diversité des arbres |
| `min_samples_split` | Min échantillons pour split | 2 | 2-20 | Régularisation |
| `min_samples_leaf` | Min échantillons par feuille | 1 | 1-10 | Régularisation |
| `class_weight` | Poids des classes | None | 'balanced', dict | Classes déséquilibrées |
| `oob_score` | Score Out-Of-Bag | False | True | Validation gratuite |
| `n_jobs` | Parallélisation | 1 | -1 | Vitesse |

### 7.2 Guide de tuning pas à pas

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# Étape 1 : Exploration large avec RandomizedSearchCV
param_distributions = {
    'n_estimators': randint(50, 500),
    'max_depth': [None, 5, 10, 15, 20, 25, 30],
    'max_features': ['sqrt', 'log2', 0.3, 0.5, 0.7],
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
}

random_search = RandomizedSearchCV(
    estimator=RandomForestClassifier(random_state=42, n_jobs=-1),
    param_distributions=param_distributions,
    n_iter=50,        # 50 combinaisons aléatoires
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

random_search.fit(X_train, y_train)

print(f"Meilleurs hyperparamètres : {random_search.best_params_}")
print(f"Meilleur score AUC-ROC (CV) : {random_search.best_score_:.4f}")

# Score final
best_rf = random_search.best_estimator_
score_final = best_rf.score(X_test, y_test)
print(f"Score test (accuracy) : {score_final:.4f}")
```

### 7.3 Règles empiriques

```
Guide rapide de tuning Random Forest :

1. n_estimators :
   → Commencer à 100, augmenter à 200-300
   → Au-delà de 500, le gain est négligeable
   → Vérifier avec le score OOB

2. max_depth :
   → None (illimité) est souvent OK pour Random Forest
   → Réduire (10-20) si overfitting détecté
   → Plus profond = plus de variance

3. max_features :
   → 'sqrt' pour la classification (défaut, bon choix)
   → 0.33 ou 'log2' sont aussi de bonnes options
   → Plus bas = arbres plus décorrélés = meilleur bagging

4. min_samples_split / min_samples_leaf :
   → Augmenter si overfitting (5-20)
   → Réduire si underfitting (2-5)
   → min_samples_leaf=1 est souvent OK pour RF

5. class_weight :
   → 'balanced' si classes déséquilibrées
   → Sinon, laisser None
```

> 💡 **Conseil** : "Random Forest est un modèle qui fonctionne bien 'out of the box'. Les valeurs par défaut de sklearn sont souvent proches de l'optimal. Commencez sans tuning, puis affinez seulement si nécessaire."

> ⚠️ **Attention** : "Le tuning des hyperparamètres donne généralement 2-5% d'amélioration. Le feature engineering en donne 10-30%. Investissez votre temps dans les features avant le tuning !"

---

## 🎯 Points clés à retenir

1. **Un arbre de décision** reproduit un raisonnement humain sous forme de questions successives — c'est le modèle le plus interprétable
2. **L'algorithme CART** choisit le meilleur split à chaque noeud en maximisant la pureté (Gini ou Entropie)
3. **L'indice de Gini** mesure l'impureté : 0 = pur, 0.5 = mélange maximal (binaire)
4. **Un arbre profond apprend par coeur** (overfitting) — utilisez les critères d'arrêt (max_depth, min_samples)
5. **Les arbres n'ont pas besoin de scaling** — seul l'ordre des valeurs compte pour les splits
6. **Random Forest = intelligence collective** : N arbres entraînés sur des données bootstrap avec des features aléatoires
7. **Le score OOB** est une validation gratuite — pas besoin de set de validation séparé
8. **100-200 arbres** suffisent dans 90% des cas — au-delà, le gain est marginal
9. **La feature importance par Gini est biaisée** — préférez la permutation importance
10. **Random Forest est le couteau suisse du ML** : peu de tuning, robuste, rapide, interprétable

---

## ✅ Checklist de validation

- [ ] Je sais expliquer un arbre de décision à un non-technique
- [ ] Je comprends l'algorithme CART (splits, Gini, entropie)
- [ ] Je sais calculer l'indice de Gini à la main
- [ ] Je sais visualiser un arbre de décision avec sklearn
- [ ] Je comprends pourquoi un arbre profond fait de l'overfitting
- [ ] Je connais la différence entre pré-pruning et post-pruning
- [ ] Je sais pourquoi les arbres n'ont pas besoin de normalisation
- [ ] Je comprends le principe de Random Forest (bagging + features aléatoires)
- [ ] Je sais expliquer le bootstrap sampling et le score OOB
- [ ] Je sais choisir le bon nombre d'arbres (impact sur performance et temps)
- [ ] Je maîtrise les hyperparamètres clés de Random Forest
- [ ] Je sais utiliser la permutation importance plutôt que l'importance Gini

---

**Précédent** : [Chapitre 9 : Modèles Linéaires et Logiques](09-modeles-lineaires.md)

**Suivant** : [Chapitre 11 : Boosting — Les Champions de Kaggle](11-boosting.md)
