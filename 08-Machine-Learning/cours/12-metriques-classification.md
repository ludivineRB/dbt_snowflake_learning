# Chapitre 12 : Métriques — Au-delà de l'Accuracy

## 🎯 Objectifs

- Comprendre pourquoi l'accuracy est souvent **trompeuse**
- Maîtriser la matrice de confusion et toutes ses dérivées
- Savoir choisir la **bonne métrique** selon le contexte métier
- Tracer et interpréter les courbes ROC et Precision-Recall
- Comprendre le log-loss et l'importance des probabilités calibrées
- Ajuster le seuil de décision pour optimiser la métrique choisie

> **Phase 4 - Semaine 12**

---

## 1. 🧠 Le piège de l'Accuracy : "Votre modèle a 95% de précision, mais il est nul"

### 1.1 Le scénario qui fait mal

Imaginez : vous travaillez pour une banque. Votre mission : **détecter les transactions frauduleuses**. Sur 10 000 transactions, seulement **100 sont frauduleuses** (1%).

Vous construisez un modèle... qui prédit **toujours "pas de fraude"**. Zéro intelligence, zéro effort.

```
Résultat :
  - 9 900 transactions légitimes prédites "légitime" → ✅ Correct
  - 100 transactions frauduleuses prédites "légitime" → ❌ Raté !

  Accuracy = 9 900 / 10 000 = 99% 🤯
```

**99% d'accuracy** pour un modèle complètement inutile. C'est le paradoxe de l'accuracy sur des **classes déséquilibrées**.

### 1.2 Démonstration en code

```python
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

# --- Simuler le scénario ---
np.random.seed(42)
n_total = 10_000
n_fraudes = 100  # 1% de fraudes

# Réalité
y_true = np.zeros(n_total)
y_true[:n_fraudes] = 1  # Les 100 premières sont des fraudes

# Modèle "stupide" : prédit toujours 0 (pas de fraude)
y_pred_stupide = np.zeros(n_total)

# Modèle "correct" : détecte 80% des fraudes mais a quelques faux positifs
y_pred_correct = np.zeros(n_total)
y_pred_correct[:80] = 1   # Détecte 80 fraudes sur 100
y_pred_correct[200:250] = 1  # 50 faux positifs

print("=== Modèle STUPIDE (toujours 'pas de fraude') ===")
print(f"Accuracy : {accuracy_score(y_true, y_pred_stupide):.2%}")
print(classification_report(y_true, y_pred_stupide, target_names=['Légitime', 'Fraude']))

print("\n=== Modèle CORRECT ===")
print(f"Accuracy : {accuracy_score(y_true, y_pred_correct):.2%}")
print(classification_report(y_true, y_pred_correct, target_names=['Légitime', 'Fraude']))
```

```
=== Modèle STUPIDE ===
Accuracy : 99.00%
              precision    recall  f1-score   support
    Légitime       0.99      1.00      1.00      9900
      Fraude       0.00      0.00      0.00       100

=== Modèle CORRECT ===
Accuracy : 99.30%
              precision    recall  f1-score   support
    Légitime       1.00      0.99      1.00      9900
      Fraude       0.62      0.80      0.70       100
```

> ⚠️ **Attention** : "Le modèle stupide a 99% d'accuracy mais un recall de 0% sur les fraudes. Il ne détecte **aucune** fraude. Ne faites **jamais** confiance à l'accuracy seule sur des données déséquilibrées."

---

## 2. 🔢 La Matrice de Confusion — La base de tout

### 2.1 Comprendre TP, TN, FP, FN

La matrice de confusion croise les **prédictions** du modèle avec la **réalité**.

```
                          PRÉDICTION DU MODÈLE
                    ┌──────────────┬──────────────┐
                    │  Prédit : 0  │  Prédit : 1  │
                    │  (Négatif)   │  (Positif)   │
┌───────────────────┼──────────────┼──────────────┤
│ Réalité : 0       │     TN       │     FP       │
│ (Négatif)         │ Vrai Négatif │ Faux Positif │
│                   │              │ (Type I)     │
├───────────────────┼──────────────┼──────────────┤
│ Réalité : 1       │     FN       │     TP       │
│ (Positif)         │ Faux Négatif │ Vrai Positif │
│                   │ (Type II)    │              │
└───────────────────┴──────────────┴──────────────┘
```

### 2.2 Analogie médicale

Imaginons un test de dépistage pour une maladie :

