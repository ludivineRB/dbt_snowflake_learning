---
title: 04_prompt_engineering
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Module 4 : L'Art de Dialoguer avec une IA - Le Prompt Engineering

Le **Prompt Engineering** est sans doute la compétence la plus importante pour quiconque travaille avec des LLMs. C'est l'art et la science de formuler des instructions (des "prompts") pour guider un modèle d'intelligence artificielle vers la réponse la plus précise, pertinente et utile possible. Maîtriser cet art, c'est passer de simple utilisateur à véritable pilote de LLM.

---

## 1. Pourquoi le Prompt Engineering est-il Crucial ?

Un LLM est un outil incroyablement puissant, mais il n'est pas télépathe. La qualité de sa réponse est directement proportionnelle à la qualité de votre question.

* **Clarté sur l'Ambiguïté :** Un bon prompt lève toute ambiguïté et donne une direction claire au modèle.
* **Pertinence sur le Bruit :** Il aide à filtrer les informations non pertinentes pour se concentrer sur l'essentiel.
* **Contrôle sur le Chaos :** Il vous permet de définir le ton, le style, le format et la structure de la sortie.

> **💡 Analogie :** Pensez à un LLM comme à un sculpteur de génie disposant d'un bloc de marbre infini. Le prompt est le ciseau et le marteau. Mieux vous les maniez, plus la sculpture finale sera fidèle à votre vision.

---

## 2. Les Techniques Fondamentales

Il existe plusieurs stratégies pour construire des prompts efficaces, des plus simples aux plus sophistiquées.

### Technique 1 : Le "Zero-Shot" (Tir à l'aveugle)
C'est la forme la plus basique. On pose une question directe sans donner d'exemple.
**Exemple :**
Résume le concept de photosynthèse.


### Technique 2 : Le "Few-Shot" (Avec Exemples)
On fournit au modèle un ou plusieurs exemples du comportement attendu pour le guider. C'est très efficace pour les tâches de formatage ou de classification.

<img src="./images/zero-shot.png" alt="Diagramme comparant Zero-shot et Few-shot prompting" width="600"/>

**Exemple :**
Tâche : Extraire la couleur et l'objet.

Phrase : "Le ciel est bleu."
Résultat : {"objet": "ciel", "couleur": "bleu"}

Phrase : "L'herbe est verte."
Résultat : {"objet": "herbe", "couleur": "verte"}

Phrase : "La voiture est rouge."
Résultat :

*Le modèle comprendra qu'il doit produire un JSON avec les clés "objet" et "couleur".*

### Technique 3 : La "Chain-of-Thought" (Chaîne de Pensée)
Pour les problèmes complexes, on incite le modèle à "réfléchir étape par étape". Cela améliore considérablement sa capacité de raisonnement logique et mathématique.

<img src="./images/chain-of-thought.png" alt="Illustration du concept de Chain-of-Thought" width="600"/>

**Exemple :**
Q : Jean a 5 pommes. Il en achète 2 caisses de 6 pommes chacune. Combien de pommes a-t-il au total ?

R : Réfléchissons étape par étape.

D'abord, on calcule le nombre de pommes dans les deux caisses : 2 caisses * 6 pommes/caisse = 12 pommes.

Ensuite, on ajoute ces nouvelles pommes aux 5 qu'il avait déjà : 12 + 5 = 17 pommes.
La réponse finale est 17.

Le simple fait d'ajouter `"Réfléchissons étape par étape"` peut déclencher ce mode de raisonnement.

---

## 3. Les Bonnes Pratiques du Parfait "Prompteur"

Pour aller plus loin, intégrez ces habitudes dans la construction de vos prompts.

| Pratique | Description | Exemple |
| :--- | :--- | :--- |
| **Persona** | Demandez au modèle d'adopter un rôle spécifique. | `Agis comme un expert en cybersécurité...` |
| **Délimiteurs** | Séparez clairement les instructions du contenu à analyser avec des `"""`, `---`, ou des balises. | `Résume le texte délimité par des triples guillemets : """[texte ici]"""` |
| **Format de Sortie** | Soyez explicite sur le format que vous attendez (JSON, liste, tableau Markdown...). | `Fournis la réponse sous forme de liste à puces.` |
| **Contraintes** | Fixez des limites claires (longueur, mots à éviter, etc.). | `Écris un résumé en 3 phrases maximum.` |
| **Itération** | Le premier prompt est rarement le bon. Testez, analysez la réponse et affinez vos instructions. | *C'est le cœur du métier !* |

Le Prompt Engineering est un processus itératif. N'hésitez jamais à reformuler, ajouter des précisions et expérimenter pour obtenir le résultat parfait.

---

## 4. Outil : Générateur de Prompt

Pour mettre en pratique ces concepts, nous avons créé un petit outil interactif qui vous aide à construire des prompts structurés en suivant les bonnes pratiques.

**[🔧 Accéder au Générateur de Prompt](../exemple/04_générateur_de_prompt.html)**

Cet outil vous guidera pour définir un persona, spécifier le format de sortie, ajouter des contraintes et bien plus encore. C'est un excellent moyen de s'exercer.

---

**[➡️ Prochain Module : Les LLMs avec Outils (Agents)](./05_llm_avec_outils.md)**
