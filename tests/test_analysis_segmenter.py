"""Focused tests for MIG-004 minimal clause segmentation."""

from __future__ import annotations

from lex_syndic.analysis import segment_document
from lex_syndic.ingestion import load_text_content

import pytest


def test_segment_document_splits_paragraphs() -> None:
    document = load_text_content(
        "Bloc 1\nligne A\n\nBloc 2\nligne B", title="Segmentation"
    )

    segmented = segment_document(document)

    assert len(segmented.clauses) == 2
    assert segmented.clauses[0].content == "Bloc 1\nligne A"
    assert segmented.clauses[1].content == "Bloc 2\nligne B"


def test_segment_document_preserves_order() -> None:
    document = load_text_content("Premier\n\nDeuxieme\n\nTroisieme", title="Ordre")

    segmented = segment_document(document)

    contents = [clause.content for clause in segmented.clauses]
    assert contents == ["Premier", "Deuxieme", "Troisieme"]


def test_segment_document_ignores_empty_blocks() -> None:
    document = load_text_content("A\n\n\n\nB\n\n", title="Vides")

    segmented = segment_document(document)

    assert [clause.content for clause in segmented.clauses] == ["A", "B"]


def test_segment_document_generates_stable_identifiers() -> None:
    document = load_text_content("A\n\nB", title="Ids", source_path="fixture.txt")

    segmented = segment_document(document)

    assert [clause.clause_id for clause in segmented.clauses] == [
        f"{document.document_id}-clause-001",
        f"{document.document_id}-clause-002",
    ]


def test_segment_document_rejects_document_without_usable_text() -> None:
    document = load_text_content("Texte", title="Base")
    object.__setattr__(document, "text", "   ")

    with pytest.raises(ValueError, match="document text must not be empty"):
        segment_document(document)


def test_segment_document_does_not_perform_legal_analysis() -> None:
    document = load_text_content("Article 1\nContenu simple", title="Neutre")

    segmented = segment_document(document)
    clause = segmented.clauses[0]

    assert clause.topic == "autre"
    assert clause.compliance_status == "unknown"
    assert clause.norm_reference_ids == ()


def test_segment_document_is_compatible_with_load_text_content() -> None:
    document = load_text_content("Ligne 1\nLigne 2", title="Compat")

    segmented = segment_document(document)

    assert segmented.title == "Compat"
    assert len(segmented.clauses) == 2
    assert [clause.content for clause in segmented.clauses] == ["Ligne 1", "Ligne 2"]
