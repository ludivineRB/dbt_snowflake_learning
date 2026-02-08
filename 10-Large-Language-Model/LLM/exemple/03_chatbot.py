# -*- coding: utf-8 -*-

import json

import requests

# L'URL de l'API d'Ollama pour la fonctionnalité de chat.
# Notez que nous utilisons "/api/chat" au lieu de "/api/generate".
url = "http://localhost:11434/api/chat"

# L'historique de la conversation.
# C'est une liste de dictionnaires. Chaque dictionnaire représente un message.
# Le "role" peut être "system", "user", ou "assistant".
# - system: Donne des instructions générales au modèle.
# - user: Le message de l'utilisateur.
# - assistant: La réponse du modèle.
history = []


def chat(messages):
    """
    Fonction pour envoyer une liste de messages au LLM et obtenir une réponse.
    """
    data = {
        "model": "llama3.2:latest",
        "messages": messages,
        "stream": False,  # On reçoit la réponse en une seule fois.
    }

    # Envoi de la requête POST avec l'historique des messages.
    response = requests.post(url, json=data)

    # Vérification de la réponse.
    if response.status_code == 200:
        response_data = json.loads(response.text)
        # La réponse de l'API de chat est un objet JSON contenant un champ "message".
        # Ce champ "message" est un dictionnaire avec "role" et "content".
        return response_data.get("message")
    else:
        print(f"Erreur : {response.status_code}")
        print(response.text)
        return None

# Demande à l'utilisateur s'il veut activer la mémoire.
use_memory = input("Activer la mémoire (historique) pour cette session ? (oui/non): ").lower()
memory_enabled = use_memory == "oui"

if memory_enabled:
    print("La mémoire est activée. L'historique de la conversation sera conservé.")
else:
    print("La mémoire est désactivée. Chaque question sera traitée indépendamment.")

# Boucle principale du chatbot.
# Le programme tournera en continu pour permettre une conversation.
while True:
    # Demande à l'utilisateur de saisir sa question.
    user_input = input("Vous: ")

    # Permet à l'utilisateur de quitter la conversation.
    if user_input.lower() in ["exit", "quit"]:
        print("Au revoir !")
        break

    # Si la mémoire est activée, on ajoute le message de l'utilisateur à l'historique.
    if memory_enabled:
        history.append({"role": "user", "content": user_input})
        messages_to_send = history
    else:
        # Si la mémoire est désactivée, on envoie uniquement le message de l'utilisateur.
        messages_to_send = [{"role": "user", "content": user_input}]

    # Affiche un message d'attente.
    print("\nAssistant: ...")

    # Appelle la fonction chat avec les messages appropriés.
    assistant_response = chat(messages_to_send)

    # Si une réponse a été reçue...
    if assistant_response:
        # Affiche le contenu de la réponse de l'assistant.
        print(f"\rAssistant: {assistant_response['content']}\n")
        # Si la mémoire est activée, on ajoute la réponse de l'assistant à l'historique.
        if memory_enabled:
            history.append(assistant_response)
