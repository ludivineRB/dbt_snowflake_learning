# Chapitre 7 : Feature Engineering — L'Art de Préparer les Données

## 🎯 Objectifs

- Comprendre pourquoi les algorithmes ML ne peuvent pas traiter directement des données brutes
- Maîtriser les différentes techniques d'encodage des variables catégorielles
- Savoir quand et comment appliquer la normalisation/standardisation
- Créer de nouvelles features pertinentes à partir des données existantes
- Sélectionner les features les plus informatives pour le modèle
- Construire des pipelines scikit-learn robustes et reproductibles

> 💡 **Conseil** : "Le feature engineering est ce qui sépare un bon data scientist d'un excellent data scientist. Un bon encodage + un bon scaling avec une régression logistique battra souvent un mauvais preprocessing avec un modèle complexe."

---

## 1. 🧠 Pourquoi une Machine ne Comprend pas "Rouge" ou "Paris"

### 1.1 Le problème fondamental

Les algorithmes de Machine Learning travaillent avec des **mathématiques** — des additions, des multiplications, des distances. Ils ne comprennent que les **nombres**.

```
Ce que VOUS voyez dans le dataset :
┌──────────┬─────────┬──────────┬─────────┐
│ Couleur  │ Ville   │ Taille   │ Prix    │
├──────────┼─────────┼──────────┼─────────┤
│ Rouge    │ Paris   │ XL       │ 49.99   │
│ Bleu     │ Lyon    │ M        │ 29.99   │
│ Vert     │ Paris   │ S        │ 19.99   │
└──────────┴─────────┴──────────┴─────────┘

Ce que l'ALGORITHME peut traiter :
┌────────┬────────┬────────┬────────┬────────┬─────────┐
│ c_bleu │ c_vert │ v_lyon │ taille │ prix   │  ...    │
├────────┼────────┼────────┼────────┼────────┼─────────┤
│   0    │   0    │   0    │   3    │ 49.99  │  ...    │
│   1    │   0    │   1    │   2    │ 29.99  │  ...    │
│   0    │   1    │   0    │   1    │ 19.99  │  ...    │
└────────┴────────┴────────┴────────┴────────┴─────────┘
```

### 1.2 Les trois transformations indispensables

| Transformation | Pourquoi | Exemple |
|---------------|----------|---------|
| **Encodage** | Transformer les catégories en nombres | "Rouge" → [1, 0, 0] |
| **Scaling** | Mettre les nombres à la même échelle | Salaire 50000 → 0.5, Âge 35 → 0.5 |
| **Création de features** | Extraire de l'information cachée | Date → jour de semaine, mois, weekend |

> ⚠️ **Attention** : "Si vous passez des données textuelles brutes à un algorithme sklearn, vous obtiendrez une erreur. Le preprocessing n'est pas optionnel — c'est **obligatoire**."

---

## 2. 🏷️ Encodage des Variables Catégorielles

### 2.1 One-Hot Encoding — Les Interrupteurs

#### Le principe visuel

Imaginez un panneau de contrôle avec des **interrupteurs**. Pour chaque catégorie, un interrupteur est soit ON (1) soit OFF (0).

```
Couleur = "Rouge"  →  [Rouge=1, Bleu=0, Vert=0]
Couleur = "Bleu"   →  [Rouge=0, Bleu=1, Vert=0]
Couleur = "Vert"   →  [Rouge=0, Bleu=0, Vert=1]

Visuellement (les interrupteurs) :

Rouge  Bleu   Vert
  ●      ○      ○     → "Rouge"
  ○      ●      ○     → "Bleu"
  ○      ○      ●     → "Vert"

(● = ON = 1, ○ = OFF = 0)
```

#### Quand l'utiliser