| Terme | Signification | Analogie médicale |
|-------|--------------|-------------------|
| **TP** (Vrai Positif) | Modèle dit "malade", patient **est** malade | Test détecte la maladie chez un vrai malade |
| **TN** (Vrai Négatif) | Modèle dit "sain", patient **est** sain | Test négatif pour un patient sain |
| **FP** (Faux Positif) | Modèle dit "malade", patient **est** sain | Fausse alerte ! Patient sain inquiété |
| **FN** (Faux Négatif) | Modèle dit "sain", patient **est** malade | Maladie **ratée** ! Danger ! |

> 💡 **Conseil** : "Pour retenir : le **deuxième mot** indique ce que le modèle a **dit**, et le **premier mot** indique s'il a **raison** (Vrai) ou **tort** (Faux)."

### 2.3 Visualisation avec sklearn

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    classification_report
)

# --- Préparer les données ---
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, test_size=0.2, random_state=42, stratify=cancer.target
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# --- Entraîner ---
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s)

# --- Matrice de confusion ---
cm = confusion_matrix(y_test, y_pred)
print("Matrice de confusion :")
print(cm)
print(f"\nTN={cm[0,0]}, FP={cm[0,1]}, FN={cm[1,0]}, TP={cm[1,1]}")

# --- Visualisation ---
fig, ax = plt.subplots(figsize=(8, 6))
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=['Malin', 'Bénin']
)
disp.plot(cmap='Blues', ax=ax, values_format='d')
plt.title('Matrice de Confusion — Cancer du sein')
plt.tight_layout()
plt.show()
```

---

## 3. 📊 Métriques expliquées avec des exemples métiers

### 3.1 Accuracy — Quand l'utiliser (et quand NE PAS)

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
         = Nombre de bonnes prédictions / Total
```

| Utiliser l'accuracy quand... | NE PAS utiliser quand... |
|------------------------------|--------------------------|
| Classes équilibrées (50/50) | Classes déséquilibrées (95/5) |
| Chaque erreur a le même coût | FP et FN ont des coûts différents |
| Cas simple (Iris, MNIST) | Détection fraude, cancer, spam |

### 3.2 Precision — "Quand je dis fraude, j'ai raison combien de fois ?"

```
Precision = TP / (TP + FP)
          = Vrais Positifs / Total des prédictions positives
```

**Question :** Parmi toutes les alertes que le modèle a levées, **combien étaient justifiées** ?

| Contexte | Pourquoi la precision compte |
|----------|------------------------------|
| **Filtre anti-spam** | Un FP = un vrai mail en spam = client furieux |
| **Recommandation** | Un FP = produit non pertinent = perte de confiance |
| **Recrutement** | Un FP = candidat non qualifié reçu en entretien = temps perdu |

### 3.3 Recall (Sensibilité) — "Je détecte combien de vraies fraudes ?"

```
Recall = TP / (TP + FN)
       = Vrais Positifs / Total des vrais positifs réels
```

**Question :** Parmi toutes les vraies fraudes, **combien le modèle en a-t-il détecté** ?

| Contexte | Pourquoi le recall compte |
|----------|--------------------------|
| **Détection cancer** | Un FN = cancer raté = danger de mort |
| **Détection fraude** | Un FN = fraude non détectée = perte financière |
| **Sécurité aérienne** | Un FN = menace non détectée = catastrophe |

> ⚠️ **Attention** : "Precision et Recall sont **antagonistes**. Augmenter l'un fait généralement baisser l'autre. C'est le **trade-off Precision/Recall**."

### 3.4 F1-Score — L'équilibre

```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

Le F1-Score est la **moyenne harmonique** de Precision et Recall. Pourquoi harmonique et pas arithmétique ?

```
Exemple :
  Precision = 0.90, Recall = 0.10

  Moyenne arithmétique = (0.90 + 0.10) / 2 = 0.50  ← Semble OK
  Moyenne harmonique   = 2 * (0.90 * 0.10) / (0.90 + 0.10) = 0.18  ← Pénalise !
```

La moyenne harmonique **pénalise fortement** les déséquilibres. Un F1-Score élevé nécessite que Precision **et** Recall soient tous les deux élevés.

### 3.5 Specificity (Taux de Vrais Négatifs)

```
Specificity = TN / (TN + FP)
            = Vrais Négatifs / Total des vrais négatifs réels
