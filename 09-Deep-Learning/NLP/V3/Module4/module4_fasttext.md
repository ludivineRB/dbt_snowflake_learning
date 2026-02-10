---
title: 'Module 4 - FastText : Au-delà des Mots Complets'
description: 'Formation NLP - Module 4 - FastText : Au-delà des Mots Complets'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# ⚡ FastText : Au-delà des Mots Complets

Comprendre les mots en les décomposant

**🎯 L'innovation de FastText :**  
"Et si on pouvait comprendre des mots qu'on n'a jamais vus ?"

[← Word2Vec](module4_word2vec.html)

**FastText - La puissance des sous-mots**  
Facebook AI Research, 2016

[Notebook Pratique →](notebook/fasttext_demo.ipynb)

## 1\. 🤔 Le Problème des Mots Inconnus

#### 💡 Imaginez cette situation

Vous entraînez un modèle Word2Vec sur un corpus en français. Plus tard, vous rencontrez le mot "surapprenant" (qui n'était pas dans vos données d'entraînement).

**Que se passe-t-il ?**

#### Avec Word2Vec

*   **Mot inconnu :** "surapprenant"
*   **Résultat :** ❌ ERREUR
*   **Problème :** Aucun vecteur disponible
*   **Solution :** Remplacer par \[UNK\] ou ignorer

L'ordinateur ne sait pas quoi faire !

#### Avec FastText

*   **Mot inconnu :** "surapprenant"
*   **Résultat :** ✅ Vecteur généré
*   **Magie :** Reconnaît "sur", "app", "ant"
*   **Compréhension :** Lié à "apprentissage"

L'ordinateur "devine" intelligemment !

#### 🔍 Exemples concrets de mots inconnus

**Réseaux sociaux :** "trop stylééé", "magnifiiiique", "coolissime"

