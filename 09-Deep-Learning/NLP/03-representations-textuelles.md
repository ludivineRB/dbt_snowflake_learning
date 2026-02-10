# 03 - Représentations Textuelles

[← 02 - Preprocessing](02-preprocessing-tokenisation.md) | [🏠 Accueil](README.md) | [04 - Embeddings →](04-word-embeddings.md)

---

## 🔢 Transformer le texte en nombres

Les algorithmes ne comprennent que les vecteurs numériques.

### 🎒 Bag of Words (BoW)
Compte simplement la fréquence de chaque mot dans un document. Ne prend pas en compte l'ordre.

### ⚖️ TF-IDF
Pondère les mots pour donner plus d'importance aux mots rares et discriminants.
- **TF (Term Frequency)** : Fréquence du mot dans le document.
- **IDF (Inverse Document Frequency)** : Rareté du mot dans tout le corpus.

### 🔗 N-grams
Prend en compte des séquences de N mots consécutifs pour capturer un peu de contexte local (ex: Bigrams, Trigrams).

---

[← 02 - Preprocessing](02-preprocessing-tokenisation.md) | [🏠 Accueil](README.md) | [04 - Embeddings →](04-word-embeddings.md)
