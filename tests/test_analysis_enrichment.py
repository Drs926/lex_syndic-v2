"""Focused tests for LEX-017 deterministic analysis enrichment."""

from __future__ import annotations

import pytest

from lex_syndic.analysis import analyze_clause, analyze_document
from lex_syndic.ingestion import load_text_content
from lex_syndic.legal.models import AnalyzedClause, Clause, LegalReference


def test_analyze_clause_extracts_legal_reference_and_analyzed_clause() -> None:
    clause = Clause(
        clause_id="clause-001",
        document_id="doc-001",
        content="Le teletravail est encadre par l'article L. 1222-9 du Code du travail.",
    )

    analyzed_clause, references = analyze_clause(clause)

    assert isinstance(analyzed_clause, AnalyzedClause)
    assert analyzed_clause.analysis_id == "clause-001-analysis"
    assert analyzed_clause.clause_id == "clause-001"
    assert analyzed_clause.document_id == "doc-001"
    assert analyzed_clause.topic == "teletravail"
    assert analyzed_clause.risk_level == "medium"
    assert analyzed_clause.extracted_reference_ids == ("clause-001-ref-001",)
    assert analyzed_clause.summary == "topic=teletravail; references=1; risk_level=medium"
    assert references == (
        LegalReference(
            reference_id="clause-001-ref-001",
            citation="L1222-9",
            kind="loi",
        ),
    )


def test_analyze_clause_deduplicates_repeated_references() -> None:
    clause = Clause(
        clause_id="clause-002",
        document_id="doc-001",
        content="Voir article L. 1222-9 et article L1222-9.",
    )

    analyzed_clause, references = analyze_clause(clause)

    assert len(references) == 1
    assert analyzed_clause.extracted_reference_ids == ("clause-002-ref-001",)


def test_analyze_clause_classifies_core_topics() -> None:
    examples = (
        ("Le salaire comprend une prime annuelle.", "remuneration"),
        ("Les conges payes sont organises par service.", "conges"),
        ("La formation professionnelle est planifiee.", "formation"),
        ("La sante et securite font l'objet d'une prevention.", "sante_securite"),
        ("L'egalite professionnelle interdit toute discrimination.", "egalite_professionnelle"),
    )

    for content, expected_topic in examples:
        analyzed_clause, _ = analyze_clause(
            Clause(clause_id=f"clause-{expected_topic}", content=content)
        )

        assert analyzed_clause.topic == expected_topic


def test_analyze_clause_assigns_high_risk_for_disciplinary_signal() -> None:
    clause = Clause(
        clause_id="clause-003",
        document_id="doc-001",
        content="Une sanction peut aller jusqu'au licenciement sans preavis.",
    )

    analyzed_clause, references = analyze_clause(clause)

    assert analyzed_clause.topic == "discipline"
    assert analyzed_clause.risk_level == "high"
    assert references == ()


def test_analyze_document_segments_when_needed_and_attaches_analysis() -> None:
    document = load_text_content(
        "Article 1\nLe temps de travail doit respecter l'article L. 3121-1.\n\n"
        "Article 2\nUne prime annuelle est versee.",
        title="Accord test",
    )

    analyzed_document = analyze_document(document)

    assert len(analyzed_document.clauses) == 2
    assert [item.topic for item in analyzed_document.analyzed_clauses] == [
        "temps_travail",
        "remuneration",
    ]
    assert [item.risk_level for item in analyzed_document.analyzed_clauses] == [
        "medium",
        "low",
    ]
    assert [reference.citation for reference in analyzed_document.legal_references] == [
        "L3121-1"
    ]


def test_analyze_document_preserves_existing_segmentation_order() -> None:
    document = load_text_content("Clause A\n\nClause B", title="Ordre")
    clauses = (
        Clause(clause_id="custom-002", document_id=document.document_id, content="Prime"),
        Clause(clause_id="custom-001", document_id=document.document_id, content="Teletravail"),
    )
    object.__setattr__(document, "clauses", clauses)

    analyzed_document = analyze_document(document)

    assert [item.clause_id for item in analyzed_document.analyzed_clauses] == [
        "custom-002",
        "custom-001",
    ]


def test_analyze_document_rejects_invalid_runtime_clauses() -> None:
    document = load_text_content("Texte", title="Invalid")
    object.__setattr__(document, "clauses", ("not-a-clause",))

    with pytest.raises(ValueError, match="document must expose segmented clauses"):
        analyze_document(document)
