# Chapitre 5 : Classification – Prédire des Catégories

## 🎯 Objectifs

- Maîtriser les algorithmes de classification fondamentaux (Logistique, KNN, SVM, Arbres)
- Comprendre en profondeur **toutes** les métriques de classification
- Savoir interpréter une matrice de confusion et une courbe ROC
- Choisir la bonne métrique selon le contexte métier
- Ajuster le seuil de décision pour optimiser les performances
- Savoir choisir le bon algorithme pour le bon problème

---

## 1. 📊 Régression Logistique

### 1.1 Concept

Malgré son nom, la régression logistique est un **classifieur** (pas un modèle de régression). Elle prédit la **probabilité** qu'un échantillon appartienne à une classe.

**Fonction sigmoïde** : transforme n'importe quel nombre en probabilité [0, 1]

```
σ(z) = 1 / (1 + e^(-z))

Où z = b₀ + b₁*x₁ + b₂*x₂ + ... + bₙ*xₙ (comme une régression linéaire)

Si σ(z) ≥ 0.5 → Classe 1 (positif)
Si σ(z) < 0.5 → Classe 0 (négatif)
```

```
  Probabilité
  1.0 │                    ___________
      │                ╱
      │              ╱
  0.5 │- - - - - -╱- - - - - - - - - -  ← Seuil de décision
      │         ╱
      │       ╱
  0.0 │______╱
      └────────────────────────── z
       Classe 0    │    Classe 1
```

### 1.2 Implémentation

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report, confusion_matrix

# --- Charger les données ---
cancer = load_breast_cancer()
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
y = cancer.target  # 0 = malin, 1 = bénin

# --- Préparer ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Entraîner ---
log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train_scaled, y_train)

# --- Prédire ---
y_pred = log_reg.predict(X_test_scaled)           # Classe prédite (0 ou 1)
y_proba = log_reg.predict_proba(X_test_scaled)     # Probabilités [P(0), P(1)]

print("=== Exemples de prédictions ===")
for i in range(5):
    print(f"  Réel: {y_test.iloc[i] if hasattr(y_test, 'iloc') else y_test[i]}, "
          f"Prédit: {y_pred[i]}, "
          f"Proba(bénin): {y_proba[i][1]:.3f}")

# --- Évaluer ---
print("\n=== Rapport de classification ===")
print(classification_report(y_test, y_pred, target_names=cancer.target_names))
```

> 💡 **Conseil** : "**Toujours** commencer par la régression logistique comme baseline pour un problème de classification. Elle est rapide, interprétable et souvent plus performante qu'on ne le croit."

> 💡 **Conseil de pro** : "Utilisez `predict_proba()` plutôt que `predict()` quand c'est possible. Les probabilités donnent plus d'information que la classe seule et permettent d'ajuster le seuil de décision."

---

## 2. 🎯 K-Nearest Neighbors (KNN)

### 2.1 Concept

KNN est l'algorithme le plus intuitif : pour classifier un point, on regarde les **K voisins les plus proches** et on vote.

```
Nouveau point (?) → On regarde les K=5 voisins les plus proches :
  - 3 sont de classe A (●)
  - 2 sont de classe B (■)
  → Vote majoritaire → Classe A ✅
```

### 2.2 Implémentation

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# --- Entraîner KNN ---
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train_scaled, y_train)  # ATTENTION : il faut normaliser !
y_pred_knn = knn.predict(X_test_scaled)

print(f"Accuracy KNN (K=5) : {accuracy_score(y_test, y_pred_knn):.4f}")

# --- Trouver le meilleur K ---
import matplotlib.pyplot as plt

k_values = range(1, 31)
scores = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train_scaled, y_train)
    scores.append(knn.score(X_test_scaled, y_test))

plt.figure(figsize=(10, 5))
plt.plot(k_values, scores, 'o-')
plt.xlabel('K (nombre de voisins)')
plt.ylabel('Accuracy')
plt.title('Score en fonction de K')
plt.axvline(x=k_values[np.argmax(scores)], color='red', linestyle='--',
            label=f'Meilleur K = {k_values[np.argmax(scores)]}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"Meilleur K : {k_values[np.argmax(scores)]}, Accuracy : {max(scores):.4f}")
```

