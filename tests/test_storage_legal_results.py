"""Tests for LEX-026 in-memory legal result store."""

from __future__ import annotations

from lex_syndic.interface import LegalAnalysisRequest, analyze_legal_text_with_report
from lex_syndic.storage import InMemoryLegalResultStore

_TEXT = (
    "Le télétravail est encadré par l'article L. 1222-9 du Code du travail.\n\n"
    "La durée du travail est fixée à 35 heures par semaine."
)


def _make_result():
    request = LegalAnalysisRequest(text=_TEXT, expected_citations=("L1222-9",))
    return analyze_legal_text_with_report(request)


# ---------------------------------------------------------------------------
# Test 1 — save puis get retourne le même résultat
# ---------------------------------------------------------------------------


def test_save_and_get_returns_same_result() -> None:
    store = InMemoryLegalResultStore()
    result = _make_result()
    record_id = store.save(result)
    assert store.get(record_id) is result


# ---------------------------------------------------------------------------
# Test 2 — get inconnu retourne None
# ---------------------------------------------------------------------------


def test_get_unknown_returns_none() -> None:
    store = InMemoryLegalResultStore()
    assert store.get("result-9999") is None


# ---------------------------------------------------------------------------
# Test 3 — list_ids retourne les ids dans un ordre stable
# ---------------------------------------------------------------------------


def test_list_ids_stable_order() -> None:
    store = InMemoryLegalResultStore()
    r1 = store.save(_make_result())
    r2 = store.save(_make_result())
    r3 = store.save(_make_result())
    assert store.list_ids() == (r1, r2, r3)


# ---------------------------------------------------------------------------
# Test 4 — clear vide le store
# ---------------------------------------------------------------------------


def test_clear_empties_store() -> None:
    store = InMemoryLegalResultStore()
    store.save(_make_result())
    store.clear()
    assert store.list_ids() == ()
    assert store.get("result-0001") is None


# ---------------------------------------------------------------------------
# Test 5 — plusieurs sauvegardes ne s'écrasent pas
# ---------------------------------------------------------------------------


def test_multiple_saves_do_not_overwrite() -> None:
    store = InMemoryLegalResultStore()
    r1 = _make_result()
    r2 = _make_result()
    id1 = store.save(r1)
    id2 = store.save(r2)
    assert id1 != id2
    assert store.get(id1) is r1
    assert store.get(id2) is r2
    assert len(store.list_ids()) == 2


# ---------------------------------------------------------------------------
# Test 6 — aucun fichier n'est créé
# ---------------------------------------------------------------------------


def test_no_file_created(tmp_path, monkeypatch) -> None:
    import os
    monkeypatch.chdir(tmp_path)
    store = InMemoryLegalResultStore()
    store.save(_make_result())
    assert list(tmp_path.iterdir()) == [], "store must not write any file"


# ---------------------------------------------------------------------------
# Test 7 — aucun import interdit dans legal_results
# ---------------------------------------------------------------------------


def test_legal_results_does_not_import_forbidden_modules() -> None:
    import lex_syndic.storage.legal_results as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("sqlite", "json", "pickle", "open(", "pathlib", "os.path"):
        assert forbidden not in source, (
            f"legal_results must not use {forbidden!r}"
        )
