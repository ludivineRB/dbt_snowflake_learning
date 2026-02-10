# Chapitre 14 : Interpréter ses Modèles et Éthique du ML

## 🎯 Objectifs

- Comprendre pourquoi l'**interprétabilité** est cruciale (confiance, légal, debug)
- Maîtriser les méthodes d'interprétation : feature importance, permutation, SHAP, PDP
- Savoir expliquer une prédiction individuelle à un non-technique
- Connaître les enjeux **éthiques** du ML : biais, fairness, RGPD
- Appliquer une checklist éthique à tout projet ML

> **Phase 5 - Semaine 14**

---

## 1. 🧠 Pourquoi l'interprétabilité est cruciale

### 1.1 Trois raisons fondamentales

**Raison 1 : La confiance métier**

Le manager ou le directeur financier ne déploiera jamais un modèle qu'il ne comprend pas. "Le modèle a dit non" n'est pas une explication acceptable.

**Raison 2 : Les obligations légales**

Le **RGPD** (Règlement Général sur la Protection des Données) impose un **droit à l'explication** : toute personne affectée par une décision automatisée a le droit de comprendre pourquoi.

```
Article 22 du RGPD :
"La personne concernée a le droit de ne pas faire l'objet d'une
décision fondée exclusivement sur un traitement automatisé [...]
produisant des effets juridiques la concernant."

→ Si un modèle refuse un crédit, le client peut exiger une explication.
```

**Raison 3 : Débugger le modèle**

Une feature importance inattendue révèle souvent un **bug** ou une **fuite de données** :

```
Exemple réel :
  Un modèle de prédiction de pneumonie trouvait que
  l'asthme RÉDUISAIT le risque de décès par pneumonie.

  Pourquoi ? Les patients asthmatiques étaient envoyés
  directement en soins intensifs → meilleure prise en
  charge → moins de décès.

  Le modèle avait appris un biais de sélection,
  pas une relation causale !
```

> ⚠️ **Attention** : "Un modèle performant avec des feature importances illogiques est potentiellement **dangereux**. Toujours vérifier que le modèle apprend les bonnes corrélations."

---

## 2. 📊 Modèles interprétables vs boîtes noires

### 2.1 Le spectre de l'interprétabilité

| Modèle | Interprétabilité | Performance typique | Quand l'utiliser |
|--------|-----------------|---------------------|------------------|
| Régression linéaire | ⭐⭐⭐⭐⭐ | Modérée | Baseline, domaines régulés |
| Arbre de décision | ⭐⭐⭐⭐ | Modérée | Quand l'explication est prioritaire |
| Régression logistique | ⭐⭐⭐⭐ | Modérée | Classification binaire simple |
| Random Forest | ⭐⭐⭐ | Bonne | Bon compromis général |
| Gradient Boosting | ⭐⭐ | Très bonne | Compétitions, performance max |
| Réseau de neurones | ⭐ | Variable | Images, texte, séquences |

```
Interprétabilité ←──────────────────────────→ Performance
  ⭐⭐⭐⭐⭐                                    ⭐⭐⭐⭐⭐

  Régression    Arbre     Random    XGBoost    Deep
  linéaire               Forest               Learning

  "Je comprends  ─────────────────────  "Je ne comprends
   exactement                             rien mais ça
   pourquoi"                              marche bien"
```

### 2.2 Le trade-off performance vs interprétabilité

> 💡 **Conseil** : "En pratique, la différence de performance entre un modèle interprétable et une boîte noire est souvent **faible** (1-2%). Si l'interprétabilité est importante pour votre cas d'usage, ne sacrifiez pas la compréhension pour un gain marginal de performance."

---

## 3. 🔍 Feature Importance globale

### 3.1 Coefficients de la régression linéaire

Les coefficients d'une régression linéaire sont **directement interprétables** :

```python
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Préparer ---
cancer = load_breast_cancer()
X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
y = cancer.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# --- Régression logistique ---
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_s, y_train)

# Coefficients (features standardisées → comparables)
coefs = pd.Series(log_reg.coef_[0], index=cancer.feature_names)
coefs_sorted = coefs.abs().sort_values(ascending=False)

print("=== Top 10 features les plus influentes ===")
for feat in coefs_sorted.head(10).index:
    direction = "↑ bénin" if coefs[feat] > 0 else "↓ malin"
    print(f"  {feat:30s} : coef = {coefs[feat]:+.4f} ({direction})")
```