| Situation | One-Hot Encoding ? |
|-----------|-------------------|
| Variable **nominale** (pas d'ordre) | ✅ Oui, c'est le choix par défaut |
| Modèles **linéaires** (régression, SVM) | ✅ Oui, indispensable |
| Peu de catégories (< 15-20) | ✅ Oui, pas de problème |
| Beaucoup de catégories (> 50) | ⚠️ Attention, explosion dimensionnelle |
| Arbres de décision | 🤷 Pas nécessaire (mais ne nuit pas) |

#### Le piège : haute cardinalité

```
Ville avec 500 catégories → 500 nouvelles colonnes !
                         → Le dataset devient énorme
                         → Le modèle est lent et peut overfitter
                         → C'est la "curse of dimensionality"
```

#### Implémentation

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# --- Méthode 1 : pd.get_dummies (simple, rapide) ---
df = pd.DataFrame({
    'couleur': ['Rouge', 'Bleu', 'Vert', 'Rouge', 'Bleu'],
    'ville': ['Paris', 'Lyon', 'Paris', 'Marseille', 'Lyon'],
    'prix': [49.99, 29.99, 19.99, 39.99, 24.99]
})

# One-Hot Encoding avec pandas
df_encoded = pd.get_dummies(df, columns=['couleur', 'ville'], drop_first=True)
print("=== pd.get_dummies (drop_first=True) ===")
print(df_encoded)
# drop_first=True : supprime la 1ère catégorie (évite la multicolinéarité)
# Si couleur_Bleu=0 ET couleur_Vert=0 → c'est forcément Rouge
```

```python
# --- Méthode 2 : OneHotEncoder de sklearn (recommandé pour les pipelines) ---
ohe = OneHotEncoder(
    sparse_output=False,        # Retourner un array dense (pas sparse)
    drop='first',               # Supprimer la 1ère catégorie
    handle_unknown='ignore'     # Ignorer les catégories inconnues en production
)

# Fit + Transform
encoded = ohe.fit_transform(df[['couleur', 'ville']])
colonnes = ohe.get_feature_names_out(['couleur', 'ville'])

df_ohe = pd.DataFrame(encoded, columns=colonnes)
print("\n=== OneHotEncoder sklearn ===")
print(df_ohe)
```

> 💡 **Conseil** : "Utilisez `drop='first'` pour éviter la **multicolinéarité** (le piège de la variable factice). Si vous avez 3 couleurs, 2 colonnes suffisent — la 3ème est implicite. C'est important pour les modèles linéaires."

> ⚠️ **Attention** : "En production, votre modèle peut rencontrer des catégories jamais vues à l'entraînement. Utilisez `handle_unknown='ignore'` dans `OneHotEncoder` pour éviter les erreurs — la catégorie inconnue sera encodée comme un vecteur de zéros."

### 2.2 Label Encoding — Transformer en Nombres

#### Le principe

Chaque catégorie reçoit un nombre entier : 0, 1, 2, 3...

```
Paris     →  0
Lyon      →  1
Marseille →  2
```

#### Le danger : créer un ordre artificiel

```
⚠️ Le modèle va interpréter :
   Marseille (2) > Lyon (1) > Paris (0)

   → Il va calculer des distances :
     distance(Paris, Marseille) = 2
     distance(Paris, Lyon) = 1

   → Il va faire des moyennes :
     moyenne(Paris, Marseille) = (0+2)/2 = 1 = Lyon ???

   → C'est ABSURDE pour des variables nominales !
```

#### Quand l'utiliser

| Situation | Label Encoding ? |
|-----------|-----------------|
| Variable **ordinale** (avec un ordre naturel) | ✅ Oui |
| **Arbres de décision** / Random Forest | ✅ Oui (ils gèrent bien) |
| Variable **nominale** | ❌ Non (sauf pour les arbres) |
| Modèles **linéaires**, SVM, KNN | ❌ Non |
| Variable **cible** (target) | ✅ Oui, toujours |

#### Implémentation

```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

# --- LabelEncoder : pour la variable cible ---
le = LabelEncoder()
y_encoded = le.fit_transform(['chat', 'chien', 'oiseau', 'chat', 'oiseau'])
print(f"Encodé : {y_encoded}")           # [0, 1, 2, 0, 2]
print(f"Classes : {le.classes_}")         # ['chat', 'chien', 'oiseau']

# Inverser l'encodage
y_original = le.inverse_transform([0, 1, 2])
print(f"Décodé : {y_original}")           # ['chat', 'chien', 'oiseau']
```

```python
# --- OrdinalEncoder : pour les features ordinales ---
# IMPORTANT : spécifier l'ORDRE des catégories

df_ordinal = pd.DataFrame({
    'taille': ['M', 'S', 'XL', 'L', 'S', 'M'],
    'satisfaction': ['Neutre', 'Mécontent', 'Satisfait', 'Très satisfait', 'Mécontent', 'Satisfait']
})

# Définir l'ordre pour chaque colonne
oe = OrdinalEncoder(categories=[
    ['S', 'M', 'L', 'XL'],                                    # taille
    ['Mécontent', 'Neutre', 'Satisfait', 'Très satisfait']    # satisfaction
])

df_ordinal[['taille_enc', 'satisfaction_enc']] = oe.fit_transform(
    df_ordinal[['taille', 'satisfaction']]
)
print(df_ordinal)
# S→0, M→1, L→2, XL→3
# Mécontent→0, Neutre→1, Satisfait→2, Très satisfait→3
```

### 2.3 Target Encoding — Utiliser l'Information de la Cible

#### Le principe

Remplacer chaque catégorie par la **moyenne de la variable cible** pour cette catégorie.

```
Ville      | Churn moyen  | Target Encoding
-----------|-------------|----------------
Paris      | 0.25        | 0.25
Lyon       | 0.40        | 0.40
Marseille  | 0.15        | 0.15
```

#### Le risque : Data Leakage

```
⚠️  DANGER : le target encoding utilise la variable cible (y) !
    Si vous l'appliquez sur tout le dataset :
    → La feature "voit" directement la target
    → Le modèle "triche" en utilisant la réponse
    → Les performances en train sont artificiellement bonnes
    → En production, les performances s'effondrent
```

#### Implémentation sécurisée

```python
from sklearn.model_selection import KFold
import numpy as np

def target_encoding_cv(df, colonne, target, n_splits=5):
    """
    Target encoding avec cross-validation pour éviter le data leakage.
    Chaque fold utilise les AUTRES folds pour calculer la moyenne.
    """
    df = df.copy()
    df[f'{colonne}_target_enc'] = np.nan

    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    global_mean = df[target].mean()

    for train_idx, val_idx in kf.split(df):
        # Calculer la moyenne sur le fold d'entraînement
        means = df.iloc[train_idx].groupby(colonne)[target].mean()
        # Appliquer sur le fold de validation
        df.loc[df.index[val_idx], f'{colonne}_target_enc'] = (
            df.iloc[val_idx][colonne].map(means)
        )

    # Remplacer les NaN par la moyenne globale
    df[f'{colonne}_target_enc'].fillna(global_mean, inplace=True)
    return df

# Utilisation
df = target_encoding_cv(df, 'ville', 'churn')
print(df[['ville', 'churn', 'ville_target_enc']].head(10))
```

> ⚠️ **Attention** : "Le target encoding est puissant mais dangereux. Utilisez TOUJOURS la version avec cross-validation pour éviter le data leakage. Sans cette précaution, vos performances en validation seront trompeusement bonnes."

### 2.4 Ordinal Encoding — Pour les Variables Ordinales

Les variables ordinales ont un **ordre naturel**. L'encodage doit le respecter.

```python
# Exemples de variables ordinales
variables_ordinales = {
    'niveau_etudes': ['Sans diplôme', 'Bac', 'Licence', 'Master', 'Doctorat'],
    'satisfaction': ['Très mécontent', 'Mécontent', 'Neutre', 'Satisfait', 'Très satisfait'],
    'tranche_age': ['18-25', '26-35', '36-45', '46-55', '56+'],
    'priorite': ['Basse', 'Moyenne', 'Haute', 'Critique']
}

from sklearn.preprocessing import OrdinalEncoder

# Encoder en respectant l'ordre
oe = OrdinalEncoder(categories=[variables_ordinales['niveau_etudes']])
df['niveau_etudes_enc'] = oe.fit_transform(df[['niveau_etudes']])
# Sans diplôme→0, Bac→1, Licence→2, Master→3, Doctorat→4
```

### 2.5 Tableau récapitulatif des encodages

| Encodage | Type de variable | Crée un ordre ? | Nb colonnes | Risque principal | Modèles compatibles |
|----------|-----------------|----------------|-------------|-----------------|-------------------|
| **One-Hot** | Nominale | Non | N-1 | Haute cardinalité | Tous |
| **Label** | Target / Ordinale | Oui | 1 | Faux ordre | Arbres |
| **Ordinal** | Ordinale | Oui (contrôlé) | 1 | Aucun si bien fait | Tous |
| **Target** | Nominale haute cardinalité | Non | 1 | Data leakage | Tous |
| **Frequency** | Nominale | Non | 1 | Catégories de même fréquence | Tous |

---

## 3. 📐 Scaling / Normalisation — Mettre les Features à la Même Échelle

### 3.1 Le problème concret

```
Imaginons deux features :

  Salaire :   10 000 ... 100 000  (range = 90 000)
  Âge :       20 ... 70           (range = 50)

Le modèle calcule des distances :
  distance = √( (salaire1 - salaire2)² + (age1 - age2)² )

  Client A : salaire=50000, age=30
  Client B : salaire=51000, age=60

  distance = √( (50000-51000)² + (30-60)² )
           = √( 1000000 + 900 )
           = √1000900
           ≈ 1000.45

  → Le salaire ÉCRASE totalement l'âge !
  → Le modèle "croit" que le salaire est 1000x plus important
  → Mais c'est juste une question d'ÉCHELLE, pas d'importance
```

> 💡 **Conseil** : "Le scaling n'est pas optionnel pour KNN, SVM et les réseaux de neurones. Sans scaling, ces modèles donnent des résultats catastrophiques car ils sont basés sur des calculs de distance."

### 3.2 MinMaxScaler — Remettre entre 0 et 1

**Formule** : `x_norm = (x - min) / (max - min)`

```python
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Données d'exemple
X = np.array([[50000, 30], [80000, 45], [30000, 25], [100000, 60]])

scaler = MinMaxScaler()  # Par défaut : [0, 1]
X_scaled = scaler.fit_transform(X)

print("Avant scaling :")
print(X)
print("\nAprès MinMaxScaler :")
print(X_scaled)
# Salaire : 30000→0.0, 100000→1.0
# Âge :     25→0.0, 60→1.0
```

### 3.3 StandardScaler — Centrer et Réduire (moyenne=0, écart-type=1)

**Formule** : `z = (x - moyenne) / écart-type`

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Après StandardScaler :")
print(X_scaled)
print(f"Moyenne : {X_scaled.mean(axis=0)}")  # ≈ [0, 0]
print(f"Std :     {X_scaled.std(axis=0)}")   # ≈ [1, 1]
```

### 3.4 RobustScaler — Résistant aux Outliers

**Formule** : `x_robust = (x - médiane) / IQR`

```python
from sklearn.preprocessing import RobustScaler

# Données avec un outlier extrême
X_avec_outlier = np.array([[50000, 30], [80000, 45], [30000, 25], [1000000, 60]])

# Comparer les scalers
scaler_standard = StandardScaler()
scaler_robust = RobustScaler()

X_standard = scaler_standard.fit_transform(X_avec_outlier)
X_robust = scaler_robust.fit_transform(X_avec_outlier)

print("StandardScaler (sensible à l'outlier 1M) :")
print(X_standard)
print("\nRobustScaler (résistant à l'outlier 1M) :")
print(X_robust)
```

### 3.5 Tableau comparatif des scalers

| Scaler | Formule | Résultat | Sensible aux outliers ? | Quand l'utiliser |
|--------|---------|---------|------------------------|-----------------|
| **MinMaxScaler** | `(x-min)/(max-min)` | Valeurs dans [0, 1] | **Très sensible** | Besoin de bornes fixes, pas d'outliers |
| **StandardScaler** | `(x-μ)/σ` | Moyenne=0, Std=1 | Sensible | Cas général, distribution ~normale |
| **RobustScaler** | `(x-médiane)/IQR` | Centré sur médiane | **Robuste** | Beaucoup d'outliers |

### 3.6 Impact du scaling sur les modèles

| Modèle | Sensible à l'échelle ? | Scaling nécessaire ? | Pourquoi |
|--------|----------------------|---------------------|---------|
| **KNN** | Très sensible | **Obligatoire** | Calcul de distances |
| **SVM** | Très sensible | **Obligatoire** | Calcul de distances et marges |
| **Régression linéaire** | Partiellement | Recommandé | Interprétation des coefficients |
| **Régression logistique** | Oui | Oui | Convergence du gradient |
| **Réseaux de neurones** | Très sensible | **Obligatoire** | Convergence du gradient |
| **Arbres de décision** | Non | Non | Splits sur des seuils |
| **Random Forest** | Non | Non | Ensemble d'arbres |
| **Gradient Boosting** | Non | Non | Ensemble d'arbres |

> 💡 **Conseil** : "En cas de doute, appliquez `StandardScaler`. Si vos données ont beaucoup d'outliers, passez à `RobustScaler`. Utilisez `MinMaxScaler` uniquement si vous avez besoin de valeurs strictement dans [0, 1] et que vos données n'ont pas d'outliers."

> ⚠️ **Attention** : "Le scaler doit être `fit` sur le **train set uniquement** et `transform` sur le train ET le test set. Si vous faites `fit_transform` sur tout le dataset avant le split → **data leakage** !"

```python
from sklearn.model_selection import train_test_split

# ✅ BON : fit sur le train, transform sur le test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)          # transform SEULEMENT

# ❌ MAUVAIS : fit_transform sur tout le dataset
# scaler.fit_transform(X)  # ← LEAKAGE !
```

---

## 4. ⚙️ Création de Features — Extraire l'Information Cachée

### 4.1 Combinaisons de features existantes

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'prix': [29.99, 149.50, 9.99, 499.00, 74.50],
    'quantite': [2, 1, 5, 1, 3],
    'surface_m2': [45, 120, 30, 200, 75],
    'nb_pieces': [2, 5, 1, 8, 3],
    'revenu_mensuel': [2500, 4500, 1800, 8000, 3200],
    'loyer': [800, 1200, 600, 2500, 950]
})