### 2.3 Paramètres importants

| Paramètre | Options | Impact |
|-----------|---------|--------|
| **n_neighbors (K)** | Entier impair (3, 5, 7...) | K petit → overfitting, K grand → underfitting |
| **metric** | 'euclidean', 'manhattan', 'minkowski' | Distance utilisée pour trouver les voisins |
| **weights** | 'uniform', 'distance' | 'distance' donne plus de poids aux voisins proches |

> ⚠️ **Attention** : "KNN est **très sensible** à l'échelle des features. Si une feature va de 0 à 1000 et une autre de 0 à 1, la première dominera le calcul de distance. **TOUJOURS normaliser** avant d'utiliser KNN."

> 💡 **Conseil** : "KNN ne fonctionne pas bien en haute dimension (**curse of dimensionality**). Au-delà de 20-30 features, les distances deviennent moins significatives. Envisagez une réduction de dimension (PCA) avant."

---

## 3. ⚡ Support Vector Machine (SVM)

### 3.1 Concept

SVM cherche l'**hyperplan** qui sépare le mieux les classes, en maximisant la **marge** (distance) entre les classes.

```
  Classe B (■)
       ■ ■
      ■  ■          Marge maximale
     ■    ■       ←─────────────→
    ────────────── Hyperplan optimal ──────────────
             ●      ●
              ● ●  ●
               ●  ●
              Classe A (●)
```

### 3.2 Le Kernel Trick

Quand les données ne sont pas linéairement séparables, le **kernel trick** projette les données dans un espace de dimension supérieure où elles deviennent séparables.

| Kernel | Quand l'utiliser | Complexité |
|--------|-----------------|-----------|
| **linear** | Données linéairement séparables, beaucoup de features | Faible |
| **rbf** (défaut) | Cas général, relations non-linéaires | Moyenne |
| **poly** | Relations polynomiales | Élevée |

### 3.3 Implémentation

```python
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# --- SVM avec kernel RBF (par défaut) ---
svm = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42, probability=True)
svm.fit(X_train_scaled, y_train)
y_pred_svm = svm.predict(X_test_scaled)

print("=== SVM (kernel=rbf) ===")
print(classification_report(y_test, y_pred_svm))

# --- Comparer les kernels ---
kernels = ['linear', 'rbf', 'poly']
for kernel in kernels:
    svm = SVC(kernel=kernel, random_state=42)
    svm.fit(X_train_scaled, y_train)
    score = svm.score(X_test_scaled, y_test)
    print(f"Kernel {kernel:>8} → Accuracy: {score:.4f}")
```

### 3.4 Paramètres importants

| Paramètre | Rôle | Impact |
|-----------|------|--------|
| **C** | Force de régularisation | C petit → marge large (plus de tolérance), C grand → marge étroite (moins de tolérance) |
| **gamma** | Influence de chaque point | gamma grand → chaque point a une petite zone d'influence, gamma petit → zone large |
| **kernel** | Type de transformation | Définit la complexité de la frontière de décision |

> 💡 **Conseil de pro** : "SVM excelle quand le **nombre de features est supérieur au nombre d'échantillons** (nb_features > nb_samples). C'est aussi un bon choix pour les petits et moyens datasets (<10 000 échantillons)."

> ⚠️ **Attention** : "SVM ne passe pas bien à l'échelle. Sur de grands datasets (>100 000 échantillons), préférez la régression logistique ou les arbres de décision."

---

## 4. 🌳 Arbres de Décision

### 4.1 Concept

Un arbre de décision est une suite de **questions if/else** qui partitionnent les données jusqu'à une prédiction.

```
                    [surface > 50m²?]
                    /              \
                  Oui              Non
                  /                  \
       [quartier = centre?]     [étage > 3?]
        /            \           /         \
      Oui           Non        Oui        Non
       |              |          |           |
   Cher (A)    Moyen (B)   Moyen (B)   Pas cher (C)
```

