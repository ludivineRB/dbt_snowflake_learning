# Chapitre 6 : Comprendre ses Données — La Vraie Vie des Data

## 🎯 Objectifs

- Identifier et distinguer les différents types de données (numériques, catégorielles, temporelles, texte, booléens)
- Mener une enquête méthodique sur les valeurs manquantes, aberrantes et les corrélations trompeuses
- Maîtriser les stratégies d'imputation adaptées à chaque situation
- Réaliser une EDA (Exploratory Data Analysis) systématique avec pandas-profiling / ydata-profiling
- Appliquer un audit qualité complet sur un dataset réel

> 💡 **Conseil** : "Ce chapitre est le plus important de votre parcours ML. Comprendre ses données, c'est 80% du travail d'un data scientist. Un modèle ne sera jamais meilleur que les données qu'on lui donne."

---

## 1. 🧠 Les Types de Données — Savoir ce qu'on manipule

Avant toute modélisation, il faut **connaître la nature** de chaque variable. Un mauvais diagnostic ici entraîne des erreurs en cascade sur tout le projet.

### 1.1 Vue d'ensemble

```
Types de données
│
├── Numériques
│   ├── Continues (prix, température, poids)
│   └── Discrètes (nombre d'enfants, nombre de pièces)
│
├── Catégorielles
│   ├── Nominales (couleur, pays, profession)
│   └── Ordinales (niveau d'études, satisfaction)
│
├── Temporelles (dates, timestamps, durées)
│
├── Texte (descriptions, commentaires, noms)
│
└── Booléens (oui/non, vrai/faux, 0/1)
```

### 1.2 Numériques : continues vs discrètes

| Type | Définition | Exemples | Opérations possibles |
|------|-----------|----------|---------------------|
| **Continue** | Peut prendre n'importe quelle valeur dans un intervalle | Prix (29.99€), température (36.7°C), taille (1.75m) | Moyenne, médiane, écart-type |
| **Discrète** | Valeurs entières, dénombrables | Nombre d'enfants (0, 1, 2...), nombre de pièces, nombre d'achats | Comptage, mode, distribution |

```python
import pandas as pd
import numpy as np

# Identifier les types numériques
df = pd.read_csv("clients.csv")

# Variables continues vs discrètes
colonnes_numeriques = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"Colonnes numériques : {colonnes_numeriques}")

# Astuce : si le nombre de valeurs uniques est faible → probablement discrète
for col in colonnes_numeriques:
    n_unique = df[col].nunique()
    dtype = "Discrète" if n_unique < 20 else "Continue"
    print(f"  {col}: {n_unique} valeurs uniques → {dtype}")
```

### 1.3 Catégorielles : nominales vs ordinales

| Type | Définition | Exemples | Encodage recommandé |
|------|-----------|----------|---------------------|
| **Nominale** | Pas d'ordre entre les catégories | Couleur (rouge, bleu), pays (France, Espagne), profession | One-Hot Encoding |
| **Ordinale** | Ordre naturel entre les catégories | Niveau d'études (bac, licence, master, doctorat), satisfaction (1-5 étoiles) | Ordinal Encoding |

> ⚠️ **Attention** : "Confondre nominal et ordinal est une erreur classique. Si vous appliquez un Label Encoding sur une variable nominale, le modèle croira qu'il y a un ordre entre les catégories (ex: France=0, Espagne=1, Japon=2 → le modèle pense que Japon > Espagne > France)."

```python
# Identifier les variables catégorielles
colonnes_cat = df.select_dtypes(include=['object', 'category']).columns.tolist()
print(f"Colonnes catégorielles : {colonnes_cat}")

for col in colonnes_cat:
    n_unique = df[col].nunique()
    print(f"  {col}: {n_unique} catégories → {df[col].unique()[:5]}")
```

### 1.4 Temporelles

Les données temporelles sont souvent sous-exploitées. Elles cachent des patterns puissants.

```python
# Convertir en datetime
df['date_inscription'] = pd.to_datetime(df['date_inscription'])

# Vérifier le type
print(df['date_inscription'].dtype)  # datetime64[ns]

# Extraire des informations
print(f"Période couverte : {df['date_inscription'].min()} → {df['date_inscription'].max()}")
print(f"Durée : {(df['date_inscription'].max() - df['date_inscription'].min()).days} jours")
```

### 1.5 Texte

Le texte brut n'est pas directement utilisable par les algorithmes ML. Il faudra le transformer (chapitre Feature Engineering).

```python
# Aperçu des colonnes texte
colonnes_texte = ['description', 'commentaire', 'nom_produit']

for col in colonnes_texte:
    if col in df.columns:
        print(f"\n--- {col} ---")
        print(f"  Longueur moyenne : {df[col].str.len().mean():.0f} caractères")
        print(f"  Nombre de mots moyen : {df[col].str.split().str.len().mean():.0f}")
        print(f"  Exemple : {df[col].iloc[0][:80]}...")
```

