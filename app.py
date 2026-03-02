"""Interface Streamlit — Assistant Documentaire IA."""

import sys
import tempfile
from pathlib import Path

import streamlit as st

# Ajouter src/ au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from config import CHROMA_DIR, TOP_K
from ingest import ingest_single_pdf, get_indexed_files
from query import ask

# --- Configuration de la page ---
st.set_page_config(
    page_title="Assistant Documentaire IA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Style CSS personnalise ---
st.markdown("""
<style>
    /* Titre principal */
    .main-title {
        color: #1e3a5f;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    .sub-title {
        color: #5a7d9a;
        font-size: 1rem;
        margin-top: 0;
    }

    /* Sources */
    .source-box {
        background-color: #f0f4f8;
        border-left: 3px solid #1e3a5f;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 4px 4px 0;
        font-size: 0.85rem;
    }

    /* Indicateur de confiance */
    .confidence-high { color: #28a745; font-weight: 600; }
    .confidence-medium { color: #ffc107; font-weight: 600; }
    .confidence-low { color: #dc3545; font-weight: 600; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)


# --- Initialisation de la session ---
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📁 Gestion des documents")

    # Upload de PDFs
    uploaded_files = st.file_uploader(
        "Deposez vos PDFs ici",
        type=["pdf"],
        accept_multiple_files=True,
        help="Les documents seront automatiquement indexes pour la recherche.",
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Verifier si deja traite dans cette session
            processed_key = f"processed_{uploaded_file.name}"
            if processed_key not in st.session_state:
                with st.spinner(f"Indexation de {uploaded_file.name}..."):
                    # Sauvegarder temporairement le fichier
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = Path(tmp.name)

                    try:
                        num_chunks = ingest_single_pdf(tmp_path)
                        st.success(f"{uploaded_file.name} — {num_chunks} chunks indexes")
                        st.session_state[processed_key] = True
                    except Exception as e:
                        st.error(f"Erreur avec {uploaded_file.name} : {e}")
                    finally:
                        tmp_path.unlink(missing_ok=True)

    # Liste des documents indexes
    st.markdown("---")
    st.markdown("### 📋 Documents indexes")

    indexed_files = get_indexed_files()
    if indexed_files:
        for f in indexed_files:
            st.markdown(f"- 📄 {f}")
        st.caption(f"{len(indexed_files)} document(s) dans la base")
    else:
        st.info("Aucun document indexe. Uploadez des PDFs ou lancez `python src/ingest.py`.")

    # Parametres
    st.markdown("---")
    st.markdown("### ⚙️ Parametres")
    top_k = st.slider(
        "Nombre de sources a consulter",
        min_value=1,
        max_value=10,
        value=TOP_K,
        help="Nombre de passages pertinents recuperes pour chaque question.",
    )


# --- Zone principale ---
st.markdown('<p class="main-title">📄 Assistant Documentaire IA</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Posez vos questions, obtenez des reponses sourcees depuis vos documents.</p>', unsafe_allow_html=True)
st.markdown("---")

# Afficher l'historique de conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Afficher les sources si c'est une reponse assistant
        if message["role"] == "assistant" and "sources" in message:
            sources = message["sources"]
            num_sources = message.get("num_sources", 0)

            # Indicateur de confiance
            if num_sources >= 4:
                confidence_class = "confidence-high"
                confidence_label = "Confiance elevee"
            elif num_sources >= 2:
                confidence_class = "confidence-medium"
                confidence_label = "Confiance moyenne"
            else:
                confidence_class = "confidence-low"
                confidence_label = "Confiance faible"

            st.markdown(
                f'<span class="{confidence_class}">{confidence_label} — {num_sources} source(s) trouvee(s)</span>',
                unsafe_allow_html=True,
            )

            # Afficher les sources
            if sources:
                with st.expander("📎 Voir les sources"):
                    for src in sources:
                        score_pct = max(0, 100 - src["score"] * 50)
                        st.markdown(
                            f'<div class="source-box">📄 <strong>{src["file"]}</strong>, '
                            f'page {src["page"]} '
                            f'<em>(pertinence : {score_pct:.0f}%)</em></div>',
                            unsafe_allow_html=True,
                        )


# Input utilisateur
if prompt := st.chat_input("Posez votre question sur vos documents..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generer la reponse
    with st.chat_message("assistant"):
        # Verifier que la base existe
        if not CHROMA_DIR.exists():
            st.warning("Aucune base documentaire trouvee. Uploadez d'abord des documents dans la sidebar.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Aucune base documentaire trouvee. Uploadez d'abord des documents.",
            })
        else:
            with st.spinner("Recherche dans vos documents..."):
                try:
                    result = ask(prompt, top_k=top_k)

                    # Afficher la reponse
                    st.markdown(result["answer"])

                    sources = result["sources"]
                    num_sources = result["num_sources"]

                    # Indicateur de confiance
                    if num_sources >= 4:
                        confidence_class = "confidence-high"
                        confidence_label = "Confiance elevee"
                    elif num_sources >= 2:
                        confidence_class = "confidence-medium"
                        confidence_label = "Confiance moyenne"
                    else:
                        confidence_class = "confidence-low"
                        confidence_label = "Confiance faible"

                    st.markdown(
                        f'<span class="{confidence_class}">{confidence_label} — {num_sources} source(s) trouvee(s)</span>',
                        unsafe_allow_html=True,
                    )

                    # Sources dans un expander
                    if sources:
                        with st.expander("📎 Voir les sources"):
                            for src in sources:
                                score_pct = max(0, 100 - src["score"] * 50)
                                st.markdown(
                                    f'<div class="source-box">📄 <strong>{src["file"]}</strong>, '
                                    f'page {src["page"]} '
                                    f'<em>(pertinence : {score_pct:.0f}%)</em></div>',
                                    unsafe_allow_html=True,
                                )

                    # Sauvegarder dans l'historique
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": sources,
                        "num_sources": num_sources,
                    })

                except Exception as e:
                    error_msg = f"Erreur lors de la generation : {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                    })
