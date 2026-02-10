# Chapitre 8 : Data Leakage — Le Crime Parfait du ML

## 🎯 Objectifs

- Comprendre ce qu'est le data leakage et pourquoi c'est le problème le plus dangereux en ML
- Identifier les différents types de leakage (target, train-test contamination, temporel)
- Détecter le leakage dans un projet ML existant
- Appliquer les bonnes pratiques pour l'éviter systématiquement
- Construire un pipeline scikit-learn robuste qui élimine les risques de leakage

> 💡 **Conseil** : "Le data leakage est responsable de la majorité des modèles qui brillent en développement mais s'effondrent en production. C'est LE piège numéro 1 en Machine Learning."

---

## 1. 🧠 Scénario : "Votre Modèle a 99% de Précision... Mais Ne Marche Pas"

### 1.1 L'histoire (vraie) d'un modèle trop beau pour être vrai

```
Lundi matin, réunion d'équipe :

  Data Scientist : "J'ai un modèle qui prédit le churn avec 99.2% de précision !"
  Manager :        "Incroyable ! Déployons-le en production !"

  Deux semaines plus tard :

  Manager :        "Les prédictions sont catastrophiques... On fait à peine 55%."
  Data Scientist : "Je ne comprends pas, sur mes données de test c'était 99.2%..."

  Que s'est-il passé ?
  → DATA LEAKAGE 🔓
```

### 1.2 Le résultat du leakage

```
Performance en développement vs production :

  Précision (%)
  100 │  ████████████████████████████  99.2%  ← développement (leakage)
      │
   80 │
      │
   60 │  ████████████████  55%  ← production (réalité)
      │
   40 │
      │
   20 │
      │
    0 └──────────────────────────
       Développement    Production

  → Vous avez construit un modèle qui TRICHE pendant l'examen
    mais qui ne sait RIEN quand il est seul face au vrai problème.
```

---

## 2. 🔍 Qu'est-ce que le Data Leakage ?

### 2.1 Définition simple

Le **data leakage** (fuite de données) se produit quand le modèle a accès, pendant l'entraînement, à des **informations qu'il ne devrait pas connaître**. Ces informations "fuient" depuis le futur, depuis le test set, ou depuis la variable cible elle-même.

### 2.2 L'analogie de l'examen

```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│  SANS leakage (situation normale) :                       │
│                                                           │
│    📚 Étudier (train)  →  📝 Passer l'examen (test)      │
│    Avec le cours           Avec des questions nouvelles   │
│                                                           │
│  AVEC leakage (triche) :                                  │
│                                                           │
│    📚 Étudier (train)  →  📝 Passer l'examen (test)      │
│    Avec le cours           Mais en ayant VU les réponses  │
│    + les réponses          → 100% à l'examen              │
│    de l'examen !           → 0% dans la vraie vie         │
│                                                           │
│  Le modèle "réussit" l'examen parce qu'il a triché,      │
│  pas parce qu'il a compris.                               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

> ⚠️ **Attention** : "Le data leakage est particulièrement insidieux parce qu'il donne l'impression que tout va bien. Les métriques sont excellentes, le modèle semble performant. Le problème n'apparaît qu'en production, quand il est trop tard."

---

## 3. 📊 Les Types de Leakage

### 3.1 Target Leakage — La Variable qui Contient Déjà la Réponse

#### Le principe

Une feature contient **directement ou indirectement** l'information de la variable cible. Le modèle n'a pas besoin d'apprendre — il lui suffit de regarder cette feature.

#### Exemple concret : prédire le défaut de paiement

```
Dataset de crédit :

| client | revenu | montant_crédit | crédit_remboursé | défaut |
|--------|--------|---------------|-----------------|--------|
| A      | 3000   | 10000         | Oui             | Non    |
| B      | 2500   | 15000         | Non             | Oui    |
| C      | 4000   | 8000          | Oui             | Non    |

⚠️  La colonne "crédit_remboursé" EST la réponse !
    Si le crédit est remboursé → pas de défaut
    Si le crédit n'est pas remboursé → défaut

    → Le modèle n'a qu'à regarder "crédit_remboursé" pour prédire "défaut"
    → Accuracy = 100% sur le train ET le test
    → Mais en production, on N'A PAS cette info au moment de la prédiction !
