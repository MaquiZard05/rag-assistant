# 🎯 ROADMAP RAG — Projet Freelance IA (5 Jours)

## Contexte Projet
**Objectif** : Construire un système RAG vendable pour PME/TPE, agences et cabinets.  
**Pitch** : "Un assistant IA qui répond aux questions de vos équipes en s'appuyant sur vos propres documents."  
**Stack** : Python + LangChain + ChromaDB + OpenAI/Claude API + Streamlit  
**Outils de travail** : Claude Code (pour coder) + Cowork (pour organiser, gérer les fichiers, automatiser les tâches non-code)  
**Profil** : Débutant tech, apprentissage par la pratique. Chaque étape inclut une explication pédagogique.

---

## 🧠 C'est quoi un RAG ? (Explication pour Marin)

**Analogie simple** : Imagine une bibliothécaire ultra-rapide. Tu lui donnes 200 documents. Quand quelqu'un pose une question, elle ne lit pas tout — elle sait exactement dans quel tiroir chercher, elle ouvre la bonne page, et elle formule une réponse claire avec la source.

**En technique** :
1. **Ingestion** → Tu donnes des documents (PDF, Word, etc.) au système
2. **Chunking** → Le système découpe les documents en morceaux digestes (comme des fiches)
3. **Embedding** → Chaque morceau est transformé en vecteur (un code numérique qui capture le SENS du texte — tu connais déjà ce concept avec Migration Predictor et les embeddings !)
4. **Stockage** → Ces vecteurs sont rangés dans une base vectorielle (ChromaDB = le tiroir de la bibliothécaire)
5. **Retrieval** → Quand l'utilisateur pose une question, on transforme sa question en vecteur et on cherche les morceaux les plus proches
6. **Generation** → On envoie la question + les morceaux trouvés au LLM (Claude ou GPT) qui formule une réponse sourcée

**Comparaison avec Migration Predictor** : Dans ton projet trading, tu utilises des embeddings pour représenter le comportement des tokens. Ici c'est pareil, sauf qu'au lieu de représenter des tokens Solana, on représente des morceaux de texte. Le principe mathématique est identique — proximité dans l'espace vectoriel = similarité de sens.

---

## 📅 PLANNING 5 JOURS

---

### JOUR 1 (Jeudi) — FONDATIONS + PREMIER PIPELINE ✅ TERMINÉ

**Matin (9h-12h) — Comprendre et installer**
- [x] Installer l'environnement Python (venv dédié au projet RAG)
- [x] Installer les dépendances : `langchain`, `chromadb`, `sentence-transformers`, `streamlit`, `pypdf`
- [x] Comprendre le flux : Document → Chunks → Embeddings → Vector Store → Query → Réponse
- [x] **Mini-exercice** : charger UN seul PDF et faire une query dessus en 20 lignes de code

**Après-midi (14h-18h) — Pipeline complet basique**
- [x] Construire le script d'ingestion (`src/ingest.py` — charge 5 PDFs, découpe en 33 chunks, stocke dans ChromaDB)
- [x] Construire le script de query (`src/query.py` — question → retrieval top 5 → réponse Groq sourcée)
- [x] Tester avec 5 documents exemples Duval & Associés (QSE, RH, FAQ, Chantier, Catalogue)
- [x] **Checkpoint** : Pipeline fonctionnel, réponses sourcées avec fichier + page ✅

**Soirée (20h-22h) — Nettoyage technique**
- [x] Suppression des fichiers templates vides (ingestion.py, retriever.py, chain.py, utils.py)
- [x] Structure src/ propre : config.py + ingest.py + query.py
- [x] Dépendances stabilisées

**🎓 Ce que tu apprends Jour 1** : Comment un document devient des vecteurs, comment la similarité vectorielle fonctionne (cosine similarity — comme dans ton projet trading), ce qu'est un "chunk" et pourquoi la taille compte.

---

### JOUR 2 (Vendredi) — QUALITÉ + INTERFACE ✅ TERMINÉ

**Matin (9h-12h) — Améliorer la qualité des réponses**
- [x] Implémenter le chunking intelligent (overlap entre les morceaux pour ne pas perdre le contexte)
- [x] Ajouter les métadonnées (nom du fichier source, numéro de page) aux chunks
- [x] Tester différentes tailles de chunks (500 vs 1000 vs 1500 tokens) — 500/100 gagne
- [x] Implémenter l'affichage des sources dans les réponses ("Source : document X, page Y")

