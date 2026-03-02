"""Script de query RAG : recherche hybride + reranking + generation sourcee."""

import sys
from pathlib import Path

from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

from config import (
    GROQ_API_KEY, EMBEDDING_MODEL, LLM_MODEL, RERANK_MODEL,
    CHROMA_DIR, TOP_K, DEFAULT_COLLECTION, DEFAULT_SYSTEM_PROMPT,
)


# Charger le reranker une seule fois (evite de le recharger a chaque question)
_reranker = None


def get_reranker():
    """Charge le modele de reranking (cross-encoder) une seule fois."""
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANK_MODEL)
    return _reranker


def load_vectorstore(collection_name: str = DEFAULT_COLLECTION):
    """Charge la base vectorielle ChromaDB pour un client."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=collection_name,
    )


def contextualize_query(question: str, history: list, llm) -> str:
    """Reformule la question en incluant le contexte de l'historique.

    Permet au retrieval de trouver les bons chunks meme quand l'utilisateur
    fait reference a un echange precedent ("Et pour le premium ?").
    """
    if not history:
        return question

    # Prendre les 3 derniers echanges max
    recent = history[-6:]  # 6 messages = 3 paires user/assistant
    history_text = ""
    for msg in recent:
        role = "Utilisateur" if msg["role"] == "user" else "Assistant"
        # Tronquer les reponses longues
        content = msg["content"][:200]
        history_text += f"{role}: {content}\n"

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Reformule la question suivante pour qu'elle soit autonome "
         "(comprehensible sans l'historique). "
         "Reponds UNIQUEMENT avec la question reformulee, rien d'autre."),
        ("human",
         "Historique:\n{history}\n\n"
         "Nouvelle question: {question}\n\n"
         "Question reformulee:"),
    ])

    chain = prompt | llm
    response = chain.invoke({"history": history_text, "question": question})
    return response.content.strip()


def hybrid_search(vectorstore, question: str, top_k: int = TOP_K) -> list:
    """Recherche hybride : combine vectorielle (sens) + BM25 (mots-cles)."""
    # 1. Recherche vectorielle
    vector_results = vectorstore.similarity_search_with_score(question, k=top_k * 2)

    # 2. Recherche BM25
    collection = vectorstore.get()
    if not collection or not collection.get("documents"):
        return vector_results[:top_k]

    all_docs = []
    for i, text in enumerate(collection["documents"]):
        meta = collection["metadatas"][i] if collection.get("metadatas") else {}
        all_docs.append(Document(page_content=text, metadata=meta))

    bm25_retriever = BM25Retriever.from_documents(all_docs, k=top_k * 2)
    bm25_results = bm25_retriever.invoke(question)

    # 3. Fusion RRF (Reciprocal Rank Fusion)
    doc_scores = {}
    k_rrf = 60

    for rank, (doc, _score) in enumerate(vector_results):
        key = doc.page_content[:100]
        doc_scores[key] = {"doc": doc, "score": 1.0 / (k_rrf + rank + 1), "original_score": _score}

    for rank, doc in enumerate(bm25_results):
        key = doc.page_content[:100]
        rrf_score = 1.0 / (k_rrf + rank + 1)
        if key in doc_scores:
            doc_scores[key]["score"] += rrf_score
        else:
            doc_scores[key] = {"doc": doc, "score": rrf_score, "original_score": 1.0}

    sorted_results = sorted(doc_scores.values(), key=lambda x: x["score"], reverse=True)
    return [(r["doc"], r["original_score"]) for r in sorted_results[:top_k * 2]]


def rerank(question: str, chunks: list, top_k: int = TOP_K) -> list:
    """Re-score les chunks avec un cross-encoder pour affiner la pertinence."""
    if not chunks:
        return []

    reranker = get_reranker()
    pairs = [[question, doc.page_content] for doc, _score in chunks]
    scores = reranker.predict(pairs)

    # Combiner les chunks avec leurs nouveaux scores
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    return [(doc, float(rerank_score)) for (doc, _orig_score), rerank_score in ranked[:top_k]]


def build_context(chunks: list) -> str:
    """Construit le contexte textuel a partir des chunks recuperes."""
    parts = []
    for i, (doc, _score) in enumerate(chunks, 1):
        source = Path(doc.metadata.get("source", "inconnu")).name
        page = doc.metadata.get("page", 0) + 1
        parts.append(f"[Source {i}: {source}, page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def generate_answer(question: str, context: str, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """Envoie la question + contexte au LLM via Groq."""
    full_prompt = system_prompt + "\n\nContexte :\n{context}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", full_prompt),
        ("human", "{question}"),
    ])

    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.3,
        timeout=30,
    )

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})
    return response.content


def ask(question: str, top_k: int = TOP_K, collection_name: str = DEFAULT_COLLECTION,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT, history: list = None) -> dict:
    """Pose une question au RAG. Pipeline complet :
    1. Reformulation avec historique
    2. Recherche hybride (vectorielle + BM25)
    3. Reranking cross-encoder
    4. Generation LLM sourcee
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY manquante dans le .env")

    if not CHROMA_DIR.exists():
        raise FileNotFoundError("Base ChromaDB introuvable. Lance d'abord : python src/ingest.py")

    # Reformuler la question si historique present
    search_question = question
    if history:
        try:
            llm = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0)
            search_question = contextualize_query(question, history, llm)
        except Exception:
            search_question = question  # Fallback sur la question brute

    vectorstore = load_vectorstore(collection_name)

    # Recherche hybride (top_k * 2 candidats)
    chunks = hybrid_search(vectorstore, search_question, top_k=top_k)

    if not chunks:
        return {"answer": "Aucun resultat trouve dans les documents.", "sources": [], "num_sources": 0}

    # Reranking (affine au top_k final)
    chunks = rerank(search_question, chunks, top_k=top_k)

    context = build_context(chunks)
    answer = generate_answer(question, context, system_prompt=system_prompt)

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


def main():
    if not GROQ_API_KEY:
        print("Erreur : GROQ_API_KEY manquante dans le .env")
        sys.exit(1)

    if not CHROMA_DIR.exists():
        print("Erreur : base ChromaDB introuvable. Lance d'abord :\n  python src/ingest.py")
        sys.exit(1)

    vectorstore = load_vectorstore()

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("\nPose ta question : ")

    if not question.strip():
        print("Erreur : question vide.")
        sys.exit(1)

    print(f"\nQuestion : {question}\n")

    result = ask(question)
    print("=== Reponse ===\n")
    print(result["answer"])
    print(f"\n({result['num_sources']} source(s))")


if __name__ == "__main__":
    main()
