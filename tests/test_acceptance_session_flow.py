"""Acceptance tests for LEX-028: full session flow analysis + store."""

from __future__ import annotations

from lex_syndic.interface import LegalAnalysisRequest, LegalSessionResult, analyze_and_store_legal_text
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


def _make_request(citations: tuple[str, ...] = ("L1222-9", "L3121-1")) -> LegalAnalysisRequest:
    return LegalAnalysisRequest(text=_ACCORD_TEXT, expected_citations=citations)


# ---------------------------------------------------------------------------
# Test 1 — retourne LegalSessionResult avec record_id non vide
# ---------------------------------------------------------------------------


def test_acceptance_session_returns_session_result_with_record_id() -> None:
    store = InMemoryLegalResultStore()
    session = analyze_and_store_legal_text(_make_request(), store)

    assert isinstance(session, LegalSessionResult)
    assert isinstance(session.record_id, str) and session.record_id


# ---------------------------------------------------------------------------
# Test 2 — store.get(record_id) is session.result
# ---------------------------------------------------------------------------


def test_acceptance_session_record_retrievable_from_store() -> None:
    store = InMemoryLegalResultStore()
    session = analyze_and_store_legal_text(_make_request(), store)

    assert store.get(session.record_id) is session.result


# ---------------------------------------------------------------------------
# Test 3 — report_text contient le titre attendu
# ---------------------------------------------------------------------------


def test_acceptance_session_report_text_contains_title() -> None:
    store = InMemoryLegalResultStore()
    session = analyze_and_store_legal_text(_make_request(), store)

    assert _REPORT_TITLE in session.result.report_text


# ---------------------------------------------------------------------------
# Test 4 — decision_status cohérent (pas insufficient_data avec citations)
# ---------------------------------------------------------------------------


def test_acceptance_session_decision_status_not_insufficient_data() -> None:
    store = InMemoryLegalResultStore()
    session = analyze_and_store_legal_text(_make_request(), store)

    assert session.result.analysis.decision_status != "insufficient_data"


# ---------------------------------------------------------------------------
# Test 5 — deux stores séparés ne partagent aucun état
# ---------------------------------------------------------------------------


def test_acceptance_session_two_stores_are_isolated() -> None:
    store_a = InMemoryLegalResultStore()
    store_b = InMemoryLegalResultStore()

    analyze_and_store_legal_text(_make_request(), store_a)
    assert store_b.list_ids() == ()
    assert len(store_a.list_ids()) == 1


# ---------------------------------------------------------------------------
# Test 6 — cas insufficient_data stocké avec decision_status correct
# ---------------------------------------------------------------------------


def test_acceptance_session_insufficient_data_is_stored() -> None:
    store = InMemoryLegalResultStore()
    session = analyze_and_store_legal_text(_make_request(citations=()), store)

    assert session.result.analysis.decision_status == "insufficient_data"
    assert store.get(session.record_id) is session.result
    assert _REPORT_TITLE in session.result.report_text