```

**Question :** Parmi toutes les transactions légitimes, combien le modèle en a-t-il correctement identifié comme légitimes ?

### 3.6 Tableau récapitulatif

| Métrique | Formule | Question métier | Priorité quand... |
|----------|---------|-----------------|-------------------|
| **Accuracy** | (TP+TN) / Total | "Quel % de bonnes réponses ?" | Classes équilibrées |
| **Precision** | TP / (TP+FP) | "Mes alertes sont-elles fiables ?" | FP coûteux |
| **Recall** | TP / (TP+FN) | "Je rate combien de cas ?" | FN coûteux |
| **F1** | Harmonic(P, R) | "Quel équilibre P/R ?" | Métrique par défaut |
| **Specificity** | TN / (TN+FP) | "Les négatifs sont-ils bien classés ?" | Beaucoup de négatifs |

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report
)

# Calcul de toutes les métriques
print("=== Métriques détaillées ===")
print(f"Accuracy    : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision   : {precision_score(y_test, y_pred):.4f}")
print(f"Recall      : {recall_score(y_test, y_pred):.4f}")
print(f"F1-Score    : {f1_score(y_test, y_pred):.4f}")

# Specificity (pas directement dans sklearn)
cm = confusion_matrix(y_test, y_pred)
specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
print(f"Specificity : {specificity:.4f}")

# Rapport complet
print("\n=== Rapport complet ===")
print(classification_report(y_test, y_pred, target_names=['Malin', 'Bénin']))
```

---

## 4. 📈 Courbe ROC et AUC

### 4.1 Courbe ROC expliquée pas à pas

La courbe ROC (Receiver Operating Characteristic) trace **TPR vs FPR** pour tous les seuils de décision possibles :

```
  TPR (Recall)
  1.0 │        ╱─────────────── Modèle parfait (AUC = 1.0)
      │      ╱
      │    ╱    ╱── Bon modèle (AUC ~ 0.85)
      │  ╱    ╱
  0.5 │╱    ╱
      │   ╱       ╱── Aléatoire (AUC = 0.5)
      │  ╱      ╱
      │╱      ╱
  0.0 │─────╱
      └──────────────────── FPR (1 - Specificity)
      0.0                 1.0
```

- **TPR** (True Positive Rate) = Recall = TP / (TP + FN)
- **FPR** (False Positive Rate) = FP / (FP + TN) = 1 - Specificity

### 4.2 AUC : interprétation

L'**AUC** (Area Under the Curve) résume la courbe ROC en un seul nombre :

| AUC | Interprétation |
|-----|---------------|
| 1.0 | Modèle parfait |
| 0.9 - 1.0 | Excellent |
| 0.8 - 0.9 | Bon |
| 0.7 - 0.8 | Acceptable |
| 0.5 - 0.7 | Médiocre |
| 0.5 | Aléatoire (aucun pouvoir discriminant) |
| < 0.5 | Pire qu'aléatoire (labels probablement inversés) |

> 💡 **Conseil** : "L'AUC peut être interprétée comme la probabilité que le modèle assigne un score plus élevé à un positif choisi au hasard qu'à un négatif choisi au hasard."

### 4.3 Code complet avec visualisation

```python
from sklearn.metrics import roc_curve, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt

# Obtenir les probabilités
y_proba = model.predict_proba(X_test_s)[:, 1]

# --- Calcul de la courbe ROC ---
fpr, tpr, seuils = roc_curve(y_test, y_proba)
auc_score = roc_auc_score(y_test, y_proba)

# --- Visualisation ---
fig, ax = plt.subplots(figsize=(8, 6))
RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auc_score).plot(ax=ax)
ax.plot([0, 1], [0, 1], 'k--', label='Aléatoire (AUC = 0.5)')
ax.set_title(f'Courbe ROC (AUC = {auc_score:.4f})')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- Comparer plusieurs modèles ---
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

modeles = {
    'Logistique': LogisticRegression(max_iter=1000, random_state=42),
    'Arbre': DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
}

fig, ax = plt.subplots(figsize=(10, 7))
for nom, mod in modeles.items():
    mod.fit(X_train_s, y_train)
    if hasattr(mod, 'predict_proba'):
        y_prob = mod.predict_proba(X_test_s)[:, 1]
    else:
        y_prob = mod.decision_function(X_test_s)
    fpr_m, tpr_m, _ = roc_curve(y_test, y_prob)
    auc_m = roc_auc_score(y_test, y_prob)
    ax.plot(fpr_m, tpr_m, label=f'{nom} (AUC = {auc_m:.3f})')

ax.plot([0, 1], [0, 1], 'k--', label='Aléatoire')
ax.set_xlabel('Taux de Faux Positifs (FPR)')
ax.set_ylabel('Taux de Vrais Positifs (TPR)')
ax.set_title('Comparaison des courbes ROC')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 5. 📉 Courbe Precision-Recall

### 5.1 Pourquoi elle est meilleure que ROC pour les données déséquilibrées

La courbe ROC peut être **trompeuse** quand les classes sont très déséquilibrées. Un modèle médiocre peut afficher un AUC-ROC élevé simplement parce que le TN est énorme.

La courbe **Precision-Recall** est plus informative car elle se concentre uniquement sur la **classe positive** (la classe rare).

```
  Precision
  1.0 │──────╲
      │       ╲        Bon modèle
      │        ╲
  0.5 │         ╲────────
      │                  ╲
      │                   ╲──── Modèle médiocre
  0.0 │
      └──────────────────────── Recall
      0.0                     1.0