### 1.6 Booléens

```python
# Les booléens peuvent être sous différentes formes
# True/False, 0/1, Oui/Non, Y/N

# Identifier les colonnes binaires
for col in df.columns:
    if df[col].nunique() == 2:
        print(f"  {col}: {df[col].unique()} → Booléen potentiel")
```

### 1.7 Diagnostic automatique avec pandas

```python
# Le diagnostic complet en une commande
print("=== Info générale ===")
print(df.info())

print("\n=== Types détectés par pandas ===")
print(df.dtypes.value_counts())

print("\n=== Statistiques descriptives (numériques) ===")
print(df.describe())

print("\n=== Statistiques descriptives (catégorielles) ===")
print(df.describe(include='object'))
```

> 💡 **Conseil** : "Méfiez-vous des types détectés automatiquement par pandas. Un code postal (75001) sera détecté comme numérique, alors que c'est une variable catégorielle. Vérifiez toujours manuellement."

---

## 2. 🔍 Enquête #1 : Les Valeurs Manquantes

Les valeurs manquantes sont le **premier problème** que vous rencontrerez sur un vrai dataset. Avant de les traiter, il faut comprendre **pourquoi** elles sont là.

### 2.1 Pourquoi des données manquent-elles ?

| Cause | Exemple concret | Type statistique |
|-------|----------------|-----------------|
| Capteur cassé | Température non enregistrée pendant 3h | MCAR |
| Refus de répondre | Client qui ne donne pas son revenu | MNAR |
| Erreur de saisie | Champ oublié dans un formulaire | MCAR |
| Donnée non applicable | Nombre d'enfants pour un célibataire sans enfant | MAR |
| Fusion de bases | Colonnes différentes selon les sources | MAR |
| Bug informatique | Fichier corrompu, API en panne | MCAR |

### 2.2 Les trois types de manquantes (expliqués simplement)

```
┌─────────────────────────────────────────────────────────────────┐
│                  TYPES DE VALEURS MANQUANTES                     │
├─────────────┬────────────────────────┬──────────────────────────┤
│    MCAR     │         MAR            │         MNAR             │
│  (Missing   │    (Missing At         │    (Missing Not          │
│  Completely │     Random)            │     At Random)           │
│  At Random) │                        │                          │
├─────────────┼────────────────────────┼──────────────────────────┤
│ Le manque   │ Le manque dépend       │ Le manque dépend         │
│ est TOTALE- │ d'AUTRES variables     │ de la VALEUR ELLE-MÊME   │
│ MENT dû au │ observées              │                          │
│ hasard      │                        │                          │
├─────────────┼────────────────────────┼──────────────────────────┤
│ Capteur en  │ Les jeunes répondent   │ Les hauts revenus ne     │
│ panne aléa- │ moins au sondage       │ déclarent pas leur       │
│ toirement   │ (lié à l'âge)          │ revenu                   │
├─────────────┼────────────────────────┼──────────────────────────┤
│ Traitement: │ Traitement:            │ Traitement:              │
│ Suppression │ Imputation basée sur   │ Le plus DIFFICILE.       │
│ OK si peu   │ les autres variables   │ Modèle spécifique ou     │
│ de données  │ (KNN, régression)      │ variable indicatrice     │
└─────────────┴────────────────────────┴──────────────────────────┘
```

> 💡 **Conseil** : "En pratique, il est souvent difficile de savoir si les données sont MCAR, MAR ou MNAR. La bonne approche : parlez aux gens qui ont collecté les données et essayez de comprendre le processus de collecte."

### 2.3 Détection des valeurs manquantes

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv("clients_churn.csv")

# --- Étape 1 : Vue d'ensemble ---
print("=== Valeurs manquantes par colonne ===")
manquantes = df.isnull().sum()
pct_manquantes = (manquantes / len(df)) * 100

rapport = pd.DataFrame({
    'Nb manquantes': manquantes,
    '% manquantes': pct_manquantes
}).sort_values('% manquantes', ascending=False)

# Afficher uniquement les colonnes avec des manquantes
rapport_filtre = rapport[rapport['Nb manquantes'] > 0]
print(rapport_filtre)
print(f"\nTotal : {df.isnull().sum().sum()} valeurs manquantes "
      f"sur {df.size} ({df.isnull().sum().sum() / df.size * 100:.2f}%)")
```

```python
# --- Étape 2 : Visualisation ---

# Barplot des % de manquantes
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Graphique 1 : Barplot
cols_manquantes = rapport_filtre.index
axes[0].barh(cols_manquantes, rapport_filtre['% manquantes'], color='coral')
axes[0].set_xlabel('% de valeurs manquantes')
axes[0].set_title('Pourcentage de valeurs manquantes par colonne')
axes[0].axvline(x=5, color='green', linestyle='--', label='Seuil 5%')
axes[0].axvline(x=50, color='red', linestyle='--', label='Seuil 50%')
axes[0].legend()

