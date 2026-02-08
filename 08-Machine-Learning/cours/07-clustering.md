# Chapitre 7 : Clustering – Découvrir des Structures Cachées

## 🎯 Objectifs

- Comprendre le principe de l'apprentissage non supervisé et du clustering
- Maîtriser les algorithmes K-Means, DBSCAN et le clustering hiérarchique
- Savoir évaluer la qualité d'un clustering avec les bonnes métriques
- Choisir le bon algorithme de clustering selon la nature des données
- Visualiser et interpréter les résultats d'un clustering

---

## 1. 🧠 Introduction au clustering

### 1.1 Qu'est-ce que le clustering ?

Le clustering (ou partitionnement) est une technique d'**apprentissage non supervisé** : il n'y a **pas de labels** (pas de variable cible). L'objectif est de découvrir des **groupes naturels** (clusters) dans les données, de telle sorte que :

- Les éléments d'un même cluster soient **similaires** entre eux
- Les éléments de clusters différents soient **dissemblables**

C'est comme trier un tas de Lego par couleur sans qu'on vous ait dit quelles couleurs existent.

### 1.2 Cas d'usage en entreprise

| Domaine | Cas d'usage | Objectif |
|---|---|---|
| **Marketing** | Segmentation clients | Personnaliser les offres par profil |
| **E-commerce** | Segmentation produits | Recommandations, merchandising |
| **Cybersécurité** | Détection d'anomalies | Identifier les comportements suspects |
| **Biologie** | Groupes de gènes | Découvrir des familles génétiques |
| **Image** | Compression d'images | Réduire le nombre de couleurs |
| **Texte** | Topic modeling | Regrouper des documents similaires |
| **Finance** | Profils de risque | Catégoriser les clients par risque |

> 💡 **Conseil** : "Le clustering est un outil d'exploration, pas de prédiction. Utilisez-le pour comprendre vos données et générer des hypothèses, que vous pourrez ensuite valider avec des méthodes supervisées."

### 1.3 La distance, notion fondamentale

Tout algorithme de clustering repose sur une notion de **distance** (ou similarité) entre les points.

| Distance | Formule | Utilisation |
|---|---|---|
| **Euclidienne** | √(Σ(xi - yi)²) | Par défaut, données numériques continues |
| **Manhattan** | Σ|xi - yi| | Données sur grille, features indépendantes |
| **Cosinus** | 1 - cos(θ) | Texte (TF-IDF), données de haute dimension |
| **Minkowski** | (Σ|xi - yi|^p)^(1/p) | Généralisation (p=1: Manhattan, p=2: Euclidienne) |

> ⚠️ **Attention** : "La distance euclidienne est très sensible à l'échelle des variables. Une feature en milliers (salaire) dominera une feature en unités (âge). Il faut TOUJOURS normaliser avant le clustering !"

---

## 2. 📊 K-Means

### 2.1 Algorithme pas à pas

K-Means est l'algorithme de clustering le plus populaire. Son fonctionnement est simple et élégant :

1. **Initialisation** : Choisir K centroïdes aléatoires (ou avec K-Means++)
2. **Assignation** : Chaque point est assigné au centroïde le plus proche
3. **Mise à jour** : Recalculer chaque centroïde comme la moyenne de ses points
4. **Répéter** les étapes 2-3 jusqu'à convergence (les assignations ne changent plus)

### 2.2 Implémentation avec scikit-learn

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs

# Générer des données d'exemple
X, y_true = make_blobs(
    n_samples=500,
    n_features=2,
    centers=4,          # 4 clusters réels
    cluster_std=1.0,
    random_state=42
)

# ÉTAPE CRUCIALE : Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Appliquer K-Means
kmeans = KMeans(
    n_clusters=4,        # nombre de clusters
    init='k-means++',    # initialisation intelligente
    n_init=10,           # nombre d'initialisations (prendre la meilleure)
    max_iter=300,        # nombre max d'itérations
    random_state=42
)

# Entraîner et prédire
clusters = kmeans.fit_predict(X_scaled)

# Résultats
print(f"Centroïdes : \n{kmeans.cluster_centers_}")
print(f"Inertie (somme des distances) : {kmeans.inertia_:.2f}")
print(f"Nombre d'itérations : {kmeans.n_iter_}")

