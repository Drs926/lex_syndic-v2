# AGENTS

Règles d'opération pour tout agent (humain ou LLM) intervenant sur V2.

## Principes

1. V2 est canonique. V1 n'est jamais copié en bloc.
2. Toute action doit être justifiée par un fichier de gouvernance
   (`PLAN.md`, `DECISIONS.md`, `MIGRATION_POLICY.md`, `SPEC.md`).
3. Toute sortie doit respecter `OUTPUT_CONTRACT.md`.
4. Aucune promesse non prouvée. Pas de capacité annoncée sans code testé.

## Périmètre autorisé par défaut

- Lecture libre de tout le dépôt.
- Écriture sur les fichiers de gouvernance racine listés ci-dessous.
- Écriture sur `docs/`.

## Périmètre interdit par défaut

- Modification de `src/` hors lot de migration `MIG-XXX` validé.
- Modification de `tests/` hors lot de migration `MIG-XXX` validé.
- Intégration de code V1 sans lot `MIG-XXX`.
- Ajout de technologie absente de `docs/architecture/software_architecture_v2.md`
  sans décision dans `DECISIONS.md`.
- Création de backend, frontend, MCP, graphe, Open WebUI, connecteurs
  Légifrance ou Judilibre sans décision préalable.

## Fichiers de gouvernance racine modifiables

- `README.md`
- `CONTEXT.md`
- `AGENTS.md`
- `PLAN.md`
- `SPEC.md`
- `OUTPUT_CONTRACT.md`
- `DECISIONS.md`
- `MIGRATION_POLICY.md`
- `STATUS.md`
- `PROMPTS_INDEX.md`

## Cycle d'une mission

1. Identifier la mission dans `PROMPTS_INDEX.md`.
2. Lire les fichiers de gouvernance pertinents.
3. Planifier les changements.
4. Exécuter les changements en respectant le périmètre.
5. Produire la sortie au format `OUTPUT_CONTRACT.md`.
6. Mettre à jour `STATUS.md` et `PROMPTS_INDEX.md` si l'état réel a changé.

## Rôles d'agents

| Rôle | Responsabilité | Écrit sur |
|------|----------------|-----------|
| Architecte | Maintient l'architecture et les décisions. | `docs/architecture/`, `DECISIONS.md` |
| Auditeur | Mesure l'état réel du dépôt. | `docs/audits/`, `STATUS.md` |
| Migrator | Exécute un lot `MIG-XXX`. | `src/`, `tests/` (uniquement dans le périmètre du lot) |
| Gouverneur | Maintient les fichiers de gouvernance racine. | Fichiers racine listés ci-dessus. |

Aucun agent ne combine les rôles Migrator et Gouverneur dans la même action.
