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

## DEC-022 — LEX-023 PASS : format_legal_report() disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : `LegalAnalysisResponse` était lisible par le code mais pas par
l'utilisateur. Un formateur était nécessaire pour transformer la réponse
structurée en texte compréhensible.
Décision : LEX-023 a créé `src/lex_syndic/report/legal_formatter.py` avec
`format_legal_report(response: LegalAnalysisResponse) -> str`. Le rapport
contient titre, statut, niveau d'alerte, justification, action recommandée,
compteurs de clauses et de comparaisons. Le couplage `report → interface`
(import de `LegalAnalysisResponse`) est accepté comme formatage de surface
sans logique métier. 132 tests globaux verts. Aucune dépendance externe.
Conséquences :
- `format_legal_report()` est la fonction de sortie lisible de référence.
- Toute extension vers un format plus riche (PDF, HTML, Markdown structuré)
  exige un nouveau cadrage dans `DECISIONS.md`.
- Le couplage `report → interface` est acceptable tant que le rapport reste
  un formateur pur sans logique métier.

## DEC-023 — LEX-024 est cadré comme exposition du rapport via l'interface
Date : 2026-06-01
Statut : Acceptée
Contexte : `analyze_legal_text()` retourne une `LegalAnalysisResponse` et
`format_legal_report()` la transforme en texte lisible, mais ces deux
fonctions ne sont pas encore chaînées dans un flux applicatif unique. Un
utilisateur doit appeler les deux séparément.
Décision : LEX-024 ajoutera une fonction dans `src/lex_syndic/interface/`
qui enchaîne `analyze_legal_text()` et `format_legal_report()`, retournant
à la fois la `LegalAnalysisResponse` structurée et le rapport texte en un
seul appel. Aucun stockage, aucun frontend, aucune API web, aucun PDF, aucun
LLM, aucune dépendance externe.
Conséquences :
- LEX-024 est borné à `src/lex_syndic/interface/` et `tests/test_interface*.py`.
- Le flux complet `texte + citations → réponse structurée + rapport lisible`
  devient l'entrée applicative de référence.
- Toute extension vers une API web ou un frontend exige un nouveau cadrage.

## DEC-024 — LEX-024 PASS : analyze_legal_text_with_report() disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : `analyze_legal_text()` et `format_legal_report()` existaient
séparément mais n'étaient pas chaînées. Un utilisateur devait effectuer deux
appels distincts pour obtenir à la fois la réponse structurée et le rapport
lisible.
Décision : LEX-024 a créé `src/lex_syndic/interface/report_handler.py` avec
`analyze_legal_text_with_report(request) -> LegalAnalysisWithReportResponse`.
La dataclass `LegalAnalysisWithReportResponse` expose `analysis` et
`report_text`. 137 tests globaux verts. Aucun stockage, aucun frontend,
aucune API web, aucun PDF, aucun LLM, aucune dépendance externe.
Conséquences :
- `analyze_legal_text_with_report()` est l'entrée applicative de référence
  pour un flux complet analyse + rapport.
- Le flux `texte + citations → LegalAnalysisWithReportResponse` est stabilisé.
- Toute extension vers une API web, un frontend ou un stockage exige un
  nouveau cadrage dans `DECISIONS.md`.

## DEC-025 — LEX-025 est cadré comme test d'acceptation du flux complet avec rapport
Date : 2026-06-01
Statut : Acceptée
Contexte : `analyze_legal_text_with_report()` est disponible mais le flux
complet analyse + rapport n'a pas encore été éprouvé sur un scénario
utilisateur réaliste de bout en bout.
Décision : LEX-025 créera un test d'acceptation dans `tests/test_acceptance*.py`
couvrant le flux complet depuis un accord d'entreprise réaliste avec citations
variées : vérification de `LegalAnalysisWithReportResponse`, cohérence de
`LegalAnalysisResponse`, présence du titre dans le rapport texte, cas
insufficient_data. Aucune modification de `src/`. Aucun mock, aucun storage,
aucun LLM.
Conséquences :
- LEX-025 est borné à `tests/` uniquement.
- Aucune modification de `src/` n'est autorisée dans LEX-025 sans bug
  bloquant prouvé.