### 4.2 Implémentation

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# --- Entraîner ---
arbre = DecisionTreeClassifier(
    max_depth=4,           # Profondeur maximale (éviter l'overfitting)
    min_samples_split=10,  # Minimum d'échantillons pour splitter
    min_samples_leaf=5,    # Minimum d'échantillons par feuille
    random_state=42
)
arbre.fit(X_train, y_train)  # PAS besoin de normaliser !
y_pred_arbre = arbre.predict(X_test)

print(f"Accuracy Arbre : {arbre.score(X_test, y_test):.4f}")

# --- Visualiser l'arbre ---
plt.figure(figsize=(20, 10))
plot_tree(
    arbre,
    feature_names=cancer.feature_names,
    class_names=cancer.target_names,
    filled=True,           # Colorer selon la classe
    rounded=True,
    fontsize=8
)
plt.title("Arbre de décision")
plt.tight_layout()
plt.show()

# --- Importance des features ---
importances = pd.DataFrame({
    'Feature': cancer.feature_names,
    'Importance': arbre.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n=== Top 10 features les plus importantes ===")
print(importances.head(10))

# Visualiser
plt.figure(figsize=(10, 6))
top_10 = importances.head(10)
plt.barh(top_10['Feature'], top_10['Importance'])
plt.xlabel('Importance')
plt.title("Importance des features (Arbre de Décision)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
```

### 4.3 Critères de split

| Critère | Formule | Quand l'utiliser |
|---------|---------|-----------------|
| **Gini** (défaut) | `1 - Σ(pᵢ²)` | Cas général, rapide |
| **Entropie** | `-Σ(pᵢ * log₂(pᵢ))` | Plus théorique, résultats similaires |

### 4.4 Avantages et Inconvénients

| Avantages | Inconvénients |
|-----------|---------------|
| ✅ Très interprétable | ❌ Overfitting facile |
| ✅ Pas besoin de normaliser | ❌ Instable (petits changements → arbre différent) |
| ✅ Gère numériques et catégorielles | ❌ Biaisé vers les features avec beaucoup de valeurs |
| ✅ Rapide à entraîner | ❌ Limité pour les relations complexes |
| ✅ Visualisable | ❌ Performances inférieures aux ensembles |

> 💡 **Conseil** : "Toujours limiter `max_depth` pour éviter l'overfitting. Un arbre trop profond mémorise les données au lieu d'apprendre les patterns."

> 💡 **Conseil de pro** : "Les arbres de décision seuls sont rarement les meilleurs modèles, mais ils sont la brique de base des **Random Forests** et du **Gradient Boosting** (XGBoost, LightGBM) qui sont parmi les meilleurs algorithmes de ML."

---

## 5. 📊 MÉTRIQUES DE CLASSIFICATION

C'est la section la plus importante de ce chapitre. Bien comprendre les métriques est **essentiel** pour évaluer correctement un classifieur.

### 5.1 Matrice de Confusion

La matrice de confusion est le point de départ de **toutes** les métriques de classification.

```
                        PRÉDICTION
                    Positif    Négatif
           ┌──────────┬──────────┐
  Positif  │    TP     │    FN    │   ← Vrais positifs
RÉALITÉ    │ (Vrai     │ (Faux    │
           │  Positif) │  Négatif)│
           ├──────────┼──────────┤
  Négatif  │    FP     │    TN    │   ← Vrais négatifs
           │ (Faux     │ (Vrai    │
           │  Positif) │  Négatif)│
           └──────────┴──────────┘
```

**Analogie médicale** (test de dépistage du cancer) :

| Terme | Signification | Exemple médical | Conséquence |
|-------|-------------|-----------------|-------------|
| **TP** (Vrai Positif) | Prédit positif, est positif | Malade détecté comme malade | ✅ Bon |
| **TN** (Vrai Négatif) | Prédit négatif, est négatif | Sain détecté comme sain | ✅ Bon |
| **FP** (Faux Positif) | Prédit positif, est négatif | Sain détecté comme malade | ⚠️ Stress, examens inutiles |
| **FN** (Faux Négatif) | Prédit négatif, est positif | Malade non détecté | ❌ **DANGEREUX** (cancer non traité) |

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Calculer la matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(cm)

# Visualiser
fig, ax = plt.subplots(figsize=(8, 6))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=cancer.target_names)
disp.plot(cmap='Blues', ax=ax, values_format='d')
plt.title('Matrice de Confusion')
plt.tight_layout()
plt.show()

# Extraire TP, TN, FP, FN (pour classification binaire)
tn, fp, fn, tp = cm.ravel()
print(f"\nTP (Vrais Positifs) : {tp}")
print(f"TN (Vrais Négatifs) : {tn}")
print(f"FP (Faux Positifs)  : {fp}")
print(f"FN (Faux Négatifs)  : {fn}")
```

### 5.2 Accuracy (Exactitude)

**Formule** : `Accuracy = (TP + TN) / (TP + TN + FP + FN)`

```python
from sklearn.metrics import accuracy_score

acc = accuracy_score(y_test, y_pred)
print(f"Accuracy : {acc:.4f}")
# Interprétation : "X% des prédictions sont correctes"
```

> ⚠️ **PIÈGE MAJEUR** : "Une accuracy de 95% sur un dataset 95/5 déséquilibré est **INUTILE**. Un modèle qui prédit toujours la classe majoritaire obtient 95% d'accuracy sans rien avoir appris !"

```python
# Démonstration du piège de l'accuracy
import numpy as np

# Dataset déséquilibré : 95% classe 0, 5% classe 1
y_desequilibre = np.array([0]*950 + [1]*50)

# Modèle "stupide" : prédit toujours 0
y_stupide = np.zeros_like(y_desequilibre)

print(f"Accuracy du modèle 'stupide' : {accuracy_score(y_desequilibre, y_stupide):.2%}")
# → 95.00% ! Mais il ne détecte AUCUN cas positif !
```

### 5.3 Precision (Précision)

**Question** : "Parmi ceux que j'ai **prédit positifs**, combien le sont **vraiment** ?"

**Formule** : `Precision = TP / (TP + FP)`

```python
from sklearn.metrics import precision_score

prec = precision_score(y_test, y_pred)
print(f"Precision : {prec:.4f}")
```

| Quand c'est important | Pourquoi | Exemple |
|----------------------|---------|---------|
| **FP coûteux** | Un faux positif a des conséquences graves | Filtre anti-spam : un vrai mail classé spam = mail perdu |
| Décision irréversible | On ne peut pas revenir en arrière | Envoi d'une offre commerciale (coûteuse) |

> 💡 **Conseil** : "La precision répond à la question : 'Quand mon modèle dit OUI, a-t-il raison ?' Si un faux positif est coûteux → optimisez la precision."

### 5.4 Recall (Rappel / Sensibilité)

**Question** : "Parmi les **vrais positifs**, combien ai-je **trouvés** ?"

**Formule** : `Recall = TP / (TP + FN)`

```python
from sklearn.metrics import recall_score

rec = recall_score(y_test, y_pred)
print(f"Recall : {rec:.4f}")
```

| Quand c'est important | Pourquoi | Exemple |
|----------------------|---------|---------|
| **FN coûteux** | Un faux négatif a des conséquences graves | Diagnostic cancer : rater un cancer = patient non traité |
| Détection critique | Ne pas rater les vrais cas | Détection de fraude bancaire |

> 💡 **Conseil** : "Le recall répond à la question : 'Parmi tous les vrais cas, combien ai-je détectés ?' Si un faux négatif est dangereux → optimisez le recall."

### 5.5 F1-Score

**Moyenne harmonique** de Precision et Recall — un compromis entre les deux.

**Formule** : `F1 = 2 * (Precision * Recall) / (Precision + Recall)`

```python
from sklearn.metrics import f1_score

f1 = f1_score(y_test, y_pred)
print(f"F1-Score : {f1:.4f}")
```

| Propriété | Détail |
|-----------|--------|
| **Plage** | [0, 1] (1 = parfait) |
| **Quand l'utiliser** | Quand Precision ET Recall comptent, classes déséquilibrées |
| **Avantage** | Pénalise fortement si l'un des deux est faible |
| **Moyenne harmonique** | Plus conservatrice que la moyenne arithmétique |

> 💡 **Conseil de pro** : "Le F1-Score est souvent la **meilleure métrique par défaut** pour la classification, surtout avec des classes déséquilibrées. Si vous ne savez pas quelle métrique choisir, commencez par le F1."

### 5.6 ROC-AUC

La **courbe ROC** trace le **Taux de Vrais Positifs** (Recall) contre le **Taux de Faux Positifs** pour tous les seuils de décision possibles.

**AUC** (Area Under the Curve) : l'aire sous la courbe ROC.

| AUC | Interprétation |
|-----|---------------|
| 1.0 | Modèle parfait |
| 0.9 - 1.0 | Excellent |
| 0.8 - 0.9 | Bon |
| 0.7 - 0.8 | Acceptable |
| 0.5 | Random (aucun pouvoir prédictif) |
| < 0.5 | Pire que le hasard (inverser les prédictions !) |

```python
from sklearn.metrics import roc_curve, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt

# Calculer les probabilités
y_proba = log_reg.predict_proba(X_test_scaled)[:, 1]

# AUC
auc = roc_auc_score(y_test, y_proba)
print(f"AUC-ROC : {auc:.4f}")

# Tracer la courbe ROC
fpr, tpr, thresholds = roc_curve(y_test, y_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, linewidth=2, label=f'Logistique (AUC = {auc:.3f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random (AUC = 0.5)')
plt.xlabel('Taux de Faux Positifs (FPR)')
plt.ylabel('Taux de Vrais Positifs (TPR / Recall)')
plt.title('Courbe ROC')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.fill_between(fpr, tpr, alpha=0.1)
plt.show()
```

### 5.7 Courbe Precision-Recall

Plus informative que la ROC pour les **classes très déséquilibrées**.

```python
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.metrics import PrecisionRecallDisplay

# Calcul
precision_vals, recall_vals, thresholds_pr = precision_recall_curve(y_test, y_proba)
ap = average_precision_score(y_test, y_proba)

# Visualisation
plt.figure(figsize=(8, 6))
plt.plot(recall_vals, precision_vals, linewidth=2, label=f'AP = {ap:.3f}')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Courbe Precision-Recall')
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)
plt.fill_between(recall_vals, precision_vals, alpha=0.1)
plt.show()
```

> 💡 **Conseil de pro** : "Pour les classes **très déséquilibrées** (>95/5), la courbe Precision-Recall est plus informative que la courbe ROC. La ROC peut donner une fausse impression de bonne performance."

### 5.8 Tableau récapitulatif de toutes les métriques

| Métrique | Question | Formule | Sensible déséquilibre | Quand l'utiliser |
|----------|----------|---------|----------------------|-----------------|
| **Accuracy** | Combien de prédictions correctes ? | (TP+TN)/Total | ⚠️ Très | Classes équilibrées uniquement |
| **Precision** | Quand je dis "oui", ai-je raison ? | TP/(TP+FP) | ✅ Non | FP coûteux (spam, pub) |
| **Recall** | Ai-je trouvé tous les positifs ? | TP/(TP+FN) | ✅ Non | FN coûteux (cancer, fraude) |
| **F1-Score** | Compromis Precision/Recall | 2*P*R/(P+R) | ✅ Non | Métrique par défaut |
| **AUC-ROC** | Qualité globale du ranking | Aire sous ROC | Modéré | Vue d'ensemble, comparaison |
| **Average Precision** | Qualité du ranking (déséquilibré) | Aire sous PR | ✅ Non | Classes très déséquilibrées |

> 💡 **Conseil de pro** : "**TOUJOURS** choisir sa métrique **AVANT** de modéliser, en fonction du **coût métier** des erreurs (FP vs FN). Ne changez jamais de métrique en cours de route pour 'améliorer' artificiellement vos résultats."

### 5.9 Fonction d'évaluation complète

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay)
import matplotlib.pyplot as plt

def evaluer_classifieur(y_true, y_pred, y_proba=None, nom="Modèle"):
    """Évaluation complète d'un classifieur binaire"""
    print(f"╔{'═'*50}╗")
    print(f"║  Évaluation : {nom:^34} ║")
    print(f"╠{'═'*50}╣")

    # Métriques textuelles
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"║  Accuracy   : {acc:.4f}                          ║")
    print(f"║  Precision  : {prec:.4f}                          ║")
    print(f"║  Recall     : {rec:.4f}                          ║")
    print(f"║  F1-Score   : {f1:.4f}                          ║")

    if y_proba is not None:
        auc = roc_auc_score(y_true, y_proba)
        print(f"║  AUC-ROC    : {auc:.4f}                          ║")

    print(f"╚{'═'*50}╝")

    # Rapport détaillé
    print("\n" + classification_report(y_true, y_pred))

    # Matrice de confusion
    fig, ax = plt.subplots(figsize=(6, 5))
    cm = confusion_matrix(y_true, y_pred)
    ConfusionMatrixDisplay(confusion_matrix=cm).plot(cmap='Blues', ax=ax)
    plt.title(f'Matrice de Confusion - {nom}')
    plt.tight_layout()
    plt.show()

# Utilisation
evaluer_classifieur(y_test, y_pred, y_proba[:, 1], "Régression Logistique")
```

---

## 6. 🎚️ Seuil de décision

### 6.1 Le problème du seuil par défaut

Par défaut, le seuil est 0.5 : si P(classe 1) >= 0.5, on prédit classe 1. Mais ce seuil n'est pas toujours optimal.

### 6.2 Impact du seuil sur Precision et Recall

```
Seuil ↑ (ex: 0.8)
  → Precision ↑ (on est plus sûr quand on dit "oui")
  → Recall ↓ (on rate plus de vrais positifs)

Seuil ↓ (ex: 0.3)
  → Precision ↓ (plus de faux positifs)
  → Recall ↑ (on détecte plus de vrais positifs)
```

> 💡 **Conseil** : "Le seuil de 0.5 n'est pas une vérité absolue. Ajustez-le en fonction de votre problème métier."

### 6.3 Trouver le seuil optimal

```python
from sklearn.metrics import precision_recall_curve, f1_score
import numpy as np
import matplotlib.pyplot as plt

# Obtenir les probabilités
y_proba = log_reg.predict_proba(X_test_scaled)[:, 1]

# --- Méthode 1 : Seuil qui maximise le F1-Score ---
precisions, recalls, seuils = precision_recall_curve(y_test, y_proba)
# Le tableau de seuils a un élément de moins que precision/recall
f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-10)
seuil_optimal_f1 = seuils[np.argmax(f1_scores)]
print(f"Seuil optimal (max F1) : {seuil_optimal_f1:.3f}")
print(f"F1 au seuil optimal    : {max(f1_scores):.4f}")