```

#### Autres exemples de target leakage

| Feature piégée | Target | Pourquoi c'est du leakage |
|---------------|--------|--------------------------|
| `crédit_remboursé` | Défaut de paiement | C'est la conséquence directe de la target |
| `date_résiliation` | Churn (désabonnement) | Si la date existe, le client a déjà résilié |
| `montant_remboursement` | Fraude | Un remboursement implique une fraude détectée |
| `score_satisfaction_post` | Churn | Mesuré APRÈS le churn, pas avant |
| `traitement_médical` | Diagnostic maladie | On traite APRÈS le diagnostic |

```python
# Comment détecter le target leakage ?
import pandas as pd

# 1. Vérifier les corrélations anormalement élevées avec la target
correlations = df.corrwith(df['target']).abs().sort_values(ascending=False)
print("=== Corrélations avec la target ===")
print(correlations.head(10))

# ⚠️ Si une feature a une corrélation > 0.95 → SUSPECT
suspects = correlations[correlations > 0.95].index.tolist()
if suspects:
    print(f"\n🔴 ALERTE : Features suspectes de leakage : {suspects}")
    print("   → Vérifiez si ces features sont disponibles AU MOMENT de la prédiction")
```

> 💡 **Conseil** : "Pour chaque feature, posez-vous LA question : 'Cette information est-elle disponible au moment où je dois faire la prédiction en production ?' Si la réponse est non → c'est du leakage. Supprimez cette feature."

### 3.2 Train-Test Contamination — Le Preprocessing qui Fuite

#### Le problème

Le preprocessing (scaling, imputation, encodage) est appliqué sur **tout le dataset** avant le split train/test. Le test set "contamine" le train set.

#### Scaler avant de split = ERREUR

```
❌ MAUVAIS (leakage) :

  Dataset complet (100%)
       ↓
  StandardScaler.fit_transform()     ← La moyenne et l'écart-type
       ↓                                sont calculés sur TOUT le dataset
  train_test_split()                    y compris le test set
       ↓
  Modèle.fit(X_train)
       ↓
  Modèle.predict(X_test)    ← Le test a été normalisé avec ses propres stats !
                                Le modèle a "vu" indirectement le test set.
```

```
✅ BON (pas de leakage) :

  Dataset complet (100%)
       ↓
  train_test_split()                 ← Split D'ABORD
       ↓                    ↓
  X_train                X_test
       ↓
  StandardScaler.fit_transform()     ← Moyenne et écart-type
       ↓                                calculés sur le TRAIN seulement
  X_train_scaled
                         ↓
  StandardScaler.transform()         ← Transform avec les stats du TRAIN
       ↓
  X_test_scaled
```

#### Démonstration en code

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

np.random.seed(42)
X = np.random.randn(1000, 10)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# ❌ MAUVAIS : scaler AVANT split
scaler_mauvais = StandardScaler()
X_scaled_mauvais = scaler_mauvais.fit_transform(X)  # Leakage !
X_train_m, X_test_m, y_train, y_test = train_test_split(
    X_scaled_mauvais, y, test_size=0.2, random_state=42
)
model_m = LogisticRegression()
model_m.fit(X_train_m, y_train)
score_mauvais = accuracy_score(y_test, model_m.predict(X_test_m))

# ✅ BON : split AVANT scaler
X_train_b, X_test_b, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler_bon = StandardScaler()
X_train_b_scaled = scaler_bon.fit_transform(X_train_b)
X_test_b_scaled = scaler_bon.transform(X_test_b)
model_b = LogisticRegression()
model_b.fit(X_train_b_scaled, y_train)
score_bon = accuracy_score(y_test, model_b.predict(X_test_b_scaled))

print(f"Score AVEC leakage    : {score_mauvais:.4f}")
print(f"Score SANS leakage    : {score_bon:.4f}")
print(f"Différence : {abs(score_mauvais - score_bon):.4f}")
print("\n⚠️ La différence semble faible ici, mais sur des données réelles")
print("   avec imputation + scaling + encoding, l'écart peut être ÉNORME.")
```

#### fit_transform sur tout le dataset = ERREUR

```python
# ❌ MAUVAIS : imputation sur tout le dataset
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)  # ← La moyenne inclut le test set !
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2)

# ✅ BON : imputation après le split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)  # Moyenne du TRAIN
X_test_imputed = imputer.transform(X_test)          # Appliquer la moyenne du TRAIN
```

> ⚠️ **Attention** : "Cette erreur est la plus fréquente chez les débutants (et même chez certains expérimentés). Chaque étape de preprocessing qui utilise des statistiques (moyenne, écart-type, min, max, fréquences) doit être fit sur le train set UNIQUEMENT."

### 3.3 Temporal Leakage — Utiliser des Données du Futur

#### Le principe

