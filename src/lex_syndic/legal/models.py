"""Canonical legal models for LEX_SYNDIC_V2.

This module intentionally stays small and deterministic.
It defines only typed, immutable legal data structures used as the
canonical foundation for later ingestion, analysis, comparison, and rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

SourceKind = Literal["accord", "projet", "reference", "unknown"]
ComplianceStatus = Literal["conforme", "risque", "non_conforme", "unknown"]
CanonicalTopic = Literal[
    "teletravail",
    "temps_travail",
    "remuneration",
    "conges",
    "discipline",
    "sante_securite",
    "formation",
    "egalite_professionnelle",
    "organisation_travail",
    "autre",
]
NormKind = Literal[
    "loi",
    "decret",
    "convention_collective",
    "accord_entreprise",
    "jurisprudence",
    "autre",
    "unknown",
]
ComparisonType = Literal[
    "unchanged",
    "rephrased",
    "modified_quantity",
    "modified_modality",
    "modified_condition",
    "modified_subject",
    "modified_action",
    "added",
    "removed",
    "unknown",
]
RiskLevel = Literal["low", "medium", "high", "unknown"]
RuleOutcome = Literal["conforme", "risque", "non_conforme", "unknown"]
MemoFormat = Literal["markdown", "json", "text", "unknown"]
AuditEventKind = Literal[
    "ingestion",
    "analysis",
    "comparison",
    "rule_check",
    "report",
    "manual_review",
    "unknown",
]

_SOURCE_KINDS = {"accord", "projet", "reference", "unknown"}
_COMPLIANCE_STATUSES = {"conforme", "risque", "non_conforme", "unknown"}
_CANONICAL_TOPICS = {
    "teletravail",
    "temps_travail",
    "remuneration",
    "conges",
    "discipline",
    "sante_securite",
    "formation",
    "egalite_professionnelle",
    "organisation_travail",
    "autre",
}
_NORM_KINDS = {
    "loi",
    "decret",
    "convention_collective",
    "accord_entreprise",
    "jurisprudence",
    "autre",
    "unknown",
}
_COMPARISON_TYPES = {
    "unchanged",
    "rephrased",
    "modified_quantity",
    "modified_modality",
    "modified_condition",
    "modified_subject",
    "modified_action",
    "added",
    "removed",
    "unknown",
}
_RISK_LEVELS = {"low", "medium", "high", "unknown"}
_RULE_OUTCOMES = {"conforme", "risque", "non_conforme", "unknown"}
_MEMO_FORMATS = {"markdown", "json", "text", "unknown"}
_AUDIT_EVENT_KINDS = {
    "ingestion",
    "analysis",
    "comparison",
    "rule_check",
    "report",
    "manual_review",
    "unknown",
}


def _validate_choice(field_name: str, value: str, allowed: set[str]) -> None:
    """Reject values outside the canonical deterministic vocabulary."""

    if value not in allowed:
        allowed_values = ", ".join(sorted(allowed))
        raise ValueError(f"{field_name} must be one of: {allowed_values}")


@dataclass(frozen=True)
class LegalDocument:
    """Canonical representation of one legal document in V2."""

    document_id: str = ""
    title: str = ""
    source_kind: SourceKind = "unknown"
    language: str = "fr"
    text: str = ""
    reference_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _validate_choice("source_kind", self.source_kind, _SOURCE_KINDS)


@dataclass(frozen=True)
class DocumentVersion:
    """Canonical representation of one version of a legal document."""

    version_id: str = ""
    document_id: str = ""
    version_label: str = ""
    created_at: str = ""
    source_document_id: str | None = None
    change_summary: str = ""


@dataclass(frozen=True)
class Clause:
    """Canonical representation of one legal clause."""

    clause_id: str = ""
    document_id: str = ""
    article_id: str = ""
    title: str = ""
    topic: CanonicalTopic = "autre"
    content: str = ""
    source_kind: SourceKind = "unknown"
    norm_reference_ids: tuple[str, ...] = field(default_factory=tuple)
    compliance_status: ComplianceStatus = "unknown"

    def __post_init__(self) -> None:
        _validate_choice("topic", self.topic, _CANONICAL_TOPICS)
        _validate_choice("source_kind", self.source_kind, _SOURCE_KINDS)
        _validate_choice(
            "compliance_status", self.compliance_status, _COMPLIANCE_STATUSES
        )


@dataclass(frozen=True)
class MetadataTag:
    """Canonical metadata tag attached to a legal object."""

    tag_id: str = ""
    target_id: str = ""
    name: str = ""
    value: str = ""
    source: str = ""


@dataclass(frozen=True)
class LegalReference:
    """Reference extracted from or attached to a legal object."""

    reference_id: str = ""
    citation: str = ""
    kind: NormKind = "unknown"
    source_url: str | None = None

    def __post_init__(self) -> None:
        _validate_choice("kind", self.kind, _NORM_KINDS)


@dataclass(frozen=True)
class AnalyzedClause:
    """Canonical deterministic analysis result for one clause."""

    analysis_id: str = ""
    clause_id: str = ""
    document_id: str = ""
    topic: CanonicalTopic = "autre"
    extracted_reference_ids: tuple[str, ...] = field(default_factory=tuple)
    risk_level: RiskLevel = "unknown"
    summary: str = ""

    def __post_init__(self) -> None:
        _validate_choice("topic", self.topic, _CANONICAL_TOPICS)
        _validate_choice("risk_level", self.risk_level, _RISK_LEVELS)


@dataclass(frozen=True)
class Norm:
    """Canonical deterministic representation of one legal norm."""

    norm_id: str = ""
    title: str = ""
    citation: str = ""
    kind: NormKind = "unknown"
    source_url: str | None = None

    def __post_init__(self) -> None:
        _validate_choice("kind", self.kind, _NORM_KINDS)


@dataclass(frozen=True)
class ComparisonResult:
    """Minimal compared-clause placeholder kept importable for later lots."""

    result_id: str = ""
    reference_clause_id: str = ""
    proposal_clause_id: str = ""
    comparison_type: ComparisonType = "unknown"
    risk_level: RiskLevel = "unknown"

    def __post_init__(self) -> None:
        _validate_choice("comparison_type", self.comparison_type, _COMPARISON_TYPES)
        _validate_choice("risk_level", self.risk_level, _RISK_LEVELS)


@dataclass(frozen=True)
class RuleCheckResult:
    """Canonical minimal result for one deterministic rule evaluation."""

    result_id: str = ""
    clause_id: str = ""
    rule_code: str = ""
    outcome: RuleOutcome = "unknown"
    message: str = ""

    def __post_init__(self) -> None:
        _validate_choice("outcome", self.outcome, _RULE_OUTCOMES)


@dataclass(frozen=True)
class CaseFile:
    """Canonical dossier grouping legal analysis artifacts."""

    case_file_id: str = ""
    project_id: str = ""
    document_ids: tuple[str, ...] = field(default_factory=tuple)
    comparison_result_ids: tuple[str, ...] = field(default_factory=tuple)
    rule_check_result_ids: tuple[str, ...] = field(default_factory=tuple)
    memo_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class GeneratedMemo:
    """Canonical generated memo attached to a legal dossier."""

    memo_id: str = ""
    case_file_id: str = ""
    title: str = ""
    format: MemoFormat = "unknown"
    content: str = ""
    source_result_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        _validate_choice("format", self.format, _MEMO_FORMATS)


@dataclass(frozen=True)
class AuditEvent:
    """Canonical trace event for auditable legal processing."""

    event_id: str = ""
    event_type: AuditEventKind = "unknown"
    target_id: str = ""
    actor: str = ""
    occurred_at: str = ""
    detail: str = ""

    def __post_init__(self) -> None:
        _validate_choice("event_type", self.event_type, _AUDIT_EVENT_KINDS)
