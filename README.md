# RAG Assistant — Assistant Documentaire IA

Un assistant IA qui repond aux questions de vos equipes en s'appuyant sur vos propres documents.

## Fonctionnalites

- **Upload de documents PDF** avec indexation automatique (drag & drop)
- **Recherche intelligente** dans vos documents (base vectorielle ChromaDB)
- **Reponses sourcees** avec nom du fichier et numero de page
- **Indicateur de confiance** (nombre de sources trouvees)
- **Interface web professionnelle** avec Streamlit
- **Chunking optimise** (500 tokens, overlap 100 — teste scientifiquement)

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

# Indexer les documents (premiere fois ou apres ajout de PDFs dans docs/)
python src/ingest.py

# Lancer l'interface web
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

## Utilisation

1. **Deposez vos PDFs** dans la sidebar (indexation automatique)
2. **Posez vos questions** dans la barre de chat
3. **Consultez les sources** citees avec chaque reponse
4. L'indicateur de confiance vous dit si la reponse est fiable

## Stack technique

| Composant | Outil |
|-----------|-------|
| Langage | Python 3.11+ |
| Orchestration RAG | LangChain |
| Base vectorielle | ChromaDB (locale, gratuite) |
| LLM | Groq API (Llama 3, gratuit) |
| Embeddings | HuggingFace sentence-transformers (local) |
| Interface | Streamlit |

## Structure du projet

```
rag-assistant/
├── app.py                 # Interface Streamlit
├── src/
│   ├── config.py          # Configuration centralisee
│   ├── ingest.py          # Ingestion PDFs → ChromaDB
│   └── query.py           # Pipeline RAG (question → reponse)
├── docs/                  # PDFs a indexer
├── data/chroma_db/        # Base vectorielle (generee)
└── tests/
    └── compare_chunks.py  # Script de comparaison de tailles de chunks
```

## Licence

Projet prive — tous droits reserves.
