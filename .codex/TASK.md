# Task

TASK_ID: LXS2-20260429-003
MODE: CODE_ACTION
TARGET_REPO: Drs926/lex_syndic-v2
TARGET_BRANCH: main
BRANCH_KIND: main
LOCAL_PATH: C:\Users\Harib\CascadeProjects\lex_syndic_v2
STATUS: READY_FOR_AGENT
OWNER: codex

## OBJECTIVE

Implémenter `MIG-006` de manière minimale et testée : module `rules`, règles calculables simples, sortie `RuleCheckResult`, sans jugement juridique avancé ni dépendance externe.

## CONTEXT

`PLAN.md` définit `MIG-006` ainsi :

- module cible : `rules` ;
- contenu : règles calculables, seuils, validation conformité ;
- critère de sortie : sortie `RuleCheckResult` testée ;
- état actuel : en attente.

`MIGRATION_POLICY.md` impose : périmètre limité à un module canonique, pas de copie aveugle depuis V1, tests obligatoires, entrée `DECISIONS.md`, sortie contractuelle.

État prouvé avant tâche :

- `MIG-005` dernière migration métier visible ;
- `RuleCheckResult` existe déjà dans `src/lex_syndic/legal/models.py` ;
- `src/lex_syndic/rules/__init__.py` est vide ;
- aucun test spécifique `rules` trouvé ;
- dernière vérification connue : `python -m pytest -q` → `47 passed`.

## PREFLIGHT_GATES

- Lire `AGENTS.md`.
- Lire `MIGRATION_POLICY.md`.
- Lire `PLAN.md`.
- Confirmer la branche courante avec `git branch --show-current`.
- Confirmer le working tree avec `git status --short`.
- Faire `git pull` avant exécution.
- BLOCK si la branche courante n’est pas `main`.
- BLOCK si le working tree contient des changements hors scope avant exécution.

## SCOPE

- Implémenter une couche minimale dans `src/lex_syndic/rules/`.
- Utiliser les modèles canoniques existants, notamment `Clause` et `RuleCheckResult`.
- Ajouter des règles déterministes simples sans raisonnement juridique avancé.
- Ajouter des tests dédiés sous `tests/`.
- Mettre à jour `DECISIONS.md` avec l’entrée MIG-006 obligatoire.
- Mettre à jour `STATUS.md`, `PLAN.md` et `PROMPTS_INDEX.md` pour refléter MIG-006 uniquement si la migration passe.
- Mettre à jour `.codex/STATUS.md`, `.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
- Exécuter `python -m pytest -q`.

## IMPLEMENTATION_BOUNDARIES

MIG-006 doit rester minimal :

- pas d’extraction juridique ;
- pas de Légifrance ;
- pas de Judilibre ;
- pas de scoring avancé ;
- pas de graphe ;
- pas de NLP ;
- pas de dépendance externe ;
- pas de modification des lots MIG-007 à MIG-010.

Exemples acceptables de règles calculables minimales :

- clause vide → `non_conforme` ;
- clause sans contenu exploitable → `risque` ou `unknown` selon convention déterministe ;
- clause avec `compliance_status` déjà renseigné → conversion déterministe vers `RuleCheckResult` ;
- règle simple avec `rule_code` stable et message déterministe.

## OUT_OF_SCOPE

- Ne pas modifier `docs/architecture/`.
- Ne pas modifier `MIGRATION_POLICY.md`.
- Ne pas modifier `AGENTS.md`.
- Ne pas introduire de technologie nouvelle.
- Ne pas créer `MIG-007` ou suivant.
- Ne pas créer de backend, frontend, MCP, graphe, Open WebUI, connecteur Légifrance ou Judilibre.
- Ne pas installer de dépendance.
- Ne pas créer de branche.
- Ne pas ouvrir de PR.
- Ne pas modifier le repo central `Drs926/agent-control-tower`.

## FILES_ALLOWED

- src/lex_syndic/rules/**
- tests/test_rules*.py
- tests/test_rules_*.py
- DECISIONS.md
- STATUS.md
- PLAN.md
- PROMPTS_INDEX.md
- .codex/STATUS.md
- .codex/RESULT.md
- .codex/PROOF.md
- .codex/HANDOFF.md

## FILES_READ_ALLOWED

- AGENTS.md
- PLAN.md
- STATUS.md
- DECISIONS.md
- MIGRATION_POLICY.md
- OUTPUT_CONTRACT.md
- PROMPTS_INDEX.md
- pyproject.toml
- src/lex_syndic/legal/models.py
- src/lex_syndic/rules/**
- tests/**
- .codex/TASK.md

## FILES_FORBIDDEN

- docs/architecture/**
- AGENTS.md
- MIGRATION_POLICY.md
- pyproject.toml
- src/lex_syndic/analysis/**
- src/lex_syndic/comparison/**
- src/lex_syndic/ingestion/**
- src/lex_syndic/retrieval/**
- src/lex_syndic/storage/**
- src/lex_syndic/report/**
- src/lex_syndic/interface/**
- tout fichier du repo central `Drs926/agent-control-tower`

## COMMANDS_ALLOWED

- git branch --show-current
- git status --short
- git pull
- git rev-list --left-right --count origin/main...main
- git diff --stat
- git diff -- src/lex_syndic/rules tests DECISIONS.md STATUS.md PLAN.md PROMPTS_INDEX.md .codex/STATUS.md .codex/RESULT.md .codex/PROOF.md .codex/HANDOFF.md
- type AGENTS.md
- type PLAN.md
- type STATUS.md
- type DECISIONS.md
- type MIGRATION_POLICY.md
- type OUTPUT_CONTRACT.md
- type PROMPTS_INDEX.md
- type pyproject.toml
- type src\lex_syndic\legal\models.py
- python -m pytest -q

## COMMAND_RULES

- Ne pas exécuter `pip install`.
- Ne pas modifier l’environnement.
- Si `python -m pytest -q` échoue après modification, corriger uniquement dans le périmètre autorisé.
- Si la correction exige un fichier interdit, STOP et documenter BLOCK.

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
- confirmation que `RuleCheckResult` est utilisé ;
- confirmation qu’aucune dépendance externe n’a été ajoutée ;
- confirmation qu’aucun fichier interdit n’a été modifié.

## PR_RULES_IF_APPLICABLE

Aucune PR dans cette tâche.

## BLOCK_CONDITIONS

- Branche courante différente de `main`.
- Working tree sale avant exécution.
- Besoin de modifier un fichier interdit.
- Besoin d’installer une dépendance.
- Besoin de changer l’architecture.
- Besoin de créer une capacité hors MIG-006.
- Tests absents ou impossibles à produire.

## NEXT_ACTION

Faire `git pull`, puis lancer Codex ou Claude localement avec : `Lis .codex/TASK.md et exécute strictement.`
