# MIGRATION_AUDIT_V1_TO_V2

Audit de récupération contrôlée : V1 → V2.

Date : 2026-04-27
Mode : lecture seule de V1. Aucun fichier V1 modifié. Aucun code copié dans V2.
Référence : `MIGRATION_POLICY.md`, `PLAN.md`, `SPEC.md`, `software_architecture_v2.md`.

---

## 1. Preuves d'intégrité

| Preuve | Résultat |
|--------|----------|
| V1 accessible en lecture | OUI — `C:\Users\Harib\CascadeProjects\lex-syndic` monté en lecture |
| V1 modifié pendant cet audit | NON — aucun outil Write/Edit appliqué sur V1 |
| V2 repository Git actif | OUI — `.git/` présent avec branche `main` |
| Code ajouté dans `src/` V2 | NON — seul `docs/audits/MIGRATION_AUDIT_V1_TO_V2.md` créé |
| Copie de code V1→V2 | NON — aucune copie directe exécutée |

---

## 2. État de V2 au moment de l'audit

| Module V2 | État |
|-----------|------|
| `core` | Squelette (`config.py`, `exceptions.py`, `types.py`) — sans logique |
| `legal` | Squelette (`models.py`) — sans logique |
| `ingestion` | `__init__.py` vide |
| `analysis` | `__init__.py` vide |
| `comparison` | `__init__.py` vide |
| `rules` | `__init__.py` vide |
| `retrieval` | `__init__.py` vide |
| `storage` | `__init__.py` vide |
| `report` | `__init__.py` vide |
| `interface` | `__init__.py` vide |
| `tests/` | Vide |
| `pyproject.toml` | Absent |

Lot en attente : `MIG-001` (module `core`). Aucun lot démarré.

---

## 3. État de V1 au moment de l'audit

V1 (`C:\Users\Harib\CascadeProjects\lex-syndic`) est un moteur déterministe complet :

- **2 pipelines actifs** : pipeline moderne (`interface/analysis_service.py`) et pipeline legacy (`reporting/pipeline_runner.py`).
- **37 tests unitaires** + 3 tests d'intégration.
- **2 dépendances externes runtime** : `pdfminer.six`, `python-docx`.
- **Dépendances non déclarées** dans `requirements.txt`.
- **6 fichiers JSON gold corpus** + 10 documents réels (PDF/DOCX) dans `data/`.

---

## 4. Classement des modules V1

### 4.1 MIGRABLE (adapté directement, sans nettoyage structurel majeur)

| Fichier V1 | Module V2 cible | Lot | Motif |
|------------|-----------------|-----|-------|
| `models/legal_clause.py` (`LegalClause`) | `legal` | MIG-002 | Dataclass frozen, immutable, aucune dépendance externe, correspond directement à `Clause` canonique V2 |
| `models/clause_decision_trace.py` (`ClauseDecisionTrace`) | `report` | MIG-009 | Frozen dataclass sans dépendance, correspond à `AuditEvent` V2 |
| `comparison/clause_semantics.py` (`ClauseSemanticView`, `build_clause_semantic_view`) | `analysis` | MIG-004 | Entièrement déterministe, pur Python/regex, aucune dépendance externe |
| `comparison/semantic_matcher.py` (`compare_semantic_views`) | `comparison` | MIG-005 | Pur Python, déterministe, produit `ComparisonResult`-compatible |
| `comparison/rights_impact_analyzer.py` (`analyze_rights_impact`) | `comparison` | MIG-005 | Pur Python, déterministe, règles explicites |
| `comparison/risk_detector.py` (`detect_risk`) | `comparison` | MIG-005 | Pur Python, déterministe, règles explicites |
| `comparison/clause_aligner.py` (`align_clauses`, `ClauseAlignment`) | `comparison` | MIG-005 | Jaccard + sémantique déterministe, pur Python |
| `comparison/agreement_impact_analyzer.py` (`analyze_agreement_impact`) | `comparison` | MIG-005 | Agrégation déterministe, pur Python |
| `extractor/normalize_text.py` (`normalize_text`) | `ingestion` | MIG-003 | Pur Python/regex, 5 règles explicites, aucune dépendance externe |

