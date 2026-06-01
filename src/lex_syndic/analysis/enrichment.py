"""Deterministic legal analysis enrichment for LEX_SYNDIC_V2."""

from __future__ import annotations

import re
import unicodedata

from lex_syndic.analysis.segmenter import segment_document
from lex_syndic.legal.models import (
    AnalyzedClause,
    CanonicalTopic,
    Clause,
    LegalDocument,
    LegalReference,
    NormKind,
    RiskLevel,
)

_REFERENCE_PATTERN = re.compile(
    r"\b(?:article|articles|art\.)\s+"
    r"(?P<citation>[LDR]\.?\s*\d+(?:-\d+){1,4})\b",
    re.IGNORECASE,
)

_TOPIC_KEYWORDS: tuple[tuple[CanonicalTopic, tuple[str, ...]], ...] = (
    ("teletravail", ("teletravail", "travail a distance", "distanciel")),
    ("temps_travail", ("temps de travail", "duree du travail", "heures supplementaires")),
    ("remuneration", ("remuneration", "salaire", "prime", "indemnite")),
    ("conges", ("conge", "conges", "repos", "absence")),
    ("discipline", ("discipline", "sanction", "avertissement", "licenciement")),
    ("sante_securite", ("sante", "securite", "risque professionnel", "prevention")),
    ("formation", ("formation", "competence", "apprentissage")),
    ("egalite_professionnelle", ("egalite", "discrimination", "parite")),
    ("organisation_travail", ("organisation", "planning", "horaire", "service")),
)

_HIGH_RISK_TERMS = (
    "licenciement",
    "sanction",
    "retenue",
    "suppression",
    "interdiction",
    "sans preavis",
)
_MEDIUM_RISK_TERMS = (
    "doit",
    "obligatoire",
    "minimum",
    "duree",
    "delai",
    "autorisation",
    "controle",
)


def _normalize_text(text: str) -> str:
    lowered = text.lower()
    decomposed = unicodedata.normalize("NFKD", lowered)
    without_accents = "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character)
    )
    return " ".join(without_accents.split())


def _reference_kind(text: str) -> NormKind:
    normalized = _normalize_text(text)
    if "convention collective" in normalized:
        return "convention_collective"
    if "accord d'entreprise" in normalized or "accord entreprise" in normalized:
        return "accord_entreprise"
    if "jurisprudence" in normalized or "cour de cassation" in normalized:
        return "jurisprudence"
    if "decret" in normalized:
        return "decret"
    return "loi"


def _extract_references(clause: Clause) -> tuple[LegalReference, ...]:
    references: list[LegalReference] = []
    seen: set[str] = set()
    kind = _reference_kind(clause.content)

    for match in _REFERENCE_PATTERN.finditer(clause.content):
        citation = re.sub(r"\s+", "", match.group("citation").upper())
        citation = citation.replace(".", "")
        if citation in seen:
            continue
        seen.add(citation)
        index = len(references) + 1
        references.append(
            LegalReference(
                reference_id=f"{clause.clause_id}-ref-{index:03d}",
                citation=citation,
                kind=kind,
            )
        )

    return tuple(references)


def _classify_topic(clause: Clause) -> CanonicalTopic:
    normalized = _normalize_text(clause.content)
    for topic, keywords in _TOPIC_KEYWORDS:
        if any(keyword in normalized for keyword in keywords):
            return topic
    return "autre"


def _risk_level(clause: Clause, references: tuple[LegalReference, ...]) -> RiskLevel:
    normalized = _normalize_text(clause.content)
    if any(term in normalized for term in _HIGH_RISK_TERMS):
        return "high"
    if references or any(term in normalized for term in _MEDIUM_RISK_TERMS):
        return "medium"
    return "low"


def analyze_clause(clause: Clause) -> tuple[AnalyzedClause, tuple[LegalReference, ...]]:
    """Analyze one clause without applying legal rules or comparison logic."""

    references = _extract_references(clause)
    topic = _classify_topic(clause)
    risk_level = _risk_level(clause, references)
    summary = (
        f"topic={topic}; references={len(references)}; risk_level={risk_level}"
    )

    return (
        AnalyzedClause(
            analysis_id=f"{clause.clause_id}-analysis",
            clause_id=clause.clause_id,
            document_id=clause.document_id,
            topic=topic,
            extracted_reference_ids=tuple(
                reference.reference_id for reference in references
            ),
            risk_level=risk_level,
            summary=summary,
        ),
        references,
    )


def analyze_document(document: LegalDocument) -> LegalDocument:
    """Attach deterministic legal analysis artifacts to a document."""

    clauses = getattr(document, "clauses", None)
    if clauses is None:
        document = segment_document(document)
        clauses = getattr(document, "clauses")

    if not isinstance(clauses, tuple) or not all(
        isinstance(clause, Clause) for clause in clauses
    ):
        raise ValueError("document must expose segmented clauses as a tuple of Clause")

    analyzed_clauses: list[AnalyzedClause] = []
    legal_references: list[LegalReference] = []

    for clause in clauses:
        analyzed_clause, references = analyze_clause(clause)
        analyzed_clauses.append(analyzed_clause)
        legal_references.extend(references)

    object.__setattr__(document, "analyzed_clauses", tuple(analyzed_clauses))
    object.__setattr__(document, "legal_references", tuple(legal_references))
    return document