# Visualiser les clusters
plt.figure(figsize=(10, 6))
scatter = plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=clusters, cmap='viridis', alpha=0.6)
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    c='red', marker='X', s=200, label='Centroïdes'
)
plt.colorbar(scatter, label='Cluster')
plt.xlabel('Feature 1 (normalisée)')
plt.ylabel('Feature 2 (normalisée)')
plt.title('Résultat du K-Means (K=4)')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 **Conseil** : "Toujours normaliser les données avant K-Means. Sans normalisation, les features avec de grandes valeurs dominent la distance et le clustering est biaisé."

### 2.3 La méthode du coude (Elbow Method) pour choisir K

Le choix de K est la question centrale de K-Means. La méthode du coude trace l'**inertie** (somme des distances au centroïde) en fonction de K.

```python
# Méthode du coude
inertias = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

# Tracer la courbe du coude
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, 'bo-', linewidth=2)
plt.xlabel('Nombre de clusters (K)')
plt.ylabel('Inertie')
plt.title('Méthode du Coude – Choix de K')
plt.xticks(K_range)
plt.grid(True, alpha=0.3)

# Annoter le coude
plt.annotate('Coude probable',
    xy=(4, inertias[2]),
    xytext=(6, inertias[0]),
    arrowprops=dict(arrowstyle='->', color='red'),
    fontsize=12, color='red'
)
plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "La méthode du coude est parfois ambiguë (pas de coude net). Complétez-la toujours avec le silhouette score pour confirmer votre choix de K."

### 2.4 K-Means++ – Une meilleure initialisation

K-Means classique initialise les centroïdes aléatoirement, ce qui peut donner de mauvais résultats. K-Means++ utilise une initialisation intelligente :

1. Choisir le premier centroïde aléatoirement
2. Pour chaque centroïde suivant : choisir un point avec une probabilité proportionnelle à sa distance au centroïde le plus proche
3. Cela garantit que les centroïdes initiaux sont **bien espacés**

> 💡 **Conseil** : "K-Means++ est activé par défaut dans scikit-learn (`init='k-means++'`). Ne changez jamais ce paramètre. Il converge plus vite et donne de meilleurs résultats."

### 2.5 Limites de K-Means

| Limitation | Explication |
|---|---|
| **Clusters sphériques** | Assume que les clusters sont ronds et de taille similaire |
| **K doit être fixé** | Il faut choisir le nombre de clusters a priori |
| **Sensible aux outliers** | Les outliers déplacent les centroïdes |
| **Sensible à l'initialisation** | Peut converger vers un optimum local |
| **Pas adapté aux densités variables** | Clusters de densités différentes mal gérés |

> ⚠️ **Attention** : "K-Means assume des clusters sphériques de taille similaire. Si vos données ont des clusters en forme de croissant, allongés ou de densités très différentes, K-Means échouera. Utilisez DBSCAN dans ce cas."

---

## 3. 🔍 DBSCAN

### 3.1 Principe : clustering par densité

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) regroupe les points qui sont **densément connectés** et identifie les points isolés comme du **bruit** (outliers).

Deux paramètres clés :

- **eps** (epsilon) : rayon de voisinage
- **min_samples** : nombre minimum de points dans le voisinage pour former un cluster

Trois types de points :

1. **Core points** : au moins `min_samples` points dans un rayon `eps`
2. **Border points** : dans le voisinage d'un core point mais pas core eux-mêmes
3. **Noise points** : ni core, ni border → outliers (label = -1)

### 3.2 Implémentation

```python
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons

# Données en forme de croissants (non sphériques)
X_moons, _ = make_moons(n_samples=500, noise=0.1, random_state=42)
X_moons_scaled = StandardScaler().fit_transform(X_moons)

# DBSCAN
dbscan = DBSCAN(
    eps=0.3,          # rayon de voisinage
    min_samples=5,    # minimum de points pour un cluster
    metric='euclidean'
)

clusters_db = dbscan.fit_predict(X_moons_scaled)

# Résultats
n_clusters = len(set(clusters_db)) - (1 if -1 in clusters_db else 0)
n_noise = list(clusters_db).count(-1)

