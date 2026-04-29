# Task

TASK_ID: LXS2-20260429-002
MODE: DOC_ONLY
TARGET_REPO: Drs926/lex_syndic-v2
TARGET_BRANCH: main
BRANCH_KIND: main
LOCAL_PATH: C:\Users\Harib\CascadeProjects\lex_syndic_v2
STATUS: READY_FOR_AGENT
OWNER: codex

## OBJECTIVE

Aligner uniquement la documentation de gouvernance avec l’état réel prouvé par `LXS2-20260429-001`, sans modifier le code, les tests, l’architecture produit ou les migrations.

## CONTEXT

La tâche `LXS2-20260429-001` a validé l’état réel suivant :

- branche `main` ;
- local et `origin/main` alignés ;
- dernière migration métier visible : `MIG-005` ;
- `python -m pytest -q` : `47 passed in 0.17s` ;
- fichiers métiers, tests, docs et gouvernance racine non modifiés pendant la mission PROOF_ONLY ;
- risque identifié : `README.md` décrit un état de vérification plus ancien que les preuves actuelles.

Cette tâche doit uniquement aligner les documents concernés avec ces preuves. Elle ne doit pas préparer ni lancer `MIG-006`.

## PREFLIGHT_GATES

- Lire `AGENTS.md`.
- Confirmer la branche courante avec `git branch --show-current`.
- Confirmer le working tree avec `git status --short`.
- BLOCK si la branche courante n’est pas `main`.
- BLOCK si le working tree contient des changements hors scope avant exécution.
- Faire `git pull` avant l’exécution.

## SCOPE

- Lire `README.md`, `STATUS.md`, `PLAN.md`, `PROMPTS_INDEX.md`, `OUTPUT_CONTRACT.md`, `.codex/RESULT.md`, `.codex/PROOF.md`.
- Modifier uniquement les documents nécessaires pour aligner l’état affiché avec les preuves actuelles.
- Priorité d’alignement : `README.md` et `STATUS.md` si leur contenu est en retard.
- Mettre à jour `.codex/STATUS.md`, `.codex/RESULT.md`, `.codex/PROOF.md` et `.codex/HANDOFF.md` pour tracer l’exécution.
- Exécuter `python -m pytest -q` après modification documentaire si disponible, pour confirmer l’absence d’impact.

## OUT_OF_SCOPE

- Ne pas modifier `src/`.
- Ne pas modifier `tests/`.
- Ne pas modifier `docs/architecture/`.
- Ne pas modifier `DECISIONS.md` sauf si une contradiction factuelle bloquante est trouvée.
- Ne pas modifier `AGENTS.md`.
- Ne pas modifier `MIGRATION_POLICY.md`.
- Ne pas créer `MIG-006`.
- Ne pas ajouter de nouvelle capacité produit.
- Ne pas installer de dépendance.
- Ne pas créer de branche.
- Ne pas ouvrir de PR.
- Ne pas modifier le repo central `Drs926/agent-control-tower`.

## FILES_ALLOWED

- README.md
- STATUS.md
- PLAN.md
- PROMPTS_INDEX.md
- .codex/STATUS.md
- .codex/RESULT.md
- .codex/PROOF.md
- .codex/HANDOFF.md

## FILES_READ_ALLOWED

- AGENTS.md
- README.md
- STATUS.md
- PLAN.md
- PROMPTS_INDEX.md
- OUTPUT_CONTRACT.md
- pyproject.toml
- .codex/TASK.md
- .codex/RESULT.md
- .codex/PROOF.md
- .codex/HANDOFF.md

## FILES_FORBIDDEN

- src/**
- tests/**
- docs/architecture/**
- AGENTS.md
- MIGRATION_POLICY.md
- DECISIONS.md sauf contradiction factuelle bloquante
- tout fichier du repo central `Drs926/agent-control-tower`

## COMMANDS_ALLOWED

- git branch --show-current
- git status --short
- git pull
- git rev-list --left-right --count origin/main...main
- git diff --stat
- git diff -- README.md STATUS.md PLAN.md PROMPTS_INDEX.md .codex/STATUS.md .codex/RESULT.md .codex/PROOF.md .codex/HANDOFF.md
- type AGENTS.md
- type README.md
- type STATUS.md
- type PLAN.md
- type PROMPTS_INDEX.md
- type OUTPUT_CONTRACT.md
- type pyproject.toml
- type .codex\RESULT.md
- type .codex\PROOF.md
- python -m pytest -q

## COMMAND_RULES

- Ne pas exécuter `pip install`.
- Ne pas modifier l’environnement.
- Si `python -m pytest -q` échoue, documenter l’échec au lieu de corriger.

## EXPECTED_RESULT_FILE

.codex/RESULT.md

## EXPECTED_PROOF_FILE

.codex/PROOF.md

## PROOFS_REQUIRED

- branche courante ;
- état `git status --short` avant action ;
- écart `origin/main...main` ;
- diff stat ;
- liste exacte des fichiers modifiés ;
- résultat `python -m pytest -q` ;
- confirmation qu’aucun fichier `src/`, `tests/`, `docs/architecture/`, `AGENTS.md`, `MIGRATION_POLICY.md` n’a été modifié.

## PR_RULES_IF_APPLICABLE

Aucune PR dans cette tâche.

## BLOCK_CONDITIONS

- Branche courante différente de `main`.
- Working tree sale avant exécution.
- Besoin de modifier un fichier interdit.
- Besoin de créer ou préparer `MIG-006`.
- Besoin d’installer une dépendance.

## NEXT_ACTION

Faire `git pull`, puis lancer Codex ou Claude localement avec : `Lis .codex/TASK.md et exécute strictement.`
