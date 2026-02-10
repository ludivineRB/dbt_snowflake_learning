---
title: 'Module 3 - N-grammes : Concepts'
description: 'Formation NLP - Module 3 - N-grammes : Concepts'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 📊 N-grammes : Concepts

Comprendre et utiliser les séquences de mots en traitement du langage naturel

## 🎯 Introduction aux N-grammes

Les n-grammes sont des séquences de n éléments (généralement des mots ou des caractères) extraites d'un texte. Ils sont largement utilisés en TAL pour capturer le contexte et les relations entre les mots.

📝 Exemple de phrase :

"Le chat noir dort sur le tapis"

#### 1-grammes (unigrammes)

"Le", "chat", "noir", "dort", "sur", "le", "tapis"

#### 2-grammes (bigrammes)

"Le chat", "chat noir", "noir dort", "dort sur", "sur le", "le tapis"

#### 3-grammes (trigrammes)

"Le chat noir", "chat noir dort", "noir dort sur", "dort sur le", "sur le tapis"

## 🔍 Pourquoi utiliser les N-grammes ?

Les n-grammes permettent de :

*   Capturer le contexte des mots (contrairement au sac de mots simple)
*   Améliorer les performances des modèles de classification de texte
*   Détecter des expressions et des motifs récurrents
*   Améliorer les suggestions de texte et la correction orthographique

**Exemple d'application :** La fonction de saisie prédictive sur votre téléphone utilise des n-grammes pour prédire le mot suivant en fonction des mots précédents.

## ⚙️ Implémentation avec Scikit-learn

Voici comment générer des n-grammes en Python :

```
from sklearn.feature_extraction.text import CountVectorizer

# Exemple de documents
documents = [
    "Le chat noir dort sur le tapis",
    "Le chien joue avec la balle",
    "Le chat attrape la souris"
]

# Création du vectoriseur avec des bigrammes
bigram_vectorizer = CountVectorizer(ngram_range=(2, 2))
X = bigram_vectorizer.fit_transform(documents)

# Affichage des caractéristiques (bigrammes)
print("Bigrammes trouvés:", bigram_vectorizer.get_feature_names_out())

# Création d'un vectoriseur avec des unigrammes et des bigrammes
vectorizer = CountVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(documents)
print("\nUnigrammes et bigrammes:", vectorizer.get_feature_names_out())
```

## 📊 Visualisation des N-grammes

Visualisons les n-grammes les plus fréquents :

```
import pandas as pd
import matplotlib.pyplot as plt

# Création d'un DataFrame avec les fréquences
df_ngrams = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Somme des fréquences par n-gramme
ngram_freq = df_ngrams.sum().sort_values(ascending=False)

# Visualisation des 10 n-grammes les plus fréquents
plt.figure(figsize=(10, 6))
ngram_freq.head(10).plot(kind='barh', color='skyblue')
plt.title('Top 10 des n-grammes les plus fréquents')
plt.xlabel('Fréquence')
plt.tight_layout()
plt.show()
```

## ⚖️ Avantages et Inconvénients

#### ✅ Avantages

*   Simple à implémenter
*   Capture le contexte local
*   Améliore les performances des modèles
*   Utile pour la détection d'expressions

#### ❌ Inconvénients

*   Explosion dimensionnelle
*   Ne capture pas les dépendances à longue distance
*   Peut être sensible au bruit
*   Nécessite beaucoup de données pour les grands n

**Bon à savoir :** En pratique, on utilise souvent des bigrammes ou des trigrammes, car au-delà, la dimensionnalité devient trop importante sans apporter beaucoup plus d'information pertinente.

## 🔍 Cas d'Utilisation des N-grammes

#### 🔤 Correction Orthographique

Détecter et corriger les fautes en utilisant la probabilité des séquences de mots.

#### 📝 Saisie Prédictive

Prédire le mot suivant en fonction des mots précédents.

#### 🧠 Modèles de Langage

Créer des modèles statistiques simples de la langue.

#### 🏷️ Classification de Texte

Améliorer les performances en capturant des expressions caractéristiques.

[← Retour à TF-IDF](module3_tfidf_demo.html) [Voir les démonstrations pratiques →](ngrams_demos.html)
