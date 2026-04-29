# Task

TASK_ID: LXS2-20260429-004
MODE: CODE_ACTION
TARGET_REPO: Drs926/lex_syndic-v2
TARGET_BRANCH: main
BRANCH_KIND: main
LOCAL_PATH: C:\Users\Harib\CascadeProjects\lex_syndic_v2
STATUS: READY_FOR_AGENT
OWNER: codex

## OBJECTIVE

Implémenter `MIG-007` de manière minimale et testée : module `retrieval`, indexation lexicale interne et recherche sur corpus de test reproductible, sans moteur externe ni recherche sémantique.

## CONTEXT

`PLAN.md` définit `MIG-007` ainsi :

- module cible : `retrieval` ;
- contenu : indexation et recherche lexicale interne ;
- critère de sortie : recherche sur corpus de test reproductible ;
- état actuel : en attente.

`software_architecture_v2.md` définit `retrieval` comme le module de recherche documentaire : indexation, recherche lexicale, recherche sémantique, récupération de textes juridiques. Pour MIG-007, seule la recherche lexicale interne minimale est autorisée.

État prouvé avant tâche :

- `MIG-006` validé ;
- tests actuels : `52 passed` ;
- `src/lex_syndic/retrieval/__init__.py` est vide ;
- les modèles canoniques disponibles incluent `LegalDocument` et `Clause` ;
- aucune dépendance externe ne doit être ajoutée.

## PREFLIGHT_GATES

- Lire `AGENTS.md`.
- Lire `MIGRATION_POLICY.md`.
- Lire `PLAN.md`.
- Lire `docs/architecture/software_architecture_v2.md`.
- Confirmer la branche courante avec `git branch --show-current`.
- Confirmer le working tree avec `git status --short`.
- Faire `git pull` avant exécution.
- BLOCK si la branche courante n’est pas `main`.
- BLOCK si le working tree contient des changements hors scope avant exécution.

## SCOPE

- Implémenter une couche minimale dans `src/lex_syndic/retrieval/`.
- Ajouter une indexation lexicale déterministe en mémoire.
- Ajouter une recherche lexicale simple sur corpus fourni en mémoire.
- Utiliser uniquement les modèles canoniques existants si nécessaire, notamment `LegalDocument` et/ou `Clause`.
- Ajouter des tests dédiés sous `tests/`.
- Mettre à jour `DECISIONS.md` avec l’entrée MIG-007 obligatoire.
- Mettre à jour `STATUS.md`, `PLAN.md` et `PROMPTS_INDEX.md` pour refléter MIG-007 uniquement si la migration passe.
- Mettre à jour `.codex/STATUS.md`, `.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
- Exécuter `python -m pytest -q`.

## IMPLEMENTATION_BOUNDARIES

MIG-007 doit rester minimal :

- pas d’OpenSearch ;
- pas de base de données ;
- pas de stockage persistant ;
- pas d’embeddings ;
- pas de recherche sémantique ;
- pas de Légifrance ;
- pas de Judilibre ;
- pas de réseau ;
- pas de dépendance externe ;
- pas de modification des lots MIG-008 à MIG-010.

Exemples acceptables :

- normalisation lexicale simple ;
- index inversé en mémoire ;
- résultat de recherche déterministe avec score simple basé sur fréquence ou présence ;
- recherche sur `LegalDocument.text` ou `Clause.content` ;
- ordre stable des résultats.

## OUT_OF_SCOPE

- Ne pas modifier `docs/architecture/`.
- Ne pas modifier `MIGRATION_POLICY.md`.
- Ne pas modifier `AGENTS.md`.
- Ne pas introduire de technologie nouvelle.
- Ne pas créer `MIG-008` ou suivant.
- Ne pas créer de backend, frontend, MCP, graphe, Open WebUI, connecteur Légifrance ou Judilibre.
- Ne pas installer de dépendance.
- Ne pas créer de branche.
- Ne pas ouvrir de PR.
- Ne pas modifier le repo central `Drs926/agent-control-tower`.

## FILES_ALLOWED

- src/lex_syndic/retrieval/**
- tests/test_retrieval*.py
- tests/test_retrieval_*.py
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
- docs/architecture/software_architecture_v2.md
- src/lex_syndic/legal/models.py
- src/lex_syndic/retrieval/**
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
- src/lex_syndic/rules/**
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
- git diff -- src/lex_syndic/retrieval tests DECISIONS.md STATUS.md PLAN.md PROMPTS_INDEX.md .codex/STATUS.md .codex/RESULT.md .codex/PROOF.md .codex/HANDOFF.md
- type AGENTS.md
- type PLAN.md
- type STATUS.md
- type DECISIONS.md
- type MIGRATION_POLICY.md
- type OUTPUT_CONTRACT.md
- type PROMPTS_INDEX.md
- type pyproject.toml
- type docs\architecture\software_architecture_v2.md
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
- confirmation qu’aucune dépendance externe n’a été ajoutée ;
- confirmation qu’aucun fichier interdit n’a été modifié ;
- confirmation que la recherche est reproductible sur corpus de test.

## PR_RULES_IF_APPLICABLE

Aucune PR dans cette tâche.

## BLOCK_CONDITIONS

- Branche courante différente de `main`.
- Working tree sale avant exécution.
- Besoin de modifier un fichier interdit.
- Besoin d’installer une dépendance.
- Besoin de changer l’architecture.
- Besoin de créer une capacité hors MIG-007.
- Tests absents ou impossibles à produire.

## NEXT_ACTION

Faire `git pull`, puis lancer Codex ou Claude localement avec : `Lis .codex/TASK.md et exécute strictement.`