Quand les données ont une dimension temporelle, utiliser des informations du **futur** pour prédire le **passé** est du leakage.

```
Timeline :

  Passé ─────────────────────────── Futur
  │                                    │
  Jan  Fév  Mar  Avr  Mai  Jun  Jul  Aoû
  ──────────────────────────────────────
  │         Train         │    Test     │
  └───────────────────────┘             │
                                        │
  ⚠️ Si une feature utilise des données de Juil-Aoû
     pour prédire Mar-Avr → LEAKAGE TEMPOREL !
```

#### Exemples

```python
# ❌ MAUVAIS : split aléatoire sur des données temporelles
X_train, X_test = train_test_split(df, test_size=0.2, random_state=42)
# → Des données de Janvier peuvent être dans le test set
#   et des données de Décembre dans le train set
#   → Le modèle utilise le futur pour prédire le passé

# ✅ BON : split temporel (respecter la chronologie)
df = df.sort_values('date')
split_date = '2024-06-01'
X_train = df[df['date'] < split_date]
X_test = df[df['date'] >= split_date]

# Ou avec un pourcentage
split_index = int(len(df) * 0.8)
X_train = df.iloc[:split_index]
X_test = df.iloc[split_index:]
```

```python
# ❌ MAUVAIS : moyenne glissante qui inclut le futur
df['moyenne_7j'] = df['ventes'].rolling(window=7, center=True).mean()
# center=True → utilise 3 jours avant ET 3 jours APRÈS

# ✅ BON : moyenne glissante qui n'utilise que le passé
df['moyenne_7j'] = df['ventes'].rolling(window=7, min_periods=1).mean()
# Par défaut, rolling utilise les 7 jours PRÉCÉDENTS
```

> 💡 **Conseil** : "Pour les données temporelles, utilisez TOUJOURS un split temporel (pas aléatoire). Et pour les lag features / rolling averages, vérifiez bien que vous n'utilisez que des données du passé."

---

## 4. 🕵️ Cas Concrets de Leakage — 5 Scénarios Piégés

### Scénario 1 : La Feature qui "Triche"

```python
# === SCÉNARIO 1 : Feature qui contient la réponse ===

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Dataset de prédiction de churn
np.random.seed(42)
n = 1000
df = pd.DataFrame({
    'age': np.random.randint(18, 70, n),
    'anciennete_mois': np.random.randint(1, 120, n),
    'nb_appels_support': np.random.randint(0, 20, n),
    'montant_mensuel': np.random.normal(50, 20, n),
    'date_resiliation': [None] * 700 + [f'2024-{np.random.randint(1,13):02d}-01' for _ in range(300)],
    'churn': [0] * 700 + [1] * 300
})

# La feature "date_resiliation" EST la réponse déguisée
# Si date_resiliation est remplie → le client a résilié → churn = 1

# Créer une feature à partir de date_resiliation
df['a_date_resiliation'] = df['date_resiliation'].notna().astype(int)

# Entraîner avec la feature piégée
X = df[['age', 'anciennete_mois', 'nb_appels_support', 'montant_mensuel', 'a_date_resiliation']]
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
score_piege = accuracy_score(y_test, model.predict(X_test))
print(f"🔴 Score AVEC feature piégée : {score_piege:.4f}")  # ~1.0

# Importance des features
importances = pd.Series(model.feature_importances_, index=X.columns)
print(f"\nImportance des features :")
print(importances.sort_values(ascending=False))
# a_date_resiliation sera largement en tête → SUSPECT !

# Entraîner SANS la feature piégée
X_propre = df[['age', 'anciennete_mois', 'nb_appels_support', 'montant_mensuel']]
X_train, X_test, y_train, y_test = train_test_split(X_propre, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)
score_propre = accuracy_score(y_test, model.predict(X_test))
print(f"\n✅ Score SANS feature piégée : {score_propre:.4f}")
```

### Scénario 2 : Preprocessing Avant Split

