# Chapitre 8 : Évaluation et Métriques – L'Art de Mesurer la Performance

> **Ce chapitre est LE plus important de toute la formation.** Un modèle de Machine Learning n'existe que par sa capacité à être évalué correctement. Un modèle mal évalué est un modèle dangereux.

## 🎯 Objectifs

- Maîtriser toutes les métriques de Machine Learning (régression et classification)
- Comprendre en profondeur l'overfitting et l'underfitting
- Maîtriser toutes les formes de cross-validation
- Savoir choisir LA bonne métrique selon le contexte métier
- Diagnostiquer les problèmes d'un modèle et savoir les corriger
- Construire une méthodologie complète d'évaluation et d'amélioration

---

## 1. 🧠 Pourquoi l'évaluation est cruciale

### 1.1 Le piège du score d'entraînement

Un modèle qui « marche » sur les données d'entraînement peut être **catastrophique** en production. C'est comme un étudiant qui apprend par cœur les réponses d'un examen passé : il obtient 100% sur cet examen, mais 30% sur un nouvel examen.

```
Entraînement (étudier)  →  accuracy_train = 99%   ← Ca ne veut RIEN dire
Test (examen)           →  accuracy_test = 72%     ← La VRAIE performance
Production (vie réelle) →  accuracy_prod = ???      ← Ce qui compte VRAIMENT
```

### 1.2 Les conséquences d'une mauvaise évaluation

| Erreur d'évaluation | Conséquence |
|---|---|
| Évaluer sur le train set | Surestimation massive de la performance |
| Mauvaise métrique choisie | Modèle optimisé pour le mauvais objectif |
| Pas de cross-validation | Résultats instables, non reproductibles |
| Data leakage | Performance artificielle, crash en production |
| Ignorer le déséquilibre des classes | Accuracy trompeuse (99% en prédisant toujours la classe majoritaire) |

> 💡 **Conseil de pro** : "La métrique choisie doit refléter le COÛT MÉTIER de l'erreur. Une accuracy de 95% ne veut rien dire si les 5% d'erreurs coûtent des millions ou des vies. Toujours demander : « Quel est le coût d'une erreur ? »"

---

## 2. 📊 Métriques de régression

### 2.0 Pour les débutants : c'est quoi une métrique de régression ?

En régression, le modèle prédit un **nombre** (un prix, une température, un âge...). La métrique mesure **à quel point la prédiction est loin de la réalité**.

#### L'analogie du GPS

Imaginez un GPS qui estime le temps de trajet :

```
Trajet réel : 30 min     GPS dit : 28 min    → Erreur = 2 min  ✅ Pas grave
Trajet réel : 30 min     GPS dit : 55 min    → Erreur = 25 min ❌ Problème !
Trajet réel : 30 min     GPS dit : 30 min    → Erreur = 0 min  🎯 Parfait !
```

Les métriques de régression quantifient ces erreurs de différentes manières.

#### Les 4 métriques essentielles expliquées simplement

| Métrique | En langage courant | Exemple avec des prix immobiliers |
|----------|-------------------|----------------------------------|
| **MAE** | "En moyenne, je me trompe de X euros" | MAE = 15 000€ → les prédictions sont à ±15 000€ du vrai prix |
| **RMSE** | "Comme la MAE, mais les grosses erreurs comptent BEAUCOUP plus" | Une erreur de 100 000€ pèse bien plus qu'une erreur de 10 000€ |
| **R²** | "Quelle proportion du prix le modèle arrive-t-il à expliquer ?" | R² = 0.85 → le modèle explique 85% des variations de prix |
| **MAPE** | "En pourcentage, je me trompe de X%" | MAPE = 8% → les prédictions sont à ±8% du vrai prix |

#### Comment savoir si c'est bon ?

```
         Bon modèle            Mauvais modèle
         ──────────            ──────────────
MAE  :   10 000€               80 000€
RMSE :   15 000€               120 000€
R²   :   0.92                  0.35
MAPE :   5%                    40%
```

> 💡 **Pour débuter** : Concentrez-vous sur le **R²** (score de 0 à 1, plus c'est proche de 1, mieux c'est) et la **MAE** (l'erreur moyenne en unité compréhensible). Les autres métriques viendront naturellement avec la pratique.

---

### 2.1 Vue d'ensemble technique

| Métrique | Formule simplifiée | Interprétation | Range | Bon si |
|---|---|---|---|---|
| **MSE** | Moyenne((y - ŷ)²) | Erreur quadratique moyenne | [0, +∞] | Proche de 0 |
| **RMSE** | √MSE | Erreur en unité de la cible | [0, +∞] | Proche de 0 |
| **MAE** | Moyenne(|y - ŷ|) | Erreur absolue moyenne | [0, +∞] | Proche de 0 |
| **R²** | 1 - SS_res/SS_tot | % de variance expliquée | [-∞, 1] | Proche de 1 |
| **MAPE** | Moyenne(|y - ŷ| / |y|) × 100 | Erreur relative en % | [0, +∞] | Proche de 0 |
| **RMSLE** | √Moyenne((log(1+y) - log(1+ŷ))²) | Erreur log (pénalise sous-estimations) | [0, +∞] | Proche de 0 |

### 2.2 Implémentation détaillée

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error
)

# Exemple : prédiction de prix immobilier
y_true = np.array([200000, 350000, 150000, 500000, 275000])
y_pred = np.array([210000, 330000, 160000, 480000, 290000])

# Calculer toutes les métriques
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
mape = mean_absolute_percentage_error(y_true, y_pred)

