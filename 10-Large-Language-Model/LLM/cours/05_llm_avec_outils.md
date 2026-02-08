---
title: 05_llm_avec_outils
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Module 5 : Donnez des Super-Pouvoirs à votre IA avec des Outils (Agents)

Nous avons vu comment les LLMs peuvent discuter (Chatbot) et interroger une base de connaissances (RAG). Il est temps de passer à la vitesse supérieure. Et si notre LLM pouvait **agir** ? S'il pouvait utiliser des outils pour accomplir des tâches dans le monde réel, bien au-delà de la simple génération de texte ?

Bienvenue dans le monde des **Agents IA** et du **Function Calling**.

---

## 1. Qu'est-ce qu'un Agent IA ?

Un **Agent** est un système qui utilise un LLM comme son "cerveau" pour raisonner et interagir avec son environnement via des outils. Au lieu de simplement répondre à une question, un agent suit un cycle de réflexion-action :

1.  **Observer & Raisonner :** L'agent analyse la demande de l'utilisateur et son état actuel. Il décompose le problème et choisit le meilleur outil pour la prochaine étape.
2.  **Agir :** Il utilise un ou plusieurs outils disponibles (une calculatrice, une API météo, un moteur de recherche...).
3.  **Itérer :** Il observe le résultat de son action, raisonne à nouveau, et décide de la prochaine étape, jusqu'à ce que la mission soit accomplie.

<img src="./images/ai_agent.png" alt="Illustration d'un Agent IA, un cerveau central connecté à divers outils comme une calculatrice, une loupe de recherche, une base de données." width="600"/>

> **💡 Analogie :** Imaginez un chef de projet (le LLM) qui ne fait pas tout lui-même. Il analyse une demande complexe, puis délègue les tâches à des experts spécialisés (les outils) : l'un pour les calculs, l'autre pour la recherche d'informations, etc.

---

## 2. Le "Function Calling" : Comment l'IA Appelle les Outils

Le **Function Calling** (ou Appel de Fonction) est la capacité du LLM à décider *quand* et *comment* appeler un outil.

Voici le déroulement typique :

<img src="./images/Function_Calling.png" alt="Diagramme du processus de Function Calling" width="600"/>

1.  **Définition :** Vous fournissez au LLM une liste des outils disponibles, avec une description claire de ce que chaque outil fait et des paramètres qu'il attend.
2.  **Décision :** Lorsque l'utilisateur pose une question, le LLM analyse si l'un des outils peut l'aider.
3.  **Appel :** S'il décide d'utiliser un outil, le LLM ne génère pas une réponse, mais un **appel de fonction structuré** (généralement en JSON), avec le nom de la fonction et les bons arguments.
4.  **Exécution :** Votre application intercepte cet appel, exécute la fonction correspondante avec les arguments fournis.
5.  **Réponse :** Le résultat de l'exécution est renvoyé au LLM, qui l'utilise pour formuler la réponse finale à l'utilisateur.

---

## 3. Implémentation avec LangChain

LangChain est le framework idéal pour construire des agents. Il fournit tous les composants nécessaires pour orchestrer ce ballet complexe.

**Lien vers le fichier de code :** `code/module5_llm_tools.py`

### Composants clés du script :

* **`Tool` :** La classe LangChain pour "emballer" une fonction Python et la rendre utilisable par le LLM. On lui donne un nom, la fonction, et une description claire. *La qualité de la description est cruciale !*
* **`create_react_agent` :** Une fonction qui assemble le LLM, les outils et un prompt système spécial pour créer un agent suivant le pattern **ReAct** (Reason, Act).
* **`AgentExecutor` :** C'est le moteur qui fait tourner l'agent. Il gère la boucle d'observation, de raisonnement et d'action.

### Comment ça fonctionne (Exemple de la Calculatrice)

Dans le script, nous créons un outil `calculator`. Quand vous demandez `"Quel est le résultat de 123 * 456 ?"`:

1.  **L'Agent Raisonne :** *"La question est un calcul. Je dois utiliser l'outil `calculator`."*
2.  **L'Agent Agit :** Il génère un appel à l'outil `calculator` avec l'entrée `"123 * 456"`.
3.  **Votre Code Exécute :** Votre script exécute la fonction et obtient le résultat `56088`.
4.  **L'Agent Observe :** Il reçoit `56088`.
5.  **L'Agent Répond :** Il formule la réponse finale : *"Le résultat de 123 * 456 est 56088."*

En activant `verbose=True` dans l'`AgentExecutor`, vous pourrez voir toute cette "pensée" interne s'afficher dans votre terminal, ce qui est extrêmement instructif.

---

Les agents ouvrent la porte à des applications d'IA dynamiques, capables de résoudre des problèmes du monde réel. C'est l'une des frontières les plus excitantes de l'IA générative.

**[➡️ Prochain Module : Les Serveurs MCP (Architecture Avancée pour Agents)](./06_mcp_servers.md)**
