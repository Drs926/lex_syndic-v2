
"""Minimal interface API for MIG-010A / LEX-021."""

from .core import InterfaceRequest, InterfaceResponse, handle_request
from .legal_handler import (
    LegalAnalysisRequest,
    LegalAnalysisResponse,
    analyze_legal_text,
)

__all__ = [
    "InterfaceRequest",
    "InterfaceResponse",
    "handle_request",
    "LegalAnalysisRequest",
    "LegalAnalysisResponse",
    "analyze_legal_text",
]