> 💡 **Conseil** : "Pour que les coefficients soient comparables entre eux, les features doivent être **standardisées** (StandardScaler). Un coefficient de 2.0 sur une feature en mètres n'est pas comparable à un coefficient de 0.001 sur une feature en millimètres."

### 3.2 Feature importance des arbres (MDI)

Les arbres calculent l'importance d'une feature comme la **diminution totale d'impureté** (Mean Decrease in Impurity) qu'elle apporte.

```python
from sklearn.ensemble import RandomForestClassifier

# --- Random Forest ---
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# Feature importance (MDI)
importances = pd.Series(rf.feature_importances_, index=cancer.feature_names)
importances_sorted = importances.sort_values(ascending=True)

# --- Visualisation ---
plt.figure(figsize=(10, 8))
importances_sorted.tail(15).plot(kind='barh', color='steelblue')
plt.xlabel('Importance (MDI)')
plt.title('Feature Importance — Random Forest (Top 15)')
plt.tight_layout()
plt.show()
```

> ⚠️ **Attention** : "La feature importance MDI des arbres est **biaisée** en faveur des features avec beaucoup de valeurs uniques (features continues vs catégorielles). Préférez la **permutation importance** pour une évaluation plus fiable."

### 3.3 Permutation importance (model-agnostic)

La permutation importance mesure la **baisse de performance** quand on mélange aléatoirement les valeurs d'une feature. Si le score baisse beaucoup, la feature est importante.

```python
from sklearn.inspection import permutation_importance

# --- Permutation importance ---
result = permutation_importance(
    rf, X_test, y_test,
    n_repeats=30,          # Répéter 30 fois pour la robustesse
    random_state=42,
    scoring='f1'
)

# Résultats
perm_importance = pd.DataFrame({
    'importance_mean': result.importances_mean,
    'importance_std': result.importances_std,
}, index=cancer.feature_names).sort_values('importance_mean', ascending=True)

# --- Visualisation ---
fig, ax = plt.subplots(figsize=(10, 8))
perm_importance.tail(15)['importance_mean'].plot(
    kind='barh',
    xerr=perm_importance.tail(15)['importance_std'],
    color='coral',
    ax=ax
)
ax.set_xlabel('Baisse de F1 quand la feature est permutée')
ax.set_title('Permutation Importance (Top 15)')
plt.tight_layout()
plt.show()
```

---

## 4. 🎯 SHAP expliqué simplement

### 4.1 Valeurs de Shapley — L'analogie avec les joueurs d'une équipe

Imaginez une équipe de football qui gagne un match. Comment attribuer le mérite à chaque joueur ?

```
Équipe : Joueur A, Joueur B, Joueur C
Score final : 3 buts

La valeur de Shapley de chaque joueur =
  sa contribution MOYENNE au score,
  en considérant TOUTES les coalitions possibles :

  - A seul : marque 1 but
  - B seul : marque 0 but
  - C seul : marque 1 but
  - A + B   : marquent 2 buts
  - A + C   : marquent 2 buts
  - B + C   : marquent 1 but
  - A + B + C : marquent 3 buts

  → Shapley(A) = contribution moyenne de A ≈ 1.17
  → Shapley(B) = contribution moyenne de B ≈ 0.50
  → Shapley(C) = contribution moyenne de C ≈ 1.33
  → Total = 3.0 ✓ (les Shapley values s'additionnent !)
```

En ML, c'est pareil : la valeur SHAP d'une feature mesure sa **contribution à la prédiction** pour UNE observation donnée.

### 4.2 Installation et usage

```python
# Installation
# pip install shap

import shap
from sklearn.ensemble import RandomForestClassifier

# --- Entraîner le modèle ---
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# --- Calculer les SHAP values ---
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# shap_values est une liste de 2 arrays (une par classe)
# shap_values[1] = contributions vers la classe 1 (bénin)
print(f"Shape des SHAP values : {shap_values[1].shape}")
# (n_échantillons, n_features)
```