```python
# === SCÉNARIO 2 : Preprocessing avant split ===

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# Dataset avec des valeurs manquantes
np.random.seed(42)
X = np.random.randn(500, 5)
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# Introduire des manquantes
mask = np.random.random(X.shape) < 0.1
X[mask] = np.nan

# ❌ MAUVAIS : imputer + scaler avant split
imputer = SimpleImputer(strategy='mean')
scaler = StandardScaler()

X_bad = imputer.fit_transform(X)    # Moyenne calculée sur TOUT (leakage)
X_bad = scaler.fit_transform(X_bad)  # Stats calculées sur TOUT (leakage)

X_train_bad, X_test_bad, y_train, y_test = train_test_split(
    X_bad, y, test_size=0.2, random_state=42
)

model = LogisticRegression()
model.fit(X_train_bad, y_train)
score_bad = model.score(X_test_bad, y_test)
print(f"❌ Score AVEC leakage (preprocessing avant split) : {score_bad:.4f}")

# ✅ BON : split d'abord, puis preprocessing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

imputer = SimpleImputer(strategy='mean')
scaler = StandardScaler()

X_train_good = imputer.fit_transform(X_train)
X_test_good = imputer.transform(X_test)

X_train_good = scaler.fit_transform(X_train_good)
X_test_good = scaler.transform(X_test_good)

model = LogisticRegression()
model.fit(X_train_good, y_train)
score_good = model.score(X_test_good, y_test)
print(f"✅ Score SANS leakage (split avant preprocessing) : {score_good:.4f}")
```

### Scénario 3 : Information du Futur

```python
# === SCÉNARIO 3 : Utiliser des données du futur ===

# Dataset de ventes quotidiennes
dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
np.random.seed(42)
df_ventes = pd.DataFrame({
    'date': dates,
    'ventes': np.random.poisson(100, len(dates)) + np.arange(len(dates)) * 0.1,
    'temperature': np.random.normal(15, 10, len(dates))
})

# ❌ MAUVAIS : utiliser la moyenne du mois (inclut le futur)
df_ventes['ventes_moy_mois'] = df_ventes.groupby(
    df_ventes['date'].dt.month
)['ventes'].transform('mean')
# → La moyenne de janvier inclut TOUS les janviers, même ceux du futur

# ❌ MAUVAIS : rolling centré (inclut le futur)
df_ventes['rolling_centre'] = df_ventes['ventes'].rolling(
    window=7, center=True
).mean()

# ✅ BON : rolling qui ne regarde que le passé
df_ventes['rolling_passe'] = df_ventes['ventes'].rolling(
    window=7, min_periods=1
).mean()

# ✅ BON : lag features (valeurs passées uniquement)
df_ventes['ventes_j-1'] = df_ventes['ventes'].shift(1)
df_ventes['ventes_j-7'] = df_ventes['ventes'].shift(7)

# ✅ BON : expanding mean (moyenne cumulative jusqu'à ce point)
df_ventes['ventes_moy_cumul'] = df_ventes['ventes'].expanding().mean()

print(df_ventes.head(10))
```

### Scénario 4 : Duplication de Données

```python
# === SCÉNARIO 4 : Données dupliquées entre train et test ===

# Si un même client apparaît dans le train ET le test
df_clients = pd.DataFrame({
    'client_id': [1, 1, 1, 2, 2, 3, 3, 3, 3, 4],
    'mois': [1, 2, 3, 1, 2, 1, 2, 3, 4, 1],
    'montant': [100, 120, 130, 200, 220, 50, 55, 60, 65, 300],
    'churn': [0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
})

# ❌ MAUVAIS : split aléatoire par ligne
# Le client 1 peut avoir des lignes dans le train ET le test
# → Le modèle reconnaît le client, pas le pattern

# ✅ BON : split par client (GroupShuffleSplit)
from sklearn.model_selection import GroupShuffleSplit

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(df_clients, groups=df_clients['client_id']))

train = df_clients.iloc[train_idx]
test = df_clients.iloc[test_idx]

print("Clients dans le train :", train['client_id'].unique())
print("Clients dans le test :", test['client_id'].unique())
# Vérifier qu'aucun client n'est dans les deux
assert len(set(train['client_id']) & set(test['client_id'])) == 0
print("✅ Aucun client en commun entre train et test")
```

### Scénario 5 : Agrégation sur Tout le Dataset

```python
# === SCÉNARIO 5 : Agrégation globale avant split ===

# ❌ MAUVAIS : calculer des features agrégées sur TOUT le dataset
df['revenu_moyen_ville'] = df.groupby('ville')['revenu'].transform('mean')
# → La moyenne de Paris inclut des clients du test set !

# ✅ BON : calculer les agrégations APRÈS le split, sur le train uniquement
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calculer les moyennes sur le TRAIN
moyennes_ville = X_train.groupby('ville')['revenu'].mean().to_dict()
global_mean = X_train['revenu'].mean()

# Appliquer sur train ET test
X_train['revenu_moyen_ville'] = X_train['ville'].map(moyennes_ville)
X_test['revenu_moyen_ville'] = X_test['ville'].map(moyennes_ville)

# Gérer les villes inconnues dans le test
X_test['revenu_moyen_ville'].fillna(global_mean, inplace=True)
```

