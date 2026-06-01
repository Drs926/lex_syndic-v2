"""Focused tests for LEX-019 minimal business rules."""

from __future__ import annotations

from lex_syndic.comparison import ClauseNormComparison
from lex_syndic.rules import (
    BusinessRuleDecision,
    evaluate_clause_norm_business_rule,
)


def _comparison(
    status: str,
    gap_level: str,
    *,
    clause_id: str = "clause-001",
    reference_id: str = "ref-001",
    citation: str = "L1222-9",
) -> ClauseNormComparison:
    return ClauseNormComparison(
        clause_id=clause_id,
        reference_id=reference_id,
        citation=citation,
        status=status,  # type: ignore[arg-type]
        gap_level=gap_level,  # type: ignore[arg-type]
        justification="fixture",
        topic="teletravail",
        risk_level="low",
    )


def test_business_rule_returns_compliant_for_all_matches() -> None:
    decision = evaluate_clause_norm_business_rule(
        (
            _comparison("match", "none", reference_id="ref-001"),
            _comparison("match", "none", reference_id="ref-002"),
        )
    )

    assert isinstance(decision, BusinessRuleDecision)
    assert decision.rule_id == "RULE_CLAUSE_NORM_MINIMAL"
    assert decision.status == "compliant"
    assert decision.alert_level == "none"
    assert decision.comparison_references == ("ref-001", "ref-002")
    assert decision.recommended_action == "No action required."


def test_business_rule_returns_non_compliant_for_missing_reference() -> None:
    decision = evaluate_clause_norm_business_rule(
        (_comparison("missing_reference", "high"),)
    )

    assert decision.status == "non_compliant"
    assert decision.alert_level == "high"
    assert decision.justification == "At least one expected norm reference is missing."
    assert decision.recommended_action == "Add or justify the missing norm reference."


def test_business_rule_returns_attention_for_risk_attention() -> None:
    decision = evaluate_clause_norm_business_rule(
        (_comparison("risk_attention", "medium"),)
    )

    assert decision.status == "attention_required"
    assert decision.alert_level == "medium"
    assert decision.justification == "At least one matched reference carries a risk signal."


def test_business_rule_returns_attention_for_topic_mismatch() -> None:
    decision = evaluate_clause_norm_business_rule(
        (_comparison("topic_mismatch", "medium"),)
    )

    assert decision.status == "attention_required"
    assert decision.alert_level == "medium"
    assert (
        decision.recommended_action
        == "Review clause classification against the expected norm topic."
    )


def test_business_rule_returns_insufficient_data_for_empty_or_invalid_input() -> None:
    empty_decision = evaluate_clause_norm_business_rule(())
    invalid_decision = evaluate_clause_norm_business_rule(("invalid",))  # type: ignore[arg-type]

    assert empty_decision.status == "insufficient_data"
    assert empty_decision.alert_level == "unknown"
    assert empty_decision.comparison_references == ()
    assert invalid_decision.status == "insufficient_data"


def test_business_rule_prioritizes_severity_across_multiple_comparisons() -> None:
    decision = evaluate_clause_norm_business_rule(
        (
            _comparison("match", "none", reference_id="ref-ok"),
            _comparison("risk_attention", "medium", reference_id="ref-risk"),
            _comparison("missing_reference", "high", reference_id="ref-missing"),
        )
    )

    assert decision.status == "non_compliant"
    assert decision.alert_level == "high"
    assert decision.comparison_references == ("ref-ok", "ref-risk", "ref-missing")


def test_business_rule_uses_citation_when_reference_id_is_missing() -> None:
    decision = evaluate_clause_norm_business_rule(
        (
            _comparison(
                "match",
                "none",
                reference_id="",
                citation="L3121-1",
            ),
        )
    )

    assert decision.status == "compliant"
    assert decision.comparison_references == ("L3121-1",)
