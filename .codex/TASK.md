TASK_ID:
LEX-044

PROJECT:
lex_syndic-v2

TASK_TYPE:
product-task

MODE:
PRODUCT_TASK

TARGET_REPO:
lex_syndic-v2

PRODUCT_BRANCH:
lex-044-list-dossiers-status

GOAL:
Execute the active cockpit cycle as a real product task.
Read governance files (PLAN.md, DECISIONS.md, STATUS.md, docs/) to understand
the exact scope. Produce only the files within the authorised scope below.
Write the 4 required .codex/ output files when done.

MISSION_DETAIL:
# LEX_044_PRODUCT_MISSION

OBJECTIF
Implémenter une nouvelle capacité Lex-Syndic permettant d'exposer un endpoint FastAPI de liste des dossiers analysés avec leur statut juridique synthétique.

ENDPOINT CIBLE
GET /v1/dossiers

RÉPONSE ATTENDUE
Retourner la liste des dossiers connus en mémoire, sans report_text complet, avec au minimum :
- dossier_id
- juridical_status
- alert_level
- recommended_action

CONTRAINTES
Do not run full-cycle automatically.
Do not invoke agent automatically.
Do not git push.
Do not create PR.
Do not merge.
Do not modify product code during ACT handoff preparation.

ATTENDU
Préparer le cycle LEX-044 comme product-task contrôlé, avec handoff agent prêt, sans exécution agent automatique.

ALLOWED_ACTIONS:
- read any file in the repository
- write or modify product files within the authorised scope
- run tests (e.g. python -m pytest -q) to verify correctness
- write .codex/STATUS.md
- write .codex/RESULT.md
- write .codex/PROOF.md
- write .codex/HANDOFF.md

FORBIDDEN_ACTIONS:
- create branch
- commit
- push
- merge
- modify governance files (STATUS.md, PLAN.md, DECISIONS.md, PROMPTS_INDEX.md,
  HISTORY.md, AUDIT.md, RETRO.md) - ACT manages those
- modify .codex/ files other than the 4 required output files
- add dependencies not explicitly authorised by this task's scope
- add authentication, disk persistence, database, MCP, LLM unless explicitly in scope

REQUIRED_OUTPUT_FILES:
Write ALL 4 files below to disk AFTER completing the implementation.

Write .codex/STATUS.md:
VERDICT: PASS
RAISON_UNIQUE: <one factual sentence>
repo_root: <absolute path>
branch: main
HEAD: <short sha>
status_clean: no
product_files_modified: <list of files written or modified>
tests_passed: <count or not applicable>

Write .codex/RESULT.md:
VERDICT: PASS
TASK_ID: LEX-044
MODE: PRODUCT_TASK
RAISON_UNIQUE: <one factual sentence>
FILES_CREATED: <list or none>
FILES_MODIFIED: <list or none>
SRC_MODIFIED: yes or no
PRODUCT_FILES_MODIFIED: yes

Write .codex/PROOF.md:
VERDICT: PASS
repo_root: <absolute path>
branch: main
HEAD: <short sha>
origin_main: <short sha>
status_clean: no
dirty_files: <list of new/modified product files>
FORBIDDEN_ACTIONS_EXECUTED: none

Write .codex/HANDOFF.md:
current_state: AGENT_COMPLETED
task_id: LEX-044
agent_verdict: PASS
files_created: <list>
files_modified: <list or none>
next_action: prepare-product-pr lex_syndic-v2 LEX-044 lex-044-list-dossiers-status