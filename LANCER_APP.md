# Comment lancer l'Assistant Documentaire IA

## Quel terminal utiliser ?

**Utilise le terminal WSL (Ubuntu)**, pas CMD ni PowerShell.

Deux options :
1. **VS Code** : ouvre le terminal integre (Ctrl+`) et verifie qu'il est en mode **WSL/Ubuntu** (en bas a gauche de VS Code tu dois voir "WSL: Ubuntu")
2. **Terminal Ubuntu** : ouvre directement l'app "Ubuntu" depuis le menu demarrer Windows

> CMD et PowerShell ne fonctionneront PAS car le projet est installe dans le systeme de fichiers Linux (WSL).

## Lancer l'application

```bash
# 1. Aller dans le projet
cd ~/Liberté/rag-assistant

# 2. Activer l'environnement Python
source venv/bin/activate

# 3. Lancer l'interface web
streamlit run app.py
```

Le terminal affiche :
```
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

## Ouvrir dans le navigateur

Ouvre ton navigateur (Chrome, Firefox, Edge...) et va sur :

**http://localhost:8501**

## Utilisation

1. **Sidebar gauche** : deposer des PDFs (indexes automatiquement)
2. **Barre en bas** : taper une question
3. **Reponse** : avec sources citees + indicateur de confiance
4. **Parametres** : ajuster le nombre de sources dans la sidebar

## Arreter l'application

Retourne dans le terminal et appuie sur **Ctrl+C**.

## En cas de probleme

```bash
# Verifier que l'environnement est actif (tu dois voir "(venv)" au debut de la ligne)
source venv/bin/activate

# Reinstaller les dependances si besoin
pip install -r requirements.txt

# Re-indexer les documents
python src/ingest.py

# Relancer
streamlit run app.py
```