# Graphique 2 : Heatmap des manquantes
axes[1].set_title('Pattern des valeurs manquantes')
sns.heatmap(df[cols_manquantes].isnull(), cbar=True, yticklabels=False, ax=axes[1])

plt.tight_layout()
plt.show()
```

```python
# --- Étape 3 : Corrélation entre les manquantes ---
# Est-ce que les manquantes sont liées entre elles ?

colonnes_avec_nan = df.columns[df.isnull().any()].tolist()
if len(colonnes_avec_nan) > 1:
    matrice_nan = df[colonnes_avec_nan].isnull().corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrice_nan, annot=True, cmap='YlOrRd', vmin=-1, vmax=1)
    plt.title("Corrélation entre les valeurs manquantes")
    plt.show()
```

### 2.4 Stratégies d'imputation

| Stratégie | Quand l'utiliser | Code sklearn | Avantage | Inconvénient |
|-----------|-----------------|-------------|----------|-------------|
| **Suppression de lignes** | < 5% manquantes, MCAR | `df.dropna()` | Simple | Perte de données |
| **Suppression de colonnes** | > 50% manquantes | `df.drop(columns=[...])` | Élimine le problème | Perte d'info |
| **Moyenne** | Numérique, distribution symétrique | `SimpleImputer(strategy='mean')` | Rapide | Sensible aux outliers |
| **Médiane** | Numérique, outliers présents | `SimpleImputer(strategy='median')` | Robuste | Réduit la variance |
| **Mode** | Catégoriel | `SimpleImputer(strategy='most_frequent')` | Adapté | Peut biaiser |
| **KNN** | Relations entre features | `KNNImputer(n_neighbors=5)` | Plus précis | Plus lent |
| **Constante** | Signification métier | `SimpleImputer(strategy='constant')` | Explicite | Ajoute une "catégorie" |
| **Indicatrice** | Garder l'info du manque | Créer colonne `_is_missing` | Conserve l'info | Ajoute des colonnes |

### 2.5 Implémentation complète

```python
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import train_test_split

# ⚠️ TOUJOURS splitter AVANT d'imputer
X = df.drop('churn', axis=1)
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Identifier les types de colonnes ---
colonnes_num = X_train.select_dtypes(include=[np.number]).columns.tolist()
colonnes_cat = X_train.select_dtypes(include=['object', 'category']).columns.tolist()

print(f"Colonnes numériques : {colonnes_num}")
print(f"Colonnes catégorielles : {colonnes_cat}")
```

```python
# --- Imputation des numériques par la médiane ---
imputer_median = SimpleImputer(strategy='median')

# Fit sur le train UNIQUEMENT
X_train[colonnes_num] = imputer_median.fit_transform(X_train[colonnes_num])
# Transform sur le test (sans fit !)
X_test[colonnes_num] = imputer_median.transform(X_test[colonnes_num])

print("Manquantes numériques après imputation :")
print(X_train[colonnes_num].isnull().sum())
```

```python
# --- Imputation des catégorielles par le mode ---
imputer_mode = SimpleImputer(strategy='most_frequent')

X_train[colonnes_cat] = imputer_mode.fit_transform(X_train[colonnes_cat])
X_test[colonnes_cat] = imputer_mode.transform(X_test[colonnes_cat])

print("Manquantes catégorielles après imputation :")
print(X_train[colonnes_cat].isnull().sum())
```

```python
# --- Imputation KNN (plus sophistiquée) ---
# KNN utilise les k voisins les plus proches pour estimer la valeur manquante
imputer_knn = KNNImputer(n_neighbors=5, weights='distance')

# ⚠️ KNNImputer ne fonctionne qu'avec des numériques
X_train_knn = pd.DataFrame(
    imputer_knn.fit_transform(X_train[colonnes_num]),
    columns=colonnes_num,
    index=X_train.index
)
X_test_knn = pd.DataFrame(
    imputer_knn.transform(X_test[colonnes_num]),
    columns=colonnes_num,
    index=X_test.index
)

print("Manquantes après KNN :")
print(X_train_knn.isnull().sum())
```

```python
# --- Astuce : Créer une variable indicatrice AVANT d'imputer ---
# Utile si le fait que la donnée manque EST une information

for col in colonnes_num:
    if X_train[col].isnull().sum() > 0:
        X_train[f'{col}_manquant'] = X_train[col].isnull().astype(int)
        X_test[f'{col}_manquant'] = X_test[col].isnull().astype(int)
        print(f"  Créé : {col}_manquant")
