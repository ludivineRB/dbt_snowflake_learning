---
title: 03_chatbot
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Jour 1 - Module 3 : Donnons une Mémoire à notre IA

Nous savons maintenant envoyer une requête unique à notre LLM. Pour créer une véritable conversation, il nous faut une pièce maîtresse : la **mémoire**. Sans elle, notre LLM est amnésique et chaque question est un nouveau départ. Dans ce module, nous allons construire un chatbot capable de se souvenir du fil de la discussion.

---

## 1. Le Défi : l'Amnésie des LLMs

Fondamentalement, les LLMs sont "sans état" (*stateless*). Chaque requête que vous envoyez est traitée de manière totalement indépendante de la précédente.

* **Vous :** "Quelle est la capitale de la France ?"
* **LLM :** "Paris."
* **Vous :** "Quel est son monument le plus célèbre ?"
* **LLM :** "De quoi parlez-vous ? 'son' se réfère à quoi ?"

Pour que le dialogue soit cohérent, nous devons fournir au LLM l'historique des échanges à chaque nouvelle question.

![Diagramme montrant une requête simple vs une requête avec historique conversationnel](https://i.imgur.com/x5bJdJd.png)

---

## 2. La Stratégie : Gérer l'Historique de Conversation

La solution consiste à maintenir une liste des messages échangés et à l'envoyer avec chaque nouvelle requête.

### Les Limites de la Mémoire

Cette approche, bien qu'efficace, a une contrainte majeure : la **fenêtre de contexte** (*context window*). Chaque modèle de langage a une limite sur la quantité de texte (mesurée en *tokens*) qu'il peut analyser en une seule fois.

| Avantages | Inconvénients & Limites |
| :--- | :--- |
| ✅ **Cohérence :** Le dialogue est fluide et naturel. | ❌ **Taille du Contexte :** Si la conversation devient trop longue, les messages les plus anciens sont "oubliés". |
| ✅ **Expérience Riche :** L'IA peut se souvenir des préférences de l'utilisateur. | ❌ **Coût et Lenteur :** Envoyer un long historique à chaque fois consomme plus de ressources et peut ralentir la réponse. |

> **Pour aller plus loin :** Pour des conversations très longues, des techniques avancées existent, comme la **compression d'historique** (un LLM résume la conversation passée) ou l'utilisation d'une mémoire externe avec **RAG** (que nous verrons bientôt !).

---

## 3. Construire notre Chatbot en Python

Le script ci-dessous met en place une boucle interactive qui :
1.  Attend la question de l'utilisateur.
2.  Ajoute la question à l'historique.
3.  Envoie l'historique complet à l'API d'Ollama.
4.  Affiche la réponse du LLM.
5.  Ajoute la réponse de l'IA à l'historique pour préparer le tour suivant.

**Lien vers le fichier de code :** `code/module3_chatbot.py`

```python
import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"

def chat_with_history(messages):
    """
    Envoie une conversation avec historique à l'API d'Ollama.
    """
    try:
        data = {
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion : {e}")
        return None

if __name__ == "__main__":
    # Initialisation de l'historique de la conversation
    conversation_history = []
    print("🤖 Votre chatbot est prêt ! Tapez 'exit' ou 'quit' pour arrêter.")

    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["exit", "quit"]:
            print("Au revoir !")
            break

        # Ajoute le message de l'utilisateur à l'historique
        conversation_history.append({"role": "user", "content": user_input})

        # Envoie l'historique complet et récupère la réponse
        response_json = chat_with_history(conversation_history)

        if response_json:
            # Ajoute la réponse de l'assistant à l'historique
            assistant_response = response_json['message']
            conversation_history.append(assistant_response)
            print(f"IA : {assistant_response['content']}")
```

### Comment ça marche ?

Le secret réside dans la structure des `messages`. Nous n'envoyons plus un simple `prompt`, mais une liste d'objets, chacun avec un `role` ("user" ou "assistant") et un `content`. C'est le format standard que les modèles de chat comprennent pour suivre une conversation.

---

Vous avez maintenant une application de chat fonctionnelle, la brique fondamentale de tout assistant virtuel.

Ceci conclut notre première journée ! Nous avons mis en place notre environnement, appris à interroger le LLM et construit un chatbot. Demain, nous aborderons un concept qui décuple la puissance des LLMs : le **RAG**.

**[➡️ Prochain Module : Introduction au RAG](./04_introduction_rag.md)**