# --- Méthode 2 : Youden's Index (max TPR - FPR) ---
from sklearn.metrics import roc_curve
fpr, tpr, seuils_roc = roc_curve(y_test, y_proba)
youden = tpr - fpr
seuil_optimal_youden = seuils_roc[np.argmax(youden)]
print(f"Seuil optimal (Youden)  : {seuil_optimal_youden:.3f}")

# --- Visualiser l'impact du seuil ---
seuils_test = np.arange(0.1, 0.95, 0.05)
prec_list, rec_list, f1_list = [], [], []

for s in seuils_test:
    y_pred_seuil = (y_proba >= s).astype(int)
    prec_list.append(precision_score(y_test, y_pred_seuil, zero_division=0))
    rec_list.append(recall_score(y_test, y_pred_seuil))
    f1_list.append(f1_score(y_test, y_pred_seuil))

plt.figure(figsize=(10, 6))
plt.plot(seuils_test, prec_list, 'b-', label='Precision')
plt.plot(seuils_test, rec_list, 'r-', label='Recall')
plt.plot(seuils_test, f1_list, 'g--', linewidth=2, label='F1-Score')
plt.axvline(x=seuil_optimal_f1, color='green', linestyle=':', label=f'Seuil optimal = {seuil_optimal_f1:.2f}')
plt.xlabel('Seuil de décision')
plt.ylabel('Score')
plt.title('Precision, Recall et F1 en fonction du seuil')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.show()

