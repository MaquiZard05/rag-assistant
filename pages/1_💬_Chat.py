"""Page Chat — Interface RAG principale avec multi-client et historique."""

import sys
import tempfile
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import TOP_K, DEFAULT_COLLECTION
from ingest import ingest_single_pdf, get_indexed_files
from query import ask
from clients import list_clients, get_client

# --- Configuration ---
st.set_page_config(
    page_title="Chat — Assistant Documentaire IA",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    css_path = Path(__file__).resolve().parent.parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")


def get_confidence(sources):
    """Determine la confiance basee sur le meilleur score de reranking."""
    if not sources:
        return "confidence-low", "Confiance faible"

    best_score = max(s["score"] for s in sources)

    if best_score > 4:
        return "confidence-high", "Confiance elevee"
    elif best_score > 1:
        return "confidence-medium", "Confiance moyenne"
    else:
        return "confidence-low", "Confiance faible"


def render_sources(sources):
    """Affiche les sources avec leur score de pertinence."""
    confidence_class, confidence_label = get_confidence(sources)

    st.markdown(
        f'<span class="{confidence_class}">{confidence_label} — {len(sources)} source(s)</span>',
        unsafe_allow_html=True,
    )

    if sources:
        with st.expander("📎 Voir les sources"):
            for src in sources:
                score_pct = min(100, max(0, src["score"] * 10))
                st.markdown(
                    f'<div class="source-box">📄 <strong>{src["file"]}</strong>, '
                    f'page {src["page"]} '
                    f'<em>(pertinence : {score_pct:.0f}%)</em></div>',
                    unsafe_allow_html=True,
                )


# --- Initialisation session ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    # Selecteur de client
    clients = list_clients()
    client_ids = list(clients.keys())
    client_names = [clients[cid]["name"] for cid in client_ids]

    st.markdown("### 👤 Client actif")
    selected_idx = st.selectbox(
        "Choisir le client",
        range(len(client_ids)),
        format_func=lambda i: client_names[i],
        label_visibility="collapsed",
    )
    active_client_id = client_ids[selected_idx]
    active_client = clients[active_client_id]

    # Reset conversation si on change de client
    if "active_client" not in st.session_state:
        st.session_state.active_client = active_client_id
    if st.session_state.active_client != active_client_id:
        st.session_state.messages = []
        st.session_state.active_client = active_client_id

    st.markdown("---")

    # Upload de PDFs
    st.markdown("### 📁 Ajouter des documents")
    uploaded_files = st.file_uploader(
        "Deposez vos PDFs ici",
        type=["pdf"],
        accept_multiple_files=True,
        help="Les documents seront indexes dans la collection du client actif.",
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            processed_key = f"processed_{active_client_id}_{uploaded_file.name}"
            if processed_key not in st.session_state:
                with st.spinner(f"Indexation de {uploaded_file.name}..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = Path(tmp.name)

                    try:
                        num_chunks = ingest_single_pdf(
                            tmp_path,
                            collection_name=active_client_id,
                            original_name=uploaded_file.name,
                        )
                        st.success(f"{uploaded_file.name} — {num_chunks} chunks")
                        st.session_state[processed_key] = True
                    except Exception as e:
                        st.error(f"Erreur : {e}")
                    finally:
                        tmp_path.unlink(missing_ok=True)

    st.markdown("---")

    # Documents indexes
    st.markdown("### 📋 Documents indexes")
    indexed_files = get_indexed_files(collection_name=active_client_id)
    if indexed_files:
        for f in indexed_files:
            st.markdown(f"📄 {f}")
        st.caption(f"{len(indexed_files)} document(s)")
    else:
        st.info("Aucun document. Uploadez des PDFs ci-dessus.")

    st.markdown("---")

    # Parametres
    st.markdown("### ⚙️ Parametres")
    top_k = st.slider("Sources a consulter", min_value=1, max_value=10, value=TOP_K)

    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()


# --- Zone principale ---
st.markdown(f"""
<div class="main-header">
    <h1>💬 {active_client['name']}</h1>
    <p>Posez vos questions sur les documents de {active_client['name']}</p>
</div>
""", unsafe_allow_html=True)

# Historique
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            render_sources(message["sources"])

# Input
if prompt := st.chat_input("Posez votre question sur vos documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        if not indexed_files:
            msg = "Aucun document indexe pour ce client. Uploadez d'abord des PDFs dans la sidebar."
            st.warning(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            with st.spinner("Recherche dans vos documents..."):
                try:
                    result = ask(
                        prompt,
                        top_k=top_k,
                        collection_name=active_client_id,
                        system_prompt=active_client.get("system_prompt", ""),
                        history=st.session_state.messages[:-1],
                    )

                    st.markdown(result["answer"])
                    render_sources(result["sources"])

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"],
                    })

                except Exception as e:
                    error_msg = f"Erreur : {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
