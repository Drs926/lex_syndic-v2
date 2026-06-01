"""Tests for LEX-021 legal pipeline interface handler."""

from __future__ import annotations

from lex_syndic.interface import (
    LegalAnalysisRequest,
    LegalAnalysisResponse,
    analyze_legal_text,
)

_TELEWORK_TEXT = (
    "Le teletravail est encadre par l'article L. 1222-9 du Code du travail.\n\n"
    "La duree du travail est fixee a 35 heures par semaine."
)

_DISCIPLINE_TEXT = (
    "La discipline est fondee sur les sanctions prevues par le reglement.\n\n"
    "Le salaire comprend une prime annuelle."
)


# ---------------------------------------------------------------------------
# Structure de réponse
# ---------------------------------------------------------------------------


def test_legal_analysis_response_has_required_fields() -> None:
    request = LegalAnalysisRequest(
        text=_TELEWORK_TEXT,
        expected_citations=("L1222-9",),
    )
    response = analyze_legal_text(request)

    assert isinstance(response, LegalAnalysisResponse)
    assert isinstance(response.document_id, str) and response.document_id
    assert isinstance(response.decision_status, str)
    assert isinstance(response.alert_level, str)
    assert isinstance(response.justification, str)
    assert isinstance(response.comparison_count, int) and response.comparison_count >= 0
    assert isinstance(response.analyzed_clause_count, int) and response.analyzed_clause_count > 0
    assert isinstance(response.recommended_action, str)


# ---------------------------------------------------------------------------
# Cas 1 — nominal : référence extraite du document, citation fournie
# ---------------------------------------------------------------------------


def test_analyze_legal_text_nominal_reference_present() -> None:
    request = LegalAnalysisRequest(
        text=_TELEWORK_TEXT,
        expected_citations=("L1222-9",),
    )
    response = analyze_legal_text(request)

    assert response.decision_status != "insufficient_data"
    assert response.comparison_count > 0
    assert response.analyzed_clause_count > 0


# ---------------------------------------------------------------------------
# Cas 2 — non_compliant : citation absente du document
# ---------------------------------------------------------------------------


def test_analyze_legal_text_non_compliant_citation_absent() -> None:
    request = LegalAnalysisRequest(
        text=_DISCIPLINE_TEXT,
        expected_citations=("L1225-1",),
    )
    response = analyze_legal_text(request)

    assert response.decision_status == "non_compliant"
    assert response.comparison_count > 0


# ---------------------------------------------------------------------------
# Cas 3 — insufficient_data : aucune citation attendue
# ---------------------------------------------------------------------------


def test_analyze_legal_text_insufficient_data_no_citations() -> None:
    request = LegalAnalysisRequest(
        text=_TELEWORK_TEXT,
        expected_citations=(),
    )
    response = analyze_legal_text(request)

    assert response.decision_status == "insufficient_data"
    assert response.comparison_count == 0


# ---------------------------------------------------------------------------
# Cas 4 — insufficient_data : texte vide
# ---------------------------------------------------------------------------


def test_analyze_legal_text_empty_text_returns_insufficient_data() -> None:
    request = LegalAnalysisRequest(text="   ", expected_citations=("L1222-9",))
    response = analyze_legal_text(request)

    assert response.decision_status == "insufficient_data"
    assert response.document_id == ""


# ---------------------------------------------------------------------------
# Isolation : aucun import storage / report / frontend / MCP
# ---------------------------------------------------------------------------


def test_legal_handler_does_not_import_forbidden_modules() -> None:
    import lex_syndic.interface.legal_handler as module

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("storage", "report", "retrieval", "mcp", "frontend"):
        assert f"lex_syndic.{forbidden}" not in source, (
            f"legal_handler must not import lex_syndic.{forbidden}"
        )
