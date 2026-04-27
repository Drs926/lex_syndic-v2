"""Focused tests for MIG-002 canonical legal models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict

import pytest

from lex_syndic.legal.models import (
    Clause,
    ComparisonResult,
    LegalDocument,
    LegalReference,
    Norm,
    RuleCheckResult,
)


def test_legal_document_is_instantiable_and_serializable() -> None:
    document = LegalDocument(
        document_id="doc-001",
        title="Accord teletravail",
        source_kind="accord",
        reference_ids=("ref-001", "ref-002"),
    )

    assert asdict(document) == {
        "document_id": "doc-001",
        "title": "Accord teletravail",
        "source_kind": "accord",
        "language": "fr",
        "text": "",
        "reference_ids": ("ref-001", "ref-002"),
    }


def test_clause_is_instantiable_and_serializable() -> None:
    clause = Clause(
        clause_id="clause-001",
        document_id="doc-001",
        article_id="art-1",
        title="Objet",
        topic="teletravail",
        content="Le teletravail est ouvert.",
        source_kind="accord",
        norm_reference_ids=("norm-001",),
        compliance_status="conforme",
    )

    assert asdict(clause) == {
        "clause_id": "clause-001",
        "document_id": "doc-001",
        "article_id": "art-1",
        "title": "Objet",
        "topic": "teletravail",
        "content": "Le teletravail est ouvert.",
        "source_kind": "accord",
        "norm_reference_ids": ("norm-001",),
        "compliance_status": "conforme",
    }


def test_legal_reference_and_norm_are_instantiable_and_serializable() -> None:
    reference = LegalReference(
        reference_id="ref-legifrance-1",
        citation="Code du travail L1222-9",
        kind="loi",
        source_url="https://example.test/legifrance",
    )
    norm = Norm(
        norm_id="norm-001",
        title="Code du travail",
        citation="Article L1222-9",
        kind="loi",
        source_url="https://example.test/legifrance",
    )

    assert asdict(reference) == {
        "reference_id": "ref-legifrance-1",
        "citation": "Code du travail L1222-9",
        "kind": "loi",
        "source_url": "https://example.test/legifrance",
    }
    assert asdict(norm) == {
        "norm_id": "norm-001",
        "title": "Code du travail",
        "citation": "Article L1222-9",
        "kind": "loi",
        "source_url": "https://example.test/legifrance",
    }


def test_comparison_result_remains_importable_and_typed() -> None:
    result = ComparisonResult(
        result_id="cmp-001",
        reference_clause_id="ref-1",
        proposal_clause_id="prop-1",
        comparison_type="modified_modality",
        risk_level="medium",
    )

    assert asdict(result) == {
        "result_id": "cmp-001",
        "reference_clause_id": "ref-1",
        "proposal_clause_id": "prop-1",
        "comparison_type": "modified_modality",
        "risk_level": "medium",
    }


def test_rule_check_result_is_instantiable_and_serializable() -> None:
    result = RuleCheckResult(
        result_id="rule-001",
        clause_id="clause-001",
        rule_code="R001",
        outcome="risque",
        message="Clause a verifier.",
    )

    assert asdict(result) == {
        "result_id": "rule-001",
        "clause_id": "clause-001",
        "rule_code": "R001",
        "outcome": "risque",
        "message": "Clause a verifier.",
    }


def test_rule_check_result_rejects_unknown_outcome() -> None:
    with pytest.raises(ValueError, match="outcome must be one of"):
        RuleCheckResult(outcome="invalide")  # type: ignore[arg-type]


def test_clause_rejects_unknown_topic() -> None:
    with pytest.raises(ValueError, match="topic must be one of"):
        Clause(topic="invalide")  # type: ignore[arg-type]


def test_legal_document_is_immutable() -> None:
    document = LegalDocument(document_id="doc-001")

    with pytest.raises(FrozenInstanceError):
        document.document_id = "doc-002"  # type: ignore[misc]