### 4.3 Visualisations SHAP

#### Summary Plot — Vue globale

```python
# Summary plot : importance ET direction de chaque feature
plt.figure(figsize=(12, 8))
shap.summary_plot(shap_values[1], X_test, feature_names=cancer.feature_names)
```

```
Interprétation du Summary Plot :
  - Chaque point = une observation
  - Axe X = valeur SHAP (contribution à la prédiction)
  - Couleur = valeur de la feature (rouge = élevée, bleu = basse)

  worst concave points  ●●●●●●●|●●●●●●●●●
  worst perimeter       ●●●●●|●●●●●●
  mean concave points   ●●●●|●●●●●
                        ────────┼──────────
                        Pousse  │  Pousse
                        vers    │  vers
                        malin   │  bénin
```

#### Waterfall Plot — Expliquer UNE prédiction

```python
# Expliquer la prédiction pour le patient n°0
idx = 0
print(f"Prédiction : {'Bénin' if rf.predict(X_test.iloc[[idx]])[0] == 1 else 'Malin'}")
print(f"Probabilité bénin : {rf.predict_proba(X_test.iloc[[idx]])[0][1]:.2%}")

# Waterfall plot
shap.plots.waterfall(shap.Explanation(
    values=shap_values[1][idx],
    base_values=explainer.expected_value[1],
    data=X_test.iloc[idx].values,
    feature_names=cancer.feature_names.tolist()
))
```

#### Force Plot — Visualisation compacte

```python
# Force plot pour une prédiction
shap.force_plot(
    explainer.expected_value[1],
    shap_values[1][idx],
    X_test.iloc[idx],
    feature_names=cancer.feature_names.tolist()
)
```

#### Dependence Plot — Relation feature / SHAP value

```python
# Comment "worst perimeter" influence la prédiction
shap.dependence_plot(
    'worst perimeter',
    shap_values[1],
    X_test,
    feature_names=cancer.feature_names.tolist()
)
```

---

## 5. 📈 Partial Dependence Plots (PDP)

### 5.1 Concept

Les PDP montrent l'effet **marginal** d'une feature sur la prédiction, en moyennant l'effet de toutes les autres features.

```
PDP pour "surface" dans un modèle de prix immobilier :

Prix prédit
  500k │                          ╱───
       │                        ╱
  400k │                      ╱
       │                   ╱
  300k │               ╱──
       │            ╱
  200k │        ╱──
       │    ╱──
  100k │╱──
       └────────────────────────── Surface (m²)
       20   40   60   80  100  120  140
```

### 5.2 Code avec sklearn

```python
from sklearn.inspection import PartialDependenceDisplay
from sklearn.ensemble import GradientBoostingClassifier

# --- Entraîner un Gradient Boosting ---
gb = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
gb.fit(X_train, y_train)

# --- PDP pour les 4 features les plus importantes ---
top_features = importances.sort_values(ascending=False).head(4).index.tolist()
top_indices = [list(cancer.feature_names).index(f) for f in top_features]

fig, ax = plt.subplots(figsize=(14, 8))
PartialDependenceDisplay.from_estimator(
    gb, X_train, features=top_indices,
    feature_names=cancer.feature_names,
    ax=ax
)
fig.suptitle('Partial Dependence Plots — Top 4 features')
plt.tight_layout()
plt.show()
```

> 💡 **Conseil** : "Les PDP montrent l'effet **moyen** d'une feature. Ils peuvent être trompeurs si les features sont fortement corrélées. Utilisez les **ICE plots** (Individual Conditional Expectation) pour voir la variabilité entre les observations."

---

## 6. 🔬 LIME (aperçu)

### 6.1 Explication locale avec LIME

LIME (Local Interpretable Model-agnostic Explanations) explique UNE prédiction en créant un **modèle simple local** autour de l'observation.

```
Principe de LIME :

1. Prendre une observation à expliquer
2. Générer des perturbations autour de cette observation
3. Prédire avec le modèle complexe sur ces perturbations
4. Entraîner un modèle simple (régression linéaire)
   sur les perturbations et leurs prédictions
5. Les coefficients du modèle simple = l'explication locale
```