```

### 5.2 Average Precision (AP)

L'**Average Precision** résume la courbe Precision-Recall en un nombre. C'est l'aire sous la courbe PR.

```python
from sklearn.metrics import (
    precision_recall_curve, average_precision_score,
    PrecisionRecallDisplay
)

# --- Courbe Precision-Recall ---
precision, recall, seuils_pr = precision_recall_curve(y_test, y_proba)
ap = average_precision_score(y_test, y_proba)

fig, ax = plt.subplots(figsize=(8, 6))
PrecisionRecallDisplay(precision=precision, recall=recall, average_precision=ap).plot(ax=ax)
ax.set_title(f'Courbe Precision-Recall (AP = {ap:.4f})')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Average Precision : {ap:.4f}")
```

> 💡 **Conseil** : "Utilisez la courbe **ROC** quand vos classes sont relativement équilibrées. Utilisez la courbe **Precision-Recall** quand la classe positive est rare (< 10% du dataset)."

---

## 6. 📐 Log-loss : La qualité des probabilités

### 6.1 Pourquoi les probabilités comptent

Tous les modèles ne se valent pas en termes de **calibration des probabilités**. Un modèle qui dit "80% de chance de fraude" devrait avoir raison 80% du temps quand il dit ça.

Le **log-loss** (ou binary cross-entropy) mesure la qualité des probabilités :

```
Log-loss = -1/N * Σ [y_i * log(p_i) + (1 - y_i) * log(1 - p_i)]
```

| Log-loss | Interprétation |
|----------|---------------|
| 0 | Parfait (probabilités 0 ou 1, toujours correctes) |
| < 0.3 | Très bon |
| 0.3 - 0.5 | Correct |
| 0.5 - 1.0 | Médiocre |
| > 1.0 | Mauvais |
| 0.693 | Aléatoire (équivalent à tirer à pile ou face) |

### 6.2 Log-loss vs Accuracy

```python
from sklearn.metrics import log_loss
import numpy as np

# Deux modèles avec la même accuracy mais des probabilités différentes
y_true = np.array([1, 1, 0, 0, 1])

# Modèle A : probabilités confiantes et correctes
y_proba_A = np.array([0.95, 0.90, 0.10, 0.05, 0.85])

# Modèle B : probabilités proches de 0.5 (peu confiant)
y_proba_B = np.array([0.55, 0.60, 0.45, 0.40, 0.55])

# Les deux ont la même accuracy
y_pred_A = (y_proba_A >= 0.5).astype(int)
y_pred_B = (y_proba_B >= 0.5).astype(int)

print(f"Accuracy A : {(y_pred_A == y_true).mean():.2f}")
print(f"Accuracy B : {(y_pred_B == y_true).mean():.2f}")

