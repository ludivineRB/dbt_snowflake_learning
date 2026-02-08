---
title: 09_interrogation_rag
tags:
  - LLM
  - 10-Large-Language-Model
category: 10-Large-Language-Model
---
# Jour 2 - Module 9 : Interroger sa Base de Connaissances avec RAG

Nous avons une base de connaissances vectorielle prête à l'emploi. Il est maintenant temps de l'utiliser pour ce pour quoi elle a été conçue : trouver des informations pertinentes et les fournir à notre LLM afin qu'il puisse répondre à nos questions de manière factuelle.

C'est ici que la magie du RAG opère. Nous allons mettre en œuvre la deuxième phase majeure de notre système : l'**interrogation**.

## 1. Le Processus d'Interrogation RAG

Le script que nous allons construire va orchestrer le flux de travail complet du RAG à chaque fois que l'utilisateur pose une question. Ce processus se déroule en trois étapes clés, qui sont la mise en application de la théorie vue précédemment.

![Diagramme simple expliquant le processus RAG en 3 étapes : Recherche, Augmentation, Génération](images/rag.png)

1.  **Étape de Recherche (Retrieval)** : Nous utilisons la question de l'utilisateur pour interroger la base ChromaDB.
    * ChromaDB transforme la question en vecteur (en utilisant le même modèle d'embedding que celui utilisé pour les documents).
    * Il compare ce vecteur à tous les vecteurs de *chunks* stockés.
    * Il retourne les *chunks* les plus similaires, c'est-à-dire le contexte le plus pertinent.

2.  **Étape d'Augmentation (Augmented)** : Nous construisons dynamiquement un nouveau prompt pour le LLM. Ce prompt est un assemblage de plusieurs éléments :
    * Une **instruction** claire pour le LLM (un "system prompt").
    * Le **contexte** retrouvé à l'étape précédente.
    * La **question originale** de l'utilisateur.

3.  **Étape de Génération (Generation)** : Ce prompt "augmenté" est envoyé au LLM (via l'API d'Ollama), qui génère la réponse finale en se basant sur le contexte fourni.

---

## 2. Implémentation Manuelle avec ChromaDB et Ollama

Cette première approche permet de bien comprendre chaque rouage du mécanisme RAG. Nous allons tout coder explicitement.

**Lien vers le fichier de code complet :** [`09_rag_complet.py`](./09_rag_complet.py)

### Étape 1 : Recherche (Retrieval)

Tout commence par la fonction `rag` qui prend la question de l'utilisateur. La première action est d'interroger la collection ChromaDB pour trouver les documents les plus pertinents.

```python
# Fichier : 09_rag_complet.py

def rag(question):
    """
    Exécute le processus RAG complet : recherche, augmentation, génération.
    """
    # 1. ÉTAPE DE RECHERCHE (Retrieval)
    # Interroge la collection ChromaDB pour trouver les 3 chunks les plus pertinents.
    # n_results=3 : on demande les 3 résultats les plus proches.
    print("   -> 1. Recherche des documents pertinents...")
    results = collection.query(query_texts=[question], n_results=3)

    # Récupère le contenu des documents (chunks) trouvés.
    context = "\n".join(results["documents"][0])
```

### Étape 2 : Augmentation (Augmented)

Avec le contexte en main, nous utilisons un template pour formater un prompt clair et précis. C'est une étape cruciale pour guider le LLM et réduire les risques d'hallucination.

💡 **Bonne pratique : Le Prompt Template**
Isoler le prompt dans un template rend le code plus lisible et facilite grandement les expérimentations. Changer le prompt est l'une des manières les plus efficaces d'améliorer les performances de votre RAG.

```python
# Fichier : 09_rag_complet.py (suite)

    # 2. ÉTAPE D'AUGMENTATION (Augmented)
    # Crée le template du prompt. L'instruction "En te basant uniquement sur le contexte suivant"
    # est essentielle pour forcer le modèle à utiliser les documents fournis.
    print("   -> 2. Augmentation du prompt...")
    prompt_template = (
        "En te basant uniquement sur le contexte suivant, réponds à la question.\n\n"
        "--- Contexte ---\n"
        "{context}"
        "--- Fin du Contexte ---\n\n"
        "Question: {question}"
    )
    # Remplit le template avec le contexte et la question.
    prompt = prompt_template.format(context=context, question=question)
```

### Étape 3 : Génération (Generation)

Le prompt final est envoyé à l'API de chat d'Ollama. Nous récupérons la réponse et la retournons à l'utilisateur.

```python
# Fichier : 09_rag_complet.py (suite)

    # 3. ÉTAPE DE GÉNÉRATION (Generation)
    # Prépare les données pour l'API de chat d'Ollama.
    print("   -> 3. Génération de la réponse par le LLM...")
    data = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    # Envoie la requête au LLM.
    response = requests.post("http://localhost:11434/api/chat", json=data)

    # Retourne la réponse du LLM.
    if response.status_code == 200:
        return json.loads(response.text)["message"]["content"]
    else:
        return f"Erreur lors de la génération : {response.text}"
```

Lancez ce script (`09_rag_complet.py`) et posez des questions sur le document que vous avez ingéré (par exemple sur les "conventional commits" si vous avez utilisé le PDF fourni). Vous verrez le processus se dérouler en direct.

## 3. Implémentation avec LangChain : Une Approche Modulaire

LangChain est un framework puissant qui simplifie le développement d'applications basées sur les LLMs. Il offre des abstractions pour chaîner les composants de manière plus propre et réutilisable.

### Pourquoi utiliser LangChain ?

*   **Modularité** : Chaque étape (retriever, prompt, modèle) est un objet distinct, facile à remplacer.
*   **Intégrations** : Connexion simplifiée à des centaines de bases de données, LLMs et outils.
*   **Lisibilité** : Le LangChain Expression Language (LCEL) permet de définir des chaînes complexes avec une syntaxe `|` (pipe) très intuitive.

**Lien vers le fichier de code :** `code/module6_rag_langchain.py` (nommé dans le document de référence).

### Comment ça fonctionne avec LangChain ?

Le code est plus concis car LangChain gère une grande partie de la complexité.

1.  **Initialisation des composants** : On crée des objets pour le LLM, les embeddings et le retriever (notre base ChromaDB).
2.  **Définition du Prompt** : On utilise `ChatPromptTemplate` pour une gestion structurée du prompt.
3.  **Création de la Chaîne (Chain)** : On utilise l'opérateur `|` pour assembler la chaîne. La lisibilité est immédiate : le contexte du retriever est "pipé" dans le prompt, qui est ensuite "pipé" dans le modèle, dont la sortie est finalement parsée.

```python
# Extrait conceptuel du code LangChain

# 1. Transformer la base de données en un "Retriever"
retriever = db.as_retriever()

# 2. Définir le template de prompt
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 3. Définir le modèle
model = ChatOllama(model="llama3.2:latest")

# 4. Créer la chaîne RAG avec LCEL (le | est un "pipe")
chain = (
    RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    )
    | prompt
    | model
    | StrOutputParser()
)

# 5. Invoquer la chaîne
response = chain.invoke("What are conventional commits?")
```

Cette approche est non seulement plus élégante mais aussi beaucoup plus facile à maintenir et à faire évoluer.

Félicitations ! Vous avez construit et utilisé un système RAG complet de deux manières différentes. C'est une compétence extrêmement précieuse qui vous permet de créer des applications d'IA capables de raisonner sur des données privées et vérifiables.
