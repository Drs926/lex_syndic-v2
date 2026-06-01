# LEX-033 — Cadrage exposition FastAPI avant implémentation

Date : 2026-06-02
Statut : Cadrage documentaire — aucune implémentation
Base : HEAD `115754c252ec4092d409416d1a92112e6086bfeb`
Référence audit : `docs/audits/LEX_029_PRODUCT_MATURITY_AUDIT.md`

---

## 1. FastAPI est-il acceptable comme prochaine dépendance ?

**Réponse : OUI, sous conditions strictes.**

### Conditions obligatoires

| Condition | Détail |
|-----------|--------|
| Périmètre local uniquement | Pas d'exposition réseau publique, pas de TLS, pas de déploiement cloud |
| Mono-utilisateur | Un seul processus, un seul worker, aucune concurrence multi-requêtes simultanées |
| Store non persistant accepté | Les résultats sont perdus au redémarrage — documenté explicitement |
| Pas d'auth pour usage local | Auth différée à une décision séparée si exposition réseau |
| Limitation taille texte imposée | Guard explicite en entrée avant traitement |
| Aucune autre dépendance ajoutée | FastAPI entraîne `starlette` + `anyio` + `pydantic` — toutes transitives, aucune autre ajoutée manuellement |

### Impact sur dépendances

Ajouter `fastapi` dans `pyproject.toml` [project.dependencies] entraîne :
- `starlette` — routage HTTP (transitive)
- `pydantic` — validation schéma (transitive)
- `anyio` — I/O async (transitive)
- `uvicorn[standard]` — serveur ASGI (à ajouter explicitement pour lancer)

Aucune de ces dépendances n'affecte la logique juridique (`legal`, `analysis`,
`comparison`, `rules`, `pipeline`, `report`). Elles s'ajoutent uniquement à
la couche `api/`.

---

## 2. Portée autorisée si FastAPI est accepté

| Critère | Valeur |
|---------|--------|
| Exposition | **Local uniquement** — `127.0.0.1` ou `localhost` |
| Utilisateurs | **Mono-utilisateur** — 1 worker, pas de concurrence |
| Store | **InMemoryLegalResultStore** — session mémoire, non partagé entre workers |
| Authentification | **Aucune** pour usage local. Obligatoire si réseau |
| Persistance | **Aucune** — les résultats ne survivent pas au redémarrage |
| Endpoints autorisés | `POST /v1/analyze`, `GET /v1/results/{record_id}`, `GET /health` |
| Endpoints interdits | Toute route admin, toute route multi-utilisateur, toute route CRUD sur store |

---

## 3. Contrat API minimal proposé

### POST /v1/analyze

**Requête**
```json
{
  "text": "string (non vide, ≤ 50 000 caractères)",
  "expected_citations": ["L1222-9", "L3121-1"],
  "title": "string (optionnel, défaut: 'document')"
}
```

**Réponse 200**
```json
{
  "record_id": "result-0001",
  "decision_status": "compliant | non_compliant | attention_required | insufficient_data",
  "alert_level": "string",
  "report_text": "string (rapport texte déterministe)",
  "recommended_action": "string"
}
```

**Réponse 422 — validation**
```json
{
  "detail": "text must not be empty | text exceeds maximum length"
}
```

**Réponse 500 — erreur interne**
```json
{
  "detail": "internal error"
}
```

---

### GET /v1/results/{record_id}

**Réponse 200**
```json
{
  "record_id": "result-0001",
  "decision_status": "string",
  "alert_level": "string",
  "report_text": "string",
  "recommended_action": "string"
}
```

**Réponse 404**
```json
{
  "detail": "record not found"
}
```

---

### GET /health

**Réponse 200**
```json
{
  "status": "ok"
}
```

---

## 4. Prérequis bloquants avant implémentation

| Prérequis | État actuel | Action requise |
|-----------|-------------|----------------|
| Limite taille texte | Absent | Ajouter guard `len(text) ≤ 50 000` dans `LocalApiAnalysisRequest` ou dans l'endpoint |
| record_id stable (UUID) | Absent — monotone par instance | Acceptable en local mono-utilisateur ; UUID différé à usage réseau |
| Store thread-safe | Absent | Acceptable avec `workers=1` explicite dans uvicorn ; documenter la limitation |
| Contrat erreur HTTP formalisé | Absent | À implémenter dans l'endpoint (422, 404, 500) |
| Auth | Absente | Acceptable local ; obligatoire si exposition réseau |
| Limitation workers=1 | Non décidée | À imposer dans la commande de lancement |

**Tous ces prérequis sont satisfaisables dans le périmètre local mono-utilisateur.**
Aucun n'exige une dépendance supplémentaire au-delà de FastAPI + uvicorn.

---

## 5. Risques

| Risque | Sévérité | Mitigation |
|--------|----------|------------|
| Faux sentiment SaaS | Haute | Documentation et avertissement explicites dans README |
| Store non persistant entre redémarrages | Haute | Documenter, logger à chaque démarrage |
| Concurrence si workers > 1 | Haute | Imposer `--workers 1` ou `workers=1` dans uvicorn |
| Texte juridique sensible en transit HTTP local | Moyenne | Usage local uniquement, pas de TLS nécessaire sur 127.0.0.1 |
| Absence sources juridiques officielles (Légifrance, Judilibre) | Haute | Disclaimer dans les réponses API — les résultats sont indicatifs |
| Dérive vers déploiement cloud non cadré | Haute | Toute exposition réseau exige une décision séparée dans DECISIONS.md |

---

## 6. Recommandation unique pour LEX-034

**LEX-034 = Implémentation FastAPI locale strictement bornée.**

### Justification

- L'API locale pure Python (`submit_analysis`) est validée et stable.
- Le couplage `storage → interface` est supprimé — l'architecture est propre.
- FastAPI est la dépendance minimale correcte pour exposer un endpoint HTTP local.
- Tous les prérequis bloquants sont satisfaisables dans le périmètre local mono-utilisateur sans dépendance supplémentaire.
- Renforcer le contrat input/error peut être fait à l'intérieur de LEX-034, pas avant.

### Périmètre LEX-034

| Élément | Valeur |
|---------|--------|
| Dépendance à ajouter | `fastapi`, `uvicorn[standard]` dans `pyproject.toml` |
| Modules à créer | `src/lex_syndic/api/app.py` — application FastAPI |
| Endpoints | `POST /v1/analyze`, `GET /v1/results/{record_id}`, `GET /health` |
| Store | Singleton local à l'application (pas global au module) |
| Workers | 1 imposé |
| Tests | `tests/test_api_fastapi.py` avec `httpx` + `TestClient` |
| Acceptation | `tests/test_acceptance_api_fastapi.py` |
| Interdits | Auth, multi-worker, persistance, exposition réseau |
| Critère de PASS | Tous tests verts. `POST /v1/analyze` retourne `record_id`. `GET /v1/results/{record_id}` retourne le résultat. `GET /health` retourne `ok`. |
