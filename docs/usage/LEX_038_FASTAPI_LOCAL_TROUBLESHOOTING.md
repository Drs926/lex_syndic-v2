# LEX-038 — FastAPI Local API: Troubleshooting Guide

DATE: 2026-06-04
BASE: LEX-037 (PR #57), HEAD 9acdcf1
TESTS: 194 passing

---

## 1. Purpose

This document lists common problems encountered when running the local FastAPI
server or its test suite on a development machine, and their resolutions.

It complements the launch and usage documentation in
`docs/usage/LEX_037_FASTAPI_LOCAL_USAGE.md`.

---

## 2. Local limitations reminder

Before troubleshooting, recall the hard constraints of this API:

| Constraint | Detail |
|-----------|--------|
| **Development only** | Not a production service. Single-user, local machine only. |
| **No authentication** | Any local process can call the API. Never expose over a network. |
| **In-memory store** | All results are lost when the server stops. This is expected. |
| **Indicative results** | Analysis is heuristic-based, not connected to Légifrance or Judilibre. All results must be validated by a qualified legal professional. |
| **Single worker mandatory** | `--workers 1` is required. Multiple workers create separate in-memory stores and produce undefined behaviour. |

---

## 3. Common problems and solutions

### 3.1 Port already in use

**Symptom:**

```
ERROR:    [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): only one usage of each socket address (protocol/network address/port) is normally permitted
```

or on Linux/macOS:

```
ERROR:    [Errno 98] error while attempting to bind on address ('127.0.0.1', 8000): address already in use
```

**Cause:** Another process is already listening on port 8000.

**Resolution — option A: change the port**

```bash
uvicorn lex_syndic.api.fastapi_app:app --host 127.0.0.1 --port 8001 --workers 1
```

Use any free port (8001, 8080, 9000, etc.). Update your curl commands or client
calls to match the new port.

**Resolution — option B: find and stop the conflicting process**

On Windows:
```bash
netstat -ano | findstr :8000
# Note the PID in the last column, then:
taskkill /PID <pid> /F
```

On Linux/macOS:
```bash
lsof -i :8000
# Note the PID, then:
kill <pid>
```

Retry the uvicorn command after stopping the conflicting process.

---

### 3.2 Python virtual environment not activated

**Symptom:**

```
ModuleNotFoundError: No module named 'lex_syndic'
```

or:

```
ModuleNotFoundError: No module named 'fastapi'
```

or:

```
uvicorn: command not found
```

**Cause:** The command is running outside the virtual environment where the
package was installed, or the package has never been installed.

**Resolution:**

1. Activate the virtual environment:

   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

   On Linux/macOS:
   ```bash
   source .venv/bin/activate
   ```

2. Verify the environment is active (the prompt should show the venv name):
   ```bash
   python -c "import sys; print(sys.prefix)"
   ```

3. If the package is still not found, install it (see §3.3 below).

---

### 3.3 Missing dependencies

**Symptom:**

```
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'uvicorn'
ModuleNotFoundError: No module named 'lex_syndic'
```

**Cause:** The package and its dependencies have not been installed into the
active environment.

**Resolution:**

```bash
# From the repository root, with the virtual environment activated:
pip install -e ".[dev]"
```

This installs `lex_syndic` in editable mode plus all development dependencies,
including `fastapi>=0.111,<1` and `uvicorn[standard]>=0.29,<1`.

**Verify the installation:**

```bash
python -c "import fastapi, uvicorn; print('OK')"
python -c "import lex_syndic; print('OK')"
```

If either command fails, re-run the `pip install` command above and check for
error output.

---

### 3.4 pytest Windows temp directory PermissionError

**Symptom:**

```
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\<user>\\AppData\\Local\\Temp\\pytest-...'
```

or:

```
ERROR collecting tests/...
...
PermissionError: [WinError 32] The process cannot access the file because it is being used by another process
```

**Cause:** On Windows, pytest's default temp directory (`%TEMP%`) can cause
permission conflicts when test processes are still holding handles to temporary
files, or when a previous test run did not clean up correctly.

**Resolution — use `--basetemp` to redirect pytest temp files:**

```bash
python -m pytest -q --basetemp=pytest_tmp
```

This directs pytest to write all temporary files into a `pytest_tmp/` directory
in the current working directory, which avoids the Windows system temp
permission issues.

The `pytest_tmp/` directory is created automatically. It can be deleted safely
after the test run.

**Alternative: run with explicit temp path in a writable location:**

```bash
python -m pytest -q --basetemp=C:/tmp/pytest_lex
```

---

### 3.5 pytest `--basetemp` usage reference

The `--basetemp` flag controls where pytest writes its temporary files during
the test session.

**Basic usage:**

```bash
python -m pytest -q --basetemp=pytest_tmp
```

**Run specific test files:**

```bash
python -m pytest tests/test_api_fastapi.py -q --basetemp=pytest_tmp
python -m pytest tests/test_acceptance_fastapi_local.py -q --basetemp=pytest_tmp
```

**Run the full test suite:**

```bash
python -m pytest -q --basetemp=pytest_tmp
```

**Expected output (194 tests passing):**

```
.......... [194 tests]
194 passed in Xs
```

**Notes:**
- `pytest_tmp/` is safe to add to `.gitignore` if it is not already listed.
- The directory is overwritten on each run; no manual cleanup is needed between
  runs.
- Do not use a path inside a OneDrive-synced or network-mapped folder —
  this can cause additional PermissionError issues.

---

## 4. Diagnostic checklist

If the server or tests fail and none of the above applies, run through this
checklist:

```
[ ] Virtual environment is activated (python --version shows 3.11+)
[ ] Package is installed (python -c "import lex_syndic; print('OK')" succeeds)
[ ] fastapi and uvicorn are installed (python -c "import fastapi, uvicorn; print('OK')" succeeds)
[ ] Port 8000 is free (or a different --port value is used)
[ ] uvicorn is launched with --workers 1
[ ] uvicorn is launched with --host 127.0.0.1
[ ] Tests are run with python -m pytest (not bare pytest) to ensure the correct interpreter
[ ] On Windows: --basetemp=pytest_tmp is used if PermissionError appears
```

---

## 5. Reference

| Document | Path |
|----------|------|
| Launch and usage documentation | `docs/usage/LEX_037_FASTAPI_LOCAL_USAGE.md` |
| FastAPI exposure framing | `docs/architecture/LEX_033_FASTAPI_EXPOSURE_FRAME.md` |
| FastAPI local maturity audit | `docs/audits/LEX_036_FASTAPI_LOCAL_MATURITY_AUDIT.md` |
| Authorising decision | `DECISIONS.md` § DEC-LEX-034 |
| FastAPI application source | `src/lex_syndic/api/fastapi_app.py` |
| Unit tests | `tests/test_api_fastapi.py` |
| Acceptance tests | `tests/test_acceptance_fastapi_local.py` |