**Après-midi (14h-18h) — Interface Streamlit**
- [x] Créer l'interface utilisateur avec Streamlit :
  - Zone d'upload de documents (drag & drop)
  - Barre de chat pour poser des questions
  - Affichage des réponses avec sources cliquables
  - Indicateur de confiance (nombre de sources trouvées)
- [x] Styler un minimum l'interface (logo, couleurs, titre professionnel)

**Soirée (20h-22h) — Tests et itération**
- [x] Tester avec différents types de documents (PDF texte)
- [x] Identifier et corriger les cas où les réponses sont mauvaises — optimisation chunk 500/100
- [x] Documenter les limites actuelles

**🎓 Ce que tu apprends Jour 2** : Pourquoi l'overlap dans le chunking améliore les résultats, comment Streamlit fonctionne (framework Python pour créer des apps web rapidement), comment un LLM utilise le "contexte" qu'on lui fournit.

---

### JOUR 3 (Samedi) — FEATURES PRO + MULTI-TENANT ✅ TERMINÉ

**Matin (9h-12h) — Fonctionnalités avancées**
- [x] Ajouter la gestion multi-collections (= multi-clients : chaque client a sa propre base de docs)
- [x] Implémenter la conversation avec historique (reformulation de question via LLM)
- [x] Ajouter un système de "system prompt" personnalisable par client (ton de réponse, langue, spécialité)

**Après-midi (14h-18h) — Robustesse**
- [x] Gérer les erreurs proprement (document corrompu, API timeout, etc.)
- [x] Ajouter un panneau admin : dashboard + gestion clients + documents + system prompts
- [x] Optimiser la qualite (reranking cross-encoder, contextual chunk headers)
- [x] Architecture multi-pages Streamlit + CSS pro externe

**Soirée (20h-22h) — Documentation technique**
- [x] README a jour
- [x] Design doc sauvegarde dans docs/plans/

**🎓 Ce que tu apprends Jour 3** : Ce qu'est le multi-tenant (= un système qui sert plusieurs clients isolés les uns des autres), comment gérer la mémoire conversationnelle, comment optimiser les coûts API en production.

---

### JOUR 4 (Dimanche) — DÉPLOIEMENT + DÉMO

**Matin (9h-12h) — Déploiement**
- [ ] Déployer sur ton VPS ou sur Streamlit Cloud (gratuit)
- [ ] Configurer un sous-domaine propre si possible
- [ ] Tester l'accès externe (quelqu'un d'autre peut y accéder)
- [ ] Sécuriser : authentification basique, rate limiting

