# 🧠 Deep Learning – Des Fondamentaux aux Applications

## 🎯 Vue d'ensemble

Ce module vous forme au Deep Learning, des bases (neurones, backpropagation) aux applications avancées (vision par ordinateur, NLP).

## 📋 Prérequis

- Python (POO, bibliothèque standard) → Module 01-Fondamentaux/Python
- Machine Learning → Module 08-Machine-Learning
- Recommandé : notions de mathématiques (algèbre linéaire, calcul différentiel)

## 📚 Structure du module

### [01-Fondamentaux-DL](01-Fondamentaux-DL/)
*Base commune obligatoire avant CNN ou NLP.*
| # | Chapitre | Durée | Niveau |
|:--|:---------|:------|:-------|
| 01 | Introduction au Deep Learning | 2h | 🟢 Fondamental |
| 02 | Réseaux de neurones | 3h | 🟢 Fondamental |
| 03 | PyTorch | 3h | 🟡 Intermédiaire |
| 04 | Entraînement pratique | 3h | 🟡 Intermédiaire |

### [02-CNN – Vision par Ordinateur](CNN/)
*Réseaux convolutifs pour le traitement d'images.*
| # | Module | Durée | Niveau |
|:--|:-------|:------|:-------|
| 01 | Fondamentaux des CNN | 45 min | 🟢 Fondamental |
| 02 | Opérations de base | 1h30 | 🟢 Fondamental |
| 03 | Techniques avancées | 2h | 🟡 Intermédiaire |
| 04 | Architectures célèbres | 1h45 | 🟡 Intermédiaire |
| 05 | Applications pratiques | 1h30 | 🟡 Intermédiaire |
| 06 | Projets et exercices | 3h+ | 🔴 Avancé |
| 07 | Métriques et optimisation | 2h | 🔴 Avancé |
| 08 | Couches avancées | 2h | 🔴 Expert |

### [03-NLP – Traitement du Langage](NLP/)
*Du preprocessing au Transformers.*
| # | Module | Durée | Niveau |
|:--|:-------|:------|:-------|
| 01 | Introduction au NLP | 2h | 🟢 Fondamental |
| 02 | Preprocessing et Tokenisation | 4h | 🟢 Fondamental |
| 03 | Représentations textuelles (BoW, TF-IDF) | 3h | 🟡 Intermédiaire |
| 04 | Word Embeddings (Word2Vec, GloVe) | 3h | 🟡 Intermédiaire |
| 05 | Réseaux récurrents (RNN, LSTM) | 4h | 🟡 Intermédiaire |
| 06 | Attention et Transformers | 4h | 🔴 Avancé |
| 07 | BERT et GPT | 4h | 🔴 Avancé |
| 08 | Déploiement en production | 3h | 🔴 Avancé |

## 🛠️ Technologies utilisées

**PyTorch** | **torchvision** | **Hugging Face Transformers** | **NLTK** | **spaCy** | **NumPy**

## 🚀 Parcours recommandé

```
01-Fondamentaux-DL (obligatoire)
         │
    ┌────┴────┐
    │         │
 02-CNN    03-NLP
 (Vision)  (Texte)
    │         │
    └────┬────┘
         │
    10-LLM (suite)
```

Vous pouvez faire CNN et NLP en parallèle ou séquentiellement. Les deux nécessitent les Fondamentaux DL.

---
[🏠 Retour à l'accueil](../README.md)
