# 🤖 Large Language Models – Du Concept à la Production

## 🎯 Vue d'ensemble

Ce module vous forme à utiliser, intégrer et personnaliser les LLM (Large Language Models). De l'installation locale avec Ollama jusqu'au fine-tuning, en passant par le RAG et les agents multi-outils.

## 📋 Prérequis

- Python (POO, API REST) → Module 01-Fondamentaux/Python
- Deep Learning / NLP (Transformers, BERT, GPT) → Module 09-Deep-Learning/03-NLP
- SQL basique → Module 01-Fondamentaux/SQL (pour le module RAG-SQL)

## 📚 Contenu du cours

### Jour 1 : Fondations LLM
| # | Module | Durée | Contenu |
|:--|:-------|:------|:--------|
| 01 | Introduction et concepts | 1h | LLM, Cloud vs Local, Ollama |
| 02 | Environnement local | 1h | Installation Ollama, premier script |
| 03 | Chatbot avec mémoire | 1h30 | Historique de conversation |
| 04 | Prompt Engineering | 1h | Zero-shot, Few-shot, Chain-of-Thought |
| 05 | Prompt Engineering avancé | 1h30 | Tree-of-Thoughts, évaluation, optimisation |
| 06 | Choisir le bon modèle LLM | 1h | Benchmarks, matrice de décision |

### Jour 2 : RAG & Agents
| # | Module | Durée | Contenu |
|:--|:-------|:------|:--------|
| 07 | LLM avec outils (Agents) | 1h30 | Function calling, tool integration |
| 08 | MCP Servers | 1h | Model Context Protocol |
| 09 | Introduction au RAG | 1h | Retrieval-Augmented Generation |
| 10 | Base de données vectorielle | 1h30 | Embeddings, ChromaDB |
| 11 | Interrogation RAG | 2h | Pipeline RAG complet, LangChain |
| 12 | RAG sur bases SQL | 1h30 | Text-to-SQL, PostgreSQL |

### Jour 3 : Production & Avancé
| # | Module | Durée | Contenu |
|:--|:-------|:------|:--------|
| 13 | Multi-agents | 1h30 | CrewAI, collaboration inter-agents |
| 14 | Vibe Coding | 1h | Cursor, Continue, AI-assisted dev |
| 15 | Introduction au Fine-tuning | 1h | RAG vs Fine-tuning |
| 16 | Pratique Fine-tuning | 2h | LoRA, Unsloth, PEFT |

### Modules avancés (depuis NLP)
| Module | Contenu |
|:-------|:--------|
| [Choisir le bon modèle LLM](cours/modules-avances/Choisir-Modele-LLM/) | Panorama, benchmarks, notebooks comparatifs |
| [Introduction aux LLM (théorie)](cours/modules-avances/Introduction-LLM/) | Architecture, tokenisation, théorie approfondie |
| [Prompt Engineering avancé](cours/modules-avances/Prompt-Engineering-Avance/) | Techniques avancées, raisonnement, évaluation |

## 🛠️ Technologies utilisées

**LangChain** | **Ollama** | **ChromaDB** | **FastAPI** | **CrewAI** | **Gradio** | **Hugging Face** | **Unsloth**

## 📁 Structure du module

```
LLM/
├── cours/                    # Modules 01-16 (.mdx)
│   └── modules-avances/      # Modules théoriques approfondis
├── exemples/                 # Scripts Python par module
├── projets/
│   ├── correction/           # Exemples corrigés
│   └── fastapi-project/      # Template FastAPI production
├── images/                   # Diagrammes et schémas
└── requirements.txt
```

## 🚀 Par où commencer ?

Suivez les modules dans l'ordre (Jour 1 → 2 → 3). Chaque module s'appuie sur le précédent.

---
[🏠 Retour à l'accueil](../../README.md)