# --- Ratios ---
df['montant_total'] = df['prix'] * df['quantite']
df['prix_par_m2'] = df['prix'] / df['surface_m2']
df['surface_par_piece'] = df['surface_m2'] / df['nb_pieces']
df['taux_effort_logement'] = df['loyer'] / df['revenu_mensuel']

# --- Transformations mathématiques ---
df['log_prix'] = np.log1p(df['prix'])           # log(1+x) pour gérer les 0
df['sqrt_surface'] = np.sqrt(df['surface_m2'])   # racine carrée
df['prix_carre'] = df['prix'] ** 2               # polynomiale

print(df)
```

> 💡 **Conseil** : "Les ratios sont souvent les features les plus puissantes. Le prix par m2 est plus informatif que le prix seul. Le taux d'effort logement (loyer/revenu) est plus informatif que le loyer seul. Réfléchissez en termes de ratios métier."

### 4.2 Binning — Discrétiser des Variables Continues

```python
# --- Binning par intervalles fixes ---
df['tranche_prix'] = pd.cut(
    df['prix'],
    bins=[0, 20, 100, 500],
    labels=['Pas cher', 'Moyen', 'Cher']
)

# --- Binning par quantiles (même nombre d'observations par bin) ---
df['quantile_revenu'] = pd.qcut(
    df['revenu_mensuel'],
    q=3,
    labels=['Bas', 'Moyen', 'Haut']
)

