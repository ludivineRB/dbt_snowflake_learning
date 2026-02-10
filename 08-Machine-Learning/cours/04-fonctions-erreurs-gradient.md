# Chapitre 4 : Fonctions, Erreurs et l'Art de s'Améliorer

## 🎯 Objectifs

- Comprendre comment une machine "apprend" à partir de ses erreurs
- Maîtriser la régression linéaire intuitivement puis mathématiquement
- Savoir ce qu'est une fonction d'erreur (MSE, MAE, RMSE) et la visualiser
- Comprendre la dérivée comme une "direction d'amélioration"
- Implémenter la descente de gradient from scratch
- Coder une régression linéaire from scratch puis avec scikit-learn
- Découvrir la régularisation (Ridge et Lasso) intuitivement

**Livrable** : Notebook "Gradient Descent expliqué à ma grand-mère"

---

## 1. 🧠 Comment une machine apprend-elle ?

### 1.1 Le problème posé

Imaginez que vous devez prédire le **prix d'un appartement** en fonction de sa **surface**. Vous avez des données historiques :

| Surface (m²) | Prix (k€) |
|:------------:|:---------:|
| 30 | 150 |
| 50 | 220 |
| 70 | 310 |
| 90 | 380 |
| 110 | 470 |

Comment trouver une **règle** qui permet de prédire le prix pour une surface de 85 m² ?

### 1.2 L'approche du Machine Learning

```
Étape 1 : Commencer avec une "devinette" (modèle initial)
         → "Le prix = 100k€ pour tout le monde" (mauvais)

Étape 2 : Mesurer l'erreur
         → "Je me trompe de beaucoup !"

Étape 3 : Ajuster pour réduire l'erreur
         → "Si j'augmente un peu la pente..."

Étape 4 : Répéter jusqu'à satisfaction
         → "Maintenant je me trompe très peu !"
```

> 💡 **Conseil** : "L'apprentissage d'une machine se résume en 3 mots : **deviner, mesurer, corriger**. C'est exactement comme un étudiant qui fait des exercices, vérifie ses réponses et s'améliore."

### 1.3 Ce que "apprendre" signifie concrètement

```
Avant l'entraînement :
  Modèle : prix = 0 × surface + 0
  → Prédit 0€ pour tout → Erreur énorme

Pendant l'entraînement :
  Le modèle ajuste ses paramètres petit à petit...
  Itération 1   : prix = 0.5 × surface + 10  → Erreur = 85000
  Itération 10  : prix = 2.0 × surface + 50  → Erreur = 12000
  Itération 100 : prix = 3.2 × surface + 55  → Erreur = 1500
  Itération 500 : prix = 3.5 × surface + 48  → Erreur = 200

Après l'entraînement :
  Modèle : prix ≈ 3.5 × surface + 48
  → Prédit 346k€ pour 85m² → Très proche de la réalité !
```

---

## 2. 🔧 Fonction = Machine à transformer

### 2.1 L'analogie de la recette de cuisine

Une **fonction** prend une entrée et produit une sortie selon une règle précise.

```
Fonction = Recette de cuisine

   Ingrédients (entrée)  →  Recette (fonction)  →  Plat (sortie)
   Farine, œufs, sucre   →  Mélanger, cuire     →  Gâteau

En maths :
   x (entrée)            →  f(x) (règle)        →  y (sortie)
   surface = 70 m²       →  prix = 3.5 × x + 50 →  prix = 295 k€
```

### 2.2 Exemples de fonctions simples

```python
import numpy as np
import matplotlib.pyplot as plt

# Fonction linéaire : f(x) = 2x + 1
def f_lineaire(x):
    return 2 * x + 1

# Fonction quadratique : f(x) = x²
def f_quadratique(x):
    return x ** 2

# Visualiser
x = np.linspace(-5, 5, 100)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(x, f_lineaire(x), 'b-', linewidth=2)
axes[0].set_title("Fonction linéaire : f(x) = 2x + 1")
axes[0].grid(True, alpha=0.3)
axes[0].axhline(y=0, color='k', linewidth=0.5)
axes[0].axvline(x=0, color='k', linewidth=0.5)

axes[1].plot(x, f_quadratique(x), 'r-', linewidth=2)
axes[1].set_title("Fonction quadratique : f(x) = x²")
axes[1].grid(True, alpha=0.3)
axes[1].axhline(y=0, color='k', linewidth=0.5)
axes[1].axvline(x=0, color='k', linewidth=0.5)

plt.tight_layout()
plt.show()
```

### 2.3 Pourquoi c'est important en ML ?

En Machine Learning, le **modèle** est une fonction :

| Élément | En maths | En ML |
|---------|---------|-------|
| Entrée | x | Features (surface, nb pièces...) |
| Fonction | f(x) | Modèle (régression, KNN...) |
| Sortie | y | Prédiction (prix, classe...) |
| Paramètres | a, b dans f(x) = ax + b | Poids appris par le modèle |

