# PROMPTS_INDEX

Index chronologique des missions exécutées sur V2.

Format d'une entrée :

```
## PROMPT-XXX — Titre court
Date : YYYY-MM-DD
Mission : ...
Périmètre autorisé : ...
Verdict : OK | PARTIAL | BLOCKED
Fichiers modifiés : ...
Référence : (commit, audit ou document de sortie)
```

---

## PROMPT-001 — Stabilisation du dépôt V2 comme base canonique gouvernable
Date : 2026-04-27
Mission : Stabiliser V2 comme base canonique sans migrer de code depuis V1.
Remplir les fichiers racine vides, créer les documents de gouvernance manquants
(`SPEC.md`, `OUTPUT_CONTRACT.md`, `DECISIONS.md`, `MIGRATION_POLICY.md`,
`STATUS.md`, `PROMPTS_INDEX.md`), définir les lots de migration `MIG-001` à
`MIG-010` dans `PLAN.md`.
Périmètre autorisé : fichiers racine de gouvernance uniquement.
Interdits respectés : pas de modification de `src/`, pas de modification de
`tests/`, pas d'intégration de code V1, pas de technologie nouvelle, pas de
backend, frontend, MCP, graphe, Open WebUI, Légifrance ou Judilibre.
Verdict : OK
Fichiers modifiés : `README.md`, `CONTEXT.md`, `AGENTS.md`, `PLAN.md`,
`SPEC.md`, `OUTPUT_CONTRACT.md`, `DECISIONS.md`, `MIGRATION_POLICY.md`,
`STATUS.md`, `PROMPTS_INDEX.md`.
Référence : sortie contractuelle de la session du 2026-04-27.

