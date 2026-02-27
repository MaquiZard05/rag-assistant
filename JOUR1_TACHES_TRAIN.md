# 🚂 JOUR 1 — Tâches Train (5h du matin)

## AVANT DE MONTER DANS LE TRAIN (chez toi, avec wifi)
- [ ] Créer le dossier **Liberté/** sur ton ordi avec les sous-dossiers (src/, docs/, demos/, commercial/, notes/)
- [ ] Mettre le fichier RAG_PROJECT_ROADMAP.md dedans
- [ ] Connecter le dossier Liberté à Cowork (ouvrir Claude Desktop > Cowork > pointer vers le dossier)
- [ ] Télécharger Claude Desktop si pas déjà fait (claude.com/download)
- [ ] Vérifier que Python est installé sur ton ordi (`python --version` dans le terminal)
- [ ] Si Python pas installé → le télécharger depuis python.org (prend 2 min)

---

## DANS LE TRAIN — PHASE 1 : Setup (peut se faire offline si tu as déjà Python)

### Étape 1 — Créer l'environnement du projet (5 min)
Ouvre ton terminal, va dans ton dossier :
```bash
cd Liberté/src
python -m venv rag-env
```
Ça crée un environnement Python isolé pour le projet (comme on a fait pour Migration Predictor).

### Étape 2 — Activer l'environnement
```bash
# Sur Mac/Linux :
source rag-env/bin/activate
# Sur Windows :
rag-env\Scripts\activate
```

### Étape 3 — Installer les dépendances (⚠️ nécessite internet)
```bash
pip install langchain langchain-community langchain-openai chromadb openai streamlit pypdf tiktoken
```
> **Si pas d'internet dans le train** : note cette commande et fais-la dès que tu as du réseau. Passe aux étapes offline en attendant.

---

## DANS LE TRAIN — PHASE 2 : Comprendre le RAG (100% offline)

### Étape 4 — Lire et comprendre le flux RAG (20-30 min)
Ouvre la roadmap et relis la section "C'est quoi un RAG". Puis écris dans **notes/jour1.md** avec tes propres mots :
1. C'est quoi un embedding ? (indice : tu connais déjà via Migration Predictor)
2. C'est quoi un chunk ?
3. Pourquoi on ne donne pas le document ENTIER au LLM ?
4. C'est quoi la différence entre "retrieval" et "generation" ?

> **Pourquoi cet exercice ?** Écrire avec tes mots force la compréhension. Si tu galères sur un point, note la question — on la résout ensemble après.

### Étape 5 — Dessiner le pipeline sur papier (10 min)
Prends une feuille ou ton app de notes et dessine le flux :
```
PDF → [Chunking] → [Embedding] → [ChromaDB] → Question → [Recherche] → [LLM] → Réponse sourcée
```
Pour chaque étape, note UNE phrase qui explique ce qui se passe.

### Étape 6 — Trouver 3-4 documents de test (15 min)
Cherche sur ton ordi ou télécharge des PDFs qui serviront de test :
- Un PDF de procédure interne (n'importe quoi, même un mode d'emploi)
- Un FAQ en PDF
- Un document technique (si tu as des DTU ou CCTP de ton ancien job, c'est parfait)
- Range-les dans **docs/**

> **Astuce** : Si t'as rien sous la main, des CGV, un règlement intérieur, un guide utilisateur d'un logiciel — tout marche.

---

## DANS LE TRAIN — PHASE 3 : Préparer le code (offline, avec Claude Code)

### Étape 7 — Ouvrir Claude Code et préparer le CLAUDE.md du projet (10 min)
Crée un fichier **CLAUDE.md** à la racine de Liberté/ avec ce contenu :
```markdown
# Projet RAG — Assistant IA sur Documents

## Objectif
Système RAG vendable : upload de documents → questions en langage naturel → réponses sourcées.

## Stack
- Python 3.11+
- LangChain (orchestration RAG)
- ChromaDB (vector store local)
- OpenAI API (embeddings + LLM)
- Streamlit (interface web)

## Structure
- src/ → code Python
- docs/ → documents de test
- demos/ → captures et vidéos
- commercial/ → supports de vente
- notes/ → bilans quotidiens

## Règles
- Code simple et commenté (je suis débutant, je dois comprendre chaque ligne)
- Pas de sur-ingénierie : on veut un MVP qui fonctionne
- Chaque fonction doit avoir un commentaire qui explique ce qu'elle fait en langage simple
```

### Étape 8 — Configurer Cowork pour le projet (5 min)
Dans Cowork, ajoute ces **instructions globales** (Settings > Cowork > Global Instructions) :
```
Je travaille sur un projet RAG (assistant IA sur documents) pour du freelance.
Je suis débutant en tech. Explique-moi simplement.
Mon dossier de travail est Liberté/.
Aide-moi à organiser mes fichiers, ma documentation et mes supports commerciaux.
Ne touche pas au code — c'est Claude Code qui s'en charge.
```

---

## QUAND TU AS INTERNET — PHASE 4 : Premier code

### Étape 9 — Demander à Claude Code de construire le premier script (30-45 min)
Une fois les dépendances installées, ouvre Claude Code dans ton dossier src/ et demande-lui :

> "Crée-moi un script Python simple (ingest.py) qui :
> 1. Charge tous les PDFs du dossier ../docs/
> 2. Les découpe en chunks de 1000 caractères avec 200 de overlap
> 3. Transforme chaque chunk en embedding avec OpenAI
> 4. Stocke tout dans une base ChromaDB locale
> 
> Commente chaque ligne, je suis débutant. Explique ce que fait chaque étape."

### Étape 10 — Demander le script de query
Ensuite demande :

> "Crée-moi un script query.py qui :
> 1. Prend une question en entrée
> 2. La transforme en embedding
> 3. Cherche les 3 chunks les plus proches dans ChromaDB
> 4. Envoie la question + ces chunks à GPT-4o-mini pour générer une réponse
> 5. Affiche la réponse avec les sources (nom du fichier, numéro de page)
>
> Commente chaque ligne, je suis débutant."

### Étape 11 — Tester ! 🎯
```bash
# D'abord ingérer tes documents
python ingest.py

# Puis poser une question
python query.py "Quelle est la procédure pour X ?"
```

**Si ça marche → CHECKPOINT JOUR 1 MATIN ✅**
Tu as un RAG fonctionnel. Prends une capture d'écran et mets-la dans demos/.

---

## 📝 BILAN DU SOIR (à remplir dans notes/jour1.md)
```
✅ Fait :
❌ Pas fait :
🚧 Bloqué sur :
💡 Questions pour demain :
```

---

## ⚠️ RAPPELS
- Bloqué > 30 min ? → Demande à Claude Code immédiatement
- Pas besoin que ce soit parfait. Il faut que ça FONCTIONNE.
- Tu auras besoin d'une clé API OpenAI (https://platform.openai.com/api-keys) — si t'en as pas, crée un compte ce soir avant de dormir. Ça coûte quasi rien pour commencer (quelques centimes par test).

*Bonne nuit Marin, demain tu construis ton premier produit IA vendable.* 🚀