### 4.2 MIGRABLE APRÈS NETTOYAGE

| Fichier V1 | Module V2 cible | Lot | Motif du nettoyage |
|------------|-----------------|-----|--------------------|
| `extractor/extract_text.py` | `ingestion` | MIG-003 | Import V1 (`lex_syndic.extractor`) à réécrire → `lex_syndic.ingestion`. Sortie `str` à adapter vers `LegalDocument`. Dépendances `pdfminer.six` + `python-docx` à déclarer dans V2 `pyproject.toml`. |
| `models/canonical_clause.py` (`CanonicalClause`, `CanonicalClausePair`) | `legal` | MIG-002 | Taxonomie canonique et normaliseurs à conserver. Imports internes V1 à réécrire. `CanonicalClause` → `Clause` V2 ; `CanonicalClausePair` → `ComparisonResult` V2. |
| `models/analyzed_clause.py` (`AnalyzedClause`) | `analysis`/`comparison` | MIG-004/MIG-005 | Import de `CanonicalClausePair` à réécrire. Logique `from_clause_results` réutilisable, à adapter au modèle canonique V2 `AnalyzedClause`. |
| `segmentation/legal_segmenter.py` | `analysis` | MIG-004 | Import V1 (`LegalClause`) à remplacer par `Clause` V2. Orchestration des sous-modules à conserver. |
| `segmentation/document_classifier.py` | `analysis` | MIG-004 | Imports internes à réécrire. Logique de classification par blocs réutilisable. |
| `segmentation/structure_detector.py` | `analysis` | MIG-004 | Imports internes à réécrire. Logique regex réutilisable. |
| `segmentation/article_splitter.py` | `analysis` | MIG-004 | Imports internes à réécrire. Logique réutilisable. |
| `segmentation/clause_splitter.py` | `analysis` | MIG-004 | Imports internes à réécrire. Logique réutilisable. |
| `segmentation/normalizer.py` | `analysis` | MIG-004 | Imports internes à réécrire. Logique réutilisable. |
| `segmentation/patterns.py` | `analysis` | MIG-004 | Patterns regex réutilisables directement après renommage du package. |
| `comparison/clause_normalizer.py` | `analysis` | MIG-004 | Imports internes à réécrire. Normalisation de texte réutilisable. |
| `comparison/clause_topic_classifier.py` | `analysis` | MIG-004 | Imports internes à réécrire. Taxonomie à aligner sur `CanonicalTopic` V2. |
| `legal_rules/legal_rules_engine.py` | `rules` | MIG-006 | Import `AnalyzedClause` V1 à réécrire. Moteur de règles déterministe réutilisable. Les 3 règles actuelles sont minimales ; V2 devra enrichir le catalogue sans changer le pattern. |
| `analysis/norm_hierarchy.py` | `rules` | MIG-006 | Logique de vérification normative réutilisable. Fonctionne actuellement avec `legal_refs = {}` dans le pipeline V1 — la mécanique est bonne, le référentiel est vide. À enrichir en V2 avec vraies normes. |
| `argumentation/legal_argument_generator.py` | `report` | MIG-009 | Imports internes à réécrire. Logique d'arguments/priorités/alertes déterministe et réutilisable. |
| `report/report_generator.py` | `report` | MIG-009 | Imports internes à réécrire. Modèles `ReportDocument`, `CriticalClause`, `ModifiedClause` à adapter aux canoniques V2. |
| `report/legal_case_report.py` (`LegalCaseReport`, `build_legal_case_report`) | `report` | MIG-009 | Imports internes à réécrire. Agrégation finale — correspond à `CaseFile` + `GeneratedMemo` V2. Nettoyage des références aux contrats de sortie legacy. |
| `report/legal_case_exporter.py` | `report` | MIG-009 | Imports internes à réécrire. Exports JSON + Markdown réutilisables. |
| `interface/analysis_service.py` | `interface` | MIG-010 | Orchestration principale réutilisable comme base du point d'entrée V2. Tous les imports internes V1 à réécrire vers V2. Sortie à adapter au contrat V2 (`OUTPUT_CONTRACT.md`). |
| `cli/main.py` | `interface` | MIG-010 | Structure CLI `argparse` réutilisable. Pipeline interne à réécrire vers V2. |

