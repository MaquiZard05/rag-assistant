---
name: streamlit-pro-ui
description: Apply when working on any Streamlit interface, UI, styling, layout, or frontend task for the RAG assistant. Also trigger when Marin mentions app.py, interface, CSS, design, sidebar, chat UI, admin panel, multi-pages, couleurs, branding, or anything visual about the app. This skill ensures Claude Code produces professional-grade Streamlit UIs instead of default unstyled output.
---

# Streamlit Pro UI — Design System RAG Assistant

## Philosophie de design (LIRE EN PREMIER)

Ces principes viennent des tendances UI/UX SaaS 2026 et doivent guider CHAQUE décision visuelle. Ne pas appliquer du CSS au hasard — comprendre le POURQUOI avant le COMMENT.

### Principe 1 : IA Invisible
L'utilisateur ne doit jamais voir la mécanique RAG. Pas de jargon technique visible (embeddings, chunks, vector store). La page Chat montre UNIQUEMENT : le header, la conversation, et l'input. Tout le reste (paramètres, gestion docs, admin) est sur des pages séparées ou derrière un menu. Le client pose une question, il obtient une réponse sourcée. Point.

### Principe 2 : Calm Design — Réduction du bruit visuel
Masquer par défaut tout ce qui n'est pas essentiel à la tâche immédiate. Pas de sliders visibles en permanence, pas de listes de documents sur la page de chat, pas de boutons rouges "Effacer". Chaque élément visible doit MÉRITER sa place à l'écran. En cas de doute, on enlève.

### Principe 3 : Profondeur 2.5D — Ombres et relief subtils
Les éléments interactifs utilisent des box-shadow et des bordures légères pour créer de l'affordance. L'utilisateur comprend instinctivement ce qui est cliquable et ce qui est du contenu. Pas de design plat brutal — des ombres subtiles qui créent de la profondeur.

### Principe 4 : Feedback vivant — Micro-interactions
Quand le système "réfléchit", ne pas afficher un simple spinner. Utiliser un indicateur de typing animé (3 dots pulsants) ou un dégradé qui pulse doucement. Le système doit paraître VIVANT, pas figé en attente.

### Principe 5 : Sobriété — Pas de couleurs criardes
Pas de bleu lavande, pas de dégradés pastel flashy, pas de couleurs "joyeuses" qui font amateur. La palette est sobre, professionnelle, contrastée. Le premium se signale par la retenue, pas par la saturation.

---

## Architecture des pages

```
rag-assistant/
├── app.py                  # Redirection + page config
├── pages/
│   ├── 1_💬_Chat.py        # UNIQUEMENT : header + conversation + input
│   └── 2_⚙️_Admin.py      # Gestion docs, collections, paramètres
├── styles/
│   └── main.css            # CSS unique pour toute l'app
```

La page Chat est SACRÉE — aucun élément technique ne doit y apparaître. L'upload de documents, la liste des fichiers indexés, les sliders de paramètres → tout ça va sur la page Admin.

---

## Injection CSS — Méthode obligatoire

```python
import streamlit as st

def load_css(css_file: str):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Première instruction après st.set_page_config() :
load_css("styles/main.css")
```

---

## CSS Complet — Copier tel quel

```css
/* ============================================
   RAG ASSISTANT — DESIGN SYSTEM 2026
   Calm Design + 2.5D + Sobriété
   ============================================ */

/* === RESET STREAMLIT DEFAULTS === */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* === TYPOGRAPHIE === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* === APP GLOBAL === */
.stApp {
    background-color: #fafafa;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #1a1a2e;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background-color: #0f1923;
    border-right: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stRadio label {
    color: #8b949e !important;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Sidebar nav — clean spacing */
[data-testid="stSidebarNav"] {
    padding-top: 1.5rem;
}

/* === CUSTOM HEADER === */
.app-header {
    background: #0f1923;
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
    position: relative;
    overflow: hidden;
}

/* Subtle gradient accent line at top */
.app-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #3b82f6);
    background-size: 200% 100%;
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.app-header h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
}

.app-header p {
    margin: 0.4rem 0 0;
    color: #8b949e;
    font-size: 0.9rem;
    font-weight: 400;
}

/* === CHAT AREA — The sacred space === */

/* All chat messages — shared base */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.75rem;
    border: 1px solid transparent;
    transition: box-shadow 0.2s ease;
}

/* User messages — subtle, recessed */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #f0f2f5;
    border-color: #e4e7eb;
}

/* Assistant messages — elevated, prominent */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #ffffff;
    border-color: #e4e7eb;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

/* Chat input — clean with focus state */
[data-testid="stChatInput"] {
    border-radius: 14px;
}

[data-testid="stChatInput"] textarea {
    border: 2px solid #e4e7eb !important;
    border-radius: 14px !important;
    padding: 0.9rem 1.2rem !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    background: #ffffff !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.08) !important;
}

/* === BUTTONS — 2.5D with shadow === */
.stButton > button {
    background-color: #1a1a2e;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    font-size: 0.875rem;
    letter-spacing: -0.01em;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
    cursor: pointer;
}

.stButton > button:hover {
    background-color: #2d2d44;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
}

/* === FILE UPLOADER — Clean drop zone === */
[data-testid="stFileUploader"] {
    border: 2px dashed #d1d5db;
    border-radius: 14px;
    padding: 1.2rem;
    background-color: #ffffff;
    transition: all 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #3b82f6;
    background-color: #f8faff;
}

/* === EXPANDERS (sources) — Subtle === */
.streamlit-expanderHeader {
    background-color: #f8f9fa;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #4b5563;
}

/* === CONFIDENCE BADGES === */
.confidence-high {
    display: inline-block;
    color: #059669;
    background: #ecfdf5;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.8rem;
}

.confidence-medium {
    display: inline-block;
    color: #d97706;
    background: #fffbeb;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.8rem;
}

.confidence-low {
    display: inline-block;
    color: #dc2626;
    background: #fef2f2;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.8rem;
}

/* === METRIC CARDS (Admin page) === */
.metric-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    border: 1px solid #e4e7eb;
    text-align: center;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.metric-card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    transform: translateY(-2px);
}

.metric-card h3 {
    color: #1a1a2e;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.03em;
}

.metric-card p {
    color: #6b7280;
    font-size: 0.82rem;
    margin: 0.3rem 0 0;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 500;
}

/* === TYPING INDICATOR — Feedback vivant === */
@keyframes typingPulse {
    0%, 60%, 100% { opacity: 0.3; transform: scale(0.8); }
    30% { opacity: 1; transform: scale(1); }
}

.typing-indicator {
    display: inline-flex;
    gap: 4px;
    padding: 0.5rem 0;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    background: #3b82f6;
    border-radius: 50%;
    animation: typingPulse 1.4s infinite;
}

.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

/* === SCROLLBAR — Subtle === */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #9ca3af;
}
```

