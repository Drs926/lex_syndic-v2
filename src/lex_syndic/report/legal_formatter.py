"""Minimal legal proof report formatter for LEX-023.

Converts a LegalAnalysisResponse into a short, stable, plain-text report.
No business logic — formatting only.
"""

from __future__ import annotations

from lex_syndic.interface.legal_handler import LegalAnalysisResponse
from lex_syndic.report.text import ReportSection, build_report, render_text

_TITLE = "Rapport juridique minimal"


def format_legal_report(response: LegalAnalysisResponse) -> str:
    """Format a LegalAnalysisResponse as a short deterministic plain-text report."""

    sections = (
        ReportSection(title="Statut", content=response.decision_status),
        ReportSection(title="Niveau d'alerte", content=response.alert_level),
        ReportSection(title="Justification", content=response.justification),
        ReportSection(title="Action recommandée", content=response.recommended_action),
        ReportSection(
            title="Clauses analysées",
            content=str(response.analyzed_clause_count),
        ),
        ReportSection(
            title="Comparaisons réalisées",
            content=str(response.comparison_count),
        ),
    )
    return render_text(build_report(_TITLE, sections=sections))
