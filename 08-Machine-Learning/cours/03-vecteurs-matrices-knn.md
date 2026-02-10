# Chapitre 3 : Vecteurs, Matrices et KNN — Les Maths comme Outils

## 🎯 Objectifs

- Comprendre ce qu'est un vecteur et pourquoi c'est la base du ML
- Savoir représenter des données sous forme de vecteurs et de matrices
- Calculer des distances entre points (euclidienne, Manhattan)
- Faire le lien entre matrices et DataFrames pandas
- Implémenter l'algorithme KNN from scratch puis avec scikit-learn
- Visualiser des clusters et comprendre la notion de similarité

---

## 1. 🧠 Intuition : Un vecteur = une fiche d'identité numérique

### 1.1 L'idée fondamentale

En Machine Learning, **tout doit être transformé en nombres**. Un vecteur, c'est simplement une **liste ordonnée de nombres** qui décrit quelque chose.

> 💡 **Conseil** : "Pensez à un vecteur comme une **fiche d'identité numérique**. Chaque nombre capture une caractéristique mesurable d'un objet, d'une personne ou d'un événement."

### 1.2 Exemple concret : décrire un client

Imaginons que vous travaillez dans une banque. Comment décrire un client avec des nombres ?

```
Client Alice :
  - Âge : 35 ans
  - Salaire annuel : 45 000 €
  - Ancienneté : 3 ans
  - Nombre de produits : 2

→ Vecteur Alice = [35, 45000, 3, 2]
```

```
Client Bob :
  - Âge : 28 ans
  - Salaire annuel : 32 000 €
  - Ancienneté : 1 an
  - Nombre de produits : 1

→ Vecteur Bob = [28, 32000, 1, 1]
```

Chaque client est maintenant un **point dans un espace à 4 dimensions**. On peut les comparer, les regrouper, mesurer leur ressemblance.

### 1.3 En Python avec NumPy

```python
import numpy as np

# Chaque client est un vecteur
alice = np.array([35, 45000, 3, 2])
bob = np.array([28, 32000, 1, 1])
charlie = np.array([42, 60000, 10, 4])

print(f"Vecteur Alice : {alice}")
print(f"Dimension : {alice.shape[0]} caractéristiques")
print(f"Type : {type(alice)}")
```

### 1.4 Pourquoi des vecteurs et pas juste des listes Python ?

| Aspect | Liste Python | Vecteur NumPy |
|--------|-------------|---------------|
| **Opérations mathématiques** | Impossible directement | Natives et rapides |
| **Performance** | Lente (boucles) | Rapide (opérations vectorisées) |
| **Mémoire** | Plus gourmande | Optimisée (types fixes) |
| **Utilisation ML** | Inadaptée | Standard du domaine |

```python
# Avec une liste Python (ne marche PAS comme attendu)
liste_a = [1, 2, 3]
liste_b = [4, 5, 6]
print(liste_a + liste_b)  # [1, 2, 3, 4, 5, 6] → concaténation !

# Avec NumPy (opérations élément par élément)
vec_a = np.array([1, 2, 3])
vec_b = np.array([4, 5, 6])
print(vec_a + vec_b)  # [5, 7, 9] → addition vectorielle !
print(vec_a * 2)      # [2, 4, 6] → multiplication par un scalaire
print(vec_a * vec_b)  # [4, 10, 18] → multiplication élément par élément
```

> ⚠️ **Attention** : "En Python pur, `+` concatène les listes. Avec NumPy, `+` additionne élément par élément. C'est un piège classique pour les débutants."

---

## 2. 📊 Visualisation : Points dans l'espace

### 2.1 Cas 2D : deux caractéristiques

Quand un vecteur n'a que **2 dimensions**, on peut le visualiser comme un point sur un graphique classique (x, y).