---

## 5. 🔎 Comment Détecter le Leakage

### 5.1 Les signaux d'alerte

```
🚨 SIGNAUX D'ALERTE DE DATA LEAKAGE :

  1. Accuracy anormalement élevée (> 98%)
     → Trop beau pour être vrai = probablement du leakage

  2. Écart énorme entre train et test
     → Train: 99.5%, Test: 99.2% → suspect (pas d'overfitting normal)

  3. Une feature domine toutes les autres
     → Feature importance : 1 feature > 80% → vérifier cette feature

  4. Le modèle simple bat le modèle complexe de loin
     → Logistic Regression: 99% vs Random Forest: 98.5% → suspect

  5. Les performances s'effondrent en production
     → Le signe le plus clair (mais le plus tardif)
```

### 5.2 Checklist de détection

```python
# === CHECKLIST DE DÉTECTION DU LEAKAGE ===

def verifier_leakage(df, target_col, date_col=None):
    """
    Vérifie les signes courants de data leakage.
    """
    print("=" * 60)
    print("🔍 VÉRIFICATION DE DATA LEAKAGE")
    print("=" * 60)

    # 1. Corrélations suspectes avec la target
    print("\n1. Corrélations avec la target :")
    colonnes_num = df.select_dtypes(include=['number']).columns.drop(target_col, errors='ignore')
    if len(colonnes_num) > 0:
        corr = df[colonnes_num].corrwith(df[target_col]).abs().sort_values(ascending=False)
        for feat, val in corr.items():
            if val > 0.95:
                print(f"   🔴 ALERTE : {feat} — corrélation = {val:.4f} (> 0.95)")
            elif val > 0.85:
                print(f"   🟠 SUSPECT : {feat} — corrélation = {val:.4f} (> 0.85)")
        print(f"   Top 5 corrélations :")
        print(f"   {corr.head().to_dict()}")

    # 2. Colonnes qui ressemblent à la target
    print("\n2. Colonnes similaires à la target :")
    for col in df.columns:
        if col == target_col:
            continue
        if df[col].nunique() == df[target_col].nunique():
            overlap = (df[col] == df[target_col]).mean()
            if overlap > 0.9:
                print(f"   🔴 ALERTE : {col} — identique à {target_col} à {overlap:.1%}")

    # 3. Features disponibles uniquement après la target
    if date_col:
        print(f"\n3. Vérification temporelle (colonne date : {date_col}) :")
        print("   → Vérifiez manuellement que les features sont disponibles AVANT la target")

    # 4. Doublons potentiels
    print(f"\n4. Lignes dupliquées : {df.duplicated().sum()}")
    if 'client_id' in df.columns:
        n_total = len(df)
        n_unique = df['client_id'].nunique()
        if n_unique < n_total:
            print(f"   ⚠️ {n_total - n_unique} lignes avec client_id en double "
                  f"→ risque de leakage si split par ligne")

    print("\n" + "=" * 60)

# Utilisation
verifier_leakage(df, target_col='churn', date_col='date_inscription')
```

### 5.3 Vérifier l'importance des features

```python
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# Entraîner un modèle rapide
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Importance des features
importances = pd.Series(rf.feature_importances_, index=X_train.columns)
importances = importances.sort_values(ascending=True)

plt.figure(figsize=(10, 8))
importances.plot(kind='barh')
plt.title("Importance des features — Vérification de leakage")
plt.xlabel("Importance")

# Seuil d'alerte
seuil_alerte = 0.5
for feat, imp in importances.items():
    if imp > seuil_alerte:
        plt.annotate(f'🔴 SUSPECT', xy=(imp, feat), fontsize=10, color='red')

plt.tight_layout()
plt.show()

# Rapport
print("\n=== Analyse des importances ===")
for feat, imp in importances.sort_values(ascending=False).items():
    if imp > 0.5:
        print(f"  🔴 {feat}: {imp:.4f} — TRÈS SUSPECT (> 50%)")
    elif imp > 0.3:
        print(f"  🟠 {feat}: {imp:.4f} — À vérifier (> 30%)")
    else:
        print(f"  ✅ {feat}: {imp:.4f}")
```

### 5.4 Vérifier la timeline des données

