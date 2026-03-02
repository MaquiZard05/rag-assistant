"""Script d'ingestion : charge les PDFs, découpe en chunks, stocke dans ChromaDB."""

import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import (
    EMBEDDING_MODEL, DOCS_DIR, CHROMA_DIR, CHUNK_SIZE, CHUNK_OVERLAP,
)


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


def create_vectorstore(chunks: list):
    """Genere les embeddings et stocke dans ChromaDB."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="rag_docs",
    )
    return vectorstore


def main():
    print("=== Ingestion des documents ===\n")

    # 1. Charger les PDFs
    print(f"1. Chargement des PDFs depuis {DOCS_DIR}/")
    documents = load_pdfs(DOCS_DIR)
    print(f"   -> {len(documents)} pages chargees\n")

    # 2. Decouper en chunks
    print("2. Decoupage en chunks")
    chunks = split_documents(documents)
    print(f"   -> {len(chunks)} chunks crees\n")

    # 3. Embeddings + stockage
    print("3. Generation des embeddings et stockage dans ChromaDB...")
    create_vectorstore(chunks)
    print(f"   -> Base vectorielle sauvegardee dans {CHROMA_DIR}\n")

    print("=== Ingestion terminee ===")


if __name__ == "__main__":
    main()
