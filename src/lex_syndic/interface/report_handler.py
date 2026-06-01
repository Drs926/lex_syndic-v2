"""Legal analysis with readable report, combined in one call [LEX-024]."""

from __future__ import annotations

from dataclasses import dataclass

from lex_syndic.interface.legal_handler import (
    LegalAnalysisRequest,
    LegalAnalysisResponse,
    analyze_legal_text,
)
from lex_syndic.report.legal_formatter import format_legal_report


@dataclass(frozen=True)
class LegalAnalysisWithReportResponse:
    """Combined structured response and readable text report."""

    analysis: LegalAnalysisResponse
    report_text: str


def analyze_legal_text_with_report(
    request: LegalAnalysisRequest,
) -> LegalAnalysisWithReportResponse:
    """Run legal analysis and return both structured response and readable report."""

    analysis = analyze_legal_text(request)
    report_text = format_legal_report(analysis)
    return LegalAnalysisWithReportResponse(analysis=analysis, report_text=report_text)
