# LEX_SYNDIC_V2

Dépôt **canonique** du projet LEX_SYNDIC.

## Position du dépôt

- **V2 (ici)** : dépôt de référence. Toute évolution se fait depuis V2.
- **V1** : `C:\Users\Harib\CascadeProjects\lex-syndic`. Source de migration **contrôlée** uniquement. Aucun code V1 n'est intégré sans lot de migration validé.

## Périmètre

Analyse juridique des accords d'entreprise (droit du travail français) :
ingestion documentaire, structuration, analyse de clauses, comparaison juridique,
règles calculables, génération de dossiers exploitables.

Le système assiste l'analyse juridique, il ne la remplace pas.

## État réel

Voir `STATUS.md`. À ce jour : architecture documentée, code métier
partiellement migré jusqu'à `MIG-005`, socle de tests vérifié localement le
2026-04-29 via `python -m pytest -q` (`47 passed in 0.17s`), packaging déclaré
dans `pyproject.toml` et validation d'exécution prouvée dans l'environnement
courant.

## Documents de gouvernance

- `PLAN.md` — feuille de route et lots de migration `MIG-001` à `MIG-010`.
- `SPEC.md` — spécification fonctionnelle synthétique.
- `OUTPUT_CONTRACT.md` — format de sortie attendu des agents.
- `DECISIONS.md` — journal des décisions architecturales.
- `MIGRATION_POLICY.md` — règles de migration depuis V1.
- `AGENTS.md` — règles d'opération pour les agents.
- `CONTEXT.md` — contexte projet.
- `STATUS.md` — état réel courant du dépôt.
- `PROMPTS_INDEX.md` — index des missions exécutées.
- `docs/architecture/software_architecture_v2.md` — architecture de référence.

## Règles non négociables

1. V2 est canonique. V1 n'est jamais copié en bloc.
2. Pas de promesse non prouvée. Toute capacité doit être reliée à du code testé.
3. Toute migration depuis V1 passe par un lot `MIG-XXX` avec tests.
4. Pas d'introduction de technologie nouvelle hors `software_architecture_v2.md`.
