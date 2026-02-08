# -*- coding: utf-8 -*-

import glob
import json
import os

import chromadb
import requests
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader

os.environ["CHROMA_ENABLE_TELEMETRY"] = "false"

# --- 1. Configuration ---
DOCUMENTS_FOLDER = "documents"
COLLECTION_NAME = "pizza_allergen_collection"
EMBEDDING_MODEL = "mxbai-embed-large"
LLM_MODEL = "llama3.2:latest"
CHROMA_DB_PATH = "./chroma_db_pizza"

# --- 2. Chargement et découpage des documents PDF ---


def load_and_chunk_pdf(file_path, chunk_size=1000, chunk_overlap=200):
    """Charge un fichier PDF et le découpe en chunks"""
    print(f"Chargement du fichier : {file_path}")
    reader = PdfReader(file_path)
    text = "".join(page.extract_text() for page in reader.pages)
    print(f"Le document contient {len(text)} caractères.")

    print("Découpage du texte en chunks...")
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunks.append(text[i : i + chunk_size])
    print(f"{len(chunks)} chunks ont été créés.")
    return chunks


def load_all_pdfs_from_folder(folder_path):
    """Charge tous les PDFs d'un dossier"""
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    all_chunks = []
    all_ids = []

    for pdf_file in pdf_files:
        chunks = load_and_chunk_pdf(pdf_file)
        filename = os.path.basename(pdf_file)

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{filename}_chunk_{i}")

    return all_chunks, all_ids


# --- 3. Initialisation de ChromaDB ---
print("Initialisation de ChromaDB...")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

print("Initialisation de la fonction d'embedding via Ollama...")
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name=EMBEDDING_MODEL,
)

# --- 4. Création de la collection et stockage des données ---
print(f"Création ou chargement de la collection : {COLLECTION_NAME}")
collection = client.get_or_create_collection(
    name=COLLECTION_NAME, embedding_function=ollama_ef
)

# Vérifier si la collection est vide
if collection.count() == 0:
    print("Collection vide. Chargement des documents PDF...")
    pdf_chunks, chunk_ids = load_all_pdfs_from_folder(DOCUMENTS_FOLDER)

    if pdf_chunks:
        print("Stockage des chunks dans ChromaDB...")
        collection.add(documents=pdf_chunks, ids=chunk_ids)
        print(
            f"--- Base de données vectorielle créée avec {len(pdf_chunks)} chunks ! ---"
        )
    else:
        print("Aucun fichier PDF trouvé dans le dossier documents/")
else:
    print(f"Collection existante chargée avec {collection.count()} documents")

# --- 5. Fonction de recherche et génération ---


def chatbot_pizza_allergens(question):
    """Chatbot simple pour les allergènes de pizza"""

    # Recherche dans la base vectorielle
    results = collection.query(query_texts=[question], n_results=3)

    # Construction du contexte
    context = "\n".join(results["documents"][0])

    # Prompt pour le LLM
    prompt = f"""Tu es un assistant spécialisé dans les allergènes des pizzas. répond uniquement à l'aide des documents
Réponds à la question en utilisant uniquement le contexte fourni.

Contexte:
{context}

Question: {question}

Réponds de façon claire et précise. Si tu n'es pas sûr, dis-le.
IMPORTANT: Recommande toujours de vérifier avec le restaurant en cas d'allergie grave.
"""

    data = {
        "model": LLM_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Tu es un assistant spécialisé dans la pizza...,Toutes les pizzas contiennent une pate fait a base de gluten. tu peux parler uniquement de pizza, d'ingrédients de pizza et d'allergènes liés à la pizza. Si on te pose une question qui ne concerne pas ces sujets, réponds poliment que tu ne peux que discuter de pizza, d'ingrédients et d'allergènes. ",
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "temperature": 0.1,
    }

    try:
        response = requests.post("http://localhost:11434/api/chat", json=data)
        if response.status_code == 200:
            return json.loads(response.text)["message"]["content"]
        else:
            return f"Erreur: {response.text}"
    except Exception as e:
        return f"Erreur de connexion: {e}"


def main():
    """Interface simple du chatbot"""
    print("\n" + "=" * 50)
    print("CHATBOT ALLERGÈNES PIZZA")
    print("=" * 50)
    print("Tapez 'exit' pour quitter.\n")

    while True:
        try:
            question = input("Vous: ")

            if question.lower() in ["exit", "quit", "sortir"]:
                print("Au revoir !")
                break

            if not question.strip():
                continue

            print("Assistant: ", end="")
            response = chatbot_pizza_allergens(question)
            print(response)
            print("-" * 30)

        except KeyboardInterrupt:
            print("\nAu revoir !")
            break
        except Exception as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    main()
