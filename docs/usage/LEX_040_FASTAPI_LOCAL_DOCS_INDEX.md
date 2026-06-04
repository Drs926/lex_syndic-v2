# LEX-040 — FastAPI Local Documentation Index

DATE: 2026-06-04
BASE: LEX-039 (PR #59), HEAD 49b86de

## Purpose

This index covers the three guides that document the local FastAPI development server for `lex_syndic_v2`. Use it to pick the right guide without reading all three.

---

## Document Map

| Document | What it covers | When to open it |
|---|---|---|
| [LEX-037 — Usage Guide](LEX_037_FASTAPI_LOCAL_USAGE.md) | How to launch the server, available endpoints, request/response examples, and the usage contract | Starting fresh — first thing to read |
| [LEX-039 — Smoke Test Guide](LEX_039_FASTAPI_LOCAL_SMOKE_TEST.md) | Step-by-step `curl` / HTTP sequences to confirm the server is working end-to-end | After launch, to verify the API responds correctly |
| [LEX-038 — Troubleshooting Guide](LEX_038_FASTAPI_LOCAL_TROUBLESHOOTING.md) | Common errors, root causes, and fixes (port conflicts, import errors, missing deps, etc.) | When something goes wrong |

---

## Recommended Reading Order

1. **[Usage Guide (LEX-037)](LEX_037_FASTAPI_LOCAL_USAGE.md)** — understand how to start the server and what endpoints exist.
2. **[Smoke Test Guide (LEX-039)](LEX_039_FASTAPI_LOCAL_SMOKE_TEST.md)** — run the quick checks to confirm everything is working.
3. **[Troubleshooting Guide (LEX-038)](LEX_038_FASTAPI_LOCAL_TROUBLESHOOTING.md)** — consult only when a step above fails.

---

## Local Server Limitations

This documentation applies to the **local development server only**.

| Limitation | Detail |
|---|---|
| Development only | Not for staging or production use |
| No authentication | All endpoints are open; no tokens or credentials required |
| In-memory store | Data is held in memory, not persisted to disk or a database |
| Results reset after restart | Stopping the server clears all state; re-run smoke tests after each restart |