```python
import matplotlib.pyplot as plt
import numpy as np

# Des clients décrits par (âge, salaire_en_milliers)
clients = np.array([
    [25, 30],  # Client 1
    [35, 45],  # Client 2
    [45, 60],  # Client 3
    [23, 28],  # Client 4
    [50, 80],  # Client 5
    [30, 35],  # Client 6
    [40, 55],  # Client 7
    [22, 25],  # Client 8
])

labels = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

plt.figure(figsize=(10, 7))
plt.scatter(clients[:, 0], clients[:, 1], s=100, c='steelblue', edgecolors='black')

for i, label in enumerate(labels):
    plt.annotate(label, (clients[i, 0] + 0.5, clients[i, 1] + 1))

plt.xlabel("Âge")
plt.ylabel("Salaire (k€)")
plt.title("Chaque client = un point dans l'espace 2D")
plt.grid(True, alpha=0.3)
plt.show()
```

```
    Salaire (k€)
    80 │                              ● C5
       │
    60 │                    ● C3
    55 │                 ● C7
    45 │          ● C2
    35 │       ● C6
    30 │    ● C1
    28 │   ● C4
    25 │  ● C8
       └──────────────────────────────────── Âge
        22  25  30  35  40  45  50
```

### 2.2 Cas 3D : trois caractéristiques

Avec 3 dimensions, on peut encore visualiser (x, y, z) :

```python
from mpl_toolkits.mplot3d import Axes3D

# Clients décrits par (âge, salaire_k, ancienneté)
clients_3d = np.array([
    [25, 30, 1],
    [35, 45, 5],
    [45, 60, 12],
    [28, 32, 2],
    [50, 80, 20],
])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(clients_3d[:, 0], clients_3d[:, 1], clients_3d[:, 2],
           s=100, c='steelblue', edgecolors='black')

ax.set_xlabel("Âge")
ax.set_ylabel("Salaire (k€)")
ax.set_zlabel("Ancienneté (ans)")
ax.set_title("Clients dans un espace 3D")
plt.show()
```

### 2.3 Au-delà de 3 dimensions

En ML, on travaille souvent avec **des dizaines ou des centaines de dimensions**. On ne peut plus visualiser directement, mais les maths fonctionnent exactement pareil !

| Dimensions | Visualisable ? | Exemple |
|-----------|---------------|---------|
| 2 | Oui (graphique x, y) | Âge + salaire |
| 3 | Oui (graphique 3D) | Âge + salaire + ancienneté |
| 4 à 10 | Non, mais réduction possible (PCA, t-SNE) | Fiche client complète |
| 100+ | Non, mais les algorithmes gèrent | Pixels d'une image |

> 💡 **Conseil** : "Ne vous inquiétez pas de ne pas pouvoir visualiser 50 dimensions. Les algorithmes de ML travaillent dans ces espaces de haute dimension sans aucun problème. La distance euclidienne fonctionne en 2D, 3D ou 1000D exactement de la même manière."

---

## 3. 📏 La distance entre deux points = « ressemblance »

### 3.1 L'intuition

La question centrale du ML est souvent : **est-ce que ces deux observations se ressemblent ?**

Pour y répondre, on mesure la **distance** entre deux vecteurs. Plus la distance est **petite**, plus les observations sont **similaires**.

```
    Similaires                          Différents
    ● ●                                ●              ●
    (distance faible)                  (distance élevée)
```

### 3.2 Distance euclidienne

C'est la distance "en ligne droite" — celle que vous connaissez déjà !

**En 2D (théorème de Pythagore)** :

```
    B (x₂, y₂)
    │╲
    │  ╲  d = distance
    │    ╲
    │______╲
    A (x₁, y₁)

    d = √[(x₂ - x₁)² + (y₂ - y₁)²]
```

**Exemple concret** :

```
Client A = (âge: 30, salaire: 40k)
Client B = (âge: 35, salaire: 50k)

d(A, B) = √[(35 - 30)² + (50 - 40)²]
        = √[25 + 100]
        = √125
        ≈ 11.18
```

