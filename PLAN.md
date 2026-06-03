# PLAN

Feuille de route opérationnelle de V2.

## Phase 0 — Stabilisation gouvernance (terminée)

- Fichiers racine renseignés : `README`, `CONTEXT`, `AGENTS`, `PLAN`, `SPEC`,
  `OUTPUT_CONTRACT`, `DECISIONS`, `MIGRATION_POLICY`, `STATUS`, `PROMPTS_INDEX`.
- Aucun code migré. Aucun test ajouté. Aucune dépendance ajoutée.

## Phase 1 — Outillage minimum (terminée)

- `pyproject.toml` créé : `lex-syndic` v2.0.0, Python ≥ 3.11, pytest ≥ 8.0.
- Backend d'installation editable corrigé : `setuptools.build_meta`.
- Pipeline de tests initialisé : `tests/conftest.py` + `tests/test_package_import.py`.
- Commande reproduite avec succès le 2026-04-27 :
  `python -m pytest tests/test_package_import.py -v -p no:cacheprovider`
  → `17 passed`.
- Audit V1→V2 produit : `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md`.

## Phase 2 — Migration contrôlée depuis V1

La migration depuis V1 se fait **par lots numérotés** `MIG-001` à `MIG-010`.
Chaque lot respecte `MIGRATION_POLICY.md` :

- périmètre limité à un module canonique de `software_architecture_v2.md` ;
- code repris **réécrit** ou **adapté** (pas de copie aveugle) ;
- tests obligatoires avant fusion ;
- pas d'introduction de technologie hors architecture ;
- entrée correspondante dans `DECISIONS.md`.

### Lots de migration

| Lot | Module cible | Contenu | Critère de sortie | État |
|-----|--------------|---------|-------------------|------|
| `MIG-001` | `core` | Packaging, pyproject.toml, pipeline de tests, squelettes importables. | `python -m pytest` passe. 17 tests verts. | **TERMINÉ** |
| `MIG-002` | `legal` | Modèles juridiques `LegalDocument`, `Clause`, `LegalReference`, `Norm`, `RuleCheckResult`. | Modèles instanciables, sérialisation testée. | **TERMINÉ** |
| `MIG-003` | `ingestion` | Lecture texte brut, chargement `.txt`, normalisation simple, sortie `LegalDocument`. | Ingestion texte testée sans dépendance externe ni segmentation avancée. | **TERMINÉ** |
| `MIG-004` | `analysis` | Segmentation minimale en clauses candidates, sans analyse juridique ni extraction. | Segmentation déterministe testée sur `LegalDocument` issu de MIG-003. | **TERMINÉ** |
| `MIG-005` | `comparison` | Comparaison minimale clause↔clause entre documents déjà segmentés, sans scoring ni jugement juridique. | Comparaison structurelle testée via `ComparisonResult` canonique et entrées ordonnées. | **TERMINÉ** |
| `MIG-006` | `rules` | Règles calculables, seuils, validation conformité. | Sortie `RuleCheckResult` testée. | **TERMINÉ** |
| `MIG-007` | `retrieval` | Indexation et recherche lexicale interne minimale. | Recherche sur corpus de test reproductible. | **TERMINÉ** |
| `MIG-008` | `storage` | Cadrage du périmètre storage, puis implémentation séparée. | Périmètre, invariants, fichiers autorisés/interdits, tests attendus et critères PASS/BLOCK définis avant code. | **TERMINÉ** |
| `MIG-009` | `report` | Cadrage du périmètre report, puis implémentation séparée. | Module `report` minimal disponible avec structure simple et rendu texte déterministe testés. | **TERMINÉ** |
| `MIG-010` | `interface` | Cadrage du périmètre interface, puis implémentation séparée. | Module `interface` minimal disponible avec requête structurée simple, réponse structurée simple et traitement local déterministe testés. | **TERMINÉ** |

### Ordre des lots

L'ordre est contraint par le graphe de dépendances de `software_architecture_v2.md` §7.
Référence détaillée : `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md` §9.

```
MIG-001 → MIG-002 → MIG-003 → MIG-004 → MIG-005 → MIG-006
                 ↘ MIG-007
                 ↘ MIG-008
MIG-005 + MIG-006 → MIG-009 → MIG-010
```

### Hors plan

Aucun lot ne couvre :
- backend applicatif,
- frontend,
- serveur MCP,
- graphe,
- Open WebUI,
- connecteurs Légifrance ou Judilibre.

Ces sujets exigeraient une décision explicite dans `DECISIONS.md`.

### Prochaine préparation