### 4.3 À ARCHIVER SEULEMENT (conserver comme référence historique, ne pas migrer)

| Fichier V1 | Motif |
|------------|-------|
| `reporting/pipeline_runner.py` | Pipeline legacy doublon. Superseded par `interface/analysis_service.py`. |
| `reporting/final_report.py` | Rapport Markdown legacy dépendant de `syndical_analysis`. Superseded par `legal_case_exporter.py`. |
| `reporting/analysis_trace.py` | Trace JSON legacy. Superseded par `ClauseDecisionTrace` + `legal_case_exporter`. |
| `reporting/case_builder.py` | Dossier legacy. Superseded par `LegalCaseReport`. |
| `syndical/syndical_analysis.py` | Analyse de changements legacy. Superseded par pipeline sémantique moderne. |
| `syndical/change_detector.py` | Détection legacy. Superseded par `semantic_matcher.py`. |
| `syndical/review_generator.py` | Génération legacy. Superseded par `legal_argument_generator.py`. |
| `models/legal_structure.py` | Modèle intermédiaire legacy. Superseded par `LegalClause` + pipeline moderne. |
| `comparison/comparator.py` | Comparateur legacy. Superseded par chaîne sémantique moderne. |
| `interface/analysis_contract.py` | Contrat JSON verrouillé app (Tkinter). Hors périmètre V2. |

### 4.4 À REJETER (ne pas migrer, ne pas archiver dans src/)

| Fichier V1 | Motif |
|------------|-------|
| `interface/analysis_app.py` | UI Tkinter. Hors périmètre V2 (pas de frontend/backend). |
| `classification/__init__.py` | Package vide, aucune logique. |
| `comparison/clause_matcher.py` | Non branché en runtime V1. Superseded par `clause_aligner.py`. |

---

## 5. Tests réutilisables

### 5.1 Récupérables directement (MIGRABLE)

| Test V1 | Lot V2 cible | Motif |
|---------|-------------|-------|
| `unit/test_extractor.py` | MIG-003 | Teste `extract_text` — logique réutilisable après adaptation des imports |
| `unit/test_normalize_text.py` | MIG-003 | Teste `normalize_text` — pur Python, directement réutilisable |
| `unit/test_legal_clause.py` | MIG-002 | Teste `LegalClause` — dataclass, directement réutilisable |
| `unit/test_segmentation.py` | MIG-004 | Teste `segment_document` — réutilisable après adaptation imports |
| `unit/test_document_classifier.py` | MIG-004 | Réutilisable après adaptation imports |
| `unit/test_clause_semantics.py` | MIG-004 | Teste `build_clause_semantic_view` — directement réutilisable |
| `unit/test_semantic_matcher.py` | MIG-005 | Réutilisable après adaptation imports |
| `unit/test_rights_impact.py` | MIG-005 | Réutilisable après adaptation imports |
| `unit/test_risk_detector.py` | MIG-005 | Réutilisable après adaptation imports |
| `unit/test_clause_alignment.py` | MIG-005 | Réutilisable après adaptation imports |
| `unit/test_comparison.py` | MIG-005 | Réutilisable après adaptation imports |
| `unit/test_agreement_impact_analyzer.py` | MIG-005 | Réutilisable après adaptation imports |
| `unit/test_legal_rules_engine.py` | MIG-006 | Réutilisable après adaptation imports |
| `unit/test_legal_rules_analyzed_clause_integration.py` | MIG-006 | Réutilisable après adaptation imports |
| `unit/test_canonical_clause.py` | MIG-002 | Réutilisable après adaptation imports |
| `unit/test_analyzed_clause.py` | MIG-004/MIG-005 | Réutilisable après adaptation imports |
| `unit/test_clause_decision_trace.py` | MIG-009 | Directement réutilisable |
| `unit/test_report_generator.py` | MIG-009 | Réutilisable après adaptation imports |
| `unit/test_legal_case_report.py` | MIG-009 | Réutilisable après adaptation imports |
| `unit/test_legal_case_exporter.py` | MIG-009 | Réutilisable après adaptation imports |
| `unit/test_legal_argument_generator.py` | MIG-009 | Réutilisable après adaptation imports |
| `unit/test_report_analyzed_clause_integration.py` | MIG-009 | Réutilisable après adaptation imports |
| `unit/test_argument_analyzed_clause_integration.py` | MIG-009 | Réutilisable après adaptation imports |
| `unit/test_analyzed_clause_from_canonical_pair.py` | MIG-002/MIG-005 | Réutilisable après adaptation imports |
| `unit/test_analyzed_clause_orchestrator.py` | MIG-004/MIG-005 | Réutilisable après adaptation imports |
| `unit/test_clause_topic_classifier.py` | MIG-004 | Réutilisable après adaptation imports |
| `unit/test_analysis_service.py` | MIG-010 | Réutilisable après réécriture complète des imports |
| `integration/test_real_evaluation.py` | MIG-010 | Fixtures réels utiles — à adapter au pipeline V2 |
| `integration/test_segmentation_audit.py` | MIG-004 | Audit de segmentation — jeux de données réels utiles |

