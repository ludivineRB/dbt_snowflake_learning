#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import datetime
import subprocess
import os
from typing import Dict, List, Any
import feedparser
import wikipediaapi

class OllamaToolsClient:
    """Client Ollama avec système d'outils intégré"""
    
    def __init__(self, model="llama3.2:latest", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.tools = self._init_tools()
    
    def _init_tools(self) -> Dict[str, callable]:
        """Initialise les outils disponibles"""
        return {
            "web_search": self._web_search,
            "news_feed": self._get_news_feed,
            "wikipedia_search": self._wikipedia_search,
            "file_operations": self._file_operations,
            "system_info": self._system_info,
            "weather": self._get_weather,
            "calculate": self._calculate,
            "translate": self._translate_text,
            "summarize_url": self._summarize_url
        }
    
    # === OUTILS DISPONIBLES ===
    
    def _web_search(self, query: str, num_results: int = 5) -> str:
        """Recherche web via DuckDuckGo API"""
        try:
            # API DuckDuckGo (gratuite)
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            results = []
            if data.get('RelatedTopics'):
                for topic in data['RelatedTopics'][:num_results]:
                    if 'Text' in topic:
                        results.append(f"• {topic['Text']}")
            
            return f"Résultats de recherche pour '{query}':\n" + "\n".join(results) if results else "Aucun résultat trouvé"
        except Exception as e:
            return f"Erreur de recherche: {e}"
    
    def _get_news_feed(self, topic: str = "intelligence artificielle") -> str:
        """Récupère les dernières actualités via RSS"""
        try:
            # Flux RSS français
            feeds = [
                f"https://news.google.com/rss/search?q={topic}&hl=fr&gl=FR&ceid=FR:fr",
                "https://www.lemonde.fr/rss/une.xml",
                "https://www.lesechos.fr/rss.xml"
            ]
            
            all_news = []
            for feed_url in feeds[:1]:  # Premier flux seulement
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:3]:
                        date = getattr(entry, 'published', 'Date inconnue')
                        all_news.append(f"• {entry.title}\n  Source: {date}")
                except:
                    continue
            
            return f"Actualités récentes sur '{topic}':\n" + "\n".join(all_news)
        except Exception as e:
            return f"Erreur actualités: {e}"
    
    def _wikipedia_search(self, query: str) -> str:
        """Recherche sur Wikipedia"""
        try:
            wiki = wikipediaapi.Wikipedia('fr')
            page = wiki.page(query)
            
            if page.exists():
                summary = page.summary[:500] + "..." if len(page.summary) > 500 else page.summary
                return f"Wikipedia - {page.title}:\n{summary}"
            else:
                return f"Aucune page Wikipedia trouvée pour '{query}'"
        except Exception as e:
            return f"Erreur Wikipedia: {e}"
    
    def _file_operations(self, operation: str, path: str = "", content: str = "") -> str:
        """Opérations sur fichiers"""
        try:
            if operation == "read" and os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f"Contenu de {path}:\n{f.read()[:1000]}..."
            elif operation == "write":
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Fichier {path} créé avec succès"
            elif operation == "list":
                files = os.listdir(path or ".")
                return f"Fichiers dans {path or 'le répertoire actuel'}:\n" + "\n".join(files[:10])
            else:
                return "Opération non supportée (read, write, list)"
        except Exception as e:
            return f"Erreur fichier: {e}"
    
    def _system_info(self) -> str:
        """Informations système"""
        try:
            info = []
            info.append(f"Date/Heure: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            info.append(f"Répertoire: {os.getcwd()}")
            
            # CPU et mémoire (Linux/Mac)
            try:
                cpu_info = subprocess.check_output("top -l1 | grep 'CPU usage'", shell=True).decode()
                info.append(f"CPU: {cpu_info.strip()}")
            except:
                info.append("CPU: Information non disponible")
            
            return "\n".join(info)
        except Exception as e:
            return f"Erreur système: {e}"
    
    def _get_weather(self, city: str = "Paris") -> str:
        """Météo via API gratuite"""
        try:
            # OpenWeatherMap (nécessite une clé API gratuite)
            # Remplacez YOUR_API_KEY par une vraie clé
            api_key = "YOUR_API_KEY"
            if api_key == "YOUR_API_KEY":
                return f"Météo simulée pour {city}: 15°C, nuageux (configurez une vraie API key)"
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"Météo à {city}: {temp}°C, {desc}"
            else:
                return f"Impossible d'obtenir la météo pour {city}"
        except Exception as e:
            return f"Erreur météo: {e}"
    
    def _calculate(self, expression: str) -> str:
        """Calculatrice avancée"""
        try:
            # Sécurisation de eval
            allowed_chars = set('0123456789+-*/.() ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"{expression} = {result}"
            else:
                return "Expression non autorisée (caractères suspects)"
        except Exception as e:
            return f"Erreur calcul: {e}"
    
    def _translate_text(self, text: str, target_lang: str = "en") -> str:
        """Traduction basique (nécessiterait une vraie API)"""
        # Ici vous pourriez intégrer Google Translate API, DeepL, etc.
        return f"Traduction simulée de '{text}' vers {target_lang}: [TRADUCTION]"
    
    def _summarize_url(self, url: str) -> str:
        """Résumé d'une page web"""
        try:
            response = requests.get(url, timeout=10)
            # Extraction basique du texte (à améliorer avec BeautifulSoup)
            content = response.text[:1000]
            return f"Contenu de {url}:\n{content}..."
        except Exception as e:
            return f"Erreur URL: {e}"
    
    # === MOTEUR PRINCIPAL ===
    
    def _detect_tools_needed(self, input_text: str) -> List[str]:
        """Détecte automatiquement les outils nécessaires"""
        text_lower = input_text.lower()
        tools_needed = []
        
        # Patterns de détection
        patterns = {
            "web_search": ["recherche", "chercher", "veille", "actualités", "dernières", "tendances"],
            "news_feed": ["actualités", "news", "nouvelles", "info"],
            "wikipedia_search": ["wikipedia", "définition", "qu'est-ce que"],
            "calculate": ["calcul", "calculer", "+", "-", "*", "/", "="],
            "weather": ["météo", "temps", "température"],
            "system_info": ["système", "heure", "date", "info"],
            "file_operations": ["fichier", "lire", "écrire", "dossier"]
        }
        
        for tool, keywords in patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                tools_needed.append(tool)
        
        return tools_needed or ["web_search"]  # Par défaut
    
    def _call_ollama(self, prompt: str) -> str:
        """Appel à Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Erreur Ollama: {response.status_code}"
        except Exception as e:
            return f"Erreur de connexion Ollama: {e}"
    
    def create_response(self, input_text: str, tools: List[str] = None) -> str:
        """Méthode principale - équivalent de client.responses.create()"""
        print(f"🔍 Traitement: {input_text}")
        
        # Détection automatique des outils si non spécifiés
        if tools is None:
            tools = self._detect_tools_needed(input_text)
        
        print(f"🔧 Outils détectés: {tools}")
        
        # Exécution des outils
        tool_results = []
        for tool_name in tools:
            if tool_name in self.tools:
                print(f"   ⚡ Exécution: {tool_name}")
                
                # Extraction des paramètres (simplifié)
                if tool_name == "web_search":
                    result = self.tools[tool_name](input_text)
                elif tool_name == "news_feed":
                    topic = "intelligence artificielle" if "ia" in input_text.lower() or "intelligence artificielle" in input_text.lower() else "actualités"
                    result = self.tools[tool_name](topic)
                elif tool_name == "calculate":
                    import re
                    expr = re.search(r'[\d\s+\-*/().]+', input_text)
                    if expr:
                        result = self.tools[tool_name](expr.group().strip())
                    else:
                        result = "Expression mathématique non trouvée"
                else:
                    result = self.tools[tool_name]()
                
                tool_results.append(f"[{tool_name}] {result}")
        
        # Génération de la réponse finale avec Ollama
        context = "\n\n".join(tool_results)
        
        prompt = f"""Basé sur les informations suivantes, réponds de manière structurée et utile à la demande de l'utilisateur.

DEMANDE: {input_text}

DONNÉES COLLECTÉES:
{context}

CONSIGNES:
- Synthétise les informations de manière claire
- Structure ta réponse (listes, points si approprié)
- Reste factuel et précis
- Si c'est une veille, présente 5 points clés maximum

RÉPONSE:"""

        final_response = self._call_ollama(prompt)
        
        return final_response

# === UTILISATION ===

def main():
    # Initialisation du client
    client = OllamaToolsClient()
    
    # Exemples d'utilisation
    examples = [
        "faire une veille sur l'intelligence artificielle et les dernières avancées en 2025 en 5 points",
        "quelle est la météo à Paris ?",
        "calcule 125 * 67 + 234",
        "cherche des informations sur les transformers en IA",
        "donne-moi les actualités du jour"
    ]
    
    print("🤖 === Client Ollama avec Outils ===\n")
    print("Exemples de commandes:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")
    
    print("\n" + "="*50)
    
    while True:
        user_input = input("\n💬 Votre demande (ou 'exit'): ").strip()
        
        if user_input.lower() == 'exit':
            break
        
        if not user_input:
            continue
        
        try:
            # Équivalent de client.responses.create()
            response = client.create_response(user_input)
            print(f"\n🤖 Réponse:\n{response}")
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()