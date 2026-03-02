"""Point d'entree Streamlit — charge le CSS, auto-ingest si besoin, page d'accueil."""

import sys
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

st.set_page_config(
    page_title="Assistant Documentaire IA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    css_path = Path(__file__).resolve().parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")

# Auto-ingest des docs de demo si la base est vide (utile sur Streamlit Cloud)
from config import CHROMA_DIR, DOCS_DIR

if not CHROMA_DIR.exists() or not any(CHROMA_DIR.iterdir()):
    docs = list(DOCS_DIR.glob("*.pdf"))
    if docs:
        with st.spinner("Premiere visite — indexation des documents de demo..."):
            from ingest import ingest_single_pdf, get_embeddings
            from langchain_community.vectorstores import Chroma
            from langchain_community.document_loaders import PyPDFLoader
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, DEFAULT_COLLECTION

            # Ingestion groupee (plus rapide que un par un)
            all_documents = []
            for pdf_path in sorted(docs):
                loader = PyPDFLoader(str(pdf_path))
                all_documents.extend(loader.load())

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            chunks = splitter.split_documents(all_documents)

            # Ajouter headers contextuels
            from ingest import add_contextual_headers
            chunks = add_contextual_headers(chunks)

            embeddings = get_embeddings()
            CHROMA_DIR.mkdir(parents=True, exist_ok=True)
            Chroma.from_documents(
                documents=chunks, embedding=embeddings,
                persist_directory=str(CHROMA_DIR),
                collection_name=DEFAULT_COLLECTION,
            )
            st.success(f"{len(docs)} documents indexes ({len(chunks)} chunks)")

st.markdown("""
<div class="app-header">
    <h1>📄 Assistant Documentaire IA</h1>
    <p>Posez vos questions, obtenez des reponses sourcees depuis vos documents.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("Utilisez le menu de navigation pour acceder aux pages :")
st.markdown("- **💬 Chat** — Posez vos questions sur vos documents")
st.markdown("- **⚙️ Admin** — Gerez vos clients, documents et parametres")