### 5.2 À archiver seulement (legacy, ne pas migrer)

| Test V1 | Motif |
|---------|-------|
| `unit/test_norm_hierarchy.py` | Legacy pipeline |
| `unit/test_legal_structure.py` | Modèle legacy |
| `unit/test_case_builder.py` | Legacy pipeline |
| `unit/test_analysis_trace.py` | Legacy trace |
| `unit/test_final_report.py` | Rapport legacy |
| `unit/test_syndical_analysis.py` | Module legacy |
| `unit/test_analysis_contract.py` | Contrat verrouillé app, hors périmètre |
| `integration/test_pipeline_runner.py` | Pipeline legacy |

---

## 6. Données récupérables

| Répertoire V1 | Contenu | Usage V2 | Lot |
|---------------|---------|----------|-----|
| `data/agreements/` | 5 fichiers (4 PDF + 1 DOCX) — accords télétravel, égalité pro | Jeux de données tests ingestion + segmentation | MIG-003, MIG-004 |
| `data/projects/` | 5 fichiers (4 PDF + 1 DOCX) — projets associés | Jeux de données tests comparaison | MIG-005 |
| `data/gold_corpus/` | 6 fichiers JSON — cas de segmentation annotés | Corpus de référence pour tests déterministes | MIG-004 |

Condition d'utilisation : les données doivent être **explicitement référencées** dans le lot concerné (cf. `MIGRATION_POLICY.md` §Cas limites).

---

## 7. Dépendances à introduire dans V2

| Dépendance | Version minimale | Module V2 | Lot | Justification |
|------------|-----------------|-----------|-----|---------------|
| `pdfminer.six` | ≥ 20221105 | `ingestion` | MIG-003 | Extraction PDF (`extract_text.py`) |
| `python-docx` | ≥ 1.1 | `ingestion` | MIG-003 | Extraction DOCX (`extract_text.py`) |
| `pytest` | ≥ 8.0 | dev | MIG-001 | Tests unitaires obligatoires |

**Ces dépendances devront être déclarées dans `pyproject.toml` V2** (inexistant à ce jour) et documentées dans `DECISIONS.md` lors du lot concerné.

Aucune autre dépendance externe n'est requise par les modules MIGRABLE ou MIGRABLE APRÈS NETTOYAGE. Toute la logique métier de V1 est en Python standard + `re` + `dataclasses`.

---

## 8. Risques d'importation