# --- Binning personnalisé métier ---
def categoriser_age(age):
    if age < 25:
        return 'Jeune'
    elif age < 45:
        return 'Adulte'
    elif age < 65:
        return 'Senior'
    else:
        return 'Retraité'

# df['categorie_age'] = df['age'].apply(categoriser_age)

print(df[['prix', 'tranche_prix', 'revenu_mensuel', 'quantile_revenu']])
```

### 4.3 Features Temporelles

```python
df_time = pd.DataFrame({
    'date_achat': pd.to_datetime([
        '2024-01-15 14:30:00',
        '2024-03-22 09:15:00',
        '2024-07-04 22:45:00',
        '2024-12-25 11:00:00',
        '2024-06-15 16:30:00'
    ])
})

# Features de base
df_time['annee'] = df_time['date_achat'].dt.year
df_time['mois'] = df_time['date_achat'].dt.month
df_time['jour'] = df_time['date_achat'].dt.day
df_time['heure'] = df_time['date_achat'].dt.hour
df_time['jour_semaine'] = df_time['date_achat'].dt.dayofweek  # 0=lundi

# Features dérivées
df_time['est_weekend'] = df_time['jour_semaine'].isin([5, 6]).astype(int)
df_time['est_matin'] = (df_time['heure'] < 12).astype(int)
df_time['trimestre'] = df_time['date_achat'].dt.quarter