**Généralisation à N dimensions** :

```
d(A, B) = √[(a₁ - b₁)² + (a₂ - b₂)² + ... + (aₙ - bₙ)²]
```

La formule est identique, on additionne simplement plus de termes.

```python
import numpy as np

def distance_euclidienne(a, b):
    """Calcule la distance euclidienne entre deux vecteurs."""
    return np.sqrt(np.sum((a - b) ** 2))

# Clients
alice = np.array([35, 45000, 3])
bob = np.array([28, 32000, 1])
charlie = np.array([34, 44000, 4])

# Distances
d_alice_bob = distance_euclidienne(alice, bob)
d_alice_charlie = distance_euclidienne(alice, charlie)

print(f"Distance Alice-Bob     : {d_alice_bob:.2f}")
print(f"Distance Alice-Charlie : {d_alice_charlie:.2f}")
print(f"\n→ Alice est plus proche de Charlie que de Bob")

# Avec NumPy directement (raccourci)
d = np.linalg.norm(alice - bob)
print(f"\nAvec np.linalg.norm : {d:.2f}")
```

### 3.3 Distance de Manhattan

Aussi appelée "distance L1" ou "distance du taxi" — c'est la distance quand on ne peut se déplacer que **en ligne droite** (comme dans les rues de Manhattan).

```
    B ─ ─ ─ ─ ─ ┐
                 │
    Manhattan    │  (on suit les rues)
                 │
    A ─ ─ ─ ─ ─ ┘

    vs.

    B
     ╲
      ╲  Euclidienne (en diagonale)
       ╲
        A
```

**Formule** :

```
d_manhattan(A, B) = |a₁ - b₁| + |a₂ - b₂| + ... + |aₙ - bₙ|
```

On somme les **valeurs absolues** des différences, au lieu de les mettre au carré.

```python
def distance_manhattan(a, b):
    """Calcule la distance de Manhattan entre deux vecteurs."""
    return np.sum(np.abs(a - b))

# Comparaison
alice = np.array([35, 45, 3])
bob = np.array([28, 32, 1])

d_eucl = distance_euclidienne(alice, bob)
d_manh = distance_manhattan(alice, bob)

print(f"Distance euclidienne : {d_eucl:.2f}")
print(f"Distance de Manhattan : {d_manh:.2f}")
```

### 3.4 Comparaison des distances

| Distance | Formule | Quand l'utiliser | Sensibilité outliers |
|----------|---------|-----------------|---------------------|
| **Euclidienne** (L2) | √(Σ(aᵢ - bᵢ)²) | Cas général, données continues | Haute (carré amplifie) |
| **Manhattan** (L1) | Σ\|aᵢ - bᵢ\| | Données avec outliers, features indépendantes | Plus robuste |
| **Minkowski** (Lp) | (Σ\|aᵢ - bᵢ\|ᵖ)^(1/p) | Généralisation (p=1 → Manhattan, p=2 → Euclidienne) | Dépend de p |

> ⚠️ **Attention** : "Si vos features ont des échelles très différentes (âge: 20-60, salaire: 20000-100000), la distance sera **dominée par le salaire**. Il faut **normaliser** les données avant de calculer des distances ! C'est une erreur très fréquente."

### 3.5 L'importance de la normalisation

```python
from sklearn.preprocessing import StandardScaler

# Données brutes (échelles très différentes)
clients = np.array([
    [35, 45000, 3],  # [âge, salaire, ancienneté]
    [28, 32000, 1],
    [34, 44000, 4],
])

# Sans normalisation : le salaire domine
d_brut = np.linalg.norm(clients[0] - clients[1])
print(f"Distance brute Alice-Bob : {d_brut:.2f}")  # ~13000 (dominé par salaire)

# Avec normalisation (StandardScaler : moyenne=0, écart-type=1)
scaler = StandardScaler()
clients_norm = scaler.fit_transform(clients)
print(f"\nDonnées normalisées :\n{clients_norm}")

d_norm = np.linalg.norm(clients_norm[0] - clients_norm[1])
print(f"\nDistance normalisée Alice-Bob : {d_norm:.2f}")  # Toutes les features comptent
```