---

## Composants Python réutilisables

### Header (chaque page)

```python
def render_header(title, subtitle=None):
    html = f'''
    <div class="app-header">
        <h1>📄 {title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)
```

### Indicateur de confiance

```python
def render_confidence(num_sources):
    if num_sources >= 3:
        cls, label = "confidence-high", "Confiance élevée"
    elif num_sources >= 1:
        cls, label = "confidence-medium", "Confiance moyenne"
    else:
        cls, label = "confidence-low", "Confiance faible"
    st.markdown(
        f'<span class="{cls}">{label} — {num_sources} source(s)</span>',
        unsafe_allow_html=True
    )
```

### Typing indicator (pendant la génération)

```python
def render_typing():
    st.markdown('''
    <div class="typing-indicator">
        <span></span><span></span><span></span>
    </div>
    ''', unsafe_allow_html=True)
```

### Metric cards (page Admin)

```python
def render_metric(value, label):
    st.markdown(f'''
    <div class="metric-card">
        <h3>{value}</h3>
        <p>{label}</p>
    </div>
    ''', unsafe_allow_html=True)
```

### Chat avec avatars

```python
with st.chat_message("user", avatar="👤"):
    st.markdown(question)

with st.chat_message("assistant", avatar="🤖"):
    st.markdown(response)
```

---

## Page config — Toujours en premier

```python
st.set_page_config(
    page_title="Assistant Documentaire IA",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"  # Calm design : sidebar fermée par défaut sur Chat
)
```

---

## Palette de couleurs

| Rôle | Hex | Quand l'utiliser |
|------|-----|-----------------|
| Background app | #fafafa | Fond global — gris ultra-léger, pas blanc pur |
| Surface / Cards | #ffffff | Bulles assistant, cards, modales |
| User bubble | #f0f2f5 | Messages utilisateur — en retrait |
| Header / Sidebar | #0f1923 | Fond sombre — contraste fort, pro |
| Text primary | #1a1a2e | Titres, corps de texte |
| Text secondary | #6b7280 | Labels, descriptions, metadata |
| Text sidebar | #c9d1d9 | Texte clair sur fond sombre |
| Accent primary | #3b82f6 | Focus states, liens, accents |
| Accent subtle | #8b5cf6 | Dégradé header, éléments premium |
| Border | #e4e7eb | Bordures subtiles partout |
| Success | #059669 sur #ecfdf5 | Badge confiance haute |
| Warning | #d97706 sur #fffbeb | Badge confiance moyenne |
| Error | #dc2626 sur #fef2f2 | Badge confiance basse |

---

## Anti-patterns — NE PAS FAIRE

- ❌ Mettre l'upload de documents sur la page Chat (ça va sur Admin)
- ❌ Afficher un slider de paramètres visible en permanence
- ❌ Utiliser des couleurs pastel lavande, rose, ou flashy
- ❌ Laisser le menu hamburger Streamlit visible
- ❌ Mettre un bouton "Effacer" rouge bien visible
- ❌ Utiliser `st.title()` ou `st.header()` seuls sans header HTML custom
- ❌ Afficher un simple spinner text pendant la génération
- ❌ Utiliser layout="centered" (toujours "wide")
- ❌ Sidebar ouverte par défaut sur la page Chat
- ❌ Montrer du jargon technique (chunks, embeddings, vector) au client