print(f"Log-loss A : {log_loss(y_true, y_proba_A):.4f}")  # Bas = bon
print(f"Log-loss B : {log_loss(y_true, y_proba_B):.4f}")  # Plus élevé = moins bon
```

> ⚠️ **Attention** : "Le log-loss **pénalise sévèrement** les prédictions confiantes mais fausses. Un modèle qui prédit 0.99 pour un cas qui est en réalité 0 sera lourdement pénalisé."

---

## 7. 📏 Métriques de régression (rappel)

Pour les problèmes de régression, les métriques principales sont :

| Métrique | Formule | Interprétation | Sensible aux outliers ? |
|----------|---------|---------------|------------------------|
| **MSE** | Σ(y - ŷ)² / n | Erreur moyenne au carré | Oui (fortement) |
| **RMSE** | √MSE | MSE dans l'unité originale | Oui |
| **MAE** | Σ\|y - ŷ\| / n | Erreur moyenne absolue | Non (robuste) |
| **R²** | 1 - SS_res/SS_tot | % de variance expliquée | Modérément |
| **MAPE** | Σ\|y - ŷ\|/\|y\| / n * 100 | Erreur en pourcentage | Non |

```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error,
    r2_score, mean_absolute_percentage_error
)
import numpy as np

y_true_reg = np.array([100, 150, 200, 250, 300])
y_pred_reg = np.array([110, 140, 210, 260, 280])

print(f"MSE  : {mean_squared_error(y_true_reg, y_pred_reg):.2f}")
print(f"RMSE : {np.sqrt(mean_squared_error(y_true_reg, y_pred_reg)):.2f}")
print(f"MAE  : {mean_absolute_error(y_true_reg, y_pred_reg):.2f}")
print(f"R²   : {r2_score(y_true_reg, y_pred_reg):.4f}")
print(f"MAPE : {mean_absolute_percentage_error(y_true_reg, y_pred_reg):.2%}")
```

---

## 8. 🧪 Exercice : Choisir la métrique selon le contexte métier

Pour chaque scénario, identifiez **la métrique principale** à optimiser et **justifiez** votre choix.

### Scénario 1 : Détection de cancer

Un hôpital déploie un modèle de dépistage du cancer du sein sur des mammographies.

> **Réponse :** **Recall** — Il vaut mieux envoyer des patientes saines faire des examens complémentaires (FP) que rater un cancer (FN). Un FN = un cancer non détecté = danger vital.

### Scénario 2 : Filtre anti-spam d'email

Gmail veut filtrer les emails spam pour les déplacer dans le dossier spam.

> **Réponse :** **Precision** — Un FP = un vrai mail important qui finit en spam = client furieux qui rate un rendez-vous, une facture, une offre d'emploi. Un FN = un spam dans la boîte de réception = désagréable mais pas grave.

### Scénario 3 : Détection de fraude bancaire

Une banque veut détecter les transactions frauduleuses en temps réel (0.5% de fraudes).

> **Réponse :** **F1-Score** (avec accent sur le Recall) et courbe **Precision-Recall**. Les fraudes sont rares (classe déséquilibrée), le Recall est crucial (rater une fraude coûte cher), mais trop de faux positifs bloquent les clients (Precision aussi importante).

### Scénario 4 : Reconnaissance de chiffres manuscrits (MNIST)

Reconnaître les chiffres de 0 à 9 écrits à la main.

> **Réponse :** **Accuracy** — Les classes sont relativement équilibrées (10 classes, ~10% chacune), et chaque erreur a le même coût. L'accuracy est pertinente ici.

### Scénario 5 : Prédiction de prix immobiliers

Un site immobilier prédit le prix de vente d'un bien.

> **Réponse :** **MAPE** ou **MAE** — C'est un problème de régression. La MAPE permet de comprendre l'erreur en pourcentage ("on se trompe de 8% en moyenne"). La MAE est robuste aux outliers (villas à plusieurs millions).

---

## 9. 🎚️ Seuil de décision : ajuster pour optimiser

### 9.1 Le principe

Par défaut, sklearn utilise un seuil de **0.5** : si P(positif) >= 0.5, on prédit la classe positive. Mais ce seuil est **arbitraire**.

```
Seuil ↑ (ex: 0.8)
  → On est plus exigeant pour dire "positif"
  → Precision ↑ (moins de faux positifs)
  → Recall ↓ (on rate plus de vrais positifs)

Seuil ↓ (ex: 0.3)
  → On est plus permissif
  → Precision ↓ (plus de faux positifs)
  → Recall ↑ (on détecte plus)
```

### 9.2 Trouver le seuil optimal

```python
from sklearn.metrics import precision_recall_curve, f1_score, roc_curve
import numpy as np
import matplotlib.pyplot as plt

# Probabilités
y_proba = model.predict_proba(X_test_s)[:, 1]