---

## 4. 🗂️ Matrices = Tableau de données

### 4.1 Qu'est-ce qu'une matrice ?

Une **matrice** est un tableau rectangulaire de nombres. Si un vecteur est une **ligne** (un seul client), une matrice c'est **toutes les lignes empilées** (tous les clients).

```
                     âge   salaire   ancienneté   produits
                   ┌─────┬─────────┬────────────┬──────────┐
   Alice (ligne 0) │  35 │  45000  │     3      │    2     │
   Bob   (ligne 1) │  28 │  32000  │     1      │    1     │
   Charlie (l. 2)  │  42 │  60000  │    10      │    4     │
   Diana (ligne 3) │  31 │  38000  │     2      │    2     │
                   └─────┴─────────┴────────────┴──────────┘

   → Matrice de dimension (4, 4) = 4 lignes × 4 colonnes
   → 4 échantillons (samples), 4 caractéristiques (features)
```

### 4.2 En NumPy

```python
import numpy as np

# Créer une matrice
clients = np.array([
    [35, 45000, 3, 2],   # Alice
    [28, 32000, 1, 1],   # Bob
    [42, 60000, 10, 4],  # Charlie
    [31, 38000, 2, 2],   # Diana
])

print(f"Shape : {clients.shape}")         # (4, 4)
print(f"Nombre de clients : {clients.shape[0]}")    # 4
print(f"Nombre de features : {clients.shape[1]}")   # 4

# Accéder à un client (une ligne)
print(f"\nAlice : {clients[0]}")          # [35, 45000, 3, 2]

# Accéder à une feature (une colonne)
print(f"Tous les âges : {clients[:, 0]}") # [35, 28, 42, 31]

# Accéder à une valeur précise
print(f"Salaire de Bob : {clients[1, 1]}")  # 32000
```

### 4.3 Le lien avec pandas DataFrame

En pratique, on utilise souvent **pandas** pour manipuler les données, mais sous le capot, un DataFrame contient un tableau NumPy.

```python
import pandas as pd

# Créer un DataFrame à partir de la matrice
df = pd.DataFrame(
    clients,
    columns=['age', 'salaire', 'anciennete', 'nb_produits'],
    index=['Alice', 'Bob', 'Charlie', 'Diana']
)

print(df)
print(f"\nType des valeurs sous-jacentes : {type(df.values)}")

# Convertir DataFrame → matrice NumPy
X = df.values  # ou df.to_numpy()
print(f"\nMatrice NumPy :\n{X}")
print(f"Shape : {X.shape}")
```

| Concept | NumPy (ndarray) | pandas (DataFrame) |
|---------|----------------|-------------------|
| **Structure** | Tableau numérique brut | Tableau avec noms de colonnes et index |
| **Utilisation** | Calculs mathématiques rapides | Manipulation et exploration de données |
| **Accès colonne** | `matrice[:, 0]` | `df['age']` ou `df.age` |
| **Accès ligne** | `matrice[0]` | `df.iloc[0]` ou `df.loc['Alice']` |
| **Types** | Un seul type par matrice | Types mixtes par colonne |
| **Quand l'utiliser** | Calculs, algorithmes ML | Chargement, nettoyage, EDA |

### 4.4 La convention X et y en ML

En Machine Learning, on sépare toujours les **features** (X) de la **target** (y) :

