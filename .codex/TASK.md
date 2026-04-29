# Task

TASK_ID: none
MODE: none
TARGET_REPO: Drs926/lex_syndic-v2
TARGET_BRANCH: main
BRANCH_KIND: main
LOCAL_PATH: C:\Users\Harib\CascadeProjects\lex_syndic_v2
STATUS: IDLE
OWNER: none

## OBJECTIVE

Aucune tâche active.

## CONTEXT

Rail `.codex` initialisé pour un projet prioritaire déjà gouverné par `AGENTS.md` et les fichiers racine du repo. Les règles existantes du projet restent souveraines.

## PREFLIGHT_GATES

- Lire `AGENTS.md`.
- Confirmer la branche courante avec `git branch --show-current`.
- Confirmer le working tree avec `git status --short`.
- Bloquer si la branche courante diffère de `TARGET_BRANCH`.
- Bloquer si le working tree contient des changements hors scope.

## SCOPE

Aucun.

## OUT_OF_SCOPE

Aucun.

## FILES_ALLOWED

Aucun.

## FILES_FORBIDDEN

Aucun.

## COMMANDS_ALLOWED

Aucune.

## EXPECTED_RESULT_FILE

.codex/RESULT.md

## EXPECTED_PROOF_FILE

.codex/PROOF.md

## BLOCK_CONDITIONS

Toute exécution tant qu'aucune tâche active n'est définie.

## NEXT_ACTION

Créer une première tâche PROOF_ONLY d'état des lieux après validation externe.
