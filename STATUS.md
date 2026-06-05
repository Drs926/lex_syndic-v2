# STATUS

Etat reel du depot V2 a date.

Derniere mise a jour : 2026-06-05.

## Resume

| Domaine | Etat reel |
|---------|-----------|
| Architecture | **Documentee** (`docs/architecture/software_architecture_v2.md`). |
| Code metier | **Partiellement migre et stabilise.** Les modules `legal`, `ingestion`, `analysis`, `comparison`, `rules`, `retrieval`, `storage`, `report`, `interface`, `pipeline` et `api` disposent d'un socle minimal documente ou teste. |
| Tests | **Operationnels selon les preuves de cycles.** Derniere preuve produit detaillee dans ce fichier : LEX-034 avec 186 tests globaux verts. |
| Packaging | **En place et verifie.** `pyproject.toml` existe, le backend editable est `setuptools.build_meta`. |
| Gouvernance | **En place.** Ce fichier est reconcilié avec l'etat ACT jusqu'a LEX-040. |
| Migration V1 | **MIG-001 a MIG-010 termines.** |
| Pipeline juridique | **Disponible.** `run_legal_pipeline()` est disponible dans `src/lex_syndic/pipeline/`. |
| API locale / FastAPI | **FastAPI locale mono-utilisateur cadree puis implementee dans le rail LEX-034.** Toute exposition publique reste hors perimetre sans decision separee. |

## Etat courant apres LEX-040

- `main` est aligne sur le merge produit LEX-040 : `2b43145`.
- LEX-040 correspond a la PR produit #60 : FastAPI local docs index.
- Le cockpit ACT a enregistre LEX-040 comme cycle merge avec PR #60 et merge commit `2b43145`.
- Lex-Syndic est pret pour un nouveau cycle controle.

## Derniers cycles suivis

| Cycle | Etat | Reference |
|-------|------|-----------|
| LEX-033 | Termine | Cadrage FastAPI, PR #53. |
| LEX-034 | Termine dans le rail ACT | API FastAPI locale mono-utilisateur. |
| LEX-037 | Termine dans le rail ACT | PR #57, merge `9acdcf1` selon cockpit ACT. |
| LEX-038 | Termine dans le rail ACT | PR #58, merge `c58f4af` selon cockpit ACT. |
| LEX-039 | Termine dans le rail ACT | PR #59, merge `49b86de` selon cockpit ACT. |
| LEX-040 | Termine dans le rail ACT | PR #60, merge `2b43145`, FastAPI local docs index. |
| LEX-041 | En cours | Reconciliation documentaire de `STATUS.md`, sans code produit. |

## Hors perimetre actuel

Aucun des elements suivants n'est autorise sans decision separee dans `DECISIONS.md` :

- exposition reseau publique ;
- usage multi-utilisateur ;
- base de donnees persistante ;
- frontend ;
- serveur MCP utilisateur ;
- graphe de connaissances ;
- Open WebUI ;
- connecteurs juridiques externes ;
- LLM, embeddings ou dependances IA.

## Prochaine action de reference

LEX-041 doit rester une reconciliation documentaire limitee. Aucun code produit, aucun test et aucune dependance ne doivent etre modifies dans ce cycle.