- Le PASS de LEX-025 clôt la phase de validation du flux applicatif complet.

## DEC-026 — LEX-025 PASS : test d'acceptation flux complet avec rapport disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-025 devait créer un test d'acceptation end-to-end pour valider
le flux complet `LegalAnalysisRequest → analyze_legal_text_with_report() →
LegalAnalysisWithReportResponse` sur un accord d'entreprise réaliste avec
citations variées.
Décision : LEX-025 a créé `tests/test_acceptance_full_flow.py` avec 4 scénarios
end-to-end verts. 141 tests globaux verts. Merge commit
`f8ca88f9d18a2ad43c67a9e489e2b80898c6c228` sur main. Aucune modification `src/`.
Conséquences :
- Le cœur applicatif `texte + citations → analyse + rapport` est validé
  de bout en bout sans mock, sans storage, sans LLM.
- Toute extension (stockage, API web, frontend) exige un nouveau cadrage.

## DEC-027 — LEX-026 est cadré comme stockage mémoire minimal des résultats d'analyse
Date : 2026-06-01
Statut : Acceptée
Contexte : Le flux produit une `LegalAnalysisWithReportResponse` exploitable
mais il n'existe pas encore de frontière minimale pour conserver un résultat
d'analyse pendant une session applicative.
Décision : LEX-026 créera `InMemoryLegalResultStore` dans
`src/lex_syndic/storage/legal_results.py`. Interface : `save(result) -> record_id`,
`get(record_id) -> result | None`, `list_ids() -> tuple[str, ...]`, `clear() -> None`.
Contraintes : aucune écriture disque, aucune sérialisation JSON, aucune base
de données, aucune dépendance externe. `record_id` monotone simple. Aucune
modification de l'interface applicative ni de `legal/models.py`.
Conséquences :
- Le store est un utilitaire de session uniquement — il ne persiste pas entre
  les processus.
- Toute persistance disque ou base de données exige un nouveau cadrage.
- L'interface applicative (`analyze_legal_text_with_report`) n'est pas modifiée.

## DEC-028 — LEX-026 PASS : InMemoryLegalResultStore disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-026 devait créer un stockage mémoire minimal pour conserver
temporairement les résultats d'analyse `LegalAnalysisWithReportResponse` pendant
une session applicative.
Décision : LEX-026 a créé `src/lex_syndic/storage/legal_results.py` avec
`InMemoryLegalResultStore` (API : `save`, `get`, `list_ids`, `clear`). Record_id
monotone déterministe. 148 tests globaux verts. Merge commit
`6516a4afa2377d71978136ad5d63fef4459f71ac` sur main. Aucune écriture disque,
aucune dépendance externe.
Conséquences :
- Le store est un utilitaire de session uniquement — il ne persiste pas entre
  les processus.
- Toute persistance disque ou base de données exige un nouveau cadrage.

## DEC-029 — LEX-027 est cadré comme flux session stockant le résultat complet
Date : 2026-06-01
Statut : Acceptée
Contexte : `InMemoryLegalResultStore` est disponible mais il n'existe pas encore
de point d'entrée applicatif combinant analyse + stockage en un seul appel.
Décision : LEX-027 créera `src/lex_syndic/interface/session_handler.py` avec
`LegalSessionResult` (record_id + result) et `analyze_and_store_legal_text(
request, store) -> LegalSessionResult`. Le store est injecté par l'appelant —
aucun store global. Aucune écriture disque, aucune API web, aucun frontend,
aucune dépendance externe. Aucune modification de `InMemoryLegalResultStore`,
`LegalAnalysisRequest` ou `LegalAnalysisWithReportResponse`.
Conséquences :
- Le flux session `request → analyse → stockage → record_id` est disponible
  via un point d'entrée unique sans effet de bord global.
- Toute extension vers une API web ou un frontend exige un nouveau cadrage.

## DEC-030 — LEX-027 PASS : flux session analyze_and_store_legal_text() disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-027 devait créer un flux session combinant analyse et stockage
en un seul appel, avec store injecté par l'appelant sans store global.
Décision : LEX-027 a créé `src/lex_syndic/interface/session_handler.py` avec
`analyze_and_store_legal_text(request, store) -> LegalSessionResult`.
`LegalSessionResult` expose `record_id` + `result`. 154 tests globaux verts.
Merge commit `060ed76770ce11cf556007f467398f5bf2e0e27a` sur main. Aucun store
global, aucune écriture disque, aucune dépendance externe.
Conséquences :
- Le flux session `request → analyse → stockage → record_id` est disponible
  via un point d'entrée unique sans effet de bord global.
