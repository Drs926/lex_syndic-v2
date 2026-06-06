"""Tests for FastAPI local HTTP API [LEX-034]."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from lex_syndic.api.fastapi_app import app

SAMPLE_TEXT = (
    "Accord d'entreprise relatif au télétravail. "
    "Article 1 : Le télétravail est mis en place conformément aux dispositions légales. "
    "Article 2 : Les salariés peuvent exercer leurs fonctions en télétravail deux jours par semaine."
)

SAMPLE_TEXT_2 = (
    "Convention collective nationale de la métallurgie. "
    "Article 3 : Les heures supplémentaires sont rémunérées conformément aux dispositions légales. "
    "Article 4 : Les congés payés sont accordés selon les termes de la convention."
)


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_valid(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert response.status_code == 200
    data = response.json()
    assert "record_id" in data
    assert "decision_status" in data
    assert "alert_level" in data
    assert "report_text" in data
    assert "recommended_action" in data


def test_analyze_empty_text(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": ""})
    assert response.status_code == 422
    assert response.json()["detail"] == "text must not be empty"


def test_analyze_whitespace_only_text(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": "   "})
    assert response.status_code == 422
    assert response.json()["detail"] == "text must not be empty"


def test_analyze_text_too_long(client: TestClient) -> None:
    long_text = "a" * 50001
    response = client.post("/v1/analyze", json={"text": long_text})
    assert response.status_code == 422
    assert response.json()["detail"] == "text exceeds maximum length"


def test_get_result_after_analysis(client: TestClient) -> None:
    post_response = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert post_response.status_code == 200
    record_id = post_response.json()["record_id"]

    get_response = client.get(f"/v1/results/{record_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["record_id"] == record_id
    assert "decision_status" in data
    assert "alert_level" in data
    assert "report_text" in data
    assert "recommended_action" in data


def test_get_result_nonexistent(client: TestClient) -> None:
    response = client.get("/v1/results/result-9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "record not found"


# LEX-033 contract: only /health, POST /v1/analyze, GET /v1/results/{id} are exposed.
# Automatic FastAPI doc routes are disabled (docs_url=None, redoc_url=None, openapi_url=None).
@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_doc_routes_not_exposed(client: TestClient, path: str) -> None:
    response = client.get(path)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# LEX-045: Acceptance tests — dossier listing and status endpoints
# ---------------------------------------------------------------------------


def test_dossiers_acceptance_list_contains_created_analyses(client: TestClient) -> None:
    """Create two analyses; both dossier_ids must appear in GET /v1/dossiers."""
    r1 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert r1.status_code == 200
    id1 = r1.json()["record_id"]

    r2 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})
    assert r2.status_code == 200
    id2 = r2.json()["record_id"]

    list_resp = client.get("/v1/dossiers")
    assert list_resp.status_code == 200
    dossiers = list_resp.json()["dossiers"]
    listed_ids = [d["dossier_id"] for d in dossiers]
    assert id1 in listed_ids
    assert id2 in listed_ids


def test_dossiers_acceptance_listed_ids_retrievable_via_status(client: TestClient) -> None:
    """Every dossier_id returned by GET /v1/dossiers must resolve via GET /v1/dossiers/{id}/status."""
    client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})

    list_resp = client.get("/v1/dossiers")
    assert list_resp.status_code == 200
    dossiers = list_resp.json()["dossiers"]
    assert len(dossiers) >= 2

    for entry in dossiers:
        dossier_id = entry["dossier_id"]
        status_resp = client.get(f"/v1/dossiers/{dossier_id}/status")
        assert status_resp.status_code == 200, f"Expected 200 for dossier_id={dossier_id}"
        data = status_resp.json()
        assert data["dossier_id"] == dossier_id
        assert "juridical_status" in data
        assert "alert_level" in data
        assert "recommended_action" in data
        assert "report_text" not in data


def test_dossiers_acceptance_status_consistent_with_list(client: TestClient) -> None:
    """Fields returned by GET /v1/dossiers match those from GET /v1/dossiers/{id}/status."""
    client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})

    list_resp = client.get("/v1/dossiers")
    assert list_resp.status_code == 200

    for entry in list_resp.json()["dossiers"]:
        dossier_id = entry["dossier_id"]
        status_resp = client.get(f"/v1/dossiers/{dossier_id}/status")
        assert status_resp.status_code == 200
        status_data = status_resp.json()
        assert status_data["juridical_status"] == entry["juridical_status"]
        assert status_data["alert_level"] == entry["alert_level"]
        assert status_data["recommended_action"] == entry["recommended_action"]


def test_dossiers_acceptance_unknown_id_returns_404(client: TestClient) -> None:
    """An unknown dossier_id must return 404 with detail 'dossier not found'."""
    response = client.get("/v1/dossiers/result-9999/status")
    assert response.status_code == 404
    assert response.json()["detail"] == "dossier not found"
