# RAG Assistant — Assistant IA sur vos documents

Un assistant IA qui répond aux questions de vos équipes en s'appuyant sur vos propres documents.

## Fonctionnalités

- Upload de documents (PDF, TXT)
- Recherche intelligente dans vos documents
- Réponses en langage naturel avec sources citées
- Interface web simple et intuitive

## Installation

```bash
# Cloner le repo
git clone https://github.com/MaquiZard05/rag-assistant.git
cd rag-assistant

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` à la racine du projet :

```
GROQ_API_KEY=votre_clé_groq
```

## Lancement

```bash
streamlit run app.py
```

## Stack technique

- **Python** + **LangChain** (orchestration RAG)
- **ChromaDB** (base vectorielle locale)
- **Groq API** (LLM — Llama 3 / Mixtral)
- **HuggingFace sentence-transformers** (embeddings)
- **Streamlit** (interface web)
