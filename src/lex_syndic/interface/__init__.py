
"""Minimal interface API for MIG-010A / LEX-021 / LEX-024."""

from .core import InterfaceRequest, InterfaceResponse, handle_request
from .legal_handler import (
    LegalAnalysisRequest,
    LegalAnalysisResponse,
    analyze_legal_text,
)
from .report_handler import (
    LegalAnalysisWithReportResponse,
    analyze_legal_text_with_report,
)
from .session_handler import LegalSessionResult, analyze_and_store_legal_text

__all__ = [
    "InterfaceRequest",
    "InterfaceResponse",
    "handle_request",
    "LegalAnalysisRequest",
    "LegalAnalysisResponse",
    "analyze_legal_text",
    "LegalAnalysisWithReportResponse",
    "analyze_legal_text_with_report",
    "LegalSessionResult",
    "analyze_and_store_legal_text",
]
