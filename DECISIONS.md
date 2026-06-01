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

## DEC-007 — MIG-005 limite la comparaison à un diff structurel par position
Date : 2026-04-27
Statut : Acceptée
Contexte : Le modèle canonique MIG-002 expose déjà `ComparisonResult`, mais ne
porte pas encore de collection dédiée pour un diff complet de document. MIG-005
doit néanmoins stabiliser une comparaison minimale sans modifier
`legal/models.py` ni introduire d'analyse juridique.
Décision : MIG-005 compare deux `LegalDocument` déjà segmentés par ordre
d'apparition des clauses. La comparaison repose sur une normalisation textuelle
stricte et produit un `ComparisonResult` canonique enrichi d'entrées runtime
ordonnées, chacune de type `unchanged`, `rephrased`, `added` ou `removed`.
Conséquences :
- Aucun scoring, aucune similarité sémantique et aucune règle juridique ne sont
  introduits.
- Le contrat runtime `document.clauses` issu de MIG-004 est consommé sans
  modifier `LegalDocument`.
- Une modélisation canonique plus riche des diffs documentaires reste reportée
  à un lot ultérieur si nécessaire.

## DEC-008 — MIG-006 limite les règles à un contrôle déterministe minimal
Date : 2026-04-29
Statut : Acceptée
Contexte : `RuleCheckResult` existe déjà depuis MIG-002, mais le module
`rules` ne contient encore aucune logique métier. MIG-006 doit fournir une
première couche calculable sans dériver vers l'analyse juridique avancée ni
introduire de dépendance externe.
Décision : MIG-006 évalue une clause avec une seule règle déterministe
prioritaire. Si `compliance_status` est déjà renseigné, il est converti tel
quel en `RuleCheckResult`. Sinon, une clause vide devient `non_conforme`, une
clause à signal textuel trop faible devient `risque`, et une clause avec
contenu exploitable minimal devient `conforme`. L'évaluation documentaire
consomme uniquement le contrat runtime `document.clauses`.
Conséquences :
- Le module `rules` reste borné à des heuristiques structurelles minimales.
- Aucun raisonnement juridique, scoring avancé, NLP ou source externe n'est
  introduit.
- Les sorties sont testées via `RuleCheckResult` avant l'ouverture de
  `MIG-007`.

## DEC-009 — MIG-007 se découpe en validation technique puis gouvernance
Date : 2026-04-30
Statut : Acceptée
Contexte : La première formulation de `MIG-007` mélangeait modifications
`Migrator` (`src/`, `tests/`) et mises à jour de gouvernance racine, en
contradiction avec `AGENTS.md`.
Décision : `MIG-007` est séparé entre `MIG-007A` (rôle `Migrator`, validation
technique du retrieval lexical minimal) et `MIG-007B` (rôle `Gouverneur`,
mise à jour de la gouvernance après preuve PASS). Les missions mixtes
`Migrator` + `Gouverneur` restent interdites et la validation technique
précède toute mise à jour de gouvernance.
Conséquences :
- Les futures missions doivent conserver un rôle unique.
- Les preuves PASS du lot technique deviennent le prérequis de la mission de
  gouvernance correspondante.

## DEC-010 — MIG-008 commence par un cadrage storage sans code
Date : 2026-04-30
Statut : Acceptée
Contexte : `storage` reste vide et l'architecture autorise plusieurs options
techniques possibles. Choisir une persistance avant d'avoir borne le périmètre
creerait un risque d'implementation prematuree.
Décision : La premiere mission `MIG-008` est documentaire et de gouvernance
uniquement. Elle definit le perimetre exact du futur module `storage`, les
invariants, les fichiers autorises/interdits, les tests attendus et les
criteres PASS/BLOCK avant toute ligne de code. Aucune persistance technique
n'est choisie sans ce perimetre valide.
Conséquences :
- `MIG-008A` devra rester une mission `Migrator` separee.
- Aucun backend de persistance n'est implicitement autorise par cette decision.