```

> ⚠️ **Attention** : "La règle d'or : fit sur le train, transform sur le test. Si vous faites `fit_transform` sur tout le dataset avant le split, vous avez un **data leakage**. Le modèle 'voit' des informations du test set à travers les moyennes/médianes calculées."

> 💡 **Conseil** : "Si le pourcentage de manquantes dépasse 50%, supprimez la colonne. Entre 5% et 50%, imputez. En dessous de 5%, la suppression de lignes est acceptable. Ce sont des règles de base — adaptez à votre contexte."

---

## 3. 🔍 Enquête #2 : Les Valeurs Aberrantes — Erreur ou Signal ?

Une valeur aberrante (outlier) est un point de données qui s'écarte significativement du reste. La question cruciale : **est-ce une erreur ou une information précieuse ?**

### 3.1 Exemples concrets

| Situation | Valeur | Erreur ou signal ? |
|-----------|--------|-------------------|
| Âge d'un client : 250 ans | 250 | ❌ Erreur de saisie |
| Salaire : 500 000€ | 500 000 | ✅ Signal (PDG, star du foot) |
| Température corporelle : 42°C | 42 | ✅ Signal (fièvre grave) |
| Prix d'un produit : -50€ | -50 | ❌ Erreur (ou remboursement ?) |
| Nombre d'achats/mois : 300 | 300 | ⚠️ Bot ? Client professionnel ? |

### 3.2 Détection par la méthode IQR

```
                   Valeurs normales
              ◄────────────────────────►
    ──────┬────────┬─────────────┬────────┬──────
          │        │             │        │
       borne_inf  Q1    médiane  Q3    borne_sup
          │        │             │        │
          │  1.5×IQR            1.5×IQR  │
          │◄──────►│             │◄──────►│
    ──────┴────────┴─────────────┴────────┴──────
 Outliers                                   Outliers
```

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Méthode IQR ---
def detecter_outliers_iqr(df, colonne):
    """
    Détecte les outliers avec la méthode IQR (Interquartile Range).
    Retourne les outliers, borne inférieure et borne supérieure.
    """
    Q1 = df[colonne].quantile(0.25)
    Q3 = df[colonne].quantile(0.75)
    IQR = Q3 - Q1
    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR

    outliers = df[(df[colonne] < borne_inf) | (df[colonne] > borne_sup)]
    return outliers, borne_inf, borne_sup

# Rapport d'outliers pour chaque colonne numérique
print("=== Rapport des valeurs aberrantes (IQR) ===\n")
for col in colonnes_num:
    outliers, b_inf, b_sup = detecter_outliers_iqr(df, col)
    pct = len(outliers) / len(df) * 100
    print(f"{col}:")
    print(f"  Bornes : [{b_inf:.2f}, {b_sup:.2f}]")
    print(f"  Outliers : {len(outliers)} ({pct:.1f}%)")
    if len(outliers) > 0:
        print(f"  Min outlier : {outliers[col].min():.2f}")
        print(f"  Max outlier : {outliers[col].max():.2f}")
    print()
```

### 3.3 Détection par Z-Score

```python
from scipy import stats

# --- Méthode Z-Score ---
def detecter_outliers_zscore(df, colonne, seuil=3):
    """
    Détecte les outliers avec le Z-Score.
    Un Z-Score > 3 (ou < -3) = valeur à plus de 3 écarts-types de la moyenne.
    """
    z_scores = np.abs(stats.zscore(df[colonne].dropna()))
    outliers_mask = z_scores > seuil
    outliers = df[colonne].dropna()[outliers_mask]
    return outliers, z_scores

print("=== Rapport des valeurs aberrantes (Z-Score > 3) ===\n")
for col in colonnes_num:
    outliers, z_scores = detecter_outliers_zscore(df, col)
    pct = len(outliers) / len(df) * 100
    print(f"{col}: {len(outliers)} outliers ({pct:.1f}%)")
    if len(outliers) > 0:
        print(f"  Z-Score max : {z_scores.max():.2f}")
```

### 3.4 Visualisation avec boxplots

```python
# Boxplots pour toutes les colonnes numériques
n_cols = len(colonnes_num)
n_rows = (n_cols + 3) // 4
fig, axes = plt.subplots(n_rows, 4, figsize=(16, 4 * n_rows))
axes = axes.flatten()

for i, col in enumerate(colonnes_num):
    sns.boxplot(y=df[col], ax=axes[i], color='lightblue')
    outliers, b_inf, b_sup = detecter_outliers_iqr(df, col)
    axes[i].axhline(y=b_inf, color='red', linestyle='--', alpha=0.5)
    axes[i].axhline(y=b_sup, color='red', linestyle='--', alpha=0.5)
    axes[i].set_title(f'{col}\n({len(outliers)} outliers)')

# Masquer les axes inutilisés
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)

plt.suptitle("Détection des valeurs aberrantes (Boxplots + bornes IQR)", y=1.02)
plt.tight_layout()
plt.show()
```

