# ROADMAP RAG — Projet Freelance IA (5 Jours)

## Contexte Projet
**Objectif** : Construire un systeme RAG vendable pour PME/TPE, agences et cabinets.
**Pitch** : "Un assistant IA qui repond aux questions de vos equipes en s'appuyant sur vos propres documents."
**Stack** : Python + LangChain + ChromaDB + Groq API (Llama 3) + Streamlit
**Profil** : Marin, non-developpeur, apprentissage par la pratique (vibe coding).

---

## PLANNING 5 JOURS

---

### JOUR 1 — FONDATIONS + PREMIER PIPELINE ✅ TERMINE

- [x] Environnement Python + dependances (langchain, chromadb, sentence-transformers, streamlit, groq)
- [x] Script d'ingestion (`src/ingest.py`) — charge PDFs, decoupe en chunks, stocke dans ChromaDB
- [x] Script de query (`src/query.py`) — question → retrieval top 5 → reponse Groq sourcee
- [x] 5 documents exemples Duval & Associes (QSE, RH, FAQ, Chantier, Catalogue) — 33 chunks
- [x] Embeddings : sentence-transformers all-MiniLM-L6-v2 (local, gratuit)
- [x] LLM : Groq API (llama-3.1-8b-instant, gratuit)
- [x] Structure propre : config.py + ingest.py + query.py

---

### JOUR 2 — QUALITE + INTERFACE ✅ TERMINE

- [x] Chunking optimise : 500/100 au lieu de 1000/200 (test scientifique via compare_chunks.py)
- [x] 62 chunks au lieu de 33 — meilleure granularite de recherche
- [x] Interface Streamlit : upload PDF, chat, sources, indicateur de confiance
- [x] Refactoring : ingest_single_pdf() + ask() pour reutilisation

---

### JOUR 3 — FEATURES PRO + MULTI-TENANT ✅ TERMINE

- [x] Architecture multi-pages : app.py + pages/1_Chat.py + pages/2_Admin.py
- [x] CSS externe pro : styles/main.css (palette sombre corporate)
- [x] Multi-client : clients.json + collection ChromaDB par client + selecteur sidebar
- [x] Historique conversation : reformulation de question via LLM avant retrieval
- [x] System prompt personnalisable par client
- [x] Panneau admin : dashboard metrics + CRUD clients + gestion docs + edit prompts
- [x] Reranking cross-encoder (ms-marco-MiniLM-L-6-v2) post-retrieval
- [x] Contextual Chunk Headers (source + page injectes dans le chunk avant embedding)
- [x] Gestion erreurs : timeout Groq, validation PDF, messages clairs

---

### JOUR 4 — DEPLOIEMENT + MULTI-FORMAT + AUDIT ✅ TERMINE

- [x] Deploiement Streamlit Cloud (st.secrets, auto-ingest, config.toml)
- [x] Ingestion multi-format : PDF, TXT, DOCX, HTML (loaders LangChain)
- [x] Interface chat style ChatGPT : sidebar visible, navigation, selecteur client
- [x] Cache embeddings (singleton) + acces ChromaDB direct pour stats (navigation instantanee)
- [x] Pool hybride search x4 pour meilleur reranking
- [x] 2 clients demo : Duval BTP (5 docs, 62 chunks) + Pulse Digital (5 docs, 533 chunks)
- [x] Audit complet J+4 : scorecard C+, 4 correctifs immediats appliques
- [x] Fix securite : XSS (html.escape), exceptions loguees, page fallback non-PDF
- [x] 8 corrections design : renommage pages, DM Sans, masquage nav Streamlit, curseur pointer
- [x] Emojis UI remplaces par icones Material/SVG (rendu pro)
- [x] README mis a jour avec toutes les features

---

### JOUR 5 — PACKAGING COMMERCIAL + OUTREACH ⬅️ PROCHAIN

**Matin — Offre commerciale**
- [ ] Definir l'offre :
  - **Starter** (500-800EUR) : RAG sur vos docs, interface chat, 1 collection, setup inclus
  - **Pro** (1000-1500EUR) : Multi-collections, personnalisation, formation equipe, support 1 mois
  - **Maintenance** (200-300EUR/mois) : Mises a jour, ajout de docs, support
- [ ] Rediger un one-pager commercial (PDF propre)
- [ ] Preparer 3 templates de messages de prospection (email, LinkedIn, DM)

**Apres-midi — Premier outreach**
- [ ] Identifier 20 prospects (agences, cabinets conseil, PME tech)
- [ ] Envoyer les 10 premiers messages personnalises
- [ ] S'inscrire sur Malt / plateformes freelance avec offre RAG
- [ ] Poster dans des communautes tech (Discord IA, forums freelance)

**Soir — Bilan et suite**
- [ ] Bilan des 5 jours
- [ ] Planifier la Semaine 2

---

## STACK TECHNIQUE

| Composant | Outil | Cout |
|-----------|-------|------|
| Langage | Python 3.11+ | Gratuit |
| Orchestration RAG | LangChain | Gratuit |
| Vector Store | ChromaDB (locale) | Gratuit |
| LLM | Groq API (Llama 3) | Gratuit |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 | Gratuit (local) |
| Reranking | Cross-encoder ms-marco-MiniLM-L-6-v2 | Gratuit (local) |
| Interface | Streamlit | Gratuit |
| Deploiement | Streamlit Cloud | Gratuit |
| Repo | GitHub public | Gratuit |

**Budget total : 0EUR** — Tout tourne gratuitement.

---

## PIPELINE RAG

```
Question utilisateur
    → Reformulation avec historique (LLM)
    → Recherche hybride (vectorielle + BM25)
    → Fusion RRF (Reciprocal Rank Fusion)
    → Reranking cross-encoder
    → Generation LLM avec contexte
    → Reponse sourcee (fichier + page + score)
```

---

## METRIQUES DE SUCCES

| Jour | Metrique | Statut |
|------|----------|--------|
| J1 | Pipeline fonctionnel : question → reponse sourcee | ✅ |
| J2 | Interface Streamlit utilisable par un non-tech | ✅ |
| J3 | Multi-client + historique conversation + admin | ✅ |
| J4 | App deployee + multi-format + audit + design pro | ✅ |
| J5 | Offre commerciale prete + premiers messages envoyes | ⬜ |

---

## IDEES PARKEES (a reprendre apres)

- RAG specialise BTP (DTU, CCTP, CCAP) — niche premium
- Outil d'analyse d'appels d'offres BTP (produit long terme)
- Integration CRM + IA automation
- Upgrade LLM payant (GPT-4o / Claude) quand clients paient

---

*Derniere mise a jour : 03/03/2026*
