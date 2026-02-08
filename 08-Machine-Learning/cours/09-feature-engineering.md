# Chapitre 9 : Feature Engineering – L'Art de Créer des Features

## 🎯 Objectifs

- Comprendre pourquoi le feature engineering est l'étape la plus décisive du ML
- Savoir créer de nouvelles features à partir de données numériques, temporelles, textuelles et catégorielles
- Maîtriser les méthodes de sélection de features (filter, wrapper, embedded)
- Comprendre la réduction de dimensionnalité avec PCA
- Construire des pipelines complets et reproductibles avec scikit-learn

---

## 1. 🧠 Pourquoi le feature engineering est décisif

### 1.1 Le carburant des modèles ML

> "Features are the fuel of ML models. Better features = better models. Period."

Le feature engineering est le processus de **transformation des données brutes en features informatives** pour les algorithmes de Machine Learning. C'est l'étape qui a le **plus grand impact** sur la performance d'un modèle.

| Levier d'amélioration | Impact typique | Effort |
|---|---|---|
| Données propres | 10-30% | Élevé |
| **Feature engineering** | **10-30%** | **Élevé** |
| Choix de l'algorithme | 5-15% | Moyen |
| Tuning des hyperparamètres | 2-5% | Moyen |
| Ensemble methods | 1-3% | Faible |

> 💡 **Conseil de pro** : "Le feature engineering est ce qui sépare un bon data scientist d'un data scientist moyen. C'est là que la connaissance du domaine métier fait la différence. Un bon feature engineering avec une régression logistique battra souvent un mauvais feature engineering avec XGBoost."

### 1.2 Principes fondamentaux

1. **Comprendre le domaine** : Parlez aux experts métier. Quelles informations utilisent-ils pour prendre des décisions ?
2. **Explorer les données** : Visualisez les distributions, les corrélations, les patterns temporels
3. **Itérer** : Créez des features, testez leur impact, gardez les meilleures, supprimez les inutiles
4. **Mesurer** : Chaque feature doit améliorer la métrique cible (ou ne pas la dégrader)

> 💡 **Conseil** : "Avant de créer des features, passez du temps à COMPRENDRE les données. Chaque colonne, chaque distribution, chaque corrélation. Le feature engineering vient naturellement quand on comprend les données."

---

## 2. ⚙️ Création de features

### 2.1 Features numériques

#### Transformations mathématiques

```python
import pandas as pd
import numpy as np

# Données d'exemple : transactions e-commerce
df = pd.DataFrame({
    'prix': [29.99, 149.50, 9.99, 499.00, 74.50],
    'quantite': [2, 1, 5, 1, 3],
    'poids_kg': [0.5, 2.1, 0.1, 5.0, 1.2],
    'surface_m2': [10, 50, 5, 200, 30],
    'anciennete_jours': [30, 365, 7, 730, 180]
})

# Features dérivées numériques
df['montant_total'] = df['prix'] * df['quantite']              # ratio / produit
df['prix_par_kg'] = df['prix'] / df['poids_kg']                # ratio
df['log_prix'] = np.log1p(df['prix'])                          # transformation log
df['prix_carre'] = df['prix'] ** 2                             # polynomiale
df['prix_racine'] = np.sqrt(df['prix'])                        # racine carrée
df['surface_log'] = np.log1p(df['surface_m2'])                 # log pour distributions skewed

# Binning (discrétisation)
df['categorie_prix'] = pd.cut(
    df['prix'],
    bins=[0, 20, 100, 500],
    labels=['pas_cher', 'moyen', 'cher']
)

# Quantile binning (même nombre d'observations par bin)
df['quantile_prix'] = pd.qcut(df['prix'], q=3, labels=['bas', 'moyen', 'haut'])

print(df)
```

> 💡 **Conseil** : "La transformation logarithmique est votre meilleur ami pour les distributions asymétriques (prix, revenus, surfaces). Elle réduit l'impact des valeurs extrêmes et rend souvent les relations plus linéaires."

#### Interactions entre features

