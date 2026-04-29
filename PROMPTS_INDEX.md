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
