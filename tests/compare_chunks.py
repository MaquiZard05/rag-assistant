"""Compare la qualite du retrieval pour differentes tailles de chunks."""

import sys
import time
from pathlib import Path

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from config import EMBEDDING_MODEL, DOCS_DIR

# Questions de test representatives
TEST_QUESTIONS = [
    "Quelles sont les regles de securite sur un chantier ?",
    "Comment se passe le processus de recrutement ?",
    "Quels sont les tarifs des services proposes ?",
    "Quelle est la procedure de suivi d'execution d'un chantier ?",
    "Comment fonctionne la periode d'essai ?",
]

# Configurations a tester
CHUNK_CONFIGS = [
    {"size": 500, "overlap": 100},
    {"size": 1000, "overlap": 200},
    {"size": 1500, "overlap": 300},
]


def load_all_pdfs():
    """Charge tous les PDFs du dossier docs."""
    documents = []
    for pdf_path in sorted(DOCS_DIR.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_path))
        documents.extend(loader.load())
    return documents


def test_config(documents, embeddings, config, questions):
    """Teste une configuration de chunks et retourne les scores moyens."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["size"],
        chunk_overlap=config["overlap"],
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    # Creer un vectorstore temporaire en memoire
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=f"test_{config['size']}",
    )

    results = []
    for question in questions:
        docs_with_scores = vectorstore.similarity_search_with_score(question, k=5)
        # Score moyen des top 5 (plus bas = plus pertinent pour ChromaDB)
        avg_score = sum(score for _, score in docs_with_scores) / len(docs_with_scores)
        best_score = docs_with_scores[0][1] if docs_with_scores else float("inf")
        results.append({"question": question, "avg_score": avg_score, "best_score": best_score})

    # Nettoyer
    vectorstore.delete_collection()

    return {"num_chunks": len(chunks), "results": results}


def main():
    print("=== Comparaison des tailles de chunks ===\n")

    # Charger les documents
    print("Chargement des PDFs...")
    documents = load_all_pdfs()
    print(f"  -> {len(documents)} pages chargees\n")

    # Charger le modele d'embeddings une seule fois
    print("Chargement du modele d'embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    print()

    # Tester chaque configuration
    all_results = {}
    for config in CHUNK_CONFIGS:
        label = f"{config['size']}/{config['overlap']}"
        print(f"Test chunk_size={config['size']}, overlap={config['overlap']}...")
        start = time.time()
        result = test_config(documents, embeddings, config, TEST_QUESTIONS)
        elapsed = time.time() - start
        all_results[label] = result
        print(f"  -> {result['num_chunks']} chunks, {elapsed:.1f}s\n")

    # Afficher le tableau recapitulatif
    print("=" * 80)
    print(f"{'Config':<12} {'Chunks':<8} {'Score moyen':<14} {'Meilleur score':<16}")
    print("-" * 80)

    for label, result in all_results.items():
        avg_all = sum(r["avg_score"] for r in result["results"]) / len(result["results"])
        best_all = sum(r["best_score"] for r in result["results"]) / len(result["results"])
        print(f"{label:<12} {result['num_chunks']:<8} {avg_all:<14.4f} {best_all:<16.4f}")

    print("=" * 80)
    print("\n(Scores plus bas = meilleure pertinence avec ChromaDB)")

    # Detail par question
    print("\n--- Detail par question ---\n")
    for i, question in enumerate(TEST_QUESTIONS):
        print(f"Q: {question}")
        for label, result in all_results.items():
            r = result["results"][i]
            print(f"  {label}: avg={r['avg_score']:.4f}, best={r['best_score']:.4f}")
        print()


if __name__ == "__main__":
    main()
