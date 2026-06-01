"""Deterministic legal pipeline: analysis → comparison → rules [LEX-020]."""

from __future__ import annotations

from dataclasses import dataclass

from lex_syndic.analysis.enrichment import analyze_document
from lex_syndic.comparison.clause_norm import (
    ClauseNormComparison,
    ClauseNormComparisonContext,
    compare_clause_to_norm,
)
from lex_syndic.legal.models import AnalyzedClause, LegalDocument, LegalReference
from lex_syndic.rules.business_rules import (
    BusinessRuleDecision,
    evaluate_clause_norm_business_rule,
)


@dataclass(frozen=True)
class PipelineResult:
    """Immutable result of one deterministic legal pipeline run."""

    document_id: str
    analyzed_clauses: tuple[AnalyzedClause, ...]
    comparisons: tuple[ClauseNormComparison, ...]
    decision: BusinessRuleDecision


def run_legal_pipeline(
    document: LegalDocument,
    expected_references: tuple[LegalReference | str, ...],
    *,
    context: ClauseNormComparisonContext | None = None,
    rule_id: str = "RULE_CLAUSE_NORM_MINIMAL",
) -> PipelineResult:
    """Run the minimal legal pipeline on a document.

    Steps:
    1. Enrich the document with analysis (topic, references, risk level).
    2. If no expected references are provided, return an insufficient_data decision.
    3. Otherwise compare every analyzed clause against every expected reference.
    4. Evaluate the collected comparisons with the business rule engine.
    5. Return a PipelineResult.
    """

    enriched = analyze_document(document)
    analyzed_clauses: tuple[AnalyzedClause, ...] = getattr(
        enriched, "analyzed_clauses", ()
    )

    if not expected_references:
        decision = evaluate_clause_norm_business_rule((), rule_id=rule_id)
        return PipelineResult(
            document_id=document.document_id,
            analyzed_clauses=analyzed_clauses,
            comparisons=(),
            decision=decision,
        )

    comparisons: list[ClauseNormComparison] = []
    for clause in analyzed_clauses:
        for expected_reference in expected_references:
            comparison = compare_clause_to_norm(clause, expected_reference, context)
            comparisons.append(comparison)

    decision = evaluate_clause_norm_business_rule(
        tuple(comparisons), rule_id=rule_id
    )

    return PipelineResult(
        document_id=document.document_id,
        analyzed_clauses=analyzed_clauses,
        comparisons=tuple(comparisons),
        decision=decision,
    )