print("=== Métriques de Régression ===")
print(f"MSE  : {mse:,.0f}")
print(f"RMSE : {rmse:,.0f} €")
print(f"MAE  : {mae:,.0f} €")
print(f"R²   : {r2:.4f}")
print(f"MAPE : {mape:.2%}")
```

### 2.3 Quand utiliser quelle métrique ?

| Métrique | Quand l'utiliser | Sensibilité aux outliers |
|---|---|---|
| **RMSE** | Quand les grosses erreurs sont très coûteuses | Très sensible |
| **MAE** | Quand toutes les erreurs ont le même coût | Robuste |
| **R²** | Pour communiquer avec des non-techniques | Modérée |
| **MAPE** | Quand on veut une erreur relative (%) | Problème si y ≈ 0 |
| **RMSLE** | Prix, comptages (valeurs très variables) | Modérée |

> 💡 **Conseil** : "Pour un problème de prix immobilier, utilisez le RMSE comme métrique principale (pénalise les grosses erreurs) et le MAPE pour communiquer (« on se trompe de 8% en moyenne »). Le R² est utile pour comparer des modèles entre eux."

> ⚠️ **Attention** : "Le R² peut être négatif ! Cela signifie que votre modèle est PIRE que la moyenne. Un R² de 0 signifie que votre modèle prédit toujours la moyenne. Seul un R² positif montre que le modèle apprend quelque chose."

### 2.4 Visualisation des erreurs de régression

```python
import matplotlib.pyplot as plt

# Graphique : Prédictions vs Valeurs réelles
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Predicted vs Actual
axes[0].scatter(y_true, y_pred, alpha=0.7)
axes[0].plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()],
             'r--', linewidth=2, label='Prédiction parfaite')
axes[0].set_xlabel('Valeurs réelles')
axes[0].set_ylabel('Prédictions')
axes[0].set_title('Prédictions vs Réalité')
axes[0].legend()

# 2. Distribution des résidus
residus = y_true - y_pred
axes[1].hist(residus, bins=20, edgecolor='black', alpha=0.7)
axes[1].axvline(x=0, color='red', linestyle='--')
axes[1].set_xlabel('Résidus (erreur)')
axes[1].set_ylabel('Fréquence')
axes[1].set_title('Distribution des Résidus')

# 3. Résidus vs Prédictions (vérifier l'homoscédasticité)
axes[2].scatter(y_pred, residus, alpha=0.7)
axes[2].axhline(y=0, color='red', linestyle='--')
axes[2].set_xlabel('Prédictions')
axes[2].set_ylabel('Résidus')
axes[2].set_title('Résidus vs Prédictions')

plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "Tracez TOUJOURS le graphique des résidus. Les résidus doivent être centrés autour de 0, de distribution normale, et sans pattern. Un pattern en U ou en éventail indique un problème dans le modèle."

---

## 3. 📊 Métriques de classification

### 3.0 Pour les débutants : c'est quoi une métrique de classification ?

En classification, le modèle prédit une **catégorie** (oui/non, spam/pas spam, malade/sain...). La métrique mesure **à quel point le modèle se trompe dans ses catégorisations**.

#### L'analogie du test médical

Imaginez un test de dépistage pour une maladie. Le test peut donner **4 résultats** :

```
                         Le test dit "Malade"       Le test dit "Sain"
                         ─────────────────────      ──────────────────
Vraiment MALADE    →     ✅ Vrai Positif (TP)       ❌ Faux Négatif (FN)
                         "Bien détecté !"            "Raté ! Dangereux !"

Vraiment SAIN      →     ❌ Faux Positif (FP)       ✅ Vrai Négatif (TN)
                         "Fausse alarme"             "Bien identifié"
```

#### Les métriques expliquées avec des mots simples

| Métrique | Question qu'elle pose | Analogie médicale |
|----------|----------------------|-------------------|
| **Accuracy** | "Quel % de réponses sont correctes ?" | "Quel % de diagnostics sont bons ?" |
| **Precision** | "Quand je dis 'positif', ai-je raison ?" | "Quand le test dit 'malade', est-ce vrai ?" |
| **Recall** | "Est-ce que je détecte TOUS les positifs ?" | "Est-ce qu'on détecte TOUS les malades ?" |
| **F1-Score** | "Compromis entre precision et recall" | "Le test est-il à la fois fiable ET exhaustif ?" |
| **AUC-ROC** | "Le modèle sait-il distinguer les classes ?" | "Le test distingue-t-il bien malades et sains ?" |

#### Le piège n°1 des débutants : l'accuracy trompeuse

**Scenario** : Sur 1000 patients, 950 sont sains et 50 sont malades.

Un modèle qui prédit **TOUJOURS "sain"** a **95% d'accuracy** ! Mais il ne détecte **AUCUN** malade. C'est un modèle **parfaitement inutile**.

> 💡 **Règle d'or** : Quand les classes sont déséquilibrées (beaucoup plus de "non" que de "oui"), **ne regardez jamais l'accuracy seule**. Utilisez le F1-Score et l'AUC-ROC.

#### Comment choisir entre Precision et Recall ?

Tout dépend du **coût de l'erreur** :

| Situation | Métrique prioritaire | Pourquoi |
|-----------|---------------------|----------|
| Détecter un cancer | **Recall** (ne rater personne) | Mieux vaut une fausse alarme que rater un malade |
| Filtrer les spams | **Precision** (ne pas se tromper) | Mieux vaut laisser passer un spam que bloquer un vrai email |
| Détecter le churn client | **F1-Score** (équilibre) | On veut détecter les départs sans harceler les clients fidèles |
| Détecter une fraude bancaire | **Recall** (ne rien rater) | Mieux vaut bloquer une transaction légitime que laisser passer une fraude |

---

### 3.1 Matrice de confusion – La base de tout

La matrice de confusion est le point de départ de TOUTES les métriques de classification.

```
                    Prédit Positif    Prédit Négatif
Réel Positif    |      TP            |      FN         |
Réel Négatif    |      FP            |      TN         |
```