# --- Appliquer le seuil optimal ---
y_pred_optimal = (y_proba >= seuil_optimal_f1).astype(int)
print("\n=== Avec seuil par défaut (0.5) ===")
print(f"F1 = {f1_score(y_test, y_pred):.4f}")
print("\n=== Avec seuil optimal ===")
print(f"F1 = {f1_score(y_test, y_pred_optimal):.4f}")
```

> 💡 **Conseil de pro** : "Dans un contexte médical (détection de cancer), baissez le seuil (ex: 0.3) pour maximiser le recall — il vaut mieux faire des examens complémentaires inutiles que rater un cancer. Dans un contexte de spam, montez le seuil (ex: 0.7) pour maximiser la precision — il ne faut pas que des vrais mails finissent en spam."

---

## 7. 🎯 Classification multi-classes

### 7.1 Stratégies

| Stratégie | Principe | Nombre de modèles |
|-----------|---------|-------------------|
| **One-vs-Rest (OvR)** | Un modèle par classe (classe X vs toutes les autres) | N modèles |
| **One-vs-One (OvO)** | Un modèle par paire de classes | N*(N-1)/2 modèles |

### 7.2 Métriques multi-classes

```python
from sklearn.metrics import classification_report, f1_score
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Charger un dataset multi-classes
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

