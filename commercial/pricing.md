# Grille Tarifaire — Assistant Conformité Chantier BTP

> Document stratégique — Mars 2026
> Produit : Assistant IA RAG pour la conformité chantier (DTU, CCTP, QSE, fiches techniques)

---

## 1. Analyse du marché

### 1.1 Marché des solutions IA/RAG pour PME en France

Le marché français des services d'IA est évalué à **1,8 milliard d'euros** en 2024 (+5% de croissance). La technologie RAG (Retrieval-Augmented Generation) se démocratise rapidement avec des guides publiés par la DGE et France Num pour accompagner les PME.

**Prix constatés pour un assistant IA/RAG sur mesure :**

| Type de solution | Fourchette de prix |
|---|---|
| Chatbot basique (FAQ, scripts) | 1 000 — 5 000 € |
| Chatbot IA avancé (RAG, NLP, intégrations) | 10 000 — 30 000 € |
| Agent IA support client / RH | 15 000 — 30 000 € |
| Agent IA connecté CRM + automatisation | 20 000 — 80 000 € |
| SaaS documentaire IA (Dust.tt) | 29 €/utilisateur/mois (Pro) |

Sources : Codeur.com, Digital Unicorn, Plateya, AIR Agent, Dust.tt

### 1.2 Tarifs freelance IA en France (2025-2026)

| Profil | TJM moyen |
|---|---|
| Développeur IA junior | 350 — 500 €/jour |
| Consultant IA confirmé | 600 — 900 €/jour |
| Expert IA / ML senior | 900 — 1 500 €/jour |
| Chef de projet IA | 500 — 800 €/jour |

**Observation clé** : un projet de chatbot IA sur mesure facturé par une agence ou un freelance senior représente typiquement **5 à 15 jours de travail**, soit **3 000 à 13 500 €** de prestation.

### 1.3 Concurrence SaaS directe

| Solution | Positionnement | Prix |
|---|---|---|
| **Dust.tt** | Agents IA collaboratifs (généraliste) | 29 €/user/mois |
| **Botnation AI** | Chatbot no-code | 39 — 449 €/mois |
| **Custom GPT (OpenAI)** | RAG simple, limité | 20 $/user/mois (ChatGPT Plus) |
| **Notion AI** | Assistant intégré Notion | 10 €/user/mois |
| **Kizeo Forms** | Formulaires terrain BTP/QSE | 12 — 30 €/user/mois |
| **Novade** | Gestion QHSE chantier | Sur devis (>200 €/mois) |

**Notre avantage concurrentiel** : aucune de ces solutions ne combine RAG documentaire spécialisé BTP + conformité DTU/CCTP + déploiement clé en main pour PME. Nous occupons une niche non adressée.

### 1.4 Spécificités du marché BTP