- **TP (True Positive)** : Correctement identifié comme positif
- **TN (True Negative)** : Correctement identifié comme négatif
- **FP (False Positive)** : Fausse alarme (prédit positif à tort)
- **FN (False Negative)** : Raté (n'a pas détecté un positif)

```python
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    average_precision_score
)
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import numpy as np

# Créer un dataset déséquilibré
X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_classes=2,
    weights=[0.9, 0.1],  # 90% classe 0, 10% classe 1
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner un modèle
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
y_proba = rf.predict_proba(X_test)[:, 1]

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(cm)

# Visualisation de la matrice de confusion
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Prédit Négatif', 'Prédit Positif'],
            yticklabels=['Réel Négatif', 'Réel Positif'])
plt.xlabel('Prédiction')
plt.ylabel('Réalité')
plt.title('Matrice de Confusion')
plt.tight_layout()
plt.show()
```

### 3.2 Les 5 métriques fondamentales

| Métrique | Formule | Question à laquelle elle répond | Range |
|---|---|---|---|
| **Accuracy** | (TP + TN) / Total | Quelle proportion est correctement classée ? | [0, 1] |
| **Precision** | TP / (TP + FP) | Parmi les prédits positifs, combien le sont vraiment ? | [0, 1] |
| **Recall** (Sensibilité) | TP / (TP + FN) | Parmi les vrais positifs, combien sont détectés ? | [0, 1] |
| **F1-Score** | 2 × (P × R) / (P + R) | Compromis harmonique precision-recall | [0, 1] |
| **AUC-ROC** | Aire sous la courbe ROC | Capacité à distinguer les classes | [0.5, 1] |

```python
# Rapport de classification complet
print("=== Rapport de Classification ===")
print(classification_report(y_test, y_pred, target_names=['Négatif', 'Positif']))

# Métriques individuelles
print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision : {precision_score(y_test, y_pred):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score  : {f1_score(y_test, y_pred):.4f}")
print(f"AUC-ROC   : {roc_auc_score(y_test, y_proba):.4f}")
```

### 3.3 Le piège de l'Accuracy

> ⚠️ **Attention** : "L'accuracy est la métrique la plus TROMPEUSE qui existe ! Sur un dataset avec 99% de négatifs, un modèle qui prédit TOUJOURS négatif a 99% d'accuracy mais ne détecte AUCUN positif. C'est un modèle parfaitement inutile."

```python
# Démonstration du piège de l'accuracy
# Modèle stupide : toujours prédire la classe majoritaire
from sklearn.dummy import DummyClassifier

dummy = DummyClassifier(strategy='most_frequent')
dummy.fit(X_train, y_train)
y_pred_dummy = dummy.predict(X_test)

print(f"Accuracy du modèle 'toujours négatif' : {accuracy_score(y_test, y_pred_dummy):.4f}")
print(f"Precision : {precision_score(y_test, y_pred_dummy, zero_division=0):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred_dummy):.4f}")
print(f"F1-Score  : {f1_score(y_test, y_pred_dummy):.4f}")
print("\n→ 90% d'accuracy mais AUCUNE détection des positifs !")
```

> 💡 **Conseil de pro** : "Ne JAMAIS utiliser l'accuracy seule comme métrique, surtout avec des classes déséquilibrées. Utilisez toujours le classification_report complet et l'AUC-ROC."

### 3.4 Courbe ROC et AUC

#### Pour les débutants : c'est quoi une courbe ROC ?

Imaginez un **curseur** de sensibilité sur votre modèle :

```
Curseur à gauche (prudent)              Curseur à droite (sensible)
──────────────────────                  ──────────────────────────
Peu de fausses alarmes                  Détecte tout
MAIS rate des positifs                  MAIS beaucoup de fausses alarmes
```

La courbe ROC trace **toutes les positions possibles du curseur**. L'**AUC** (l'aire sous la courbe) résume la qualité globale :

| AUC | Interprétation |
|-----|---------------|
| 0.50 | Le modèle tire au hasard (pile ou face) |
| 0.60-0.70 | Médiocre |
| 0.70-0.80 | Acceptable |
| 0.80-0.90 | Bon modèle |
| 0.90-1.00 | Excellent modèle |

> 💡 **Astuce de lecture** : Plus la courbe est proche du **coin supérieur gauche** du graphique, meilleur est le modèle.

#### Explication technique

La courbe ROC (Receiver Operating Characteristic) trace le **True Positive Rate** (Recall) en fonction du **False Positive Rate** pour différents seuils de classification.

```python
# Courbe ROC
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
auc = roc_auc_score(y_test, y_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, 'b-', linewidth=2, label=f'Random Forest (AUC = {auc:.3f})')
plt.plot([0, 1], [0, 1], 'r--', linewidth=1, label='Aléatoire (AUC = 0.5)')
plt.fill_between(fpr, tpr, alpha=0.1, color='blue')

plt.xlabel('Taux de Faux Positifs (FPR)')
plt.ylabel('Taux de Vrais Positifs (TPR / Recall)')
plt.title('Courbe ROC')
plt.legend(loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Trouver le seuil optimal (point le plus proche du coin supérieur gauche)
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]
print(f"Seuil optimal : {optimal_threshold:.3f}")
print(f"TPR au seuil optimal : {tpr[optimal_idx]:.3f}")
print(f"FPR au seuil optimal : {fpr[optimal_idx]:.3f}")
```

### 3.5 Courbe Precision-Recall

#### Pour les débutants : comprendre le compromis Precision-Recall

C'est un **dilemme** permanent :

- **Augmenter la Precision** (moins de fausses alarmes) → on baisse le Recall (on rate des vrais positifs)
- **Augmenter le Recall** (détecter tout) → on baisse la Precision (plus de fausses alarmes)

> **Analogie du filet de pêche** : Un filet à mailles serrées capture TOUS les poissons (Recall élevé) mais aussi des déchets (Precision basse). Un filet à grosses mailles ne capture que les gros poissons (Precision élevée) mais en laisse échapper beaucoup (Recall bas). Le F1-Score trouve le meilleur compromis entre les deux.

La courbe Precision-Recall visualise ce compromis pour tous les seuils possibles.

Pour les datasets très déséquilibrés, la courbe Precision-Recall est souvent **plus informative** que la courbe ROC.