| Risque | Sévérité | Module V1 concerné | Mesure |
|--------|----------|-------------------|--------|
| **Conflit de nommage de package** : V1 `extractor` → V2 `ingestion` ; V1 `legal_rules` → V2 `rules` ; V1 `report` + `reporting` → V2 `report` | ÉLEVÉ | Tous | Aucun import direct de V1. Chaque module réécrit avec les nouveaux chemins V2. |
| **Modèle `LegalClause` V1 ≠ `Clause` V2** : les champs ne correspondent pas 1:1 | ÉLEVÉ | `legal`, `analysis`, `comparison` | Définir `Clause` canonique V2 en MIG-002 avant toute migration de segmentation. |
| **Double pipeline V1** : `reporting/pipeline_runner.py` et `interface/analysis_service.py` ont des sorties divergentes | MOYEN | `interface` | Ne migrer que `interface/analysis_service.py`. Le pipeline legacy ne doit pas entrer dans V2. |
| **Taxonomie de topics duale** : `analysis_contract.py` et `canonical_clause.py` ont des ensembles différents | MOYEN | `legal`, `analysis` | Adopter la taxonomie de `canonical_clause.py` (10 topics) comme référence V2 dès MIG-002. |
| **`AnalyzedClause` importe `CanonicalClausePair`** : dépendance interne entre deux modèles | MOYEN | MIG-002/MIG-004 | MIG-002 doit définir les deux modèles avant MIG-004. |
| **`classification/__init__.py` vide** : peut polluer si importé | FAIBLE | `analysis` | Ne pas migrer. Package rejeté. |
| **`norm_hierarchy.py` opère avec `legal_refs = {}`** : conformité normative sans données réelles | FAIBLE | `rules` | Migrer le mécanisme, pas le référentiel. Enrichir les références en MIG-006. |
| **Dépendances runtime non déclarées dans V1** : `pdfminer.six`, `python-docx` absentes de `requirements.txt` | FAIBLE | `ingestion` | Déclarer explicitement dans `pyproject.toml` V2 lors de MIG-003. |

---

## 9. Ordre exact de migration par lots

L'ordre respecte le graphe de dépendances de `software_architecture_v2.md` §7 et les contraintes identifiées ci-dessus.

```
MIG-001 : core
  ├── Source V1 : aucune (créer ex-nihilo)
  ├── Contenu V2 : config, exceptions, types communs, logging
  └── Prérequis : aucun

MIG-002 : legal
  ├── Sources V1 : models/legal_clause.py, models/canonical_clause.py, models/clause_decision_trace.py
  ├── Contenu V2 : LegalDocument, Clause, LegalReference, Norm, CanonicalTopic, ClauseDecisionTrace
  └── Prérequis : MIG-001

MIG-003 : ingestion
  ├── Sources V1 : extractor/extract_text.py, extractor/normalize_text.py
  ├── Contenu V2 : lecture PDF/DOCX, normalisation, sortie LegalDocument
  ├── Dépendances nouvelles : pdfminer.six, python-docx → pyproject.toml
  └── Prérequis : MIG-001, MIG-002

MIG-004 : analysis
  ├── Sources V1 : segmentation/* (6 fichiers), comparison/clause_semantics.py,
  │              comparison/clause_normalizer.py, comparison/clause_topic_classifier.py,
  │              models/analyzed_clause.py
  ├── Contenu V2 : segmentation, classification thématique, extraction sémantique, AnalyzedClause
  ├── Données V1 : data/gold_corpus/* (6 JSON), data/agreements/* (fixtures tests)
  └── Prérequis : MIG-001, MIG-002, MIG-003

MIG-005 : comparison
  ├── Sources V1 : comparison/clause_aligner.py, comparison/semantic_matcher.py,
  │              comparison/rights_impact_analyzer.py, comparison/risk_detector.py,
  │              comparison/agreement_impact_analyzer.py
  ├── Contenu V2 : alignement, comparaison sémantique, scoring, ComparisonResult
  ├── Données V1 : data/agreements/* + data/projects/* (paires de documents réels)
  └── Prérequis : MIG-001, MIG-002, MIG-004

MIG-006 : rules
  ├── Sources V1 : legal_rules/legal_rules_engine.py, analysis/norm_hierarchy.py (mécanisme seul)
  ├── Contenu V2 : moteur de règles déterministes, seuils, RuleCheckResult
  └── Prérequis : MIG-001, MIG-002, MIG-005

MIG-007 : retrieval
  ├── Source V1 : aucune (créer ex-nihilo)
  ├── Contenu V2 : indexation lexicale, recherche sur corpus
  └── Prérequis : MIG-001, MIG-002

MIG-008 : storage
  ├── Source V1 : aucune (créer ex-nihilo)
  ├── Contenu V2 : persistance fichier, métadonnées, résultats
  └── Prérequis : MIG-001, MIG-002

MIG-009 : report
  ├── Sources V1 : report/report_generator.py, report/legal_case_report.py,
  │              report/legal_case_exporter.py, argumentation/legal_argument_generator.py,
  │              models/clause_decision_trace.py (déjà en MIG-002)
  ├── Contenu V2 : CaseFile, GeneratedMemo, exports JSON + Markdown
  └── Prérequis : MIG-001, MIG-002, MIG-005, MIG-006

MIG-010 : interface
  ├── Sources V1 : interface/analysis_service.py (base), cli/main.py (structure CLI)
  ├── Contenu V2 : point d'entrée CLI, orchestration pipeline complet
  └── Prérequis : MIG-001 à MIG-009
```

