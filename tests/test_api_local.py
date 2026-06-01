"""Tests for LEX-030 local single-user API wrapper."""

from __future__ import annotations

from lex_syndic.api import LocalApiAnalysisRequest, LocalApiAnalysisResponse, submit_analysis
from lex_syndic.storage import InMemoryLegalResultStore

_TEXT = (
    "Le télétravail est encadré par l'article L. 1222-9 du Code du travail.\n\n"
    "La durée du travail est fixée à 35 heures par semaine."
)

_REPORT_TITLE = "Rapport juridique minimal"


def _make_request(citations: tuple[str, ...] = ("L1222-9",)) -> LocalApiAnalysisRequest:
    return LocalApiAnalysisRequest(text=_TEXT, expected_citations=citations)


# ---------------------------------------------------------------------------
# Test 1 — submit_analysis retourne record_id + statut + rapport
# ---------------------------------------------------------------------------


def test_submit_analysis_returns_record_id_status_and_report() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(), store)

    assert isinstance(response, LocalApiAnalysisResponse)
    assert isinstance(response.record_id, str) and response.record_id
    assert response.decision_status
    assert response.alert_level
    assert _REPORT_TITLE in response.report_text
    assert response.recommended_action


# ---------------------------------------------------------------------------
# Test 2 — record_id permet de retrouver le résultat dans le store
# ---------------------------------------------------------------------------


def test_record_id_retrieves_result_from_store() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(), store)

    stored = store.get(response.record_id)
    assert stored is not None
    assert stored.analysis.decision_status == response.decision_status


# ---------------------------------------------------------------------------
# Test 3 — expected_citations=() retourne insufficient_data
# ---------------------------------------------------------------------------


def test_empty_citations_returns_insufficient_data() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(citations=()), store)

    assert response.decision_status == "insufficient_data"
    assert _REPORT_TITLE in response.report_text


# ---------------------------------------------------------------------------
# Test 4 — deux stores sont isolés
# ---------------------------------------------------------------------------


def test_two_stores_are_isolated() -> None:
    store_a = InMemoryLegalResultStore()
    store_b = InMemoryLegalResultStore()

    submit_analysis(_make_request(), store_a)
    assert store_b.list_ids() == ()


# ---------------------------------------------------------------------------
# Test 5 — aucune écriture disque
# ---------------------------------------------------------------------------


def test_no_file_created(tmp_path, monkeypatch) -> None:
    import os
    monkeypatch.chdir(tmp_path)
    store = InMemoryLegalResultStore()
    submit_analysis(_make_request(), store)
    assert list(tmp_path.iterdir()) == []


# ---------------------------------------------------------------------------
# Test 6 — aucun store global
# ---------------------------------------------------------------------------


def test_no_global_store() -> None:
    store_1 = InMemoryLegalResultStore()
    store_2 = InMemoryLegalResultStore()
    submit_analysis(_make_request(), store_1)
    # store_2 untouched — proves no shared global state
    assert store_2.list_ids() == ()


# ---------------------------------------------------------------------------
# Test 7 — aucun import FastAPI dans local.py
# ---------------------------------------------------------------------------


def test_local_api_does_not_import_fastapi_or_http() -> None:
    import lex_syndic.api.local as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("fastapi", "flask", "starlette", "uvicorn", "httpx",
                      "aiohttp", "django", "tornado"):
        assert forbidden not in source.lower(), (
            f"local.py must not import {forbidden}"
        )
