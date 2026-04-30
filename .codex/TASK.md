# Task

TASK_ID:
LXS2-20260430-005A

TITLE:
MIG-008A — minimal storage implementation

ROLE:
Migrator

GOAL:
Implémenter un module `storage` minimal, local, déterministe et sans dépendance externe, capable de stocker et restituer les objets nécessaires au pipeline actuel sous forme simple et testable.

FILES_ALLOWED:
- `.codex/TASK.md`
- `.codex/STATUS.md`
- `.codex/RESULT.md`
- `.codex/PROOF.md`
- `.codex/HANDOFF.md`
- `src/lex_syndic/storage/**`
- `tests/test_storage*.py`

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
- `src/lex_syndic/retrieval/**`
- `pyproject.toml`
- `README.md`

REQUIRED_IMPLEMENTATION:
- Créer le package `src/lex_syndic/storage/`.
- Fournir une API minimale et explicite.
- Utiliser uniquement la bibliothèque standard Python.
- Implémenter un storage local en mémoire par défaut.
- Autoriser l’ajout d’éléments simples identifiés.
- Autoriser la récupération déterministe.
- Préserver l’ordre d’insertion ou un ordre explicitement stable.
- Gérer le cas vide.
- Gérer les identifiants inconnus sans exception inutile.
- Ne pas persister sur disque dans cette mission sauf si le cadrage existant l’exige explicitement.
- Ne pas coupler le storage au retrieval.
- Ne pas modifier les modèles juridiques existants.

API ATTENDUE:
- `InMemoryStore`
- `add(key: str, value: object) -> None`
- `get(key: str) -> object | None`
- `list_keys() -> list[str]`
- `list_values() -> list[object]`
- `clear() -> None`
