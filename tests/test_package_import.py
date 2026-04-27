"""Tests minimaux de socle — lot MIG-001.

Ces tests vérifient uniquement que le package est importable et que les
squelettes de modules canoniques sont accessibles. Aucune logique métier
n'est testée ici.
"""

import importlib


def test_root_package_importable() -> None:
    """Le package racine lex_syndic doit être importable."""
    mod = importlib.import_module("lex_syndic")
    assert mod is not None


def test_core_subpackage_importable() -> None:
    """Le sous-package core doit être importable."""
    mod = importlib.import_module("lex_syndic.core")
    assert mod is not None


def test_core_exceptions_importable() -> None:
    """LexSyndicError doit être importable depuis core.exceptions."""
    from lex_syndic.core.exceptions import LexSyndicError
    assert issubclass(LexSyndicError, Exception)


def test_core_exceptions_is_base_exception() -> None:
    """LexSyndicError doit être instanciable et lever correctement."""
    from lex_syndic.core.exceptions import LexSyndicError
    err = LexSyndicError("test")
    assert str(err) == "test"


def test_legal_subpackage_importable() -> None:
    """Le sous-package legal doit être importable."""
    mod = importlib.import_module("lex_syndic.legal")
    assert mod is not None


def test_legal_models_placeholders_importable() -> None:
    """Les modèles placeholder legal/models.py doivent être importables."""
    from lex_syndic.legal.models import LegalDocument, Clause, LegalReference, ComparisonResult
    assert LegalDocument is not None
    assert Clause is not None
    assert LegalReference is not None
    assert ComparisonResult is not None


def test_legal_models_instantiable() -> None:
    """Les dataclasses placeholder doivent être instanciables."""
    from lex_syndic.legal.models import LegalDocument, Clause
    doc = LegalDocument(document_id="test-doc-1")
    clause = Clause(clause_id="test-clause-1")
    assert doc.document_id == "test-doc-1"
    assert clause.clause_id == "test-clause-1"


def test_ingestion_subpackage_importable() -> None:
    """Le sous-package ingestion doit être importable."""
    mod = importlib.import_module("lex_syndic.ingestion")
    assert mod is not None


def test_analysis_subpackage_importable() -> None:
    """Le sous-package analysis doit être importable."""
    mod = importlib.import_module("lex_syndic.analysis")
    assert mod is not None


def test_comparison_subpackage_importable() -> None:
    """Le sous-package comparison doit être importable."""
    mod = importlib.import_module("lex_syndic.comparison")
    assert mod is not None


def test_rules_subpackage_importable() -> None:
    """Le sous-package rules doit être importable."""
    mod = importlib.import_module("lex_syndic.rules")
    assert mod is not None


def test_retrieval_subpackage_importable() -> None:
    """Le sous-package retrieval doit être importable."""
    mod = importlib.import_module("lex_syndic.retrieval")
    assert mod is not None


def test_storage_subpackage_importable() -> None:
    """Le sous-package storage doit être importable."""
    mod = importlib.import_module("lex_syndic.storage")
    assert mod is not None


def test_report_subpackage_importable() -> None:
    """Le sous-package report doit être importable."""
    mod = importlib.import_module("lex_syndic.report")
    assert mod is not None


def test_interface_subpackage_importable() -> None:
    """Le sous-package interface doit être importable."""
    mod = importlib.import_module("lex_syndic.interface")
    assert mod is not None


def test_no_business_logic_in_core_config() -> None:
    """core/config.py ne doit exposer aucune logique métier à ce stade."""
    import lex_syndic.core.config as config_mod
    public_names = [n for n in dir(config_mod) if not n.startswith("_")]
    assert public_names == [], (
        f"core/config.py expose des noms publics inattendus : {public_names}"
    )


def test_no_business_logic_in_core_types() -> None:
    """core/types.py ne doit exposer aucune logique métier à ce stade."""
    import lex_syndic.core.types as types_mod
    public_names = [n for n in dir(types_mod) if not n.startswith("_")]
    assert public_names == [], (
        f"core/types.py expose des noms publics inattendus : {public_names}"
    )
