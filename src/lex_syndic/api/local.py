"""Local single-user API wrapper — pure Python, no HTTP server [LEX-030].

Limits accepted (DEC-035):
- Single-user only.
- No authentication.
- No thread-safety.
- No disk persistence.
- No UUID — record_id is monotone per store instance.
- No external dependency.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from lex_syndic.interface import LegalAnalysisRequest, analyze_and_store_legal_text
from lex_syndic.storage.legal_results import InMemoryLegalResultStore


@dataclass(frozen=True)
class LocalApiAnalysisRequest:
    """Flat API-level request for legal analysis."""

    text: str
    expected_citations: tuple[str, ...] = field(default_factory=tuple)
    title: str = "document"


@dataclass(frozen=True)
class LocalApiAnalysisResponse:
    """Flat API-level response with record identifier and analysis summary."""

    record_id: str
    decision_status: str
    alert_level: str
    report_text: str
    recommended_action: str


def submit_analysis(
    request: LocalApiAnalysisRequest,
    store: InMemoryLegalResultStore,
) -> LocalApiAnalysisResponse:
    """Convert a local API request, run analysis, store result, return flat response.

    The caller owns the store — no global store is created here.
    """

    legal_request = LegalAnalysisRequest(
        text=request.text,
        expected_citations=request.expected_citations,
        title=request.title,
    )
    session = analyze_and_store_legal_text(legal_request, store)

    return LocalApiAnalysisResponse(
        record_id=session.record_id,
        decision_status=session.result.analysis.decision_status,
        alert_level=session.result.analysis.alert_level,
        report_text=session.result.report_text,
        recommended_action=session.result.analysis.recommended_action,
    )
