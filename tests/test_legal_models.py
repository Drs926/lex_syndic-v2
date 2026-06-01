"""Focused tests for MIG-002 canonical legal models."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, asdict

import pytest

from lex_syndic.legal.models import (
    AnalyzedClause,
    AuditEvent,
    CaseFile,
    Clause,
    ComparisonResult,
    DocumentVersion,
    GeneratedMemo,
    LegalDocument,
    LegalReference,
    MetadataTag,
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


def test_document_version_and_metadata_tag_are_instantiable() -> None:
    version = DocumentVersion(
        version_id="version-001",
        document_id="doc-001",
        version_label="v1",
        created_at="2026-06-01",
        source_document_id="doc-source",
        change_summary="Initial version.",
    )
    tag = MetadataTag(
        tag_id="tag-001",
        target_id="doc-001",
        name="theme",
        value="teletravail",
        source="manual",
    )

    assert asdict(version) == {
        "version_id": "version-001",
        "document_id": "doc-001",
        "version_label": "v1",
        "created_at": "2026-06-01",
        "source_document_id": "doc-source",
        "change_summary": "Initial version.",
    }
    assert asdict(tag) == {
        "tag_id": "tag-001",
        "target_id": "doc-001",
        "name": "theme",
        "value": "teletravail",
        "source": "manual",
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


def test_analyzed_clause_is_instantiable_and_serializable() -> None:
    analyzed_clause = AnalyzedClause(
        analysis_id="analysis-001",
        clause_id="clause-001",
        document_id="doc-001",
        topic="teletravail",
        extracted_reference_ids=("ref-001",),
        risk_level="low",
        summary="Clause analysee.",
    )

    assert asdict(analyzed_clause) == {
        "analysis_id": "analysis-001",
        "clause_id": "clause-001",
        "document_id": "doc-001",
        "topic": "teletravail",
        "extracted_reference_ids": ("ref-001",),
        "risk_level": "low",
        "summary": "Clause analysee.",
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


def test_case_file_and_generated_memo_are_instantiable() -> None:
    case_file = CaseFile(
        case_file_id="case-001",
        project_id="project-001",
        document_ids=("doc-001",),
        comparison_result_ids=("cmp-001",),
        rule_check_result_ids=("rule-001",),
        memo_ids=("memo-001",),
    )
    memo = GeneratedMemo(
        memo_id="memo-001",
        case_file_id="case-001",
        title="Synthese",
        format="markdown",
        content="# Synthese",
        source_result_ids=("cmp-001", "rule-001"),
    )

    assert asdict(case_file) == {
        "case_file_id": "case-001",
        "project_id": "project-001",
        "document_ids": ("doc-001",),
        "comparison_result_ids": ("cmp-001",),
        "rule_check_result_ids": ("rule-001",),
        "memo_ids": ("memo-001",),
    }
    assert asdict(memo) == {
        "memo_id": "memo-001",
        "case_file_id": "case-001",
        "title": "Synthese",
        "format": "markdown",
        "content": "# Synthese",
        "source_result_ids": ("cmp-001", "rule-001"),
    }


def test_audit_event_is_instantiable_and_serializable() -> None:
    event = AuditEvent(
        event_id="audit-001",
        event_type="analysis",
        target_id="clause-001",
        actor="system",
        occurred_at="2026-06-01T10:00:00Z",
        detail="Clause analysis completed.",
    )

    assert asdict(event) == {
        "event_id": "audit-001",
        "event_type": "analysis",
        "target_id": "clause-001",
        "actor": "system",
        "occurred_at": "2026-06-01T10:00:00Z",
        "detail": "Clause analysis completed.",
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


def test_generated_memo_rejects_unknown_format() -> None:
    with pytest.raises(ValueError, match="format must be one of"):
        GeneratedMemo(format="pdf")  # type: ignore[arg-type]


def test_audit_event_rejects_unknown_event_type() -> None:
    with pytest.raises(ValueError, match="event_type must be one of"):
        AuditEvent(event_type="invalid")  # type: ignore[arg-type]


def test_legal_document_is_immutable() -> None:
    document = LegalDocument(document_id="doc-001")

    with pytest.raises(FrozenInstanceError):
        document.document_id = "doc-002"  # type: ignore[misc]
