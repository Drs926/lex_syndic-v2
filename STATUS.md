# STATUS

État réel du dépôt V2 à date.

Dernière mise à jour : 2026-06-01.

## Résumé

| Domaine | État réel |
|---------|-----------|
| Architecture | **Documentée** (`docs/architecture/software_architecture_v2.md`). |
| Code métier | **Partiellement migré.** Les modules `legal`, `ingestion`, `analysis`, `comparison`, `rules`, `retrieval`, `storage`, `report` et `interface` disposent d'un socle minimal testé. |
| Tests | **Opérationnels.** `python -m pytest tests/test_interface_minimal.py tests/test_package_import.py -v -p no:cacheprovider` a passé : `28 passed in 0.13s` le 2026-04-30. |
| Packaging | **En place et vérifié.** `pyproject.toml` existe, le backend editable est `setuptools.build_meta`, et l'exécution locale de `pytest` a été revalidée le 2026-04-29. |
| Gouvernance | **En place** (fichiers racine `README`, `CONTEXT`, `AGENTS`, `PLAN`, `SPEC`, `OUTPUT_CONTRACT`, `DECISIONS`, `MIGRATION_POLICY`, `STATUS`, `PROMPTS_INDEX`). |
| Migration V1 | **MIG-001 à MIG-010 terminés.** |
| Pipeline juridique | **LEX-020 mergé.** `run_legal_pipeline()` disponible dans `src/lex_syndic/pipeline/`. |
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
| `retrieval` | MIG-007A PASS. Retrieval lexical minimal disponible depuis le commit `d7278b7`, avec index en mémoire, score déterministe et ordre stable sans dépendance externe. |
| `storage` | MIG-008A PASS. Storage minimal disponible depuis le commit `f8dec95`, avec API memoire deterministe, aucun ajout de dependance et aucun couplage au retrieval. |
| `report` | MIG-009A PASS. Module minimal disponible depuis le commit `6b90ff4`, avec package `src/lex_syndic/report/`, structure de rapport simple, rendu texte deterministe, aucune dependance externe et aucun couplage `retrieval`/`storage`. |
| `interface` | MIG-010A PASS. Module minimal disponible depuis le commit `1973e44`, avec package `src/lex_syndic/interface/`, requête structurée simple, réponse structurée simple, traitement local deterministe, aucune dependance externe et aucun couplage direct `retrieval`/`storage`/`report`. |
| `pipeline` | LEX-020 PASS. Pipeline juridique minimal disponible depuis le commit `cba40ee`, avec `run_legal_pipeline()` orchestrant `analysis → comparison → rules`, contexte de comparaison construit automatiquement depuis les références extraites, sortie `PipelineResult` immuable, 117 tests verts, aucune dépendance externe. |
| `interface` (LEX-021) | LEX-021 PASS. `analyze_legal_text()` disponible depuis le commit `3a8f4cf`, acceptant `LegalAnalysisRequest(text, expected_citations)` et retournant `LegalAnalysisResponse`, 123 tests verts, aucun couplage storage/report/MCP. |
| `acceptance` (LEX-022) | LEX-022 PASS. `tests/test_acceptance_legal_pipeline.py` disponible depuis le commit `1d0ce87`. 4 scénarios end-to-end verts sur accord d'entreprise réaliste. 127 tests globaux verts. Aucune modification `src/`. |
| `report` (LEX-023) | LEX-023 PASS. `format_legal_report()` disponible depuis le commit `4334814`. Rapport texte court déterministe depuis `LegalAnalysisResponse`. 132 tests globaux verts. Aucune dépendance externe. |
| `interface` (LEX-024) | LEX-024 PASS. `analyze_legal_text_with_report()` disponible depuis le commit `8687a86`. `LegalAnalysisWithReportResponse` expose `analysis` + `report_text`. 137 tests globaux verts. Aucune dépendance externe. |
| `acceptance` (LEX-025) | LEX-025 PASS. `tests/test_acceptance_full_flow.py` disponible depuis le commit `fe6e472`. 4 scénarios end-to-end verts sur accord réaliste. 141 tests globaux verts. Aucune modification `src/`. |
| `storage` (LEX-026) | LEX-026 PASS. `InMemoryLegalResultStore` disponible dans `src/lex_syndic/storage/legal_results.py`. API : `save`, `get`, `list_ids`, `clear`. 148 tests globaux verts. Aucune écriture disque, aucune dépendance externe. |
| `interface` (LEX-027) | LEX-027 EN COURS. `analyze_and_store_legal_text()` dans `src/lex_syndic/interface/session_handler.py`. `LegalSessionResult` expose `record_id` + `result`. 154 tests globaux verts. Aucun store global. Aucune dépendance externe. |

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

LEX-027 EN COURS. `analyze_and_store_legal_text()` disponible dans `src/lex_syndic/interface/session_handler.py`. 154 tests globaux verts. Toute suite exige un nouveau cadrage explicite dans `DECISIONS.md`.

## Séquence rail validée

Le dépôt `lex_syndic_v2` sert désormais aussi de support contrôlé pour valider
le rail ChatGPT → GitHub → Codex. Dans cette séquence, les lots fonctionnels
Lex-Syndic restent secondaires par rapport à la preuve du rail.

- `RAIL-002` a validé un cycle propre avec branche dédiée, push de branche et préparation de PR.
- `RAIL-004` a validé le cycle issue GitHub `#2` → branche dédiée → commit → push → PR.
- `RAIL-005` a validé le cycle issue GitHub `#4` → branche locale dédiée → preuve locale → préparation PR.
- `RAIL-006` a validé un cycle accéléré gouverné `#6` exécuté en une seule mission Codex.
- `RAIL-007` est PASS et mergé sur `main` via le merge commit `6a83e27`, avec réconciliation des traces racine et `.codex`.

## État courant après LEX-027

- `main = origin/main = 6516a4afa2377d71978136ad5d63fef4459f71ac` (base LEX-027)
- LEX-026 mergé via PR #40 — `InMemoryLegalResultStore` disponible, 148 tests verts
- LEX-027 en cours via issue #41 — `analyze_and_store_legal_text()` disponible, 154 tests verts
- prochaine étape : merger PR LEX-027, puis finaliser

## Notes d'execution

- Le warning `pytest_asyncio` sur `asyncio_default_fixture_loop_scope` reste un
  bruit non bloquant.
- Le wildcard PowerShell `tests/test_retrieval*.py` n'est pas fiable sans
  expansion explicite dans cet environnement.
- Le warning Git `C:\Users\Harib\.config\git\ignore` reste un bruit
  d'environnement non bloquant.
