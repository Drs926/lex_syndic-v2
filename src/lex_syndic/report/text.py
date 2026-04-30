"""Deterministic text report helpers for MIG-009A."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReportSection:
    """One report section with stable text content."""

    title: str = ""
    content: str = ""


@dataclass(frozen=True)
class Report:
    """Minimal report structure with ordered sections."""

    title: str = ""
    sections: tuple[ReportSection, ...] = field(default_factory=tuple)


def build_report(
    title: str, sections: list[ReportSection] | tuple[ReportSection, ...] | None = None
) -> Report:
    """Build a deterministic report from ordered sections."""

    normalized_sections = tuple(sections or ())
    return Report(title=title, sections=normalized_sections)


def render_text(report: Report) -> str:
    """Render a report to a stable plain-text representation."""

    lines = [f"# {report.title}"]
    for section in report.sections:
        lines.append("")
        lines.append(f"## {section.title}")
        lines.append(section.content)
    return "\n".join(lines)