## DEC-011 — MIG-008 reste borne a un storage memoire minimal
Date : 2026-04-30
Statut : Acceptée
Contexte : `MIG-008` a ete separe entre cadrage, implementation technique et
mise a jour de gouvernance. `MIG-008A` prouve qu'un storage minimal suffit au
pipeline courant sans persistance complexe.
Décision : `MIG-008` est formellement decoupe entre `MIG-008` (cadrage),
`MIG-008A` (implementation `Migrator`) et `MIG-008B` (gouvernance). Le
storage reste volontairement en memoire a ce stade. Aucune persistance disque,
base externe, vector DB, IA, LLM ou embedding n'est introduit. Les missions
mixtes `Migrator` + `Gouverneur` restent interdites.
Conséquences :
- Toute evolution de `storage` au-dela de la memoire devra faire l'objet d'un
  nouveau cadrage explicite.
- La gouvernance ne peut etre mise a jour qu'apres preuve PASS de la mission
  technique correspondante.

## DEC-012 — MIG-009 commence par un cadrage report sans code
Date : 2026-04-30
Statut : Acceptée
Contexte : Le module `report` reste a definir et plusieurs formes de sortie
seraient possibles. Choisir un format ou un moteur de rendu avant d'avoir borne
le besoin creerait un risque de surimplementation.
Décision : La premiere mission `MIG-009` est documentaire et de gouvernance
uniquement. Elle definit le perimetre exact du futur module `report`, ses
entrees, sa sortie minimale, ses invariants, ses fichiers autorises/interdits,
ses tests attendus et ses criteres PASS/BLOCK avant toute ligne de code. Aucun
format de sortie complexe n'est choisi a ce stade ; le rapport minimal doit
d'abord rester une structure deterministe et testable, pas un rendu final.
Conséquences :
- Une future `MIG-009A` devra rester une mission `Migrator` separee.
- Aucun rendu PDF, DOCX, HTML ni moteur de template n'est implicitement
  autorise par cette decision.

## DEC-013 — MIG-009 reste borne a un report texte minimal
Date : 2026-04-30
Statut : Acceptée
Contexte : `MIG-009` a ete separe entre cadrage, implementation technique et
mise a jour de gouvernance. `MIG-009A` prouve qu'un module `report` minimal
suffit au pipeline courant sans rendu complexe ni dependance externe.
Décision : `MIG-009` est formellement decoupe entre `MIG-009` (cadrage),
`MIG-009A` (implementation `Migrator`) et `MIG-009B` (gouvernance). Le module
`report` reste volontairement minimal. Le rendu actuel est texte, local,
deterministe et testable. Aucun export PDF, DOCX, HTML, template engine, IA,
LLM, embedding ou service externe n'est introduit. Les missions mixtes
`Migrator` + `Gouverneur` restent interdites.
Conséquences :
- Toute evolution de `report` vers un format de sortie plus riche devra faire
  l'objet d'un cadrage explicite.
- La gouvernance ne peut etre mise a jour qu'apres preuve PASS de la mission
  technique correspondante.

## DEC-014 — MIG-010 commence par un cadrage interface sans code
Date : 2026-04-30
Statut : Acceptée
Contexte : Le module `interface` reste a definir et plusieurs options
d'interface sont possibles. Choisir une interface web, graphique ou un serveur
API avant d'avoir borne le perimetre creerait un risque de surimplementation.
Décision : La premiere mission `MIG-010` est documentaire et de gouvernance
uniquement. Elle definit le perimetre exact du futur module `interface`, le
type d'interface minimal, ses entrees, ses sorties, ses invariants, ses
fichiers autorises/interdits, ses tests attendus et ses criteres PASS/BLOCK
avant toute ligne de code. Aucune interface web, graphique ou serveur API
n'est choisie a ce stade ; l'interface minimale doit d'abord rester une couche
Python deterministe et testable.
Conséquences :
- Une future `MIG-010A` devra rester une mission `Migrator` separee.
- Aucune dependance CLI ou framework d'interface n'est implicitement autorise
  par cette decision.

