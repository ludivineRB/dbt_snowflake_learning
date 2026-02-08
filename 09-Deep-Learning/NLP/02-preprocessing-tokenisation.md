# 02 - Preprocessing et Tokenisation

[← 01 - Introduction](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - Représentations →](03-representations-textuelles.md)

---

## 🧹 Le Pipeline de Preprocessing

Avant d'être analysé, le texte brut doit être nettoyé et structuré.

### 1. Nettoyage
- Suppression de la ponctuation, des caractères spéciaux et des URLs.
- Conversion en minuscules (lowercase).
- Gestion des accents.

### 2. Tokenisation
Action de découper une phrase en unités minimales appelées **tokens** (mots ou sous-mots).

### 3. Stopwords
Suppression des mots fréquents qui n'apportent pas de sens (le, la, et, de...).

### 4. Normalisation
- **Stemming** : Réduction à la racine brute (ex: "mangé" -> "mang").
- **Lemmatisation** : Retour à la forme du dictionnaire (ex: "mangé" -> "manger").

---

[← 01 - Introduction](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - Représentations →](03-representations-textuelles.md)
