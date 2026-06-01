"""Legal pipeline interface handler for LEX-021."""

from __future__ import annotations

from dataclasses import dataclass, field

from lex_syndic.ingestion import load_text_content
from lex_syndic.legal.models import LegalReference
from lex_syndic.pipeline import run_legal_pipeline


@dataclass(frozen=True)
class LegalAnalysisRequest:
    """Minimal structured request for legal pipeline analysis."""

    text: str
    expected_citations: tuple[str, ...] = field(default_factory=tuple)
    title: str = "document"
    rule_id: str = "RULE_CLAUSE_NORM_MINIMAL"


@dataclass(frozen=True)
class LegalAnalysisResponse:
    """Minimal structured response from legal pipeline analysis."""

    document_id: str
    decision_status: str
    alert_level: str
    justification: str
    comparison_count: int
    analyzed_clause_count: int
    recommended_action: str


def analyze_legal_text(request: LegalAnalysisRequest) -> LegalAnalysisResponse:
    """Run the legal pipeline from a plain-text request and return a compact response."""

    if not request.text or not request.text.strip():
        return LegalAnalysisResponse(
            document_id="",
            decision_status="insufficient_data",
            alert_level="unknown",
            justification="Request text is empty.",
            comparison_count=0,
            analyzed_clause_count=0,
            recommended_action="Provide a non-empty legal document text.",
        )

    document = load_text_content(request.text, title=request.title)

    expected_references: tuple[LegalReference, ...] = tuple(
        LegalReference(reference_id="", citation=citation, kind="loi")
        for citation in request.expected_citations
        if citation.strip()
    )

    result = run_legal_pipeline(
        document,
        expected_references,
        rule_id=request.rule_id,
    )

    return LegalAnalysisResponse(
        document_id=result.document_id,
        decision_status=result.decision.status,
        alert_level=result.decision.alert_level,
        justification=result.decision.justification,
        comparison_count=len(result.comparisons),
        analyzed_clause_count=len(result.analyzed_clauses),
        recommended_action=result.decision.recommended_action,
    )
