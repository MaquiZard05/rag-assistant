import os
from pathlib import Path
from dotenv import load_dotenv

# Charger le .env depuis la racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# --- API ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Modèles ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"

# --- Chemins ---
DOCS_DIR = PROJECT_ROOT / "docs"
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma_db"

# --- Chunking ---
# Teste avec compare_chunks.py : 500/100 donne les meilleurs scores de pertinence
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# --- Retrieval ---
TOP_K = 5
