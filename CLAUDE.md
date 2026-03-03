# CLAUDE.md — Projet RAG Freelance IA

## Identité
Tu travailles avec Marin sur un projet RAG (Retrieval-Augmented Generation) vendable en freelance.
Marin est un non-développeur qui apprend par la pratique (vibe coding). Il a de l'expérience avec Python via son projet Migration Predictor (XGBoost, embeddings, MLP) mais c'est son premier projet web/IA orienté client.

## Objectif du Projet
Construire un **Assistant conformite chantier BTP** verticalisé, vendable en freelance.
Pitch : "Vos equipes terrain posent une question → reponse sourcee en 3 secondes avec le DTU, la page, et le score de fiabilite."
Cible : PME BTP, conducteurs de travaux, chefs de chantier, dirigeants.
Le produit doit être FONCTIONNEL et MONTRABLE. Pas parfait — vendable.

## Stack Technique (NE PAS CHANGER SANS DEMANDER)
- **Langage** : Python 3.11+
- **Orchestration RAG** : LangChain
- **Vector Store** : ChromaDB
- **LLM** : Groq API (gratuit) — Llama 3 ou Mixtral
- **Embeddings** : HuggingFace sentence-transformers en local (gratuit, pas d'API nécessaire)
- **Interface** : Streamlit
- **Déploiement** : Streamlit Cloud (gratuit) — nécessite un repo GitHub public lié

> ⚠️ Ne propose JAMAIS de changer de lib ou d'outil (ex: passer à Pinecone, FAISS, FastAPI, etc.) sans que Marin le demande explicitement. On reste sur cette stack.

## Structure du Projet
```
rag-assistant/
├── CLAUDE.md              # Ce fichier
├── README.md              # Documentation publique (GitHub)
├── requirements.txt       # Dépendances Python
├── .env                   # Clés API (jamais commit)
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration centralisée (modèles, params, chemins)
│   ├── clients.py         # CRUD clients multi-tenant
│   ├── ingest.py          # Ingestion (PDFs → chunks + headers → ChromaDB)
│   └── query.py           # Pipeline RAG (historique → hybride → rerank → LLM)
├── app.py                 # Point d'entrée Streamlit (CSS + redirect)
├── pages/
│   ├── 1_Chat.py           # Interface RAG (chat + upload + historique)
│   └── 2_Admin.py          # Panneau admin (clients, docs, prompts)
├── styles/
│   └── main.css           # Design system BTP (dark theme, orange chantier)
├── data/
│   ├── clients.json       # Config clients (Thermex BTP + Pulse Digital)
│   └── chroma_db/         # Base vectorielle ChromaDB (persistante)
├── tests/
│   ├── compare_chunks.py  # Script de test chunking
│   └── test_categories.py # Tests filtrage par categorie BTP (pytest)
└── docs/
    └── *.pdf              # 6 PDFs demo BTP (DTU, CCTP, QSE, Fiches, DOE, Memo)
```

## Conventions de Code

### Langue
- **Noms de variables, fonctions, classes** : anglais
- **Commentaires dans le code** : français
- **Docstrings** : français
- **Messages utilisateur (Streamlit)** : français (on vend à des PME françaises)
- **README GitHub** : français
- **Commits** : français, format court ("ajout ingestion PDF", "fix chunking overlap")

### Style
- Code SIMPLE et LISIBLE. Pas d'abstraction inutile.
- Une fonction = une responsabilité claire.
- Pas de classes si une fonction suffit.
- Pas de design patterns complexes (factory, singleton, etc.) sauf nécessité absolue.
- Noms de variables explicites (`chunk_size`, pas `cs`).
- Imports en haut du fichier, groupés (stdlib / third-party / local).

### Gestion d'erreurs
- Try/except autour des appels API (OpenAI, Claude).
- Messages d'erreur clairs en français dans l'interface Streamlit.
- Logging basique avec `print()` pour le debug (pas besoin de logging lib complexe pour l'instant).

## Comportement Attendu de Claude Code

### Par défaut
- **Code directement**, sans longues explications préalables.
- Quand tu crées ou modifies un fichier, montre uniquement les parties modifiées sauf si Marin demande le fichier complet.
- Teste ton code mentalement avant de le proposer. Si un import manque ou une variable n'existe pas, corrige AVANT.
- Propose des checkpoints réguliers ("ça marche, on peut tester — tu veux passer à la suite ?").

### Mode pédagogique (SEULEMENT si Marin demande)
- Si Marin dit "explique", "c'est quoi", "pourquoi", "je comprends pas" → passe en mode pédagogique.
- Utilise des analogies simples. Relie les concepts à ce qu'il connaît déjà (Migration Predictor, embeddings, XGBoost).
- Sinon, reste concis et orienté action.

### Après chaque grande action (OBLIGATOIRE)
Après chaque bloc de travail significatif (feature, fix, audit, etc.) :
1. **Commit + push** automatiquement (sans attendre que Marin le demande)
2. **Mettre à jour CLAUDE.md** (roadmap, structure si changée)
3. **Mettre à jour le README** si le comportement utilisateur change

### Anti-patterns (NE PAS FAIRE)
- ❌ Ne pas ajouter de features hors de la roadmap du jour en cours.
- ❌ Ne pas sur-ingénierer (pas de microservices, pas de Docker pour l'instant, pas de CI/CD).
- ❌ Ne pas proposer des alternatives de stack sans qu'on te le demande.
- ❌ Ne pas écrire de longs paragraphes d'explication quand Marin veut juste du code.
- ❌ Ne pas refactorer du code qui fonctionne sauf si Marin le demande.
- ❌ Ne pas créer des fichiers inutiles (pas de config YAML, pas de Makefile, pas de docker-compose).

## Roadmap (Référence Rapide)
- **Jour 1** : Pipeline fonctionnel (ingestion → query → réponse sourcée) ✅ TERMINÉ
  - config.py + ingest.py + query.py fonctionnels
  - 5 PDFs démo ingérés (33 chunks dans ChromaDB)
  - Embeddings : sentence-transformers all-MiniLM-L6-v2 (local)
  - LLM : Groq API (llama-3.1-8b-instant)
  - Nettoyage technique fait (fichiers vides supprimés, dépendances OK)
- **Jour 2** : Qualité des réponses + interface Streamlit ✅ TERMINÉ
  - Chunking optimisé : 500/100 au lieu de 1000/200 (test scientifique via compare_chunks.py)
  - 62 chunks au lieu de 33 — meilleure granularité de recherche
  - app.py Streamlit : interface pro, upload PDF immédiat, chat, sources, indicateur de confiance
  - Refactoring : ingest_single_pdf() + ask() pour réutilisation
  - Script de comparaison tests/compare_chunks.py
- **Jour 3** : Multi-tenant + historique conversation + admin ✅ TERMINÉ
  - Architecture multi-pages : app.py + pages/1_Chat.py + pages/2_Admin.py
  - CSS externe pro : styles/main.css (palette bleu corporate)
  - Multi-client : clients.json + collection ChromaDB par client + selecteur sidebar
  - Historique conversation : reformulation de question via LLM avant retrieval
  - System prompt personnalisable par client
  - Panneau admin : dashboard metrics + CRUD clients + gestion docs + edit prompts
  - Reranking cross-encoder (ms-marco-MiniLM-L-6-v2) post-retrieval
  - Contextual Chunk Headers (source + page injectes dans le chunk avant embedding)
  - Gestion erreurs : timeout Groq, validation PDF, messages clairs
- **Jour 4** : Déploiement + multi-format + demo + audit ✅ TERMINÉ
  - Déploiement Streamlit Cloud (st.secrets, auto-ingest, config.toml)
  - Ingestion multi-format : PDF, TXT, DOCX, HTML (loaders LangChain)
  - Interface chat style ChatGPT : sidebar visible, navigation, sélecteur client
  - Cache embeddings (singleton) + accès ChromaDB direct pour stats (navigation instantanée)
  - Pool hybride search x4 pour reranking (remplace par corpus complet au Jour 5)
  - 2 clients demo : Duval BTP (5 docs, 62 chunks) + Pulse Digital (5 docs, 533 chunks)
  - Audit complet J+4 : scorecard C+, 4 correctifs immédiats appliqués
  - Fix sécurité : XSS (html.escape), exceptions loguées, page fallback non-PDF
  - 8 corrections design : renommage pages sans emojis, DM Sans, masquage nav Streamlit, curseur pointer, sidebar-doc-name
  - Emojis UI remplaces par icones Material/SVG
- **Jour 5** : Pivot BTP + packaging commercial ⬅️ EN COURS
  - Verticalisation "Assistant conformite chantier BTP"
  - Dark theme industrie : #1A1B1E, accent orange #E8A23A, Source Sans 3 + JetBrains Mono
  - Sidebar BTP : logo, categories chantier (Normes, CCTP, QSE, Fiches tech, DOE, Admin)
  - 6 questions suggerees BTP sur ecran d'accueil
  - 6 PDFs BTP demo : DTU, CCTP, QSE, Fiches tech, DOE, Memo (89 chunks)
  - **Retrieval** :
    - Recherche pre-filtree : vector(top_k*4) + BM25(top_k*4) au lieu de corpus complet
    - Reranking adaptatif : TOP_K=5 garanti + chunks au-dela si score >= 2.0, max 10
    - Seuil de pertinence MIN_RELEVANCE_SCORE=0.3 (pas de LLM si rien pertinent)
  - **Format reponses "fiche chantier"** :
    - System prompt : titre emoji, sections, cle:valeur en gras, point de vigilance
    - build_context() envoie le contenu brut (plus de marqueurs [Source X])
    - clean_response() : regex post-LLM pour supprimer tout [Source X] residuel
    - Sources affichees separement sous la reponse (Markdown pur, indicateur pertinence)
  - 3/3 tests format valides (delais CCTP, accident chantier, Knauf TH38)
  - **Filtrage par categorie BTP** :
    - `CATEGORY_FILTERS` dans query.py : 6 categories (normes→DTU, cctp→CCTP, qse→QSE, fiches→Fiches, doe→DOE, admin→Memo)
    - `hybrid_search()` + `ask()` acceptent `category: str | None` pour filtrer par type de document
    - Boutons sidebar fonctionnels : toggle on/off, distinction visuelle (type="primary")
    - 10/10 tests pytest (test_categories.py) : filtrage par categorie, multi-source, edge cases
  - **Audit J+5 complet (agent team : security + performance + ux-review)** :
    - Score avant corrections : D+ (4/10) — 28 findings (6 critiques, 7 hauts, 12 moyens, 5 bas)
    - Top 5 corrections appliquees :
      1. Pre-filtrage reranker : candidate_pool = top_k*4 au lieu de corpus complet (-80% latence)
      2. Mot de passe Admin (ADMIN_PASSWORD via env/secrets)
      3. Validation regex client_id + sanitisation filenames
      4. Jargon retire du header ("Recherche intelligente dans vos documents")
      5. Limite upload 50 MB
    - "chunks" renomme "sections" dans toute l'interface admin
    - Score apres corrections : B- (6-7/10)
    - Rapports detailles dans notes/audit/ (security.md, performance.md, ux-review.md, RAPPORT_AUDIT.md)

> Quand Marin dit "on est au jour X", applique les objectifs de ce jour. Ne propose pas de tâches du jour suivant.

## Variables d'Environnement Requises (.env)
```
GROQ_API_KEY=gsk_...
```

## Commandes Utiles
```bash
# Activer l'environnement
source venv/bin/activate

# Ingestion des PDFs
python src/ingest.py

# Poser une question (interactif ou en argument)
python src/query.py
python src/query.py "Ta question ici"

# Lancer l'app Streamlit (Jour 2+)
streamlit run app.py

# Installer les dépendances
pip install -r requirements.txt
```

## Contexte Business
- **Budget projet : 0€.** Tout doit être gratuit (API, hébergement, outils). Ce projet est un POC / proof of work pour décrocher des missions payantes.
- Cible : PME BTP françaises (conducteurs de travaux, chefs de chantier, dirigeants).
- Le produit doit être compréhensible par un non-tech en 30 secondes.
- Les démos doivent montrer : upload de doc → question → réponse sourcée.
- Prix visé pour les futures missions clients : 500-1500€ la mise en place + 200-300€/mois de maintenance.
- Quand un client paiera, on pourra upgrader vers GPT-4o ou Claude — mais le POC tourne 100% gratuit.

## Notes Importantes
- Le projet est développé en local sur un environnement Linux.
- **Repo GitHub** : git@github.com:MaquiZard05/rag-assistant.git
- Déploiement via Streamlit Cloud → lié au repo GitHub ci-dessus.
- Marin utilise Claude Code en terminal pour coder, pas un IDE classique.
- Le code doit rester déployable à tout moment (pas de WIP cassé sur main).
- Chaque fin de session : résumer ce qui a été fait et ce qui reste.
