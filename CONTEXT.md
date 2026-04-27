# CONTEXT

## Projet

LEX_SYNDIC : système d'analyse juridique des accords d'entreprise français,
au service des représentants du personnel.

## Dépôts

| Dépôt | Chemin | Rôle |
|-------|--------|------|
| V2 | `C:\Users\Harib\CascadeProjects\lex_syndic_v2` | Dépôt **canonique** et gouverné. |
| V1 | `C:\Users\Harib\CascadeProjects\lex-syndic` | Code historique, instable. **Source de migration contrôlée uniquement.** |

## Décision structurante

V2 est canonique. V1 ne sera **pas** migré en bloc.
La migration se fait par lots numérotés `MIG-XXX`, chacun couvert par des tests
et validé indépendamment. Voir `MIGRATION_POLICY.md` et `DECISIONS.md` (DEC-001).

## Cadre architectural

L'architecture de référence est `docs/architecture/software_architecture_v2.md`.
Aucun module, aucune technologie, aucun service ne peut être ajouté en dehors de
ce document sans entrée correspondante dans `DECISIONS.md`.

## État opérationnel

- Architecture : documentée.
- Code métier : non migré.
- Tests : présents, non vérifiés dans l'environnement courant (`pytest` absent sur `python` 3.12 local).
- Packaging : déclaré via `pyproject.toml`, non validé en exécution dans l'environnement courant.

Détail dans `STATUS.md`.

## Hors périmètre actuel

- Backend applicatif.
- Frontend.
- Serveur MCP.
- Graphe de connaissances.
- Open WebUI.
- Connecteurs Légifrance / Judilibre.

Ces sujets pourront entrer dans le périmètre via une décision explicite
documentée dans `DECISIONS.md`.
