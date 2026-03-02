# Design Jour 2 — Qualite + Interface Streamlit

## Objectifs
1. Script de comparaison de tailles de chunks (500/1000/1500)
2. Interface Streamlit pro/corporate avec upload immediat
3. Refactoring minimal d'ingest.py pour ingestion unitaire

## Interface Streamlit (app.py)
- Sidebar : upload PDF (ingestion immediate), liste docs indexes, param Top K
- Zone principale : chat avec historique (st.chat_message), reponses sourcees, indicateur confiance
- Style : sobre, bleu/gris, titre "Assistant Documentaire IA"

## Fichiers touches
- `app.py` : creer — interface Streamlit
- `src/ingest.py` : modifier — ajouter ingest_single_pdf()
- `src/query.py` : modifier — extraire fonctions pour reutilisation
- `tests/compare_chunks.py` : creer — comparaison tailles chunks