```python
# Installation
# pip install lime

from lime.lime_tabular import LimeTabularExplainer
import numpy as np

# --- Créer l'explainer ---
explainer_lime = LimeTabularExplainer(
    X_train.values,
    feature_names=cancer.feature_names,
    class_names=['Malin', 'Bénin'],
    mode='classification'
)

# --- Expliquer une prédiction ---
idx = 0
explanation = explainer_lime.explain_instance(
    X_test.iloc[idx].values,
    rf.predict_proba,
    num_features=10
)

# Afficher
explanation.show_in_notebook()
# Ou en texte :
print("=== Explication LIME ===")
for feature, weight in explanation.as_list():
    print(f"  {feature:40s} : {weight:+.4f}")
```

### 6.2 LIME vs SHAP

| Critère | LIME | SHAP |
|---------|------|------|
| **Type** | Local (1 prédiction) | Local + Global |
| **Théorie** | Approximation locale | Théorie des jeux (Shapley) |
| **Consistance** | Peut varier entre exécutions | Garanti mathématiquement |
| **Vitesse** | Rapide | Plus lent (exact) |
| **Quand utiliser** | Explication rapide | Explication rigoureuse |

---

## 7. 🧪 TP : Expliquer une décision de crédit à un client

### 7.1 Scénario

Vous travaillez pour une banque. Un client demande un crédit et le modèle le refuse. Le client demande **pourquoi**. Vous devez fournir une explication compréhensible.

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import shap

# --- Simuler un dataset de crédit ---
np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'revenu_annuel': np.random.normal(45000, 15000, n).clip(15000),
    'montant_credit': np.random.normal(15000, 8000, n).clip(1000),
    'duree_emploi_mois': np.random.exponential(48, n).astype(int).clip(0),
    'nb_credits_en_cours': np.random.poisson(1.5, n),
    'taux_endettement': np.random.uniform(0.05, 0.60, n),
    'age': np.random.normal(40, 12, n).clip(18, 75).astype(int),
    'historique_paiement': np.random.choice([0, 1, 2, 3], n, p=[0.6, 0.2, 0.1, 0.1]),
})

# Target : 1 = crédit accordé, 0 = refusé
score = (
    0.3 * (data['revenu_annuel'] > 35000).astype(int) +
    0.2 * (data['taux_endettement'] < 0.35).astype(int) +
    0.2 * (data['duree_emploi_mois'] > 24).astype(int) +
    0.15 * (data['historique_paiement'] == 0).astype(int) +
    0.15 * (data['nb_credits_en_cours'] < 3).astype(int) +
    np.random.normal(0, 0.15, n)
)
data['credit_accorde'] = (score > 0.5).astype(int)

X = data.drop('credit_accorde', axis=1)
y = data['credit_accorde']

# --- Entraîner ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_credit = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=42)
model_credit.fit(X_train, y_train)

# --- Client refusé ---
client_refuse = X_test[model_credit.predict(X_test) == 0].iloc[0]
print("=== Profil du client refusé ===")
for col in X.columns:
    print(f"  {col:25s} : {client_refuse[col]:.2f}")

proba = model_credit.predict_proba(client_refuse.values.reshape(1, -1))[0]
print(f"\nProbabilité d'accord : {proba[1]:.2%}")
print(f"Décision : {'Accordé' if proba[1] > 0.5 else 'REFUSÉ'}")

# --- Explication SHAP ---
explainer = shap.TreeExplainer(model_credit)
shap_values = explainer.shap_values(client_refuse.values.reshape(1, -1))

print("\n=== Explication pour le client ===")
contributions = pd.Series(shap_values[0], index=X.columns)
contributions_sorted = contributions.abs().sort_values(ascending=False)

for feat in contributions_sorted.index:
    val = client_refuse[feat]
    contrib = contributions[feat]
    direction = "FAVORABLE" if contrib > 0 else "DÉFAVORABLE"
    print(f"  {feat:25s} = {val:8.2f} → {direction} (impact : {contrib:+.4f})")
```

**Explication au client** (en langage clair) :

```
"Monsieur, votre demande de crédit a été refusée principalement
pour les raisons suivantes :

