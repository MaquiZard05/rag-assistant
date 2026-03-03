import os
from pathlib import Path
from dotenv import load_dotenv

# Charger le .env depuis la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# --- API ---
# Supporte .env (local) et st.secrets (Streamlit Cloud)
def _get_secret(key: str) -> str | None:
    """Recupere une cle API depuis .env ou st.secrets (Streamlit Cloud)."""
    value = os.getenv(key)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(key)
    except Exception:
        return None

GROQ_API_KEY = _get_secret("GROQ_API_KEY")

# --- Modèles ---
# Modele multilingue : comprend le francais technique (vs all-MiniLM-L6-v2 qui est anglophone)
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "llama-3.1-8b-instant"

# --- Chemins ---
DOCS_DIR = PROJECT_ROOT / "docs"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"
CLIENTS_FILE = PROJECT_ROOT / "data" / "clients.json"

# --- Chunking ---
# Teste avec compare_chunks.py : 500/100 donne les meilleurs scores de pertinence
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# --- Retrieval ---
TOP_K = 5                # Minimum de chunks garantis apres reranking
MAX_CHUNKS = 10          # Maximum absolu de chunks envoyes au LLM
RERANK_THRESHOLD = 2.0   # Score cross-encoder minimum pour inclure un chunk au-dela de TOP_K
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# --- Multi-tenant ---
DEFAULT_COLLECTION = "default"
DEFAULT_SYSTEM_PROMPT = (
    "Tu es un assistant qui repond aux questions en te basant UNIQUEMENT "
    "sur le contexte fourni ci-dessous. "
    "Si l'information n'est pas dans le contexte, dis-le clairement. "
    "Cite toujours tes sources (nom du fichier et numero de page)."
)
