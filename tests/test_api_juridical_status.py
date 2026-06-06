"""Unit tests for GET /v1/dossiers/{dossier_id}/status [LEX-043]."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from lex_syndic.api.fastapi_app import app

SAMPLE_TEXT = (
    "Accord d'entreprise relatif au télétravail. "
    "Article 1 : Le télétravail est mis en place conformément aux dispositions légales. "
    "Article 2 : Les salariés peuvent exercer leurs fonctions en télétravail deux jours par semaine."
)


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def stored_dossier_id(client: TestClient) -> str:
    """Submit an analysis and return the resulting record_id as dossier_id."""
    response = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert response.status_code == 200
    return response.json()["record_id"]


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


def test_get_dossier_status_returns_200(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 200


def test_get_dossier_status_response_shape(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"dossier_id", "juridical_status", "alert_level", "recommended_action"}


def test_get_dossier_status_dossier_id_matches(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 200
    assert response.json()["dossier_id"] == stored_dossier_id


def test_get_dossier_status_juridical_status_non_empty(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 200
    assert response.json()["juridical_status"] != ""


def test_get_dossier_status_alert_level_non_empty(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 200
    assert response.json()["alert_level"] != ""


def test_get_dossier_status_does_not_include_report_text(
    client: TestClient, stored_dossier_id: str
) -> None:
    """Status endpoint must NOT expose the full report text (LEX-043 contract)."""
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 200
    assert "report_text" not in response.json()


def test_get_dossier_status_consistent_with_analyze(
    client: TestClient,
) -> None:
    """juridical_status in status endpoint must match decision_status from analyze."""
    post_response = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert post_response.status_code == 200
    post_data = post_response.json()
    dossier_id = post_data["record_id"]

    status_response = client.get(f"/v1/dossiers/{dossier_id}/status")
    assert status_response.status_code == 200
    status_data = status_response.json()

    assert status_data["juridical_status"] == post_data["decision_status"]
    assert status_data["alert_level"] == post_data["alert_level"]
    assert status_data["recommended_action"] == post_data["recommended_action"]


# ---------------------------------------------------------------------------
# 404 cases
# ---------------------------------------------------------------------------


def test_get_dossier_status_nonexistent_returns_404(client: TestClient) -> None:
    response = client.get("/v1/dossiers/dossier-9999/status")
    assert response.status_code == 404


def test_get_dossier_status_nonexistent_detail(client: TestClient) -> None:
    response = client.get("/v1/dossiers/unknown-id/status")
    assert response.status_code == 404
    assert response.json()["detail"] == "dossier not found"


def test_get_dossier_status_different_ids_are_independent(
    client: TestClient,
) -> None:
    """Two independent analyses produce independent dossier statuses."""
    r1 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    r2 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert r1.status_code == 200
    assert r2.status_code == 200

    id1 = r1.json()["record_id"]
    id2 = r2.json()["record_id"]
    assert id1 != id2

    s1 = client.get(f"/v1/dossiers/{id1}/status")
    s2 = client.get(f"/v1/dossiers/{id2}/status")
    assert s1.status_code == 200
    assert s2.status_code == 200
    assert s1.json()["dossier_id"] == id1
    assert s2.json()["dossier_id"] == id2
