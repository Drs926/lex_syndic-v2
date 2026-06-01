"""Deterministic clause-to-norm comparison for LEX-018."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from lex_syndic.legal.models import (
    AnalyzedClause,
    CanonicalTopic,
    Clause,
    LegalReference,
    RiskLevel,
)

ClauseNormStatus = Literal[
    "match",
    "missing_reference",
    "topic_mismatch",
    "risk_attention",
    "insufficient_data",
]
GapLevel = Literal["none", "low", "medium", "high", "unknown"]


@dataclass(frozen=True)
class ClauseNormComparisonContext:
    """Minimal local context for clause-to-norm comparison."""

    expected_topic: CanonicalTopic | None = None
    known_references: tuple[LegalReference, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ClauseNormComparison:
    """Local comparison result prepared for later rule evaluation."""

    clause_id: str
    reference_id: str
    citation: str
    status: ClauseNormStatus
    gap_level: GapLevel
    justification: str
    topic: CanonicalTopic | None = None
    risk_level: RiskLevel | None = None


def _normalize_reference(value: str) -> str:
    return "".join(character for character in value.upper() if character.isalnum())


def _expected_reference_parts(reference: LegalReference | str) -> tuple[str, str]:
    if isinstance(reference, LegalReference):
        return reference.reference_id, reference.citation
    if isinstance(reference, str):
        return "", reference
    return "", ""


def _target_reference_ids(target: Clause | AnalyzedClause) -> tuple[str, ...]:
    if isinstance(target, AnalyzedClause):
        return target.extracted_reference_ids
    return target.norm_reference_ids


def _target_topic(target: Clause | AnalyzedClause) -> CanonicalTopic:
    return target.topic


def _target_risk_level(target: Clause | AnalyzedClause) -> RiskLevel:
    if isinstance(target, AnalyzedClause):
        return target.risk_level
    return "unknown"


def _reference_matches(
    target_reference_ids: tuple[str, ...],
    expected_reference_id: str,
    expected_citation: str,
    known_references: tuple[LegalReference, ...],
) -> bool:
    if expected_reference_id and expected_reference_id in target_reference_ids:
        return True

    expected_normalized = _normalize_reference(expected_citation)
    if not expected_normalized:
        return False

    for reference in known_references:
        if reference.reference_id not in target_reference_ids:
            continue
        if _normalize_reference(reference.citation) == expected_normalized:
            return True
    return False


def compare_clause_to_norm(
    target: Clause | AnalyzedClause,
    expected_reference: LegalReference | str,
    context: ClauseNormComparisonContext | None = None,
) -> ClauseNormComparison:
    """Compare one analyzed clause signal against one expected norm reference."""

    context = context or ClauseNormComparisonContext()
    expected_reference_id, expected_citation = _expected_reference_parts(
        expected_reference
    )
    clause_id = getattr(target, "clause_id", "")

    if not isinstance(target, (Clause, AnalyzedClause)) or not clause_id:
        return ClauseNormComparison(
            clause_id=clause_id,
            reference_id=expected_reference_id,
            citation=expected_citation,
            status="insufficient_data",
            gap_level="unknown",
            justification="Target clause data is missing or invalid.",
        )
    if not expected_reference_id and not expected_citation:
        return ClauseNormComparison(
            clause_id=clause_id,
            reference_id="",
            citation="",
            status="insufficient_data",
            gap_level="unknown",
            justification="Expected norm reference is missing.",
            topic=_target_topic(target),
            risk_level=_target_risk_level(target),
        )

    topic = _target_topic(target)
    risk_level = _target_risk_level(target)
    if context.expected_topic is not None and topic != context.expected_topic:
        return ClauseNormComparison(
            clause_id=clause_id,
            reference_id=expected_reference_id,
            citation=expected_citation,
            status="topic_mismatch",
            gap_level="medium",
            justification="Clause topic does not match expected norm topic.",
            topic=topic,
            risk_level=risk_level,
        )

    has_reference = _reference_matches(
        _target_reference_ids(target),
        expected_reference_id,
        expected_citation,
        context.known_references,
    )
    if not has_reference:
        return ClauseNormComparison(
            clause_id=clause_id,
            reference_id=expected_reference_id,
            citation=expected_citation,
            status="missing_reference",
            gap_level="high",
            justification="Expected norm reference is not attached to the clause.",
            topic=topic,
            risk_level=risk_level,
        )

    if risk_level in {"medium", "high"}:
        return ClauseNormComparison(
            clause_id=clause_id,
            reference_id=expected_reference_id,
            citation=expected_citation,
            status="risk_attention",
            gap_level=risk_level,
            justification="Expected reference is present but risk level requires attention.",
            topic=topic,
            risk_level=risk_level,
        )

    return ClauseNormComparison(
        clause_id=clause_id,
        reference_id=expected_reference_id,
        citation=expected_citation,
        status="match",
        gap_level="none",
        justification="Expected norm reference is present for the clause.",
        topic=topic,
        risk_level=risk_level,
    )
