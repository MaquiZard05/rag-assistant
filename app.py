"""Point d'entree Streamlit — charge le CSS et redirige vers la page Chat."""

import sys
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

# --- Configuration de la page ---
st.set_page_config(
    page_title="Assistant Documentaire IA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    """Charge et injecte un fichier CSS custom."""
    css_path = Path(__file__).resolve().parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Charger le CSS global
load_css("styles/main.css")

# Page d'accueil
st.markdown("""
<div class="main-header">
    <h1>📄 Assistant Documentaire IA</h1>
    <p>Posez vos questions, obtenez des reponses sourcees depuis vos documents.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("Utilisez le menu dans la sidebar pour naviguer :")
st.markdown("- **💬 Chat** — Posez vos questions sur vos documents")
st.markdown("- **⚙️ Admin** — Gerez vos clients, documents et parametres")