```python
# Pour les données temporelles : vérifier que le test est APRÈS le train
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])

    print(f"Date min (train) : {X_train['date'].min()}")
    print(f"Date max (train) : {X_train['date'].max()}")
    print(f"Date min (test)  : {X_test['date'].min()}")
    print(f"Date max (test)  : {X_test['date'].max()}")

    # Vérifier le chevauchement
    overlap = X_test[X_test['date'] <= X_train['date'].max()]
    if len(overlap) > 0:
        print(f"\n🔴 ALERTE : {len(overlap)} lignes du test set sont AVANT "
              f"la fin du train set → leakage temporel possible")
    else:
        print(f"\n✅ Pas de chevauchement temporel")
```

---

## 6. 🛡️ Comment Éviter le Leakage

### 6.1 Règle n.1 : Toujours Split AVANT le Preprocessing

```python
from sklearn.model_selection import train_test_split

# ÉTAPE 1 : Séparer X et y
X = df.drop('target', axis=1)
y = df['target']

# ÉTAPE 2 : Split AVANT tout preprocessing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ÉTAPE 3 : Preprocessing sur le train UNIQUEMENT
# (voir Pipeline ci-dessous)
```

### 6.2 Règle n.2 : Utiliser les Pipelines scikit-learn

Les pipelines **garantissent** qu'il n'y a pas de leakage. Le `fit` est automatiquement appelé uniquement sur les données d'entraînement.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Colonnes par type
colonnes_num = ['age', 'revenu', 'anciennete_mois', 'nb_achats']
colonnes_cat = ['ville', 'canal', 'type_contrat']

# Pipeline numériques
pipe_num = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline catégorielles
pipe_cat = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
])

# ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', pipe_num, colonnes_num),
    ('cat', pipe_cat, colonnes_cat)
])

# Pipeline complet
pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(n_estimators=200, random_state=42))
])

# Utilisation : UNE ligne pour tout
pipeline.fit(X_train, y_train)
score = pipeline.score(X_test, y_test)
print(f"Score (sans leakage, garanti par le pipeline) : {score:.4f}")
```

### 6.3 Règle n.3 : Validation Temporelle pour les Time Series

```python
from sklearn.model_selection import TimeSeriesSplit

# TimeSeriesSplit respecte la chronologie
tscv = TimeSeriesSplit(n_splits=5)

scores = []
for i, (train_idx, test_idx) in enumerate(tscv.split(X)):
    X_train_fold = X.iloc[train_idx]
    X_test_fold = X.iloc[test_idx]
    y_train_fold = y.iloc[train_idx]
    y_test_fold = y.iloc[test_idx]

    pipeline.fit(X_train_fold, y_train_fold)
    score = pipeline.score(X_test_fold, y_test_fold)
    scores.append(score)

    print(f"Fold {i+1}: train [{train_idx[0]}-{train_idx[-1]}] "
          f"→ test [{test_idx[0]}-{test_idx[-1]}] "
          f"→ score = {score:.4f}")

print(f"\nScore moyen : {np.mean(scores):.4f} (+/- {np.std(scores):.4f})")
```

```
Visualisation du TimeSeriesSplit :

Fold 1:  [TRAIN]           [TEST]
Fold 2:  [TRAIN──────]     [TEST]
Fold 3:  [TRAIN────────────][TEST]
Fold 4:  [TRAIN──────────────────][TEST]
Fold 5:  [TRAIN────────────────────────][TEST]

→ Le train grandit à chaque fold
→ Le test est TOUJOURS après le train
→ Pas de leakage temporel !
```

### 6.4 Récapitulatif des bonnes pratiques

| Règle | Mauvaise pratique | Bonne pratique |
|-------|------------------|----------------|
| **Split** | Preprocessing puis split | **Split puis preprocessing** |
| **Scaling** | `fit_transform` sur tout | `fit` sur train, `transform` sur test |
| **Imputation** | Moyenne de tout le dataset | Moyenne du **train set** |
| **Encoding** | Target encoding global | Target encoding avec **CV** |
| **Time series** | Split aléatoire | Split **temporel** |
| **Doublons** | Split par ligne | Split par **groupe** (client) |
| **Features** | Toutes les colonnes | Vérifier la **disponibilité en production** |
| **Agrégations** | Sur tout le dataset | Sur le **train set** uniquement |

---

## 7. 🏋️ TP : Chasse au Leakage — Dataset Piégé avec 5 Erreurs

### 7.1 Contexte

Vous recevez un notebook d'un collègue qui a construit un modèle de prédiction de churn. Son modèle affiche 98.7% de précision. Votre mission : **trouver les 5 erreurs de leakage**.

### 7.2 Le code piégé (trouvez les 5 erreurs)

```python
# === CODE PIÉGÉ — TROUVEZ LES 5 ERREURS ===

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Charger les données
df = pd.read_csv("clients_churn.csv")

