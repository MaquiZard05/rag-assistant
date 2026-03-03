"""Tests pour le filtrage par categories BTP dans le pipeline RAG.

Verifie que CATEGORY_FILTERS est complet et que hybrid_search()
filtre correctement les resultats par categorie.
"""

import os
import sys
from pathlib import Path

import pytest

# Ajouter src/ au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from query import CATEGORY_FILTERS, hybrid_search, load_vectorstore
from config import DEFAULT_COLLECTION

# Collection de test BTP avec les 6 PDFs
BTP_COLLECTION = "thermex_btp"

# Mapping categorie → pattern attendu dans le nom de fichier source
EXPECTED_PATTERNS = {
    "normes": "dtu",
    "cctp": "cctp",
    "qse": "qse",
    "fiches": "fiches",
    "doe": "doe",
    "admin": "memo",
}


def test_category_filters_exist():
    """Verifie que CATEGORY_FILTERS contient bien les 6 categories BTP attendues."""
    expected_keys = {"normes", "cctp", "qse", "fiches", "doe", "admin"}
    assert set(CATEGORY_FILTERS.keys()) == expected_keys, (
        f"CATEGORY_FILTERS devrait contenir {expected_keys}, "
        f"mais contient {set(CATEGORY_FILTERS.keys())}"
    )


@pytest.fixture(scope="module")
def vectorstore():
    """Charge le vectorstore thermex_btp une seule fois pour tous les tests du module."""
    return load_vectorstore(BTP_COLLECTION)


@pytest.mark.parametrize("category", list(CATEGORY_FILTERS.keys()))
def test_hybrid_search_with_category(vectorstore, category):
    """Verifie que hybrid_search filtre correctement par categorie.

    Pour chaque categorie, tous les resultats doivent avoir un nom de fichier
    source contenant le pattern attendu (ex: 'normes' → 'dtu' dans le source).
    """
    question = "quelles sont les exigences ?"
    results = hybrid_search(vectorstore, question, category=category)

    assert len(results) > 0, (
        f"La categorie '{category}' ne retourne aucun resultat — "
        f"verifier que la collection {BTP_COLLECTION} contient des docs correspondants"
    )

    pattern = EXPECTED_PATTERNS[category]
    for doc, _score in results:
        source = doc.metadata.get("source", "").lower()
        assert pattern in source, (
            f"Categorie '{category}' : le document source '{source}' "
            f"ne contient pas le pattern attendu '{pattern}'"
        )


def test_hybrid_search_without_category(vectorstore):
    """Verifie que sans filtre de categorie, les resultats proviennent de plusieurs fichiers.

    Un search sans categorie doit retourner des chunks de sources variees,
    prouvant qu'aucun filtre n'est applique par defaut.
    """
    question = "quelles sont les exigences du chantier ?"
    results = hybrid_search(vectorstore, question, category=None)

    assert len(results) > 0, "La recherche sans categorie ne retourne aucun resultat"

    # Collecter les sources uniques
    sources = set()
    for doc, _score in results:
        source = doc.metadata.get("source", "")
        sources.add(source)

    assert len(sources) > 1, (
        f"Sans filtre de categorie, on attend des resultats de plusieurs fichiers, "
        f"mais on n'a que : {sources}"
    )


def test_category_filter_no_results():
    """Verifie qu'un vectorstore vide ou une categorie sans docs retourne une liste vide.

    On cree un vectorstore sur une collection qui n'existe pas ou est vide,
    et on verifie que hybrid_search renvoie [] sans erreur.
    """
    # Utiliser une collection inexistante pour simuler un vectorstore vide
    empty_vs = load_vectorstore("collection_inexistante_test")
    results = hybrid_search(empty_vs, "test question", category="normes")
    assert results == [], (
        f"Un vectorstore vide devrait retourner [], mais retourne {len(results)} resultats"
    )


@pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY non disponible — test d'integration skippe"
)
def test_ask_passes_category():
    """Verifie que ask() accepte le parametre category sans erreur.

    Test d'integration leger : appelle le pipeline complet avec une categorie.
    Necessite GROQ_API_KEY pour fonctionner.
    """
    from query import ask

    result = ask(
        question="Quels DTU sont applicables ?",
        collection_name=BTP_COLLECTION,
        category="normes",
    )

    assert "answer" in result, "ask() doit retourner un dict avec une cle 'answer'"
    assert "sources" in result, "ask() doit retourner un dict avec une cle 'sources'"
    assert isinstance(result["sources"], list), "Les sources doivent etre une liste"