- Après `MIG-007`, la prochaine étape logique est le cadrage séparé de
  `MIG-008` (`storage`) sans implémentation dans cette mission.

### Cadrage MIG-008

- Cette mission de cadrage ne lance aucune implémentation `storage`.
- Sorties attendues du cadrage :
  - périmètre fonctionnel storage ;
  - fichiers autorisés pour la future mission d'implémentation ;
  - fichiers interdits ;
  - invariants ;
  - tests attendus ;
  - critères PASS/BLOCK.

### Prochaine préparation

- Après `MIG-010`, aucune nouvelle implémentation n'est planifiée dans le
  périmètre V2 courant sans nouveau cadrage explicite.

## Phase 3 — Pipeline juridique minimal (en cours)

### LEX-020 — Pipeline analysis → comparison → rules

| Lot | Contenu | Critère de sortie | État |
|-----|---------|-------------------|------|
| `LEX-020` | Création de `src/lex_syndic/pipeline/` avec `run_legal_pipeline()` et `PipelineResult`. Pipeline déterministe reliant analysis, comparison et rules sans dépendance externe. | 117 tests verts. Contexte de comparaison construit automatiquement depuis les références extraites. | **TERMINÉ** — merge commit `cba40ee` |
| `LEX-020B` | Mise à jour de gouvernance post-LEX-020 : `DECISIONS.md` (DEC-017), `STATUS.md`, `PLAN.md`. | Seuls les fichiers de gouvernance modifiés. Aucun code produit touché. | **TERMINÉ** — PR #20 |
| `LEX-021` | Exposition du pipeline via `analyze_legal_text()` dans `src/lex_syndic/interface/legal_handler.py`. Entrée : `LegalAnalysisRequest`. Sortie : `LegalAnalysisResponse`. | 123 tests verts. Aucun couplage storage/report/MCP. | **TERMINÉ** — PR #22 |
| `LEX-021B/022` | Gouvernance post-LEX-021 (DEC-018, DEC-019) + cadrage LEX-022 sans implémentation. | Seuls DECISIONS.md, STATUS.md, PLAN.md modifiés. | **TERMINÉ** — PR #24 |
| `LEX-022` | Test d'acceptation end-to-end : `tests/test_acceptance_legal_pipeline.py`. 4 scénarios sur accord réaliste. 127 tests verts. | Tests verts, aucune modification `src/`. | **TERMINÉ** — PR #26 |
| `LEX-022B/023` | Gouvernance post-LEX-022 (DEC-020, DEC-021) + cadrage LEX-023 sans implémentation. | Seuls DECISIONS.md, STATUS.md, PLAN.md modifiés. | **TERMINÉ** — PR #28 |
| `LEX-023` | `format_legal_report()` dans `src/lex_syndic/report/legal_formatter.py`. Rapport texte court déterministe depuis `LegalAnalysisResponse`. 5 tests verts. | 132 tests globaux verts. Aucune dépendance externe. | **TERMINÉ** — PR #30 |
| `LEX-023B/024` | Gouvernance post-LEX-023 (DEC-022, DEC-023) + cadrage LEX-024 sans implémentation. | Seuls DECISIONS.md, STATUS.md, PLAN.md modifiés. | **TERMINÉ** — PR #32 |
| `LEX-024` | `analyze_legal_text_with_report()` dans `src/lex_syndic/interface/report_handler.py`. `LegalAnalysisWithReportResponse` expose `analysis` + `report_text`. 5 tests verts. | 137 tests globaux verts. Aucune dépendance externe. | **TERMINÉ** — PR #34 |
| `LEX-024B/025` | Gouvernance post-LEX-024 (DEC-024, DEC-025) + cadrage LEX-025 sans implémentation. | Seuls DECISIONS.md, STATUS.md, PLAN.md modifiés. | **TERMINÉ** — PR #36 |
| `LEX-025` | Test d'acceptation flux complet : `tests/test_acceptance_full_flow.py`. 4 scénarios sur accord réaliste avec citations variées. | 141 tests verts. Aucune modification `src/`. | **TERMINÉ** — PR #38 |
| `LEX-026` | `InMemoryLegalResultStore` dans `src/lex_syndic/storage/legal_results.py`. API : `save`, `get`, `list_ids`, `clear`. 7 tests verts. | 148 tests globaux verts. Aucune écriture disque. Aucune dépendance externe. | **TERMINÉ** — PR #40 |
| `LEX-027` | `analyze_and_store_legal_text()` dans `src/lex_syndic/interface/session_handler.py`. `LegalSessionResult` expose `record_id` + `result`. 6 tests verts. Store injecté par l'appelant. | 154 tests globaux verts. Aucun store global. Aucune dépendance externe. | **TERMINÉ** — PR #42 |
| `LEX-028` | Test d'acceptation session complet : `tests/test_acceptance_session_flow.py`. 6 scénarios sur accord réaliste avec citations variées, isolation stores, cas insufficient_data. | 160 tests globaux verts. Aucune modification `src/`. | **TERMINÉ** — PR #44 |
| `LEX-029` | Audit maturité produit avant exposition externe : `docs/audits/LEX_029_PRODUCT_MATURITY_AUDIT.md`. Évaluation contrats, couplages, limites métier, verdict API. | Audit produit. Aucune modification `src/` ni `tests/`. | **TERMINÉ** — PR #45 |
| `LEX-030` | Couche API locale mono-utilisateur pure Python : `src/lex_syndic/api/local.py`. `LocalApiAnalysisRequest` → `submit_analysis()` → `LocalApiAnalysisResponse`. 7 tests verts. Sans serveur HTTP, sans dépendance externe. | 167 tests globaux verts. Aucun store global. | **TERMINÉ** — PR #47 |
| `LEX-031` | Test d'acceptation API locale : `tests/test_acceptance_api_local.py`. 7 scénarios sur accord réaliste, record_id, store.get(), report_text, insufficient_data, isolation stores, absence FastAPI. | 174 tests globaux verts. Aucune modification `src/`. | **TERMINÉ** — PR #49 |
| `LEX-032` | Découplage `storage → interface` : `InMemoryLegalResultStore` rendu générique via `Generic[T]`. Aucun import `lex_syndic.interface` dans `storage`. 2 tests de découplage ajoutés. | 176 tests globaux verts. Comportement inchangé. | **TERMINÉ** — PR #51 |
| `LEX-033` | Cadrage FastAPI avant implémentation : `docs/architecture/LEX_033_FASTAPI_EXPOSURE_FRAME.md`. Contrat API (`POST /v1/analyze`, `GET /v1/results/{record_id}`, `GET /health`), prérequis, risques, recommandation LEX-034. | Document de cadrage. Aucune modification `src/` ni `tests/`. | **TERMINÉ** — PR #53 |
| `LEX-034` | API FastAPI locale mono-utilisateur : `src/lex_syndic/api/fastapi_app.py`. `POST /v1/analyze`, `GET /v1/results/{record_id}`, `GET /health`. Routes `/docs` `/redoc` `/openapi.json` désactivées. Guard texte (vide → 422, > 50 000 chars → 422). `fastapi` + `uvicorn[standard]` ajoutés. 7 tests dans `tests/test_api_fastapi.py`. | 183 tests globaux verts. Aucune persistance, aucune auth, aucun DB. DEC-LEX-034 ajoutée. | **EN COURS** — PR #54, validation ChatGPT requise |