```python
# Interactions polynomiales
from sklearn.preprocessing import PolynomialFeatures

X_num = df[['prix', 'quantite', 'poids_kg']].values

# Créer des interactions d'ordre 2 (a, b, a², ab, b²)
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_poly = poly.fit_transform(X_num)

# Voir les noms des features créées
feature_names = poly.get_feature_names_out(['prix', 'quantite', 'poids_kg'])
print(f"Features originales : {X_num.shape[1]}")
print(f"Features après polynomiales : {X_poly.shape[1]}")
print(f"Noms : {feature_names}")
```

> ⚠️ **Attention** : "Les features polynomiales peuvent exploser combinatoirement. Avec 10 features et degree=3, vous obtenez 286 features ! Utilisez `interaction_only=True` pour limiter aux interactions sans les puissances."

### 2.2 Features temporelles

Les données temporelles sont une mine d'or pour le feature engineering :

```python
# Données temporelles
df_time = pd.DataFrame({
    'date_achat': pd.to_datetime([
        '2024-01-15 14:30:00',
        '2024-03-22 09:15:00',
        '2024-07-04 22:45:00',
        '2024-12-25 11:00:00',
        '2024-06-15 16:30:00'
    ]),
    'montant': [50, 120, 30, 200, 75]
})

# Features temporelles de base
df_time['annee'] = df_time['date_achat'].dt.year
df_time['mois'] = df_time['date_achat'].dt.month
df_time['jour'] = df_time['date_achat'].dt.day
df_time['heure'] = df_time['date_achat'].dt.hour
df_time['jour_semaine'] = df_time['date_achat'].dt.dayofweek  # 0=lundi, 6=dimanche
df_time['jour_annee'] = df_time['date_achat'].dt.dayofyear
df_time['semaine'] = df_time['date_achat'].dt.isocalendar().week.astype(int)

# Features dérivées
df_time['est_weekend'] = df_time['jour_semaine'].isin([5, 6]).astype(int)
df_time['est_matin'] = (df_time['heure'] < 12).astype(int)
df_time['trimestre'] = df_time['date_achat'].dt.quarter

# Saisonnalité (encodage cyclique pour capturer la circularité)
df_time['mois_sin'] = np.sin(2 * np.pi * df_time['mois'] / 12)
df_time['mois_cos'] = np.cos(2 * np.pi * df_time['mois'] / 12)
df_time['heure_sin'] = np.sin(2 * np.pi * df_time['heure'] / 24)
df_time['heure_cos'] = np.cos(2 * np.pi * df_time['heure'] / 24)

# Jours fériés (simplifié)
jours_feries = ['2024-01-01', '2024-07-14', '2024-12-25']
df_time['est_ferie'] = df_time['date_achat'].dt.date.astype(str).isin(jours_feries).astype(int)

print(df_time)
```

#### Lag features et rolling averages (séries temporelles)

```python
# Lag features : valeur aux pas de temps précédents
df_ts = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30, freq='D'),
    'ventes': np.random.randint(50, 200, 30)
})
df_ts = df_ts.set_index('date')

# Lag features
df_ts['ventes_j-1'] = df_ts['ventes'].shift(1)   # ventes d'hier
df_ts['ventes_j-7'] = df_ts['ventes'].shift(7)   # ventes il y a 7 jours

# Rolling averages (moyenne glissante)
df_ts['moyenne_7j'] = df_ts['ventes'].rolling(window=7).mean()
df_ts['moyenne_14j'] = df_ts['ventes'].rolling(window=14).mean()
df_ts['std_7j'] = df_ts['ventes'].rolling(window=7).std()

# Variation par rapport à la moyenne
df_ts['ratio_vs_moy7j'] = df_ts['ventes'] / df_ts['moyenne_7j']

# Tendance (différence)
df_ts['diff_j-1'] = df_ts['ventes'].diff(1)

print(df_ts.head(15))
```

> 💡 **Conseil de pro** : "Pour les séries temporelles, les lag features et les rolling averages sont parmi les features les plus puissantes. Testez toujours les lags 1, 7, 14, 28 (quotidien) ou 1, 12, 24 (horaire). L'encodage cyclique (sin/cos) est crucial pour les heures et les mois."

> ⚠️ **Attention** : "Les lag features créent des valeurs manquantes en début de série (shift). N'oubliez pas de les supprimer ou de les imputer. Et surtout : JAMAIS utiliser des données futures dans les lags → data leakage temporel !"