```python
# Distribution + boxplot combinés
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

col_exemple = 'revenu'

# Histogramme
axes[0].hist(df[col_exemple].dropna(), bins=50, edgecolor='black', alpha=0.7)
axes[0].set_title(f'Distribution de {col_exemple}')
axes[0].set_xlabel(col_exemple)
axes[0].set_ylabel('Fréquence')

# Boxplot horizontal
sns.boxplot(x=df[col_exemple], ax=axes[1], color='lightcoral')
axes[1].set_title(f'Boxplot de {col_exemple}')

plt.tight_layout()
plt.show()
```

### 3.5 Que faire des outliers ?

| Décision | Quand | Code |
|----------|-------|------|
| **Supprimer** | Clairement une erreur (âge = 250) | `df = df[df['age'] < 150]` |
| **Capper (winsoriser)** | Valeur extrême mais plausible | `df[col] = df[col].clip(lower=b_inf, upper=b_sup)` |
| **Transformer (log)** | Distribution très asymétrique | `df['col_log'] = np.log1p(df['col'])` |
| **Garder** | Information légitime (fraude, VIP) | Ne rien faire |
| **Variable indicatrice** | Garder l'information sans le bruit | `df['col_outlier'] = (df['col'] > seuil).astype(int)` |

```python
# --- Capping (winsorisation) ---
def capper_outliers(df, colonne):
    """Remplace les outliers par les bornes IQR."""
    Q1 = df[colonne].quantile(0.25)
    Q3 = df[colonne].quantile(0.75)
    IQR = Q3 - Q1
    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR

    n_avant = ((df[colonne] < borne_inf) | (df[colonne] > borne_sup)).sum()
    df[colonne] = df[colonne].clip(lower=borne_inf, upper=borne_sup)
    print(f"  {colonne}: {n_avant} outliers cappés dans [{borne_inf:.2f}, {borne_sup:.2f}]")
    return df

# Appliquer sur les colonnes choisies
for col in ['revenu', 'montant_dernier_achat']:
    if col in df.columns:
        df = capper_outliers(df, col)
```

```python
# --- Transformation logarithmique ---
# Idéale pour les distributions très asymétriques (prix, revenus, surfaces)

col_asym = 'revenu'
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df[col_asym].dropna(), bins=50, edgecolor='black', alpha=0.7)
axes[0].set_title(f'{col_asym} — Distribution originale')

df[f'{col_asym}_log'] = np.log1p(df[col_asym])
axes[1].hist(df[f'{col_asym}_log'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='green')
axes[1].set_title(f'{col_asym}_log — Après transformation log')

plt.tight_layout()
plt.show()
```

> 💡 **Conseil** : "Avant de supprimer un outlier, posez-vous la question : est-ce une erreur de saisie ou un cas réel ? Un client qui achète pour 50 000€ est un outlier statistique mais c'est peut-être votre client le plus important. La détection de fraude repose justement sur les outliers."

---

## 4. 🔍 Enquête #3 : Les Corrélations Trompeuses

### 4.1 Corrélation ≠ Causalité

C'est LA règle d'or en data science. Deux variables peuvent être corrélées **sans qu'aucune ne cause l'autre**.

```
┌────────────────────────────────────────────────────────┐
│         CORRÉLATION  ≠  CAUSALITÉ                       │
│                                                         │
│  Corrélation :  A et B bougent ensemble                 │
│  Causalité :    A PROVOQUE B                            │
│                                                         │
│  Exemples célèbres de corrélations absurdes :           │
│                                                         │
│  🍦 Ventes de glaces  ↔  Nombre de noyades             │
│     → Variable cachée : la CHALEUR                      │
│                                                         │
│  👟 Ventes de chaussures  ↔  Taux de divorce            │
│     → Variable cachée : la TAILLE de la population      │
│                                                         │
│  🧀 Consommation de fromage  ↔  Morts par strangulation │
│     → Pure coïncidence statistique !                    │
└────────────────────────────────────────────────────────┘
```

### 4.2 Les pièges classiques

| Piège | Explication | Exemple |
|-------|------------|---------|
| **Variable confondante** | Une 3ème variable cause les deux | Chaleur → glaces ET noyades |
| **Corrélation fortuite** | Coïncidence sur la période | Fromage et strangulations |
| **Causalité inversée** | B cause A, pas A cause B | Pompiers et dégâts (plus de pompiers = plus de dégâts ?) |
| **Biais de sélection** | Données non représentatives | Survivants d'avion → conclusions biaisées |

### 4.3 Matrice de corrélation (heatmap)

```python
# Matrice de corrélation complète
colonnes_num = df.select_dtypes(include=[np.number]).columns.tolist()
correlation_matrix = df[colonnes_num].corr()

# Heatmap
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))  # masquer le triangle supérieur
sns.heatmap(
    correlation_matrix,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    vmin=-1, vmax=1,
    square=True,
    linewidths=0.5
)
plt.title("Matrice de corrélation (Pearson)")
plt.tight_layout()
plt.show()
```

