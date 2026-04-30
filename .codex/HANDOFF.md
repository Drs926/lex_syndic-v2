# HANDOFF

Mission `LXS2-20260430-005` prete pour commit de cadrage.

Etat transmis:
- depot sur `main`
- `origin/main` et `main` alignes
- aucun code `storage` implemente
- cadrage `MIG-008` prepare pour la future mission technique

FUTURE_ROLE:
Migrator

FUTURE_FILES_ALLOWED:
- `src/lex_syndic/storage/**`
- `tests/test_storage*.py`
- `.codex/TASK.md`
- `.codex/STATUS.md`
- `.codex/RESULT.md`
- `.codex/PROOF.md`
- `.codex/HANDOFF.md`

FUTURE_FILES_FORBIDDEN:
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
- `src/lex_syndic/retrieval/**`

FUTURE_STORAGE_SCOPE:
- stockage local minimal en mémoire ou fichier simple uniquement si déjà justifié par le projet ;
- API déterministe ;
- aucun service externe ;
- aucune base vectorielle ;
- aucune IA ;
- aucune dépendance nouvelle ;
- aucun mécanisme complexe de migration ;
- sérialisation simple et testable des objets nécessaires au pipeline actuel.

FUTURE_TESTS_EXPECTED:
- création d’un store minimal ;
- ajout d’un document ou segment ;
- récupération déterministe ;
- cas vide ;
- stabilité d’ordre ;
- non-régression import package.

Prochaine action suggeree:
- lancer `MIG-008A` en role `Migrator` uniquement pour une implementation storage minimale conforme a ce cadrage.
