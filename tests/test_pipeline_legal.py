"""Tests for the minimal legal pipeline [LEX-020]."""

from __future__ import annotations

from lex_syndic.legal.models import LegalDocument, LegalReference
from lex_syndic.pipeline import PipelineResult, run_legal_pipeline


_TELEWORK_TEXT = (
    "Le teletravail est encadre par l'article L. 1222-9 du Code du travail.\n\n"
    "La duree du travail est fixee a 35 heures par semaine."
)

_DISCIPLINE_TEXT = (
    "La discipline est fondee sur les sanctions prevues par le reglement.\n\n"
    "Le salaire comprend une prime annuelle."
)


def _doc(text: str, doc_id: str = "doc-test") -> LegalDocument:
    return LegalDocument(
        document_id=doc_id,
        title=doc_id,
        source_kind="unknown",
        text=text,
    )


def _ref(citation: str, ref_id: str = "ref-001") -> LegalReference:
    return LegalReference(reference_id=ref_id, citation=citation, kind="loi")


# ---------------------------------------------------------------------------
# Structure of PipelineResult
# ---------------------------------------------------------------------------


def test_pipeline_result_has_required_fields() -> None:
    doc = _doc(_TELEWORK_TEXT)
    result = run_legal_pipeline(doc, (_ref("L1222-9"),))

    assert isinstance(result, PipelineResult)
    assert isinstance(result.document_id, str)
    assert result.document_id == "doc-test"
    assert isinstance(result.analyzed_clauses, tuple)
    assert isinstance(result.comparisons, tuple)
    assert hasattr(result, "decision")


# ---------------------------------------------------------------------------
# Cas 1 — nominal: pipeline complet avec référence fournie
# ---------------------------------------------------------------------------


def test_pipeline_nominal_reference_present() -> None:
    doc = _doc(_TELEWORK_TEXT)
    expected_ref = LegalReference(reference_id="", citation="L1222-9", kind="loi")

    result = run_legal_pipeline(doc, (expected_ref,))

    matched = {c.status for c in result.comparisons}
    assert matched & {"match", "risk_attention"}, (
        f"Expected at least one match or risk_attention, got: {matched}"
    )
    assert result.decision.status != "insufficient_data"


# ---------------------------------------------------------------------------
# Cas 2 — non_compliant: référence attendue absente du document
# ---------------------------------------------------------------------------


def test_pipeline_non_compliant_reference_absent() -> None:
    doc = _doc(_DISCIPLINE_TEXT, doc_id="doc-discipline")
    result = run_legal_pipeline(doc, (_ref("L1225-1"),))

    assert result.decision.status == "non_compliant"
    assert result.document_id == "doc-discipline"


# ---------------------------------------------------------------------------
# Cas 3 — insufficient_data: aucune expected_reference fournie
# ---------------------------------------------------------------------------


def test_pipeline_insufficient_data_no_references() -> None:
    doc = _doc(_TELEWORK_TEXT)
    result = run_legal_pipeline(doc, ())

    assert result.decision.status == "insufficient_data"
    assert result.comparisons == ()
    assert len(result.analyzed_clauses) > 0


# ---------------------------------------------------------------------------
# Isolation: pipeline n'importe pas storage / report / interface
# ---------------------------------------------------------------------------


def test_pipeline_does_not_import_storage_report_interface() -> None:
    import lex_syndic.pipeline.legal_pipeline as module
    import sys

    source_path = getattr(module, "__file__", "") or ""
    with open(source_path, encoding="utf-8") as f:
        source = f.read()

    for forbidden in ("storage", "report", "interface", "retrieval"):
        assert f"lex_syndic.{forbidden}" not in source, (
            f"Pipeline must not import lex_syndic.{forbidden}"
        )