- **Maturité numérique** : 80% des PME françaises ont entamé une digitalisation, mais le BTP reste en retard sur les usages avancés (IA, automatisation)
- **Budget IT** : 42% des PME ont investi plus de 1 000 € dans le numérique en 2024 — budgets modestes mais en croissance
- **Aides disponibles** : Chèque Numérique France Num (jusqu'à 15 000 €), plan Bpifrance 10 Md€ pour l'IA dans les PME
- **Douleur conformité** : les pénalités de non-conformité DTU vont de 0,1 à 0,5% par jour de retard. Les amendes peuvent atteindre **150 000 à 375 000 €**. L'URSSAF a redressé le BTP à hauteur de **877 M€ en 2024**
- **Coût des sinistres** : une malfaçon non détectée coûte en moyenne **plusieurs dizaines de milliers d'euros** en réparation, sans compter la perte de réputation et les exclusions d'assurance décennale

---

## 2. Grille Tarifaire — 3 Offres

### Philosophie de pricing

Notre positionnement : **10x moins cher qu'une agence, 10x plus spécialisé qu'un SaaS généraliste.** On se positionne entre le Custom GPT à 20 €/mois (trop limité) et l'agent IA sur mesure à 15 000 € (trop cher pour une PME BTP).

---

### STARTER — "Découverte IA"

> Pour les petites entreprises BTP qui veulent tester l'IA documentaire sans engagement lourd.

| | Détail |
|---|---|
| **Setup (une fois)** | **490 €** |
| **Abonnement mensuel** | **149 €/mois** |
| **Engagement** | 3 mois minimum |

**Inclus :**
- Intégration de **50 documents max** (DTU, CCTP, fiches techniques)
- **3 utilisateurs** inclus
- Assistant IA accessible via navigateur (Streamlit)
- Recherche hybride (sémantique + mots-clés)
- Réponses sourcées avec références aux documents
- Support par email (réponse sous 48h)
- 1 session de formation à distance (1h)

**Non inclus :**
- Mise à jour des documents après setup (facturée 50 €/lot)
- Personnalisation de l'interface
- Intégrations tierces (API, webhook)
- Support prioritaire

**Coût réel pour Marin :**
- Setup : ~3h de travail (ingestion docs + configuration) = ~163 €/h
- Mensuel : ~1h/mois de maintenance = ~149 €/h
- **Marge nette estimée : ~80%** (hors coûts API Groq, hébergement minimal)

---

### PRO — "Conformité Terrain" (RECOMMANDEE)

> L'offre principale pour les PME BTP qui veulent sécuriser leur conformité chantier au quotidien.

| | Détail |
|---|---|
| **Setup (une fois)** | **990 €** |
| **Abonnement mensuel** | **249 €/mois** |
| **Engagement** | 6 mois minimum |

**Inclus :**
- Intégration de **200 documents max** (DTU, CCTP, plans QSE, PPSPS, fiches techniques, DOE)
- **10 utilisateurs** inclus
- Assistant IA accessible via navigateur
- Recherche hybride avancée (sémantique + BM25 + filtres par catégorie)
- Réponses sourcées avec page et paragraphe exact
- **1 mise à jour documentaire/mois** incluse (ajout/remplacement de documents)
- Support par email prioritaire (réponse sous 24h)
- 2 sessions de formation à distance (1h chacune)
- Tableau de bord d'usage (nombre de requêtes, documents les plus consultés)
- Configuration personnalisée par projet/chantier

**Non inclus :**
- Intégrations API externes
- Personnalisation graphique avancée
- Utilisateurs supplémentaires (25 €/user/mois)
- Formation sur site

**Coût réel pour Marin :**
- Setup : ~6h de travail (ingestion volumineuse + configuration multi-projets) = ~165 €/h
- Mensuel : ~2h/mois (maintenance + 1 mise à jour docs) = ~125 €/h
- **Marge nette estimée : ~75%**

---

### PREMIUM — "Pilotage Complet"

> Pour les PME structurées qui veulent un assistant IA intégré à leur processus qualité avec un suivi dédié.

| | Détail |
|---|---|
| **Setup (une fois)** | **1 990 €** |
| **Abonnement mensuel** | **449 €/mois** |
| **Engagement** | 12 mois |

**Inclus :**
- **Documents illimités** (toute la base documentaire de l'entreprise)
- **Utilisateurs illimités**
- Tout le contenu de l'offre Pro
- **2 mises à jour documentaires/mois** incluses
- Support prioritaire par email + téléphone (réponse sous 4h en semaine)
- **Audit initial de la base documentaire** (recommandations de structuration)
- 4 sessions de formation (dont 1 sur site possible en IDF)
- Rapport mensuel d'usage et recommandations
- Accès API pour intégration avec outils existants (ERP, GED)
- Personnalisation de l'interface aux couleurs de l'entreprise
- Référent dédié (Marin)

**Non inclus :**
- Développement sur mesure (devis séparé)
- Hébergement on-premise (option à +200 €/mois)

**Coût réel pour Marin :**
- Setup : ~12h (audit documentaire + ingestion complète + personnalisation) = ~166 €/h
- Mensuel : ~5h/mois (maintenance + mises à jour + rapport + support) = ~90 €/h
- **Marge nette estimée : ~65%**

---

### Tableau comparatif

| | Starter | Pro | Premium |
|---|---|---|---|
| **Setup** | 490 € | 990 € | 1 990 € |
| **Mensuel** | 149 €/mois | 249 €/mois | 449 €/mois |
| **Engagement** | 3 mois | 6 mois | 12 mois |
| **Coût total an 1** | **2 278 €** | **3 978 €** | **7 378 €** |
| Documents | 50 max | 200 max | Illimité |
| Utilisateurs | 3 | 10 | Illimité |
| Mises à jour docs | Payantes | 1/mois incluse | 2/mois incluses |
| Support | Email 48h | Email 24h | Email + tel 4h |
| Formation | 1 session | 2 sessions | 4 sessions |
| Tableau de bord | Non | Oui | Oui |
| API | Non | Non | Oui |
| Référent dédié | Non | Non | Oui |

---

## 3. Argumentaire Prix

### 3.1 Pourquoi ces prix sont justifiés

**Par rapport au marché :**
- Un chatbot IA sur mesure coûte **10 000 à 30 000 €** via une agence. Notre offre Pro revient à **3 978 € la première année** — soit **3 à 8x moins cher**.
- Un consultant IA facture **600 à 900 €/jour**. Notre setup Pro (990 €) équivaut à **1,5 jour de consultant** pour un outil qui reste fonctionnel toute l'année.
- Les SaaS généralistes (Dust.tt à 29 €/user/mois) coûtent **290 €/mois pour 10 users** sans aucune spécialisation BTP ni accompagnement. Notre offre Pro à 249 €/mois inclut la spécialisation métier et le support.

**Par rapport à la valeur délivrée :**
- La stack technique est 100% gratuite (pas de coûts de licence récurrents lourds). Le prix rémunère l'expertise métier BTP, la configuration, et le support — pas un logiciel.
- L'assistant est opérationnel en 48h après signature, pas en 3 mois comme un développement sur mesure.

### 3.2 ROI pour le client BTP

**Scénario concret — PME BTP de 30 salariés, offre Pro :**

| Gain | Estimation annuelle |
|---|---|
| Temps gagné par conducteur de travaux (recherche DTU, CCTP) | 2h/semaine x 45 sem. x 40 €/h = **3 600 €/conducteur** |
| Pour 3 conducteurs | **10 800 €/an** |
| Réduction du risque de non-conformité (1 erreur évitée/an) | **5 000 — 50 000 €** économisés |
| Réduction des appels au bureau d'études | ~500 €/an |
| **Total gains estimés** | **16 300 — 61 300 €/an** |
| **Coût de la solution (Pro)** | **3 978 €/an** |
| **ROI** | **4x à 15x le coût** |

**Message clé** : "Pour le prix d'un déjeuner d'équipe par semaine, vous sécurisez la conformité de tous vos chantiers."

### 3.3 Objections courantes et réponses

| Objection | Réponse |
|---|---|
| **"C'est trop cher pour nous"** | L'offre Starter à 149 €/mois = 5 €/jour ouvré. Moins cher qu'un café par jour pour chaque utilisateur. Et les aides France Num peuvent couvrir jusqu'à 15 000 €. |
| **"On a déjà nos documents en PDF"** | Justement ! L'assistant exploite vos PDFs existants. Pas besoin de ressaisir quoi que ce soit. On ingère vos documents tels quels. |
| **"Nos gars sur le terrain ne sont pas à l'aise avec l'informatique"** | L'interface est aussi simple qu'une barre de recherche Google. On tape sa question, on obtient la réponse avec la référence exacte du document. Formation incluse. |
| **"L'IA va se tromper / halluciner"** | Notre technologie RAG ne répond QUE sur la base de vos documents. Chaque réponse cite sa source (document, page). Pas d'invention. Et quand l'assistant ne sait pas, il le dit. |
| **"On veut tester avant de s'engager"** | On propose une **démo gratuite de 30 minutes** avec vos propres documents. Vous voyez le résultat avant de signer. |
| **"Pourquoi pas ChatGPT directement ?"** | ChatGPT ne connaît pas vos DTU spécifiques, vos CCTP de chantier, vos procédures QSE. Il invente des réponses. Notre assistant ne répond que sur VOS documents, avec les bonnes références. |
| **"Nos données sont confidentielles"** | Vos documents restent dans une base de données dédiée et isolée. Pas de partage avec d'autres clients. Option hébergement privé disponible en Premium. |
| **"On n'a que 10 documents"** | L'offre Starter est faite pour ça. Et quand votre base grandit, on monte en gamme sans tout reconfigurer. |

---

## 4. Options et compléments

| Option | Prix |
|---|---|
| Utilisateur supplémentaire (Pro) | 25 €/user/mois |
| Mise à jour documentaire ponctuelle (Starter) | 50 €/lot (jusqu'à 20 docs) |
| Formation supplémentaire (1h, à distance) | 150 € |
| Formation sur site (demi-journée, IDF) | 490 € |
| Hébergement dédié / on-premise | +200 €/mois |
| Développement sur mesure (intégration ERP, API) | Sur devis (TJM 600 €) |
| Audit documentaire approfondi | 490 € (inclus dans Premium) |

---

## 5. Projections de revenus pour Marin

### Scénario conservateur — 6 premiers mois

| Mois | Clients Starter | Clients Pro | Clients Premium | MRR | Setup cumulé |
|---|---|---|---|---|---|
| M1 | 1 | 0 | 0 | 149 € | 490 € |
| M2 | 1 | 1 | 0 | 398 € | 1 480 € |
| M3 | 2 | 1 | 0 | 547 € | 1 970 € |
| M4 | 2 | 2 | 0 | 796 € | 2 960 € |
| M5 | 3 | 2 | 1 | 1 394 € | 5 440 € |
| M6 | 3 | 3 | 1 | 1 543 € | 6 430 € |

**A M6** : MRR de ~1 500 €/mois + 6 430 € de setup encaissés = **15 688 € de CA sur 6 mois**

### Temps de travail estimé

| Tâche | Heures/mois (à M6, 10 clients) |
|---|---|
| Setup nouveaux clients (~1-2/mois) | 6 — 12h |
| Maintenance + mises à jour | 8 — 15h |
| Support client | 3 — 5h |
| Prospection / vente | 10 — 15h |
| **Total** | **27 — 47h/mois** |

Soit un **taux horaire effectif de 60 à 100 €/h** au démarrage, en progression avec la base clients.

---

## 6. Stratégie de lancement recommandée

1. **Offre de lancement** (M1-M3) : -20% sur le setup pour les 5 premiers clients ("early adopter")
2. **Démo gratuite** : systématique, 30 min avec les vrais documents du prospect
3. **Cas d'usage Duval BTP** : utiliser le client démo existant comme référence
4. **Chèque France Num** : accompagner les prospects dans la demande d'aide (argument de vente puissant)
5. **Focus sur l'offre Pro** : c'est le sweet spot rentabilité/accessibilité. Le Starter sert de porte d'entrée, le Premium de vitrine.

---

*Document généré le 3 mars 2026 — À réviser trimestriellement en fonction des retours marché.*