**Fautes de frappe :** "ordiateur" (au lieu d'ordinateur)

**Néologismes :** "googliser", "ubériser", "instagrammable"

**Mots composés :** "anti-inflammatoire", "multicolore"

## 2\. 🧩 Comment FastText Décompose les Mots

#### 🔍 L'idée géniale

Au lieu de traiter chaque mot comme un bloc indivisible, FastText découpe les mots en petits morceaux appelés **sous-mots** ou **n-grammes de caractères**.

### 📚 Exemple concret : "apprentissage"

#### 🪚 Décomposition en sous-mots

apprentissage

→

<ap

app

ppr

pre

ren

ent

nti

tis

iss

ssa

sag

age

ge>

**📝 Explication :**

*   **< et >** : Marqueurs de début/fin de mot
*   **3-grammes :** Morceaux de 3 caractères
*   **Mot complet :** "apprentissage" lui-même

Vecteur final = Moyenne de tous ces morceaux !

#### 🎯 Pourquoi ça marche ?

**Mot nouveau :** "réapprentissage"

**FastText reconnaît :** "ré-" (préfixe), "app", "ent", "iss", "age" → morceaux d'apprentissage

**Résultat :** Vecteur proche de "apprentissage" automatiquement !

## 3\. ⚖️ FastText vs Word2Vec

#### 📝 Word2Vec (2013)

**Unité de base :** Mots entiers

**Vocabulaire :**

*   "chat" → Vecteur A
*   "chats" → Vecteur B
*   "chatton" → Vecteur C

❌ Aucun lien entre ces mots !

**Mots inconnus :** Impossible à gérer

#### ⚡ FastText (2016)

**Unité de base :** Sous-mots + Mot complet

**Vocabulaire :**

*   "chat" → Vecteur de "<ch", "cha", "hat", "at>" + "chat"
*   "chats" → Partage "<ch", "cha", "hat" avec "chat"
*   "chatton" → Partage "<ch", "cha", "hat" aussi

✅ Lien automatique grâce aux sous-mots !

**Mots inconnus :** Génération automatique

#### 🧠 En résumé

**Word2Vec** dit : "Je connais 50 000 mots exactement"

**FastText** dit : "Je connais 50 000 mots ET je peux comprendre des millions d'autres !"

## 4\. 🌍 FastText Brille avec Certaines Langues

FastText est particulièrement puissant pour les langues qui créent beaucoup de variations de mots :

🇩🇪

#### Allemand

**Mots composés géants :**

"Donaudampfschifffahrt"

(navigation à vapeur sur le Danube)

🇹🇷

#### Turc

**Agglutination :**

"evlerinizden"

\= ev+ler+iniz+den  
(de vos maisons)

🇫🇮

#### Finnois

**15 cas grammaticaux :**

"talo → talossa → talosta"

(maison → dans la maison → de la maison)

🇫🇷

#### Français

**Variantes et erreurs :**

"ordinateur ≈ ordi ≈ ordinatuer"

(tolérance aux fautes)

#### 💡 Pourquoi ces langues bénéficient de FastText

**Problème :** Ces langues créent des millions de formes différentes à partir d'un même mot racine

**Word2Vec :** Doit apprendre chaque forme séparément

**FastText :** Reconnaît les patterns communs et les réutilise

## 5\. 🚀 Quand Utiliser FastText ?

#### 📱 Réseaux Sociaux

**Problème :** Hashtags créatifs, abréviations, fautes

**Exemple :** "#tropcoool", "c genial", "magnifiiiique"

**FastText :** Comprend grâce aux morceaux reconnaissables

#### 🏥 Domaine Médical

**Problème :** Terminologie technique, nouveaux médicaments

**Exemple :** "anti-inflammatoire", "cardio-vasculaire"

**FastText :** Reconnaît les préfixes/suffixes médicaux

#### 🔬 Recherche & Tech

**Problème :** Néologismes, termes techniques nouveaux

**Exemple :** "blockchain", "deepfake", "cryptomonnaie"

**FastText :** Compose à partir de morceaux connus

#### 🌐 Multilingual

**Problème :** Langues avec peu de données

**Exemple :** Langues rares, dialectes

**FastText :** Meilleure généralisation avec peu de données

#### ⚡ Classification Rapide

**Problème :** Classifier des millions de textes rapidement

**Exemple :** Filtrage de spam, modération de contenu

**FastText :** 1000x plus rapide qu'un réseau de neurones

#### 🔍 Recherche Robuste

**Problème :** Utilisateurs font des fautes de frappe

**Exemple :** "voitue" au lieu de "voiture"

**FastText :** Trouve quand même les bons résultats

## 6\. ⚖️ Avantages et Limitations

#### ✅ Avantages de FastText

*   **Mots inconnus :** Génère des vecteurs automatiquement
*   **Morphologie :** Comprend la structure des mots
*   **Langues rares :** Meilleure performance avec peu de données
*   **Fautes de frappe :** Tolérant aux erreurs
*   **Domaines spécialisés :** S'adapte à la terminologie technique
*   **Classification :** Mode ultra-rapide inclus

#### ❌ Limitations

*   **Mémoire :** Utilise plus de RAM (sous-mots)
*   **Vitesse :** Plus lent à entraîner que Word2Vec
*   **Langues isolantes :** Moins utile pour chinois/anglais
*   **Bruit :** Peut apprendre des patterns incorrects
*   **Interprétabilité :** Plus difficile à analyser
*   **Complexité :** Plus de paramètres à ajuster

#### 🎯 Conseil pratique

**Utilisez FastText quand :**

*   Vous travaillez avec des langues riches morphologiquement
*   Vous rencontrez beaucoup de mots inconnus
*   Vous voulez une classification ultra-rapide
*   Vos données contiennent des fautes ou abréviations

**Restez avec Word2Vec quand :**

*   Vous avez un vocabulaire stable et fermé
*   La vitesse et la mémoire sont critiques
*   Vous travaillez principalement en anglais

## 7\. 💻 FastText en Action

#### 📝 Scénario : Classification de commentaires

**Données d'entraînement :** 10 000 commentaires étiquetés (positif/négatif)

**Nouveau commentaire :** "C troppp coooool !!!"

**Word2Vec :** ❌ Mots inconnus ("troppp", "coooool")

**FastText :** ✅ Reconnaît "trop" dans "troppp" et "cool" dans "coooool"

**Résultat :** Classification correcte en "positif"

**\# Exemple simple avec FastText**  
from gensim.models import FastText  
  
\# Entraînement  
model = FastText(  
    sentences=corpus,  
    vector\_size=100,  
    window=5,  
    min\_count=1,  
    min\_n=3,        # N-grammes min (3 caractères)  
    max\_n=6,        # N-grammes max (6 caractères)  
    sg=1  
)  
  
\# Mot connu  
vector1 = model.wv\['ordinateur'\]  
  
\# Mot inconnu - FastText peut le gérer !  
vector2 = model.wv\['ordinatuer'\]  # Faute de frappe  
vector3 = model.wv\['superordinateur'\]  # Mot composé

#### 🎯 Ce qui se passe sous le capot

Pour "superordinateur" (mot jamais vu) :

*   FastText reconnaît "ord", "rdi", "din", "ina", "nat", "ate", "teu", "eur" (morceaux d'ordinateur)
*   Il reconnaît aussi "sup", "upe", "per" (morceaux de super)
*   Il combine ces informations pour créer un vecteur cohérent
*   Le résultat : un vecteur proche de "ordinateur" avec une nuance de "super"

[← Word2Vec](module4_word2vec.html)

**Prêt à expérimenter ?**  
Testez FastText dans le notebook

[Notebook Pratique →](notebook/fasttext_demo.ipynb)
