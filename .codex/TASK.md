# Task

TASK_ID:
LXS2-20260429-004B

TITLE:
MIG-007B — Gouverneur

ROLE:
Gouverneur

GOAL:
Mettre à jour la gouvernance racine et les traces `.codex` après la réussite prouvée de `MIG-007A`, sans modifier `src/`, `tests/` ni `docs/`.

FILES_ALLOWED:
- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `PROMPTS_INDEX.md`
- `.codex/TASK.md`
- `.codex/STATUS.md`
- `.codex/RESULT.md`
- `.codex/PROOF.md`
- `.codex/HANDOFF.md`

FILES_FORBIDDEN:
- `AGENTS.md`
- `MIGRATION_POLICY.md`
- `OUTPUT_CONTRACT.md`
- `docs/**`
- `src/**`
- `tests/**`
- `pyproject.toml`
- `README.md`

REQUIRED_CHECKS:
- `git diff -- PLAN.md STATUS.md DECISIONS.md PROMPTS_INDEX.md .codex/TASK.md .codex/STATUS.md .codex/RESULT.md .codex/PROOF.md .codex/HANDOFF.md`
- `git diff --cached --name-only`

COMMIT_MESSAGE:
`update governance after MIG-007A lexical retrieval`
