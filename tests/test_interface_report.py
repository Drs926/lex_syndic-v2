"""Tests for LEX-024 combined legal analysis and report interface."""

from __future__ import annotations

from lex_syndic.interface import (
    LegalAnalysisRequest,
    LegalAnalysisWithReportResponse,
    analyze_legal_text_with_report,
)

_REPORT_TITLE = "Rapport juridique minimal"

_TELEWORK_TEXT = (
    "Le teletravail est encadre par l'article L. 1222-9 du Code du travail.\n\n"
    "La duree du travail est fixee a 35 heures par semaine."
)

_DISCIPLINE_TEXT = (
    "La discipline est fondee sur les sanctions prevues par le reglement.\n\n"
    "Le salaire comprend une prime annuelle."
)


# ---------------------------------------------------------------------------
# Test 1 — analyse + rapport retournés en un seul appel
# ---------------------------------------------------------------------------


def test_analyze_with_report_returns_both_analysis_and_text() -> None:
    request = LegalAnalysisRequest(
        text=_TELEWORK_TEXT,
        expected_citations=("L1222-9",),
    )
    result = analyze_legal_text_with_report(request)

    assert isinstance(result, LegalAnalysisWithReportResponse)
    assert result.analysis is not None
    assert isinstance(result.report_text, str) and result.report_text


# ---------------------------------------------------------------------------
# Test 2 — report_text contient le titre attendu
# ---------------------------------------------------------------------------


def test_analyze_with_report_text_contains_title() -> None:
    request = LegalAnalysisRequest(
        text=_TELEWORK_TEXT,
        expected_citations=("L1222-9",),
    )
    result = analyze_legal_text_with_report(request)

    assert _REPORT_TITLE in result.report_text


# ---------------------------------------------------------------------------
# Test 3 — decision_status cohérent avec analyze_legal_text()
# ---------------------------------------------------------------------------


def test_analyze_with_report_status_coherent_with_plain_analysis() -> None:
    from lex_syndic.interface import analyze_legal_text

    request = LegalAnalysisRequest(
        text=_DISCIPLINE_TEXT,
        expected_citations=("L1225-1",),
    )
    plain = analyze_legal_text(request)
    combined = analyze_legal_text_with_report(request)

    assert combined.analysis.decision_status == plain.decision_status
    assert combined.analysis.decision_status == "non_compliant"


# ---------------------------------------------------------------------------
# Test 4 — insufficient_data produit aussi un rapport lisible
# ---------------------------------------------------------------------------


def test_analyze_with_report_insufficient_data_has_readable_report() -> None:
    request = LegalAnalysisRequest(
        text=_TELEWORK_TEXT,
        expected_citations=(),
    )
    result = analyze_legal_text_with_report(request)

    assert result.analysis.decision_status == "insufficient_data"
    assert _REPORT_TITLE in result.report_text
    assert "insufficient_data" in result.report_text


# ---------------------------------------------------------------------------
# Test 5 — aucune importation interdite dans report_handler
# ---------------------------------------------------------------------------


def test_report_handler_does_not_import_forbidden_modules() -> None:
    import lex_syndic.interface.report_handler as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("storage", "pipeline", "retrieval", "mcp", "frontend"):
        assert f"lex_syndic.{forbidden}" not in source, (
            f"report_handler must not import lex_syndic.{forbidden}"
        )
