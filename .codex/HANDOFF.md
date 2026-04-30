# HANDOFF

Mission `LXS2-20260430-007` prete pour commit `Gouverneur / Architecte`.

Etat transmis:
- depot sur `main`
- `origin/main` et `main` alignes
- cadrage `MIG-010` prepare
- aucun fichier technique modifie

FUTURE_ROLE:
Migrator

FUTURE_FILES_ALLOWED:
- `src/lex_syndic/interface/**`
- `tests/test_interface*.py`
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
- `src/lex_syndic/storage/**`
- `src/lex_syndic/report/**`
- `pyproject.toml`
- `README.md`

FUTURE_INTERFACE_SCOPE:
- module local minimal ;
- aucune dependance externe ;
- aucune interface web ;
- aucune interface graphique ;
- aucun serveur API ;
- aucune IA ;
- aucun LLM ;
- aucun service externe ;
- pas d'ecriture disque ;
- pas de modification des modules existants ;
- couche Python simple permettant d'orchestrer des entrees structurees vers une sortie structuree ou textuelle ;
- pas de couplage fort au retrieval, storage ou report ;
- les fonctions doivent rester deterministes et testables.

FUTURE_MINIMAL_API_EXPECTED:
- `InterfaceRequest`
- `InterfaceResponse`
- `handle_request(request: InterfaceRequest) -> InterfaceResponse`

FUTURE_TESTS_EXPECTED:
- import du package `interface` ;
- creation d'une requete minimale ;
- generation d'une reponse minimale ;
- gestion entree vide ;
- statut de reponse deterministe ;
- message de reponse deterministe ;
- absence de dependance directe au retrieval ;
- absence de dependance directe au storage ;
- absence de dependance directe au report ;
- non-regression import package.

Prochaine action suggeree:
- lancer `MIG-010A` en mission `Migrator` uniquement pour l'implementation minimale de `interface`.
