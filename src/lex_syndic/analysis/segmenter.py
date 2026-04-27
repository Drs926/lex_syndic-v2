"""Minimal deterministic clause segmentation for MIG-004."""

from __future__ import annotations

from lex_syndic.legal.models import Clause, LegalDocument


def _split_candidate_blocks(text: str) -> list[str]:
    """Split normalized text into simple candidate blocks."""

    paragraphs = [block.strip() for block in text.split("\n\n") if block.strip()]
    if len(paragraphs) > 1:
        return paragraphs
    return [line.strip() for line in text.split("\n") if line.strip()]


def _make_clause(document: LegalDocument, block: str, index: int) -> Clause:
    """Build one deterministic clause candidate without legal analysis."""

    return Clause(
        clause_id=f"{document.document_id}-clause-{index:03d}",
        document_id=document.document_id,
        article_id=f"candidate-{index:03d}",
        title=f"Clause candidate {index}",
        topic="autre",
        content=block,
        source_kind=document.source_kind,
        norm_reference_ids=(),
        compliance_status="unknown",
    )


def segment_document(document: LegalDocument) -> LegalDocument:
    """Attach simple clause candidates to a LegalDocument.

    The function is intentionally limited to structural segmentation:
    no legal interpretation, no topic classification, no reference extraction.
    """

    text = document.text.strip()
    if not text:
        raise ValueError("document text must not be empty for segmentation")

    blocks = _split_candidate_blocks(text)
    if not blocks:
        raise ValueError("document text must contain at least one non-empty block")

    clauses = tuple(
        _make_clause(document, block, index)
        for index, block in enumerate(blocks, start=1)
    )
    object.__setattr__(document, "clauses", clauses)
    return document
