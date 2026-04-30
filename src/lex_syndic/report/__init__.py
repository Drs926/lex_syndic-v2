"""Minimal report API for MIG-009A."""

from .text import Report, ReportSection, build_report, render_text

__all__ = ["Report", "ReportSection", "build_report", "render_text"]
