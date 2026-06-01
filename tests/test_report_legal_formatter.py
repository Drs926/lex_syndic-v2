"""Tests for LEX-023 minimal legal proof report formatter."""

from __future__ import annotations

from lex_syndic.interface import LegalAnalysisResponse
from lex_syndic.report import format_legal_report

_TITLE = "Rapport juridique minimal"


def _response(
    *,
    document_id: str = "doc-001",
    decision_status: str = "compliant",
    alert_level: str = "none",
    justification: str = "All expected norm references are matched without gap.",
    comparison_count: int = 2,
    analyzed_clause_count: int = 3,
    recommended_action: str = "No action required.",
) -> LegalAnalysisResponse:
    return LegalAnalysisResponse(
        document_id=document_id,
        decision_status=decision_status,
        alert_level=alert_level,
        justification=justification,
        comparison_count=comparison_count,
        analyzed_clause_count=analyzed_clause_count,
        recommended_action=recommended_action,
    )


# ---------------------------------------------------------------------------
# Test 1 — rapport nominal avec tous les champs
# ---------------------------------------------------------------------------


def test_format_legal_report_nominal_contains_all_fields() -> None:
    response = _response()
    report = format_legal_report(response)

    assert _TITLE in report
    assert "compliant" in report
    assert "none" in report
    assert "All expected norm references are matched without gap." in report
    assert "No action required." in report
    assert "3" in report
    assert "2" in report


# ---------------------------------------------------------------------------
# Test 2 — rapport insufficient_data
# ---------------------------------------------------------------------------


def test_format_legal_report_insufficient_data() -> None:
    response = _response(
        decision_status="insufficient_data",
        alert_level="unknown",
        justification="No valid clause-norm comparison was provided.",
        comparison_count=0,
        analyzed_clause_count=1,
        recommended_action="Provide at least one valid clause-norm comparison.",
    )
    report = format_legal_report(response)

    assert "insufficient_data" in report
    assert "unknown" in report
    assert "No valid clause-norm comparison was provided." in report
    assert "0" in report


# ---------------------------------------------------------------------------
# Test 3 — ordre stable des lignes
# ---------------------------------------------------------------------------


def test_format_legal_report_line_order_is_stable() -> None:
    response = _response()
    report = format_legal_report(response)
    lines = report.splitlines()

    def line_index(label: str) -> int:
        for i, line in enumerate(lines):
            if label in line:
                return i
        raise AssertionError(f"Label not found: {label!r}")

    assert line_index("Statut") < line_index("Niveau d'alerte")
    assert line_index("Niveau d'alerte") < line_index("Justification")
    assert line_index("Justification") < line_index("Action recommandée")
    assert line_index("Action recommandée") < line_index("Clauses analysées")
    assert line_index("Clauses analysées") < line_index("Comparaisons réalisées")


# ---------------------------------------------------------------------------
# Test 4 — sortie déterministe
# ---------------------------------------------------------------------------


def test_format_legal_report_is_deterministic() -> None:
    response = _response()
    assert format_legal_report(response) == format_legal_report(response)


# ---------------------------------------------------------------------------
# Test 5 — aucun import interdit depuis le formatter
# ---------------------------------------------------------------------------


def test_legal_formatter_does_not_import_forbidden_modules() -> None:
    import lex_syndic.report.legal_formatter as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("storage", "pipeline", "retrieval", "mcp", "frontend"):
        assert f"lex_syndic.{forbidden}" not in source, (
            f"legal_formatter must not import lex_syndic.{forbidden}"
        )
