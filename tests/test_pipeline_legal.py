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
    from lex_syndic.analysis.enrichment import analyze_document
    from lex_syndic.comparison.clause_norm import ClauseNormComparisonContext

    doc = _doc(_TELEWORK_TEXT)
    # Pre-run analysis to discover the extracted reference ID so the comparison
    # engine can match citation by ID.
    enriched = analyze_document(doc)
    first_clause = enriched.analyzed_clauses[0]
    extracted_ref_ids = first_clause.extracted_reference_ids
    assert extracted_ref_ids, "Expected at least one extracted reference in clause 1"

    known_ref = LegalReference(
        reference_id=extracted_ref_ids[0],
        citation="L1222-9",
        kind="loi",
    )
    expected_ref = LegalReference(reference_id="", citation="L1222-9", kind="loi")
    context = ClauseNormComparisonContext(known_references=(known_ref,))

    result = run_legal_pipeline(doc, (expected_ref,), context=context)

    # Pipeline must have produced analysis, comparisons and a rule decision.
    assert len(result.analyzed_clauses) > 0
    assert len(result.comparisons) > 0
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