```python
# Identifier les paires fortement corrélées
def trouver_fortes_correlations(df, seuil=0.7):
    """Trouve les paires de features avec |corrélation| > seuil."""
    corr_matrix = df.corr()
    upper_tri = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    paires = []
    for col in upper_tri.columns:
        for row in upper_tri.index:
            val = upper_tri.loc[row, col]
            if abs(val) > seuil:
                paires.append((col, row, round(val, 3)))

    paires.sort(key=lambda x: abs(x[2]), reverse=True)
    return paires

paires_correlees = trouver_fortes_correlations(df[colonnes_num], seuil=0.7)

print("=== Paires fortement corrélées (|r| > 0.7) ===")
for col1, col2, corr in paires_correlees:
    emoji = "🔴" if abs(corr) > 0.9 else "🟠" if abs(corr) > 0.8 else "🟡"
    print(f"  {emoji} {col1} ↔ {col2} : r = {corr}")
```

```python
# Corrélation avec la target (variable cible)
print("\n=== Corrélation avec la target (churn) ===")
if 'churn' in df.columns:
    corr_target = df[colonnes_num].corrwith(df['churn']).sort_values(ascending=False)
    print(corr_target)

    # Visualisation
    plt.figure(figsize=(10, 6))
    corr_target.plot(kind='barh', color=['green' if x > 0 else 'red' for x in corr_target])
    plt.title("Corrélation de chaque feature avec la target (churn)")
    plt.xlabel("Coefficient de corrélation (Pearson)")
    plt.axvline(x=0, color='black', linewidth=0.5)
    plt.tight_layout()
    plt.show()
```

> ⚠️ **Attention** : "La corrélation de Pearson ne capture que les relations **linéaires**. Deux variables peuvent avoir une corrélation de 0 tout en étant fortement liées de manière non linéaire (ex: relation en U). Utilisez la mutual information pour détecter les relations non linéaires."

```python
# --- Mutual Information : détecte les relations non linéaires ---
from sklearn.feature_selection import mutual_info_classif

if 'churn' in df.columns:
    # ⚠️ Uniquement sur les colonnes numériques, sans NaN
    X_num_clean = df[colonnes_num].dropna()
    y_clean = df.loc[X_num_clean.index, 'churn']

    mi_scores = mutual_info_classif(X_num_clean, y_clean, random_state=42)
    mi_df = pd.DataFrame({
        'feature': colonnes_num,
        'mutual_info': mi_scores
    }).sort_values('mutual_info', ascending=False)

    print("\n=== Mutual Information avec la target ===")
    print(mi_df)
```

> 💡 **Conseil** : "Quand vous trouvez une forte corrélation, demandez-vous toujours : est-ce que A cause B ? Est-ce que B cause A ? Ou est-ce qu'une variable cachée C cause les deux ? Ne tirez jamais de conclusions causales à partir d'une simple corrélation."

---

## 5. 📊 EDA Systématique avec ydata-profiling

### 5.1 Pourquoi automatiser l'EDA ?

L'EDA manuelle est longue et on oublie souvent des vérifications. `ydata-profiling` (anciennement `pandas-profiling`) génère un rapport complet en **une seule ligne de code**.

```python
# Installation
# uv add ydata-profiling
```

### 5.2 Générer un rapport complet

```python
from ydata_profiling import ProfileReport

# Générer le rapport
profile = ProfileReport(
    df,
    title="Audit Qualité — Dataset Clients Churn",
    explorative=True,
    correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": False},
    }
)

# Sauvegarder en HTML
profile.to_file("rapport_eda_churn.html")
print("Rapport sauvegardé : rapport_eda_churn.html")

# Ou afficher dans un notebook Jupyter
# profile.to_notebook_iframe()
```

### 5.3 Ce que contient le rapport

| Section | Contenu | Utilité |
|---------|---------|--------|
| **Overview** | Nombre de lignes, colonnes, manquantes, doublons | Vue d'ensemble rapide |
| **Variables** | Distribution, stats, valeurs extrêmes par colonne | Analyse détaillée |
| **Interactions** | Scatter plots entre variables | Relations visuelles |
| **Correlations** | Heatmaps (Pearson, Spearman) | Corrélations |
| **Missing values** | Pattern des manquantes, matrice, heatmap | Comprendre les NaN |
| **Duplicates** | Lignes dupliquées | Nettoyage |
| **Alerts** | Avertissements automatiques (haute corrélation, constantes...) | Points d'attention |

### 5.4 EDA manuelle complémentaire

Le rapport automatique ne remplace pas le regard humain. Voici les vérifications complémentaires :

