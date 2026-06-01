# LEX-029 — Audit maturité produit avant exposition externe

Date : 2026-06-01
Auteur : LEX-029 mission audit
Base : HEAD `302e0041790ddeb83362744c534fdadf6b2413c4`
Tests : 160 passed

---

## 1. Flux utilisateur réel actuel

```
LegalAnalysisRequest(text, expected_citations)
    → analyze_and_store_legal_text(request, store)
    → LegalSessionResult
        .record_id          # identifiant monotone, ex. "result-0001"
        .result             # LegalAnalysisWithReportResponse
            .analysis       # LegalAnalysisResponse
                .document_id
                .decision_status    # "compliant" | "non_compliant" |
                                    # "attention_required" | "insufficient_data"
                .alert_level
                .justification
                .comparison_count
                .analyzed_clause_count
                .recommended_action
            .report_text    # rapport texte déterministe (Markdown-like)
```

Le flux secondaire sans stockage :

```
analyze_legal_text_with_report(request) → LegalAnalysisWithReportResponse
analyze_legal_text(request)             → LegalAnalysisResponse
```

---

## 2. Contrats publics exposés

### 2.1 Points d'entrée stables

| Symbole | Module | Statut |
|---------|--------|--------|
| `LegalAnalysisRequest` | `interface` | Stable — frozen dataclass |
| `LegalAnalysisResponse` | `interface` | Stable — frozen dataclass |
| `LegalAnalysisWithReportResponse` | `interface` | Stable — frozen dataclass |
| `LegalSessionResult` | `interface` | Stable — frozen dataclass |
| `analyze_legal_text()` | `interface` | Stable |
| `analyze_legal_text_with_report()` | `interface` | Stable |
| `analyze_and_store_legal_text()` | `interface` | Stable |
| `InMemoryLegalResultStore` | `storage` | Stable |

### 2.2 Champs `LegalAnalysisRequest`

| Champ | Type | Défaut | Remarque |
|-------|------|--------|----------|
| `text` | `str` | — | Obligatoire |
| `expected_citations` | `tuple[str, ...]` | `()` | Chaînes libres, pas de format imposé |
| `title` | `str` | `"document"` | Utilisé comme document_id de base |
| `rule_id` | `str` | `"RULE_CLAUSE_NORM_MINIMAL"` | Règle unique actuellement |

---

## 3. Risques d'import et de couplage

### 3.1 Couplages actifs

| Dépendance | Direction | Risque |
|------------|-----------|--------|
| `report.legal_formatter` → `interface.legal_handler` | cross-boundary | Faible : non-cyclique, accepté DEC-022 |
| `storage.legal_results` → `interface.report_handler` | cross-boundary | **Moyen** : si `interface` importe `storage` au module level → cycle. Actuellement non-cyclique car seul `interface.session_handler` importe `storage`. |
| `interface.session_handler` → `storage.legal_results` | interne | Non-cyclique ✓ |

### 3.2 Risque de cycle potentiel

Si une future mission ajoute un import de `storage` dans `interface/__init__.py`
ou dans `legal_handler.py`/`report_handler.py`, un cycle se forme car
`storage.legal_results` importe déjà `interface.report_handler`.

**Mitigation recommandée avant API** : extraire `LegalAnalysisWithReportResponse`
dans `legal/models.py` ou un module `interface/models.py` pour casser ce couplage.

### 3.3 Couplage store ↔ type stocké

`InMemoryLegalResultStore` est typé exclusivement sur
`LegalAnalysisWithReportResponse`. Un stockage générique existait (MIG-008A
`InMemoryStore`) mais n'est pas utilisé. Ce n'est pas un bug mais limite
la réutilisabilité du store.

---

## 4. Limites métier restantes

| Limite | Criticité pour API | Décision requise |
|--------|-------------------|-----------------|
| Aucune validation de format de citation (ex. "L1222-9" vs "article L.1222-9") | Haute | Oui |
| `rule_id` unique : `RULE_CLAUSE_NORM_MINIMAL` — pas de table de règles extensible | Haute | Oui |
| Segmentation clause uniquement sur `\n\n` — fragile sur textes mal formatés | Haute | Oui |
| Comparaison lexicale uniquement — aucune sémantique juridique | Haute | Hors périmètre actuel |
| `record_id` monotone par instance de store — pas d'UUID, pas de déduplication | Moyenne | Oui avant API multi-utilisateur |
| `list_ids()` sans pagination — exposition raw à éviter sur grande volumétrie | Moyenne | Oui avant API |
| Pas d'horodatage sur les résultats stockés | Basse | Oui avant API |
| Aucun champ utilisateur/session dans `LegalSessionResult` | Haute | Oui avant API multi-utilisateur |

---

## 5. Ce qui est PRÊT pour une API locale mono-utilisateur

- Contrats de requête/réponse : stables, typés, immuables.
- Déterminisme : même entrée → même sortie (pas de random, pas d'I/O).
- Gestion `insufficient_data` : chemin d'erreur fonctionnel et testé.
- Rapport texte : déterministe, lisible, sans dépendance externe.
- Stockage session mémoire : fonctionnel, injecté, isolé.
- Suite de tests : 160 tests couvrant tous les modules et flux d'acceptation.

---

## 6. Ce qui N'EST PAS prêt pour une API publique ou multi-utilisateur

| Blocage | Sévérité |
|---------|----------|
| Pas d'authentification ni d'autorisation | CRITIQUE |
| Store non thread-safe (dict Python sans verrou) | CRITIQUE multi-thread |
| record_id non-universel (reset au redémarrage, collision entre instances) | CRITIQUE persistance |
| Aucune limite de taille sur `text` en entrée | HAUTE |
| Aucun contrat d'erreur HTTP formalisé (codes, formats) | HAUTE |
| Couplage `storage → interface` à casser avant extension | MOYENNE |
| Pas de versioning de l'API (`/v1/`, content-type) | MOYENNE |
| Pas de rate limiting | MOYENNE |

---

## 7. Prochaine étape recommandée

**Option A — API locale FastAPI mono-utilisateur (portée minimale)**
- Wrapper HTTP sur `analyze_and_store_legal_text()`.
- Store unique injecté par l'application (pas par requête).
- Contrat: `POST /analyze` → `{ record_id, analysis, report_text }`.
- Limites acceptées : mono-utilisateur, pas de persistance, pas d'auth.
- Prérequis : décision explicite dans `DECISIONS.md`.

**Option B — Renforcement du modèle de données avant API**
- Extraire `LegalAnalysisWithReportResponse` dans `legal/models.py`.
- Ajouter UUID à `record_id`.
- Ajouter horodatage `created_at` à `LegalSessionResult`.
- Puis Option A.

**Option C — Nouvelle fonctionnalité métier (règles, citations)**
- Validation de format de citation.
- Table de règles extensible.
- Puis Options A ou B.

**Recommandation** : Option A avec périmètre explicitement mono-utilisateur,
précédée d'une décision dans `DECISIONS.md` confirmant les limites acceptées.
Ne pas démarrer sans ce cadrage — l'exposition externe sans auth est un risque
de sécurité même en environnement local.

---

## 8. Verdict maturité

| Domaine | Verdict |
|---------|---------|
| Contrats internes | PRÊT |
| Tests de non-régression | PRÊT |
| Déterminisme | PRÊT |
| Exposition API mono-utilisateur locale | PRÊT avec cadrage |
| Exposition API publique/multi-utilisateur | NON PRÊT |
| Persistance disque/DB | NON DÉCIDÉ |
| Frontend/MCP/LLM | HORS PÉRIMÈTRE |