```python
# Courbe Precision-Recall
precision_curve, recall_curve, thresholds_pr = precision_recall_curve(y_test, y_proba)
ap = average_precision_score(y_test, y_proba)

plt.figure(figsize=(8, 6))
plt.plot(recall_curve, precision_curve, 'g-', linewidth=2,
         label=f'Random Forest (AP = {ap:.3f})')
plt.fill_between(recall_curve, precision_curve, alpha=0.1, color='green')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Courbe Precision-Recall')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "Pour des classes très déséquilibrées (fraude, maladie rare), la courbe Precision-Recall et l'AP (Average Precision) sont PLUS fiables que la courbe ROC. L'AUC-ROC peut être trompeusement élevée quand la classe négative est très majoritaire."

### 3.6 Ajuster le seuil de classification

#### Pour les débutants : c'est quoi le seuil ?

Le modèle ne répond pas directement "oui" ou "non". Il donne une **probabilité** : "ce patient a 73% de chances d'être malade". Le **seuil** est la limite à partir de laquelle on décide "positif".

```
Seuil = 0.3 (prudent)              Seuil = 0.7 (strict)
──────────────────                  ──────────────────
"Dès que c'est > 30%,              "Seulement si c'est > 70%,
 je dis POSITIF"                     je dis POSITIF"

→ Détecte plus de positifs          → Détecte moins de positifs
→ Plus de fausses alarmes           → Moins de fausses alarmes
→ Meilleur Recall                   → Meilleure Precision
```

> 💡 **Pour débuter** : Gardez le seuil par défaut (0.5) pour commencer. Ajustez-le uniquement quand vous comprenez le coût métier de chaque type d'erreur.

Par défaut, sklearn utilise un seuil de 0.5. Mais ce n'est pas toujours optimal !

```python
# Analyser l'impact du seuil
seuils = np.arange(0.1, 0.9, 0.05)
resultats_seuil = []

for seuil in seuils:
    y_pred_seuil = (y_proba >= seuil).astype(int)
    resultats_seuil.append({
        'seuil': seuil,
        'precision': precision_score(y_test, y_pred_seuil, zero_division=0),
        'recall': recall_score(y_test, y_pred_seuil),
        'f1': f1_score(y_test, y_pred_seuil, zero_division=0),
        'accuracy': accuracy_score(y_test, y_pred_seuil)
    })

df_seuils = pd.DataFrame(resultats_seuil)

# Visualiser
plt.figure(figsize=(10, 6))
plt.plot(df_seuils['seuil'], df_seuils['precision'], 'b-', label='Precision', linewidth=2)
plt.plot(df_seuils['seuil'], df_seuils['recall'], 'r-', label='Recall', linewidth=2)
plt.plot(df_seuils['seuil'], df_seuils['f1'], 'g-', label='F1-Score', linewidth=2)
plt.axvline(x=0.5, color='gray', linestyle='--', label='Seuil par défaut')
plt.xlabel('Seuil de classification')
plt.ylabel('Score')
plt.title('Impact du seuil sur les métriques')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

> 💡 **Conseil** : "Le seuil de 0.5 n'est pas sacré ! Si les faux négatifs coûtent cher (diagnostic médical), baissez le seuil (ex: 0.3) pour augmenter le recall. Si les faux positifs coûtent cher (spam filter), augmentez le seuil (ex: 0.7) pour augmenter la precision."

---

## 4. 📊 Choisir LA bonne métrique

### 4.1 Selon le type de problème

| Problème | Métrique principale | Pourquoi | Métrique secondaire |
|---|---|---|---|
| **Prix immobilier** | RMSE | Même unité que la cible, pénalise les grosses erreurs | R², MAPE |
| **Détection de spam** | Precision | FP coûteux (email légitime en spam) | F1, Recall |
| **Diagnostic médical** | Recall | FN coûteux (rater une maladie = mortel) | F1, Specificity |
| **Fraude bancaire** | F1 ou AUC-PR | Classes très déséquilibrées | Precision, Recall |
| **Prédiction de churn** | AUC-PR | Classes déséquilibrées + besoin de ranking | F1 |
| **Scoring crédit** | AUC-ROC | Besoin de bien discriminer les profils | KS statistic |
| **Demande de stock** | MAE | Erreurs symétriques, pas de grosses pénalités | MAPE |
| **Prévision météo** | Accuracy | Classes relativement équilibrées | F1 par classe |
| **Recommandation** | AUC-ROC | Capacité à classer les items pertinents | Precision@K |
| **Véhicule autonome** | Recall | FN = ne pas détecter un piéton = mortel | Latence |

### 4.2 Selon le contexte métier : coût asymétrique des erreurs

La question clé à poser au métier est : **« Qu'est-ce qui coûte le plus cher, un faux positif ou un faux négatif ? »**

| Scénario | FP (fausse alarme) | FN (raté) | Métrique privilégiée |
|---|---|---|---|
| **Cancer** | Examen inutile (~500€) | Mort possible (~∞) | **Recall** |
| **Spam** | Email légitime perdu | Spam dans inbox | **Precision** |
| **Fraude CB** | Carte bloquée à tort | Fraude non détectée (~5000€) | **Recall** (seuil bas) |
| **Embauche** | Candidat refusé à tort | Mauvais recrutement (~50k€) | **Precision** |
| **Assurance** | Prime sous-estimée | Prime surestimée | **MAE symétrique** |

> 💡 **Conseil de pro** : "Demandez TOUJOURS au métier : « Qu'est-ce qui coûte le plus cher, un faux positif ou un faux négatif ? ». La réponse détermine votre métrique. Si le métier ne sait pas, utilisez le F1-Score comme compromis."

> 🧠 **Pour aller plus loin** : "Dans les cas avancés, vous pouvez définir une **matrice de coûts** personnalisée et optimiser directement le coût total. Par exemple : coût_total = nb_FP × coût_FP + nb_FN × coût_FN. Minimiser cette fonction est l'objectif ultime."

---

## 5. ⚙️ Overfitting vs Underfitting

### 5.0 Pour les débutants : l'analogie de l'étudiant

Imaginez 3 étudiants qui préparent un examen de maths :

