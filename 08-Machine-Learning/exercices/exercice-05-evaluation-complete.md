# Exercice 5 : Évaluation Complète — Prouver que le Modèle est Bon

**Phase 4 — Chapitres 12 & 13** | Durée estimée : 2h30 | Niveau : Intermédiaire-Avancé

---

## 🎯 Objectifs

- Maîtriser toutes les métriques de classification
- Comprendre et diagnostiquer l'overfitting avec les courbes d'apprentissage
- Ajuster le seuil de décision selon le contexte métier
- Utiliser la cross-validation pour une estimation robuste

---

## 📋 Contexte

Le modèle de churn est prêt (exercice 4). Mais avant le déploiement, l'équipe Data Engineering exige un **rapport d'évaluation complet** prouvant que le modèle est fiable et généralisable.

---

## 📝 Instructions

### Partie 1 : Le piège de l'accuracy (30 min)

1. Créez un dataset très déséquilibré :
   ```python
   # 95% classe 0, 5% classe 1
   import numpy as np
   y_fake = np.array([0]*950 + [1]*50)
   y_stupide = np.zeros(1000)  # Prédit toujours 0
   ```

2. Calculez l'accuracy du "modèle stupide" — est-elle bonne ?
3. Calculez la precision, le recall et le F1 — que constatez-vous ?
4. Expliquez en 3 phrases pourquoi l'accuracy est trompeuse ici

### Partie 2 : Seuil de décision (45 min)

5. Sur votre meilleur modèle (exercice 4), récupérez les probabilités :
   ```python
   y_proba = model.predict_proba(X_test)[:, 1]
   ```

6. Tracez Precision et Recall en fonction du seuil (de 0.1 à 0.9)

7. **Contexte A** — Rétention client (FN coûteux) :
   - Quel seuil maximise le Recall tout en gardant Precision > 0.4 ?
   - Combien de clients churners supplémentaires détecte-t-on ?

8. **Contexte B** — Budget limité pour la rétention (FP coûteux) :
   - Quel seuil maximise la Precision tout en gardant Recall > 0.6 ?
   - Combien de budget économise-t-on en faux positifs ?

9. Tracez la courbe ROC et la courbe Precision-Recall

### Partie 3 : Cross-validation (30 min)

10. Évaluez votre modèle avec :
    - 5-Fold Cross-Validation
    - Stratified 5-Fold
    - Repeated 5-Fold (3 répétitions)

11. Comparez :
    - Les scores moyens et les écarts-types
    - Y a-t-il une grande variance entre les folds ?
    - Que nous apprend l'écart-type ?

### Partie 4 : Courbes d'apprentissage (30 min)

12. Tracez les courbes d'apprentissage avec `learning_curve` de sklearn :
    ```python
    from sklearn.model_selection import learning_curve
    ```

13. Diagnostiquez :
    - Y a-t-il de l'overfitting ? (train score >> test score)
    - Y a-t-il de l'underfitting ? (les deux scores sont bas)
    - Plus de données aideraient-elles ? (les courbes convergent-elles ?)

14. Tracez les courbes de validation pour 1 hyperparamètre clé

### Partie 5 : Rapport final (15 min)

15. Créez un résumé d'évaluation avec :

```
╔══════════════════════════════════════╗
║  RAPPORT D'ÉVALUATION — Churn Model ║
╠══════════════════════════════════════╣
║  Modèle     : [nom]                 ║
║  Dataset    : [taille]              ║
║  Features   : [nombre]              ║
╠══════════════════════════════════════╣
║  MÉTRIQUES (test set)               ║
║  Accuracy   : X.XXXX                ║
║  Precision  : X.XXXX                ║
║  Recall     : X.XXXX                ║
║  F1-Score   : X.XXXX                ║
║  AUC-ROC    : X.XXXX                ║
╠══════════════════════════════════════╣
║  CROSS-VALIDATION (5-fold)          ║
║  F1 moyen   : X.XXXX ± X.XXXX      ║
╠══════════════════════════════════════╣
║  DIAGNOSTIC                         ║
║  Overfitting : Oui/Non              ║
║  Stabilité   : Bonne/Moyenne        ║
╚══════════════════════════════════════╝
```

---

## ✅ Critères de réussite

- [ ] Le piège de l'accuracy est compris et démontré
- [ ] Le seuil optimal est différent selon le contexte métier
- [ ] La cross-validation est implémentée correctement (stratifiée)
- [ ] Les courbes d'apprentissage sont tracées et interprétées
- [ ] Le rapport d'évaluation est complet et professionnel
