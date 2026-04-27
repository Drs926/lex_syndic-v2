"""Minimal text-only ingestion for MIG-003.

This module intentionally stays narrow:
- text content only
- plain text files only
- no clause segmentation
- no external dependencies
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from lex_syndic.legal.models import LegalDocument


def _normalize_text(content: str) -> str:
    """Normalize line endings and trim outer blank space deterministically."""

    normalized = content.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise ValueError("content must not be empty or whitespace-only")
    return normalized


def _build_document_id(title: str, content: str, source_path: str | None) -> str:
    """Build a deterministic identifier for minimal ingestion outputs."""

    material = "\n".join([title, content, source_path or ""])
    digest = hashlib.sha1(material.encode("utf-8")).hexdigest()
    return f"doc-{digest[:12]}"


def _attach_metadata(document: LegalDocument, source_path: str | None) -> LegalDocument:
    """Attach lightweight runtime metadata without changing the legal model."""

    metadata: dict[str, str] = {}
    if source_path is not None:
        metadata["source_path"] = source_path
    object.__setattr__(document, "metadata", metadata)
    return document


def load_text_content(
    content: str, *, title: str, source_path: str | None = None
) -> LegalDocument:
    """Convert plain text content into one canonical LegalDocument."""

    normalized = _normalize_text(content)
    source_kind = "reference" if source_path is not None else "unknown"
    document = LegalDocument(
        document_id=_build_document_id(title, normalized, source_path),
        title=title,
        source_kind=source_kind,
        text=normalized,
    )
    return _attach_metadata(document, source_path)


def load_text_file(path: str) -> LegalDocument:
    """Load one plain text file into one canonical LegalDocument."""

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"file not found: {path}")
    if file_path.suffix.lower() != ".txt":
        raise ValueError("only .txt files are supported in MIG-003")

    content = file_path.read_text(encoding="utf-8")
    return load_text_content(content, title=file_path.stem, source_path=str(file_path))
