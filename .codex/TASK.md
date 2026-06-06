# Task

TASK_ID:
ACT-013-RECOVERY-AUDIT-LEX-SYNDIC-V2

MODE:
PROOF_ONLY

STATUS:
EXECUTED

TARGET_REPO:
lex_syndic-v2

GOAL:
produce a full factual repository state without modification

product_task_authorized:
no

implementation_authorized:
no

ALLOWED_ACTIONS:
- read governance files
- read .codex files
- run git proof commands
- produce the final report

FORBIDDEN_ACTIONS:
- modify files
- create branch
- commit
- push
- merge
- install dependencies
- launch refactor

REQUIRED_PROOFS:
- repo root
- branch
- HEAD
- origin/main
- git status
- root governance files present
- .codex files present
- active task state or no active task state

OUTPUT_FORMAT:
- VERDICT
- RAISON UNIQUE
- REPO_STATE
- GOVERNANCE_FILES
- CODEX_FILES
- ACTIVE_TASK_STATE
- RISKS
- NEXT_REQUIRED_ACTION

next_required_action:
- explicit new scoping or collection by agent-control-tower before any development