print(f"Nombre de clusters trouvés : {n_clusters}")
print(f"Points de bruit (outliers) : {n_noise}")

# Visualisation
plt.figure(figsize=(10, 6))
plt.scatter(
    X_moons_scaled[:, 0], X_moons_scaled[:, 1],
    c=clusters_db, cmap='viridis', alpha=0.7
)
# Mettre en évidence les outliers
mask_bruit = clusters_db == -1
plt.scatter(
    X_moons_scaled[mask_bruit, 0],
    X_moons_scaled[mask_bruit, 1],
    c='red', marker='x', s=100, label='Bruit (outliers)'
)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title(f'DBSCAN : {n_clusters} clusters, {n_noise} outliers')
plt.legend()
plt.tight_layout()
plt.show()
```

### 3.3 Comment choisir eps ?

Le **knee plot des k-distances** est la méthode standard pour trouver eps :

```python
from sklearn.neighbors import NearestNeighbors

# Calculer la distance au k-ième voisin le plus proche
k = 5  # même valeur que min_samples
nn = NearestNeighbors(n_neighbors=k)
nn.fit(X_moons_scaled)
distances, _ = nn.kneighbors(X_moons_scaled)

# Trier les distances au k-ième voisin
k_distances = np.sort(distances[:, k-1])

# Tracer le graphique
plt.figure(figsize=(8, 5))
plt.plot(k_distances, linewidth=2)
plt.xlabel('Points (triés)')
plt.ylabel(f'Distance au {k}-ème voisin')
plt.title(f'Knee Plot – Choix de eps (k={k})')
plt.grid(True, alpha=0.3)

# Le coude indique la valeur de eps
plt.axhline(y=0.3, color='red', linestyle='--', label=f'eps ≈ 0.3')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "Utilisez le knee plot des k-distances pour trouver eps. Le coude dans la courbe correspond au seuil naturel entre les points denses (clusters) et les points isolés (bruit). Fixez min_samples = 2 * n_features comme point de départ."

### 3.4 Avantages et inconvénients de DBSCAN

