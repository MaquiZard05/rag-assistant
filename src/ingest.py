"""Script d'ingestion : charge les documents (PDF, TXT, DOCX, HTML), decoupe en chunks, stocke dans ChromaDB."""

import sys
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    BSHTMLLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import (
    EMBEDDING_MODEL, DOCS_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP,
    DEFAULT_COLLECTION,
)

# Formats supportes : extension -> loader class
SUPPORTED_FORMATS = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".docx": Docx2txtLoader,
    ".html": BSHTMLLoader,
    ".htm": BSHTMLLoader,
}


_embeddings_cache = None


def get_embeddings():
    """Retourne le modele d'embeddings (charge une seule fois, garde en memoire)."""
    global _embeddings_cache
    if _embeddings_cache is None:
        _embeddings_cache = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings_cache


def _get_loader(file_path: Path):
    """Retourne le loader adapte au format du fichier."""
    ext = file_path.suffix.lower()
    loader_class = SUPPORTED_FORMATS.get(ext)
    if not loader_class:
        raise ValueError(
            f"Format non supporte : {ext}. "
            f"Formats acceptes : {', '.join(SUPPORTED_FORMATS.keys())}"
        )
    if ext == ".txt":
        return loader_class(str(file_path), encoding="utf-8")
    return loader_class(str(file_path))


def load_documents(docs_dir: Path) -> list:
    """Charge tous les documents supportes du dossier (PDF, TXT, DOCX, HTML)."""
    documents = []
    all_files = sorted(
        f for f in docs_dir.iterdir()
        if f.suffix.lower() in SUPPORTED_FORMATS
    )

    if not all_files:
        print(f"Aucun document trouve dans {docs_dir}")
        sys.exit(1)

    for file_path in all_files:
        print(f"  - {file_path.name}")
        loader = _get_loader(file_path)
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
    """Ajoute un header contextuel a chaque chunk (source + page si dispo).

    Le header est encode dans le vecteur, ce qui ameliore la pertinence
    de la recherche semantique.
    """
    for chunk in chunks:
        source = Path(chunk.metadata.get("source", "inconnu")).name
        page = chunk.metadata.get("page")
        if page is not None:
            header = f"[Source: {source} | Page {page + 1}]\n\n"
        else:
            header = f"[Source: {source}]\n\n"
        chunk.page_content = header + chunk.page_content
    return chunks


def ingest_single_file(file_path: Path, collection_name: str = DEFAULT_COLLECTION,
                       original_name: str = None) -> int:
    """Ingere un document (PDF, TXT, DOCX, HTML) dans ChromaDB.

    Retourne le nombre de chunks ajoutes.
    collection_name : collection ChromaDB (= client)
    original_name : nom original du fichier (pour les uploads Streamlit)
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Format non supporte : {ext}. "
            f"Formats acceptes : {', '.join(SUPPORTED_FORMATS.keys())}"
        )

    # Charger le document avec le bon loader
    try:
        loader = _get_loader(file_path)
        documents = loader.load()
    except Exception as e:
        raise ValueError(f"Impossible de lire '{file_path.name}' : {e}")

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
    """Retourne la liste des fichiers indexes (acces direct ChromaDB, sans embeddings)."""
    if not CHROMA_DIR.exists():
        return []

    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection(collection_name)
        results = collection.get(include=["metadatas"])

        if not results or not results.get("metadatas"):
            return []

        files = set()
        for meta in results["metadatas"]:
            source = meta.get("source", "")
            if source:
                files.add(Path(source).name)

        return sorted(files)
    except Exception:
        return []


def ingest_single_pdf(pdf_path: Path, collection_name: str = DEFAULT_COLLECTION,
                      original_name: str = None) -> int:
    """Alias de compatibilite — redirige vers ingest_single_file."""
    return ingest_single_file(pdf_path, collection_name, original_name)


def main():
    """Ingestion CLI des documents du dossier docs/ dans la collection par defaut."""
    print("=== Ingestion des documents ===\n")

    print(f"1. Chargement des documents depuis {DOCS_DIR}/")
    documents = load_documents(DOCS_DIR)
    print(f"   -> {len(documents)} pages/sections chargees\n")

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
