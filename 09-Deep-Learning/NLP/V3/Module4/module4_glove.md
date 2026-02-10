---
title: Module 4 - GloVe
description: Formation NLP - Module 4 - GloVe
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 📊 GloVe

Global Vectors for Word Representation

[← Word2Vec](module4_word2vec.html)

**GloVe - Statistiques Globales**  
Stanford NLP Group, 2014

[Notebook Pratique →](notebook/module4_glove_demo.ipynb)

## 🌟 Introduction à GloVe

**GloVe (Global Vectors for Word Representation)** est une méthode développée par Jeffrey Pennington, Richard Socher et Christopher Manning à Stanford en 2014. Elle combine les avantages des méthodes de factorisation matricielle et des modèles de contexte local comme Word2Vec.

#### 💡 L'innovation Stanford

Alors que Word2Vec n'utilise que l'information locale (fenêtre glissante), GloVe exploite les **statistiques globales** de co-occurrence de tout le corpus. L'idée : utiliser les informations de fréquence globale pour améliorer l'apprentissage des embeddings.

### 🎯 Pourquoi GloVe ?

*   **Vision globale :** Exploite toutes les statistiques du corpus
*   **Efficacité :** Pré-calcul de la matrice de co-occurrence
*   **Parallélisation :** Plus facile à paralléliser que Word2Vec
*   **Performance :** Souvent supérieur sur les tâches d'analogies

## 🧠 Principe Fondamental

GloVe repose sur une observation simple mais puissante : *les ratios de probabilités de co-occurrence révèlent les relations sémantiques*.

#### 💡 Exemple concret

Considérons les mots "glace" et "vapeur" avec le mot de contexte "solide" :

*   P(solide | glace) sera élevé (la glace est solide)
*   P(solide | vapeur) sera faible (la vapeur n'est pas solide)
*   **Le ratio P(solide | glace) / P(solide | vapeur)** sera très élevé

Ce ratio capture une relation sémantique importante que GloVe exploite.

**Objectif de GloVe :**  
F(wᵢ, wⱼ, w̃ₖ) = Pᵢₖ / Pⱼₖ  
*où F est une fonction des vecteurs de mots qui reproduit les ratios de co-occurrence*

## 📊 Matrice de Co-occurrence Globale

Contrairement à Word2Vec qui traite les paires de mots une par une, GloVe commence par construire une matrice de co-occurrence sur tout le corpus.

#### Exemple de matrice de co-occurrence

*Phrase : "Le roi règne sur son royaume et la reine gouverne"*

roi

règne

reine

royaume

roi

0

2

1

3

règne

2

0

0

1

reine

1

0

0

1

royaume

3

1

1

0

**Xᵢⱼ** = nombre de fois que le mot j apparaît dans le contexte du mot i

1

#### Construction

Parcourir tout le corpus pour compter les co-occurrences

2

#### Pondération

Appliquer des poids selon la distance dans la fenêtre

3

#### Optimisation

Factoriser la matrice pour obtenir les embeddings

## 🎯 Fonction de Coût GloVe

GloVe optimise une fonction de coût qui force les produits scalaires des embeddings à reproduire les logarithmes des probabilités de co-occurrence.

**Fonction de coût :**  
J = Σᵢ,ⱼ f(Xᵢⱼ) (wᵢᵀ w̃ⱼ + bᵢ + b̃ⱼ - log Xᵢⱼ)²  
  
**où :**  
• wᵢ, w̃ⱼ = vecteurs d'embeddings  
• bᵢ, b̃ⱼ = termes de biais  
• f(Xᵢⱼ) = fonction de pondération  
• Xᵢⱼ = co-occurrence observée

#### 🎯 Fonction de Pondération f(x)

Donne moins d'importance aux co-occurrences très rares ou très fréquentes :

**f(x) = (x/xₘₐₓ)^α** si x < xₘₐₓ, sinon 1

Typiquement : xₘₐₓ = 100, α = 0.75

#### 📐 Factorisation Matricielle

L'objectif est de factoriser la matrice log(X) :

**log(Xᵢⱼ) ≈ wᵢᵀ w̃ⱼ + bᵢ + b̃ⱼ**

Les embeddings finaux combinent W et W̃

## ⚖️ GloVe vs Word2Vec

Aspect

Word2Vec

GloVe

**Approche**

Prédictive locale

Factorisation de matrice globale

**Information utilisée**

Contexte local (fenêtre)

Statistiques globales du corpus

**Pré-calcul**

❌ Traitement séquentiel

✅ Matrice de co-occurrence

**Parallélisation**

⚠️ Limitée

✅ Excellente

**Performance analogies**

✅ Très bonne

✅ Souvent supérieure

**Mémoire requise**

✅ Modérée

⚠️ Élevée (matrice)

**Convergence**

⚠️ Plus lente

✅ Plus rapide

## ⚖️ Avantages et Limites

#### ✅ Avantages de GloVe

*   **Vision globale :** Exploite toutes les statistiques du corpus
*   **Efficacité :** Parallélisation facile, convergence rapide
*   **Performance :** Excellent sur les tâches d'analogies
*   **Reproductibilité :** Résultats déterministes
*   **Scalabilité :** Fonctionne bien sur de gros corpus

#### ⚠️ Limites de GloVe

*   **Mémoire :** Stockage de la matrice de co-occurrence
*   **Preprocessing :** Construction de la matrice coûteuse
*   **Vocabulaire :** Taille limitée par la mémoire
*   **Nouveaux mots :** Pas de gestion des mots OOV
*   **Complexité :** Plus de paramètres à ajuster

## 🚀 Applications et Usage

GloVe est particulièrement efficace pour :

#### 🧩 Analogies Complexes

Excelle sur les benchmarks d'analogies grâce à sa vision globale des relations sémantiques.

#### 📊 Analyse Sémantique

Capture efficacement les relations sémantiques subtiles entre concepts.

#### 🔍 Recherche Documentaire

Améliore la recherche sémantique grâce à des embeddings de haute qualité.

#### 🎯 Transfer Learning

Embeddings pré-entraînés utilisables comme features pour diverses tâches NLP.

#### 📚 Sources et Ressources Officielles

Pour approfondir vos connaissances sur GloVe :

[📄 Paper Original - GloVe: Global Vectors for Word Representation](https://aclanthology.org/D14-1162/) [🏛️ Site Officiel Stanford NLP](https://nlp.stanford.edu/projects/glove/) [💻 Code Source Officiel (GitHub)](https://github.com/stanfordnlp/GloVe) [📦 Embeddings Pré-entraînés](https://nlp.stanford.edu/data/glove.6B.zip) [🐍 Utilisation avec Gensim](https://radimrehurek.com/gensim/scripts/glove2word2vec.html)

[← Index Module 4](index.html)

**Prêt pour FastText ?**  
Découvrez la gestion des sous-mots

[FastText →](module4_fasttext.html)