| Avantages | Inconvénients |
|---|---|
| Détecte les **formes arbitraires** | Sensible aux paramètres eps et min_samples |
| **Gère le bruit** (outliers automatiques) | Pas adapté aux **densités variables** |
| Pas besoin de spécifier K | **Difficile** en haute dimension |
| Robuste aux outliers | Pas de `predict()` pour de nouvelles données |
| Déterministe (pas d'initialisation aléatoire) | Peut échouer si les clusters ont des densités très différentes |

> 💡 **Conseil** : "DBSCAN est excellent pour la détection d'anomalies : les points étiquetés comme « bruit » (-1) sont vos anomalies. C'est souvent plus intuitif que les algorithmes dédiés à la détection d'anomalies."

---

## 4. 🌳 Clustering hiérarchique

### 4.1 Principe

Le clustering hiérarchique construit une **hiérarchie de clusters** représentée sous forme de **dendrogramme**. Deux approches :

- **Agglomératif (bottom-up)** : chaque point commence seul → on fusionne progressivement les clusters les plus proches
- **Divisif (top-down)** : tous les points commencent dans un seul cluster → on divise progressivement

En pratique, l'approche **agglomérative** est la plus utilisée.

### 4.2 Types de linkage

Le linkage définit comment on mesure la distance **entre deux clusters** :

| Linkage | Distance entre clusters | Propriétés |
|---|---|---|
| **Single** | Min des distances point-à-point | Détecte les formes allongées, sensible au bruit |
| **Complete** | Max des distances point-à-point | Clusters compacts, sensible aux outliers |
| **Average** | Moyenne des distances | Compromis entre single et complete |
| **Ward** | Minimise la variance intra-cluster | Clusters sphériques et de taille similaire (le plus utilisé) |

### 4.3 Implémentation et dendrogramme

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.datasets import make_blobs

# Données d'exemple
X_hier, _ = make_blobs(n_samples=150, centers=4, cluster_std=1.0, random_state=42)
X_hier_scaled = StandardScaler().fit_transform(X_hier)

# Calculer le linkage pour le dendrogramme
Z = linkage(X_hier_scaled, method='ward', metric='euclidean')

# Tracer le dendrogramme
plt.figure(figsize=(14, 7))
dendrogram(
    Z,
    truncate_mode='level',
    p=5,                     # afficher 5 niveaux
    leaf_rotation=90,
    leaf_font_size=8,
    color_threshold=7        # seuil de couleur pour les clusters
)
plt.xlabel('Échantillons')
plt.ylabel('Distance')
plt.title('Dendrogramme – Clustering Hiérarchique (Ward)')
plt.axhline(y=7, color='red', linestyle='--', label='Seuil de coupe (4 clusters)')
plt.legend()
plt.tight_layout()
plt.show()

# Appliquer le clustering agglomératif
agg = AgglomerativeClustering(
    n_clusters=4,       # ou distance_threshold pour couper automatiquement
    linkage='ward'
)

clusters_hier = agg.fit_predict(X_hier_scaled)

# Visualiser
plt.figure(figsize=(8, 6))
plt.scatter(X_hier_scaled[:, 0], X_hier_scaled[:, 1], c=clusters_hier, cmap='viridis', alpha=0.7)
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Clustering Hiérarchique Agglomératif (Ward, K=4)')
plt.colorbar(label='Cluster')
plt.tight_layout()
plt.show()
```

> 💡 **Conseil** : "Le dendrogramme est un outil visuel puissant. Le bon nombre de clusters correspond souvent à l'endroit où les branches du dendrogramme sont les plus longues avant de fusionner. C'est là qu'il faut « couper »."

### 4.4 Quand utiliser le clustering hiérarchique ?

| Situation | Recommandé ? |
|---|---|
| Explorer la structure hiérarchique des données | Oui |
| Petit dataset (< 10 000 points) | Oui |
| Grand dataset (> 50 000 points) | Non (complexité O(n³) avec Ward) |
| Besoin de visualiser la hiérarchie | Oui (dendrogramme) |
| Clusters de formes complexes | Dépend du linkage |

---

## 5. 📊 MÉTRIQUES DE CLUSTERING – Évaluer sans labels

L'évaluation du clustering est un défi particulier car il n'y a **pas de vérité terrain**. On utilise des métriques **intrinsèques** qui mesurent la qualité de la structure trouvée.

### 5.1 Silhouette Score (-1 à 1)

Le silhouette score mesure à quel point chaque point est bien assigné à son cluster. Pour chaque point i :

- **a(i)** = distance moyenne aux autres points du **même cluster** (cohésion)
- **b(i)** = distance moyenne aux points du **cluster le plus proche** (séparation)
- **s(i)** = (b(i) - a(i)) / max(a(i), b(i))

| Valeur | Interprétation |
|---|---|
| **s ≈ 1** | Point bien assigné, loin des autres clusters |
| **s ≈ 0** | Point à la frontière entre deux clusters |
| **s < 0** | Point probablement mal assigné |

```python
from sklearn.metrics import silhouette_score, silhouette_samples

# Calculer le silhouette score global
sil_score = silhouette_score(X_scaled, clusters)
print(f"Silhouette Score global : {sil_score:.4f}")

# Silhouette score pour chaque K
sil_scores = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    sil_scores.append(score)
    print(f"K={k} : Silhouette = {score:.4f}")

# Tracer
plt.figure(figsize=(8, 5))
plt.plot(K_range, sil_scores, 'go-', linewidth=2)
plt.xlabel('Nombre de clusters (K)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score en fonction de K')
plt.xticks(K_range)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

#### Silhouette Plot – Visualisation détaillée

```python
from sklearn.metrics import silhouette_samples

# Silhouette plot pour K=4
km = KMeans(n_clusters=4, init='k-means++', n_init=10, random_state=42)
labels = km.fit_predict(X_scaled)
sil_values = silhouette_samples(X_scaled, labels)

fig, ax = plt.subplots(figsize=(8, 6))
y_lower = 10

for i in range(4):
    # Valeurs de silhouette pour le cluster i
    cluster_sil = sil_values[labels == i]
    cluster_sil.sort()

    size_cluster = len(cluster_sil)
    y_upper = y_lower + size_cluster

    ax.fill_betweenx(
        np.arange(y_lower, y_upper),
        0, cluster_sil,
        alpha=0.7, label=f'Cluster {i}'
    )
    y_lower = y_upper + 10

# Ligne verticale pour le score moyen
sil_avg = silhouette_score(X_scaled, labels)
ax.axvline(x=sil_avg, color='red', linestyle='--', label=f'Moyenne ({sil_avg:.3f})')

ax.set_xlabel('Silhouette Score')
ax.set_ylabel('Échantillons (par cluster)')
ax.set_title('Silhouette Plot (K=4)')
ax.legend()
plt.tight_layout()
plt.show()
```

> 💡 **Conseil de pro** : "Le silhouette score est la métrique la plus universelle pour le clustering. Visez un score > 0.5 pour un bon clustering. En dessous de 0.25, la structure est faible. Utilisez le silhouette plot pour identifier les clusters problématiques."

### 5.2 Inertie (K-Means)

L'inertie est la **somme des distances** de chaque point à son centroïde le plus proche. C'est la métrique optimisée par K-Means.

- **Plus l'inertie est faible**, plus les clusters sont compacts
- L'inertie diminue **toujours** quand K augmente (elle atteint 0 quand K = n)
- On cherche le **coude** dans la courbe inertie vs K

```python
# Déjà calculée dans la section méthode du coude
print(f"Inertie (K=4) : {kmeans.inertia_:.2f}")
```

> ⚠️ **Attention** : "L'inertie seule n'est pas suffisante pour choisir K car elle diminue toujours. Elle doit être combinée avec le silhouette score ou d'autres métriques."

### 5.3 Calinski-Harabasz Index

Le Calinski-Harabasz Index (aussi appelé Variance Ratio Criterion) mesure le **ratio entre la dispersion inter-clusters et la dispersion intra-clusters**. Plus il est élevé, mieux c'est.

```python
from sklearn.metrics import calinski_harabasz_score

ch_score = calinski_harabasz_score(X_scaled, clusters)
print(f"Calinski-Harabasz Index : {ch_score:.2f}")

# Pour chaque K
ch_scores = []
for k in K_range:
    km = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    score = calinski_harabasz_score(X_scaled, labels)
    ch_scores.append(score)
    print(f"K={k} : CH = {score:.2f}")
```

### 5.4 Davies-Bouldin Index

Le Davies-Bouldin Index mesure la **similarité entre clusters**. Plus il est **bas**, mieux c'est (les clusters sont bien séparés).

```python
from sklearn.metrics import davies_bouldin_score

db_score = davies_bouldin_score(X_scaled, clusters)
print(f"Davies-Bouldin Index : {db_score:.4f}")
```

### 5.5 Table comparative des métriques de clustering

| Métrique | Range | Meilleur si | Avantages | Limites |
|---|---|---|---|---|
| **Silhouette Score** | -1 à 1 | Proche de 1 | Universelle, intuitive | O(n²) pour grands datasets |
| **Inertie** | 0 à +∞ | Bas (coude) | Simple, native K-Means | Diminue toujours avec K |
| **Calinski-Harabasz** | 0 à +∞ | Haut | Rapide à calculer | Favorise les clusters sphériques |
| **Davies-Bouldin** | 0 à +∞ | Bas | Simple d'interprétation | Favorise les clusters convexes |

> 💡 **Conseil** : "Utilisez toujours plusieurs métriques en parallèle. Si le silhouette score, le Calinski-Harabasz et la méthode du coude convergent vers le même K, vous pouvez être confiant dans votre choix."

---

## 6. 📈 Comment améliorer un clustering

### 6.1 Checklist d'amélioration

1. **Normaliser les données** : StandardScaler ou MinMaxScaler (indispensable !)
2. **Choisir le bon K** : méthode du coude + silhouette score
3. **Sélectionner les bonnes features** : éliminer les features non pertinentes
4. **Essayer plusieurs algorithmes** : K-Means, DBSCAN, Hiérarchique
5. **Réduire la dimension** : PCA ou t-SNE pour explorer visuellement
6. **Traiter les outliers** : les retirer ou utiliser DBSCAN
7. **Interpréter les clusters** : statistiques descriptives par cluster

### 6.2 Visualisation avec PCA pour vérification

```python
from sklearn.decomposition import PCA

# Réduire à 2D pour visualisation
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"Variance expliquée : {pca.explained_variance_ratio_.sum():.2%}")

# Visualiser les clusters dans l'espace PCA
plt.figure(figsize=(10, 7))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis', alpha=0.6)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('Visualisation des clusters (PCA 2D)')
plt.colorbar(scatter, label='Cluster')
plt.tight_layout()
plt.show()
```

### 6.3 Profiling des clusters

```python
# Créer un DataFrame avec les clusters
df_clusters = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
df_clusters['cluster'] = clusters

# Statistiques par cluster
profil = df_clusters.groupby('cluster').agg(['mean', 'std', 'count'])
print("Profil des clusters :")
print(profil)

# Taille des clusters
print("\nTaille des clusters :")
print(df_clusters['cluster'].value_counts().sort_index())
```

> 💡 **Conseil de pro** : "Un clustering n'a de valeur que si les clusters sont interprétables et actionnables. Après le clustering, faites TOUJOURS un profiling : quelles sont les caractéristiques de chaque groupe ? Donnez des noms parlants à vos clusters (« Clients premium », « Acheteurs occasionnels », etc.)."

### 6.4 Comparaison des algorithmes de clustering

| Critère | K-Means | DBSCAN | Hiérarchique |
|---|---|---|---|
| **Forme des clusters** | Sphérique | Arbitraire | Dépend du linkage |
| **Nombre de clusters** | À fixer (K) | Automatique | À fixer ou seuil |
| **Gestion du bruit** | Non | Oui (outliers) | Non |
| **Scalabilité** | Excellente (O(nKT)) | Bonne (O(n log n)) | Faible (O(n²) à O(n³)) |
| **Taille max** | Millions | Centaines de milliers | Dizaines de milliers |
| **Reproductibilité** | Non (init aléatoire) | Oui (déterministe) | Oui |
| **Interprétabilité** | Centroïdes | Densité | Dendrogramme |

> 💡 **Conseil** : "Pour choisir votre algorithme : (1) Essayez K-Means en premier car c'est le plus rapide. (2) Si les clusters ne sont pas sphériques ou s'il y a des outliers, passez à DBSCAN. (3) Si vous voulez explorer la hiérarchie des données, utilisez le clustering hiérarchique avec un dendrogramme."

---

## 🎯 Points clés à retenir

1. Le clustering est un apprentissage **non supervisé** : pas de labels, on découvre des groupes
2. **K-Means** est rapide et simple mais assume des clusters sphériques
3. **DBSCAN** détecte les formes arbitraires et gère les outliers automatiquement
4. Le **clustering hiérarchique** fournit un dendrogramme pour explorer la structure
5. **Toujours normaliser** les données avant le clustering (StandardScaler)
6. Le **silhouette score** est la métrique la plus fiable (viser > 0.5)
7. Combiner **plusieurs métriques** : silhouette, Calinski-Harabasz, Davies-Bouldin
8. La **méthode du coude** aide à choisir K mais n'est pas toujours claire
9. Toujours **profiler les clusters** pour les rendre interprétables
10. **Visualiser avec PCA** 2D pour vérifier la qualité du clustering

## ✅ Checklist de validation

- [ ] Je comprends la différence entre apprentissage supervisé et non supervisé
- [ ] Je sais appliquer K-Means et choisir K (coude + silhouette)
- [ ] Je sais utiliser DBSCAN et trouver les bons paramètres (eps, min_samples)
- [ ] Je sais lire un dendrogramme et choisir où couper
- [ ] Je maîtrise les 4 métriques de clustering (silhouette, inertie, CH, DB)
- [ ] Je sais normaliser les données avant le clustering
- [ ] Je sais profiler et interpréter les clusters obtenus
- [ ] Je sais choisir entre K-Means, DBSCAN et Hiérarchique

---

[⬅️ Chapitre 6 : Méthodes d'Ensemble](06-ensemble-methods.md) | [➡️ Chapitre 8 : Évaluation et Métriques](08-evaluation-metriques.md)