### 2.3 Features textuelles

```python
# Features de base à partir de texte
df_text = pd.DataFrame({
    'description': [
        'Excellent produit, livraison rapide !',
        'Nul. Produit cassé à la réception.',
        'Correct pour le prix. RAS.',
        'INCROYABLE !!! Le meilleur achat de ma vie !!!',
        'Bof, pas terrible mais pas catastrophique non plus.'
    ]
})

# Features simples
df_text['nb_mots'] = df_text['description'].str.split().str.len()
df_text['nb_caracteres'] = df_text['description'].str.len()
df_text['nb_exclamation'] = df_text['description'].str.count('!')
df_text['nb_majuscules'] = df_text['description'].str.count('[A-Z]')
df_text['ratio_majuscules'] = df_text['nb_majuscules'] / df_text['nb_caracteres']
df_text['nb_points'] = df_text['description'].str.count('\\.')
df_text['longueur_moy_mot'] = (
    df_text['nb_caracteres'] / df_text['nb_mots']
)

print(df_text)
```

#### TF-IDF pour le texte (introduction vers le NLP)

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# TF-IDF : Term Frequency - Inverse Document Frequency
tfidf = TfidfVectorizer(
    max_features=100,      # garder les 100 mots les plus importants
    stop_words=None,       # ou liste de stop words français
    ngram_range=(1, 2),    # unigrammes et bigrammes
    min_df=1,              # mot doit apparaître au moins 1 fois
    max_df=0.95            # pas de mots dans 95%+ des documents
)

tfidf_matrix = tfidf.fit_transform(df_text['description'])
tfidf_df = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=tfidf.get_feature_names_out()
)

print(f"Shape TF-IDF : {tfidf_df.shape}")
print(tfidf_df.head())
```

> 💡 **Conseil** : "Les features textuelles simples (longueur, nombre de mots, ponctuation) sont souvent très utiles en complément du TF-IDF. Un avis avec beaucoup de points d'exclamation et de majuscules a souvent un sentiment fort."

### 2.4 Features catégorielles avancées

Au-delà du One-Hot Encoding classique, il existe des encodages plus sophistiqués :

#### Target Encoding

```python
# Target encoding : remplacer la catégorie par la moyenne de la cible
df_cat = pd.DataFrame({
    'ville': ['Paris', 'Lyon', 'Paris', 'Marseille', 'Lyon', 'Paris', 'Marseille', 'Lyon'],
    'prix': [500, 300, 450, 280, 320, 480, 260, 310]
})

# Target encoding avec régularisation (smoothing)
global_mean = df_cat['prix'].mean()
smoothing = 10  # paramètre de lissage

target_encoding = df_cat.groupby('ville')['prix'].agg(['mean', 'count'])
target_encoding['target_encode'] = (
    (target_encoding['count'] * target_encoding['mean'] + smoothing * global_mean) /
    (target_encoding['count'] + smoothing)
)

df_cat['ville_encoded'] = df_cat['ville'].map(target_encoding['target_encode'])
print(df_cat)
```

> ⚠️ **Attention** : "Le target encoding peut facilement créer un data leakage ! La cible (target) est utilisée pour encoder les features. Utilisez TOUJOURS le target encoding dans un pipeline avec cross-validation pour éviter ce problème."

#### Frequency Encoding

```python
# Frequency encoding : remplacer par la fréquence d'apparition
freq = df_cat['ville'].value_counts(normalize=True)
df_cat['ville_freq'] = df_cat['ville'].map(freq)
print(df_cat[['ville', 'ville_freq']])
```

> 💡 **Conseil de pro** : "Le frequency encoding est un bon compromis entre simplicité et performance. Il capture l'information de rareté sans data leakage. Utilisez-le pour les features catégorielles à haute cardinalité (>20 catégories)."

#### Interactions entre features catégorielles

```python
# Combiner deux catégories
df_inter = pd.DataFrame({
    'ville': ['Paris', 'Lyon', 'Paris', 'Marseille'],
    'type_bien': ['Appartement', 'Maison', 'Maison', 'Appartement']
})