- Toute extension vers une API web ou un frontend exige un nouveau cadrage.

## DEC-031 — LEX-028 est cadré comme test d'acceptation du flux session complet
Date : 2026-06-01
Statut : Acceptée
Contexte : `analyze_and_store_legal_text()` est disponible mais le flux session
complet n'a pas encore été éprouvé sur un scénario utilisateur réaliste de bout
en bout avec vérification du store.
Décision : LEX-028 créera `tests/test_acceptance_session_flow.py` couvrant :
store séparé par test, accord réaliste avec citations variées, vérification
`record_id` + `store.get()` + `report_text` + `decision_status`, cas
`insufficient_data`, isolation entre stores. Aucune modification de `src/`.
Conséquences :
- LEX-028 est borné à `tests/` uniquement.
- Aucune modification de `src/` n'est autorisée dans LEX-028 sans bug bloquant.
- Le PASS de LEX-028 clôt la phase de validation du flux session complet.

## DEC-032 — LEX-028 PASS : test d'acceptation session complet disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-028 devait créer un test d'acceptation end-to-end pour valider
le flux session complet sur un accord réaliste avec vérification du store,
du rapport et de l'isolation entre stores.
Décision : LEX-028 a créé `tests/test_acceptance_session_flow.py` avec 6 scénarios
end-to-end verts. Merge commit `302e0041790ddeb83362744c534fdadf6b2413c4` sur main.
160 tests globaux verts. Aucune modification `src/`.
Conséquences :
- Le flux session `request → analyse → stockage → record_id` est validé
  de bout en bout sans mock, sans disque, sans LLM.
- Toute exposition externe (API, frontend) exige un audit préalable.

## DEC-033 — LEX-029 : audit maturité obligatoire avant exposition externe
Date : 2026-06-01
Statut : Acceptée
Contexte : Le flux session est validé mais aucune API, frontend ni persistance
disque n'est encore décidé. Avant toute exposition externe, un audit structuré
est nécessaire pour identifier les blocages et les prérequis.
Décision : LEX-029 produit `docs/audits/LEX_029_PRODUCT_MATURITY_AUDIT.md`
évaluant les contrats publics, les risques de couplage, les limites métier
et les conditions d'exposition API. Aucune modification de `src/` ni `tests/`.
Conséquences :
- Toute API, frontend ou persistance disque exige une décision explicite dans
  `DECISIONS.md` référençant les blocages identifiés dans LEX-029.
- L'exposition API mono-utilisateur locale est la prochaine option recommandée,
  sous réserve d'un cadrage explicite.
- L'exposition API publique ou multi-utilisateur est BLOQUÉE sans auth, UUID
  et thread-safety.

## DEC-034 — LEX-029 PASS : audit maturité produit disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-029 devait produire un audit maturité avant toute exposition
externe pour identifier les blocages et prérequis.
Décision : LEX-029 a produit `docs/audits/LEX_029_PRODUCT_MATURITY_AUDIT.md`.
Verdict : API locale mono-utilisateur acceptable avec cadrage. API publique/
multi-utilisateur BLOQUÉE sans auth, UUID et thread-safety. Merge commit
`2f824a65ce4a967154df1d3f97a499d3fb66a528` sur main. Aucune modification
`src/` ni `tests/`.
Conséquences :
- Toute API publique exige auth, UUID, thread-safety — hors périmètre actuel.
- API locale mono-utilisateur possible sous réserve de cadrage explicite.

