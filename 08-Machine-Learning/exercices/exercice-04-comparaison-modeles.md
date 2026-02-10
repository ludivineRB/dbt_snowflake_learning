# Exercice 4 : Comparaison de Modèles — Le Shootout des Algorithmes

**Phase 3 — Chapitres 9, 10 & 11** | Durée estimée : 3h | Niveau : Intermédiaire

---

## 🎯 Objectifs

- Entraîner et comparer au moins 6 algorithmes de classification
- Utiliser une méthodologie rigoureuse (même pipeline, même split, mêmes métriques)
- Tuner les hyperparamètres des meilleurs modèles
- Interpréter les résultats et choisir le meilleur modèle

---

## 📋 Contexte

Votre équipe doit choisir le meilleur modèle pour prédire le churn client. La direction veut un **tableau comparatif** et une **recommandation argumentée**. Le coût d'un faux négatif (client churné non détecté) est 5 fois plus élevé que celui d'un faux positif (offre de rétention envoyée à un client fidèle).

---

## 📝 Instructions

### Partie 1 : Préparation (30 min)

1. Chargez `data/clients_churn.csv`
2. Réutilisez le Pipeline de l'exercice 3 pour le preprocessing
3. Faites un train/test split (80/20, stratifié, random_state=42)
4. **Question** : quelle métrique principale utiliser vu le contexte métier (FN 5x plus coûteux que FP) ? Justifiez.

### Partie 2 : Le Shootout (1h)

5. Entraînez les 6 modèles suivants avec leurs paramètres par défaut :

| # | Modèle | Classe sklearn |
|---|--------|---------------|
| 1 | Régression Logistique | `LogisticRegression(max_iter=1000)` |
| 2 | KNN | `KNeighborsClassifier(n_neighbors=5)` |
| 3 | Arbre de Décision | `DecisionTreeClassifier(max_depth=5)` |
| 4 | Random Forest | `RandomForestClassifier(n_estimators=100)` |
| 5 | Gradient Boosting | `GradientBoostingClassifier(n_estimators=100)` |
| 6 | XGBoost | `XGBClassifier(n_estimators=100, use_label_encoder=False)` |

6. Pour chaque modèle, calculez :
   - Accuracy
   - Precision
   - Recall
   - F1-Score
   - AUC-ROC

7. Affichez un tableau comparatif trié par la métrique principale choisie

### Partie 3 : Tuning des top 3 (1h)

8. Prenez les 3 meilleurs modèles et tuner leurs hyperparamètres avec `GridSearchCV` ou `RandomizedSearchCV` :

   **Pour Random Forest** :
   ```python
   param_grid_rf = {
       'n_estimators': [100, 200, 500],
       'max_depth': [5, 10, 20, None],
       'min_samples_split': [2, 5, 10]
   }
   ```

   **Pour XGBoost** :
   ```python
   param_grid_xgb = {
       'n_estimators': [100, 200, 300],
       'max_depth': [3, 5, 7],
       'learning_rate': [0.01, 0.1, 0.3]
   }
   ```

9. Après tuning, refaites le tableau comparatif

### Partie 4 : Analyse et recommandation (30 min)

10. Pour le meilleur modèle :
    - Tracez la matrice de confusion
    - Tracez la courbe ROC
    - Affichez le feature importance (top 10)

11. Rédigez une recommandation de 5-10 lignes pour la direction :
    - Quel modèle recommandez-vous ?
    - Quelle est sa performance ?
    - Quelles sont les features les plus importantes ?
    - Quelles sont les limites ?

---

## 💡 Indices

```python
from sklearn.model_selection import GridSearchCV, cross_val_score
import pandas as pd

# Pour un beau tableau comparatif
resultats = []
for nom, modele in modeles.items():
    modele.fit(X_train, y_train)
    y_pred = modele.predict(X_test)
    resultats.append({
        'Modèle': nom,
        'Recall': recall_score(y_test, y_pred),
        # ...
    })
df_resultats = pd.DataFrame(resultats).sort_values('Recall', ascending=False)
```

---

## ✅ Critères de réussite

- [ ] Au moins 6 modèles sont comparés avec les mêmes données et métriques
- [ ] La métrique principale est justifiée par le contexte métier
- [ ] Le tuning est fait sur les top 3 modèles avec cross-validation
- [ ] Les résultats avant/après tuning sont présentés
- [ ] La recommandation est argumentée (pas juste "c'est le meilleur score")
- [ ] Les feature importances du meilleur modèle sont analysées
