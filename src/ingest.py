"""Script d'ingestion : charge les PDFs, découpe en chunks, stocke dans ChromaDB."""

import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import (
    EMBEDDING_MODEL, DOCS_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP,
    DEFAULT_COLLECTION,
)


def get_embeddings():
    """Retourne le modele d'embeddings."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_pdfs(docs_dir: Path) -> list:
    """Charge tous les PDFs du dossier."""
    documents = []
    pdf_files = sorted(docs_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"Aucun PDF trouve dans {docs_dir}")
        sys.exit(1)

    for pdf_path in pdf_files:
        print(f"  - {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        documents.extend(docs)

    return documents


def split_documents(documents: list) -> list:
    """Decoupe les documents en chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def add_contextual_headers(chunks: list) -> list:
    """Ajoute un header contextuel a chaque chunk (source + page).

    Le header est encode dans le vecteur, ce qui ameliore la pertinence
    de la recherche semantique.
    """
    for chunk in chunks:
        source = Path(chunk.metadata.get("source", "inconnu")).name
        page = chunk.metadata.get("page", 0) + 1
        header = f"[Source: {source} | Page {page}]\n\n"
        chunk.page_content = header + chunk.page_content
    return chunks


def ingest_single_pdf(pdf_path: Path, collection_name: str = DEFAULT_COLLECTION,
                      original_name: str = None) -> int:
    """Ingere un seul PDF dans ChromaDB. Retourne le nombre de chunks ajoutes.

    collection_name : collection ChromaDB (= client)
    original_name : nom original du fichier (pour les uploads Streamlit)
    """
    # Verifier que le fichier existe et est un PDF
    if not pdf_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Le fichier n'est pas un PDF : {pdf_path.name}")

    # Charger le PDF
    try:
        loader = PyPDFLoader(str(pdf_path))
        documents = loader.load()
    except Exception as e:
        raise ValueError(f"Impossible de lire le PDF '{pdf_path.name}' : {e}")

    # Remplacer le chemin temporaire par le vrai nom de fichier
    if original_name:
        for doc in documents:
            doc.metadata["source"] = original_name

    # Decouper en chunks + ajouter les headers contextuels
    chunks = split_documents(documents)
    chunks = add_contextual_headers(chunks)

    if not chunks:
        return 0

    # Ajouter a la collection du client
    embeddings = get_embeddings()
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=collection_name,
    )
    vectorstore.add_documents(chunks)

    return len(chunks)


def get_indexed_files(collection_name: str = DEFAULT_COLLECTION) -> list[str]:
    """Retourne la liste des fichiers indexes dans une collection."""
    if not CHROMA_DIR.exists():
        return []

    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    collection = vectorstore.get()
    if not collection or not collection.get("metadatas"):
        return []

    files = set()
    for meta in collection["metadatas"]:
        source = meta.get("source", "")
        if source:
            files.add(Path(source).name)

    return sorted(files)


def main():
    """Ingestion CLI des PDFs du dossier docs/ dans la collection par defaut."""
    print("=== Ingestion des documents ===\n")

    print(f"1. Chargement des PDFs depuis {DOCS_DIR}/")
    documents = load_pdfs(DOCS_DIR)
    print(f"   -> {len(documents)} pages chargees\n")

    print("2. Decoupage en chunks")
    chunks = split_documents(documents)
    chunks = add_contextual_headers(chunks)
    print(f"   -> {len(chunks)} chunks crees\n")

    print("3. Generation des embeddings et stockage dans ChromaDB...")
    embeddings = get_embeddings()
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=DEFAULT_COLLECTION,
    )
    print(f"   -> Base vectorielle sauvegardee dans {CHROMA_DIR}\n")

    print("=== Ingestion terminee ===")


if __name__ == "__main__":
    main()