## DEC-015 — MIG-010 reste borne a une interface Python minimale
Date : 2026-04-30
Statut : Acceptée
Contexte : `MIG-010` a ete separe entre cadrage, implementation technique et
mise a jour de gouvernance. `MIG-010A` prouve qu'un module `interface` minimal
suffit au pipeline courant sans interface riche ni dependance externe.
Décision : `MIG-010` est formellement decoupe entre `MIG-010` (cadrage),
`MIG-010A` (implementation `Migrator`) et `MIG-010B` (gouvernance). Le module
`interface` reste volontairement minimal. L'interface actuelle est une couche
Python locale, deterministe et testable. Aucune interface web, graphique,
serveur API, dependance CLI externe, IA, LLM, embedding ou service externe
n'est introduit. Les missions mixtes `Migrator` + `Gouverneur` restent
interdites.
Conséquences :
- Toute evolution de `interface` vers une interface plus riche devra faire
  l'objet d'un cadrage explicite.
- La gouvernance ne peut etre mise a jour qu'apres preuve PASS de la mission
  technique correspondante.

## DEC-016 — Le dépôt V2 peut servir de support contrôlé de validation du rail
Date : 2026-05-01
Statut : Acceptée
Contexte : Une séquence dédiée doit valider le rail ChatGPT → GitHub → Codex
sans faire dériver le produit `lex_syndic_v2` hors de son périmètre minimal.
Décision : Le dépôt `lex_syndic_v2` peut être utilisé comme dépôt support pour
des missions de validation de rail, à condition que ces missions restent
bornées à un diff minimal de gouvernance si aucun besoin produit n'est prouvé.
Toute mission future de rail doit distinguer explicitement l'objectif rail,
l'objectif produit, la preuve attendue, l'état GitHub, le retour Codex et le
verdict ChatGPT.
Conséquences :
- Une mission de rail ne vaut pas ouverture implicite d'un nouveau lot produit.
- L'absence de test produit est acceptable si la mission reste documentaire et
  le justifie explicitement.

## DEC-017 — LEX-020 crée un pipeline juridique minimal reliant analysis, comparison et rules
Date : 2026-06-01
Statut : Acceptée
Contexte : Les modules `analysis`, `comparison` et `rules` sont stables et
testés depuis MIG-004 à MIG-006 / LEX-017 à LEX-019. Aucun glue code
n'existait pour les chaîner de façon déterministe. La preuve de valeur
juridique exige une orchestration bout-en-bout avant toute persistance ou
interface riche.
Décision : LEX-020 crée `src/lex_syndic/pipeline/` avec `run_legal_pipeline()`
retournant un `PipelineResult` immuable (document_id, analyzed_clauses,
comparisons, decision). Le pipeline construit automatiquement le contexte de
comparaison depuis les références extraites par l'analyse, permettant un usage
naturel par citation sans exposition des identifiants internes. Aucune
dépendance externe, aucun couplage à `storage`, `report` ou `interface`.
Conséquences :
- Le pipeline est la seule entrée autorisée pour orchestrer les trois briques.
- Toute extension du pipeline (persistance, rapport, interface) exige un
  cadrage explicite dans `DECISIONS.md` avant implémentation.
- `storage`, `report` et `interface` restent hors périmètre du pipeline à ce
  stade.

## DEC-018 — LEX-021 expose le pipeline juridique via la couche interface
Date : 2026-06-01
Statut : Acceptée
Contexte : `run_legal_pipeline()` est disponible depuis LEX-020 mais ne
dispose d'aucune entrée applicative. L'appelant doit construire lui-même
`LegalDocument` et `expected_references`. Cette friction empêche la preuve
d'un flux utilisateur réel.
Décision : LEX-021 ajoute `analyze_legal_text()` dans
`src/lex_syndic/interface/legal_handler.py`. Cette fonction accepte
`LegalAnalysisRequest(text, expected_citations, title, rule_id)`, construit
le document et les références, appelle `run_legal_pipeline()`, et retourne
`LegalAnalysisResponse(document_id, decision_status, alert_level,
justification, comparison_count, analyzed_clause_count, recommended_action)`.
`analyze_legal_text()` devient l'entrée applicative minimale du système.
Aucun frontend, aucun storage, aucun report, aucun MCP, aucune dépendance
externe ne sont introduits.
Conséquences :
- Tout appel applicatif au pipeline doit passer par `analyze_legal_text()` ou
  une couche équivalente décidée explicitement.
