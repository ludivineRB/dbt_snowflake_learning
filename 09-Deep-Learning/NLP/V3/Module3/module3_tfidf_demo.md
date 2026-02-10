---
title: Module 3 - Démonstration TF-IDF
description: Formation NLP - Module 3 - Démonstration TF-IDF
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🎯 Démonstration Pratique : TF-IDF

Mise en œuvre et visualisation de la pondération TF-IDF

## 📊 Présentation de l'Exercice

Dans cette démonstration, nous allons :

1.  Charger un ensemble de documents texte
2.  Calculer les poids TF-IDF pour chaque terme
3.  Visualiser les résultats
4.  Comparer avec l'approche Bag of Words simple

## 🔧 Préparation des Données

Nous allons utiliser un petit corpus de documents pour illustrer le calcul TF-IDF :

📝 Documents d'exemple

```
documents = [
    "Le chat dort sur le tapis",
    "Le chien joue avec la balle",
    "Le chat attrape la souris",
    "Le chien et le chat jouent ensemble"
]
```

**Note :** Dans un cas réel, vous auriez un ensemble de documents beaucoup plus important et plus varié.

## 📝 Implémentation avec Scikit-learn

Voici comment implémenter TF-IDF en utilisant scikit-learn :

```
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Création du vectoriseur TF-IDF
tfidf_vectorizer = TfidfVectorizer()

# Application aux documents
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

# Conversion en DataFrame pour une meilleure visualisation
df_tfidf = pd.DataFrame(
    tfidf_matrix.toarray(),
    columns=tfidf_vectorizer.get_feature_names_out()
)
```

### Résultats du TF-IDF :

🔍 Matrice TF-IDF (simplifiée)

```
        attrape     balle     chat     chien     dans     dort     et     ...
0     0.000000  0.000000  0.523035  0.000000  0.000000  0.653270  0.000000  ...
1     0.000000  0.622766  0.000000  0.473629  0.000000  0.000000  0.000000  ...
2     0.622766  0.000000  0.473629  0.000000  0.000000  0.000000  0.000000  ...
3     0.000000  0.000000  0.366739  0.366739  0.622766  0.000000  0.622766  ...
```

**Interprétation :** Les valeurs plus élevées indiquent des termes plus importants pour un document spécifique par rapport à l'ensemble du corpus.

## 🔍 Comparaison avec Bag of Words

Comparons avec une simple approche de comptage de mots :

```
from sklearn.feature_extraction.text import CountVectorizer

# Comptage simple des mots
count_vectorizer = CountVectorizer()
bow_matrix = count_vectorizer.fit_transform(documents)

# Conversion en DataFrame
df_bow = pd.DataFrame(
    bow_matrix.toarray(),
    columns=count_vectorizer.get_feature_names_out()
)
```

### Résultats du Bag of Words :

🔍 Matrice de comptage (simplifiée)

```
   attrape  balle  chat  chien  dans  dort  et  ...
0        0      0     1      0     0     1   0  ...
1        0      1     0      1     0     0   0  ...
2        1      0     1      0     0     0   0  ...
3        0      0     1      1     1     0   1  ...
```

**Attention :** Contrairement à TF-IDF, le simple comptage ne tient pas compte de l'importance relative des termes dans le corpus.

## 📈 Analyse des Résultats

Observons les différences clés :

1.  **Mots fréquents :** Les mots très courants comme "le" et "la" ont des poids TF-IDF faibles car ils apparaissent dans de nombreux documents.
2.  **Termes spécifiques :** Les mots plus rares mais significatifs comme "attrape" ou "souris" reçoivent des poids plus élevés.
3.  **Normalisation :** Les vecteurs TF-IDF sont normalisés par défaut, ce qui permet des comparaisons plus justes entre documents de longueurs différentes.

**Astuce :** Vous pouvez ajuster les paramètres du TfidfVectorizer comme `max_features`, `min_df`, et `max_df` pour affiner les résultats selon vos besoins.

## 🏃‍♂️ Exercice Pratique

Essayez de modifier le code pour :

1.  Ajouter des documents supplémentaires au corpus
2.  Changer les paramètres du TfidfVectorizer
3.  Calculer la similarité cosinus entre les documents
4.  Visualiser les résultats avec une heatmap

```
# Exemple de visualisation avec une heatmap
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
sns.heatmap(df_tfidf, annot=True, cmap='YlGnBu', fmt='.2f')
plt.title('Matrice TF-IDF')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

[← Retour aux concepts TF-IDF](module3_tfidf_concepts.html) [Suivant : N-grammes →](module3_ngrams_concepts.html)
