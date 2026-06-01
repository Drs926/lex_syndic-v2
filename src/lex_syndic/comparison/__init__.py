
"""Minimal structural comparison for MIG-005."""

from lex_syndic.comparison.clause_norm import (
    ClauseNormComparison,
    ClauseNormComparisonContext,
    compare_clause_to_norm,
)
from lex_syndic.comparison.simple_comparator import compare_documents

__all__ = [
    "ClauseNormComparison",
    "ClauseNormComparisonContext",
    "compare_clause_to_norm",
    "compare_documents",
]