1. Votre taux d'endettement (45%) est supérieur au seuil recommandé (35%)
   → C'est le facteur le plus impactant dans la décision.

2. Vous avez 4 crédits en cours, ce qui augmente le risque.

3. Votre ancienneté dans votre emploi actuel (6 mois) est considérée
   comme insuffisante pour ce montant de crédit.

Pour améliorer vos chances :
- Réduisez votre taux d'endettement en remboursant un crédit existant
- Attendez d'avoir au moins 2 ans d'ancienneté dans votre emploi"
```

---

## 8. ⚖️ Éthique et Fairness

### 8.1 Biais dans les données — Exemples célèbres

**Amazon (2018) :** Un outil de recrutement par IA entraîné sur 10 ans de données pénalisait les candidates **femmes**. Les données historiques reflétaient le biais de l'industrie tech, majoritairement masculine.

**COMPAS (2016) :** Un algorithme de prédiction de récidive criminelle utilisé par la justice américaine donnait des scores de risque **plus élevés** aux personnes noires qu'aux personnes blanches, à profil équivalent.

**Soins de santé (2019) :** Un algorithme utilisé par des hôpitaux américains assignait des scores de risque plus bas aux patients noirs qu'aux patients blancs pour un même niveau de maladie, car il utilisait les **coûts de santé** comme proxy de la maladie (les patients noirs avaient moins accès aux soins, donc des coûts plus bas).

### 8.2 Types de biais

| Type de biais | Description | Exemple |
|---------------|-------------|---------|
| **Biais historique** | Les données reflètent des discriminations passées | Données de recrutement sexistes |
| **Biais de représentation** | Certains groupes sont sous-représentés | Dataset de visages avec 90% de blancs |
| **Biais de mesure** | Les variables proxy capturent des inégalités | Code postal comme proxy de l'ethnie |
| **Biais d'agrégation** | Un modèle unique pour des populations différentes | Même seuil médical pour hommes et femmes |
| **Biais de confirmation** | On cherche des résultats qui confirment nos hypothèses | Sélection de features biaisée |

### 8.3 Disparate Impact

Le **disparate impact** mesure si un modèle traite différemment des groupes protégés (genre, ethnie, age...).

```
Disparate Impact Ratio = P(favorable | groupe défavorisé)
                         ─────────────────────────────────
                         P(favorable | groupe favorisé)

Si le ratio < 0.8 → "Règle des 4/5" → Discrimination potentielle
```

```python
# Exemple : vérifier le disparate impact par genre
def disparate_impact(y_pred, group):
    """Calcule le disparate impact ratio."""
    groups = np.unique(group)
    rates = {}
    for g in groups:
        mask = group == g
        rates[g] = y_pred[mask].mean()

    min_rate = min(rates.values())
    max_rate = max(rates.values())

    ratio = min_rate / max_rate if max_rate > 0 else 0
    return ratio, rates

# Simuler
np.random.seed(42)
y_pred_credit = np.random.choice([0, 1], 1000, p=[0.3, 0.7])
genre = np.random.choice(['H', 'F'], 1000)

# Introduire un biais
y_pred_credit[genre == 'F'] = np.random.choice([0, 1], (genre == 'F').sum(), p=[0.45, 0.55])