## PROMPT-002 — Alignement documentaire avec la preuve du dépôt
Date : 2026-04-29
Mission : Aligner uniquement la documentation de gouvernance avec l'état réel
prouvé par `LXS2-20260429-001`, sans modifier le code, les tests,
l'architecture produit ou les migrations.
Périmètre autorisé : `README.md`, `STATUS.md`, `PLAN.md`, `PROMPTS_INDEX.md`
et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `README.md`, `STATUS.md`, `PROMPTS_INDEX.md`,
`.codex/STATUS.md`, `.codex/RESULT.md`, `.codex/PROOF.md`,
`.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-29 pour
`LXS2-20260429-002`.

## PROMPT-003 — MIG-006 minimal et teste pour le module rules
Date : 2026-04-29
Mission : Implementer `MIG-006` de maniere minimale et testee pour le module
`rules`, sans dependance externe ni capacite hors lot.
Périmètre autorisé : `src/lex_syndic/rules/**`, `tests/test_rules*.py`,
`DECISIONS.md`, `STATUS.md`, `PLAN.md`, `PROMPTS_INDEX.md` et fichiers
`.codex/`.
Verdict : OK
Fichiers modifiés : `src/lex_syndic/rules/__init__.py`,
`src/lex_syndic/rules/simple_rules.py`, `tests/test_rules_simple_rules.py`,
`DECISIONS.md`, `STATUS.md`, `PLAN.md`, `PROMPTS_INDEX.md`,
`.codex/STATUS.md`, `.codex/RESULT.md`, `.codex/PROOF.md`,
`.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-29 pour
`LXS2-20260429-003`.

## PROMPT-004 — MIG-007A retrieval lexical minimal
Date : 2026-04-30
Mission : Executer `LXS2-20260429-004A` en role `Migrator` strict pour
implementer un retrieval lexical minimal, local, deterministe et teste, sans
modifier la gouvernance racine.
Périmètre autorisé : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`, `src/lex_syndic/retrieval/**`,
`tests/test_retrieval*.py`.
Verdict : OK
Fichiers modifiés : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`,
`src/lex_syndic/retrieval/__init__.py`,
`src/lex_syndic/retrieval/lexical.py`, `tests/test_retrieval_lexical.py`.
Référence : commit `d7278b7` et sortie contractuelle de la session du
2026-04-30 pour `LXS2-20260429-004A`.

## PROMPT-005 — MIG-007B gouvernance après MIG-007A
Date : 2026-04-30
Mission : Executer la mission `Gouverneur` de mise a jour de la gouvernance
apres la reussite de `MIG-007A`, sans modifier `src/`, `tests/` ou `docs/`.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260429-004B`.

## PROMPT-006 — MIG-008 cadrage storage sans implementation
Date : 2026-04-30
Mission : Prepararer `MIG-008` en mission de cadrage uniquement pour definir
le perimetre `storage` avant toute implementation de code.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260430-005`.

## PROMPT-007 — MIG-008A storage minimal implementation
Date : 2026-04-30
Mission : Executer `LXS2-20260430-005A` en role `Migrator` strict pour
implementer un storage minimal, local, deterministe et teste, sans modifier la
gouvernance racine.
Périmètre autorisé : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`, `src/lex_syndic/storage/**`,
`tests/test_storage*.py`.
Verdict : OK
Fichiers modifiés : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`, `src/lex_syndic/storage/__init__.py`,
`src/lex_syndic/storage/memory.py`, `tests/test_storage_minimal.py`.
Référence : commit `f8dec95` et sortie contractuelle de la session du
2026-04-30 pour `LXS2-20260430-005A`.

## PROMPT-008 — MIG-008B gouvernance après MIG-008A
Date : 2026-04-30
Mission : Executer la mission `Gouverneur` de mise a jour de la gouvernance
apres la reussite de `MIG-008A`, sans modifier `src/`, `tests/` ou `docs/`.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260430-005B`.

## PROMPT-009 — MIG-009 cadrage report sans implementation
Date : 2026-04-30
Mission : Preparer `MIG-009` en mission de cadrage uniquement pour definir
precisement le perimetre du futur module `report` avant toute implementation
de code.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260430-006`.

## PROMPT-010 — MIG-009A report minimal implementation
Date : 2026-04-30
Mission : Executer `LXS2-20260430-006A` en role `Migrator` strict pour
implementer un module `report` minimal, local, deterministe et teste, sans
modifier la gouvernance racine.
Périmètre autorisé : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`, `src/lex_syndic/report/**`,
`tests/test_report*.py`.
Verdict : OK
Fichiers modifiés : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`, `src/lex_syndic/report/__init__.py`,
`src/lex_syndic/report/text.py`, `tests/test_report_minimal.py`.
Référence : commit `6b90ff4` et sortie contractuelle de la session du
2026-04-30 pour `LXS2-20260430-006A`.

## PROMPT-011 — MIG-009B gouvernance après MIG-009A
Date : 2026-04-30
Mission : Executer la mission `Gouverneur` de mise a jour de la gouvernance
apres la reussite de `MIG-009A`, sans modifier `src/`, `tests/` ou `docs/`.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260430-006B`.

## PROMPT-012 — MIG-010 cadrage interface sans implementation
Date : 2026-04-30
Mission : Preparer `MIG-010` en mission de cadrage uniquement pour definir
precisement le perimetre du futur module `interface` avant toute
implementation de code.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260430-007`.

## PROMPT-013 — MIG-010A interface minimal implementation
Date : 2026-04-30
Mission : Executer `LXS2-20260430-007A` en role `Migrator` strict pour
implementer un module `interface` minimal, local, deterministe et teste, sans
modifier la gouvernance racine.
Périmètre autorisé : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`, `src/lex_syndic/interface/**`,
`tests/test_interface*.py`.
Verdict : OK
Fichiers modifiés : `.codex/TASK.md`, `.codex/STATUS.md`, `.codex/RESULT.md`,
`.codex/PROOF.md`, `.codex/HANDOFF.md`,
`src/lex_syndic/interface/__init__.py`,
`src/lex_syndic/interface/core.py`, `tests/test_interface_minimal.py`.
Référence : commit `1973e44` et sortie contractuelle de la session du
2026-04-30 pour `LXS2-20260430-007A`.

## PROMPT-014 — MIG-010B gouvernance après MIG-010A
Date : 2026-04-30
Mission : Executer la mission `Gouverneur` de mise a jour de la gouvernance
apres la reussite de `MIG-010A`, sans modifier `src/`, `tests/` ou `docs/`.
Périmètre autorisé : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md` et fichiers `.codex/`.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`, `.codex/TASK.md`, `.codex/STATUS.md`,
`.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
Référence : sortie contractuelle de la session du 2026-04-30 pour
`LXS2-20260430-007B`.

## PROMPT-015 — RAIL-001 validation du rail ChatGPT → GitHub → Codex
Date : 2026-05-01
Mission : Valider le rail de travail ChatGPT → GitHub → Codex sur
`lex_syndic_v2` via une modification documentaire minimale, sans créer de
nouvelle brique produit ni élargir le périmètre fonctionnel de Lex-Syndic.
Périmètre autorisé : fichiers de gouvernance racine strictement nécessaires.
Verdict : OK
Fichiers modifiés : `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`PROMPTS_INDEX.md`.
Référence : sortie contractuelle de la session du 2026-05-01 pour
`RAIL-001`.

## PROMPT-016 — RAIL-005A trace locale issue → branche → preuve
Date : 2026-05-01
Mission : Ajouter une trace documentaire minimale de `RAIL-005` depuis le
worktree sain `lex_syndic_v2_clean`, après création de l'issue GitHub `#4` et
de la branche locale `rail/005-local-proof-issue-handoff`, sans changement
produit.
Périmètre autorisé : `STATUS.md` et `PROMPTS_INDEX.md` uniquement.
Verdict : OK
Fichiers modifiés : `STATUS.md`, `PROMPTS_INDEX.md`.
Référence : sortie contractuelle de la session du 2026-05-01 pour `RAIL-005A`.

## PROMPT-017 — RAIL-006 cycle accéléré gouverné
Date : 2026-05-01
Mission : Exécuter en une seule mission le cycle `RAIL-006` depuis le
worktree sain `lex_syndic_v2_clean` : issue GitHub `#6`, branche dédiée,
diff documentaire minimal, commit, push et création de PR, sans changement
produit ni merge.
Périmètre autorisé : `STATUS.md` et `PROMPTS_INDEX.md` uniquement.
Verdict : OK
Fichiers modifiés : `STATUS.md`, `PROMPTS_INDEX.md`.
Référence : sortie contractuelle de la session du 2026-05-01 pour `RAIL-006`.
