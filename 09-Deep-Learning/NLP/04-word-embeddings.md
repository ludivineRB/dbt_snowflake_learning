# 04 - Word Embeddings

[← 03 - Représentations](03-representations-textuelles.md) | [🏠 Accueil](README.md) | [05 - Réseaux Récurrents →](05-reseaux-recurrents.md)

---

## 🧠 Représentation Sémantique

Les **word embeddings** sont des vecteurs denses qui capturent le sens des mots. Les mots similaires sont proches dans l'espace vectoriel.

### 🧮 Word2Vec
Algorithme de Google (2013) basé sur l'idée que le sens d'un mot dépend de ses voisins.
- **Skip-gram** : Prédit les voisins à partir du mot.
- **CBOW** : Prédit le mot à partir de ses voisins.

### 🌐 GloVe (Stanford)
Combine les statistiques globales du corpus pour construire les vecteurs.

### ⚡ FastText (Facebook)
Traite les mots comme des sacs de sous-mots (n-grams de caractères), idéal pour les mots inconnus ou les fautes de frappe.

---

[← 03 - Représentations](03-representations-textuelles.md) | [🏠 Accueil](README.md) | [05 - Réseaux Récurrents →](05-reseaux-recurrents.md)
