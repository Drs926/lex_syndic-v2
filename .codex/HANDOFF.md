# HANDOFF

Mission `LXS2-20260430-006` prete pour commit `Gouverneur / Architecte`.

Etat transmis:
- depot sur `main`
- `origin/main` et `main` alignes
- cadrage `MIG-009` prepare
- aucun fichier technique modifie

FUTURE_ROLE:
Migrator

FUTURE_FILES_ALLOWED:
- `src/lex_syndic/report/**`
- `tests/test_report*.py`
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
- `pyproject.toml`
- `README.md`

FUTURE_REPORT_SCOPE:
- module local minimal ;
- aucune dependance externe ;
- aucune IA ;
- aucun LLM ;
- aucun export PDF/DOCX/HTML ;
- aucune generation graphique ;
- aucune persistance disque ;
- sortie Python simple, deterministe et testable ;
- rapport base sur des donnees deja structurees ;
- pas de couplage direct au retrieval ni au storage ;
- pas de modification des modeles juridiques existants.

FUTURE_MINIMAL_API_EXPECTED:
- `ReportSection`
- `Report`
- `build_report(title: str, sections: list[ReportSection]) -> Report`
- `render_text(report: Report) -> str`

FUTURE_TESTS_EXPECTED:
- import du package `report` ;
- creation d'un rapport vide ou minimal ;
- ajout de sections ;
- rendu texte deterministe ;
- ordre stable des sections ;
- gestion titre vide ou sections vides ;
- absence de dependance au retrieval ;
- absence de dependance au storage ;
- non-regression import package.

Prochaine action suggeree:
- lancer `MIG-009A` en mission `Migrator` uniquement pour l'implementation minimale de `report`.