**Lots sans source V1 directe : MIG-001, MIG-007, MIG-008.**
Ces lots doivent être créés ex-nihilo en respectant l'architecture V2.

---

## 10. Bloquants identifiés

| Bloquant | Impact | Lot bloqué | Action requise |
|---------|--------|-----------|----------------|
| **`pyproject.toml` absent dans V2** | Packaging et dépendances impossibles | MIG-001 | Créer `pyproject.toml` V2 en phase MIG-001 |
| **`tests/` vide dans V2** | Aucun lot ne peut être fusionné sans tests | MIG-001 | Initialiser le pipeline pytest en MIG-001 |
| **`Clause` canonique V2 non définie** | Tous les modules en aval bloqués | MIG-002 | Définir `Clause` avant MIG-003+ |
| **Taxonomie de topics non figée** | Divergence entre modules | MIG-002 | Adopter la taxonomie `canonical_clause.py` V1 comme référence et geler dans MIG-002 |
| **Absence de données de test dans V2** | Tests d'ingestion et de segmentation impossibles | MIG-003/MIG-004 | Référencer explicitement les données V1 dans les lots concernés (cf. `MIGRATION_POLICY.md`) |

---

## 11. Synthèse de classement

| Catégorie | Nombre de fichiers | Modules V2 couverts |
|-----------|-------------------|---------------------|
| MIGRABLE | 9 | `legal`, `analysis`, `comparison`, `report` |
| MIGRABLE APRÈS NETTOYAGE | 20 | `ingestion`, `legal`, `analysis`, `comparison`, `rules`, `report`, `interface` |
| À ARCHIVER SEULEMENT | 10 | (legacy pipeline + UI + contrats obsolètes) |
| À REJETER | 3 | (UI Tkinter, packages vides, doublons non branchés) |
| **Total** | **42** | |

---

## 12. Prochaine action recommandée

Ouvrir le lot `MIG-001` en respectant `MIGRATION_POLICY.md` :

1. Créer `pyproject.toml` V2 (Python ≥ 3.11, dépendances dev `pytest`).
2. Initialiser `tests/conftest.py` vide.
3. Implémenter `core/config.py`, `core/exceptions.py`, `core/types.py` (logique fondatrice, aucune source V1 directe).
4. Ajouter les tests unitaires correspondants.
5. Documenter la décision dans `DECISIONS.md`.
6. Mettre à jour `STATUS.md`.

---

*Audit produit en lecture seule. Aucun fichier V1 modifié. Aucun code copié dans V2 `src/`.*
