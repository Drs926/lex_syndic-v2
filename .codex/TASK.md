# Task

TASK_ID:
LXS2-20260429-004A

TITLE:
MIG-007A — retrieval lexical minimal

ROLE:
Migrator

GOAL:
Implémenter un module minimal de retrieval lexical permettant de classer ou retourner des segments/documents selon une correspondance lexicale simple, déterministe et testée.

FILES_ALLOWED:
- `.codex/TASK.md`
- `.codex/STATUS.md`
- `.codex/RESULT.md`
- `.codex/PROOF.md`
- `.codex/HANDOFF.md`
- `src/lex_syndic/retrieval/**`
- `tests/test_retrieval*.py`

FILES_FORBIDDEN:
- `AGENTS.md`
- `MIGRATION_POLICY.md`
- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `OUTPUT_CONTRACT.md`
- `PROMPTS_INDEX.md`
- `docs/**`
- `src/lex_syndic/legal/**`
- `src/lex_syndic/analysis/**`
- `src/lex_syndic/ingestion/**`

REQUIRED_IMPLEMENTATION:
- Créer ou compléter un package `src/lex_syndic/retrieval/`.
- Fournir une API minimale, explicite et déterministe.
- Utiliser uniquement la bibliothèque standard Python sauf dépendance déjà présente et justifiée.
- Ne pas introduire de moteur vectoriel.
- Ne pas introduire d’IA, LLM, embedding, base externe ou index persistant.
- Le retrieval doit rester lexical, local, simple et testable.
- Les scores doivent être stables et explicables.
- Les tests doivent couvrir au minimum :
  - requête avec correspondance ;
  - requête sans correspondance ;
  - ordre de classement déterministe ;
  - gestion entrée vide ou quasi vide ;
  - non-régression import package.

REQUIRED_CHECKS:
- `python -m pytest tests/test_retrieval*.py tests/test_package_import.py -v -p no:cacheprovider`
- `git diff --cached --name-only`

COMMIT_MESSAGE:
`implement MIG-007A minimal lexical retrieval`

PUSH_POLICY:
Commit et push direct autorisés uniquement si :
- pytest PASS ;
- `git diff --cached --name-only` ne contient que FILES_ALLOWED ;
- aucun fichier FILES_FORBIDDEN modifié ;
- résultat documenté dans `.codex/RESULT.md`, `.codex/PROOF.md`, `.codex/HANDOFF.md`.
