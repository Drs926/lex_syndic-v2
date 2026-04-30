"""Tests for MIG-007A minimal lexical retrieval."""

from lex_syndic.legal.models import Clause, LegalDocument
from lex_syndic.retrieval import LexicalRetrievalIndex


def test_query_with_match_returns_ranked_results() -> None:
    index = LexicalRetrievalIndex(
        [
            LegalDocument(document_id="doc-1", text="teletravail teletravail accord"),
            LegalDocument(document_id="doc-2", text="accord travail hybride"),
        ]
    )

    results = index.search("teletravail accord")

    assert tuple(result.item_id for result in results) == ("doc-1", "doc-2")
    assert results[0].score == 3
    assert results[1].score == 1


def test_query_without_match_returns_empty_tuple() -> None:
    index = LexicalRetrievalIndex(
        [LegalDocument(document_id="doc-1", text="temps de travail")]
    )

    results = index.search("prime")

    assert results == ()


def test_ranking_is_deterministic_for_same_score() -> None:
    index = LexicalRetrievalIndex(
        [
            Clause(clause_id="clause-b", content="prime annuelle"),
            Clause(clause_id="clause-a", content="prime annuelle"),
        ]
    )

    results = index.search("prime")

    assert tuple(result.item_id for result in results) == ("clause-a", "clause-b")


def test_empty_or_low_signal_query_returns_empty_tuple() -> None:
    index = LexicalRetrievalIndex(
        [LegalDocument(document_id="doc-1", text="teletravail accord")]
    )

    assert index.search("") == ()
    assert index.search("   ") == ()
    assert index.search("...") == ()


def test_package_export_is_importable() -> None:
    index = LexicalRetrievalIndex(
        [Clause(clause_id="clause-1", content="formation professionnelle")]
    )

    results = index.search("formation")

    assert len(results) == 1
    assert results[0].item_type == "clause"
