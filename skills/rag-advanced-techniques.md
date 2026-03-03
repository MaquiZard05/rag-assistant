---
name: rag-advanced-techniques
description: Apply when working on the RAG assistant project — any retrieval, ingestion, chunking, query, or response quality task. Also trigger when Marin mentions embeddings, search quality, retrieval, re-ranking, BM25, fusion, chunk strategy, or metadata filtering. This skill ensures Claude Code produces state-of-the-art RAG code instead of basic vanilla implementations.
---

# RAG Advanced Techniques — Patterns de référence

Basé sur NirDiamant/RAG_Techniques (24k+ ⭐), adapté à la stack Marin : LangChain + ChromaDB + sentence-transformers + Groq.

## Principe fondamental

Ne jamais implémenter un RAG avec une seule méthode de retrieval. La recherche sémantique seule rate les correspondances exactes (noms propres, codes, numéros). Le BM25 seul rate le sens. Toujours combiner les deux.

## 1. Fusion Retrieval (sémantique + BM25)

Combine ChromaDB (cosine similarity sur embeddings) avec BM25 (correspondance de mots-clés). Les scores sont normalisés puis fusionnés avec un poids configurable.

Pattern d'implémentation :
```python
from rank_bm25 import BM25Okapi
import numpy as np

def fusion_retrieve(query, collection, documents, alpha=0.7, top_k=5):
    """
    alpha : poids de la recherche sémantique (0.7 = 70% sémantique, 30% BM25)
    """
    # 1. Recherche sémantique via ChromaDB
    sem_results = collection.query(query_texts=[query], n_results=top_k * 2)
    
    # 2. Recherche BM25
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    bm25_scores = bm25.get_scores(query.split())
    
    # 3. Normalisation min-max des deux sets de scores
    # 4. Score final = alpha * sem_score + (1 - alpha) * bm25_score
    # 5. Retourner top_k par score fusionné
```

Dépendance à ajouter : `rank_bm25` (pip install rank-bm25).

Le BM25 index doit être recalculé à chaque ajout de documents. Pour le MVP, recalculer à chaque query est acceptable. En production, maintenir un index persistant.

## 2. Reranking post-retrieval

Après le retrieval (fusion ou simple), un modèle cross-encoder re-score chaque paire (question, chunk) pour affiner la pertinence. Le cross-encoder est plus précis que le bi-encoder (embeddings) car il voit la question ET le chunk ensemble.

Pattern d'implémentation :
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, chunks, top_k=3):
    """Re-score les chunks et retourne les top_k plus pertinents."""
    pairs = [[query, chunk.page_content] for chunk in chunks]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    return [chunk for chunk, score in ranked[:top_k]]
```

Le modèle `cross-encoder/ms-marco-MiniLM-L-6-v2` est gratuit, local, rapide (~50ms pour 10 chunks). Pas d'API nécessaire. Compatible avec la contrainte budget 0€.

Pipeline complet : Query → Fusion Retrieval (top 10) → Reranking (top 3-5) → LLM Generation.

## 3. Contextual Chunk Headers

Chaque chunk stocké doit inclure son contexte d'origine. Sans ça, un chunk isolé comme "La durée est de 3 mois" est inutile — on ne sait pas de quoi on parle.

Pattern d'ingestion :
```python
def add_contextual_header(chunk, filename, page_num, section_title=None):
    header = f"[Source: {filename} | Page {page_num}"
    if section_title:
        header += f" | Section: {section_title}"
    header += "]\n\n"
    chunk.page_content = header + chunk.page_content
    return chunk
```

Appliquer AVANT l'embedding, pour que le contexte soit encodé dans le vecteur. Stocker aussi en metadata pour l'affichage.

## 4. Metadata Filtering

ChromaDB supporte le filtrage par metadata au moment du query. Stocker systématiquement :
- `source_file` : nom du fichier original
- `page_number` : numéro de page
- `doc_type` : catégorie (procédure, FAQ, contrat, etc.)
- `upload_date` : date d'upload
- `collection_id` : ID client (multi-tenant)

Pattern de query avec filtre :
```python
results = collection.query(
    query_texts=[query],
    n_results=10,
    where={"doc_type": "procedure"}  # filtre metadata
)
```

Les filtres metadata sont exécutés AVANT la recherche vectorielle — très performant même sur de grosses collections.

## 5. Conversation avec historique (Memory)

Pour le chat multi-tour, contextualiser la question avec l'historique avant le retrieval.

Pattern :
```python
def contextualize_query(query, history, llm):
    """Reformule la question en incluant le contexte de l'historique."""
    if not history:
        return query
    prompt = f"""Étant donné l'historique de conversation suivant et la nouvelle question,
    reformule la question pour qu'elle soit autonome (compréhensible sans l'historique).
    
    Historique: {history[-3:]}  # 3 derniers échanges max
    Nouvelle question: {query}
    
    Question reformulée:"""
    return llm.invoke(prompt)
```

Appliquer la question reformulée au retrieval, PAS la question brute. Limiter l'historique à 3-5 échanges pour ne pas exploser les tokens.

## Anti-patterns à éviter

- Ne PAS envoyer tous les chunks récupérés au LLM — toujours limiter à 3-5 après reranking
- Ne PAS utiliser des chunks trop gros (>1000 tokens) — 500 tokens avec 100 d'overlap est optimal pour des docs PME
- Ne PAS oublier les metadata à l'ingestion — c'est très dur à rajouter après
- Ne PAS faire de reranking avec le LLM principal (Groq) en production — trop lent et coûteux. Utiliser le cross-encoder local
- Ne PAS recréer le BM25 index à chaque question en production — le cacher en session state