# Encodage cyclique (capturer la circularité du temps)
# Janvier (1) et Décembre (12) sont proches, mais 1 et 12 sont loin en nombre
df_time['mois_sin'] = np.sin(2 * np.pi * df_time['mois'] / 12)
df_time['mois_cos'] = np.cos(2 * np.pi * df_time['mois'] / 12)
df_time['heure_sin'] = np.sin(2 * np.pi * df_time['heure'] / 24)
df_time['heure_cos'] = np.cos(2 * np.pi * df_time['heure'] / 24)

print(df_time)
```

> 💡 **Conseil** : "L'encodage cyclique (sin/cos) est crucial pour les heures et les mois. Sans cela, le modèle croit que Décembre (12) et Janvier (1) sont très éloignés alors qu'ils sont consécutifs. Avec sin/cos, les valeurs cycliques sont correctement représentées."

### 4.4 Features Textuelles

```python
df_text = pd.DataFrame({
    'commentaire': [
        'Excellent produit, livraison rapide !',
        'Nul. Produit cassé à la réception.',
        'Correct pour le prix. RAS.',
        'INCROYABLE !!! Le meilleur achat de ma vie !!!',
        'Bof, pas terrible.'
    ]
})

# Features simples mais efficaces
df_text['nb_mots'] = df_text['commentaire'].str.split().str.len()
df_text['nb_caracteres'] = df_text['commentaire'].str.len()
df_text['nb_exclamation'] = df_text['commentaire'].str.count('!')
df_text['nb_points_inter'] = df_text['commentaire'].str.count('\\?')
df_text['nb_majuscules'] = df_text['commentaire'].str.count('[A-Z]')
df_text['ratio_majuscules'] = df_text['nb_majuscules'] / df_text['nb_caracteres']
df_text['longueur_moy_mot'] = df_text['nb_caracteres'] / df_text['nb_mots']