```python
# --- Vérifications complémentaires ---

# 1. Doublons
print(f"Lignes dupliquées : {df.duplicated().sum()}")
print(f"Lignes dupliquées (%) : {df.duplicated().sum() / len(df) * 100:.2f}%")

# 2. Constantes (colonnes avec une seule valeur → inutiles)
constantes = [col for col in df.columns if df[col].nunique() <= 1]
print(f"\nColonnes constantes (à supprimer) : {constantes}")

# 3. Quasi-constantes (>95% la même valeur)
quasi_constantes = []
for col in df.columns:
    if df[col].value_counts(normalize=True).iloc[0] > 0.95:
        quasi_constantes.append(col)
print(f"Colonnes quasi-constantes (>95%) : {quasi_constantes}")

# 4. Haute cardinalité (trop de catégories)
for col in colonnes_cat:
    n = df[col].nunique()
    if n > 50:
        print(f"\n⚠️  {col} : {n} catégories (haute cardinalité)")

# 5. Identifiants (colonnes uniques → inutiles pour le ML)
identifiants = [col for col in df.columns if df[col].nunique() == len(df)]
print(f"\nIdentifiants potentiels (à exclure) : {identifiants}")
```

```python
# 6. Distribution de la target
if 'churn' in df.columns:
    print("\n=== Distribution de la target ===")
    print(df['churn'].value_counts())
    print(df['churn'].value_counts(normalize=True).apply(lambda x: f"{x:.1%}"))

    plt.figure(figsize=(6, 4))
    df['churn'].value_counts().plot(kind='bar', color=['steelblue', 'coral'])
    plt.title("Distribution de la variable cible (churn)")
    plt.xlabel("Churn")
    plt.ylabel("Nombre de clients")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
```

> 💡 **Conseil** : "Lancez toujours ydata-profiling en premier pour avoir une vue d'ensemble. Puis complétez avec une EDA manuelle ciblée sur les points d'alerte identifiés dans le rapport. Cette double approche vous fait gagner un temps considérable."

---

## 6. 🏗️ Exercice Fil Rouge : Audit Qualité du Dataset clients_churn.csv

### 6.1 Contexte

Vous êtes data scientist dans une entreprise de télécommunications. On vous confie le dataset `clients_churn.csv` et on vous demande un **audit qualité complet** avant toute modélisation.

### 6.2 Étapes de l'audit

```python
# ============================================================
# AUDIT QUALITÉ — DATASET CLIENTS_CHURN.CSV
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Étape 1 : Chargement et première impression ---
df = pd.read_csv("clients_churn.csv")

print("=" * 60)
print("ÉTAPE 1 : Vue d'ensemble")
print("=" * 60)
print(f"Shape : {df.shape}")
print(f"Colonnes : {df.columns.tolist()}")
print(f"\nTypes :")
print(df.dtypes)
print(f"\nPremières lignes :")
print(df.head())
```

```python
# --- Étape 2 : Valeurs manquantes ---
print("\n" + "=" * 60)
print("ÉTAPE 2 : Valeurs manquantes")
print("=" * 60)

manquantes = df.isnull().sum()
pct = (manquantes / len(df) * 100).round(2)

rapport_manquantes = pd.DataFrame({
    'Nb_manquantes': manquantes,
    'Pct_manquantes': pct
}).sort_values('Pct_manquantes', ascending=False)

print(rapport_manquantes[rapport_manquantes['Nb_manquantes'] > 0])

# Décision pour chaque colonne
print("\n--- Décisions ---")
for col, row in rapport_manquantes.iterrows():
    if row['Pct_manquantes'] > 50:
        print(f"  ❌ {col} ({row['Pct_manquantes']}%) → SUPPRIMER la colonne")
    elif row['Pct_manquantes'] > 5:
        print(f"  🔧 {col} ({row['Pct_manquantes']}%) → IMPUTER")
    elif row['Pct_manquantes'] > 0:
        print(f"  ✅ {col} ({row['Pct_manquantes']}%) → Imputer ou supprimer lignes")
```

```python
# --- Étape 3 : Valeurs aberrantes ---
print("\n" + "=" * 60)
print("ÉTAPE 3 : Valeurs aberrantes")
print("=" * 60)

colonnes_num = df.select_dtypes(include=[np.number]).columns.tolist()

for col in colonnes_num:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    b_inf = Q1 - 1.5 * IQR
    b_sup = Q3 + 1.5 * IQR
    n_outliers = ((df[col] < b_inf) | (df[col] > b_sup)).sum()
    pct_out = n_outliers / len(df) * 100

    if pct_out > 0:
        print(f"  {col}: {n_outliers} outliers ({pct_out:.1f}%) "
              f"— min={df[col].min():.2f}, max={df[col].max():.2f}, "
              f"bornes=[{b_inf:.2f}, {b_sup:.2f}]")
```

```python
# --- Étape 4 : Corrélations ---
print("\n" + "=" * 60)
print("ÉTAPE 4 : Corrélations")
print("=" * 60)

# Corrélations entre features
paires = trouver_fortes_correlations(df[colonnes_num], seuil=0.7)
if paires:
    print("Paires fortement corrélées (|r| > 0.7) :")
    for col1, col2, corr in paires:
        print(f"  {col1} ↔ {col2} : r = {corr}")
else:
    print("Aucune paire avec |r| > 0.7")

# Corrélation avec la target
if 'churn' in df.columns:
    corr_target = df[colonnes_num].corrwith(df['churn']).abs().sort_values(ascending=False)
    print("\nTop 5 features corrélées avec churn :")
    print(corr_target.head())
```