**L'étudiant qui apprend par cœur (Overfitting)** 🤖
- Il mémorise toutes les réponses des exercices du livre
- Il a 100% sur les exercices déjà faits... mais 30% à l'examen (questions nouvelles)
- Il n'a pas **compris** les règles, il a juste **mémorisé** les exemples

**L'étudiant qui ne travaille pas assez (Underfitting)** 😴
- Il survole le cours sans approfondir
- Il a 50% partout (exercices ET examen)
- Son "modèle mental" est trop **simpliste** pour résoudre les problèmes

**L'étudiant qui comprend (Bon modèle)** 🎯
- Il comprend les concepts et sait les appliquer
- Il a 90% sur les exercices ET 85% à l'examen
- Il **généralise** bien car il a compris les règles sous-jacentes

#### Comment le détecter ?

```
Score train = 99%, Score test = 50%  →  🔴 OVERFITTING (a appris par cœur)
Score train = 55%, Score test = 50%  →  🟡 UNDERFITTING (modèle trop simple)
Score train = 92%, Score test = 88%  →  🟢 BON MODÈLE (généralise bien)
```

> 💡 **Règle simple** : Si le score train est **beaucoup plus élevé** que le score test, c'est de l'overfitting. Si les **deux sont bas**, c'est de l'underfitting.

---

### 5.1 Diagnostic

| Symptôme | Diagnostic | Analogie |
|---|---|---|
| Train score élevé + Test score faible | **Overfitting** (sur-apprentissage) | Apprendre par cœur un examen |
| Train ET Test scores faibles | **Underfitting** (sous-apprentissage) | Ne pas assez étudier |
| Train ≈ Test ≈ élevés | **Bon modèle** | Bien comprendre le cours |

```python
from sklearn.model_selection import learning_curve
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import numpy as np

def tracer_learning_curves(model, X, y, title="Learning Curves", cv=5):
    """Trace les learning curves pour diagnostiquer overfitting/underfitting."""

    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y,
        cv=cv,
        n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='roc_auc',
        random_state=42
    )

    # Moyennes et écarts-types
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    test_mean = test_scores.mean(axis=1)
    test_std = test_scores.std(axis=1)

    plt.figure(figsize=(10, 6))

    # Score d'entraînement
    plt.plot(train_sizes, train_mean, 'b-', linewidth=2, label='Score train')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                     alpha=0.1, color='blue')

    # Score de validation
    plt.plot(train_sizes, test_mean, 'r-', linewidth=2, label='Score validation')
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std,
                     alpha=0.1, color='red')

    plt.xlabel('Taille du jeu d\'entraînement')
    plt.ylabel('Score AUC-ROC')
    plt.title(title)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.ylim(0.5, 1.05)
    plt.tight_layout()
    plt.show()

    # Diagnostic automatique
    gap = train_mean[-1] - test_mean[-1]
    if gap > 0.1:
        print(f"⚠️ OVERFITTING détecté (gap = {gap:.3f})")
        print("   → Simplifier le modèle, plus de données, ou régularisation")
    elif test_mean[-1] < 0.7:
        print(f"⚠️ UNDERFITTING détecté (test score = {test_mean[-1]:.3f})")
        print("   → Modèle plus complexe, feature engineering, moins de régularisation")
    else:
        print(f"✅ Bon équilibre (gap = {gap:.3f}, test score = {test_mean[-1]:.3f})")

# Exemple d'utilisation
rf = RandomForestClassifier(n_estimators=100, random_state=42)
tracer_learning_curves(rf, X_train, y_train, title="Learning Curves - Random Forest")
```

> 💡 **Conseil** : "Tracez TOUJOURS les learning curves. C'est le meilleur outil de diagnostic. En 30 secondes, vous savez si votre problème est l'overfitting, l'underfitting, ou le manque de données."

### 5.2 Solutions à l'overfitting

L'overfitting se produit quand le modèle apprend le **bruit** des données d'entraînement en plus du signal.

| Solution | Description | Quand l'utiliser |
|---|---|---|
| **Plus de données** | Augmenter le dataset | Si possible (le plus efficace) |
| **Régularisation L1/L2** | Pénaliser les poids trop élevés | Régression, SVM, réseaux de neurones |
| **Simplifier le modèle** | Réduire max_depth, min_samples_leaf | Arbres, Random Forest |
| **Sélection de features** | Éliminer les features bruitées | Toujours pertinent |
| **Early stopping** | Arrêter l'entraînement avant convergence | Gradient Boosting, XGBoost |
| **Cross-validation** | Évaluation robuste sur plusieurs folds | Toujours |
| **Dropout** | Désactiver aléatoirement des neurones | Réseaux de neurones |
| **Data augmentation** | Générer des variations des données | Images, texte |
| **Ensemble methods** | Combiner plusieurs modèles | Toujours bénéfique |

```python
# Exemple : réduire l'overfitting d'un Random Forest
from sklearn.ensemble import RandomForestClassifier

# Modèle qui overfit (trop complexe)
rf_overfit = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,        # profondeur illimitée → apprend le bruit
    min_samples_leaf=1,    # feuilles avec 1 seul échantillon
    random_state=42
)
rf_overfit.fit(X_train, y_train)
print(f"Overfitting - Train: {rf_overfit.score(X_train, y_train):.4f}, "
      f"Test: {rf_overfit.score(X_test, y_test):.4f}")

# Modèle régularisé
rf_regularise = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,          # limiter la profondeur
    min_samples_leaf=5,    # au moins 5 échantillons par feuille
    min_samples_split=10,  # au moins 10 pour splitter
    max_features='sqrt',   # sous-ensemble de features
    random_state=42
)
rf_regularise.fit(X_train, y_train)
print(f"Régularisé  - Train: {rf_regularise.score(X_train, y_train):.4f}, "
      f"Test: {rf_regularise.score(X_test, y_test):.4f}")
```

### 5.3 Solutions à l'underfitting

L'underfitting se produit quand le modèle est **trop simple** pour capturer les patterns des données.