**Après-midi (14h-18h) — Créer la démo vendable**
- [ ] Charger un jeu de données démo convaincant (ex : FAQ d'une entreprise fictive, ou docs BTP si tu en as)
- [ ] Préparer 5-6 questions types qui montrent la puissance du système
- [ ] Enregistrer une démo Loom de 2-3 minutes MAX :
  - 30s : le problème ("vos équipes perdent X heures à chercher dans les docs")
  - 60s : la démo live (upload + questions + réponses sourcées)
  - 30s : le résultat ("réponses instantanées, sourcées, sur VOS données")
- [ ] Créer une version GIF courte pour les messages de prospection

**Soirée (20h-22h) — GitHub + Portfolio**
- [ ] Push le code propre sur GitHub (repo public)
- [ ] Écrire une description de projet vendeuse dans le README
- [ ] Préparer 2-3 screenshots professionnels

**🎓 Ce que tu apprends Jour 4** : Comment déployer une app Python en production, les bases de la sécurité web (auth, rate limiting), comment créer une démo qui vend (pas une démo technique, une démo orientée problème/solution).

---

### JOUR 5 (Lundi) — PACKAGING COMMERCIAL + LANCEMENT OUTREACH

**Matin (9h-12h) — Offre commerciale**
- [ ] Définir ton offre :
  - **Offre Starter** (500-800€) : RAG sur vos docs, interface chat, 1 collection, setup inclus
  - **Offre Pro** (1000-1500€) : Multi-collections, personnalisation, formation équipe, support 1 mois
  - **Abonnement maintenance** (200-300€/mois) : Mises à jour, ajout de docs, support
- [ ] Rédiger un one-pager commercial (PDF propre)
- [ ] Préparer 3 templates de messages de prospection (email froid, message LinkedIn, DM Twitter)

**Après-midi (14h-18h) — Premier outreach**
- [ ] Identifier 20 prospects (agences, cabinets conseil, PME tech)
- [ ] Envoyer les 10 premiers messages personnalisés
- [ ] S'inscrire sur Malt, Upwork, et/ou Fiverr avec ton offre RAG
- [ ] Poster dans des communautés tech (Discord IA, Reddit, forums freelance)

**Soirée (20h-22h) — Bilan et suite**
- [ ] Faire le bilan des 5 jours
- [ ] Documenter ce qui a marché et ce qui doit être amélioré
- [ ] Planifier la Semaine 2 (Email Automation + suite de la prospection)

**🎓 Ce que tu apprends Jour 5** : Comment packager une compétence technique en offre commerciale, comment pricer un service IA, les bases de la prospection freelance tech.

---

## 🛠️ STACK TECHNIQUE DÉTAILLÉE

| Composant | Outil | Pourquoi |
|-----------|-------|----------|
| Langage | Python 3.11+ | Tu le connais déjà via Migration Predictor |
| Orchestration RAG | LangChain | Framework le plus utilisé, documentation massive, facilite tout le pipeline |
| Vector Store | ChromaDB | Simple à installer, fonctionne en local, gratuit, parfait pour commencer |
| LLM | OpenAI GPT-4o-mini ou Claude API | Bon rapport qualité/prix pour la génération |
| Embeddings | OpenAI text-embedding-3-small | Pas cher (0.02$/1M tokens), performant |
| Interface | Streamlit | Framework Python pour apps web, zéro HTML/CSS nécessaire |
| Déploiement | Streamlit Cloud ou VPS (Nuremberg) | Tu as déjà un VPS, autant l'utiliser |

---

## 🔧 UTILISATION DE COWORK

**Ce que Cowork va faire pour toi sur ce projet :**
- Organiser tes fichiers projet automatiquement (docs/, src/, demos/)
- Générer et mettre à jour ta documentation
- Préparer tes templates de prospection
- Gérer tes tâches quotidiennes (si connecteur agenda dispo)
- Faire des recherches web pour trouver des prospects
- Créer tes supports commerciaux (one-pager, présentations)

**Ce que Claude Code va faire :**
- Écrire le code du RAG
- Debugger
- Déployer
- Gérer le repo GitHub

**Règle simple** : Si ça touche au code → Claude Code. Si ça touche à l'organisation, la doc, ou les fichiers non-code → Cowork.

---

## ⚠️ RÈGLES ANTI-DISPERSION (pour Marin)

1. **PAS de nouvelle idée pendant ces 5 jours.** L'outil BTP, le CRM, les autres projets — tout est noté et REPORTÉ à la semaine 2+.
2. **1 jour = 1 objectif.** Si c'est pas fini, tu continues. Tu ne passes PAS au jour suivant sans le checkpoint ✅.
3. **Bloqué > 30 minutes ?** Tu demandes à Claude Code immédiatement. Pas de spirale de recherche Google.
4. **Chaque soir** : Tu fais le point en 3 lignes (fait / pas fait / bloqué sur).
5. **Le code n'a pas besoin d'être parfait.** Il a besoin de FONCTIONNER et d'être MONTRABLE.

---

## 📊 MÉTRIQUES DE SUCCÈS

| Jour | Métrique |
|------|----------|
| J1 | Pipeline fonctionnel : question → réponse sourcée ✅ |
| J2 | Interface Streamlit utilisable par un non-tech ✅ |
| J3 | Multi-client + historique de conversation ✅ |
| J4 | App déployée + démo Loom enregistrée ✅ |
| J5 | Offre commerciale prête + 10 premiers messages envoyés ✅ |

---

## 💡 IDÉES PARKÉES (à reprendre après)

- RAG spécialisé BTP (DTU, CCTP, CCAP) — niche premium
- Outil d'analyse d'appels d'offres BTP (produit long terme)
- Intégration CRM + IA automation
- Email Automation (Semaine 2 du plan 30 jours)

---

*Document généré le 26/02/2026 — Projet RAG Freelance IA*
*À utiliser avec Claude Code + Cowork pour l'exécution*
