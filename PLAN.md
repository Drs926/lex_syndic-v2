# PLAN

Feuille de route opérationnelle de V2.

## Phase 0 — Stabilisation gouvernance (terminée)

- Fichiers racine renseignés : `README`, `CONTEXT`, `AGENTS`, `PLAN`, `SPEC`,
  `OUTPUT_CONTRACT`, `DECISIONS`, `MIGRATION_POLICY`, `STATUS`, `PROMPTS_INDEX`.
- Aucun code migré. Aucun test ajouté. Aucune dépendance ajoutée.

## Phase 1 — Outillage minimum (terminée)

- `pyproject.toml` créé : `lex-syndic` v2.0.0, Python ≥ 3.11, pytest ≥ 8.0.
- Backend d'installation editable corrigé : `setuptools.build_meta`.
- Pipeline de tests initialisé : `tests/conftest.py` + `tests/test_package_import.py`.
- Commande reproduite avec succès le 2026-04-27 :
  `python -m pytest tests/test_package_import.py -v -p no:cacheprovider`
  → `17 passed`.
- Audit V1→V2 produit : `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md`.

## Phase 2 — Migration contrôlée depuis V1

La migration depuis V1 se fait **par lots numérotés** `MIG-001` à `MIG-010`.
Chaque lot respecte `MIGRATION_POLICY.md` :

- périmètre limité à un module canonique de `software_architecture_v2.md` ;
- code repris **réécrit** ou **adapté** (pas de copie aveugle) ;
- tests obligatoires avant fusion ;
- pas d'introduction de technologie hors architecture ;
- entrée correspondante dans `DECISIONS.md`.

### Lots de migration

| Lot | Module cible | Contenu | Critère de sortie | État |
|-----|--------------|---------|-------------------|------|
| `MIG-001` | `core` | Packaging, pyproject.toml, pipeline de tests, squelettes importables. | `python -m pytest` passe. 17 tests verts. | **TERMINÉ** |
| `MIG-002` | `legal` | Modèles juridiques `LegalDocument`, `Clause`, `LegalReference`, `Norm`, `RuleCheckResult`. | Modèles instanciables, sérialisation testée. | **TERMINÉ** |
| `MIG-003` | `ingestion` | Lecture texte brut, chargement `.txt`, normalisation simple, sortie `LegalDocument`. | Ingestion texte testée sans dépendance externe ni segmentation avancée. | **TERMINÉ** |
| `MIG-004` | `analysis` | Segmentation minimale en clauses candidates, sans analyse juridique ni extraction. | Segmentation déterministe testée sur `LegalDocument` issu de MIG-003. | **TERMINÉ** |
| `MIG-005` | `comparison` | Comparaison minimale clause↔clause entre documents déjà segmentés, sans scoring ni jugement juridique. | Comparaison structurelle testée via `ComparisonResult` canonique et entrées ordonnées. | **TERMINÉ** |
| `MIG-006` | `rules` | Règles calculables, seuils, validation conformité. | Sortie `RuleCheckResult` testée. | **TERMINÉ** |
| `MIG-007` | `retrieval` | Indexation et recherche lexicale interne minimale. | Recherche sur corpus de test reproductible. | **TERMINÉ** |
| `MIG-008` | `storage` | Persistance fichier, métadonnées, résultats. | Round-trip lecture/écriture testé. | En attente |
| `MIG-009` | `report` | Synthèse Markdown et JSON. | Génération déterministe testée. | En attente |
| `MIG-010` | `interface` | Point d'entrée minimal (CLI). | Exécution pipeline complet sur exemple. | En attente |

### Ordre des lots

L'ordre est contraint par le graphe de dépendances de `software_architecture_v2.md` §7.
Référence détaillée : `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md` §9.

```
MIG-001 → MIG-002 → MIG-003 → MIG-004 → MIG-005 → MIG-006
                 ↘ MIG-007
                 ↘ MIG-008
MIG-005 + MIG-006 → MIG-009 → MIG-010
```

### Hors plan

Aucun lot ne couvre :
- backend applicatif,
- frontend,
- serveur MCP,
- graphe,
- Open WebUI,
- connecteurs Légifrance ou Judilibre.

Ces sujets exigeraient une décision explicite dans `DECISIONS.md`.

### Prochaine préparation

- Après `MIG-007`, la prochaine étape logique est le cadrage séparé de
  `MIG-008` (`storage`) sans implémentation dans cette mission.
