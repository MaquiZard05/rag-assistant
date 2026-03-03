"""Gestion des clients multi-tenant : CRUD sur clients.json + collections ChromaDB."""

import json
from pathlib import Path

import chromadb

from config import (
    CLIENTS_FILE, CHROMA_DIR,
    DEFAULT_COLLECTION, DEFAULT_SYSTEM_PROMPT,
)


def _get_chroma_client():
    """Client ChromaDB natif — pas besoin d'embeddings pour les operations de lecture."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def _load_clients() -> dict:
    """Charge le fichier clients.json."""
    if not CLIENTS_FILE.exists():
        return {}
    with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_clients(clients: dict):
    """Sauvegarde le fichier clients.json."""
    CLIENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, ensure_ascii=False, indent=2)


def list_clients() -> dict:
    """Retourne tous les clients. Cree le client par defaut si aucun n'existe."""
    clients = _load_clients()
    if not clients:
        clients[DEFAULT_COLLECTION] = {
            "name": "General",
            "system_prompt": DEFAULT_SYSTEM_PROMPT,
        }
        _save_clients(clients)
    return clients


def get_client(client_id: str) -> dict | None:
    """Retourne un client par son ID."""
    clients = _load_clients()
    return clients.get(client_id)


def create_client(client_id: str, name: str, system_prompt: str = None) -> bool:
    """Cree un nouveau client. Retourne False si l'ID existe deja."""
    clients = _load_clients()
    if client_id in clients:
        return False
    clients[client_id] = {
        "name": name,
        "system_prompt": system_prompt or DEFAULT_SYSTEM_PROMPT,
    }
    _save_clients(clients)
    return True


def update_client_prompt(client_id: str, system_prompt: str) -> bool:
    """Met a jour le system prompt d'un client."""
    clients = _load_clients()
    if client_id not in clients:
        return False
    clients[client_id]["system_prompt"] = system_prompt
    _save_clients(clients)
    return True


def delete_client(client_id: str) -> bool:
    """Supprime un client et sa collection ChromaDB."""
    if client_id == DEFAULT_COLLECTION:
        return False

    clients = _load_clients()
    if client_id not in clients:
        return False

    # Supprimer la collection ChromaDB (acces direct, sans embeddings)
    try:
        chroma_client = _get_chroma_client()
        chroma_client.delete_collection(client_id)
    except Exception:
        pass

    del clients[client_id]
    _save_clients(clients)
    return True


def get_collection_stats(client_id: str) -> dict:
    """Retourne les stats d'une collection (acces direct ChromaDB, sans embeddings)."""
    try:
        chroma_client = _get_chroma_client()
        collection = chroma_client.get_or_create_collection(client_id)
        results = collection.get(include=["metadatas"])

        if not results or not results.get("metadatas"):
            return {"num_chunks": 0, "num_docs": 0, "files": []}

        files = set()
        for meta in results["metadatas"]:
            source = meta.get("source", "")
            if source:
                files.add(Path(source).name)

        return {
            "num_chunks": len(results["ids"]),
            "num_docs": len(files),
            "files": sorted(files),
        }
    except Exception:
        return {"num_chunks": 0, "num_docs": 0, "files": []}


def delete_document(client_id: str, filename: str) -> int:
    """Supprime tous les chunks d'un document (acces direct, sans embeddings)."""
    try:
        chroma_client = _get_chroma_client()
        collection = chroma_client.get_or_create_collection(client_id)
        results = collection.get(include=["metadatas"])

        if not results or not results.get("metadatas"):
            return 0

        ids_to_delete = []
        for i, meta in enumerate(results["metadatas"]):
            source = Path(meta.get("source", "")).name
            if source == filename:
                ids_to_delete.append(results["ids"][i])

        if ids_to_delete:
            collection.delete(ids=ids_to_delete)

        return len(ids_to_delete)
    except Exception:
        return 0
