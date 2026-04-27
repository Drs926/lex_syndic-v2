# DECISIONS

Journal des décisions structurantes du projet.

Format d'une entrée :

```
## DEC-XXX — Titre court
Date : YYYY-MM-DD
Statut : Proposée | Acceptée | Remplacée par DEC-YYY | Rejetée
Contexte : ...
Décision : ...
Conséquences : ...
```

---

## DEC-001 — V2 canonique, V1 source de migration contrôlée
Date : 2026-04-27
Statut : Acceptée
Contexte : Deux dépôts coexistent. V1 (`C:\Users\Harib\CascadeProjects\lex-syndic`)
contient du code utile mais instable. V2 (`C:\Users\Harib\CascadeProjects\lex_syndic_v2`)
porte une architecture documentée et propre.
Décision : V2 est le dépôt **canonique**. V1 ne sert que de **source de
migration contrôlée**. Aucun code V1 n'est intégré sans lot `MIG-XXX` validé.
Conséquences :
- Toute modification structurante se fait sur V2.
- V1 reste accessible en lecture seule pour référence et migration.
- La migration est encadrée par `MIGRATION_POLICY.md` et `PLAN.md`.

## DEC-002 — Architecture v2 figée comme cadre de migration
Date : 2026-04-27
Statut : Acceptée
Contexte : `docs/architecture/software_architecture_v2.md` définit modules,
modèles canoniques, dépendances autorisées et interdites.
Décision : Toute migration et toute évolution doivent rester dans le cadre de
ce document. Toute extension nécessite une nouvelle décision référencée ici.
Conséquences :
- Pas de backend, frontend, MCP, graphe, Open WebUI, Légifrance ou Judilibre
  introduits sans nouvelle décision.
- Les modules autorisés sont ceux listés à `software_architecture_v2.md` §3.

## DEC-003 — Sortie contractuelle des missions
Date : 2026-04-27
Statut : Acceptée
Contexte : Plusieurs agents interviendront successivement.
Décision : Chaque mission produit une sortie au format défini dans
`OUTPUT_CONTRACT.md`.
Conséquences :
- Les missions sont auditables et comparables.
- Une mission qui ne respecte pas le format est considérée comme non livrée.

## DEC-004 — MIG-002 stabilise un modèle juridique minimal et immuable
Date : 2026-04-27
Statut : Acceptée
Contexte : `Clause` canonique V2 est un prérequis explicite pour `MIG-003+`.
Le dépôt V2 ne doit pas importer le double pipeline V1, mais peut s'inspirer
de `models/legal_clause.py` et de la taxonomie de `models/canonical_clause.py`.
Décision : `src/lex_syndic/legal/models.py` définit en MIG-002 un socle minimal
et immuable comprenant `LegalDocument`, `Clause`, `LegalReference`, `Norm`,
`RuleCheckResult` et un `ComparisonResult` conservé comme placeholder typé. La
taxonomie de thèmes canonique est gelée sur les 10 valeurs de
`canonical_clause.py`.
Conséquences :
- Aucun pipeline n'est introduit en MIG-002.
- Aucun import runtime depuis V1 n'est autorisé.
- Les modèles doivent être instanciables et sérialisables par tests avant toute
  ouverture de `MIG-003`.

## DEC-005 — MIG-003 démarre par une ingestion texte pure et bornée
Date : 2026-04-27
Statut : Acceptée
Contexte : L'audit V1 mentionne `extract_text.py` pour MIG-003, mais cette
source introduit PDF/DOCX et des dépendances externes interdites dans cette
mission. `legal_segmenter.py` appartient en outre à MIG-004, pas à l'ingestion.
Décision : MIG-003 commence par une ingestion minimale limitée au texte brut et
aux fichiers `.txt`, avec normalisation simple des retours ligne et production
d'un unique `LegalDocument` sans segmentation juridique avancée.
Conséquences :
- Aucune dépendance externe n'est ajoutée dans MIG-003.
- Aucun PDF, DOCX ou pipeline de segmentation n'entre dans ce lot.
- `source_path` est conservé comme métadonnée légère sur l'instance du document
  sans modification du modèle canonique `LegalDocument`.

## DEC-006 — MIG-004 limite l'analyse à une segmentation structurelle minimale
Date : 2026-04-27
Statut : Acceptée
Contexte : `legal_segmenter.py` V1 montre une chaîne de segmentation plus large,
mais MIG-004 doit rester borné et ne pas dériver vers l'analyse juridique
complète ni vers les dépendances de lots ultérieurs.
Décision : MIG-004 segmente uniquement un `LegalDocument` en clauses candidates
par paragraphes séparés par lignes vides, avec un fallback par lignes non vides
si un seul bloc existe. Les clauses générées restent neutres : `topic="autre"`,
`compliance_status="unknown"` et aucune référence normative n'est ajoutée.
Conséquences :
- Aucun moteur d'analyse juridique n'est introduit.
- Aucun `AnalyzedClause` n'est ajouté dans ce lot.
- La sortie reste un `LegalDocument` enrichi de clauses candidates ordonnées.
