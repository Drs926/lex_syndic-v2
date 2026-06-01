"""Acceptance tests for LEX-025: full legal flow analysis + readable report."""

from __future__ import annotations

from lex_syndic.interface import (
    LegalAnalysisRequest,
    LegalAnalysisWithReportResponse,
    analyze_legal_text_with_report,
)

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


# ---------------------------------------------------------------------------
# Test 1 — flux complet retourne analysis et report cohérents
# ---------------------------------------------------------------------------


def test_acceptance_full_flow_returns_analysis_and_report() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=("L1222-9", "L3121-1"),
    )
    result = analyze_legal_text_with_report(request)

    assert isinstance(result, LegalAnalysisWithReportResponse)
    assert result.analysis.document_id
    assert result.analysis.analyzed_clause_count > 0
    assert result.analysis.comparison_count > 0
    assert result.analysis.decision_status != "insufficient_data"
    assert _REPORT_TITLE in result.report_text
    assert result.analysis.decision_status in result.report_text
    assert result.analysis.recommended_action in result.report_text


# ---------------------------------------------------------------------------
# Test 2 — citation absente visible dans le rapport
# ---------------------------------------------------------------------------


def test_acceptance_full_flow_absent_citation_is_visible_in_report() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=("L1225-1",),
    )
    result = analyze_legal_text_with_report(request)

    assert result.analysis.decision_status == "non_compliant"
    assert "non_compliant" in result.report_text
    assert result.analysis.justification in result.report_text


# ---------------------------------------------------------------------------
# Test 3 — aucune citation attendue produit un rapport lisible
# ---------------------------------------------------------------------------


def test_acceptance_full_flow_no_expected_citation_has_report() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=(),
    )
    result = analyze_legal_text_with_report(request)

    assert result.analysis.decision_status == "insufficient_data"
    assert result.analysis.comparison_count == 0
    assert "insufficient_data" in result.report_text
    assert _REPORT_TITLE in result.report_text


# ---------------------------------------------------------------------------
# Test 4 — forme stable de LegalAnalysisWithReportResponse
# ---------------------------------------------------------------------------


def test_acceptance_full_flow_shape_is_stable() -> None:
    from lex_syndic.interface import LegalAnalysisResponse

    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=("L1222-9",),
    )
    result = analyze_legal_text_with_report(request)

    assert hasattr(result, "analysis")
    assert hasattr(result, "report_text")
    assert isinstance(result.analysis, LegalAnalysisResponse)
    assert hasattr(result.analysis, "document_id")
    assert hasattr(result.analysis, "decision_status")
    assert hasattr(result.analysis, "alert_level")
    assert hasattr(result.analysis, "justification")
    assert hasattr(result.analysis, "comparison_count")
    assert hasattr(result.analysis, "analyzed_clause_count")
    assert hasattr(result.analysis, "recommended_action")
