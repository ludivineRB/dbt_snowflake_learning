---
title: 10_rag_avec_bases_de_donnees_sql
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Jour X - Module 10 : RAG avec Bases de Données SQL (Text-to-SQL)

Jusqu'à présent, nous avons utilisé le RAG pour interroger des documents non structurés (PDFs, textes). Mais que faire si nos connaissances sont stockées dans une base de données relationnelle comme PostgreSQL ? C'est là qu'intervient le concept de **SQL-RAG** ou **Text-to-SQL**.

## Qu'est-ce que le SQL-RAG ?

Le SQL-RAG permet à un LLM de répondre à des questions en langage naturel en les traduisant en requêtes SQL, en exécutant ces requêtes sur une base de données, puis en interprétant les résultats pour formuler une réponse.

Le processus se déroule comme suit :

1.  **Question en langage naturel :** L'utilisateur pose une question (ex: "Combien de produits coûtent plus de 100 euros ?").
2.  **Compréhension du schéma :** Le LLM a accès au schéma de la base de données (noms des tables, colonnes, types, relations).
3.  **Génération SQL :** Le LLM génère une requête SQL valide basée sur la question et le schéma.
4.  **Exécution SQL :** La requête SQL est exécutée sur la base de données (PostgreSQL dans notre cas).
5.  **Récupération des résultats :** Les données brutes sont extraites de la base.
6.  **Génération de réponse :** Le LLM interprète les résultats et formule une réponse en langage naturel pour l'utilisateur.

## Pourquoi utiliser le SQL-RAG ?

* **Accès aux données structurées :** Permet d'interroger des bases de données complexes sans avoir à écrire de SQL manuellement.
* **Mise à jour facile :** Les données sont toujours à jour dans la base de données.
* **Précision :** Les réponses sont basées sur des données factuelles extraites directement de la source.

## Implémentation avec LangChain

LangChain offre des outils puissants pour construire des agents capables d'interagir avec des bases de données SQL. L'agent SQL de LangChain est conçu pour comprendre le schéma de votre base de données, générer des requêtes SQL, les exécuter et interpréter les résultats.

**Lien vers le fichier de code :** [code/10_rag_postgres.py](./code/10_rag_postgres.py)

### Composants clés du script :

* **`SQLDatabase.from_uri()` :** Permet à LangChain de se connecter à votre base de données PostgreSQL en utilisant une chaîne de connexion standard.
* **`ChatOllama` :** Notre LLM local via Ollama, qui servira de "cerveau" à l'agent.
* **`create_sql_agent()` :** La fonction magique de LangChain qui assemble tous les composants. Elle crée un agent capable de raisonner sur les questions, de générer du SQL, d'exécuter et de répondre.
* **`SystemMessage` :** Un prompt système est utilisé pour guider le comportement de l'agent, en lui donnant des instructions sur la manière de générer le SQL et de formuler les réponses.

### Prérequis pour le script :

1.  **Base de données PostgreSQL :** Assurez-vous d'avoir une instance PostgreSQL en cours d'exécution et accessible.
2.  **Données de test :** Pour tester, vous pouvez créer une table simple et y insérer quelques données, comme suggéré dans les commentaires du script `10_rag_postgres.py`.
3.  **Librairies Python :** Installez les packages nécessaires :
    ```bash
    pip install langchain-community sqlalchemy psycopg2-binary
    ```
4.  **Modèle Ollama :** Assurez-vous d'avoir téléchargé le modèle LLM spécifié (`llama3.2:latest` par défaut) via `ollama pull <model_name>`.

## Comment ça fonctionne ?

L'agent SQL de LangChain utilise un processus itératif (un "cycle de pensée") :

1.  L'utilisateur pose une question.
2.  Le LLM analyse la question et le schéma de la base de données.
3.  Il décide d'une action : générer une requête SQL.
4.  La requête SQL est exécutée.
5.  Le LLM reçoit le résultat de la requête.
6.  Il utilise ce résultat pour formuler une réponse en langage naturel à l'utilisateur.

Le paramètre `verbose=True` dans `create_sql_agent` est très utile pour voir ce processus de pensée de l'agent en action, ce qui est excellent pour le débogage.

---

Le SQL-RAG ouvre des possibilités immenses pour interroger des données structurées avec la flexibilité du langage naturel. C'est une compétence clé pour construire des applications d'IA d'entreprise.

**[Retour à la Conclusion](./11_multi_agent_collaboration.md)**
