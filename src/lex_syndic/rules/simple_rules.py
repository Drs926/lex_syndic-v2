"""Minimal deterministic rule checks for MIG-006.

The rules layer stays intentionally small in this migration lot:
- no legal extraction;
- no external corpus;
- no probabilistic scoring.
"""

from __future__ import annotations

from lex_syndic.legal.models import Clause, LegalDocument, RuleCheckResult


def _normalize_content(content: str) -> str:
    """Collapse whitespace to keep the rules deterministic."""

    return " ".join(content.split())


def _alnum_length(content: str) -> int:
    """Measure exploitable signal with a stable character count."""

    return sum(1 for character in content if character.isalnum())


def evaluate_clause_rule(clause: Clause) -> RuleCheckResult:
    """Return one canonical deterministic rule result for one clause."""

    normalized_content = _normalize_content(clause.content)
    result_id = f"rule-check:{clause.clause_id or 'unknown'}"

    if clause.compliance_status != "unknown":
        return RuleCheckResult(
            result_id=result_id,
            clause_id=clause.clause_id,
            rule_code="RULE_STATUS_MAPPING",
            outcome=clause.compliance_status,
            message=(
                "Outcome derived deterministically from clause compliance_status."
            ),
        )

    if not normalized_content:
        return RuleCheckResult(
            result_id=result_id,
            clause_id=clause.clause_id,
            rule_code="RULE_EMPTY_CLAUSE",
            outcome="non_conforme",
            message="Clause content is empty after whitespace normalization.",
        )

    if _alnum_length(normalized_content) < 5:
        return RuleCheckResult(
            result_id=result_id,
            clause_id=clause.clause_id,
            rule_code="RULE_LOW_SIGNAL_CLAUSE",
            outcome="risque",
            message="Clause content is too short to be exploitable deterministically.",
        )

    return RuleCheckResult(
        result_id=result_id,
        clause_id=clause.clause_id,
        rule_code="RULE_MIN_CONTENT_PRESENT",
        outcome="conforme",
        message="Clause content satisfies the minimal deterministic content rule.",
    )


def evaluate_document_rules(document: LegalDocument) -> tuple[RuleCheckResult, ...]:
    """Evaluate all runtime clauses attached to one document."""

    clauses = getattr(document, "clauses", ())
    return tuple(evaluate_clause_rule(clause) for clause in clauses)
