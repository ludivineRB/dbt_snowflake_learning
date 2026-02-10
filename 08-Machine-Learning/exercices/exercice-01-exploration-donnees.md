# Exercice 1 : Exploration de Données — Audit Qualité

**Phase 0 — Chapitres 1 & 2** | Durée estimée : 2h | Niveau : Débutant

---

## 🎯 Objectifs

- Charger et explorer un dataset avec Pandas
- Identifier les types de variables
- Détecter les problèmes de qualité (valeurs manquantes, aberrantes, doublons)
- Produire un rapport d'exploration en français

---

## 📋 Contexte

Vous venez d'être embauché comme Data Analyst junior chez **TelcoPlus**, un opérateur télécom. Votre manager vous confie le fichier `clients_churn.csv` et vous demande : *"Avant de construire quoi que ce soit, dis-moi ce qu'il y a dans ces données."*

---

## 📝 Instructions

### Partie 1 : Chargement et premiers regards (30 min)

1. Chargez le fichier `data/clients_churn.csv` avec Pandas
2. Répondez à ces questions :
   - Combien de lignes et de colonnes ?
   - Quels sont les noms des colonnes ?
   - Quels sont les types de données (dtypes) ?
   - Y a-t-il des valeurs manquantes ? Si oui, combien et dans quelles colonnes ?
3. Affichez les 5 premières et 5 dernières lignes

### Partie 2 : Statistiques descriptives (30 min)

4. Pour chaque variable **numérique** :
   - Calculez : moyenne, médiane, écart-type, min, max
   - Y a-t-il des valeurs qui semblent aberrantes ?
5. Pour chaque variable **catégorielle** :
   - Combien de valeurs uniques ?
   - Quelle est la distribution (value_counts) ?
6. Quelle est la proportion de clients qui ont churné vs non ?

### Partie 3 : Visualisations (30 min)

7. Créez un histogramme pour chaque variable numérique
8. Créez un countplot pour la variable cible (churn)
9. Créez une heatmap de corrélation entre les variables numériques
10. Créez un boxplot pour détecter les outliers sur 2-3 variables

### Partie 4 : Rapport d'audit (30 min)

11. Rédigez un court rapport (en markdown ou dans un notebook) qui répond à :
    - **Taille du dataset** : nombre d'observations et de features
    - **Qualité** : problèmes identifiés (manquants, aberrants, doublons)
    - **Distribution de la cible** : équilibrée ou déséquilibrée ?
    - **Variables potentiellement utiles** : lesquelles semblent liées au churn ?
    - **Recommandations** : que faut-il nettoyer/transformer avant de modéliser ?

---

## 💡 Indices

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement
df = pd.read_csv("../data/clients_churn.csv")

# Fonctions utiles
df.shape          # (lignes, colonnes)
df.info()         # Types et valeurs manquantes
df.describe()     # Stats descriptives
df.isnull().sum() # Nombre de NaN par colonne
df.duplicated().sum()  # Nombre de doublons
df['colonne'].value_counts()  # Distribution d'une catégorielle
```

---

## ✅ Critères de réussite

- [ ] Le dataset est chargé correctement
- [ ] Les types de variables sont identifiés (numériques vs catégorielles)
- [ ] Les valeurs manquantes sont quantifiées
- [ ] Au moins 4 visualisations sont produites
- [ ] Le rapport d'audit couvre les 5 points demandés
- [ ] **Aucune ligne de Machine Learning** — c'est un exercice d'exploration pure