```python
# --- Étape 5 : Doublons et anomalies ---
print("\n" + "=" * 60)
print("ÉTAPE 5 : Doublons et anomalies")
print("=" * 60)

print(f"Doublons complets : {df.duplicated().sum()}")

colonnes_cat = df.select_dtypes(include=['object']).columns.tolist()
for col in colonnes_cat:
    print(f"\n{col} ({df[col].nunique()} catégories) :")
    print(df[col].value_counts().head(10))
```

```python
# --- Étape 6 : Rapport ydata-profiling ---
from ydata_profiling import ProfileReport

profile = ProfileReport(df, title="Audit Clients Churn", explorative=True)
profile.to_file("audit_clients_churn.html")
print("\n✅ Rapport complet sauvegardé : audit_clients_churn.html")
```

### 6.3 Template de rapport d'audit

À la fin de votre audit, remplissez ce tableau récapitulatif :

| Critère | Résultat | Action |
|---------|----------|--------|
| Nombre de lignes | ... | — |
| Nombre de colonnes | ... | — |
| % global de manquantes | ... | Imputer / Supprimer |
| Colonnes à supprimer (>50% NaN) | ... | `df.drop(columns=[...])` |
| Nombre d'outliers détectés | ... | Capper / Transformer / Garder |
| Paires corrélées (>0.8) | ... | Supprimer une des deux |
| Doublons | ... | `df.drop_duplicates()` |
| Colonnes identifiant | ... | Exclure du ML |
| Distribution target | ... | Stratifier / SMOTE si déséquilibré |

> 💡 **Conseil** : "Cet audit qualité doit être fait **systématiquement** sur tout nouveau dataset. Créez-vous un template réutilisable. Avec le temps, vous développerez un instinct pour repérer les problèmes rapidement."

---

## 🎯 Points clés à retenir

1. **Connaître ses types de données** : numériques (continues/discrètes), catégorielles (nominales/ordinales), temporelles, texte, booléens — chaque type requiert un traitement spécifique
2. **Les valeurs manquantes ont des causes** : MCAR (hasard pur), MAR (lié à d'autres variables), MNAR (lié à la valeur elle-même) — comprendre la cause guide le choix du traitement
3. **Imputer intelligemment** : médiane pour les numériques avec outliers, mode pour les catégorielles, KNN quand les features sont liées — et toujours fit sur le train, transform sur le test
4. **Les outliers ne sont pas toujours des erreurs** : distinguer erreur de saisie (supprimer) et signal réel (garder) est une compétence clé
5. **Méthode IQR et Z-Score** : deux outils complémentaires pour détecter les valeurs aberrantes — les visualiser avec des boxplots avant de décider
6. **Corrélation ≠ Causalité** : toujours chercher la variable confondante avant de conclure — les corrélations trompeuses sont partout
7. **ydata-profiling pour l'EDA automatique** : un rapport complet en une ligne de code — complétez-le par une analyse manuelle ciblée
8. **L'audit qualité est systématique** : avant toute modélisation, passez par les 6 étapes — manquantes, outliers, corrélations, doublons, distribution target
9. **Créer des variables indicatrices** : le fait qu'une donnée manque EST souvent une information utile — créez une colonne `_manquant`
10. **80% du temps d'un data scientist** est passé sur la compréhension et la préparation des données — ne négligez jamais cette étape

---

## ✅ Checklist de validation

- [ ] Je sais distinguer les types de données (continu, discret, nominal, ordinal, temporel, texte, booléen)
- [ ] Je sais détecter les valeurs manquantes et calculer leur pourcentage par colonne
- [ ] Je connais la différence entre MCAR, MAR et MNAR
- [ ] Je sais choisir la bonne stratégie d'imputation selon le contexte
- [ ] Je maîtrise SimpleImputer et KNNImputer de scikit-learn
- [ ] Je sais détecter les outliers avec la méthode IQR et le Z-Score
- [ ] Je sais visualiser les outliers avec des boxplots
- [ ] Je sais décider si un outlier est une erreur ou un signal
- [ ] Je comprends que corrélation ≠ causalité et je sais donner des exemples
- [ ] Je sais créer une matrice de corrélation (heatmap) et l'interpréter
- [ ] Je sais utiliser ydata-profiling pour générer un rapport EDA automatique
- [ ] Je sais mener un audit qualité complet sur un dataset
- [ ] Je respecte la règle : fit sur le train, transform sur le test

---

**Précédent** : [Chapitre 5 : Classification](05-classification.md)

**Suivant** : [Chapitre 7 : Feature Engineering — L'Art de Préparer les Données](07-feature-engineering.md)
