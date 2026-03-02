"""Script de query RAG : recherche les chunks pertinents + genere une reponse sourcee."""

import sys
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

from config import (
    GROQ_API_KEY, EMBEDDING_MODEL, LLM_MODEL,
    CHROMA_DIR, TOP_K,
)

SYSTEM_PROMPT = (
    "Tu es un assistant qui repond aux questions en te basant UNIQUEMENT "
    "sur le contexte fourni ci-dessous. "
    "Si l'information n'est pas dans le contexte, dis-le clairement. "
    "Cite toujours tes sources (nom du fichier et numero de page)."
    "\n\nContexte :\n{context}"
)


def load_vectorstore():
    """Charge la base vectorielle ChromaDB existante."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name="rag_docs",
    )


def retrieve(vectorstore, question: str) -> list:
    """Recherche les chunks les plus pertinents."""
    return vectorstore.similarity_search_with_score(question, k=TOP_K)


def build_context(chunks: list) -> str:
    """Construit le contexte textuel a partir des chunks recuperes."""
    parts = []
    for i, (doc, _score) in enumerate(chunks, 1):
        source = Path(doc.metadata.get("source", "inconnu")).name
        page = doc.metadata.get("page", 0) + 1
        parts.append(f"[Source {i}: {source}, page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def generate_answer(question: str, context: str) -> str:
    """Envoie la question + contexte au LLM via Groq."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.3,
    )

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})
    return response.content


def display_sources(chunks: list):
    """Affiche les sources utilisees (dedupliquees)."""
    print("\n--- Sources ---")
    seen = set()
    for doc, score in chunks:
        source = Path(doc.metadata.get("source", "inconnu")).name
        page = doc.metadata.get("page", 0) + 1
        key = (source, page)
        if key not in seen:
            seen.add(key)
            print(f"  - {source}, page {page} (score: {score:.3f})")


def ask(question: str, top_k: int = TOP_K) -> dict:
    """Pose une question au RAG. Retourne reponse, sources et scores.

    Fonction principale pour l'integration Streamlit.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY manquante dans le .env")

    if not CHROMA_DIR.exists():
        raise FileNotFoundError("Base ChromaDB introuvable. Lance d'abord : python src/ingest.py")

    vectorstore = load_vectorstore()
    chunks = vectorstore.similarity_search_with_score(question, k=top_k)

    if not chunks:
        return {"answer": "Aucun resultat trouve dans les documents.", "sources": [], "num_sources": 0}

    context = build_context(chunks)
    answer = generate_answer(question, context)

    # Extraire les sources dedupliquees
    sources = []
    seen = set()
    for doc, score in chunks:
        source = Path(doc.metadata.get("source", "inconnu")).name
        page = doc.metadata.get("page", 0) + 1
        key = (source, page)
        if key not in seen:
            seen.add(key)
            sources.append({"file": source, "page": page, "score": score})

    return {"answer": answer, "sources": sources, "num_sources": len(sources)}


def main():
    if not GROQ_API_KEY:
        print("Erreur : GROQ_API_KEY manquante dans le .env")
        sys.exit(1)

    if not CHROMA_DIR.exists():
        print("Erreur : base ChromaDB introuvable. Lance d'abord :\n  python src/ingest.py")
        sys.exit(1)

    # Charger la base
    vectorstore = load_vectorstore()

    # Recuperer la question (argument CLI ou input interactif)
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("\nPose ta question : ")

    if not question.strip():
        print("Erreur : question vide.")
        sys.exit(1)

    print(f"\nQuestion : {question}\n")

    # Recherche
    print("Recherche dans les documents...")
    chunks = retrieve(vectorstore, question)

    if not chunks:
        print("Aucun resultat trouve.")
        sys.exit(0)

    # Generation
    print("Generation de la reponse...\n")
    context = build_context(chunks)
    answer = generate_answer(question, context)

    # Affichage
    print("=== Reponse ===\n")
    print(answer)
    display_sources(chunks)


if __name__ == "__main__":
    main()
