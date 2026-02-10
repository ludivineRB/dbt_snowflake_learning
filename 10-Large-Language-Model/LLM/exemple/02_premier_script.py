# -*- coding: utf-8 -*-

# Importe la librairie `requests` pour pouvoir faire des appels HTTP (communiquer avec l'API d'Ollama).
# Importe la librairie `json` pour manipuler les données au format JSON.
import json

import requests

# URL de l'API d'Ollama. Par défaut, Ollama tourne sur le port 11434 de votre machine locale.
url = "http://localhost:11434/api/generate"

# Les données que nous allons envoyer à l'API.
# C'est un dictionnaire Python qui sera converti en JSON.
data = {
    # "model": "mistral", # Vous pouvez changer le modèle ici si vous en avez téléchargé d'autres.
    "model": "llama3.2:latest",
    # "prompt": "Pourquoi le ciel est-il bleu ?",
    "prompt": "donne moi 3 idées de startup dans les énergies renouvelables",
    # "stream": False signifie que nous voulons recevoir la réponse complète en une seule fois,
    # et non pas mot par mot (en streaming).
    "stream": False,
}

# Affiche un message pour indiquer que nous envoyons la requête.
print(f"Envoi de la requête au modèle {data['model']}...")

# Utilise `requests.post` pour envoyer une requête HTTP POST à l'URL spécifiée.
# `json=data` convertit automatiquement notre dictionnaire `data` en format JSON.
# `stream=True` est important pour que la connexion reste ouverte et que nous puissions recevoir les données en continu.
response = requests.post(url, json=data, stream=data.get("stream", False))

# Vérifie si la requête s'est bien déroulée (code de statut HTTP 200).
if response.status_code == 200:
    # Affiche un message de succès.
    print("Réponse reçue !")
    print("\n--- Réponse du LLM ---")

    # Si le streaming est activé, on traite la réponse ligne par ligne.
    if data.get("stream", False):
        full_response = []
        # `response.iter_lines()` permet de parcourir la réponse ligne par ligne.
        for line in response.iter_lines():
            if line:
                # Chaque ligne est un objet JSON, on le décode.
                response_data = json.loads(line)
                # On extrait le contenu de la réponse.
                content = response_data.get("response", "")
                # On l'affiche immédiatement.
                print(content, end="", flush=True)
                full_response.append(content)
        print("\n-----------------------\n")
    else:
        # Si le streaming est désactivé, on traite la réponse comme un seul objet JSON.
        response_data = json.loads(response.text)
        content = response_data.get("response")
        print(content)
        print("-----------------------\n")

else:
    # En cas d'erreur, affiche le code de statut et le message d'erreur.
    print(f"Erreur lors de la requête : {response.status_code}")
    print(response.text)
