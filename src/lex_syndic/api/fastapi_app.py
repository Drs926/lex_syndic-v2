"""FastAPI local single-user HTTP API for lex_syndic [LEX-034 / LEX-043 / LEX-044].

Constraints (from LEX-033 contract):
- Bind to 127.0.0.1 only — no public network exposure.
- Single worker, no concurrency (workers=1 imposed at launch).
- InMemoryLegalResultStore — results lost on restart.
- No authentication.
- Text guard: len(text) > 50000 → HTTP 422 before calling pipeline.

LEX-043 addition:
- GET /v1/dossiers/{dossier_id}/status — lightweight juridical status for a
  case file (dossier).  In the current single-document architecture a dossier_id
  maps 1-to-1 to the record_id returned by POST /v1/analyze.  Returns only the
  status fields; the full report text remains available via GET /v1/results/{id}.

LEX-044 addition:
- GET /v1/dossiers — list all known dossiers with their juridical status summary.
  Returns dossier_id, juridical_status, alert_level, recommended_action for every
  stored dossier.  report_text is intentionally excluded.  Empty list when the
  in-memory store contains no records.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from lex_syndic.api.local import LocalApiAnalysisRequest, submit_analysis
from lex_syndic.storage.legal_results import InMemoryLegalResultStore


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.store = InMemoryLegalResultStore()
    yield


app = FastAPI(
    lifespan=lifespan,
    # Disable automatic doc routes — not in LEX-033 contract (DEC-LEX-034).
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


class AnalyzeRequest(BaseModel):
    text: str
    expected_citations: list[str] = Field(default_factory=list)
    title: str = "document"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/analyze")
def analyze(body: AnalyzeRequest, request: Request) -> JSONResponse:
    if not body.text.strip():
        raise HTTPException(status_code=422, detail="text must not be empty")
    if len(body.text) > 50000:
        raise HTTPException(status_code=422, detail="text exceeds maximum length")

    try:
        api_request = LocalApiAnalysisRequest(
            text=body.text,
            expected_citations=tuple(body.expected_citations),
            title=body.title,
        )
        response = submit_analysis(api_request, request.app.state.store)
    except Exception:
        raise HTTPException(status_code=500, detail="internal error")

    return JSONResponse(
        status_code=200,
        content={
            "record_id": response.record_id,
            "decision_status": response.decision_status,
            "alert_level": response.alert_level,
            "report_text": response.report_text,
            "recommended_action": response.recommended_action,
        },
    )


@app.get("/v1/results/{record_id}")
def get_result(record_id: str, request: Request) -> JSONResponse:
    store: InMemoryLegalResultStore = request.app.state.store
    record = store.get(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="record not found")

    # record is LegalAnalysisWithReportResponse stored by submit_analysis
    return JSONResponse(
        status_code=200,
        content={
            "record_id": record_id,
            "decision_status": record.analysis.decision_status,
            "alert_level": record.analysis.alert_level,
            "report_text": record.report_text,
            "recommended_action": record.analysis.recommended_action,
        },
    )


@app.get("/v1/dossiers")
def list_dossiers(request: Request) -> JSONResponse:
    """Return the list of all dossiers with their juridical status summary [LEX-044].

    Each entry contains only lightweight status fields; report_text is excluded.
    Returns an empty list when no dossier has been analysed yet.

    Returns:
        200  {"dossiers": [{"dossier_id", "juridical_status", "alert_level",
              "recommended_action"}, ...]}
    """
    store: InMemoryLegalResultStore = request.app.state.store
    dossiers = []
    for dossier_id in store.list_ids():
        record = store.get(dossier_id)
        if record is not None:
            dossiers.append(
                {
                    "dossier_id": dossier_id,
                    "juridical_status": record.analysis.decision_status,
                    "alert_level": record.analysis.alert_level,
                    "recommended_action": record.analysis.recommended_action,
                }
            )
    return JSONResponse(status_code=200, content={"dossiers": dossiers})


@app.get("/v1/dossiers/{dossier_id}/status")
def get_dossier_juridical_status(dossier_id: str, request: Request) -> JSONResponse:
    """Return the lightweight juridical analysis status for a dossier [LEX-043].

    In the current single-document architecture, dossier_id equals the record_id
    returned by POST /v1/analyze.  Only status fields are returned; the full
    analysis report remains available via GET /v1/results/{record_id}.

    Returns:
        200  {"dossier_id", "juridical_status", "alert_level", "recommended_action"}
        404  {"detail": "dossier not found"}
    """
    store: InMemoryLegalResultStore = request.app.state.store
    record = store.get(dossier_id)
    if record is None:
        raise HTTPException(status_code=404, detail="dossier not found")

    return JSONResponse(
        status_code=200,
        content={
            "dossier_id": dossier_id,
            "juridical_status": record.analysis.decision_status,
            "alert_level": record.analysis.alert_level,
            "recommended_action": record.analysis.recommended_action,
        },
    )