> L'objectif du ML est de **trouver la bonne fonction** (les bons paramètres) qui transforme les features en prédictions correctes.

### 2.4 Fonction linéaire vs non-linéaire

```
Linéaire : y = ax + b            Non-linéaire : y = ax² + bx + c

    y│      /                       y│       ╱╲
     │    /                          │     ╱    ╲
     │  /                            │   ╱        ╲
     │/                              │ ╱            ╲
     └────── x                       └──────────────── x

→ Une seule droite                  → Courbes, polynômes, etc.
→ Simple, interprétable             → Plus flexible, risque d'overfitting
```

---

## 3. 📈 Régression linéaire : trouver la meilleure droite

### 3.1 L'intuition visuelle

La régression linéaire cherche la **droite** qui passe "au mieux" à travers un nuage de points.

```
   Prix (k€)
    500 │                           ●
        │                      ●  /
    400 │                  ●  / ←── droite y = ax + b
        │              ● /
    300 │          ● /
        │       ● /
    200 │     /●
        │   /●
    100 │  /
        │ /
      0 └──────────────────────────── Surface (m²)
         0   20   40   60   80  100  120
```

### 3.2 L'équation y = ax + b

```
y = ax + b

Où :
  y = la prédiction (prix)
  x = la feature (surface)
  a = la pente (combien y augmente quand x augmente de 1)
  b = l'ordonnée à l'origine (y quand x = 0)
```

**Interprétation concrète** :

```
prix = 3.5 × surface + 50

→ a = 3.5 : chaque m² supplémentaire coûte 3 500 €
→ b = 50  : un appartement de 0 m² coûterait 50 000 € (coût fixe théorique)
```

### 3.3 Visualiser avec Python

```python
import numpy as np
import matplotlib.pyplot as plt

# Données
surfaces = np.array([30, 50, 70, 90, 110])
prix = np.array([150, 220, 310, 380, 470])

# Tracer le nuage de points
plt.figure(figsize=(10, 6))
plt.scatter(surfaces, prix, s=100, c='steelblue', edgecolors='black', zorder=5)

# Tracer plusieurs droites candidates
x_line = np.linspace(20, 120, 100)
plt.plot(x_line, 2 * x_line + 100, 'r--', alpha=0.5, label='y = 2x + 100 (trop plate)')
plt.plot(x_line, 5 * x_line - 20, 'g--', alpha=0.5, label='y = 5x - 20 (trop pentue)')
plt.plot(x_line, 3.5 * x_line + 50, 'b-', linewidth=2, label='y = 3.5x + 50 (bonne !)')

plt.xlabel("Surface (m²)")
plt.ylabel("Prix (k€)")
plt.title("Quelle droite est la meilleure ?")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

> 💡 **Conseil** : "La 'meilleure' droite est celle qui **minimise l'écart total** entre les prédictions et les vraies valeurs. C'est exactement ce que fait la fonction d'erreur."

### 3.4 Le cas multi-variables

En réalité, le prix dépend de **plusieurs** features :

```
prix = a₁ × surface + a₂ × nb_pièces + a₃ × étage + b

