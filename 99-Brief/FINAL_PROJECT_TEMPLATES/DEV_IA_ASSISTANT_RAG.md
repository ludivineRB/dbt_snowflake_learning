# Projet Final : Développeur IA
## Sujet : Assistant IA Spécialisé avec RAG

### 📝 Scénario
Vous travaillez pour une entreprise qui souhaite déployer un assistant IA interne capable de répondre aux questions des employés en se basant sur la documentation technique de l'entreprise (PDF, Markdown, pages web).

### 🏗️ Architecture Attendue
1. **Ingestion documentaire** : Script Python chargeant et découpant les documents sources (PDF, Markdown) en chunks.
2. **Base vectorielle** : Stockage des embeddings dans ChromaDB (ou équivalent).
3. **Pipeline RAG** : Chaîne LangChain orchestrant la recherche sémantique et la génération de réponses via un LLM (Ollama ou API OpenAI).
4. **API de production** : Endpoint FastAPI exposant l'assistant (POST `/ask` avec question → réponse + sources).
5. **Interface utilisateur** : Interface Gradio ou Streamlit pour interagir avec l'assistant.
6. **Conteneurisation** : L'ensemble packagé dans Docker (docker-compose).

### 🎯 Fonctionnalités Attendues
- [ ] Réponse contextualisée avec citation des sources utilisées.
- [ ] Gestion de l'historique de conversation (mémoire).
- [ ] Détection des questions hors-périmètre ("Je ne sais pas").
- [ ] Endpoint de health check et métriques basiques (temps de réponse, nombre de requêtes).

### ✅ Critères de Validation
- [ ] Historique Git propre (Conventional Commits).
- [ ] Présence d'un fichier `docker-compose.yml` pour lancer la stack complète.
- [ ] Code Python respectant les standards PEP8, vérifié par un linter (ruff).
- [ ] Tests unitaires sur le pipeline RAG (pytest, coverage > 60%).
- [ ] README détaillant l'architecture, les choix techniques et comment lancer le projet.
- [ ] Notebook de démonstration montrant 5 questions/réponses pertinentes.

### 💡 Bonus
- Ajout d'un modèle ML classique (classification de tickets, analyse de sentiment) intégré dans l'API.
- Fine-tuning d'un petit modèle sur les données métier.
- Pipeline CI/CD (GitHub Actions) avec linting et tests automatisés.
