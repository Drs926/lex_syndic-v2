# STATUS

État réel du dépôt V2 à date.

Dernière mise à jour : 2026-04-27.

## Résumé

| Domaine | État réel |
|---------|-----------|
| Architecture | **Documentée** (`docs/architecture/software_architecture_v2.md`). |
| Code métier | **Non migré.** Aucun module n'implémente de logique fonctionnelle. |
| Tests | **Opérationnels.** `python -m pytest tests/test_package_import.py -v -p no:cacheprovider` a passé : `17 passed` le 2026-04-27. |
| Packaging | **En place et vérifié.** `pyproject.toml` existe, le backend editable est `setuptools.build_meta`, et l'installation locale permet l'exécution de `pytest`. |
| Gouvernance | **En place** (fichiers racine `README`, `CONTEXT`, `AGENTS`, `PLAN`, `SPEC`, `OUTPUT_CONTRACT`, `DECISIONS`, `MIGRATION_POLICY`, `STATUS`, `PROMPTS_INDEX`). |
| Migration V1 | **MIG-001 à MIG-003 terminés.** `MIG-004` à `MIG-010` non démarrés. |
| Audit V1→V2 | **Produit.** `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md` — 42 fichiers classés, 10 lots ordonnés. |

## Détail par module canonique

Modules présents en arborescence sous `src/lex_syndic/` mais sans logique
fonctionnelle (placeholders) :

| Module | État |
|--------|------|
| `core` | Squelette (`config.py`, `exceptions.py`, `types.py`). Importable avec `src/` dans `sys.path`. |
| `legal` | MIG-002 terminé. `models.py` contient les modèles canoniques immuables `LegalDocument`, `Clause`, `LegalReference`, `Norm`, `RuleCheckResult` et un `ComparisonResult` typé, avec tests dédiés verts. |
| `ingestion` | MIG-003 terminé. Ingestion texte minimale stabilisée autour de `load_text_content` et `load_text_file`, sans dépendance externe ni segmentation avancée. |
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

`MIG-003` est vérifié. Toute ouverture de `MIG-004` doit rester séparée et explicite.