| Solution | Description | Quand l'utiliser |
|---|---|---|
| **Modèle plus complexe** | Passer de linéaire à Random Forest/XGBoost | Relation non linéaire |
| **Feature engineering** | Créer de nouvelles features informatives | Toujours (le plus efficace) |
| **Moins de régularisation** | Réduire alpha, C, augmenter max_depth | Si trop régularisé |
| **Plus de features** | Ajouter des variables explicatives | Si données disponibles |
| **Polynomiales** | Ajouter des interactions et termes polynomiaux | Relations non linéaires |
| **Réduire la simplification** | Augmenter max_depth, réduire min_samples_leaf | Arbres trop simples |

> 💡 **Conseil de pro** : "L'underfitting est souvent le signe que vos FEATURES sont insuffisantes, pas que votre modèle est trop simple. Investissez dans le feature engineering avant de complexifier le modèle."

---

## 6. 🔄 Cross-Validation

### 6.0 Pour les débutants : pourquoi ne pas simplement couper en train/test ?

#### Le problème du split unique

Quand vous coupez vos données en train (80%) et test (20%), le résultat **dépend du hasard du découpage**. Si par malchance, tous les cas faciles sont dans le test, le score sera artificiellement élevé.

> **Analogie de l'examen** : Évaluer un étudiant sur UN SEUL examen n'est pas fiable. Il a peut-être eu de la chance ce jour-là. Mieux vaut lui faire passer **5 examens différents** et faire la moyenne.

#### La cross-validation en images

```
Données : [■■■■■|□□□□□|■■■■■|■■■■■|■■■■■]

Fold 1 : [TEST |Train |Train |Train |Train ]  → Score = 0.85
Fold 2 : [Train|TEST  |Train |Train |Train ]  → Score = 0.82
Fold 3 : [Train|Train |TEST  |Train |Train ]  → Score = 0.87
Fold 4 : [Train|Train |Train |TEST  |Train ]  → Score = 0.84
Fold 5 : [Train|Train |Train |Train |TEST  ]  → Score = 0.83

                                     Moyenne = 0.84 (+/- 0.02)
```

Chaque partie sert de test **une et une seule fois**. Le résultat est une **moyenne et un écart-type**, ce qui est beaucoup plus fiable qu'un seul score.

> 💡 **Pour débuter** : Utilisez toujours `cross_val_score` avec `cv=5` pour avoir un résultat fiable. Un seul split train/test peut être trompeur.

La cross-validation est la méthode standard pour évaluer un modèle de manière **robuste et fiable**, en utilisant au mieux les données disponibles.

### 6.1 K-Fold Cross-Validation

Le dataset est divisé en **K parties** (folds). À tour de rôle, chaque fold sert de validation pendant que les K-1 autres servent d'entraînement.

```python
from sklearn.model_selection import cross_val_score, cross_validate

# Cross-validation simple (5-fold)
scores = cross_val_score(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X_train, y_train,
    cv=5,               # 5 folds
    scoring='roc_auc',  # métrique
    n_jobs=-1
)

print(f"Scores par fold : {scores}")
print(f"AUC-ROC moyenne : {scores.mean():.4f} (+/- {scores.std():.4f})")

# Cross-validate avec plusieurs métriques
results = cross_validate(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X_train, y_train,
    cv=5,
    scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
    return_train_score=True,
    n_jobs=-1
)

print("\n=== Résultats détaillés (5-Fold CV) ===")
for metric in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']:
    train_scores = results[f'train_{metric}']
    test_scores = results[f'test_{metric}']
    gap = train_scores.mean() - test_scores.mean()
    print(f"{metric:>12} : Train={train_scores.mean():.4f}, "
          f"Val={test_scores.mean():.4f} (+/- {test_scores.std():.4f}), "
          f"Gap={gap:.4f}")
```

> 💡 **Conseil** : "K=5 est le standard. K=10 pour des datasets plus grands. K=3 si l'entraînement est très lent. Le compromis est : plus de folds = estimation plus fiable mais plus lente."

### 6.2 Stratified K-Fold

Pour les **classes déséquilibrées**, le Stratified K-Fold garantit que chaque fold a la même proportion de classes que le dataset complet.

```python
from sklearn.model_selection import StratifiedKFold

# Stratified K-Fold (préserve les proportions des classes)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores_strat = cross_val_score(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X_train, y_train,
    cv=skf,
    scoring='roc_auc',
    n_jobs=-1
)

print(f"Stratified K-Fold AUC : {scores_strat.mean():.4f} (+/- {scores_strat.std():.4f})")
```

> 💡 **Conseil de pro** : "Utilisez TOUJOURS StratifiedKFold pour la classification, surtout avec des classes déséquilibrées. C'est le comportement par défaut de cross_val_score pour la classification, mais soyez explicite pour plus de clarté."

### 6.3 Leave-One-Out (LOO)

Chaque observation sert de validation une fois, les N-1 autres servent d'entraînement. Utile pour les très petits datasets.

```python
from sklearn.model_selection import LeaveOneOut

# LOO - attention : très lent pour les grands datasets
loo = LeaveOneOut()

# Uniquement pour les petits datasets (< 500 observations)
# scores_loo = cross_val_score(model, X_small, y_small, cv=loo, scoring='accuracy')
```

> ⚠️ **Attention** : "LOO est N fois plus lent qu'un train/test simple. Ne l'utilisez que pour des datasets de moins de 500 observations. Au-delà, K-Fold avec K=10 est suffisant."

### 6.4 Time Series Split

Pour les données temporelles, il est **interdit** de mélanger passé et futur. Le Time Series Split respecte l'ordre chronologique.

```python
from sklearn.model_selection import TimeSeriesSplit

# Time Series Split (respecte l'ordre chronologique)
tscv = TimeSeriesSplit(n_splits=5)

# Visualiser les splits
for i, (train_idx, test_idx) in enumerate(tscv.split(X_train)):
    print(f"Fold {i+1} : Train[{train_idx[0]}:{train_idx[-1]}], "
          f"Test[{test_idx[0]}:{test_idx[-1]}]")

# Utilisation
scores_ts = cross_val_score(
    RandomForestClassifier(n_estimators=100, random_state=42),
    X_train, y_train,
    cv=tscv,
    scoring='roc_auc',
    n_jobs=-1
)

print(f"\nTime Series CV AUC : {scores_ts.mean():.4f} (+/- {scores_ts.std():.4f})")
```

