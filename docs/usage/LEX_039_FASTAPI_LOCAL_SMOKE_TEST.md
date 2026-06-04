# LEX-039 — FastAPI Local API: Smoke Test Guide

DATE: 2026-06-04
BASE: LEX-038 (PR #58), HEAD c58f4af
TESTS: 194 passing

---

## 1. Purpose

A smoke test is a minimal check that the server starts and responds to basic
requests. It does not test every endpoint in depth — that is the role of the
automated test suite. Run this guide after a fresh install or environment
change to confirm the API is wired up correctly before doing any real work.

---

## 2. Start the server

From the repository root, with your virtual environment activated:

```bash
uvicorn lex_syndic.api.fastapi_app:app --host 127.0.0.1 --port 8000 --workers 1
```

**Expected startup output:**

```
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

If you do not see `Application startup complete.`, stop here and consult
[§4 Quick failure interpretation](#4-quick-failure-interpretation).

---

## 3. Health check

In a second terminal, confirm the server is reachable:

```bash
curl http://127.0.0.1:8000/health
```

**Expected response:**

```json
{"status":"ok"}
```

HTTP 200 and `{"status":"ok"}` means the server is running and responsive.

---

## 4. Analysis endpoint check

Submit a minimal legal text to confirm the analysis pipeline is reachable:

```bash
curl -X POST http://127.0.0.1:8000/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Article 1 : Le présent accord s applique à l ensemble des salariés. Conformément à L1222-9, le télétravail est autorisé.",
    "expected_citations": ["L1222-9"],
    "title": "Smoke test"
  }'
```

**Expected: HTTP 200 with a JSON body containing:**

- `record_id` — a string such as `"result-0001"`
- `decision_status` — one of `compliant`, `non_compliant`, `attention_required`, `insufficient_data`
- `alert_level`, `report_text`, `recommended_action` — non-empty strings

Any 200 response with these fields present means the full pipeline is
functioning correctly.

---

## 5. Signs of success

| Check | Expected sign |
|-------|--------------|
| Server starts | `Application startup complete.` in the uvicorn log |
| Health endpoint | HTTP 200, `{"status":"ok"}` |
| Analysis endpoint | HTTP 200, JSON body with `record_id` and `decision_status` |

If all three pass, the local API is working correctly.

---

## 6. Quick failure interpretation

### Server not started

```
curl: (7) Failed to connect to 127.0.0.1 port 8000: Connection refused
```

The uvicorn process is not running. Start it with the command in §2 and wait
for `Application startup complete.`.

---

### Wrong port

```
curl: (7) Failed to connect to 127.0.0.1 port 8000: Connection refused
```

If uvicorn started on a different port (e.g. `--port 8001`), update your curl
command to match:

```bash
curl http://127.0.0.1:8001/health
```

The port in your curl command must match `--port` in the uvicorn command.

---

### Virtualenv or dependencies missing

```
ModuleNotFoundError: No module named 'lex_syndic'
ModuleNotFoundError: No module named 'fastapi'
uvicorn: command not found
```

Activate your virtual environment and install dependencies:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Then install
pip install -e ".[dev]"
```

Verify the installation:

```bash
python -c "import fastapi, uvicorn, lex_syndic; print('OK')"
```

---

### In-memory data reset after restart

A `GET /v1/results/<record_id>` that previously returned 200 now returns:

```json
{"detail":"record not found"}
```

This is expected behaviour. The store is in-memory only — all results are lost
when the server process stops. Resubmit the analysis with `POST /v1/analyze`
to get a new `record_id`.

---

## 7. Reference

| Document | Path |
|----------|------|
| Full launch procedure and API contract | `docs/usage/LEX_037_FASTAPI_LOCAL_USAGE.md` |
| Common problems and resolutions | `docs/usage/LEX_038_FASTAPI_LOCAL_TROUBLESHOOTING.md` |
| Authorising decision | `DECISIONS.md` § DEC-LEX-034 |
| FastAPI application source | `src/lex_syndic/api/fastapi_app.py` |
| Unit tests | `tests/test_api_fastapi.py` |
| Acceptance tests | `tests/test_acceptance_fastapi_local.py` |
