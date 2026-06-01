"""Minimal report API for MIG-009A / LEX-023."""

from .legal_formatter import format_legal_report
from .text import Report, ReportSection, build_report, render_text

__all__ = [
    "Report",
    "ReportSection",
    "build_report",
    "render_text",
    "format_legal_report",
]
