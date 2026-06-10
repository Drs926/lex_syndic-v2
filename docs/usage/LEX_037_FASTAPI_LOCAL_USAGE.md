# LEX-037 — FastAPI Local API: Launch Documentation and Usage Contract

DATE: 2026-06-08
BASE: LEX-045 (PR #65), HEAD 8addd86
TESTS: 222 passing

---

## 1. Purpose

This document provides:
- the exact procedure to launch the local FastAPI HTTP API;
- the API usage contract for any team member calling the endpoints;
- the internal developer contract governing future modifications.

The API (`src/lex_syndic/api/fastapi_app.py`) is a **single-user, local-only**
HTTP interface to the `lex_syndic` legal analysis pipeline. It is not a
production service.

---

## 2. Prerequisites

### Python environment

```bash
# From repository root — requires Python >= 3.11
pip install -e ".[dev]"
# or
pip install -e .
```

This installs `fastapi>=0.111,<1` and `uvicorn[standard]>=0.29,<1` as declared
in `pyproject.toml`.

### Verify installation

```bash
python -c "import fastapi, uvicorn; print('OK')"
```

---

## 3. Launch procedure

**Required command:**

```bash
uvicorn lex_syndic.api.fastapi_app:app --host 127.0.0.1 --port 8000 --workers 1
```

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--host 127.0.0.1` | Mandatory | Local-only binding. Any other value violates DEC-LEX-034. |
| `--port 8000` | Recommended default | May be changed if 8000 is occupied. |
| `--workers 1` | Mandatory | `InMemoryLegalResultStore` is not thread-safe. More than 1 worker creates separate stores and undefined behaviour. |

**Expected startup output:**

```
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 4. API contract

### 4.1 GET /health

Liveness check. No authentication required.

**Request:** `GET http://127.0.0.1:8000/health`

**Response 200:**
```json
{ "status": "ok" }
```

**curl example:**
```bash
curl http://127.0.0.1:8000/health
```

---

### 4.2 POST /v1/analyze

Submit a legal text for analysis. Returns a structured decision and a formatted
text report.

**Request body (JSON):**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `text` | string | Yes | Non-empty, ≤ 50 000 characters |
| `expected_citations` | list[string] | No | Default: `[]` |
| `title` | string | No | Default: `"document"` |

**Response 200:**

| Field | Type | Description |
|-------|------|-------------|
| `record_id` | string | Unique identifier for this result (e.g. `"result-0001"`) |
| `decision_status` | string | One of: `compliant`, `non_compliant`, `attention_required`, `insufficient_data` |
| `alert_level` | string | Severity indicator |
| `report_text` | string | Human-readable analysis report |
| `recommended_action` | string | Recommended next step |

**Response 422 — validation error:**
```json
{ "detail": "text must not be empty" }
```
or
```json
{ "detail": "text exceeds maximum length" }
```

**Response 500 — internal error:**
```json
{ "detail": "internal error" }
```

**curl example:**
```bash
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Article 1 : Le présent accord s applique à l ensemble des salariés. Conformément à L1222-9, le télétravail est autorisé.",
    "expected_citations": ["L1222-9"],
    "title": "Accord télétravail"
  }'
```

---

### 4.3 GET /v1/results/{record_id}

Retrieve a previously stored analysis result by its `record_id`.

**Response 200:** Same shape as POST /v1/analyze response.

**Response 404:**
```json
{ "detail": "record not found" }
```

**curl example:**
```bash
curl http://127.0.0.1:8000/v1/results/result-0001
```

---

### 4.4 GET /v1/dossiers

List all dossiers that have been analysed in the current session. Returns a
lightweight status summary for each one; `report_text` is intentionally excluded.
Returns an empty list when the in-memory store contains no records.

**Request:** `GET http://127.0.0.1:8000/v1/dossiers`

**Response 200:**

```json
{
  "dossiers": [
    {
      "dossier_id": "result-0001",
      "juridical_status": "compliant",
      "alert_level": "low",
      "recommended_action": "No action required."
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `dossiers` | list | Ordered list of dossier summaries (empty if none stored) |
| `dossier_id` | string | Equals the `record_id` returned by POST /v1/analyze |
| `juridical_status` | string | One of: `compliant`, `non_compliant`, `attention_required`, `insufficient_data` |
| `alert_level` | string | Severity indicator |
| `recommended_action` | string | Recommended next step |

**curl example:**
```bash
curl http://127.0.0.1:8000/v1/dossiers
```

---

### 4.5 GET /v1/dossiers/{dossier_id}/status

Retrieve the lightweight juridical status for a single dossier. In the current
single-document architecture, `dossier_id` equals the `record_id` returned by
POST /v1/analyze. Only status fields are returned; the full report text is
available via GET /v1/results/{record_id}.

**Response 200:**

| Field | Type | Description |
|-------|------|-------------|
| `dossier_id` | string | The requested identifier |
| `juridical_status` | string | One of: `compliant`, `non_compliant`, `attention_required`, `insufficient_data` |
| `alert_level` | string | Severity indicator |
| `recommended_action` | string | Recommended next step |

**Response 404:**
```json
{ "detail": "dossier not found" }
```

**curl example:**
```bash
curl http://127.0.0.1:8000/v1/dossiers/result-0001/status
```

---

### 4.6 Disabled routes

The following routes are **intentionally disabled** (return HTTP 404):

| Route | Reason |
|-------|--------|
| `/docs` | Not in LEX-033 contract (DEC-LEX-034) |
| `/redoc` | Not in LEX-033 contract (DEC-LEX-034) |
| `/openapi.json` | Not in LEX-033 contract (DEC-LEX-034) |

Re-enabling these routes requires a new decision in `DECISIONS.md`.

---

## 5. Known constraints and limitations

| Constraint | Detail |
|-----------|--------|
| **Volatile store** | All results are lost when the server process stops. This is expected behaviour — the store is in-memory only. |
| **No authentication** | Any local process can call the API. Do not expose over a network. |
| **Local only** | Binding to anything other than `127.0.0.1` violates DEC-LEX-034. |
| **Single worker** | `workers=1` is mandatory. Multiple workers each have their own store — a `record_id` from worker A cannot be retrieved from worker B. |
| **Indicative results** | The analysis pipeline uses heuristic rules, not live access to Légifrance or Judilibre. All results are **indicative only** and must be validated by a qualified legal professional. |
| **No concurrency guarantee** | No request queue, no rate limiting, no concurrency handling. Designed for sequential single-user use. |

---

## 6. Internal developer usage contract

This section governs future modifications to `src/lex_syndic/api/fastapi_app.py`
and the broader `api/` module.

### What is frozen

| Element | Rule |
|---------|------|
| Endpoint paths | `POST /v1/analyze`, `GET /v1/results/{record_id}`, `GET /health`, `GET /v1/dossiers`, `GET /v1/dossiers/{dossier_id}/status` are the authorised paths. |
| Disabled routes | `/docs`, `/redoc`, `/openapi.json` must remain disabled unless a new DECISIONS.md entry explicitly activates them. |
| Host binding | Must remain `127.0.0.1`. Any non-localhost binding requires a new decision. |
| Workers | Must remain 1. Multi-worker requires a thread-safe store and a new decision. |
| Store type | `InMemoryLegalResultStore` only. Disk or database storage requires a new decision. |
| Authentication | None for local use. Adding auth requires a new decision. |

### What requires a new DECISIONS.md entry before implementation

- Any new endpoint
- Activation of `/docs`, `/redoc`, `/openapi.json`
- Any non-localhost network binding
- Any persistence mechanism (disk, DB, Redis, etc.)
- Authentication or authorization layer
- Workers > 1 or async concurrency model
- Any new external dependency beyond `fastapi` and `uvicorn[standard]`
- MCP integration, LLM calls, external legal connectors

### Dependency chain (informational)

```
fastapi_app.py
  → lex_syndic.api.local (submit_analysis, LocalApiAnalysisRequest)
    → lex_syndic.interface.session_handler (analyze_and_store_legal_text)
      → lex_syndic.interface.report_handler (analyze_legal_text_with_report)
        → lex_syndic.interface.legal_handler (analyze_legal_text)
          → lex_syndic.pipeline (run_legal_pipeline)
  → lex_syndic.storage.legal_results (InMemoryLegalResultStore)
```

No circular dependencies. `storage` does not import from `interface` (LEX-032).

### Testing obligations

Any modification to `fastapi_app.py` must:
1. Keep all 194 existing tests green.
2. Add tests in `tests/test_api_fastapi.py` for any new endpoint behaviour.
3. Add or update acceptance tests in `tests/test_acceptance_fastapi_local.py`
   for any user-observable change.

---

## 7. Reference

| Document | Path |
|----------|------|
| FastAPI exposure framing | `docs/architecture/LEX_033_FASTAPI_EXPOSURE_FRAME.md` |
| FastAPI local maturity audit | `docs/audits/LEX_036_FASTAPI_LOCAL_MATURITY_AUDIT.md` |
| Authorising decision | `DECISIONS.md` § DEC-LEX-034 |
| FastAPI application source | `src/lex_syndic/api/fastapi_app.py` |
| Unit tests (core) | `tests/test_api_fastapi.py` |
| Unit tests (dossiers list) | `tests/test_api_list_dossiers.py` |
| Acceptance tests (FastAPI) | `tests/test_acceptance_fastapi_local.py` |
| Acceptance tests (juridical status) | `tests/test_acceptance_juridical_status.py` |