> ⚠️ **Attention** : "JAMAIS de K-Fold standard sur des séries temporelles ! Cela crée un data leakage temporel : le modèle voit le futur pendant l'entraînement. Les résultats seront trompeusement bons mais le modèle échouera en production."

### 6.5 Résumé des méthodes de cross-validation

| Méthode | Quand l'utiliser | Nombre d'entraînements | Stabilité |
|---|---|---|---|
| **K-Fold** | Cas général | K (5-10) | Bonne |
| **Stratified K-Fold** | Classes déséquilibrées | K (5-10) | Très bonne |
| **Leave-One-Out** | Très petit dataset (<500) | N | Excellente mais lente |
| **Time Series Split** | Données temporelles | K (5-10) | Bonne (respecte le temps) |
| **Repeated K-Fold** | Haute fiabilité requise | K × R | Excellente |
| **Group K-Fold** | Groupes à ne pas séparer | K | Bonne (pas de leakage) |

---

## 7. ⚙️ Hyperparameter Tuning

### 7.1 GridSearchCV

Recherche **exhaustive** de toutes les combinaisons d'hyperparamètres.

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_leaf': [1, 2, 5]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1,
    return_train_score=True
)

grid_search.fit(X_train, y_train)

print(f"Meilleurs paramètres : {grid_search.best_params_}")
print(f"Meilleur AUC (CV) : {grid_search.best_score_:.4f}")

# Vérifier l'overfitting
best_idx = grid_search.best_index_
train_score = grid_search.cv_results_['mean_train_score'][best_idx]
test_score = grid_search.cv_results_['mean_test_score'][best_idx]
print(f"Train score : {train_score:.4f}")
print(f"Val score   : {test_score:.4f}")
print(f"Gap         : {train_score - test_score:.4f}")
```

### 7.2 RandomizedSearchCV

Recherche **aléatoire** dans des distributions d'hyperparamètres. Plus efficace pour de grands espaces de recherche.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_distributions = {
    'n_estimators': randint(50, 500),
    'max_depth': randint(3, 30),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': uniform(0.1, 0.9)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions=param_distributions,
    n_iter=50,       # 50 combinaisons aléatoires
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

random_search.fit(X_train, y_train)
print(f"Meilleurs paramètres : {random_search.best_params_}")
print(f"Meilleur AUC (CV) : {random_search.best_score_:.4f}")
```

### 7.3 Optimisation bayésienne (introduction)

L'optimisation bayésienne utilise un **modèle probabiliste** (Gaussian Process) pour guider la recherche vers les régions prometteuses de l'espace des hyperparamètres.

```python
# Installation : uv add scikit-optimize
# from skopt import BayesSearchCV
# from skopt.space import Integer, Real

# Exemple conceptuel (nécessite scikit-optimize)
# bayes_search = BayesSearchCV(
#     RandomForestClassifier(random_state=42),
#     search_spaces={
#         'n_estimators': Integer(50, 500),
#         'max_depth': Integer(3, 30),
#         'min_samples_leaf': Integer(1, 10),
#         'max_features': Real(0.1, 0.9)
#     },
#     n_iter=30,
#     cv=5,
#     scoring='roc_auc',
#     n_jobs=-1,
#     random_state=42
# )
```

> 💡 **Conseil de pro** : "Le tuning des hyperparamètres donne généralement 2-5% d'amélioration. Le feature engineering en donne 10-30%. Ne passez pas 3 heures à tuner si vos features sont médiocres. L'ordre d'investissement : données propres > features > algorithme > tuning."

---

## 8. 📈 Méthodologie complète d'amélioration

### La checklist ultime pour améliorer un modèle

Cette checklist doit être suivie **dans l'ordre**. La plupart des data scientists sautent directement aux étapes 7-10 alors que le problème se trouve aux étapes 1-4.

```
📋 CHECKLIST D'AMÉLIORATION D'UN MODÈLE ML

Étape 1 : ✅ Vérifier les données
   □ Valeurs manquantes identifiées et traitées
   □ Outliers analysés (garder, transformer ou supprimer)
   □ Distribution des features examinée
   □ Pas de data leakage (feature qui "voit" la cible)
   □ Classes équilibrées ou stratégie de gestion définie

Étape 2 : ✅ Établir une baseline
   □ DummyClassifier / DummyRegressor (modèle stupide)
   □ Régression logistique / Régression linéaire (modèle simple)
   □ Métriques de la baseline notées → tout modèle doit faire MIEUX

Étape 3 : ✅ Tester plusieurs algorithmes
   □ Logistic Regression / Linear Regression
   □ Random Forest
   □ XGBoost / Gradient Boosting
   □ Comparer les scores en cross-validation

Étape 4 : ✅ Choisir les bonnes métriques
   □ Métrique alignée avec le coût métier
   □ Pas JUSTE l'accuracy !
   □ classification_report complet
   □ Courbes ROC et Precision-Recall

Étape 5 : ✅ Cross-validation
   □ K-Fold (K=5 minimum)
   □ Stratified pour classes déséquilibrées
   □ TimeSeriesSplit pour données temporelles
   □ Vérifier la stabilité (écart-type entre folds)

Étape 6 : ✅ Learning curves
   □ Diagnostiquer overfitting vs underfitting
   □ Gap train/test < 5% idéalement
   □ Assez de données ?

Étape 7 : ✅ Feature engineering
   □ Nouvelles features (interactions, polynomiales, temporelles)
   □ Connaissance du domaine exploitée
   □ Impact mesuré sur la métrique cible

Étape 8 : ✅ Feature selection
   □ Éliminer les features bruitées
   □ Permutation importance
   □ Corrélation avec la cible (mutual information)

Étape 9 : ✅ Tuning des hyperparamètres
   □ RandomizedSearchCV d'abord (exploration large)
   □ GridSearchCV ensuite (affinage)
   □ Vérifier que le tuning n'overfitte pas

Étape 10 : ✅ Ensemble de modèles
   □ Voting (combiner les prédictions)
   □ Stacking (méta-modèle)
   □ Blending
```

