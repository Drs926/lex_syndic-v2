# LEX-036 — FastAPI local maturity audit

DATE: 2026-06-03
BASE: LEX-034 (PR #54), LEX-035 (PR #55)
TESTS: 194 passing

## VERDICT
PASS

## RAISON UNIQUE
The FastAPI local HTTP API introduced in LEX-034 and validated by LEX-035 is fully functional and correctly constrained for single-user local development use, with all endpoints tested, all forbidden routes disabled, and all architecture contract obligations fulfilled.

## Scope audited
- src/lex_syndic/api/fastapi_app.py
- tests/test_api_fastapi.py (10 cases)
- tests/test_acceptance_fastapi_local.py (8 cases)
- docs/architecture/LEX_033_FASTAPI_EXPOSURE_FRAME.md
- DECISIONS.md (DEC-LEX-034)
- pyproject.toml (fastapi + uvicorn[standard])

## What is validated
- POST /v1/analyze, GET /v1/results/{record_id}, GET /health available and tested
- /docs, /redoc, /openapi.json disabled and tested to return 404
- InMemoryLegalResultStore: session-scoped, no disk write
- Text guard enforced: empty text and text >50000 chars rejected with 422
- fastapi>=0.111,<1 and uvicorn[standard]>=0.29,<1 added; no other dependency added
- 10 unit-level API test cases pass (test_api_fastapi.py)
- 8 acceptance-level test cases pass on realistic accord d'entreprise (test_acceptance_fastapi_local.py)
- All 194 existing tests pass; zero regressions introduced by LEX-034/035
- No src/ modification outside src/lex_syndic/api/fastapi_app.py

## Current maturity
- Usable locally (single user, development): YES — endpoints functional, tested, guards enforced
- Usable over network: NO — no TLS, no auth, bound to 127.0.0.1
- Usable in production: NO — no persistence, no auth, volatile store, single worker
- Usable for controlled internal demonstration: YES — with explicit disclaimer about volatile store

## Risks
- Store is volatile: all results lost on server restart
- No authentication: any local process can call the API
- Thread-safety not guaranteed if workers > 1 (uvicorn must be launched with workers=1)
- Internal exceptions masked as HTTP 500 "internal error" — no structured error logging
- No formal API versioning (URL prefix /v1/ exists but no versioning contract)
- No user-facing launch documentation in the repository

## Forbidden without new decision in DECISIONS.md
- Network exposure (any non-localhost binding)
- Authentication layer
- Disk persistence or database
- Activation of /docs, /redoc, /openapi.json
- MCP integration
- LLM calls inside API endpoints
- External legal connectors (Légifrance, Judilibre)

## Recommendation
LEX-037 — User-facing launch documentation and internal usage contract.
The API is operational but has no documented launch procedure or usage contract in the repository; adding these would make the local API usable by any team member without requiring code archaeology.
