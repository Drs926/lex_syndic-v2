"""Focused tests for MIG-003 minimal text ingestion."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pytest

from lex_syndic.ingestion import load_text_content, load_text_file


def test_load_text_content_from_string() -> None:
    document = load_text_content(
        "Titre\r\n\r\nContenu", title="Accord test", source_path="input/demo.txt"
    )

    assert document.title == "Accord test"
    assert document.text == "Titre\n\nContenu"
    assert document.source_kind == "reference"
    assert document.document_id.startswith("doc-")
    assert asdict(document)["title"] == "Accord test"


def test_load_text_file_from_temp_txt(monkeypatch: pytest.MonkeyPatch) -> None:
    file_path = Path("sandbox_temp/accord.txt")

    monkeypatch.setattr(Path, "exists", lambda self: self == file_path)
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda self, encoding="utf-8": "Ligne 1\r\nLigne 2\r\n",
    )

    document = load_text_file(str(file_path))

    assert document.title == "accord"
    assert document.text == "Ligne 1\nLigne 2"
    assert document.metadata["source_path"] == str(file_path)


def test_load_text_content_rejects_blank_content() -> None:
    with pytest.raises(ValueError, match="content must not be empty"):
        load_text_content("   \n\t", title="Vide")


def test_load_text_content_preserves_title_and_source_path_metadata() -> None:
    document = load_text_content(
        "Contenu utile", title="Titre conserve", source_path="fixtures/a.txt"
    )

    assert document.title == "Titre conserve"
    assert document.metadata == {"source_path": "fixtures/a.txt"}


def test_text_loader_uses_no_external_dependency() -> None:
    source = Path("src/lex_syndic/ingestion/text_loader.py").read_text(encoding="utf-8")

    assert "pdfminer" not in source
    assert "docx" not in source
    assert "docling" not in source
    assert "markitdown" not in source


def test_text_loader_does_not_perform_advanced_legal_segmentation() -> None:
    document = load_text_content(
        "Article 1\nLe texte reste brut.", title="Sans segmentation"
    )

    assert not hasattr(document, "clauses")
    assert document.text == "Article 1\nLe texte reste brut."


def test_load_text_file_rejects_non_txt_extension(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    file_path = Path("sandbox_temp/accord.md")

    monkeypatch.setattr(Path, "exists", lambda self: self == file_path)

    with pytest.raises(ValueError, match="only .txt files are supported"):
        load_text_file(str(file_path))
