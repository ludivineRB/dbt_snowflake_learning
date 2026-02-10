# Exercice 2 : Distances, Vecteurs et KNN from Scratch

**Phase 1 — Chapitres 3 & 4** | Durée estimée : 2h30 | Niveau : Débutant-Intermédiaire

---

## 🎯 Objectifs

- Calculer des distances entre points (euclidienne, Manhattan)
- Implémenter KNN from scratch
- Comprendre la descente de gradient visuellement
- Coder une régression linéaire simple from scratch

---

## 📋 Contexte

Avant d'utiliser scikit-learn, vous allez **coder les algorithmes vous-même**. L'objectif n'est pas de réinventer la roue, mais de comprendre ce qui se passe sous le capot.

---

## 📝 Instructions

### Partie 1 : Calcul de distances (30 min)

Voici 5 clients représentés par 2 features (normalisées entre 0 et 1) :

| Client | Ancienneté (norm.) | Montant mensuel (norm.) | Churn ? |
|--------|-------------------|------------------------|---------|
| A | 0.8 | 0.2 | Non |
| B | 0.3 | 0.7 | Oui |
| C | 0.9 | 0.3 | Non |
| D | 0.1 | 0.9 | Oui |
| E | 0.5 | 0.5 | Non |

1. **À la main** : calculez la distance euclidienne entre le nouveau client `X = [0.4, 0.6]` et chacun des 5 clients
2. **En Python** : vérifiez vos calculs avec NumPy
3. Avec K=3, quel serait le vote majoritaire pour X ?
4. Répétez avec la distance de Manhattan. Le résultat change-t-il ?

### Partie 2 : KNN from scratch (45 min)

5. Implémentez une fonction `knn_predict(X_train, y_train, x_new, k)` qui :
   - Calcule la distance entre `x_new` et tous les points de `X_train`
   - Trie par distance croissante
   - Prend les K plus proches voisins
   - Retourne la classe majoritaire

6. Testez votre fonction sur les données de la Partie 1
7. Comparez avec `KNeighborsClassifier` de scikit-learn — les résultats sont-ils identiques ?

### Partie 3 : Descente de gradient (45 min)

8. Soit la fonction `f(x) = (x - 3)² + 2` (une parabole dont le minimum est en x=3)
   - Tracez cette fonction avec matplotlib
   - Calculez la dérivée `f'(x) = 2*(x - 3)`
   - Implémentez la descente de gradient :
     ```
     x = point_depart (ex: 10)
     pour chaque itération:
         gradient = 2 * (x - 3)
         x = x - learning_rate * gradient
     ```
   - Tracez la trajectoire de x sur la courbe
   - Testez avec `learning_rate = 0.01`, `0.1`, `0.5`, `1.1` — que se passe-t-il ?

### Partie 4 : Régression linéaire from scratch (30 min)

9. Générez des données synthétiques :
   ```python
   import numpy as np
   np.random.seed(42)
   X = np.random.rand(50) * 10  # Surface (m²)
   y = 2.5 * X + 10 + np.random.randn(50) * 3  # Prix
   ```

10. Implémentez la régression linéaire par descente de gradient :
    - Initialisez `a = 0`, `b = 0`
    - Pour chaque itération :
      - Calculez les prédictions : `y_pred = a * X + b`
      - Calculez l'erreur MSE
      - Calculez les gradients de a et b
      - Mettez à jour a et b
    - Tracez la droite de régression sur le nuage de points

11. Comparez avec `LinearRegression` de scikit-learn

---

## 💡 Indices

```python
# Distance euclidienne
def distance_euclidienne(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Gradient pour régression linéaire
# dMSE/da = -2/n * sum(X * (y - y_pred))
# dMSE/db = -2/n * sum(y - y_pred)
```

---

## ✅ Critères de réussite

- [ ] Les distances sont calculées correctement (à la main ET en Python)
- [ ] KNN from scratch donne les mêmes résultats que scikit-learn
- [ ] La descente de gradient converge vers le minimum de la parabole
- [ ] L'impact du learning rate est compris et documenté
- [ ] La régression linéaire from scratch donne des résultats proches de scikit-learn