## DEC-035 — LEX-030 : couche API locale mono-utilisateur pure Python
Date : 2026-06-01
Statut : Acceptée
Contexte : L'audit LEX-029 valide une API locale mono-utilisateur. FastAPI
n'est pas dans les dépendances projet (pyproject.toml). Aucune dépendance
externe ne doit être ajoutée.
Décision : LEX-030 créera `src/lex_syndic/api/local.py` avec
`LocalApiAnalysisRequest`, `LocalApiAnalysisResponse` et
`submit_analysis(request, store) -> LocalApiAnalysisResponse`.
Implémentation pure Python sans serveur web, sans endpoint HTTP, sans
dépendance externe. Store injecté par l'appelant. Réponse API aplatie
(record_id + decision_status + alert_level + report_text + recommended_action).
Limites acceptées explicitement : mono-utilisateur, pas d'auth, pas de
thread-safety, pas de persistance, pas d'UUID.
Conséquences :
- Aucun serveur HTTP n'est lancé — la couche API est un adaptateur local.
- Toute API web réelle (FastAPI, Flask, etc.) exige un cadrage séparé.
- Le module `api` devient le point d'entrée canonique pour les intégrations
  futures une fois les prérequis (auth, UUID, thread-safety) satisfaits.

## DEC-036 — LEX-030 PASS : couche API locale pure Python disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-030 devait créer une couche API locale mono-utilisateur pure
Python sans serveur HTTP, sans FastAPI et sans dépendance externe.
Décision : LEX-030 a créé `src/lex_syndic/api/local.py` avec
`submit_analysis(request, store) -> LocalApiAnalysisResponse`. Réponse API
aplatie exposant record_id, decision_status, alert_level, report_text,
recommended_action. FastAPI absent de pyproject.toml — aucune dépendance ajoutée.
167 tests globaux verts. Merge commit `d2f4a7b0bfad3ac5d9fca237c79a8a188e037e9d`
sur main. Aucun store global, aucune écriture disque.
Conséquences :
- `submit_analysis()` est le point d'entrée API canonique local.
- Toute API web réelle exige un cadrage séparé avec auth, UUID, thread-safety.

## DEC-037 — LEX-031 est cadré comme test d'acceptation de l'API locale
Date : 2026-06-01
Statut : Acceptée
Contexte : `submit_analysis()` est disponible mais le flux API local complet
n'a pas encore été éprouvé sur un scénario utilisateur réaliste de bout en bout.
Décision : LEX-031 créera `tests/test_acceptance_api_local.py` couvrant :
accord réaliste avec citations variées, vérification record_id, store.get(),
report_text, decision_status, insufficient_data, isolation stores, absence
d'import FastAPI/HTTP. Aucune modification de `src/`.
Conséquences :
- LEX-031 est borné à `tests/` uniquement.
- Le PASS de LEX-031 clôt la phase de validation de l'API locale.

## DEC-038 — LEX-031 PASS : test d'acceptation API locale disponible
Date : 2026-06-01
Statut : Acceptée
Contexte : LEX-031 devait créer un test d'acceptation end-to-end pour valider
l'API locale pure Python sur un scénario utilisateur réaliste.
Décision : LEX-031 a créé `tests/test_acceptance_api_local.py` avec 7 scénarios
end-to-end verts. 174 tests globaux verts. Merge commit
`15e154f54dec59d0a47d94ca308bc2ebc13d5d27` sur main. Aucune modification `src/`.
Aucune dépendance HTTP/FastAPI.
Conséquences :
- L'API locale `submit_analysis()` est validée de bout en bout.
- Le couplage `storage → interface` reste le prochain blocage avant API web réelle.

## DEC-039 — LEX-032 : casser le couplage storage → interface
Date : 2026-06-01
Statut : Acceptée
Contexte : L'audit LEX-029 a identifié que `storage.legal_results` importe
`LegalAnalysisWithReportResponse` depuis `interface.report_handler`. Si une
future mission ajoute un import de `storage` dans `interface/legal_handler.py`
ou `interface/report_handler.py`, un cycle se formerait.
Décision : LEX-032 rend `InMemoryLegalResultStore` générique via `Generic[T]`
(Python typing). Le store ne connaît plus aucun type de `interface`. Les callers
(`session_handler`, `api/local`) gardent leur comportement. Aucun changement
fonctionnel, aucune modification du format `record_id`, aucune modification
de l'API publique `save/get/list_ids/clear`.
Conséquences :
- `storage` devient indépendant de `interface` — le risque de cycle est éliminé.
- Les tests prouvent l'absence d'import `lex_syndic.interface` dans `storage`.
- Toute API web réelle reste différée à un cadrage séparé.
