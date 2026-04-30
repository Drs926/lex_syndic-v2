"""Tests for MIG-009A minimal report module."""

import importlib

from lex_syndic.report import ReportSection, build_report, render_text


def test_report_package_importable() -> None:
    module = importlib.import_module("lex_syndic.report")
    assert module is not None


def test_build_minimal_report() -> None:
    report = build_report("Accord")

    assert report.title == "Accord"
    assert report.sections == ()


def test_build_report_without_sections() -> None:
    report = build_report("Sans section", sections=None)

    assert report.sections == ()
    assert render_text(report) == "# Sans section"


def test_build_report_with_sections_preserves_order() -> None:
    report = build_report(
        "Titre",
        sections=[
            ReportSection(title="B", content="beta"),
            ReportSection(title="A", content="alpha"),
        ],
    )

    assert tuple(section.title for section in report.sections) == ("B", "A")


def test_render_text_is_deterministic() -> None:
    report = build_report(
        "Rapport",
        sections=[ReportSection(title="Section", content="Contenu")],
    )

    expected = "# Rapport\n\n## Section\nContenu"
    assert render_text(report) == expected
    assert render_text(report) == expected


def test_render_text_with_empty_title_is_stable() -> None:
    report = build_report("", sections=[ReportSection(title="Section", content="Texte")])

    assert render_text(report) == "# \n\n## Section\nTexte"


def test_render_text_with_empty_content_is_stable() -> None:
    report = build_report("Rapport", sections=[ReportSection(title="Vide", content="")])

    assert render_text(report) == "# Rapport\n\n## Vide\n"


def test_report_module_has_no_retrieval_dependency() -> None:
    import lex_syndic.report.text as text_module

    public_names = [name for name in dir(text_module) if "retrieval" in name.lower()]
    assert public_names == []


def test_report_module_has_no_storage_dependency() -> None:
    import lex_syndic.report.text as text_module

    public_names = [name for name in dir(text_module) if "storage" in name.lower()]
    assert public_names == []
