"""Focused tests for LEX-018 clause-to-norm comparison."""

from __future__ import annotations

from lex_syndic.comparison import (
    ClauseNormComparisonContext,
    compare_clause_to_norm,
)
from lex_syndic.legal.models import AnalyzedClause, Clause, LegalReference


def test_compare_clause_to_norm_matches_present_reference() -> None:
    expected = LegalReference(
        reference_id="ref-001",
        citation="L1222-9",
        kind="loi",
    )
    analyzed_clause = AnalyzedClause(
        clause_id="clause-001",
        document_id="doc-001",
        topic="teletravail",
        extracted_reference_ids=("ref-001",),
        risk_level="low",
    )

    result = compare_clause_to_norm(
        analyzed_clause,
        expected,
        ClauseNormComparisonContext(
            expected_topic="teletravail",
            known_references=(expected,),
        ),
    )

    assert result.clause_id == "clause-001"
    assert result.reference_id == "ref-001"
    assert result.citation == "L1222-9"
    assert result.status == "match"
    assert result.gap_level == "none"
    assert result.topic == "teletravail"
    assert result.risk_level == "low"
    assert result.justification == "Expected norm reference is present for the clause."


def test_compare_clause_to_norm_reports_missing_reference() -> None:
    analyzed_clause = AnalyzedClause(
        clause_id="clause-002",
        document_id="doc-001",
        topic="teletravail",
        extracted_reference_ids=("ref-other",),
        risk_level="low",
    )

    result = compare_clause_to_norm(
        analyzed_clause,
        LegalReference(reference_id="ref-expected", citation="L1222-9", kind="loi"),
        ClauseNormComparisonContext(expected_topic="teletravail"),
    )

    assert result.status == "missing_reference"
    assert result.gap_level == "high"
    assert result.justification == "Expected norm reference is not attached to the clause."


def test_compare_clause_to_norm_reports_topic_mismatch() -> None:
    analyzed_clause = AnalyzedClause(
        clause_id="clause-003",
        document_id="doc-001",
        topic="remuneration",
        extracted_reference_ids=("ref-001",),
        risk_level="low",
    )

    result = compare_clause_to_norm(
        analyzed_clause,
        LegalReference(reference_id="ref-001", citation="L1222-9", kind="loi"),
        ClauseNormComparisonContext(expected_topic="teletravail"),
    )

    assert result.status == "topic_mismatch"
    assert result.gap_level == "medium"
    assert result.topic == "remuneration"


def test_compare_clause_to_norm_reports_risk_attention() -> None:
    expected = LegalReference(
        reference_id="ref-004",
        citation="L3121-1",
        kind="loi",
    )
    analyzed_clause = AnalyzedClause(
        clause_id="clause-004",
        document_id="doc-001",
        topic="temps_travail",
        extracted_reference_ids=("ref-004",),
        risk_level="high",
    )

    result = compare_clause_to_norm(
        analyzed_clause,
        expected,
        ClauseNormComparisonContext(
            expected_topic="temps_travail",
            known_references=(expected,),
        ),
    )

    assert result.status == "risk_attention"
    assert result.gap_level == "high"
    assert result.risk_level == "high"
    assert (
        result.justification
        == "Expected reference is present but risk level requires attention."
    )


def test_compare_clause_to_norm_reports_insufficient_data() -> None:
    result = compare_clause_to_norm(
        Clause(),
        LegalReference(reference_id="ref-005", citation="L1222-9", kind="loi"),
    )

    assert result.status == "insufficient_data"
    assert result.gap_level == "unknown"
    assert result.justification == "Target clause data is missing or invalid."


def test_compare_clause_to_norm_accepts_clause_reference_ids() -> None:
    clause = Clause(
        clause_id="clause-006",
        document_id="doc-001",
        topic="teletravail",
        norm_reference_ids=("ref-006",),
    )

    result = compare_clause_to_norm(
        clause,
        LegalReference(reference_id="ref-006", citation="L1222-9", kind="loi"),
        ClauseNormComparisonContext(expected_topic="teletravail"),
    )

    assert result.status == "match"
    assert result.risk_level == "unknown"
