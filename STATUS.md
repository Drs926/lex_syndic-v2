# STATUS

État réel du dépôt V2 à date.

Dernière mise à jour : 2026-04-27.

## Résumé

| Domaine | État réel |
|---------|-----------|
| Architecture | **Documentée** (`docs/architecture/software_architecture_v2.md`). |
| Code métier | **Non migré.** Aucun module n'implémente de logique fonctionnelle. |
| Tests | **Présents mais non validés dans l'environnement courant.** `tests/test_package_import.py` contient 17 tests, mais `python -m pytest` échoue actuellement avec `No module named pytest`. |
| Packaging | **Déclaré mais non validé en exécution ici.** `pyproject.toml` existe, mais l'interpréteur `python` courant ne dispose pas de `pytest`. |
| Gouvernance | **En place** (fichiers racine `README`, `CONTEXT`, `AGENTS`, `PLAN`, `SPEC`, `OUTPUT_CONTRACT`, `DECISIONS`, `MIGRATION_POLICY`, `STATUS`, `PROMPTS_INDEX`). |
| Migration V1 | **Lot MIG-001 à stabiliser.** `MIG-002` à `MIG-010` listés dans `PLAN.md` non démarrés. |
| Audit V1→V2 | **Produit.** `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md` — 42 fichiers classés, 10 lots ordonnés. |

## Détail par module canonique

Modules présents en arborescence sous `src/lex_syndic/` mais sans logique
fonctionnelle (placeholders) :

| Module | État |
|--------|------|
| `core` | Squelette (`config.py`, `exceptions.py`, `types.py`). Importable avec `src/` dans `sys.path`. |
| `legal` | Squelette (`models.py`). Placeholders `LegalDocument`, `Clause`, `LegalReference`, `ComparisonResult`. Importable avec `src/` dans `sys.path`. |
| `ingestion` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `analysis` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `comparison` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `rules` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `retrieval` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `storage` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `report` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |
| `interface` | Squelette (`__init__.py`). Importable avec `src/` dans `sys.path`. |

## Hors périmètre actuel

Aucun des éléments suivants n'est présent dans V2 et aucun ne doit l'être
sans décision dans `DECISIONS.md` :

- backend applicatif,
- frontend,
- serveur MCP,
- graphe de connaissances,
- Open WebUI,
- connecteurs Légifrance / Judilibre.

## Prochaine action de référence

Stabiliser et vérifier `MIG-001` dans un environnement où `python -m pytest`
est reproductible, puis seulement ouvrir `MIG-002`.