print(df_text)
```

> 💡 **Conseil** : "Ces features textuelles simples sont souvent très prédictives. Un commentaire avec beaucoup de majuscules et de points d'exclamation exprime un sentiment fort (positif ou négatif). Testez-les toujours en complément du TF-IDF."

---

## 5. 🔍 Sélection de Features — Garder l'Essentiel

Trop de features = bruit, overfitting, lenteur. La sélection de features élimine les features inutiles ou redondantes.

### 5.1 Variance Threshold — Supprimer les Features Constantes

```python
from sklearn.feature_selection import VarianceThreshold

# Supprimer les features avec une variance quasi nulle
selector = VarianceThreshold(threshold=0.01)  # variance < 0.01 → supprimée
X_selected = selector.fit_transform(X)

# Quelles features ont été gardées ?
mask = selector.get_support()
features_gardees = [f for f, m in zip(feature_names, mask) if m]
features_supprimees = [f for f, m in zip(feature_names, mask) if not m]

print(f"Features gardées : {len(features_gardees)}")
print(f"Features supprimées (variance trop faible) : {features_supprimees}")
```

### 5.2 Corrélation avec la Target

```python
import pandas as pd
import numpy as np

# Corrélation de chaque feature avec la cible
correlations = df[colonnes_num].corrwith(df['target']).abs().sort_values(ascending=False)

print("=== Corrélation avec la target ===")
print(correlations)

# Garder les features avec |corrélation| > seuil
seuil = 0.05
features_pertinentes = correlations[correlations > seuil].index.tolist()
features_inutiles = correlations[correlations <= seuil].index.tolist()

print(f"\nFeatures pertinentes (|r| > {seuil}) : {features_pertinentes}")
print(f"Features à supprimer (|r| ≤ {seuil}) : {features_inutiles}")
```

### 5.3 Feature Importance (aperçu)

```python
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

# Entraîner un Random Forest pour obtenir l'importance des features
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# Importance des features
importances = pd.Series(rf.feature_importances_, index=feature_names)
importances = importances.sort_values(ascending=True)

# Visualisation
plt.figure(figsize=(10, 8))
importances.plot(kind='barh', color='steelblue')
plt.title("Importance des features (Random Forest)")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()

