"""Page Admin — Gestion clients, documents, upload, system prompts."""

import sys
import tempfile
from html import escape
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from clients import (
    list_clients, create_client, update_client_prompt,
    delete_client, get_collection_stats, delete_document,
)
from ingest import ingest_single_file

# --- Configuration ---
st.set_page_config(
    page_title="Admin — Assistant Documentaire IA",
    page_icon=":material/settings:",
    layout="centered",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    css_path = Path(__file__).resolve().parent.parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")


def render_header(title, subtitle=None):
    html = f'''
    <div class="app-header">
        <h1>{escape(str(title))}</h1>
        {"<p>" + escape(str(subtitle)) + "</p>" if subtitle else ""}
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)


def render_metric(value, label):
    st.markdown(f'''
    <div class="metric-card">
        <h3>{value}</h3>
        <p>{label}</p>
    </div>
    ''', unsafe_allow_html=True)


# --- Sidebar navigation ---
with st.sidebar:
    st.markdown("### Administration")
    st.caption("Gestion clients, documents, parametres")
    st.markdown("---")
    st.page_link("pages/1_Chat.py", label="Retour au Chat", icon=":material/chat:")
    st.page_link("app.py", label="Accueil", icon=":material/home:")

# --- Header ---
render_header("Administration", "Gerez vos clients, documents et parametres")

# --- Dashboard ---
clients = list_clients()

total_docs = 0
total_chunks = 0
all_stats = {}
for cid in clients:
    stats = get_collection_stats(cid)
    all_stats[cid] = stats
    total_docs += stats["num_docs"]
    total_chunks += stats["num_chunks"]

col1, col2, col3 = st.columns(3)
with col1:
    render_metric(total_docs, "Documents")
with col2:
    render_metric(total_chunks, "Chunks")
with col3:
    render_metric(len(clients), "Clients")

st.markdown("<br>", unsafe_allow_html=True)

# --- Nouveau client ---
st.markdown("### Nouveau client")

with st.form("new_client_form"):
    col_id, col_name = st.columns(2)
    with col_id:
        new_id = st.text_input("Identifiant (sans espaces)", placeholder="cabinet-dupont")
    with col_name:
        new_name = st.text_input("Nom complet", placeholder="Cabinet Dupont & Fils")

    submitted = st.form_submit_button("Creer le client")
    if submitted:
        if not new_id or not new_name:
            st.error("L'identifiant et le nom sont obligatoires.")
        elif " " in new_id:
            st.error("L'identifiant ne doit pas contenir d'espaces.")
        else:
            if create_client(new_id.lower().strip(), new_name.strip()):
                st.success(f"Client '{new_name}' cree.")
                st.rerun()
            else:
                st.error(f"L'identifiant '{new_id}' existe deja.")

st.markdown("---")

# --- Clients existants ---
for cid, client in clients.items():
    stats = all_stats.get(cid, {"num_docs": 0, "num_chunks": 0, "files": []})

    with st.expander(f"{client['name']} — {stats['num_docs']} doc(s), {stats['num_chunks']} chunks"):

        # Upload de documents pour ce client
        st.markdown("**Ajouter des documents**")
        uploaded_files = st.file_uploader(
            f"Deposez des documents pour {client['name']}",
            type=["pdf", "txt", "docx", "html", "htm"],
            accept_multiple_files=True,
            key=f"upload_{cid}",
            label_visibility="collapsed",
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                processed_key = f"processed_{cid}_{uploaded_file.name}"
                if processed_key not in st.session_state:
                    with st.spinner(f"Indexation de {uploaded_file.name}..."):
                        suffix = Path(uploaded_file.name).suffix
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                            tmp.write(uploaded_file.read())
                            tmp_path = Path(tmp.name)

                        try:
                            num_chunks = ingest_single_file(
                                tmp_path,
                                collection_name=cid,
                                original_name=uploaded_file.name,
                            )
                            st.success(f"{uploaded_file.name} — {num_chunks} chunks indexes")
                            st.session_state[processed_key] = True
                        except Exception as e:
                            st.error(f"Erreur : {e}")
                        finally:
                            tmp_path.unlink(missing_ok=True)

        # Documents indexes
        if stats["files"]:
            st.markdown("**Documents indexes**")
            for filename in stats["files"]:
                col_file, col_btn = st.columns([4, 1])
                with col_file:
                    st.markdown(f"{filename}")
                with col_btn:
                    if st.button("Supprimer", key=f"del_doc_{cid}_{filename}"):
                        deleted = delete_document(cid, filename)
                        st.success(f"{filename} supprime ({deleted} chunks)")
                        st.rerun()

        st.markdown("---")

        # System prompt
        st.markdown("**System prompt**")
        new_prompt = st.text_area(
            "Prompt",
            value=client.get("system_prompt", ""),
            height=120,
            key=f"prompt_{cid}",
            label_visibility="collapsed",
        )

        col_save, col_delete = st.columns([1, 1])
        with col_save:
            if st.button("Sauvegarder", key=f"save_{cid}"):
                update_client_prompt(cid, new_prompt)
                st.success("Prompt sauvegarde.")

        with col_delete:
            if cid != "default":
                if st.button("Supprimer ce client", key=f"del_client_{cid}"):
                    delete_client(cid)
                    st.success(f"Client '{client['name']}' supprime.")
                    st.rerun()
