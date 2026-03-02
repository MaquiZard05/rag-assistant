"""Page Admin — Gestion clients, documents, system prompts."""

import sys
from pathlib import Path

import streamlit as st

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from clients import (
    list_clients, create_client, update_client_prompt,
    delete_client, get_collection_stats, delete_document,
)

# --- Configuration ---
st.set_page_config(
    page_title="Admin — Assistant Documentaire IA",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css(css_file: str):
    css_path = Path(__file__).resolve().parent.parent / css_file
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("styles/main.css")


def render_metric_card(value, label):
    st.markdown(f'''
    <div class="metric-card">
        <h3>{value}</h3>
        <p>{label}</p>
    </div>
    ''', unsafe_allow_html=True)


# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>⚙️ Administration</h1>
    <p>Gerez vos clients, documents et parametres</p>
</div>
""", unsafe_allow_html=True)

# --- Dashboard global ---
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
    render_metric_card(total_docs, "Documents indexes")
with col2:
    render_metric_card(total_chunks, "Chunks en base")
with col3:
    render_metric_card(len(clients), "Clients actifs")

st.markdown("<br>", unsafe_allow_html=True)

# --- Creer un nouveau client ---
st.markdown("### ➕ Nouveau client")

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
                st.success(f"Client '{new_name}' cree avec succes.")
                st.rerun()
            else:
                st.error(f"L'identifiant '{new_id}' existe deja.")

st.markdown("---")

# --- Liste des clients ---
st.markdown("### 📂 Clients existants")

for cid, client in clients.items():
    stats = all_stats.get(cid, {"num_docs": 0, "num_chunks": 0, "files": []})

    with st.expander(f"📂 {client['name']} — {stats['num_docs']} doc(s), {stats['num_chunks']} chunks"):

        # Documents indexes
        if stats["files"]:
            st.markdown("**Documents indexes :**")
            for filename in stats["files"]:
                col_file, col_btn = st.columns([4, 1])
                with col_file:
                    st.markdown(f"📄 {filename}")
                with col_btn:
                    if st.button("🗑️", key=f"del_doc_{cid}_{filename}", help=f"Supprimer {filename}"):
                        deleted = delete_document(cid, filename)
                        st.success(f"{filename} supprime ({deleted} chunks)")
                        st.rerun()
        else:
            st.info("Aucun document indexe pour ce client.")

        st.markdown("---")

        # System prompt
        st.markdown("**System prompt :**")
        prompt_key = f"prompt_{cid}"
        new_prompt = st.text_area(
            "System prompt",
            value=client.get("system_prompt", ""),
            height=120,
            key=prompt_key,
            label_visibility="collapsed",
        )

        col_save, col_delete = st.columns([1, 1])

        with col_save:
            if st.button("💾 Sauvegarder le prompt", key=f"save_{cid}"):
                update_client_prompt(cid, new_prompt)
                st.success("Prompt sauvegarde.")

        with col_delete:
            if cid != "default":
                if st.button("🗑️ Supprimer ce client", key=f"del_client_{cid}", type="secondary"):
                    delete_client(cid)
                    st.success(f"Client '{client['name']}' supprime.")
                    st.rerun()