# Entraîner
log_reg_multi = LogisticRegression(max_iter=1000, random_state=42)
log_reg_multi.fit(X_train, y_train)
y_pred_multi = log_reg_multi.predict(X_test)

# Rapport détaillé par classe
print("=== Rapport de classification (multi-classes) ===")
print(classification_report(y_test, y_pred_multi, target_names=iris.target_names))

# Différentes moyennes pour le F1
print("=== Moyennes F1 ===")
print(f"F1 macro    : {f1_score(y_test, y_pred_multi, average='macro'):.4f}")
print(f"F1 micro    : {f1_score(y_test, y_pred_multi, average='micro'):.4f}")
print(f"F1 weighted : {f1_score(y_test, y_pred_multi, average='weighted'):.4f}")
```

### 7.3 Comprendre les moyennes

| Moyenne | Calcul | Quand l'utiliser |
|---------|--------|-----------------|
| **macro** | Moyenne simple des F1 par classe | Toutes les classes ont la même importance |
| **micro** | TP/FP/FN globaux | Donne plus de poids aux classes fréquentes |
| **weighted** | Moyenne pondérée par le support | Classes déséquilibrées |

> 💡 **Conseil** : "Utilisez `average='weighted'` pour le F1-Score si les classes sont déséquilibrées. Utilisez `average='macro'` si toutes les classes sont aussi importantes."

---

## 8. 📈 Comment améliorer son classifieur

### 8.1 Checklist d'amélioration

| Étape | Action | Outil/Méthode |
|-------|--------|--------------|
| 1️⃣ | **Vérifier le déséquilibre** des classes | `value_counts()`, `class_weight='balanced'` |
| 2️⃣ | **Tester plusieurs algorithmes** | Logistique, KNN, SVM, Arbre, Random Forest |
| 3️⃣ | **Tuner les hyperparamètres** | `GridSearchCV`, `RandomizedSearchCV` |
| 4️⃣ | **Feature engineering** | Créer de nouvelles features, sélectionner les meilleures |
| 5️⃣ | **Plus de données ?** | Courbes d'apprentissage |
| 6️⃣ | **Ajuster le seuil** | Courbe Precision-Recall |
| 7️⃣ | **Ensembles** | Random Forest, Gradient Boosting, Voting |

### 8.2 Comparaison de plusieurs algorithmes

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd

# Définir les modèles
modeles = {
    'Logistique': LogisticRegression(max_iter=1000, random_state=42),
    'KNN (K=5)': KNeighborsClassifier(n_neighbors=5),
    'SVM (rbf)': SVC(kernel='rbf', random_state=42),
    'Arbre': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

# Entraîner et évaluer
resultats = []
for nom, modele in modeles.items():
    # KNN et SVM nécessitent des données normalisées
    if nom in ['KNN (K=5)', 'SVM (rbf)', 'Logistique']:
        modele.fit(X_train_scaled, y_train)
        y_pred_m = modele.predict(X_test_scaled)
    else:
        modele.fit(X_train, y_train)
        y_pred_m = modele.predict(X_test)

    resultats.append({
        'Modèle': nom,
        'Accuracy': accuracy_score(y_test, y_pred_m),
        'F1': f1_score(y_test, y_pred_m),
        'Precision': precision_score(y_test, y_pred_m),
        'Recall': recall_score(y_test, y_pred_m)
    })

# Afficher le tableau comparatif
df_resultats = pd.DataFrame(resultats).sort_values('F1', ascending=False)
print("=== Comparaison des algorithmes ===")
print(df_resultats.to_string(index=False))
```

