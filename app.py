"""Point d'entree Streamlit — charge le CSS et affiche la page d'accueil."""

from pathlib import Path

import streamlit as st

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

st.markdown("""
<div class="app-header">
    <h1>📄 Assistant Documentaire IA</h1>
    <p>Posez vos questions, obtenez des reponses sourcees depuis vos documents.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("Utilisez le menu de navigation pour acceder aux pages :")
st.markdown("- **💬 Chat** — Posez vos questions sur vos documents")
st.markdown("- **⚙️ Admin** — Gerez vos clients, documents et parametres")
