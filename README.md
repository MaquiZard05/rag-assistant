# Assistant Conformite Chantier BTP

Assistant IA specialise BTP qui repond aux questions de vos equipes terrain en s'appuyant sur vos documents internes (DTU, CCTP, QSE, fiches techniques, DOE).

**Pitch :** Vos equipes posent une question → reponse structuree en fiche chantier avec les sources en 3 secondes.

## Fonctionnalites

- **Reponses format fiche chantier** : titre, sections, valeurs en gras, point de vigilance — exploitable en reunion
- **Recherche hybride** : vectorielle + BM25 + reranking adaptatif cross-encoder (corpus complet)
- **Sources separees** : affichees proprement sous la reponse avec indicateur de pertinence
- **Upload de documents** (PDF, TXT, DOCX, HTML) avec indexation automatique
- **Multi-client** : espaces de travail isoles par client (collection ChromaDB separee)
- **Historique conversation** : reformulation automatique des questions avec contexte
- **System prompt personnalisable** par client (format fiche chantier pour le BTP)
- **Panneau admin** : gestion clients, documents, prompts
- **Dark theme industrie** adapte au terrain (orange chantier, contrastes forts)
- **Deploiement** Streamlit Cloud (gratuit)

## Installation

```bash
# Cloner le repo
git clone https://github.com/MaquiZard05/rag-assistant.git
cd rag-assistant

# Creer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dependances
pip install -r requirements.txt
```

## Configuration

Creer un fichier `.env` a la racine du projet :

```
GROQ_API_KEY=votre_cle_groq
```

Obtenir une cle gratuite sur [console.groq.com](https://console.groq.com).

## Lancement

```bash
# Activer l'environnement
source venv/bin/activate

# Lancer l'interface web
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`. Les documents de demo sont indexes automatiquement au premier lancement.

## Utilisation

1. **Selectionnez un client** dans la sidebar (espace de travail)
2. **Deposez vos documents** via le panneau Administration (PDF, TXT, DOCX, HTML)
3. **Posez vos questions** dans la barre de chat
4. **Consultez les sources** citees avec chaque reponse
5. L'indicateur de confiance vous dit si la reponse est fiable

## Stack technique

| Composant | Outil |
|-----------|-------|
| Langage | Python 3.11+ |
| Orchestration RAG | LangChain |
| Base vectorielle | ChromaDB (locale, gratuite) |
| LLM | Groq API (Llama 3, gratuit) |
| Embeddings | HuggingFace sentence-transformers (local) |
| Reranking | Cross-encoder ms-marco-MiniLM-L-6-v2 |
| Interface | Streamlit (dark theme BTP) |
| Deploiement | Streamlit Cloud |

## Structure du projet

```
rag-assistant/
├── app.py                 # Point d'entree Streamlit (CSS + auto-ingest)
├── pages/
│   ├── 1_Chat.py          # Interface chat RAG (historique + sources)
│   └── 2_Admin.py         # Panneau admin (clients, docs, prompts)
├── src/
│   ├── config.py          # Configuration centralisee
│   ├── clients.py         # CRUD clients multi-tenant
│   ├── ingest.py          # Ingestion multi-format → ChromaDB
│   └── query.py           # Pipeline RAG (hybride → rerank → LLM)
├── styles/
│   └── main.css           # Design system BTP (dark theme, orange chantier)
├── data/
│   ├── clients.json       # Config clients
│   └── chroma_db/         # Base vectorielle (generee)
├── docs/                  # Documents de demo
└── tests/
    └── compare_chunks.py  # Script de test chunking
```

## Pipeline RAG

```
Question → Reformulation (historique) → Recherche hybride (vectorielle + BM25, corpus complet)
→ Fusion RRF → Reranking adaptatif cross-encoder (TOP_K garanti + seuil confiance)
→ Generation LLM (format fiche chantier) → Nettoyage post-LLM → Reponse + Sources separees
```

## Offre commerciale

3 offres adaptees aux PME BTP :

| | Starter | Pro | Premium |
|---|---|---|---|
| **Setup** | 490 EUR | 990 EUR | 1 990 EUR |
| **Mensuel** | 149 EUR/mois | 249 EUR/mois | 449 EUR/mois |
| Documents | 50 max | 200 max | Illimite |
| Utilisateurs | 3 | 10 | Illimite |
| Support | Email 48h | Email 24h | Email + tel 4h |

Demo gratuite de 15 min sur vos propres documents. Contact : marin@liberte-ia.fr

## Licence

Projet prive — tous droits reserves.