### 8.3 GridSearchCV pour le tuning

```python
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# Grille d'hyperparamètres
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# GridSearch
grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='f1',         # Optimiser pour le F1
    n_jobs=-1,
    verbose=1
)
grid.fit(X_train, y_train)

print(f"Meilleurs paramètres : {grid.best_params_}")
print(f"Meilleur F1 (CV) : {grid.best_score_:.4f}")
print(f"F1 test : {f1_score(y_test, grid.predict(X_test)):.4f}")
```

> 💡 **Conseil de pro** : "Ne comparez **JAMAIS** des modèles avec des métriques différentes. Fixez **UNE** métrique principale (ex: F1-Score) et utilisez-la systématiquement pour toutes les comparaisons."

### 8.4 Guide de choix d'algorithme

| Critère | Logistique | KNN | SVM | Arbre | Random Forest |
|---------|-----------|-----|-----|-------|--------------|
| **Interprétabilité** | ⭐⭐⭐ | ⭐ | ⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Rapidité entraînement** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Rapidité prédiction** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Grands datasets** | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Normalisation nécessaire** | Oui | **Oui** | **Oui** | Non | Non |
| **Non-linéarité** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Premier choix ?** | Baseline | Prototypage | Petit dataset | Explicabilité | Performance |

---

## 🎯 Points clés à retenir

