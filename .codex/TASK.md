# Task

TASK_ID: LXS2-20260429-001
MODE: PROOF_ONLY
TARGET_REPO: Drs926/lex_syndic-v2
TARGET_BRANCH: main
BRANCH_KIND: main
LOCAL_PATH: C:\Users\Harib\CascadeProjects\lex_syndic_v2
STATUS: READY_FOR_AGENT
OWNER: codex

## OBJECTIVE

Réaliser un état des lieux factuel du repo `Drs926/lex_syndic-v2` sans modifier le code, sans modifier la gouvernance existante et sans committer de fichier métier.

## CONTEXT

`lex_syndic-v2` est un projet prioritaire de système d’analyse juridique syndicale. Le repo local a été synchronisé avec `origin/main` au commit `c138f7a8fa6fb1e84feadb30d3bfd9936f18cb95`, puis le rail `.codex` minimal a été ajouté sur GitHub. Le fichier `AGENTS.md` existe déjà et reste souverain pour les règles projet.

Cette première tâche sert uniquement à produire une photographie vérifiable de l’état réel avant toute nouvelle action.

## PREFLIGHT_GATES

- Lire `AGENTS.md`.
- Confirmer la branche courante avec `git branch --show-current`.
- Confirmer le working tree avec `git status --short`.
- BLOCK si la branche courante n’est pas `main`.
- BLOCK si le working tree contient des changements hors scope avant exécution.
- Faire `git pull` avant l’exécution pour récupérer les fichiers `.codex` ajoutés sur GitHub.

## SCOPE

- Lire la structure du repo.
- Lire les fichiers de gouvernance racine existants : `README.md`, `AGENTS.md`, `PLAN.md`, `SPEC.md`, `STATUS.md`, `DECISIONS.md`, `MIGRATION_POLICY.md`, `OUTPUT_CONTRACT.md`, `PROMPTS_INDEX.md` si présents.
- Lire les dossiers structurants visibles : `src/`, `tests/`, `docs/` si présents.
- Identifier les commits récents et la dernière migration visible.
- Identifier les commandes de vérification disponibles sans installer de dépendance.
- Exécuter uniquement les commandes de lecture et de vérification explicitement autorisées.
- Mettre à jour uniquement `.codex/STATUS.md`, `.codex/RESULT.md`, `.codex/PROOF.md` et `.codex/HANDOFF.md`.

## OUT_OF_SCOPE

- Ne pas modifier `src/`.
- Ne pas modifier `tests/`.
- Ne pas modifier `docs/`.
- Ne pas modifier les fichiers de gouvernance racine.
- Ne pas modifier `AGENTS.md`.
- Ne pas installer de dépendance.
- Ne pas créer de branche.
- Ne pas ouvrir de PR.
- Ne pas modifier le repo central `Drs926/agent-control-tower`.

## FILES_ALLOWED

- .codex/STATUS.md
- .codex/RESULT.md
- .codex/PROOF.md
- .codex/HANDOFF.md

## FILES_READ_ALLOWED

- AGENTS.md
- README.md
- PLAN.md
- SPEC.md
- STATUS.md
- DECISIONS.md
- MIGRATION_POLICY.md
- OUTPUT_CONTRACT.md
- PROMPTS_INDEX.md
- pyproject.toml
- pytest.ini
- requirements.txt
- docs/**
- src/**
- tests/**
- .codex/TASK.md

## FILES_FORBIDDEN

- Tout fichier hors `FILES_ALLOWED` en écriture.
- Tout fichier du repo central `Drs926/agent-control-tower`.

## COMMANDS_ALLOWED

- git branch --show-current
- git status --short
- git log --oneline --decorate -10
- git rev-list --left-right --count origin/main...main
- git ls-files
- git diff --stat
- type AGENTS.md
- type README.md
- type PLAN.md
- type SPEC.md
- type STATUS.md
- type DECISIONS.md
- type MIGRATION_POLICY.md
- type OUTPUT_CONTRACT.md
- type PROMPTS_INDEX.md
- type pyproject.toml
- type pytest.ini
- python -m pytest -q

## COMMAND_RULES

- Ne lancer `python -m pytest -q` que si un fichier de configuration ou un dossier `tests/` existe.
- Ne pas exécuter `pip install`.
- Ne pas modifier l’environnement.
- Si une commande échoue, documenter l’échec au lieu de corriger.

## EXPECTED_RESULT_FILE

.codex/RESULT.md

## EXPECTED_PROOF_FILE

.codex/PROOF.md

## PROOFS_REQUIRED

- branche courante ;
- état `git status --short` avant action ;
- écart `origin/main...main` ;
- liste synthétique des fichiers lus ;
- commandes exécutées ;
- résultat des commandes ;
- liste exacte des fichiers modifiés ;
- confirmation qu’aucun fichier métier n’a été modifié.

## PR_RULES_IF_APPLICABLE

Aucune PR dans cette tâche.

## BLOCK_CONDITIONS

- Branche courante différente de `main`.
- Working tree sale avant exécution hors fichiers `.codex` synchronisés.
- Besoin de modifier un fichier hors `.codex`.
- Besoin d’installer une dépendance.
- Test ou commande destructrice nécessaire.

## NEXT_ACTION

Faire `git pull`, puis lancer Codex ou Claude localement avec : `Lis .codex/TASK.md et exécute strictement.`