> 💡 **Conseil de pro** : "Suivez cette checklist dans l'ORDRE. La plupart des gens sautent aux étapes 7-10 alors que le problème est aux étapes 1-4. Un bon data scientist passe 80% de son temps sur les données (étapes 1-2) et 20% sur les modèles."

### Comparaison de l'impact de chaque étape

| Étape | Amélioration typique | Effort | Priorité |
|---|---|---|---|
| Données propres (étape 1) | 10-30% | Élevé | Critique |
| Bonne métrique (étape 4) | N/A (change la perspective) | Faible | Critique |
| Feature engineering (étape 7) | 10-30% | Élevé | Très haute |
| Algorithme approprié (étape 3) | 5-15% | Moyen | Haute |
| Cross-validation (étape 5) | Stabilité, pas de score | Faible | Haute |
| Feature selection (étape 8) | 2-10% | Moyen | Moyenne |
| Tuning (étape 9) | 2-5% | Moyen | Moyenne |
| Ensembles (étape 10) | 1-3% | Élevé | Faible |

---

## 9. ✅ Validation finale

### 9.1 Le split train / validation / test

```
Dataset complet
├── 60% Train       → entraîner les modèles
├── 20% Validation  → tuner, comparer, sélectionner
└── 20% Test        → évaluation FINALE (UNE SEULE FOIS)
```

```python
from sklearn.model_selection import train_test_split

# Split en 3 parties
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.25, random_state=42, stratify=y_train_full
)
# 0.25 × 0.8 = 0.2 → 60% train, 20% val, 20% test

print(f"Train      : {len(X_train)} ({len(X_train)/len(X):.0%})")
print(f"Validation : {len(X_val)} ({len(X_val)/len(X):.0%})")
print(f"Test       : {len(X_test)} ({len(X_test)/len(X):.0%})")
```

### 9.2 Le test set ne sert QU'UNE SEULE FOIS

> ⚠️ **Attention** : "Le test set est votre **estimation de la performance en production**. Si vous l'utilisez plusieurs fois pour prendre des décisions (choisir un modèle, tuner des hyperparamètres), ce n'est plus un test set : c'est un validation set, et votre estimation de performance est biaisée. Résultat : votre modèle performera MOINS BIEN en production que ce que le test set indique."

```python
# PROCESSUS CORRECT :
# 1. Entraîner et tuner sur train + validation (ou cross-validation sur train)
# 2. Choisir le meilleur modèle
# 3. Évaluer UNE SEULE FOIS sur le test set
# 4. Rapporter ce score comme performance attendue en production

# Score final sur le test set
best_model = grid_search.best_estimator_
y_pred_final = best_model.predict(X_test)
y_proba_final = best_model.predict_proba(X_test)[:, 1]

print("=== ÉVALUATION FINALE (Test Set) ===")
print(f"Accuracy  : {accuracy_score(y_test, y_pred_final):.4f}")
print(f"Precision : {precision_score(y_test, y_pred_final):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred_final):.4f}")
print(f"F1-Score  : {f1_score(y_test, y_pred_final):.4f}")
print(f"AUC-ROC   : {roc_auc_score(y_test, y_proba_final):.4f}")
print("\n⚠️ Ce score est votre estimation de performance en production.")
print("   Il ne doit PAS être utilisé pour prendre d'autres décisions.")
```

> 💡 **Conseil de pro** : "Si votre score test est significativement inférieur à votre score de cross-validation, vous avez probablement une fuite de données (data leakage) ou vous avez sur-optimisé sur le validation set. Investiguez."

---

## 🎯 Points clés à retenir

1. **La métrique choisie** doit refléter le coût métier de l'erreur
2. **L'accuracy est trompeuse** : ne l'utilisez jamais seule, surtout avec des classes déséquilibrées
3. **RMSE** pour la régression (pénalise les grosses erreurs), **MAE** pour la robustesse
4. **Precision** quand les FP coûtent cher, **Recall** quand les FN coûtent cher, **F1** pour l'équilibre
5. **AUC-ROC** pour évaluer la discrimination, **AUC-PR** pour les classes très déséquilibrées
6. **Learning curves** = outil de diagnostic #1 (overfitting vs underfitting)
7. **Cross-validation** TOUJOURS (K-Fold pour le standard, Stratified pour les classes, TimeSeries pour le temporel)
8. Le **test set** ne sert QU'UNE SEULE FOIS (sinon ce n'est plus un test)
9. **Feature engineering** > tuning (10-30% vs 2-5% d'amélioration)
10. Suivre la **checklist** dans l'ordre : données > baseline > métriques > modèles > tuning

## ✅ Checklist de validation

- [ ] Je sais calculer et interpréter MSE, RMSE, MAE, R², MAPE
- [ ] Je sais lire une matrice de confusion et calculer precision, recall, F1
- [ ] Je comprends pourquoi l'accuracy est trompeuse
- [ ] Je sais tracer et interpréter les courbes ROC et Precision-Recall
- [ ] Je sais choisir la bonne métrique selon le contexte métier
- [ ] Je sais diagnostiquer l'overfitting et l'underfitting avec les learning curves
- [ ] Je maîtrise la cross-validation (K-Fold, Stratified, TimeSeriesSplit)
- [ ] Je sais utiliser GridSearchCV et RandomizedSearchCV
- [ ] Je comprends le protocole train/validation/test
- [ ] Je connais la checklist d'amélioration d'un modèle et son ordre

---

[⬅️ Chapitre 7 : Clustering](07-clustering.md) | [➡️ Chapitre 9 : Feature Engineering](09-feature-engineering.md)