# Interaction : combiner les catégories
df_inter['ville_type'] = df_inter['ville'] + '_' + df_inter['type_bien']
print(df_inter)
```

---

## 3. 🔍 Sélection de features

Trop de features = bruit, overfitting, lenteur. La sélection de features élimine les features inutiles.

### 3.1 Filter methods (avant le modèle)

Les filter methods évaluent les features **indépendamment du modèle**, en utilisant des statistiques.

```python
from sklearn.feature_selection import (
    mutual_info_classif,
    chi2,
    f_classif,
    SelectKBest
)
from sklearn.datasets import make_classification

# Données d'exemple
X, y = make_classification(
    n_samples=1000, n_features=20,
    n_informative=10, n_redundant=5, n_useless=5,
    random_state=42
)

feature_names = [f'feature_{i}' for i in range(20)]

# Mutual Information (fonctionne pour toute relation, pas juste linéaire)
mi_scores = mutual_info_classif(X, y, random_state=42)
mi_df = pd.DataFrame({
    'feature': feature_names,
    'mutual_info': mi_scores
}).sort_values('mutual_info', ascending=False)

print("Top 10 features (Mutual Information) :")
print(mi_df.head(10))

# ANOVA F-test (linéaire)
f_scores, p_values = f_classif(X, y)
f_df = pd.DataFrame({
    'feature': feature_names,
    'f_score': f_scores,
    'p_value': p_values
}).sort_values('f_score', ascending=False)

print("\nTop 10 features (ANOVA F-test) :")
print(f_df.head(10))

# Sélectionner les K meilleures features
selector = SelectKBest(score_func=mutual_info_classif, k=10)
X_selected = selector.fit_transform(X, y)

# Quelles features ont été sélectionnées ?
selected_mask = selector.get_support()
selected_features = [f for f, s in zip(feature_names, selected_mask) if s]
print(f"\nFeatures sélectionnées : {selected_features}")
```

#### Matrice de corrélation

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Matrice de corrélation
df_corr = pd.DataFrame(X, columns=feature_names)
correlation_matrix = df_corr.corr()

# Visualisation
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0, vmin=-1, vmax=1)
plt.title('Matrice de Corrélation des Features')
plt.tight_layout()
plt.show()

# Identifier les features très corrélées entre elles (> 0.8)
upper_tri = correlation_matrix.where(
    np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
)
high_corr = [(col, row, correlation_matrix.loc[row, col])
             for col in upper_tri.columns
             for row in upper_tri.index
             if abs(upper_tri.loc[row, col]) > 0.8]

print(f"\nPaires très corrélées (|r| > 0.8) :")
for col, row, corr in high_corr:
    print(f"  {col} <-> {row} : {corr:.3f}")
```

> 💡 **Conseil** : "Supprimez une des deux features dans chaque paire très corrélée (|r| > 0.8). Elles apportent la même information mais ajoutent du bruit et ralentissent l'entraînement."

### 3.2 Wrapper methods (avec le modèle)

Les wrapper methods utilisent le **modèle lui-même** pour évaluer les features.

#### RFE (Recursive Feature Elimination)

```python
from sklearn.feature_selection import RFE, RFECV
from sklearn.ensemble import RandomForestClassifier

# RFE : élimination récursive
rfe = RFE(
    estimator=RandomForestClassifier(n_estimators=100, random_state=42),
    n_features_to_select=10,  # garder 10 features
    step=1                     # éliminer 1 feature à chaque étape
)

rfe.fit(X, y)

# Features sélectionnées
rfe_features = [f for f, s in zip(feature_names, rfe.support_) if s]
print(f"Features sélectionnées (RFE) : {rfe_features}")
print(f"Ranking : {dict(zip(feature_names, rfe.ranking_))}")

# RFECV : RFE avec cross-validation (trouve automatiquement le nombre optimal)
rfecv = RFECV(
    estimator=RandomForestClassifier(n_estimators=100, random_state=42),
    step=1,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1
)

rfecv.fit(X, y)
print(f"\nNombre optimal de features : {rfecv.n_features_}")
print(f"Score avec les features optimales : {rfecv.cv_results_['mean_test_score'].max():.4f}")
```