- Toute extension vers un frontend, une API web, un stockage ou un rapport
  exige un cadrage dans `DECISIONS.md` avant implémentation.
- Le flux `texte + citations → LegalAnalysisResponse` est la surface
  applicative de référence pour les prochains tests de comportement.

## DEC-019 — LEX-022 est cadré comme scénario d'acceptation end-to-end
Date : 2026-06-01
Statut : Acceptée
Contexte : Le flux applicatif `texte + citations → LegalAnalysisResponse` est
disponible mais n'a pas encore été éprouvé sur un scénario utilisateur réel
complet. Avant d'ouvrir storage, report ou NLP, il faut prouver que le
comportement observable est correct et stable de bout en bout.
Décision : LEX-022 créera un test d'acceptation end-to-end couvrant le flux
complet depuis un texte juridique réaliste (accord d'entreprise minimal) avec
des citations attendues variées, sans mock, sans storage, sans LLM. Ce test
prouve le comportement utilisateur réel avant toute extension du système.
Aucune nouvelle brique fonctionnelle n'est créée dans LEX-022 : seul le test
d'acceptation est produit.
Conséquences :
- LEX-022 reste borné à `tests/` uniquement.
- Aucune modification de `src/` n'est autorisée dans LEX-022 sans bug
  bloquant prouvé.
- Le PASS de LEX-022 conditionne toute décision d'extension ultérieure
  (storage, report, NLP, frontend).

## DEC-020 — LEX-022 PASS : le flux utilisateur observable est validé
Date : 2026-06-01
Statut : Acceptée
Contexte : `analyze_legal_text()` était disponible depuis LEX-021 mais aucun
scénario utilisateur réaliste n'avait été exécuté de bout en bout.
Décision : LEX-022 a créé `tests/test_acceptance_legal_pipeline.py` avec un
accord d'entreprise réaliste (4 articles, référencements L.1222-9 et
L.3121-1). Les 4 scénarios d'acceptation sont verts : citations présentes,
citation absente → non_compliant, aucune citation → insufficient_data, shape
stable. 127 tests globaux verts. Aucune modification de `src/`. Aucun mock,
aucun storage, aucun LLM. Le flux `texte + citations → LegalAnalysisResponse`
est désormais prouvé observable et stable.
Conséquences :
- Le flux applicatif est la référence de comportement pour toute extension.
- L'extension vers un rapport lisible (LEX-023) est autorisée dans le périmètre
  défini par DEC-021.
- Toute autre extension (storage, NLP, frontend) exige un nouveau cadrage
  avant implémentation.

## DEC-021 — LEX-023 est cadré comme rapport minimal de preuve juridique
Date : 2026-06-01
Statut : Acceptée
Contexte : La `LegalAnalysisResponse` produite par `analyze_legal_text()` est
structurée mais non lisible directement par un utilisateur. Les champs
`decision_status`, `alert_level`, `justification` et `recommended_action`
contiennent les données nécessaires à une restitution compréhensible.
Décision : LEX-023 ajoutera une fonction `format_legal_report()` dans le
module `report` existant, acceptant `LegalAnalysisResponse` et retournant une
chaîne de texte courte, lisible et déterministe. Le rapport est structuré
(titre, statut, niveau d'alerte, justification, action recommandée, compteurs)
sans mise en page riche. Aucun PDF, aucune UI, aucun stockage, aucun LLM, aucun
template engine externe.
Conséquences :
- LEX-023 est borné à `src/lex_syndic/report/` et `tests/test_report*.py`.
- Aucune modification de `legal/models.py`, `pipeline/`, `interface/` n'est
  autorisée dans LEX-023 sans bug bloquant prouvé.
- Le rapport reste du texte brut déterministe et testable.
