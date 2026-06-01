"""Tests for LEX-027 session flow: analyze and store legal result."""

from __future__ import annotations

from lex_syndic.interface import (
    LegalAnalysisRequest,
    LegalAnalysisWithReportResponse,
    LegalSessionResult,
    analyze_and_store_legal_text,
)
from lex_syndic.storage import InMemoryLegalResultStore

_TEXT = (
    "Le télétravail est encadré par l'article L. 1222-9 du Code du travail.\n\n"
    "La durée du travail est fixée à 35 heures par semaine."
)

_TEXT_NO_CITATION = (
    "L'employeur garantit la sécurité des travailleurs dans l'établissement.\n\n"
    "Un règlement intérieur est affiché dans les locaux."
)


# ---------------------------------------------------------------------------
# Test 1 — retourne record_id + result
# ---------------------------------------------------------------------------


def test_analyze_and_store_returns_record_id_and_result() -> None:
    store = InMemoryLegalResultStore()
    request = LegalAnalysisRequest(text=_TEXT, expected_citations=("L1222-9",))
    session = analyze_and_store_legal_text(request, store)

    assert isinstance(session, LegalSessionResult)
    assert isinstance(session.record_id, str) and session.record_id
    assert isinstance(session.result, LegalAnalysisWithReportResponse)


# ---------------------------------------------------------------------------
# Test 2 — record_id permet de retrouver exactement le même result
# ---------------------------------------------------------------------------


def test_record_id_retrieves_exact_result() -> None:
    store = InMemoryLegalResultStore()
    request = LegalAnalysisRequest(text=_TEXT, expected_citations=("L1222-9",))
    session = analyze_and_store_legal_text(request, store)

    retrieved = store.get(session.record_id)
    assert retrieved is session.result


# ---------------------------------------------------------------------------
# Test 3 — plusieurs appels créent des ids distincts
# ---------------------------------------------------------------------------


def test_multiple_calls_create_distinct_ids() -> None:
    store = InMemoryLegalResultStore()
    request = LegalAnalysisRequest(text=_TEXT, expected_citations=("L1222-9",))
    s1 = analyze_and_store_legal_text(request, store)
    s2 = analyze_and_store_legal_text(request, store)
    s3 = analyze_and_store_legal_text(request, store)

    ids = {s1.record_id, s2.record_id, s3.record_id}
    assert len(ids) == 3


# ---------------------------------------------------------------------------
# Test 4 — cas insufficient_data est aussi stocké
# ---------------------------------------------------------------------------


def test_insufficient_data_is_stored() -> None:
    store = InMemoryLegalResultStore()
    request = LegalAnalysisRequest(text=_TEXT, expected_citations=())
    session = analyze_and_store_legal_text(request, store)

    assert session.result.analysis.decision_status == "insufficient_data"
    assert store.get(session.record_id) is session.result


# ---------------------------------------------------------------------------
# Test 5 — aucun store global partagé entre tests
# ---------------------------------------------------------------------------


def test_no_shared_global_store() -> None:
    store_a = InMemoryLegalResultStore()
    store_b = InMemoryLegalResultStore()
    request = LegalAnalysisRequest(text=_TEXT, expected_citations=("L1222-9",))

    analyze_and_store_legal_text(request, store_a)
    assert store_b.list_ids() == ()


# ---------------------------------------------------------------------------
# Test 6 — aucun import interdit dans session_handler
# ---------------------------------------------------------------------------


def test_session_handler_does_not_import_forbidden_modules() -> None:
    import lex_syndic.interface.session_handler as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("sqlite", "json", "pickle", "open(", "pathlib", "os.path",
                      "frontend", "mcp", "pipeline", "analysis", "comparison",
                      "rules"):
        assert f"lex_syndic.{forbidden}" not in source or forbidden in ("open(", "sqlite", "json", "pickle", "pathlib", "os.path"), (
            f"session_handler must not import lex_syndic.{forbidden}"
        )