> 💡 **Conseil de pro** : "RFECV est la méthode la plus fiable pour la sélection de features car elle utilise la cross-validation. C'est lent mais robuste. Pour aller plus vite, utilisez `step=2` ou `step=0.1` (10% des features éliminées à chaque étape)."

### 3.3 Embedded methods (pendant le modèle)

Les embedded methods intègrent la sélection de features **dans l'entraînement du modèle**.

```python
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestClassifier

# Lasso (L1) : met automatiquement certains coefficients à 0
lasso = LassoCV(cv=5, random_state=42)
# lasso.fit(X, y)  # pour la régression

# Feature importance du Random Forest
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X, y)

# Sélection par importance (seuil = moyenne)
from sklearn.feature_selection import SelectFromModel

selector_rf = SelectFromModel(rf, threshold='mean')
X_selected_rf = selector_rf.fit_transform(X, y)

selected_rf = [f for f, s in zip(feature_names, selector_rf.get_support()) if s]
print(f"Features sélectionnées (RF importance > moyenne) : {selected_rf}")
print(f"Nombre : {len(selected_rf)} / {len(feature_names)}")
```

### 3.4 Comparaison des méthodes de sélection

| Méthode | Type | Avantages | Inconvénients | Quand utiliser |
|---|---|---|---|---|
| **Corrélation** | Filter | Rapide, simple | Linéaire uniquement | Exploration rapide |
| **Mutual Info** | Filter | Détecte les relations non linéaires | Peut être bruitée | Toujours en complément |
| **Chi2** | Filter | Adapté aux features catégorielles | Features positives uniquement | Texte (TF-IDF) |
| **RFE** | Wrapper | Fiable, utilise le modèle | Lent | Sélection finale |
| **RFECV** | Wrapper | Le plus fiable, trouve le nombre optimal | Très lent | Quand la performance prime |
| **Lasso (L1)** | Embedded | Intégré à l'entraînement | Linéaire | Régression, interprétabilité |
| **Feature importance RF** | Embedded | Rapide, non linéaire | Biaisé (haute cardinalité) | Exploration rapide |

> 💡 **Conseil** : "Utilisez une approche en entonnoir : (1) Filter method pour une première élimination rapide (supprimer les features corrélées, p-value > 0.05). (2) Embedded method pour affiner (RF importance). (3) RFECV pour la sélection finale."

---

## 4. 📊 PCA (Principal Component Analysis)

### 4.1 Concept

La PCA (Analyse en Composantes Principales) est une technique de **réduction de dimensionnalité**. Elle transforme les features originales en un nouveau jeu de **composantes principales** qui :

1. Sont **orthogonales** (non corrélées) entre elles
2. Maximisent la **variance expliquée**
3. Sont ordonnées par variance décroissante (PC1 capture le plus de variance)

### 4.2 Implémentation

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# IMPORTANT : toujours normaliser avant PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA : garder 95% de la variance
pca = PCA(n_components=0.95)  # garder 95% de la variance
X_pca = pca.fit_transform(X_scaled)

print(f"Features originales : {X.shape[1]}")
print(f"Composantes PCA : {X_pca.shape[1]}")
print(f"Variance expliquée : {pca.explained_variance_ratio_.sum():.2%}")
print(f"Variance par composante : {pca.explained_variance_ratio_}")

# Visualisation : Scree plot (variance expliquée cumulée)
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.bar(range(1, len(pca.explained_variance_ratio_) + 1),
        pca.explained_variance_ratio_, alpha=0.7)
plt.xlabel('Composante principale')
plt.ylabel('Variance expliquée')
plt.title('Variance par composante')

plt.subplot(1, 2, 2)
plt.plot(range(1, len(pca.explained_variance_ratio_) + 1),
         np.cumsum(pca.explained_variance_ratio_), 'bo-', linewidth=2)
plt.axhline(y=0.95, color='red', linestyle='--', label='95% de variance')
plt.xlabel('Nombre de composantes')
plt.ylabel('Variance expliquée cumulée')
plt.title('Variance cumulée')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 4.3 Visualisation 2D avec PCA

```python
# PCA pour visualisation (2D)
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X_scaled)

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y, cmap='viridis', alpha=0.5)
plt.xlabel(f'PC1 ({pca_2d.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca_2d.explained_variance_ratio_[1]:.1%} variance)')
plt.title('Projection PCA 2D')
plt.colorbar(scatter, label='Classe')
plt.tight_layout()
plt.show()
```