# --- Erreur 1 : ??? ---
# Créer une feature à partir de la date de résiliation
df['a_resilie'] = df['date_resiliation'].notna().astype(int)

# --- Erreur 2 : ??? ---
# Calculer le revenu moyen par ville (sur tout le dataset)
df['revenu_moyen_ville'] = df.groupby('ville')['revenu'].transform('mean')

# --- Erreur 3 : ??? ---
# Imputer les valeurs manquantes (avant le split)
imputer = SimpleImputer(strategy='mean')
df[['age', 'revenu', 'anciennete']] = imputer.fit_transform(
    df[['age', 'revenu', 'anciennete']]
)

# --- Erreur 4 : ??? ---
# Standardiser (avant le split)
scaler = StandardScaler()
df[['age', 'revenu', 'anciennete']] = scaler.fit_transform(
    df[['age', 'revenu', 'anciennete']]
)

# Séparer features et target
X = df.drop('churn', axis=1)
y = df['churn']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Erreur 5 : ??? ---
# Le dataset contient plusieurs lignes par client
# et le split est fait par ligne, pas par client

# Entraîner
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")  # 98.7% !
```

### 7.3 Les 5 erreurs expliquées

```python
# === CORRECTIONS ===

# Erreur 1 : TARGET LEAKAGE
# 'a_resilie' est directement liée à 'churn' (si résiliation → churn)
# → SOLUTION : supprimer cette feature et 'date_resiliation'
df = df.drop(columns=['date_resiliation'])

# Erreur 2 : AGRÉGATION SUR TOUT LE DATASET
# La moyenne par ville inclut les données du test set
# → SOLUTION : calculer APRÈS le split, sur le train uniquement

# Erreur 3 : IMPUTATION AVANT LE SPLIT
# La moyenne d'imputation utilise le test set
# → SOLUTION : split d'abord, imputer ensuite (fit sur train)

# Erreur 4 : STANDARDISATION AVANT LE SPLIT
# La moyenne et l'écart-type incluent le test set
# → SOLUTION : split d'abord, scaler ensuite (fit sur train)

# Erreur 5 : SPLIT PAR LIGNE (PAS PAR CLIENT)
# Le même client peut être dans le train ET le test
# → SOLUTION : GroupShuffleSplit ou split par client_id
```

### 7.4 Le code corrigé

```python
# === CODE CORRIGÉ — SANS LEAKAGE ===

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score

# Charger les données
df = pd.read_csv("clients_churn.csv")

# ✅ Correction 1 : supprimer les features qui "trichent"
df = df.drop(columns=['date_resiliation'], errors='ignore')

# ✅ Corrections 2-4 : utiliser un Pipeline (pas de preprocessing avant split)
X = df.drop(columns=['churn', 'client_id'])
y = df['churn']
groups = df['client_id']

# ✅ Correction 5 : split par client
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

# Identifier les types de colonnes
colonnes_num = X.select_dtypes(include=['number']).columns.tolist()
colonnes_cat = X.select_dtypes(include=['object', 'category']).columns.tolist()

# ✅ Pipeline robuste (tout le preprocessing est DANS le pipeline)
preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), colonnes_num),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
    ]), colonnes_cat)
])

pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(n_estimators=200, random_state=42))
])

# Entraîner et évaluer
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

score = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy (sans leakage) : {score:.4f}")
# Score réaliste : probablement autour de 70-80%, pas 98.7%
```

---

## 8. 📦 Livrable : Pipeline Scikit-Learn Robuste

### 8.1 Template de Pipeline Anti-Leakage

```python
"""
Template de Pipeline ML Robuste — Anti-Leakage
================================================
Ce template garantit l'absence de data leakage grâce à :
- Split AVANT tout preprocessing
- Tout le preprocessing dans le Pipeline
- ColumnTransformer pour traitement différencié
- Sauvegarde du pipeline complet
"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report
import joblib

# ============================================
# 1. CHARGEMENT ET NETTOYAGE INITIAL
# ============================================
df = pd.read_csv("votre_dataset.csv")

# Supprimer les colonnes identifiant et les features suspectes de leakage
colonnes_a_supprimer = ['id', 'client_id', 'date_resiliation']  # À adapter
df = df.drop(columns=colonnes_a_supprimer, errors='ignore')

# ============================================
# 2. SPLIT AVANT TOUT PREPROCESSING
# ============================================
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train : {len(X_train)} échantillons")
print(f"Test  : {len(X_test)} échantillons")

# ============================================
# 3. IDENTIFIER LES TYPES DE COLONNES
# ============================================
colonnes_num = X.select_dtypes(include=['number']).columns.tolist()
colonnes_cat = X.select_dtypes(include=['object', 'category']).columns.tolist()

print(f"Numériques    : {colonnes_num}")
print(f"Catégorielles : {colonnes_cat}")

# ============================================
# 4. CONSTRUIRE LE PIPELINE
# ============================================
pipe_num = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

pipe_cat = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer([
    ('num', pipe_num, colonnes_num),
    ('cat', pipe_cat, colonnes_cat)
], remainder='drop')

pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(n_estimators=200, random_state=42))
])

# ============================================
# 5. ENTRAÎNER ET ÉVALUER
# ============================================

# Cross-validation
scores_cv = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='roc_auc', n_jobs=-1)
print(f"\nAUC-ROC (5-Fold CV) : {scores_cv.mean():.4f} (+/- {scores_cv.std():.4f})")

# Entraîner le modèle final
pipeline.fit(X_train, y_train)

# Évaluer sur le test set (UNE SEULE FOIS)
y_pred = pipeline.predict(X_test)
print(f"\n=== Rapport sur le test set ===")
print(classification_report(y_test, y_pred))

# ============================================
# 6. SAUVEGARDER LE PIPELINE COMPLET
# ============================================
joblib.dump(pipeline, 'pipeline_robuste_v1.joblib')
print("\n✅ Pipeline sauvegardé : pipeline_robuste_v1.joblib")

# ============================================
# 7. UTILISER EN PRODUCTION
# ============================================
pipeline_prod = joblib.load('pipeline_robuste_v1.joblib')

# Prédiction sur des données brutes
nouvelles_donnees = pd.DataFrame({...})  # données brutes
predictions = pipeline_prod.predict(nouvelles_donnees)
probas = pipeline_prod.predict_proba(nouvelles_donnees)[:, 1]
```

> 💡 **Conseil** : "Ce template est votre point de départ pour TOUT projet ML. Copiez-le, adaptez les colonnes et le modèle, mais ne changez JAMAIS la structure : split → pipeline → évaluation. C'est votre assurance anti-leakage."

---

## 🎯 Points clés à retenir

1. **Le data leakage est le piège n.1 du ML** — il donne des résultats artificiellement bons en développement qui s'effondrent en production
2. **Target leakage** : une feature contient directement ou indirectement la réponse — posez-vous toujours la question "cette info est-elle disponible au moment de la prédiction ?"
3. **Train-test contamination** : le preprocessing (scaling, imputation) est appliqué avant le split — le test set "contamine" le train set via les statistiques calculées
4. **Temporal leakage** : utiliser des données du futur pour prédire le passé — toujours faire un split temporel pour les données time series
5. **Signaux d'alerte** : accuracy > 98%, une feature qui domine à > 50% d'importance, performances qui s'effondrent en production
6. **Règle d'or : split AVANT tout preprocessing** — c'est la règle la plus importante de tout le ML
7. **Les Pipelines sklearn sont la solution** — ils garantissent que le fit se fait uniquement sur le train set
8. **TimeSeriesSplit pour les données temporelles** — le train est toujours avant le test, pas de mélange chronologique
9. **GroupShuffleSplit si données multi-lignes par entité** — un même client ne doit pas être dans le train ET le test
10. **Sauvegarder le pipeline complet** — en production, les données brutes entrent, les prédictions sortent, pas de preprocessing manuel

---

## ✅ Checklist de validation

- [ ] Je sais expliquer ce qu'est le data leakage avec l'analogie de l'examen
- [ ] Je sais identifier un target leakage (feature qui contient la réponse)
- [ ] Je comprends pourquoi scaler/imputer avant le split est du leakage
- [ ] Je connais le problème du leakage temporel et sais utiliser TimeSeriesSplit
- [ ] Je sais détecter le leakage (corrélations suspectes, feature importance, accuracy trop élevée)
- [ ] J'applique la règle : split AVANT tout preprocessing
- [ ] Je sais construire un Pipeline avec ColumnTransformer anti-leakage
- [ ] Je sais utiliser GroupShuffleSplit pour les données multi-lignes par entité
- [ ] J'ai corrigé les 5 erreurs du TP "Chasse au leakage"
- [ ] Je sais sauvegarder et utiliser un pipeline complet en production

---

**Précédent** : [Chapitre 7 : Feature Engineering](07-feature-engineering.md)

**Suivant** : [Chapitre 9 : Feature Engineering Avancé](09-feature-engineering.md)
