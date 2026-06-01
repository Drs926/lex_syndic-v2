"""LEX-022 — End-to-end acceptance test for the legal app flow.

Flow under test:
    texte juridique + citations attendues
    → LegalAnalysisRequest
    → analyze_legal_text()
    → LegalAnalysisResponse

No mocks. No storage. No LLM. Real deterministic pipeline only.
"""

from __future__ import annotations

from dataclasses import fields

from lex_syndic.interface import (
    LegalAnalysisRequest,
    LegalAnalysisResponse,
    analyze_legal_text,
)

# ---------------------------------------------------------------------------
# Accord d'entreprise minimal réaliste — plusieurs clauses thématiques
# ---------------------------------------------------------------------------

_ACCORD_TEXT = """\
Article 1 — Télétravail

Le présent accord encadre le télétravail conformément à l'article L. 1222-9
du Code du travail. Tout salarié peut demander à exercer ses fonctions en
télétravail dans les conditions définies ci-après.

Article 2 — Durée du travail

La durée du travail applicable est régie par l'article L. 3121-1 du Code du
travail. La durée hebdomadaire de référence est fixée à 35 heures.

Article 3 — Rémunération

Le salaire de base est maintenu sans modification lors du passage en
télétravail. Une prime de matériel peut être versée selon les modalités
définies par la direction.

Article 4 — Santé et sécurité

L'employeur veille à la prévention des risques professionnels. Les règles
de sécurité applicables au poste habituel s'appliquent également en
télétravail.
"""

# ---------------------------------------------------------------------------
# Test 1 — Citations présentes → réponse structurée valide
# ---------------------------------------------------------------------------


def test_acceptance_present_citations_return_structured_response() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=("L1222-9", "L3121-1"),
        title="accord-entreprise-minimal",
    )

    response = analyze_legal_text(request)

    assert isinstance(response, LegalAnalysisResponse)
    assert response.document_id, "document_id must not be empty"
    assert response.analyzed_clause_count > 0, "at least one clause must be analyzed"
    assert response.comparison_count > 0, "at least one comparison must be produced"
    assert response.decision_status != "insufficient_data"
    assert isinstance(response.alert_level, str) and response.alert_level
    assert isinstance(response.justification, str) and response.justification
    assert isinstance(response.recommended_action, str) and response.recommended_action


# ---------------------------------------------------------------------------
# Test 2 — Citation absente → non_compliant
# ---------------------------------------------------------------------------


def test_acceptance_absent_citation_returns_non_compliant() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=("L1225-1",),
        title="accord-entreprise-minimal",
    )

    response = analyze_legal_text(request)

    assert response.decision_status == "non_compliant"
    assert response.comparison_count > 0
    assert response.recommended_action


# ---------------------------------------------------------------------------
# Test 3 — Aucune citation attendue → insufficient_data
# ---------------------------------------------------------------------------


def test_acceptance_no_expected_citation_returns_insufficient_data() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=(),
        title="accord-entreprise-minimal",
    )

    response = analyze_legal_text(request)

    assert response.decision_status == "insufficient_data"
    assert response.comparison_count == 0
    assert response.analyzed_clause_count > 0, "analysis must still run with no citations"


# ---------------------------------------------------------------------------
# Test 4 — Shape de réponse stable
# ---------------------------------------------------------------------------


def test_acceptance_response_shape_is_stable() -> None:
    request = LegalAnalysisRequest(
        text=_ACCORD_TEXT,
        expected_citations=("L1222-9",),
        title="accord-entreprise-minimal",
    )

    response = analyze_legal_text(request)

    expected_fields = {
        "document_id",
        "decision_status",
        "alert_level",
        "justification",
        "comparison_count",
        "analyzed_clause_count",
        "recommended_action",
    }
    actual_fields = {f.name for f in fields(response)}
    assert actual_fields == expected_fields, (
        f"Response shape mismatch. Expected {expected_fields}, got {actual_fields}"
    )