### 4.4 Quand utiliser PCA ?

| Situation | PCA recommandé ? | Pourquoi |
|---|---|---|
| Beaucoup de features (100+) | Oui | Réduction du bruit et de la dimensionnalité |
| Visualisation en 2D/3D | Oui | Projection exploratoire |
| Features très corrélées | Oui | PCA les décorrèle |
| Besoin d'interprétabilité | Non | Les composantes n'ont pas de sens métier |
| Peu de features (<20) | Non | Pas nécessaire |
| Features non linéaires | Non (ou Kernel PCA) | PCA est linéaire |

> 💡 **Conseil** : "PCA perd l'interprétabilité. Les composantes principales n'ont pas de signification métier (« PC1 » ne veut rien dire pour un métier). Utilisez PCA surtout pour la visualisation ou quand vous avez 100+ features et que l'interprétabilité n'est pas critique."

> ⚠️ **Attention** : "TOUJOURS normaliser (StandardScaler) avant PCA. Sans normalisation, les features avec de grandes valeurs dominent les composantes principales."

---

## 5. 🔧 Pipelines complets scikit-learn

### 5.1 Pourquoi les pipelines ?

Un pipeline regroupe toutes les étapes de preprocessing et de modélisation en **un seul objet**. Avantages :

1. **Pas de data leakage** : le fit se fait uniquement sur le train set
2. **Code reproductible** : une seule ligne pour tout le processus
3. **Déploiement facile** : sauvegarder le pipeline = sauvegarder tout le workflow
4. **Compatible avec GridSearchCV** : tuner le preprocessing ET le modèle ensemble

### 5.2 Pipeline simple

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# Pipeline : normalisation → modèle
pipeline_simple = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Entraîner et évaluer en une seule ligne
scores = cross_val_score(pipeline_simple, X, y, cv=5, scoring='roc_auc')
print(f"AUC-ROC : {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### 5.3 Pipeline complet avec ColumnTransformer

Le ColumnTransformer permet d'appliquer des transformations **différentes** selon le type de colonne :

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV

# Simuler un dataset réaliste
import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'age': np.random.randint(18, 70, n),
    'revenu': np.random.normal(45000, 15000, n),
    'nb_achats': np.random.randint(0, 50, n),
    'anciennete_mois': np.random.randint(1, 120, n),
    'ville': np.random.choice(['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nantes'], n),
    'type_contrat': np.random.choice(['CDI', 'CDD', 'Freelance'], n),
    'canal_acquisition': np.random.choice(['Web', 'Magasin', 'Telephone'], n),
})
df['churn'] = (
    (df['nb_achats'] < 10).astype(int) * 0.3 +
    (df['anciennete_mois'] < 12).astype(int) * 0.4 +
    np.random.random(n) * 0.3
) > 0.5
df['churn'] = df['churn'].astype(int)

# Introduire des valeurs manquantes
df.loc[np.random.choice(n, 50), 'revenu'] = np.nan
df.loc[np.random.choice(n, 30), 'age'] = np.nan

X = df.drop('churn', axis=1)
y = df['churn']

# Identifier les colonnes par type
colonnes_num = ['age', 'revenu', 'nb_achats', 'anciennete_mois']
colonnes_cat = ['ville', 'type_contrat', 'canal_acquisition']

# Définir les transformations par type de colonne
preprocessing_num = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),  # valeurs manquantes → médiane
    ('scaler', StandardScaler())                     # normalisation
])

preprocessing_cat = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),  # valeurs manquantes → mode
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# ColumnTransformer : appliquer les bonnes transformations aux bonnes colonnes
preprocessor = ColumnTransformer(
    transformers=[
        ('num', preprocessing_num, colonnes_num),
        ('cat', preprocessing_cat, colonnes_cat)
    ]
)

# Pipeline complet : preprocessing → modèle
pipeline_complet = Pipeline([
    ('preprocessing', preprocessor),
    ('model', RandomForestClassifier(n_estimators=200, random_state=42))
])