```python
# X = matrice des features (ce qu'on observe)
# y = vecteur de la target (ce qu'on veut prédire)

# Exemple : prédire si un client va résilier (churn)
df = pd.DataFrame({
    'age': [35, 28, 42, 31, 55],
    'salaire': [45000, 32000, 60000, 38000, 75000],
    'anciennete': [3, 1, 10, 2, 15],
    'churn': [0, 1, 0, 1, 0]  # 0 = reste, 1 = part
})

# Séparer features et target
X = df[['age', 'salaire', 'anciennete']].values  # Matrice (5, 3)
y = df['churn'].values                            # Vecteur (5,)

print(f"X shape : {X.shape}")  # (5, 3)
print(f"y shape : {y.shape}")  # (5,)
print(f"\nX :\n{X}")
print(f"\ny : {y}")
```

```
Convention ML :
                                        Target
    Features (X)                         (y)
┌─────┬─────────┬────────────┐      ┌────────┐
│ 35  │  45000  │     3      │      │   0    │
│ 28  │  32000  │     1      │      │   1    │
│ 42  │  60000  │    10      │      │   0    │
│ 31  │  38000  │     2      │      │   1    │
│ 55  │  75000  │    15      │      │   0    │
└─────┴─────────┴────────────┘      └────────┘
  n_samples × n_features              n_samples
```

> 💡 **Conseil** : "En scikit-learn, **X** est toujours une matrice 2D (n_samples, n_features) et **y** est toujours un vecteur 1D (n_samples,). Respecter cette convention vous évitera beaucoup d'erreurs."

### 4.5 Opérations utiles sur les matrices

```python
# Opérations statistiques par colonne
print(f"Moyenne par feature : {np.mean(X, axis=0)}")
print(f"Écart-type par feature : {np.std(X, axis=0)}")
print(f"Min par feature : {np.min(X, axis=0)}")
print(f"Max par feature : {np.max(X, axis=0)}")

# Transposée : échanger lignes et colonnes
print(f"\nX shape : {X.shape}")
print(f"X transposée shape : {X.T.shape}")

# Produit matriciel (utile pour la régression linéaire)
# y_pred = X @ w  (prédiction = features × poids)
w = np.array([0.1, 0.00005, 0.5])  # Poids fictifs
y_pred = X @ w  # Produit matriciel
print(f"\nPrédictions : {y_pred}")
```

---

## 5. 🤖 Application : l'algorithme KNN (K-Nearest Neighbors)

### 5.1 L'intuition (sans formule)

L'idée de KNN est **incroyablement simple** :

> Pour prédire la classe d'un nouveau point, on regarde les **K points les plus proches** (les "voisins") et on **vote à la majorité**.

**Analogie** : vous déménagez dans un nouveau quartier. Pour deviner si vous allez aimer le restaurant du coin, vous demandez l'avis de vos **5 voisins les plus proches**. Si 4 sur 5 disent "c'est bon", vous prédisez que c'est bon.

```
    Nouveau client (?)
         │
         ▼
    On regarde les K=5 voisins les plus proches
         │
         ▼
    3 voisins = "ne résilie pas" (●)
    2 voisins = "résilie" (▲)
         │
         ▼
    Prédiction : "ne résilie pas" (majorité = ●)
```

```
   Salaire
    │
    │  ▲         ● ●
    │     ▲    ●
    │        ❓←── Nouveau point
    │     ●      ●
    │  ▲     ●
    │
    └───────────────── Âge

   ● = Ne résilie pas    ▲ = Résilie

   Les 5 plus proches voisins de ❓ :
   → 3 sont ● et 2 sont ▲
   → Prédiction : ● (ne résilie pas)
```

### 5.2 L'algorithme étape par étape

```
Algorithme KNN :
─────────────────────────────────────────────────────
1. Choisir K (nombre de voisins, ex: K=5)
2. Pour un nouveau point X_new :
   a. Calculer la distance entre X_new et TOUS les points d'entraînement
   b. Trier les distances par ordre croissant
   c. Sélectionner les K points les plus proches
   d. Compter les classes parmi ces K voisins
   e. Retourner la classe majoritaire
─────────────────────────────────────────────────────
```

### 5.3 KNN from scratch (~20 lignes)

