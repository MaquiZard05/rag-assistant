"""Page Chat — Assistant BTP. Sidebar categories, questions suggerees, sources detaillees."""

import sys
from html import escape
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from config import TOP_K, DEFAULT_COLLECTION
from ingest import get_indexed_files
from query import ask, CATEGORY_FILTERS
from clients import list_clients

# --- Configuration ---
st.set_page_config(
    page_title="Chat — Assistant BTP",
    page_icon=":material/chat:",
    layout="centered",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    css_path = Path(__file__).resolve().parent.parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")


# --- Categories BTP ---
BTP_CATEGORIES = [
    {"icon": "straighten", "label": "Normes & DTU", "key": "normes"},
    {"icon": "description", "label": "CCTP / CCAP", "key": "cctp"},
    {"icon": "health_and_safety", "label": "QSE / PPSPS", "key": "qse"},
    {"icon": "build", "label": "Fiches techniques", "key": "fiches"},
    {"icon": "folder", "label": "DOE / PV reception", "key": "doe"},
    {"icon": "article", "label": "Administratif", "key": "admin"},
]

SUGGESTED_QUESTIONS = [
    {"cat": "Normes & DTU", "q": "Quel DTU s'applique pour l'isolation thermique par l'exterieur ?"},
    {"cat": "QSE / PPSPS", "q": "Quelles sont les obligations du PPSPS pour un chantier > 500 000 EUR ?"},
    {"cat": "CCTP / CCAP", "q": "Quels sont les delais d'execution prevus au lot gros oeuvre du CCTP ?"},
    {"cat": "Fiches techniques", "q": "Quelle est la resistance thermique du Knauf TH38 en 120mm ?"},
    {"cat": "QSE / PPSPS", "q": "Procedure en cas d'accident sur chantier — quelles etapes immediates ?"},
    {"cat": "DOE", "q": "Quels documents sont exiges dans le DOE pour la reception ?"},
]


def format_source_indicator(score):
    """Convertit un score cross-encoder en indicateur visuel."""
    if score >= 5.0:
        return "Tres pertinent"
    elif score >= 2.0:
        return "Pertinent"
    else:
        return "Pertinence moderee"


def render_sources(sources):
    """Affiche les sources en Markdown pur — format fiche chantier."""
    if not sources:
        return

    displayed = [s for s in sources if s.get("score", 0) >= 0.3]

    if not displayed:
        st.markdown("*Aucune source suffisamment pertinente pour cette question.*")
        return

    lines = []
    lines.append("---")
    lines.append(f"**Sources utilisees** ({len(displayed)})")
    lines.append("")

    for src in displayed:
        filename = src.get("file", "Document inconnu")
        page = src.get("page")
        score = src.get("score", 0)
        indicator = format_source_indicator(score)

        page_str = f" — Page {page}" if page is not None else ""
        lines.append(f"- **{filename}**{page_str} — {indicator}")

    st.markdown("\n".join(lines))


def generate_response(question, indexed_files, active_client_id, active_client, active_cat_key=None):
    """Lance la requete RAG et affiche la reponse avec sources."""
    with st.chat_message("assistant"):
        if not indexed_files:
            msg = "Aucun document disponible. Rendez-vous sur la page **Administration** pour en ajouter."
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        else:
            typing_placeholder = st.empty()
            typing_placeholder.markdown('''
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            ''', unsafe_allow_html=True)

            try:
                result = ask(
                    question,
                    top_k=TOP_K,
                    collection_name=active_client_id,
                    system_prompt=active_client.get("system_prompt", ""),
                    history=st.session_state.messages[:-1],
                    category=active_cat_key,
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


# --- Initialisation session ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_category" not in st.session_state:
    st.session_state.active_category = None

# --- Sidebar BTP ---
with st.sidebar:
    # Logo
    st.markdown('''
    <div class="btp-logo">
        <div class="btp-logo-icon">B</div>
        <div class="btp-logo-text">
            <span class="btp-logo-title">Assistant BTP</span>
            <span class="btp-logo-sub">Intelligence documentaire</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # Selecteur de client
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

    # Metriques sidebar
    indexed_files = get_indexed_files(collection_name=active_client_id)
    st.markdown(f'''
    <div class="sidebar-metrics">
        <div class="sidebar-metric">
            <div class="sidebar-metric-value">{len(indexed_files)}</div>
            <div class="sidebar-metric-label">Documents</div>
        </div>
        <div class="sidebar-metric">
            <div class="sidebar-metric-value">{len(BTP_CATEGORIES)}</div>
            <div class="sidebar-metric-label">Categories</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # Categories BTP
    st.markdown('<div class="sidebar-section-label">Base documentaire</div>', unsafe_allow_html=True)

    for cat in BTP_CATEGORIES:
        is_active = st.session_state.active_category == cat["label"]
        if st.button(
            f":{cat['icon']}: {cat['label']}",
            key=f"cat_{cat['key']}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            # Toggle : recliquer desactive le filtre
            if st.session_state.active_category == cat["label"]:
                st.session_state.active_category = None
            else:
                st.session_state.active_category = cat["label"]
            st.rerun()

    st.markdown("---")

    # Bouton nouvelle conversation
    if st.button("Nouvelle conversation", icon=":material/add:", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_category = None
        st.rerun()

    st.markdown("---")

    # Navigation
    st.page_link("pages/2_Admin.py", label="Administration", icon=":material/settings:")
    st.page_link("app.py", label="Accueil", icon=":material/home:")


# --- Mapping categorie active → cle pour le filtrage RAG ---
active_cat_key = None
if st.session_state.active_category:
    for cat in BTP_CATEGORIES:
        if cat["label"] == st.session_state.active_category:
            active_cat_key = cat["key"]
            break

# --- Header zone chat ---
active_cat_label = st.session_state.active_category or "Tous les documents"
st.markdown(f'''
<div class="chat-header">
    <div class="chat-header-left">
        <span class="chat-header-title">{escape(active_cat_label)}</span>
        <span class="chat-header-sub">Recherche intelligente dans vos documents</span>
    </div>
    <div class="chat-header-status">{escape(active_client["name"])} — {len(indexed_files)} documents</div>
</div>
''', unsafe_allow_html=True)


# --- Ecran d'accueil (pas de messages) ---
if not st.session_state.messages:
    st.markdown(f'''
    <div class="welcome-screen">
        <div class="welcome-logo">B</div>
        <div class="welcome-title">Assistant documentaire BTP</div>
        <div class="welcome-subtitle">
            Posez une question sur les documents de {escape(active_client["name"])} —
            normes, CCTP, procedures QSE, fiches techniques.
            Reponses sourcees avec score de fiabilite.
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Grille de questions suggerees
    cols = st.columns(2)
    for i, sq in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 2]:
            # Utiliser un bouton Streamlit avec le texte de la question
            if st.button(
                sq["q"],
                key=f"suggest_{i}",
                use_container_width=True,
                help=sq["cat"],
            ):
                st.session_state.messages.append({"role": "user", "content": sq["q"]})
                st.rerun()


# --- Historique ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            render_sources(message["sources"])

# --- Question en attente (question suggeree sans reponse) ---
if (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
):
    generate_response(
        st.session_state.messages[-1]["content"],
        indexed_files, active_client_id, active_client, active_cat_key,
    )

# --- Input ---
if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    generate_response(prompt, indexed_files, active_client_id, active_client, active_cat_key)

# Disclaimer
st.markdown(
    '<div class="chat-disclaimer">Reponses generees a partir de vos documents internes — Sources citees systematiquement</div>',
    unsafe_allow_html=True,
)