# Évaluation avec cross-validation
scores = cross_val_score(pipeline_complet, X, y, cv=5, scoring='roc_auc', n_jobs=-1)
print(f"AUC-ROC (5-Fold CV) : {scores.mean():.4f} (+/- {scores.std():.4f})")
```

### 5.4 Tuning du pipeline complet avec GridSearchCV

```python
# Grille d'hyperparamètres (noter la syntaxe avec __ pour accéder aux étapes)
param_grid = {
    'preprocessing__num__imputer__strategy': ['mean', 'median'],
    'model__n_estimators': [100, 200, 300],
    'model__max_depth': [5, 10, 15, None],
    'model__min_samples_leaf': [1, 2, 5]
}

# GridSearchCV sur le pipeline complet
grid = GridSearchCV(
    pipeline_complet,
    param_grid=param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid.fit(X, y)

print(f"Meilleurs paramètres : {grid.best_params_}")
print(f"Meilleur AUC-ROC : {grid.best_score_:.4f}")
```

> 💡 **Conseil de pro** : "Un pipeline bien construit = code reproductible + pas de data leakage + déploiement facile. TOUJOURS mettre le preprocessing dans le pipeline, JAMAIS le faire séparément avant le split. Sinon vous avez un data leakage (le scaler voit les données de test)."

### 5.5 Sauvegarder le pipeline complet

```python
import joblib

# Entraîner le meilleur pipeline
best_pipeline = grid.best_estimator_

# Sauvegarder TOUT le pipeline (preprocessing + modèle)
joblib.dump(best_pipeline, 'pipeline_churn_v1.joblib')

# Charger et utiliser
pipeline_charge = joblib.load('pipeline_churn_v1.joblib')

# Prédiction sur de nouvelles données brutes (le pipeline gère tout)
nouveau_client = pd.DataFrame({
    'age': [35],
    'revenu': [52000],
    'nb_achats': [3],
    'anciennete_mois': [6],
    'ville': ['Paris'],
    'type_contrat': ['CDI'],
    'canal_acquisition': ['Web']
})

prediction = pipeline_charge.predict(nouveau_client)
proba = pipeline_charge.predict_proba(nouveau_client)[:, 1]
print(f"Prédiction : {'Churn' if prediction[0] else 'Pas de churn'}")
print(f"Probabilité de churn : {proba[0]:.2%}")
```

> 💡 **Conseil** : "Quand vous sauvegardez un modèle, sauvegardez le PIPELINE COMPLET (preprocessing + modèle). Ainsi, en production, vous passez les données brutes directement et le pipeline fait tout le travail."

---

## 🎯 Points clés à retenir

1. Le **feature engineering** est l'étape qui a le plus grand impact sur la performance (10-30%)
2. Les **features numériques** : log, ratio, polynomiales, binning
3. Les **features temporelles** : jour, heure, weekend, lag, rolling average, encodage cyclique
4. Les **features textuelles** : longueur, ponctuation, TF-IDF
5. Le **target encoding** est puissant mais attention au data leakage
6. **Filter methods** pour une sélection rapide, **RFECV** pour la sélection finale
7. **PCA** pour la réduction de dimension (normaliser avant !)
8. **Pipelines sklearn** = pas de data leakage + code reproductible + déploiement facile
9. **ColumnTransformer** pour traiter différemment les colonnes numériques et catégorielles
10. **Sauvegarder le pipeline complet**, jamais juste le modèle

## ✅ Checklist de validation

- [ ] Je sais créer des features numériques (log, ratio, polynomiales)
- [ ] Je sais extraire des features temporelles (lag, rolling, cyclique)
- [ ] Je connais les méthodes de sélection de features (filter, wrapper, embedded)
- [ ] Je sais utiliser PCA et interpréter le scree plot
- [ ] Je maîtrise Pipeline et ColumnTransformer
- [ ] Je sais intégrer le tuning dans un pipeline avec GridSearchCV
- [ ] Je sais sauvegarder et charger un pipeline complet
- [ ] Je comprends pourquoi le preprocessing doit être DANS le pipeline

---

[⬅️ Chapitre 8 : Évaluation et Métriques](08-evaluation-metriques.md) | [➡️ Chapitre 10 : MLOps](10-mlops-production.md)
