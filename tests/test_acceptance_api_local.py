"""Acceptance tests for LEX-031: local API wrapper end-to-end coverage."""

from __future__ import annotations

from lex_syndic.api import LocalApiAnalysisRequest, LocalApiAnalysisResponse, submit_analysis
from lex_syndic.storage import InMemoryLegalResultStore

_REPORT_TITLE = "Rapport juridique minimal"

_ACCORD_TEXT = """
Article 1 — Télétravail
Le télétravail est encadré conformément aux dispositions de l'article L. 1222-9
du Code du travail. Les modalités de mise en oeuvre sont définies par accord
entre l'employeur et le salarié.

Article 2 — Durée du travail
La durée du travail est fixée conformément à l'article L. 3121-1 du Code du
travail. Le temps de travail effectif est le temps pendant lequel le salarié
est à la disposition de l'employeur.

Article 3 — Rémunération
Le salaire de base comprend une prime annuelle versée en décembre. Les
augmentations sont négociées chaque année lors de la réunion de la commission
paritaire.

Article 4 — Santé et sécurité
L'employeur prend les mesures nécessaires pour assurer la sécurité et protéger
la santé physique et mentale des travailleurs conformément aux règles en vigueur.
"""


def _make_request(citations: tuple[str, ...] = ("L1222-9", "L3121-1")) -> LocalApiAnalysisRequest:
    return LocalApiAnalysisRequest(text=_ACCORD_TEXT, expected_citations=citations)


# ---------------------------------------------------------------------------
# Test 1 — réponse LocalApiAnalysisResponse avec record_id non vide
# ---------------------------------------------------------------------------


def test_acceptance_api_returns_response_with_record_id() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(), store)

    assert isinstance(response, LocalApiAnalysisResponse)
    assert isinstance(response.record_id, str) and response.record_id


# ---------------------------------------------------------------------------
# Test 2 — record_id permet de retrouver le résultat dans le store
# ---------------------------------------------------------------------------


def test_acceptance_api_record_retrievable_from_store() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(), store)

    stored = store.get(response.record_id)
    assert stored is not None
    assert stored.analysis.decision_status == response.decision_status


# ---------------------------------------------------------------------------
# Test 3 — report_text contient le titre attendu
# ---------------------------------------------------------------------------


def test_acceptance_api_report_text_contains_title() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(), store)

    assert _REPORT_TITLE in response.report_text


# ---------------------------------------------------------------------------
# Test 4 — decision_status != insufficient_data avec citations présentes
# ---------------------------------------------------------------------------


def test_acceptance_api_decision_status_not_insufficient_data() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(), store)

    assert response.decision_status != "insufficient_data"


# ---------------------------------------------------------------------------
# Test 5 — expected_citations=() retourne insufficient_data
# ---------------------------------------------------------------------------


def test_acceptance_api_empty_citations_returns_insufficient_data() -> None:
    store = InMemoryLegalResultStore()
    response = submit_analysis(_make_request(citations=()), store)

    assert response.decision_status == "insufficient_data"
    assert _REPORT_TITLE in response.report_text


# ---------------------------------------------------------------------------
# Test 6 — deux stores séparés ne partagent aucun état
# ---------------------------------------------------------------------------


def test_acceptance_api_two_stores_are_isolated() -> None:
    store_a = InMemoryLegalResultStore()
    store_b = InMemoryLegalResultStore()

    submit_analysis(_make_request(), store_a)
    assert store_b.list_ids() == ()
    assert len(store_a.list_ids()) == 1


# ---------------------------------------------------------------------------
# Test 7 — aucun import FastAPI/HTTP dans lex_syndic.api.local
# ---------------------------------------------------------------------------


def test_acceptance_api_local_has_no_fastapi_or_http_import() -> None:
    import lex_syndic.api.local as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("fastapi", "flask", "starlette", "uvicorn", "httpx",
                      "aiohttp", "django", "tornado"):
        assert forbidden not in source.lower(), (
            f"api/local.py must not import {forbidden}"
        )
