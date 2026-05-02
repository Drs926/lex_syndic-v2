# PROOF

## Repository state

- Branch expected: `main`
- Local and remote must be aligned before this mission.
- Worktree must be clean before this mission.

## Governance state used as source

Root governance files declare:
- `MIG-001` to `MIG-010` completed.
- `MIG-010A PASS`.
- Rail validation sequence documented through `RAIL-006`.
- No active product implementation task.

## Scope proof

Allowed changed files:
- `.codex/STATUS.md`
- `.codex/RESULT.md`
- `.codex/PROOF.md`
- `.codex/HANDOFF.md`

Forbidden changed files:
- `src/**`
- `tests/**`
- `docs/**`
- root governance files
- dependency files

## Required post-change checks

Run:

git diff --name-only
git diff --stat
git status --short

PASS only if the diff is limited to the four allowed `.codex/*` files.