# Top 10 features
print("Top 10 features les plus importantes :")
print(importances.sort_values(ascending=False).head(10))
```

> 💡 **Conseil** : "L'importance des features du Random Forest est un excellent point de départ pour comprendre quelles features comptent. Mais attention : elle est biaisée en faveur des features à haute cardinalité et des features numériques. Utilisez-la comme un indicateur, pas comme une vérité absolue."

---

## 6. 🔗 Pipelines scikit-learn — Tout Assembler

### 6.1 Pourquoi les Pipelines sont Indispensables

```
SANS Pipeline :                    AVEC Pipeline :
┌─────────────┐                   ┌─────────────────────────┐
│ Imputer     │ → fit_transform   │                         │
├─────────────┤    sur tout ?     │  Pipeline               │
│ Scaler      │ → fit_transform   │  ┌─ Imputer            │
├─────────────┤    sur tout ?     │  ├─ Scaler             │
│ Encoder     │ → fit_transform   │  ├─ Encoder            │
├─────────────┤    sur tout ?     │  └─ Modèle             │
│ Modèle      │                   │                         │
└─────────────┘                   │  .fit(X_train, y_train) │
                                  │  .predict(X_test)       │
❌ Risque de leakage              └─────────────────────────┘
❌ Code fragile                    ✅ Pas de leakage
❌ Non reproductible               ✅ Reproductible
❌ Difficile à déployer            ✅ Un seul objet à sauvegarder
```

### 6.2 ColumnTransformer — Traitement Différencié par Type

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Identifier les colonnes par type
colonnes_num = ['age', 'revenu', 'nb_achats', 'anciennete_mois']
colonnes_cat_nominales = ['ville', 'canal_acquisition']
colonnes_cat_ordinales = ['niveau_etudes']

# --- Transformations pour les colonnes numériques ---
pipeline_num = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# --- Transformations pour les colonnes catégorielles nominales ---
pipeline_cat_nom = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
])

# --- Transformations pour les colonnes catégorielles ordinales ---
pipeline_cat_ord = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OrdinalEncoder(categories=[
        ['Sans diplôme', 'Bac', 'Licence', 'Master', 'Doctorat']
    ]))
])

# --- Combiner avec ColumnTransformer ---
preprocessor = ColumnTransformer(
    transformers=[
        ('num', pipeline_num, colonnes_num),
        ('cat_nom', pipeline_cat_nom, colonnes_cat_nominales),
        ('cat_ord', pipeline_cat_ord, colonnes_cat_ordinales)
    ],
    remainder='drop'  # Supprimer les colonnes non listées
)
```

### 6.3 Pipeline Complet : Preprocessing + Modèle

```python
from sklearn.model_selection import train_test_split, cross_val_score

# Pipeline complet
pipeline_complet = Pipeline([
    ('preprocessing', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=200, random_state=42))
])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Entraîner
pipeline_complet.fit(X_train, y_train)

# Évaluer
score_train = pipeline_complet.score(X_train, y_train)
score_test = pipeline_complet.score(X_test, y_test)
print(f"Score train : {score_train:.4f}")
print(f"Score test  : {score_test:.4f}")

# Cross-validation (plus fiable)
scores_cv = cross_val_score(pipeline_complet, X, y, cv=5, scoring='roc_auc', n_jobs=-1)
print(f"AUC-ROC (5-Fold CV) : {scores_cv.mean():.4f} (+/- {scores_cv.std():.4f})")
```

### 6.4 Tuning du Pipeline avec GridSearchCV

```python
from sklearn.model_selection import GridSearchCV

# Grille d'hyperparamètres
# Syntaxe : 'étape__sous_étape__paramètre'
param_grid = {
    'preprocessing__num__imputer__strategy': ['mean', 'median'],
    'preprocessing__num__scaler': [StandardScaler(), MinMaxScaler()],
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [5, 10, 15, None],
}

grid = GridSearchCV(
    pipeline_complet,
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid.fit(X_train, y_train)

print(f"Meilleurs paramètres : {grid.best_params_}")
print(f"Meilleur AUC-ROC (CV) : {grid.best_score_:.4f}")
print(f"Score sur test set : {grid.score(X_test, y_test):.4f}")
```

