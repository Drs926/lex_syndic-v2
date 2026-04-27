"""Focused tests for MIG-005 minimal clause comparison."""

from __future__ import annotations

from lex_syndic.analysis import segment_document
from lex_syndic.comparison import compare_documents
from lex_syndic.ingestion import load_text_content

import pytest


def _make_segmented_document(content: str, *, title: str):
    return segment_document(load_text_content(content, title=title))


def test_compare_documents_marks_identical_documents_as_unchanged() -> None:
    reference = _make_segmented_document("Alpha\n\nBeta", title="Reference")
    candidate = _make_segmented_document("Alpha\n\nBeta", title="Candidate")

    result = compare_documents(reference, candidate)

    assert result.comparison_type == "unchanged"
    assert [entry.comparison_type for entry in result.entries] == [
        "unchanged",
        "unchanged",
    ]


def test_compare_documents_marks_modified_clause_as_rephrased() -> None:
    reference = _make_segmented_document("Alpha\n\nBeta", title="Reference")
    candidate = _make_segmented_document("Alpha\n\nBeta modifie", title="Candidate")

    result = compare_documents(reference, candidate)

    assert [entry.comparison_type for entry in result.entries] == [
        "unchanged",
        "rephrased",
    ]


def test_compare_documents_marks_added_clause() -> None:
    reference = _make_segmented_document("Alpha", title="Reference")
    candidate = _make_segmented_document("Alpha\n\nBeta", title="Candidate")

    result = compare_documents(reference, candidate)

    assert [entry.comparison_type for entry in result.entries] == [
        "unchanged",
        "added",
    ]
    assert result.entries[1].proposal_clause_id.endswith("-clause-002")


def test_compare_documents_marks_removed_clause() -> None:
    reference = _make_segmented_document("Alpha\n\nBeta", title="Reference")
    candidate = _make_segmented_document("Alpha", title="Candidate")

    result = compare_documents(reference, candidate)

    assert [entry.comparison_type for entry in result.entries] == [
        "unchanged",
        "removed",
    ]
    assert result.entries[1].reference_clause_id.endswith("-clause-002")


def test_compare_documents_preserves_clause_order() -> None:
    reference = _make_segmented_document("A\n\nB\n\nC", title="Reference")
    candidate = _make_segmented_document("A\n\nB change\n\nC", title="Candidate")

    result = compare_documents(reference, candidate)

    assert [entry.result_id for entry in result.entries] == [
        "cmp-001",
        "cmp-002",
        "cmp-003",
    ]
    assert [entry.comparison_type for entry in result.entries] == [
        "unchanged",
        "rephrased",
        "unchanged",
    ]


def test_compare_documents_is_compatible_with_ingestion_and_segmentation() -> None:
    reference = _make_segmented_document("Bloc 1\n\nBloc 2", title="Ref")
    candidate = _make_segmented_document("Bloc 1\n\nBloc 2", title="Cand")

    result = compare_documents(reference, candidate)

    assert result.reference_document_id == reference.document_id
    assert result.candidate_document_id == candidate.document_id
    assert len(result.entries) == 2


def test_compare_documents_does_not_perform_legal_rules_or_risk_scoring() -> None:
    reference = _make_segmented_document("Article 1\nContenu", title="Reference")
    candidate = _make_segmented_document("Article 1\nContenu adapte", title="Candidate")

    result = compare_documents(reference, candidate)

    assert result.risk_level == "unknown"
    assert all(entry.risk_level == "unknown" for entry in result.entries)


def test_compare_documents_requires_segmented_documents() -> None:
    reference = load_text_content("Alpha", title="Reference")
    candidate = load_text_content("Alpha", title="Candidate")

    with pytest.raises(
        ValueError,
        match="document must expose segmented clauses as a tuple of Clause",
    ):
        compare_documents(reference, candidate)
