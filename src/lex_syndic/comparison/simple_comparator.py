"""Minimal deterministic clause comparison for MIG-005.

This module stays intentionally narrow:
- two already segmented LegalDocument instances
- structural comparison only
- no legal interpretation
- no external dependencies
"""

from __future__ import annotations

from itertools import zip_longest

from lex_syndic.legal.models import Clause, ComparisonResult, LegalDocument


def _normalize_clause_text(content: str) -> str:
    """Normalize clause text with a strict deterministic rule."""

    return "\n".join(line.strip() for line in content.replace("\r", "").split("\n")).strip()


def _get_document_clauses(document: LegalDocument) -> tuple[Clause, ...]:
    """Read the runtime clause contract established by MIG-004."""

    clauses = getattr(document, "clauses", None)
    if not isinstance(clauses, tuple) or not all(
        isinstance(clause, Clause) for clause in clauses
    ):
        raise ValueError("document must expose segmented clauses as a tuple of Clause")
    if not clauses:
        raise ValueError("document must expose at least one segmented clause")
    return clauses


def _compare_clause_pair(
    index: int,
    reference_clause: Clause | None,
    candidate_clause: Clause | None,
) -> ComparisonResult:
    """Compare one clause position without semantic interpretation."""

    result_id = f"cmp-{index:03d}"
    if reference_clause is None and candidate_clause is not None:
        return ComparisonResult(
            result_id=result_id,
            reference_clause_id="",
            proposal_clause_id=candidate_clause.clause_id,
            comparison_type="added",
            risk_level="unknown",
        )
    if reference_clause is not None and candidate_clause is None:
        return ComparisonResult(
            result_id=result_id,
            reference_clause_id=reference_clause.clause_id,
            proposal_clause_id="",
            comparison_type="removed",
            risk_level="unknown",
        )
    if reference_clause is None or candidate_clause is None:
        raise ValueError("clause comparison requires at least one clause")

    comparison_type = (
        "unchanged"
        if _normalize_clause_text(reference_clause.content)
        == _normalize_clause_text(candidate_clause.content)
        else "rephrased"
    )
    return ComparisonResult(
        result_id=result_id,
        reference_clause_id=reference_clause.clause_id,
        proposal_clause_id=candidate_clause.clause_id,
        comparison_type=comparison_type,
        risk_level="unknown",
    )


def _summarize(entries: tuple[ComparisonResult, ...]) -> str:
    """Build one narrow top-level status from positional entries."""

    entry_types = {entry.comparison_type for entry in entries}
    if entry_types == {"unchanged"}:
        return "unchanged"
    if len(entry_types) == 1:
        return next(iter(entry_types))
    return "unknown"


def compare_documents(
    reference: LegalDocument, candidate: LegalDocument
) -> ComparisonResult:
    """Compare two segmented documents position by position.

    The returned object is the canonical ComparisonResult placeholder from MIG-002.
    Detailed structural entries are attached as a tested runtime attribute because
    the canonical collection model is intentionally deferred to a later lot.
    """

    reference_clauses = _get_document_clauses(reference)
    candidate_clauses = _get_document_clauses(candidate)

    entries = tuple(
        _compare_clause_pair(index, reference_clause, candidate_clause)
        for index, (reference_clause, candidate_clause) in enumerate(
            zip_longest(reference_clauses, candidate_clauses),
            start=1,
        )
    )
    result = ComparisonResult(
        result_id=f"{reference.document_id}__{candidate.document_id}",
        reference_clause_id=reference_clauses[0].clause_id,
        proposal_clause_id=candidate_clauses[0].clause_id,
        comparison_type=_summarize(entries),
        risk_level="unknown",
    )
    object.__setattr__(result, "entries", entries)
    object.__setattr__(result, "reference_document_id", reference.document_id)
    object.__setattr__(result, "candidate_document_id", candidate.document_id)
    return result
