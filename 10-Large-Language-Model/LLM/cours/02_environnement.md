---
title: 02_environnement
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Jour 1 - Module 2 : Mettre en Place Votre Atelier IA Local

Maintenant que nous avons exploré la théorie, il est temps de se salir les mains !  
Dans ce module, nous allons installer l'outil essentiel **Ollama** et écrire notre tout premier script Python pour dialoguer avec un Grand Modèle de Langage (LLM) directement sur notre ordinateur.  
C'est la première étape concrète pour donner vie à vos projets d'IA.

---

## Étape 1 : Installer Ollama, le Cœur de Notre Système

**Ollama** est un outil formidable qui simplifie radicalement l'exécution de LLMs en local.  
Il s'occupe de toute la complexité pour nous.

Pour l'installer, rendez-vous sur la page de téléchargement officielle et suivez les instructions pour votre système d'exploitation (Windows, macOS, ou Linux).

➡️ [**Page de Téléchargement d'Ollama**](https://ollama.com/download)

L'installation est simple et rapide.  
Une fois terminée, ouvrez un terminal (ou PowerShell sur Windows) et vérifiez que tout est en ordre avec la commande :

```bash
ollama --version
```

Vous devriez voir apparaître la version d'Ollama, confirmant que l'installation a réussi.

## Étape 2 : Télécharger Votre Premier Modèle de Langage

Ollama a besoin d'un "cerveau" pour fonctionner.  
Nous allons télécharger llama3, un excellent modèle polyvalent développé par Meta, idéal pour commencer.

Dans votre terminal, tapez simplement :

```bash
ollama pull llama3
```

Le téléchargement peut prendre un certain temps, car les modèles sont des fichiers volumineux (plusieurs gigaoctets).  
Une fois terminé, vous pouvez tester le modèle directement dans votre terminal pour une conversation instantanée :

```bash
ollama run llama3
```

Vous pouvez alors poser une question, par exemple :

```
>>> Pourquoi le ciel est-il bleu ?
```

Pour quitter la conversation, tapez `/bye`.

## Étape 3 : Dialoguer avec le LLM en Python

Discuter dans un terminal est amusant, mais le véritable pouvoir se révèle lorsque nous intégrons le LLM dans nos propres applications.  
Ollama rend cela possible en exposant une API locale sur votre machine, que nous pouvons interroger avec un simple script Python.

### Conseil Pro : Toujours Utiliser un Environnement Virtuel !

Avant d'installer des bibliothèques Python, il est crucial d'isoler votre projet.  
Un environnement virtuel (venv) crée une bulle pour votre projet, évitant les conflits entre les dépendances de différents projets.

Créez l'environnement (à la racine de votre projet) :

```bash
python3 -m venv .venv
```

Activez-le :

**Sur macOS/Linux :**
```bash
source .venv/bin/activate
```

**Sur Windows (CMD) :**
```cmd
.venv\Scripts\activate
```

**Sur Windows (PowerShell) :**
```powershell
.venv\Scripts\Activate.ps1
```

Votre invite de commande devrait maintenant afficher `(.venv)`, indiquant que vous êtes dans votre environnement isolé.

### Installation de la Bibliothèque requests

Pour communiquer avec l'API d'Ollama, nous utiliserons la bibliothèque requests, un standard en Python pour effectuer des requêtes HTTP.

```bash
pip install requests
```

### Notre Premier Script d'Interaction

Voici un script simple pour poser une question au modèle llama3 et afficher sa réponse.

📄 **Lien vers le fichier de code :** `code/module2_premier_script.py`

```python
import requests
import json

# L'URL de l'API locale d'Ollama
OLLAMA_API_URL = "http://localhost:11434/api/chat"

def query_llm(prompt):
    """
    Envoie une requête au LLM via l'API d'Ollama et retourne la réponse.
    """
    try:
        # Les données à envoyer dans la requête POST
        data = {
            "model": "llama3",  # Le modèle que nous voulons utiliser
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False  # Pour recevoir la réponse en une seule fois
        }

        # Envoi de la requête POST
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP

        # Extraction et affichage de la réponse
        response_json = response.json()
        print("Réponse du LLM :", response_json['message']['content'])

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API d'Ollama : {e}")
        print("Veuillez vous assurer qu'Ollama est en cours d'exécution.")

if __name__ == "__main__":
    user_prompt = "Explique le concept de trou noir de manière simple."
    query_llm(user_prompt)
```

**Note importante :**  
Pour que ce script fonctionne, le service Ollama doit être lancé sur votre machine.  
Si le script échoue avec une erreur de connexion, c'est probablement que l'application Ollama n'est pas active.

## 🎉 Félicitations !

Vous avez franchi une étape majeure.  
Vous disposez maintenant d'un LLM fonctionnant en local et vous savez comment interagir avec lui en utilisant Python.  
Cette compétence est la fondation sur laquelle nous allons construire des applications de plus en plus sophistiquées.

➡️ **Prochain Module :** Construire un Chatbot simple