1. **Régression logistique** = baseline de classification. Commencez **toujours** par elle
2. **KNN** : simple mais sensible à l'échelle. Toujours normaliser
3. **SVM** : puissant sur petits datasets, kernel trick pour non-linéarité
4. **Arbres** : interprétables mais overfittent. Toujours limiter `max_depth`
5. **Accuracy** est **trompeuse** avec des classes déséquilibrées
6. **Precision** quand FP coûteux (spam), **Recall** quand FN coûteux (cancer)
7. **F1-Score** = métrique par défaut recommandée
8. **AUC-ROC** pour la vue d'ensemble, **PR-AUC** pour les classes très déséquilibrées
9. **Le seuil de 0.5** n'est pas sacré — ajustez-le selon le contexte métier
10. **Choisir la métrique AVANT** de modéliser, en fonction du coût des erreurs

---

## ✅ Checklist de validation

- [ ] Je sais implémenter une régression logistique et interpréter `predict_proba`
- [ ] Je sais implémenter KNN et trouver le meilleur K
- [ ] Je comprends le concept de SVM et quand l'utiliser
- [ ] Je sais entraîner un arbre de décision et le visualiser
- [ ] Je sais lire et interpréter une matrice de confusion (TP, TN, FP, FN)
- [ ] Je connais la différence entre Accuracy, Precision, Recall et F1
- [ ] Je sais tracer et interpréter une courbe ROC et calculer l'AUC
- [ ] Je sais tracer une courbe Precision-Recall
- [ ] Je sais ajuster le seuil de décision selon le contexte métier
- [ ] Je sais comparer plusieurs algorithmes avec les mêmes métriques
- [ ] Je sais utiliser GridSearchCV pour tuner les hyperparamètres
- [ ] Je sais utiliser `classification_report` pour un rapport complet

---

**Précédent** : [Chapitre 4 : Régression – Prédire des Valeurs Continues](04-regression.md)