ratio, rates = disparate_impact(y_pred_credit, genre)
print(f"Taux d'acceptation par genre : {rates}")
print(f"Disparate Impact Ratio : {ratio:.3f}")
print(f"Discrimination potentielle : {'OUI' if ratio < 0.8 else 'NON'} (seuil = 0.80)")
```

### 8.4 Comment mitiger les biais

| Étape | Action | Détails |
|-------|--------|---------|
| **Avant** | Auditer les données | Vérifier la représentation, les proxy variables |
| **Avant** | Diversifier les données | Collecter des données plus représentatives |
| **Pendant** | Contraintes de fairness | Ajouter des contraintes d'équité dans la loss |
| **Pendant** | Reweighting | Repondérer les échantillons sous-représentés |
| **Après** | Ajuster les seuils | Seuils différents par groupe pour égaliser les taux |
| **Après** | Monitorer | Vérifier les métriques de fairness en production |

### 8.5 Fairness metrics

| Métrique | Définition | Objectif |
|----------|-----------|----------|
| **Demographic Parity** | P(ŷ=1\|A=0) = P(ŷ=1\|A=1) | Même taux de positifs par groupe |
| **Equal Opportunity** | P(ŷ=1\|Y=1,A=0) = P(ŷ=1\|Y=1,A=1) | Même recall par groupe |
| **Equalized Odds** | TPR et FPR égaux entre groupes | Même TPR et FPR par groupe |
| **Predictive Parity** | P(Y=1\|ŷ=1,A=0) = P(Y=1\|ŷ=1,A=1) | Même precision par groupe |

> ⚠️ **Attention** : "Il est mathématiquement **impossible** de satisfaire toutes les métriques de fairness simultanément (théorème d'impossibilité de Chouldechova/Kleinberg). Vous devez **choisir** quelle notion d'équité est la plus pertinente pour votre cas d'usage."

### 8.6 Checklist éthique pour tout projet ML

```
CHECKLIST ÉTHIQUE — À vérifier pour CHAQUE projet ML

DONNÉES
□ Les données sont-elles représentatives de la population cible ?
□ Y a-t-il des groupes sous-représentés ?
□ Des variables proxy pourraient-elles capturer des attributs sensibles ?
□ Les labels sont-ils fiables et non biaisés ?

MODÉLISATION
□ Le modèle est-il suffisamment interprétable pour le cas d'usage ?
□ Les feature importances sont-elles cohérentes avec le domaine métier ?
□ A-t-on testé le modèle sur différents sous-groupes ?
□ Le disparate impact ratio est-il supérieur à 0.8 ?

DÉPLOIEMENT
□ Les personnes affectées peuvent-elles demander une explication ?
□ Existe-t-il un processus de recours humain ?
□ Le modèle est-il monitoré pour détecter les dérives ?
□ Qui est responsable en cas de décision erronée ?

DOCUMENTATION
□ Les choix de modélisation sont-ils documentés ?
□ Les limitations connues sont-elles listées ?
□ Les biais potentiels sont-ils identifiés ?
```

---

## 🎯 Points clés à retenir

1. **L'interprétabilité** n'est pas un luxe : c'est une nécessité légale (RGPD), technique (debug) et métier (confiance)
2. Les **coefficients de régression** sont l'outil d'interprétation le plus simple (features standardisées !)
3. La **permutation importance** est model-agnostic et plus fiable que le MDI des arbres
4. **SHAP** est la méthode de référence : fondée théoriquement (Shapley values) et visuelle
5. Les **PDP** montrent l'effet marginal d'une feature sur la prédiction
6. **LIME** est rapide mais moins rigoureux que SHAP pour les explications locales
7. Les **biais dans les données** se retrouvent dans les modèles — "garbage in, garbage out"
8. Le **disparate impact** (règle des 4/5) est un indicateur simple de discrimination
9. Il est **impossible** de satisfaire toutes les métriques de fairness simultanément
10. Une **checklist éthique** devrait accompagner chaque projet ML en production

---

## ✅ Checklist de validation

- [ ] Je comprends les 3 raisons de l'interprétabilité (confiance, légal, debug)
- [ ] Je sais interpréter les coefficients d'une régression linéaire
- [ ] Je sais calculer et visualiser la feature importance d'un Random Forest
- [ ] Je sais utiliser la permutation importance (model-agnostic)
- [ ] Je sais installer et utiliser SHAP (summary plot, waterfall, force plot)
- [ ] Je sais créer et interpréter un Partial Dependence Plot
- [ ] Je connais LIME et sais quand l'utiliser vs SHAP
- [ ] Je sais expliquer une décision de crédit en langage clair à un client
- [ ] Je connais les exemples célèbres de biais en ML (Amazon, COMPAS)
- [ ] Je sais calculer le disparate impact ratio
- [ ] Je connais les principales fairness metrics et le théorème d'impossibilité
- [ ] Je sais appliquer la checklist éthique à un projet ML

---

**Précédent** : [Chapitre 13 : Validation et Généralisation](13-validation-generalisation.md)

**Suivant** : [Chapitre 15 : Du Notebook à l'API — Mettre en Production](15-notebook-api.md)
