# LEX-050 - FastAPI v1 HTTP Error Contract

Date: 2026-09-20
Scope: local FastAPI v1 API error responses
Status: Contract test coverage added in `tests/test_api_error_contract.py`

---

## 1. Purpose

This document freezes the observable HTTP error contract for the local
single-user FastAPI API. It documents existing behavior only. It does not
authorize a new endpoint, a new dependency, persistence, authentication, public
network exposure, OpenAPI activation, MCP integration, LLM integration, or any
change to API behavior.

The contract applies to JSON responses returned by
`src/lex_syndic/api/fastapi_app.py`.

---

## 2. Error Shape

All covered errors return a JSON object with one field:

```json
{ "detail": "..." }
```

The `detail` value is stable for the cases listed below. Clients must not rely
on stack traces, Python exception messages, or internal implementation details.

---

## 3. Frozen Cases

| Case | Request | HTTP status | Response body |
|------|---------|-------------|---------------|
| Empty analysis text | `POST /v1/analyze` with `text: ""` | 422 | `{ "detail": "text must not be empty" }` |
| Whitespace-only analysis text | `POST /v1/analyze` with whitespace-only `text` | 422 | `{ "detail": "text must not be empty" }` |
| Analysis text too long | `POST /v1/analyze` with `text` longer than 50,000 characters | 422 | `{ "detail": "text exceeds maximum length" }` |
| Unknown result | `GET /v1/results/{record_id}` for an unknown id | 404 | `{ "detail": "record not found" }` |
| Unknown dossier status | `GET /v1/dossiers/{dossier_id}/status` for an unknown id | 404 | `{ "detail": "dossier not found" }` |
| Unknown dossier deletion | `DELETE /v1/dossiers/{dossier_id}` for an unknown id | 404 | `{ "detail": "dossier not found" }` |
| Unexpected analysis failure | `POST /v1/analyze` when `submit_analysis` raises an unexpected exception | 500 | `{ "detail": "internal error" }` |

---

## 4. Internal Error Rule

Unexpected exceptions raised while processing `POST /v1/analyze` are hidden
from HTTP clients. The response body must stay:

```json
{ "detail": "internal error" }
```

The original exception message must not be exposed in the HTTP response.

---

## 5. Verification

The dedicated contract test file is:

```text
tests/test_api_error_contract.py
```

It covers the seven cases listed in this document. Future changes to
`fastapi_app.py` that alter these responses must update this document and the
contract tests in the same mission, within an explicitly authorized scope.
