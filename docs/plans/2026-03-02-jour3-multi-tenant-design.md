# Design Jour 3 — Features Pro + Multi-tenant

## Architecture
- Multi-pages Streamlit : app.py (entree) + pages/1_Chat.py + pages/2_Admin.py
- CSS externe : styles/main.css (palette bleu corporate)
- Multi-client : selecteur sidebar, 1 collection ChromaDB par client
- Config clients : data/clients.json

## Fichiers
- app.py : rewrite — point entree minimaliste
- pages/1_Chat.py : creer — chat + upload + historique conversation
- pages/2_Admin.py : creer — dashboard + gestion clients + system prompt
- styles/main.css : creer — CSS pro
- src/clients.py : creer — CRUD clients
- src/config.py : modifier — constantes multi-tenant
- src/ingest.py : modifier — collection_name param + chunk headers
- src/query.py : modifier — historique conversation + reranking

## RAG Ameliorations
- Contextual Chunk Headers avant embedding
- Reranking cross-encoder post-retrieval
- Reformulation question avec historique conversation
