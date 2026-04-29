# STATUS

État réel du dépôt V2 à date.

Dernière mise à jour : 2026-04-29.

## Résumé

| Domaine | État réel |
|---------|-----------|
| Architecture | **Documentée** (`docs/architecture/software_architecture_v2.md`). |
| Code métier | **Partiellement migré.** Les modules `legal`, `ingestion`, `analysis`, `comparison` et `rules` disposent d'un socle minimal testé. |
| Tests | **Opérationnels.** `python -m pytest -q` a passé : `52 passed in 0.17s` le 2026-04-29. |
| Packaging | **En place et vérifié.** `pyproject.toml` existe, le backend editable est `setuptools.build_meta`, et l'exécution locale de `pytest` a été revalidée le 2026-04-29. |
| Gouvernance | **En place** (fichiers racine `README`, `CONTEXT`, `AGENTS`, `PLAN`, `SPEC`, `OUTPUT_CONTRACT`, `DECISIONS`, `MIGRATION_POLICY`, `STATUS`, `PROMPTS_INDEX`). |
| Migration V1 | **MIG-001 à MIG-006 terminés.** `MIG-007` à `MIG-010` non démarrés. |
| Audit V1→V2 | **Produit.** `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md` — 42 fichiers classés, 10 lots ordonnés. |

## Détail par module canonique

Modules présents en arborescence sous `src/lex_syndic/` mais sans logique
fonctionnelle (placeholders) :

| Module | État |
|--------|------|
| `core` | Squelette (`config.py`, `exceptions.py`, `types.py`). Importable avec `src/` dans `sys.path`. |
| `legal` | MIG-002 terminé. `models.py` contient les modèles canoniques immuables `LegalDocument`, `Clause`, `LegalReference`, `Norm`, `RuleCheckResult` et un `ComparisonResult` typé, avec tests dédiés verts. |
| `ingestion` | MIG-003 terminé. Ingestion texte minimale stabilisée autour de `load_text_content` et `load_text_file`, sans dépendance externe ni segmentation avancée. |
| `analysis` | MIG-004 terminé. Segmentation minimale déterministe en clauses candidates stabilisée sans analyse juridique, sans extraction et sans dépendance externe. |
| `comparison` | MIG-005 terminé. Comparaison structurelle minimale entre documents déjà segmentés, par ordre de clauses, sans scoring ni interprétation juridique. |
| `rules` | MIG-006 terminé. Evaluation déterministe minimale via `evaluate_clause_rule` et `evaluate_document_rules`, avec sortie `RuleCheckResult` testée sans dependance externe. |
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

`MIG-006` est verifie. Toute ouverture de `MIG-007` doit rester separee et explicite.
