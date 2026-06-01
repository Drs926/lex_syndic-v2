"""Session flow combining legal analysis and in-memory storage [LEX-027]."""

from __future__ import annotations

from dataclasses import dataclass

from lex_syndic.interface.report_handler import (
    LegalAnalysisRequest,
    LegalAnalysisWithReportResponse,
    analyze_legal_text_with_report,
)
from lex_syndic.storage.legal_results import InMemoryLegalResultStore


@dataclass(frozen=True)
class LegalSessionResult:
    """Record id and full result returned by a session analysis call."""

    record_id: str
    result: LegalAnalysisWithReportResponse


def analyze_and_store_legal_text(
    request: LegalAnalysisRequest,
    store: InMemoryLegalResultStore,
) -> LegalSessionResult:
    """Run legal analysis with report and persist result in the given store."""

    result = analyze_legal_text_with_report(request)
    record_id = store.save(result)
    return LegalSessionResult(record_id=record_id, result=result)