# --- Méthode 1 : Maximiser le F1-Score ---
precisions, recalls, seuils = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-10)
seuil_optimal_f1 = seuils[np.argmax(f1_scores)]
print(f"Seuil optimal (max F1) : {seuil_optimal_f1:.3f}")

# --- Méthode 2 : Youden's Index (max TPR - FPR) ---
fpr, tpr, seuils_roc = roc_curve(y_test, y_proba)
youden = tpr - fpr
seuil_optimal_youden = seuils_roc[np.argmax(youden)]
print(f"Seuil optimal (Youden) : {seuil_optimal_youden:.3f}")

# --- Visualiser ---
seuils_test = np.arange(0.05, 0.96, 0.01)
prec_list, rec_list, f1_list = [], [], []

for s in seuils_test:
    y_pred_s = (y_proba >= s).astype(int)
    prec_list.append(precision_score(y_test, y_pred_s, zero_division=0))
    rec_list.append(recall_score(y_test, y_pred_s))
    f1_list.append(f1_score(y_test, y_pred_s))

plt.figure(figsize=(10, 6))
plt.plot(seuils_test, prec_list, 'b-', label='Precision')
plt.plot(seuils_test, rec_list, 'r-', label='Recall')
plt.plot(seuils_test, f1_list, 'g--', linewidth=2, label='F1-Score')
plt.axvline(x=0.5, color='gray', linestyle=':', alpha=0.5, label='Seuil par défaut (0.5)')
plt.axvline(x=seuil_optimal_f1, color='green', linestyle=':', label=f'Seuil optimal = {seuil_optimal_f1:.2f}')
plt.xlabel('Seuil de décision')
plt.ylabel('Score')
plt.title('Precision, Recall et F1 en fonction du seuil')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- Appliquer ---
y_pred_default = (y_proba >= 0.5).astype(int)
y_pred_optimal = (y_proba >= seuil_optimal_f1).astype(int)

print(f"\nSeuil 0.5     → F1 = {f1_score(y_test, y_pred_default):.4f}")
print(f"Seuil optimal → F1 = {f1_score(y_test, y_pred_optimal):.4f}")
```

> 💡 **Conseil** : "En contexte médical, baissez le seuil (ex: 0.3) pour maximiser le recall. En contexte spam, montez le seuil (ex: 0.7) pour maximiser la precision. Le seuil de 0.5 n'est pas une vérité absolue."

---

## 🎯 Points clés à retenir

1. **L'accuracy est trompeuse** sur des classes déséquilibrées — un modèle trivial peut atteindre 99%
2. **La matrice de confusion** est le point de départ de toutes les métriques : TP, TN, FP, FN
3. **Precision** = fiabilité des alertes positives (priorité quand FP coûteux)
4. **Recall** = capacité à détecter tous les cas positifs (priorité quand FN coûteux)
5. **F1-Score** = moyenne harmonique qui pénalise les déséquilibres entre Precision et Recall
6. **AUC-ROC** donne une vue d'ensemble du pouvoir discriminant du modèle
7. **Courbe Precision-Recall** est préférable à ROC quand les classes sont très déséquilibrées
8. **Log-loss** mesure la qualité des probabilités, pas seulement des classes prédites
9. **Le seuil de 0.5 est arbitraire** — adaptez-le au contexte métier
10. **Choisissez la métrique AVANT de modéliser** en fonction du coût des erreurs

---

## ✅ Checklist de validation

- [ ] Je comprends pourquoi l'accuracy est trompeuse sur des classes déséquilibrées
- [ ] Je sais lire et interpréter une matrice de confusion (TP, TN, FP, FN)
- [ ] Je connais la différence entre Precision, Recall et F1-Score
- [ ] Je sais calculer toutes ces métriques avec sklearn
- [ ] Je sais tracer et interpréter une courbe ROC et calculer l'AUC
- [ ] Je sais tracer une courbe Precision-Recall et calculer l'Average Precision
- [ ] Je comprends le log-loss et pourquoi les probabilités calibrées comptent
- [ ] Je sais choisir la bonne métrique selon le contexte métier
- [ ] Je sais ajuster le seuil de décision pour optimiser precision ou recall
- [ ] Je connais les métriques de régression : MSE, RMSE, MAE, R², MAPE

---

**Précédent** : [Chapitre 11 : Réduction de dimensionnalité](11-reduction-dimensionnalite.md)

**Suivant** : [Chapitre 13 : Validation et Généralisation](13-validation-generalisation.md)
