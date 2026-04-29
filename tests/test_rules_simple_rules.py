"""Tests for the minimal deterministic rules layer introduced in MIG-006."""

from lex_syndic.legal.models import Clause, LegalDocument, RuleCheckResult
from lex_syndic.rules import evaluate_clause_rule, evaluate_document_rules


def test_evaluate_clause_rule_maps_existing_compliance_status() -> None:
    clause = Clause(
        clause_id="clause-1",
        content="Le teletravail est ouvert a tous.",
        compliance_status="risque",
    )

    result = evaluate_clause_rule(clause)

    assert isinstance(result, RuleCheckResult)
    assert result.clause_id == "clause-1"
    assert result.rule_code == "RULE_STATUS_MAPPING"
    assert result.outcome == "risque"


def test_evaluate_clause_rule_marks_empty_clause_non_conforme() -> None:
    clause = Clause(clause_id="clause-2", content="   \n\t ", compliance_status="unknown")

    result = evaluate_clause_rule(clause)

    assert result.rule_code == "RULE_EMPTY_CLAUSE"
    assert result.outcome == "non_conforme"
    assert "empty" in result.message


def test_evaluate_clause_rule_marks_low_signal_clause_as_risk() -> None:
    clause = Clause(clause_id="clause-3", content="...", compliance_status="unknown")

    result = evaluate_clause_rule(clause)

    assert result.rule_code == "RULE_LOW_SIGNAL_CLAUSE"
    assert result.outcome == "risque"


def test_evaluate_clause_rule_accepts_minimal_exploitable_content() -> None:
    clause = Clause(
        clause_id="clause-4",
        content="Prime annuelle versee.",
        compliance_status="unknown",
    )

    result = evaluate_clause_rule(clause)

    assert result.rule_code == "RULE_MIN_CONTENT_PRESENT"
    assert result.outcome == "conforme"


def test_evaluate_document_rules_uses_runtime_clauses() -> None:
    document = LegalDocument(document_id="doc-1", text="irrelevant")
    document.__dict__["clauses"] = (
        Clause(clause_id="clause-a", content="", compliance_status="unknown"),
        Clause(clause_id="clause-b", content="Accord valide", compliance_status="conforme"),
    )

    results = evaluate_document_rules(document)

    assert tuple(result.clause_id for result in results) == ("clause-a", "clause-b")
    assert tuple(result.rule_code for result in results) == (
        "RULE_EMPTY_CLAUSE",
        "RULE_STATUS_MAPPING",
    )
