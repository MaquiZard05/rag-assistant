"""Page Chat — Interface RAG style ChatGPT. Sidebar toujours visible."""

import sys
from html import escape
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import TOP_K, DEFAULT_COLLECTION
from ingest import get_indexed_files
from query import ask
from clients import list_clients

# --- Configuration ---
st.set_page_config(
    page_title="Chat — Assistant Documentaire IA",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    css_path = Path(__file__).resolve().parent.parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")


def get_confidence(sources):
    """Confiance basee sur le meilleur score de reranking."""
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
    confidence_class, confidence_label = get_confidence(sources)
    st.markdown(
        f'<span class="{confidence_class}">{confidence_label} — {len(sources)} source(s)</span>',
        unsafe_allow_html=True,
    )
    if sources:
        with st.expander("Voir les sources"):
            for src in sources:
                score_pct = min(100, max(0, src["score"] * 10))
                page_info = f", page {src['page']}" if src.get("page") is not None else ""
                st.markdown(
                    f'<div class="source-box"><strong>{escape(src["file"])}</strong>'
                    f'{page_info} '
                    f'<em>(pertinence : {score_pct:.0f}%)</em></div>',
                    unsafe_allow_html=True,
                )


# --- Initialisation session ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar style ChatGPT ---
with st.sidebar:
    st.markdown("### 💬 Assistant IA")
    st.caption("Posez vos questions sur vos documents")

    st.markdown("---")

    # Selecteur de client (= espace de travail)
    clients = list_clients()
    client_ids = list(clients.keys())
    client_names = [clients[cid]["name"] for cid in client_ids]

    selected_idx = st.selectbox(
        "Espace client",
        range(len(client_ids)),
        format_func=lambda i: client_names[i],
    )
    active_client_id = client_ids[selected_idx]
    active_client = clients[active_client_id]

    # Reset conversation si changement de client
    if "active_client" not in st.session_state:
        st.session_state.active_client = active_client_id
    if st.session_state.active_client != active_client_id:
        st.session_state.messages = []
        st.session_state.active_client = active_client_id

    # Bouton nouvelle conversation
    if st.button("🗑 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    # Stats rapides
    indexed_files = get_indexed_files(collection_name=active_client_id)
    st.markdown(f"**{len(indexed_files)} document(s)** indexes")
    if indexed_files:
        for f in indexed_files:
            st.markdown(f'<div class="sidebar-doc-name">📄 {escape(f)}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.page_link("pages/2_Admin.py", label="⚙️ Administration", icon="⚙️")
    st.page_link("app.py", label="🏠 Accueil", icon="🏠")


# --- Zone de chat principale ---

# Message d'accueil si conversation vide
if not st.session_state.messages:
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
        <h2 style="color: #1a1a2e; font-weight: 600;">Bonjour 👋</h2>
        <p style="font-size: 1.05rem; max-width: 500px; margin: 0.5rem auto;">
            Posez une question sur les documents de <strong>{escape(active_client['name'])}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Historique
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            render_sources(message["sources"])

# --- Input ---
if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        if not indexed_files:
            msg = "Aucun document disponible. Rendez-vous sur la page **⚙️ Administration** pour en ajouter."
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            # Typing indicator
            typing_placeholder = st.empty()
            typing_placeholder.markdown('''
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            ''', unsafe_allow_html=True)

            try:
                result = ask(
                    prompt,
                    top_k=TOP_K,
                    collection_name=active_client_id,
                    system_prompt=active_client.get("system_prompt", ""),
                    history=st.session_state.messages[:-1],
                )

                typing_placeholder.empty()

                st.markdown(result["answer"])
                render_sources(result["sources"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })

            except Exception as e:
                typing_placeholder.empty()
                error_msg = f"Erreur : {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
