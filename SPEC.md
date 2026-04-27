# SPEC

Spécification fonctionnelle synthétique de LEX_SYNDIC_V2.

Référence d'architecture : `docs/architecture/software_architecture_v2.md`.
Cette spécification ne crée pas de fonctionnalité nouvelle. Elle décrit ce que
le système **doit pouvoir** atteindre, dans le périmètre de l'architecture v2.

## Utilisateurs cibles

Représentants du personnel et conseils techniques agissant en droit du
travail français. Le système assiste l'analyse, il ne la remplace pas.

## Objets canoniques

Conformément à `software_architecture_v2.md` §6, les objets juridiques ont
**une seule représentation canonique** :

- `LegalDocument`
- `DocumentVersion`
- `Clause`
- `LegalReference`
- `MetadataTag`
- `AnalyzedClause`
- `ComparisonResult`
- `RuleCheckResult`
- `CaseFile`
- `GeneratedMemo`
- `AuditEvent`

Toute représentation parallèle est interdite.

## Pipeline de référence

Document → ingestion → structuration légale → analyse de clauses → recherche
documentaire → comparaison → règles calculables → rapport → synthèse LLM.

Le LLM intervient **uniquement en fin de pipeline** (`software_architecture_v2.md` §2.5).

## Exigences fonctionnelles

| ID | Exigence | Module |
|----|----------|--------|
| F1 | Charger un accord d'entreprise au format texte ou bureautique. | ingestion |
| F2 | Produire un `LegalDocument` structuré et versionné. | ingestion + legal |
| F3 | Segmenter le document en `Clause`. | analysis |
| F4 | Extraire les `LegalReference` citées. | analysis |
| F5 | Comparer deux clauses ou une clause à une norme. | comparison |
| F6 | Appliquer des règles calculables et produire un `RuleCheckResult`. | rules |
| F7 | Indexer et rechercher dans un corpus interne. | retrieval |
| F8 | Persister documents, métadonnées et résultats. | storage |
| F9 | Générer un dossier juridique (`CaseFile`, `GeneratedMemo`). | report |
| F10 | Exposer un point d'entrée pour exécuter le pipeline. | interface |

## Exigences non fonctionnelles

| ID | Exigence |
|----|----------|
| N1 | Traçabilité juridique : toute conclusion référence une clause, une norme ou une règle (`software_architecture_v2.md` §2.3). |
| N2 | Déterminisme : le pipeline est reproductible hors étape LLM. |
| N3 | Modularité stricte : aucune dépendance interdite (`software_architecture_v2.md` §8). |
| N4 | Auditabilité : toute exécution produit des `AuditEvent`. |
| N5 | Aucune introduction de dépendance hors architecture sans `DECISIONS.md`. |

## Hors périmètre

Hors périmètre actuel, comme indiqué dans `CONTEXT.md` : backend, frontend,
MCP, graphe, Open WebUI, Légifrance, Judilibre.

## Critères d'acceptation par lot

Chaque lot `MIG-XXX` (voir `PLAN.md`) doit satisfaire :

1. Les exigences fonctionnelles assignées au module concerné.
2. Les exigences non fonctionnelles N1 à N5.
3. Une couverture de tests prouvant le comportement minimal du module.