Sous forme matricielle : y = X @ w + b
  X = matrice des features
  w = vecteur des poids (à apprendre)
  b = biais (ordonnée à l'origine)
```

```python
# Régression multi-variables : plusieurs features
import pandas as pd

df = pd.DataFrame({
    'surface': [30, 50, 70, 90, 110],
    'nb_pieces': [1, 2, 3, 4, 5],
    'etage': [0, 2, 5, 3, 8],
    'prix': [150, 220, 310, 380, 470]
})

X = df[['surface', 'nb_pieces', 'etage']].values  # Matrice (5, 3)
y = df['prix'].values                               # Vecteur (5,)

print(f"X shape : {X.shape}")
print(f"y shape : {y.shape}")
```

---

## 4. 📉 Erreur = Distance entre prédiction et réalité

### 4.1 Visualiser les erreurs

Pour savoir si une droite est "bonne", on mesure les **écarts** (résidus) entre les prédictions et les vraies valeurs :

```
   Prix (k€)
    │                    ● (vrai = 380)
    │                    │
    │                    │ erreur = 30
    │                    │
    │               ─────●───── (prédit = 350)
    │          ● (vrai = 310)
    │          │
    │          │ erreur = -15
    │          │
    │     ─────●───── (prédit = 295)
    │
    └──────────────────────── Surface
```

```python
# Prédictions avec la droite y = 3.5x + 50
surfaces = np.array([30, 50, 70, 90, 110], dtype=float)
prix = np.array([150, 220, 310, 380, 470], dtype=float)
predictions = 3.5 * surfaces + 50

# Erreurs (résidus)
erreurs = prix - predictions

print("Surface | Prix réel | Prix prédit | Erreur")
print("-" * 50)
for s, p, pred, err in zip(surfaces, prix, predictions, erreurs):
    print(f"  {s:>3.0f} m² |   {p:>3.0f} k€  |   {pred:>5.0f} k€  |  {err:>+.0f} k€")

# Visualiser les erreurs
plt.figure(figsize=(10, 6))
plt.scatter(surfaces, prix, s=100, c='steelblue', edgecolors='black',
            zorder=5, label='Valeurs réelles')
plt.plot(surfaces, predictions, 'r-', linewidth=2, label='Prédictions')

# Tracer les erreurs (segments verticaux)
for s, p, pred in zip(surfaces, prix, predictions):
    plt.plot([s, s], [p, pred], 'r--', alpha=0.7, linewidth=1.5)

plt.xlabel("Surface (m²)")
plt.ylabel("Prix (k€)")
plt.title("Erreurs = écarts entre prédictions et réalité")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 4.2 MSE — Mean Squared Error (Erreur Quadratique Moyenne)

La MSE est la métrique d'erreur la plus utilisée en régression.

```
                    1     n
MSE = ─── × Σ  (yᵢ - ŷᵢ)²
                    n    i=1

Où :
  yᵢ  = valeur réelle du point i
  ŷᵢ  = valeur prédite pour le point i
  n   = nombre de points
```

**Pourquoi mettre au carré ?**

| Raison | Explication |
|--------|-------------|
| **Éliminer les signes** | Sans carré, les erreurs positives et négatives s'annulent |
| **Pénaliser les grosses erreurs** | Une erreur de 10 compte 4× plus qu'une erreur de 5 (100 vs 25) |
| **Propriété mathématique** | La fonction est dérivable partout → facile à optimiser |

```python
def mse(y_true, y_pred):
    """Calcule la Mean Squared Error."""
    return np.mean((y_true - y_pred) ** 2)

# Calculer la MSE de notre droite
erreur_mse = mse(prix, predictions)
print(f"MSE = {erreur_mse:.2f}")
```

### 4.3 MAE — Mean Absolute Error

```
                    1     n
MAE = ─── × Σ  |yᵢ - ŷᵢ|
                    n    i=1
```

La MAE est **plus robuste aux outliers** car elle ne met pas les erreurs au carré.

```python
def mae(y_true, y_pred):
    """Calcule la Mean Absolute Error."""
    return np.mean(np.abs(y_true - y_pred))

erreur_mae = mae(prix, predictions)
print(f"MAE = {erreur_mae:.2f} k€")
print(f"→ En moyenne, nos prédictions se trompent de ±{erreur_mae:.0f} k€")
```

### 4.4 RMSE — Root Mean Squared Error

```
RMSE = √MSE
```

L'avantage du RMSE est d'être dans la **même unité** que la target (k€ ici), tout en pénalisant les grosses erreurs.

```python
def rmse(y_true, y_pred):
    """Calcule le Root Mean Squared Error."""
    return np.sqrt(mse(y_true, y_pred))

erreur_rmse = rmse(prix, predictions)
print(f"RMSE = {erreur_rmse:.2f} k€")
```

### 4.5 Comparaison des métriques

| Métrique | Formule | Unité | Sensibilité aux outliers | Quand l'utiliser |
|----------|---------|-------|--------------------------|------------------|
| **MSE** | Σ(y-ŷ)²/n | unité² | Très haute | Optimisation (gradient) |
| **MAE** | Σ\|y-ŷ\|/n | unité | Modérée | Interprétation, outliers |
| **RMSE** | √MSE | unité | Haute | Interprétation + pénalise grosses erreurs |
| **R²** | 1 - MSE/Var(y) | sans unité | — | Comparer des modèles (0 à 1) |

> 💡 **Conseil** : "Utilisez le **RMSE** pour communiquer avec les métiers ('on se trompe en moyenne de ±15k€'). Utilisez la **MSE** pour l'optimisation mathématique (descente de gradient). Utilisez le **R²** pour comparer des modèles entre eux."

### 4.6 Visualiser l'erreur en fonction des paramètres

```python
# Tester différentes pentes (a) et voir l'erreur
pentes = np.linspace(1, 6, 100)
erreurs_mse = []

for a in pentes:
    pred = a * surfaces + 50  # On fixe b=50
    erreurs_mse.append(mse(prix, pred))

plt.figure(figsize=(10, 6))
plt.plot(pentes, erreurs_mse, 'b-', linewidth=2)
plt.xlabel("Pente (a)")
plt.ylabel("MSE")
plt.title("MSE en fonction de la pente — On cherche le minimum !")
plt.axvline(x=pentes[np.argmin(erreurs_mse)], color='red', linestyle='--',
            label=f'Meilleure pente ≈ {pentes[np.argmin(erreurs_mse)]:.2f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

### 4.7 Surface d'erreur en 3D (pente ET ordonnée à l'origine)

```python
from mpl_toolkits.mplot3d import Axes3D

# Tester des combinaisons de (a, b)
a_vals = np.linspace(1, 6, 50)
b_vals = np.linspace(-50, 150, 50)
A, B = np.meshgrid(a_vals, b_vals)
Z = np.zeros_like(A)

for i in range(len(a_vals)):
    for j in range(len(b_vals)):
        pred = A[j, i] * surfaces + B[j, i]
        Z[j, i] = mse(prix, pred)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(A, B, Z, cmap='coolwarm', alpha=0.8)
ax.set_xlabel("Pente (a)")
ax.set_ylabel("Ordonnée à l'origine (b)")
ax.set_zlabel("MSE")
ax.set_title("Surface d'erreur — La descente de gradient cherche le creux")
plt.show()
```

> 💡 **Conseil** : "La surface d'erreur ressemble à un **bol**. La descente de gradient, c'est une bille qu'on lâche sur le bord du bol et qui roule vers le fond (le minimum d'erreur)."

---

## 5. 🏔️ Dérivée = Direction pour réduire l'erreur

### 5.1 L'analogie de la montagne dans le brouillard

Imaginez que vous êtes en montagne, dans un **brouillard épais**, et vous voulez descendre dans la **vallée** (le minimum d'erreur). Vous ne voyez pas le paysage, mais vous pouvez sentir la **pente sous vos pieds**.

```
        ╱╲
       ╱  ╲             Vous êtes ici
      ╱    ╲                 ↓
     ╱      ╲    ╱╲    ● ──→ La pente descend vers la droite
    ╱        ╲  ╱  ╲       → Donc allez à droite !
   ╱          ╲╱    ╲
  ╱                  ╲
 ╱        ★           ╲    ★ = Vallée (minimum d'erreur)
╱                      ╲       C'est là qu'on veut aller !
```

**La dérivée, c'est la pente sous vos pieds** :
- Pente négative (descend vers la droite) → allez à droite
- Pente positive (descend vers la gauche) → allez à gauche
- Pente = 0 → vous êtes au minimum !

### 5.2 La dérivée visuellement

```
   f(x) = x²

   f(x)
    │
  25│                          ●
    │                      ╱
  16│                  ● ╱
    │               ╱  ╱
   9│           ● ╱  pente = 2x = 6  (x=3)
    │        ╱
   4│     ●╱  pente = 2x = 4  (x=2)
    │   ╱
   1│ ●╱  pente = 2x = 2  (x=1)
    │╱
   0●  pente = 0 → MINIMUM !
    └──────────────────────── x
    0  1  2  3  4  5

   La pente (dérivée) indique si la fonction monte ou descend.
   Au minimum (x=0), la pente = 0.
```

### 5.3 Exemples de dérivées courantes

| Fonction f(x) | Dérivée f'(x) | Interprétation |
|--------------|---------------|----------------|
| f(x) = c (constante) | f'(x) = 0 | Plat, pas de pente |
| f(x) = ax | f'(x) = a | Pente constante |
| f(x) = x² | f'(x) = 2x | Pente qui augmente avec x |
| f(x) = x³ | f'(x) = 3x² | Pente qui augmente encore plus vite |
| f(x) = ax² + bx + c | f'(x) = 2ax + b | Parabole : un seul minimum |

> 💡 **Conseil** : "Pas besoin de retenir toutes les règles de dérivation. L'important est de comprendre que la dérivée nous dit **dans quelle direction** modifier un paramètre pour **réduire** l'erreur."

### 5.4 La dérivée appliquée à la MSE

Pour la régression linéaire `ŷ = a*x + b`, on veut trouver les valeurs de `a` et `b` qui minimisent la MSE.

```
MSE(a, b) = (1/n) × Σ(yᵢ - (a×xᵢ + b))²

Dérivée par rapport à a (comment a affecte l'erreur) :
∂MSE/∂a = -(2/n) × Σ xᵢ × (yᵢ - (a×xᵢ + b))

Dérivée par rapport à b (comment b affecte l'erreur) :
∂MSE/∂b = -(2/n) × Σ (yᵢ - (a×xᵢ + b))
```

> ⚠️ **Attention** : "On n'a pas besoin de résoudre ces équations à la main ! La descente de gradient le fait automatiquement, itération par itération."

---

## 6. 🚀 La descente de gradient expliquée pas à pas

### 6.1 L'algorithme en français

```
Algorithme : Descente de gradient
─────────────────────────────────────────────────────
1. Initialiser les paramètres au hasard (a=0, b=0)
2. Répéter N fois :
   a. Calculer les prédictions : ŷ = a×x + b
   b. Calculer l'erreur (MSE)
   c. Calculer les gradients (dérivées) :
      - gradient_a = comment a doit changer
      - gradient_b = comment b doit changer
   d. Mettre à jour les paramètres :
      - a = a - learning_rate × gradient_a
      - b = b - learning_rate × gradient_b
3. Retourner a et b optimisés
─────────────────────────────────────────────────────
```

### 6.2 Le Learning Rate

Le **learning rate** (taux d'apprentissage) contrôle la **taille des pas** que l'on fait.

```
Learning rate trop GRAND :          Learning rate trop PETIT :

    ╱╲                                  ╱╲
   ╱  ╲    ╱╲                         ╱  ╲
  ●    ╲  ╱  ●  ← On oscille !      ╱    ╲
 ╱      ╲╱    ╲                     ●      ╲
╱   ★         ╲╱                   ╱●       ╲
                                  ╱  ●       ╲
→ Ne converge jamais !           ╱   ●●●★     ╲
                                      ↑
                              Trop lent (10000 itérations)

Learning rate BON :

    ╱╲
   ╱  ╲
  ●    ╲
 ╱ ●    ╲
╱   ●★   ╲

→ Converge en quelques itérations !
```

| Learning Rate | Effet | Risque |
|:------------:|-------|--------|
| Trop grand (> 0.1) | Grands pas, rapide | Oscillation, divergence |
| Bon (0.001 - 0.01) | Convergence stable | — |
| Trop petit (< 0.00001) | Très petits pas | Extrêmement lent |

### 6.3 Descente de gradient from scratch (~30 lignes)

```python
import numpy as np

def mse(y_true, y_pred):
    """Mean Squared Error."""
    return np.mean((y_true - y_pred) ** 2)

def descente_gradient(X, y, learning_rate=0.01, n_iterations=1000):
    """
    Descente de gradient pour régression linéaire (y = a*x + b).

    Args:
        X: features (1D)
        y: target
        learning_rate: taux d'apprentissage
        n_iterations: nombre d'itérations

    Returns:
        a, b: paramètres optimisés
        historique: liste des MSE à chaque itération
    """
    n = len(X)

    # 1. Initialisation à zéro
    a = 0.0
    b = 0.0
    historique = []

    for i in range(n_iterations):
        # 2. Prédictions avec les paramètres actuels
        y_pred = a * X + b

        # 3. Calcul de l'erreur
        erreur = mse(y, y_pred)
        historique.append(erreur)

        # 4. Calcul des gradients (dérivées partielles)
        gradient_a = -(2 / n) * np.sum(X * (y - y_pred))
        gradient_b = -(2 / n) * np.sum(y - y_pred)

        # 5. Mise à jour des paramètres (on descend la pente)
        a = a - learning_rate * gradient_a
        b = b - learning_rate * gradient_b

        # Afficher la progression
        if i % 200 == 0:
            print(f"Itération {i:>4} | MSE = {erreur:>10.4f} | a = {a:.4f} | b = {b:.4f}")

    return a, b, historique
```

### 6.4 Tester la descente de gradient

```python
# Données
surfaces = np.array([30, 50, 70, 90, 110], dtype=float)
prix = np.array([150, 220, 310, 380, 470], dtype=float)

# Normaliser pour faciliter la convergence
X_mean, X_std = surfaces.mean(), surfaces.std()
y_mean, y_std = prix.mean(), prix.std()

X_norm = (surfaces - X_mean) / X_std
y_norm = (prix - y_mean) / y_std

# Lancer la descente de gradient
a, b, historique = descente_gradient(X_norm, y_norm, learning_rate=0.1, n_iterations=1000)

print(f"\nRésultat final (normalisé) : y = {a:.4f} * x + {b:.4f}")

# Convertir les paramètres dans l'échelle originale
a_original = a * (y_std / X_std)
b_original = y_mean + b * y_std - a_original * X_mean
print(f"Résultat final (original) : prix = {a_original:.2f} × surface + {b_original:.2f}")

# Visualiser la convergence
plt.figure(figsize=(10, 5))
plt.plot(historique, 'b-', linewidth=2)
plt.xlabel("Itérations")
plt.ylabel("MSE")
plt.title("Convergence de la descente de gradient")
plt.grid(True, alpha=0.3)
plt.show()
```

### 6.5 Visualiser l'apprentissage étape par étape

```python
def descente_gradient_visual(X, y, learning_rate=0.1, n_iterations=1000, save_every=100):
    """Descente de gradient avec sauvegarde des étapes intermédiaires."""
    n = len(X)
    a, b = 0.0, 0.0
    etapes = []

    for i in range(n_iterations):
        y_pred = a * X + b
        gradient_a = -(2 / n) * np.sum(X * (y - y_pred))
        gradient_b = -(2 / n) * np.sum(y - y_pred)
        a -= learning_rate * gradient_a
        b -= learning_rate * gradient_b

        if i % save_every == 0:
            etapes.append((i, a, b, mse(y, y_pred)))

    return a, b, etapes

# Lancer
a_final, b_final, etapes = descente_gradient_visual(X_norm, y_norm)

# Visualiser les droites successives
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for idx, (iteration, a, b, err) in enumerate(etapes[:6]):
    ax = axes[idx]
    ax.scatter(X_norm, y_norm, c='steelblue', edgecolors='black', zorder=5)
    x_line = np.linspace(X_norm.min() - 0.5, X_norm.max() + 0.5, 100)
    ax.plot(x_line, a * x_line + b, 'r-', linewidth=2)
    ax.set_title(f"Itération {iteration} | MSE = {err:.4f}")
    ax.set_xlabel("Surface (normalisée)")
    ax.set_ylabel("Prix (normalisé)")
    ax.grid(True, alpha=0.3)

plt.suptitle("La droite s'ajuste au fil des itérations", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 6.6 Impact du learning rate

```python
# Comparer différents learning rates
learning_rates = [0.001, 0.01, 0.1, 0.5]

plt.figure(figsize=(12, 6))

for lr in learning_rates:
    _, _, hist = descente_gradient(X_norm, y_norm, learning_rate=lr, n_iterations=500)
    plt.plot(hist, linewidth=2, label=f'lr = {lr}')

plt.xlabel("Itérations")
plt.ylabel("MSE")
plt.title("Impact du learning rate sur la convergence")
plt.legend()
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.show()
```

> ⚠️ **Attention** : "Toujours **normaliser** les données avant d'appliquer la descente de gradient ! Sans normalisation, les gradients peuvent être énormes pour certaines features et minuscules pour d'autres, ce qui empêche la convergence."

---

## 7. 🛠️ Régression linéaire from scratch puis avec scikit-learn

### 7.1 Régression linéaire multi-variables from scratch

```python
class RegressionLineaireFromScratch:
    """Régression linéaire par descente de gradient (multi-variables)."""

    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.lr = learning_rate
        self.n_iter = n_iterations
        self.weights = None
        self.bias = None
        self.historique = []

    def fit(self, X, y):
        """Entraîner le modèle sur les données."""
        n_samples, n_features = X.shape

        # Initialisation des paramètres à zéro
        self.weights = np.zeros(n_features)
        self.bias = 0.0

        for i in range(self.n_iter):
            # Prédictions : y_pred = X @ w + b
            y_pred = X @ self.weights + self.bias

            # Gradients (dérivées partielles de la MSE)
            dw = -(2 / n_samples) * (X.T @ (y - y_pred))
            db = -(2 / n_samples) * np.sum(y - y_pred)

            # Mise à jour des paramètres
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            # Sauvegarder l'historique de l'erreur
            self.historique.append(np.mean((y - y_pred) ** 2))

        return self

    def predict(self, X):
        """Prédire les valeurs pour de nouvelles données."""
        return X @ self.weights + self.bias

    def score(self, X, y):
        """Calculer le R² (coefficient de détermination)."""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)      # Somme des résidus au carré
        ss_tot = np.sum((y - np.mean(y)) ** 2)   # Variance totale
        return 1 - (ss_res / ss_tot)
```

### 7.2 Tester notre régression from scratch

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Charger les données
housing = fetch_california_housing()
X, y = housing.data, housing.target

# Séparer train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Normaliser (CRUCIAL pour la descente de gradient)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entraîner notre modèle
model = RegressionLineaireFromScratch(learning_rate=0.01, n_iterations=1000)
model.fit(X_train_scaled, y_train)

# Évaluer
r2_train = model.score(X_train_scaled, y_train)
r2_test = model.score(X_test_scaled, y_test)
print(f"R² train : {r2_train:.4f}")
print(f"R² test  : {r2_test:.4f}")

# Visualiser la convergence
plt.figure(figsize=(10, 5))
plt.plot(model.historique, 'b-', linewidth=1)
plt.xlabel("Itérations")
plt.ylabel("MSE")
plt.title("Convergence de notre régression from scratch")
plt.grid(True, alpha=0.3)
plt.show()
```

### 7.3 Avec scikit-learn (3 lignes !)

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Entraîner (scikit-learn utilise une solution analytique, pas la descente de gradient)
model_sklearn = LinearRegression()
model_sklearn.fit(X_train, y_train)  # Pas besoin de normaliser !

# Prédire
y_pred = model_sklearn.predict(X_test)

# Évaluer
print(f"R² : {r2_score(y_test, y_pred):.4f}")
print(f"RMSE : {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"\nCoefficients : {model_sklearn.coef_}")
print(f"Intercept : {model_sklearn.intercept_:.4f}")
```

### 7.4 Comparaison : from scratch vs scikit-learn

| Aspect | From scratch | scikit-learn |
|--------|-------------|--------------|
| **Lignes de code** | ~30 | ~3 |
| **Normalisation** | Obligatoire | Optionnelle |
| **Méthode** | Descente de gradient (itérative) | Solution analytique (OLS) |
| **Vitesse** | Plus lent | Très rapide |
| **Hyperparamètres** | learning_rate, n_iterations | Aucun |
| **Valeur pédagogique** | Excellente | Faible |
| **En production** | Non | Oui |

> 💡 **Conseil** : "Coder from scratch est **essentiel pour comprendre**. Mais en pratique, utilisez **toujours** scikit-learn. La bibliothèque est optimisée, testée et maintenue par une communauté de développeurs."

### 7.5 Interpréter les coefficients

```python
import pandas as pd

# Quels facteurs influencent le plus le prix ?
feature_names = housing.feature_names
coefficients = model_sklearn.coef_

# Trier par importance (valeur absolue)
importance = pd.DataFrame({
    'Feature': feature_names,
    'Coefficient': coefficients,
    'Importance absolue': np.abs(coefficients)
}).sort_values('Importance absolue', ascending=False)

print(importance.to_string(index=False))

# Visualiser
plt.figure(figsize=(10, 6))
colors = ['#e74c3c' if c > 0 else '#3498db' for c in importance['Coefficient']]
plt.barh(importance['Feature'], importance['Coefficient'], color=colors)
plt.xlabel("Coefficient")
plt.title("Importance des features dans la régression linéaire")
plt.axvline(x=0, color='black', linewidth=0.5)
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()
```

---

## 8. 🛡️ Régularisation intuitive : Ridge et Lasso

### 8.1 Le problème de l'overfitting en régression

Quand un modèle a **trop de liberté** (trop de features, coefficients trop grands), il peut **mémoriser le bruit** au lieu d'apprendre les vrais patterns.

```
Sans régularisation (overfitting) :     Avec régularisation :

   y│    ●                               y│    ●
    │   ╱╲  ●                             │   ╱  ●
    │  ╱  ╲╱╲   ● ←── La courbe           │  ╱     ●  ←── La droite est
    │ ╱      ╲ ╱      passe par             │ ╱    ●       plus simple
    │╱  ●     ●       tous les points       │╱  ●          et généralise mieux
    └──────────── x                         └──────────── x
    Coefficients énormes                    Coefficients modérés
```

### 8.2 L'idée de la régularisation

La régularisation ajoute une **pénalité** sur la taille des coefficients :

```
Sans régularisation :
   Objectif = minimiser MSE

Avec régularisation :
   Objectif = minimiser MSE + λ × (taille des coefficients)

   λ (lambda, appelé alpha dans scikit-learn) :
   λ = 0    → pas de régularisation (régression classique)
   λ petit  → légère régularisation
   λ grand  → forte régularisation (coefficients → 0)
   λ → ∞   → tous les coefficients → 0 (modèle trivial)
```

> 💡 **Conseil** : "La régularisation, c'est comme dire au modèle : 'Trouve de bons coefficients, MAIS garde-les aussi petits que possible.' Ça l'empêche de devenir trop complexe."

### 8.3 Ridge (L2) vs Lasso (L1)

| Aspect | Ridge (L2) | Lasso (L1) |
|--------|-----------|-----------|
| **Pénalité** | Σ(wᵢ²) — somme des carrés | Σ\|wᵢ\| — somme des valeurs absolues |
| **Effet** | Réduit tous les coefficients (aucun à zéro) | Met certains coefficients **exactement à 0** |
| **Sélection de features** | Non (garde toutes les features) | Oui (supprime les features inutiles) |
| **Quand l'utiliser** | Toutes les features sont potentiellement utiles | Beaucoup de features, certaines inutiles |
| **Analogie** | "Baisse le volume de tous les instruments" | "Coupe certaines pistes audio" |

```
Ridge : w = [0.8, 0.3, 0.5, 0.1, 0.2]  → Tous non-nuls, mais plus petits
Lasso : w = [1.2, 0.0, 0.7, 0.0, 0.0]  → Certains exactement à 0 !
```

### 8.4 En pratique avec scikit-learn

```python
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.preprocessing import StandardScaler

# Normaliser (important pour la régularisation)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Comparer les modèles
models = {
    'Régression linéaire': LinearRegression(),
    'Ridge (α=0.1)': Ridge(alpha=0.1),
    'Ridge (α=1.0)': Ridge(alpha=1.0),
    'Ridge (α=10.0)': Ridge(alpha=10.0),
    'Lasso (α=0.01)': Lasso(alpha=0.01),
    'Lasso (α=0.1)': Lasso(alpha=0.1),
    'Lasso (α=1.0)': Lasso(alpha=1.0),
}

print(f"{'Modèle':<25} {'R² Train':>10} {'R² Test':>10} {'Coefs ≈ 0':>12}")
print("-" * 60)

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    r2_train = model.score(X_train_scaled, y_train)
    r2_test = model.score(X_test_scaled, y_test)
    n_zeros = np.sum(np.abs(model.coef_) < 0.001)
    print(f"{name:<25} {r2_train:>10.4f} {r2_test:>10.4f} {n_zeros:>12}")
```

### 8.5 Visualiser l'effet de la régularisation

```python
# Impact de alpha sur les coefficients Ridge
alphas = np.logspace(-2, 4, 100)
coefs_ridge = []

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    ridge.fit(X_train_scaled, y_train)
    coefs_ridge.append(ridge.coef_)

coefs_ridge = np.array(coefs_ridge)

plt.figure(figsize=(12, 6))
for i in range(coefs_ridge.shape[1]):
    plt.plot(alphas, coefs_ridge[:, i], linewidth=2, label=housing.feature_names[i])

plt.xscale('log')
plt.xlabel("Alpha (force de régularisation)")
plt.ylabel("Valeur du coefficient")
plt.title("Ridge : les coefficients diminuent quand alpha augmente")
plt.legend(loc='best', fontsize=8)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linewidth=0.5)
plt.show()
```

### 8.6 Choisir le bon alpha avec Cross-Validation

```python
from sklearn.linear_model import RidgeCV, LassoCV

# Ridge avec cross-validation automatique
ridge_cv = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0, 100.0], cv=5)
ridge_cv.fit(X_train_scaled, y_train)
print(f"Meilleur alpha Ridge : {ridge_cv.alpha_}")
print(f"R² test : {ridge_cv.score(X_test_scaled, y_test):.4f}")

# Lasso avec cross-validation automatique
lasso_cv = LassoCV(alphas=[0.001, 0.01, 0.1, 1.0], cv=5)
lasso_cv.fit(X_train_scaled, y_train)
print(f"\nMeilleur alpha Lasso : {lasso_cv.alpha_}")
print(f"R² test : {lasso_cv.score(X_test_scaled, y_test):.4f}")
print(f"Features éliminées : {np.sum(lasso_cv.coef_ == 0)} / {X.shape[1]}")
```

### 8.7 Elastic Net : le meilleur des deux mondes

```python
from sklearn.linear_model import ElasticNet, ElasticNetCV

# Elastic Net combine Ridge et Lasso
# l1_ratio = 0 → Ridge pur, l1_ratio = 1 → Lasso pur
elastic_cv = ElasticNetCV(l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9], cv=5)
elastic_cv.fit(X_train_scaled, y_train)
print(f"Meilleur l1_ratio : {elastic_cv.l1_ratio_}")
print(f"Meilleur alpha : {elastic_cv.alpha_:.4f}")
print(f"R² test : {elastic_cv.score(X_test_scaled, y_test):.4f}")
```

### 8.8 Guide de choix

| Situation | Méthode recommandée |
|-----------|-------------------|
| Peu de features, pas d'overfitting | **Régression linéaire** simple |
| Beaucoup de features, toutes utiles | **Ridge** |
| Beaucoup de features, certaines inutiles | **Lasso** |
| Pas sûr, veut un compromis | **Elastic Net** |
| Besoin de sélection automatique de features | **Lasso** ou **Elastic Net** |

> ⚠️ **Attention** : "La régularisation nécessite des données **normalisées** (StandardScaler). Sinon, les features avec de grandes valeurs seront plus pénalisées que les autres, ce qui fausse le résultat."

---

## 🎯 Points clés à retenir

1. **L'apprentissage ML** = deviner, mesurer l'erreur, corriger — en boucle
2. **Une fonction** transforme des entrées en sorties ; en ML, le modèle est une fonction à optimiser
3. **La régression linéaire** cherche la droite `y = ax + b` qui minimise l'erreur
4. **La MSE** (Mean Squared Error) est la métrique d'erreur standard : elle pénalise les grosses erreurs
5. **La MAE** est plus robuste aux outliers, le **RMSE** est interprétable dans l'unité de y
6. **La dérivée** indique la direction de descente — comme la pente sous vos pieds dans le brouillard
7. **La descente de gradient** ajuste les paramètres pas à pas en suivant la pente négative
8. **Le learning rate** contrôle la taille des pas : trop grand → diverge, trop petit → trop lent
9. **Toujours normaliser** les données avant la descente de gradient et la régularisation
10. **Ridge (L2)** réduit tous les coefficients, **Lasso (L1)** met certains à zéro (sélection de features)

---

## ✅ Checklist de validation

- [ ] Je comprends l'analogie "deviner, mesurer, corriger" de l'apprentissage
- [ ] Je sais expliquer la régression linéaire `y = ax + b` intuitivement
- [ ] Je sais calculer la MSE, la MAE et le RMSE à la main et en Python
- [ ] Je comprends pourquoi la MSE met au carré les erreurs (3 raisons)
- [ ] Je sais expliquer la dérivée comme une "direction d'amélioration"
- [ ] Je comprends l'analogie de la montagne dans le brouillard
- [ ] Je sais implémenter la descente de gradient from scratch (~30 lignes)
- [ ] Je comprends l'impact du learning rate sur la convergence
- [ ] Je sais coder une régression linéaire from scratch et avec scikit-learn
- [ ] Je sais interpréter les coefficients d'une régression linéaire
- [ ] Je comprends l'intuition derrière Ridge (L2) et Lasso (L1)
- [ ] Je sais quand utiliser la régularisation et comment choisir alpha
- [ ] J'ai réalisé le notebook "Gradient Descent expliqué à ma grand-mère"

---

**Précédent** : [Chapitre 3 : Vecteurs, Matrices et KNN](03-vecteurs-matrices-knn.md)

**Suivant** : [Chapitre 5 : Probabilités pour ne plus avoir Peur de l'Incertitude](05-probabilites-incertitude.md)
