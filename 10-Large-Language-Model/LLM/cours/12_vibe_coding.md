---
title: 12_vibe_coding
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# 12. Outils de Développement Assisté par IA

## Introduction au "Vibe Coding"

Le "Vibe Coding" est une approche de développement logiciel qui met l'accent sur une collaboration fluide et intuitive entre le développeur et l'intelligence artificielle. Plutôt que de simplement utiliser l'IA comme un outil de complétion de code, le Vibe Coding vise à intégrer l'IA plus profondément dans le processus de développement, en l'utilisant pour la génération de code, le refactoring, le débogage et même la conception d'architecture. L'objectif est de créer une expérience de développement plus naturelle et efficace, où le développeur peut se concentrer sur la logique métier et la créativité, tandis que l'IA s'occupe des tâches plus répétitives et fastidieuses.

## Cursor : L'éditeur de code "IA-first"

Cursor est un éditeur de code "IA-first" basé sur VS Code. Il intègre nativement des fonctionnalités d'intelligence artificielle pour améliorer la productivité des développeurs. Voici quelques-unes de ses fonctionnalités clés :

*   **Chat avec votre codebase** : Vous pouvez poser des questions sur l'ensemble de votre projet en langage naturel. L'IA de Cursor a une connaissance approfondie de votre code et peut vous aider à comprendre des parties complexes, à trouver des définitions de fonctions ou à obtenir des suggestions de refactoring.
*   **Édition en ligne** : Sélectionnez un bloc de code et donnez une instruction en langage naturel pour le modifier. C'est particulièrement utile pour les petites modifications et le refactoring.
*   **Génération de code** : Cursor peut générer du code à partir d'une simple instruction. Vous pouvez lui demander de créer une fonction, une classe ou même un fichier entier.
*   **Aide au débogage** : L'IA peut vous aider à analyser le code, à suggérer des corrections et à fournir des explications en langage clair.
*   **Environnement familier** : Comme Cursor est un fork de VS Code, vous pouvez importer vos extensions, thèmes et raccourcis clavier existants.

## VS Code avec l'extension Continue

Continue est une extension open-source pour VS Code qui vous permet de créer votre propre assistant de codage IA. Elle est hautement personnalisable et peut être configurée pour utiliser des modèles locaux via Ollama, vous offrant ainsi une solution privée et puissante.

### Configuration avec Ollama

Pour utiliser Continue avec Ollama, suivez ces étapes :

1.  **Installez Ollama** : Si ce n'est pas déjà fait, installez Ollama sur votre machine.
2.  **Téléchargez un modèle** : Utilisez la commande `ollama pull <nom_du_modele>` pour télécharger un modèle de langage adapté au codage, comme `codellama` ou `starcoder2`.
3.  **Installez l'extension Continue** : Recherchez "Continue" dans le Marketplace de VS Code et installez l'extension.
4.  **Configurez Continue** :
    *   Ouvrez la palette de commandes (Cmd+Shift+P ou Ctrl+Shift+P) et recherchez "Continue: Open Config".
    *   Dans le fichier `config.json`, ajoutez une nouvelle configuration pour Ollama en spécifiant l'URL de l'API (généralement `http://localhost:11434`), le nom du modèle que vous avez téléchargé et un titre pour la configuration.

Une fois configuré, vous pouvez interagir avec votre assistant IA local directement dans VS Code, en bénéficiant d'une complétion de code intelligente, d'un chat contextuel et de bien d'autres fonctionnalités.


## Exemples Pratiques

Voici quelques scénarios où ces outils peuvent être particulièrement utiles :

### 1. Refactoring de code avec Cursor

Imaginez que vous avez une fonction complexe que vous souhaitez refactoriser.

**Code original :**
```python
def process_data(data):
    # ... 15 lignes de code complexes ...
    return result
```

**Avec Cursor :**
1.  Sélectionnez la fonction `process_data`.
2.  Ouvrez le chat et tapez : "Refactorise cette fonction pour la rendre plus lisible et modulaire. Sépare la logique de traitement des données de la logique de validation."
3.  Cursor va analyser la fonction et proposer une version refactorisée, potentiellement en créant de nouvelles fonctions auxiliaires.

### 2. Génération de tests unitaires avec VS Code + Continue

Vous venez d'écrire une nouvelle fonction et vous devez créer des tests unitaires pour celle-ci.

**Votre fonction :**
```python
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

**Avec Continue :**
1.  Ouvrez la fenêtre de chat de Continue.
2.  Tapez : "Génère des tests unitaires pour la fonction `calculate_average` en utilisant le framework pytest. N'oublie pas de tester le cas où la liste est vide."
3.  Continue va générer un ensemble de tests que vous pourrez ensuite placer dans votre fichier de test.

### 3. Comprendre un nouveau projet

Lorsque vous rejoignez un nouveau projet, il peut être difficile de comprendre la base de code.

**Avec Cursor ou Continue :**
1.  Ouvrez le chat.
2.  Posez des questions comme :
    *   "Quel est le point d'entrée de l'application ?"
    *   "Comment est gérée l'authentification des utilisateurs ?"
    *   "Où se trouve la logique de connexion à la base de données ?"
    
3.  L'IA vous guidera à travers le code, vous faisant gagner un temps précieux.

