"""Minimal deterministic business rules for LEX-019."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

from lex_syndic.comparison import ClauseNormComparison

BusinessRuleStatus = Literal[
    "compliant",
    "attention_required",
    "non_compliant",
    "insufficient_data",
]
BusinessAlertLevel = Literal["none", "low", "medium", "high", "unknown"]

_ALERT_PRIORITY: dict[BusinessAlertLevel, int] = {
    "none": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "unknown": -1,
}


@dataclass(frozen=True)
class BusinessRuleDecision:
    """Local deterministic decision produced from clause-norm comparisons."""

    rule_id: str
    status: BusinessRuleStatus
    alert_level: BusinessAlertLevel
    justification: str
    comparison_references: tuple[str, ...]
    recommended_action: str


def _comparison_reference(comparison: ClauseNormComparison) -> str:
    if comparison.reference_id:
        return comparison.reference_id
    if comparison.citation:
        return comparison.citation
    return comparison.clause_id


def _highest_alert(levels: Iterable[BusinessAlertLevel]) -> BusinessAlertLevel:
    highest: BusinessAlertLevel = "unknown"
    for level in levels:
        if _ALERT_PRIORITY[level] > _ALERT_PRIORITY[highest]:
            highest = level
    return highest


def evaluate_clause_norm_business_rule(
    comparisons: tuple[ClauseNormComparison, ...],
    *,
    rule_id: str = "RULE_CLAUSE_NORM_MINIMAL",
) -> BusinessRuleDecision:
    """Evaluate a minimal business decision from clause-to-norm comparisons."""

    if not comparisons or not all(
        isinstance(comparison, ClauseNormComparison) for comparison in comparisons
    ):
        return BusinessRuleDecision(
            rule_id=rule_id,
            status="insufficient_data",
            alert_level="unknown",
            justification="No valid clause-norm comparison was provided.",
            comparison_references=(),
            recommended_action="Provide at least one valid clause-norm comparison.",
        )

    comparison_references = tuple(
        _comparison_reference(comparison) for comparison in comparisons
    )

    if any(comparison.status == "insufficient_data" for comparison in comparisons):
        return BusinessRuleDecision(
            rule_id=rule_id,
            status="insufficient_data",
            alert_level="unknown",
            justification="At least one comparison has insufficient data.",
            comparison_references=comparison_references,
            recommended_action="Complete clause analysis and expected reference data.",
        )

    if any(comparison.status == "missing_reference" for comparison in comparisons):
        return BusinessRuleDecision(
            rule_id=rule_id,
            status="non_compliant",
            alert_level="high",
            justification="At least one expected norm reference is missing.",
            comparison_references=comparison_references,
            recommended_action="Add or justify the missing norm reference.",
        )

    if any(comparison.status == "topic_mismatch" for comparison in comparisons):
        alert_level = _highest_alert(
            comparison.gap_level
            for comparison in comparisons
            if comparison.status == "topic_mismatch"
        )
        return BusinessRuleDecision(
            rule_id=rule_id,
            status="attention_required",
            alert_level=alert_level if alert_level != "unknown" else "medium",
            justification="At least one clause topic differs from the expected norm topic.",
            comparison_references=comparison_references,
            recommended_action="Review clause classification against the expected norm topic.",
        )

    if any(comparison.status == "risk_attention" for comparison in comparisons):
        alert_level = _highest_alert(
            comparison.gap_level
            for comparison in comparisons
            if comparison.status == "risk_attention"
        )
        return BusinessRuleDecision(
            rule_id=rule_id,
            status="attention_required",
            alert_level=alert_level if alert_level != "unknown" else "medium",
            justification="At least one matched reference carries a risk signal.",
            comparison_references=comparison_references,
            recommended_action="Review the risky matched clause before validation.",
        )

    if all(
        comparison.status == "match" and comparison.gap_level == "none"
        for comparison in comparisons
    ):
        return BusinessRuleDecision(
            rule_id=rule_id,
            status="compliant",
            alert_level="none",
            justification="All expected norm references are matched without gap.",
            comparison_references=comparison_references,
            recommended_action="No action required.",
        )

    return BusinessRuleDecision(
        rule_id=rule_id,
        status="insufficient_data",
        alert_level="unknown",
        justification="Comparison statuses are not sufficient for a deterministic decision.",
        comparison_references=comparison_references,
        recommended_action="Review comparison statuses before rule evaluation.",
    )
