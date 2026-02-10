# 02 - Opérations de Base des CNN

[← 01 - Fondamentaux](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - Techniques Avancées →](03-techniques-avancees.md)

---

## 🏗️ Opérations fondamentales

### 1. Opération de Convolution
Consiste à faire "glisser" un petit filtre (kernel) sur l'image pour détecter des motifs (bords, textures).

### 2. Fonction d'Activation ReLU
**ReLU (Rectified Linear Unit)** : f(x) = max(0, x). Transforme les valeurs négatives en zéro pour introduire de la non-linéarité et accélérer les calculs.

### 3. Max Pooling
Réduit la dimensionnalité en ne gardant que la valeur maximale d'une région (fenêtre 2x2 en général).

### 4. Flatten et Couche Dense
- **Flatten** : Transforme la matrice 2D en vecteur 1D.
- **Dense** : Couche entièrement connectée pour la classification finale.

---

[← 01 - Fondamentaux](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - Techniques Avancées →](03-techniques-avancees.md)