```python
import numpy as np
from collections import Counter

class KNNFromScratch:
    def __init__(self, k=5):
        self.k = k

    def fit(self, X_train, y_train):
        """Stocker les données d'entraînement (pas d'apprentissage réel)."""
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        """Prédire la classe pour chaque point de X_test."""
        return np.array([self._predict_one(x) for x in X_test])

    def _predict_one(self, x):
        """Prédire la classe pour UN seul point."""
        # 1. Calculer les distances avec tous les points d'entraînement
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))

        # 2. Trouver les indices des K plus proches
        k_indices = np.argsort(distances)[:self.k]

        # 3. Récupérer les classes de ces K voisins
        k_labels = self.y_train[k_indices]

        # 4. Voter : la classe la plus fréquente gagne
        most_common = Counter(k_labels).most_common(1)
        return most_common[0][0]
```

### 5.4 Tester notre KNN from scratch

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Générer un dataset simple
X, y = make_classification(
    n_samples=200,
    n_features=2,
    n_redundant=0,
    n_informative=2,
    n_clusters_per_class=1,
    random_state=42
)

# Séparer train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entraîner et prédire avec notre KNN
knn = KNNFromScratch(k=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# Évaluer
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy de notre KNN : {accuracy:.2%}")
```

### 5.5 Visualiser les voisins

```python
import matplotlib.pyplot as plt

# Visualiser le résultat
plt.figure(figsize=(12, 5))

# Subplot 1 : Données d'entraînement
plt.subplot(1, 2, 1)
plt.scatter(X_train[y_train == 0, 0], X_train[y_train == 0, 1],
            c='blue', label='Classe 0', alpha=0.6)
plt.scatter(X_train[y_train == 1, 0], X_train[y_train == 1, 1],
            c='red', label='Classe 1', alpha=0.6)
plt.title("Données d'entraînement")
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2 : Prédictions sur le test
plt.subplot(1, 2, 2)
correct = y_pred == y_test
plt.scatter(X_test[correct, 0], X_test[correct, 1],
            c='green', label='Correct', marker='o', s=60)
plt.scatter(X_test[~correct, 0], X_test[~correct, 1],
            c='red', label='Erreur', marker='x', s=100)
plt.title(f"Prédictions (accuracy = {accuracy:.2%})")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 5.6 Visualiser la frontière de décision

```python
from matplotlib.colors import ListedColormap

def plot_decision_boundary(model, X, y, title="Frontière de décision KNN"):
    """Visualise la frontière de décision d'un modèle 2D."""
    h = 0.05  # Pas de la grille
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(10, 7))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap=ListedColormap(['#AAAAFF', '#FFAAAA']))
    plt.scatter(X[y == 0, 0], X[y == 0, 1], c='blue', label='Classe 0', edgecolors='black')
    plt.scatter(X[y == 1, 0], X[y == 1, 1], c='red', label='Classe 1', edgecolors='black')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Visualiser
knn = KNNFromScratch(k=5)
knn.fit(X_train, y_train)
plot_decision_boundary(knn, X_train, y_train, "KNN (K=5) — Frontière de décision")
```

### 5.7 KNN avec scikit-learn

En pratique, on utilise la version optimisée de scikit-learn :

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Créer un pipeline : normalisation + KNN
pipeline = Pipeline([
    ('scaler', StandardScaler()),       # Normaliser les features
    ('knn', KNeighborsClassifier(n_neighbors=5))  # KNN avec K=5
])

# Entraîner
pipeline.fit(X_train, y_train)

# Prédire
y_pred_sklearn = pipeline.predict(X_test)

# Évaluer
print(f"Accuracy : {accuracy_score(y_test, y_pred_sklearn):.2%}")
print(f"\nRapport de classification :")
print(classification_report(y_test, y_pred_sklearn))
```

### 5.8 Comment choisir K ?

Le choix de **K** est crucial. Trop petit → trop sensible au bruit. Trop grand → trop lissé.

```
K=1 : Chaque point est classé selon      K=50 : Presque tout le dataset vote
      son voisin le PLUS proche                 → frontière trop lissée
      → Frontière très irrégulière              → underfitting possible
      → Overfitting possible

    │  ●/▲●/▲●                              │  ●●●●●●●●●
    │  ▲/●▲/●▲  (zigzag)                    │  ●●●●●●●●●
    │  ●/▲●/▲●                              │  ▲▲▲▲▲▲▲▲▲  (ligne droite)
    └────────────                            └────────────

K=5 : Bon compromis — frontière
      lisse mais qui capture les
      patterns

    │  ●●●●●
    │  ●●●●●  (courbure raisonnable)
    │  ▲▲▲▲▲
    └────────────
```

```python
# Tester différentes valeurs de K
k_values = range(1, 31)
accuracies = []

for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    acc = knn.score(X_test, y_test)
    accuracies.append(acc)

# Visualiser
plt.figure(figsize=(10, 6))
plt.plot(k_values, accuracies, 'bo-', linewidth=2)
plt.xlabel("Nombre de voisins (K)")
plt.ylabel("Accuracy")
plt.title("Accuracy en fonction de K")
plt.axvline(x=k_values[np.argmax(accuracies)], color='red',
            linestyle='--', label=f'Meilleur K = {k_values[np.argmax(accuracies)]}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"Meilleur K = {k_values[np.argmax(accuracies)]} (accuracy = {max(accuracies):.2%})")
```

> 💡 **Conseil** : "Utilisez toujours un **K impair** pour éviter les égalités lors du vote. K=5 est un bon point de départ dans la plupart des cas."

### 5.9 Avantages et limites de KNN

| Avantage | Inconvénient |
|----------|-------------|
| Très simple à comprendre | Lent sur de gros datasets (calcule toutes les distances) |
| Aucun apprentissage réel (lazy learner) | Sensible aux échelles (normalisation obligatoire) |
| Fonctionne bien en faible dimension | Mauvais en haute dimension (curse of dimensionality) |
| Pas d'hypothèse sur la forme des données | Sensible au bruit et aux outliers |
| Bon pour commencer / baseline | Le choix de K est critique |

> ⚠️ **Attention** : "KNN stocke **toutes** les données d'entraînement en mémoire et calcule les distances avec **chaque point** à chaque prédiction. Sur un dataset de 1 million de lignes, ça peut être très lent. Pour de gros volumes, préférez des algorithmes comme Random Forest ou les SVM."

---

## 6. 🏋️ Exercices pratiques

### Exercice 1 : Calculer des distances

```python
# Calculez les distances euclidiennes et Manhattan entre ces clients :
clients = {
    'Alice':   np.array([30, 40000, 5]),
    'Bob':     np.array([25, 35000, 2]),
    'Charlie': np.array([45, 65000, 15]),
    'Diana':   np.array([32, 42000, 6]),
}

# TODO : Calculer la matrice de distances (toutes les paires)
# TODO : Qui est le plus proche d'Alice ?
# TODO : Qui est le plus éloigné de Bob ?
# TODO : Comparer les résultats euclidien vs Manhattan
```

### Exercice 2 : KNN sur le dataset Iris

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Charger le dataset Iris
iris = load_iris()
X, y = iris.data, iris.target

# TODO : Séparer train/test (80/20)
# TODO : Normaliser les données
# TODO : Entraîner un KNN avec K=5
# TODO : Calculer l'accuracy
# TODO : Tester K de 1 à 20 et tracer la courbe d'accuracy
# TODO : Quel est le meilleur K ?
```

### Exercice 3 : Visualiser des clusters

```python
from sklearn.datasets import make_blobs

# Générer des clusters
X, y = make_blobs(n_samples=300, centers=4, cluster_std=1.5, random_state=42)

# TODO : Visualiser les points colorés par cluster
# TODO : Choisir un point au hasard et trouver ses 5 plus proches voisins
# TODO : Visualiser ce point et ses 5 voisins en surbrillance
# TODO : Utiliser KNN pour classifier — quelle accuracy ?
```

### Exercice 4 : Impact de la normalisation

```python
# Données avec des échelles très différentes
X_raw = np.array([
    [25, 100000, 1],
    [30, 105000, 2],
    [60, 30000, 30],
    [65, 28000, 32],
    [35, 95000, 3],   # Point à classer
])

y_raw = np.array([0, 0, 1, 1, -1])  # -1 = inconnu (à prédire)

# TODO : Calculer les distances SANS normalisation
# TODO : Trouver les 3 plus proches voisins (K=3) et prédire
# TODO : Normaliser avec StandardScaler
# TODO : Recalculer les distances AVEC normalisation
# TODO : Trouver les 3 plus proches voisins et prédire
# TODO : La prédiction change-t-elle ? Pourquoi ?
```

### Exercice 5 : Matrice de distances complète

```python
from scipy.spatial.distance import cdist

# 10 points aléatoires en 2D
np.random.seed(42)
points = np.random.randn(10, 2) * 5

# TODO : Calculer la matrice de distances euclidiennes (10x10)
#        Indice : utiliser scipy.spatial.distance.cdist
# TODO : Afficher cette matrice sous forme de heatmap avec seaborn
# TODO : Identifier les deux points les plus proches
# TODO : Identifier les deux points les plus éloignés
```

---

## 🎯 Points clés à retenir

1. **Un vecteur** est une liste ordonnée de nombres qui décrit un objet — c'est la base de la représentation en ML
2. **Chaque observation** (client, image, transaction) est un point dans un espace à N dimensions
3. **La distance euclidienne** mesure la "ressemblance" entre deux points en ligne droite : `√(Σ(aᵢ - bᵢ)²)`
4. **La distance de Manhattan** somme les différences absolues et est plus robuste aux outliers
5. **Une matrice** = un tableau de vecteurs empilés = un DataFrame pandas en version numérique
6. **Convention ML** : X (matrice de features) et y (vecteur target), toujours séparés
7. **KNN** prédit en regardant les K voisins les plus proches et en votant à la majorité
8. **La normalisation** est obligatoire avant de calculer des distances (sinon les grandes échelles dominent)
9. **Le choix de K** est un hyperparamètre crucial : K petit → overfitting, K grand → underfitting
10. **KNN est un lazy learner** : il stocke tout et calcule à la prédiction, ce qui le rend lent sur de gros datasets

---

## ✅ Checklist de validation

- [ ] Je sais expliquer ce qu'est un vecteur et pourquoi c'est utile en ML
- [ ] Je sais créer et manipuler des vecteurs et matrices avec NumPy
- [ ] Je comprends la différence entre une liste Python et un ndarray NumPy
- [ ] Je sais calculer la distance euclidienne entre deux vecteurs
- [ ] Je sais calculer la distance de Manhattan entre deux vecteurs
- [ ] Je comprends le lien entre matrice NumPy et DataFrame pandas
- [ ] Je connais la convention X (features) et y (target)
- [ ] Je peux expliquer l'algorithme KNN sans formule (l'intuition)
- [ ] J'ai codé un KNN from scratch et je comprends chaque ligne
- [ ] Je sais utiliser `KNeighborsClassifier` de scikit-learn
- [ ] Je comprends pourquoi la normalisation est obligatoire pour KNN
- [ ] Je sais choisir une bonne valeur de K et tester plusieurs valeurs
- [ ] J'ai réalisé les exercices de calcul de distances et de visualisation

---

**Précédent** : [Chapitre 2 : Environnement et Outils](02-environnement-setup.md)

**Suivant** : [Chapitre 4 : Fonctions, Erreurs et l'Art de s'Améliorer](04-fonctions-erreurs-gradient.md)