### Hors plan à ce stade

Aucune décision n'est prise sur :
- persistance disque ou base de données des résultats ;
- toute brique NLP, LLM, Légifrance, Judilibre ;
- frontend, MCP utilisateur ;
- exposition réseau (route publique ou TLS) — exige décision séparée dans DECISIONS.md ;
- activation des routes de documentation FastAPI — exige décision séparée dans DECISIONS.md.

### Séquence rail

- `RAIL-001` utilise `lex_syndic_v2` comme dépôt support de validation du rail
  ChatGPT → GitHub → Codex.
- Dans cette séquence, l'objectif rail prime sur l'avancement fonctionnel du
  produit.
- Toute mission future de rail doit expliciter séparément l'objectif rail,
  l'objectif produit, la preuve attendue, l'état GitHub, le retour Codex et le
  verdict ChatGPT.

### Cadrage MIG-009

- Cette mission de cadrage ne lance aucune implémentation `report`.
- Sorties attendues du cadrage :
  - périmètre fonctionnel report ;
  - entrées attendues ;
  - sortie minimale attendue ;
  - fichiers autorisés pour la future mission d'implémentation ;
  - fichiers interdits ;
  - invariants ;
  - tests attendus ;
  - critères PASS/BLOCK.

### Cadrage MIG-010

- Cette mission de cadrage ne lance aucune implémentation `interface`.
- Sorties attendues du cadrage :
  - périmètre fonctionnel interface ;
  - type d'interface minimal ;
  - entrées attendues ;
  - sorties attendues ;
  - fichiers autorisés pour la future mission d'implémentation ;
  - fichiers interdits ;
  - invariants ;
  - tests attendus ;
  - critères PASS/BLOCK.
