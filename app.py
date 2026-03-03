"""Point d'entree Streamlit — charge le CSS, auto-ingest si besoin, page d'accueil."""

import sys
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

st.set_page_config(
    page_title="Assistant Documentaire IA",
    page_icon="📄",
    layout="centered",
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
    from ingest import SUPPORTED_FORMATS, _get_loader, get_embeddings, add_contextual_headers
    docs = [f for f in DOCS_DIR.iterdir() if f.suffix.lower() in SUPPORTED_FORMATS]
    if docs:
        with st.spinner("Premiere visite — indexation des documents de demo..."):
            from langchain_community.vectorstores import Chroma
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            from config import CHUNK_SIZE, CHUNK_OVERLAP, DEFAULT_COLLECTION

            all_documents = []
            for doc_path in sorted(docs):
                loader = _get_loader(doc_path)
                all_documents.extend(loader.load())

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,
                separators=["\n\n", "\n", ". ", " ", ""],
            )
            chunks = splitter.split_documents(all_documents)
            chunks = add_contextual_headers(chunks)

            embeddings = get_embeddings()
            CHROMA_DIR.mkdir(parents=True, exist_ok=True)
            Chroma.from_documents(
                documents=chunks, embedding=embeddings,
                persist_directory=str(CHROMA_DIR),
                collection_name=DEFAULT_COLLECTION,
            )
            st.success(f"{len(docs)} documents indexes ({len(chunks)} chunks)")

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📄 Assistant IA")
    st.markdown("---")
    st.page_link("pages/1_Chat.py", label="Chat", icon="💬")
    st.page_link("pages/2_Admin.py", label="Administration", icon="⚙️")

st.markdown("""
<div class="app-header">
    <h1>📄 Assistant Documentaire IA</h1>
    <p>Posez vos questions, obtenez des reponses sourcees depuis vos documents.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Chat.py", label="Ouvrir le Chat", icon="💬", use_container_width=True)
with col2:
    st.page_link("pages/2_Admin.py", label="Administration", icon="⚙️", use_container_width=True)