### 6.5 Sauvegarder et Charger le Pipeline

```python
import joblib

# Sauvegarder le meilleur pipeline (preprocessing + modèle)
best_pipeline = grid.best_estimator_
joblib.dump(best_pipeline, 'pipeline_churn_v1.joblib')
print("Pipeline sauvegardé : pipeline_churn_v1.joblib")

# Charger en production
pipeline_prod = joblib.load('pipeline_churn_v1.joblib')

# Prédire sur des données brutes (le pipeline fait TOUT)
nouveau_client = pd.DataFrame({
    'age': [35],
    'revenu': [52000],
    'nb_achats': [3],
    'anciennete_mois': [6],
    'ville': ['Paris'],
    'canal_acquisition': ['Web'],
    'niveau_etudes': ['Master']
})

prediction = pipeline_prod.predict(nouveau_client)
proba = pipeline_prod.predict_proba(nouveau_client)[:, 1]
print(f"Prédiction : {'Churn' if prediction[0] else 'Pas de churn'}")
print(f"Probabilité de churn : {proba[0]:.2%}")
```

> 💡 **Conseil** : "En production, vous ne sauvegardez JAMAIS le modèle seul. Vous sauvegardez le **pipeline complet** (imputation + encodage + scaling + modèle). Ainsi, les données brutes entrent directement et les prédictions sortent. Pas besoin de recoder le preprocessing."

---

## 🎯 Points clés à retenir

1. **Les algorithmes ML ne comprennent que les nombres** — tout texte, catégorie ou date doit être transformé en représentation numérique
2. **One-Hot Encoding pour les nominales** — créer des colonnes binaires (interrupteurs), attention à la haute cardinalité (> 50 catégories)
3. **Label/Ordinal Encoding pour les ordinales** — respecter l'ordre naturel des catégories, ne JAMAIS l'utiliser sur du nominal pour les modèles linéaires
4. **Target Encoding avec cross-validation** — puissant pour la haute cardinalité mais risque de data leakage sans précautions
5. **Le scaling est obligatoire pour KNN, SVM et réseaux de neurones** — StandardScaler par défaut, RobustScaler si outliers, MinMaxScaler si besoin de bornes [0,1]
6. **Créer des ratios et combinaisons** — prix/m2, taux d'effort, features temporelles (weekend, mois cyclique) — c'est là que la connaissance métier fait la différence
7. **Sélectionner les features pertinentes** — variance threshold, corrélation, importance RF — trop de features = overfitting
8. **Les Pipelines sklearn sont indispensables** — pas de data leakage, code reproductible, déploiement en un objet
9. **ColumnTransformer pour traiter différemment chaque type** — numériques (impute + scale), catégorielles (impute + encode), ordinales (impute + ordinal encode)
10. **Sauvegarder le pipeline complet**, jamais le modèle seul — en production, les données brutes entrent et les prédictions sortent

---

## ✅ Checklist de validation

- [ ] Je comprends pourquoi les algorithmes ML ne peuvent pas traiter du texte ou des catégories directement
- [ ] Je sais utiliser One-Hot Encoding (pd.get_dummies et OneHotEncoder) avec `drop='first'`
- [ ] Je connais le danger du Label Encoding sur les variables nominales
- [ ] Je sais quand utiliser One-Hot, Label, Ordinal et Target Encoding
- [ ] Je comprends le problème d'échelle entre features et ses conséquences sur KNN/SVM
- [ ] Je sais choisir entre MinMaxScaler, StandardScaler et RobustScaler
- [ ] Je sais créer des features (ratios, binning, temporelles, textuelles)
- [ ] Je sais sélectionner les features pertinentes (variance, corrélation, importance)
- [ ] Je maîtrise Pipeline et ColumnTransformer de scikit-learn
- [ ] Je sais intégrer le tuning (GridSearchCV) dans un pipeline
- [ ] Je sais sauvegarder et charger un pipeline complet avec joblib
- [ ] Je respecte la règle : fit sur le train, transform sur le test — TOUJOURS

---

**Précédent** : [Chapitre 6 : Comprendre ses Données](06-comprendre-donnees.md)

**Suivant** : [Chapitre 8 : Data Leakage — Le Crime Parfait du ML](08-data-leakage.md)
