"""Unit tests for DELETE /v1/dossiers/{dossier_id} [LEX-047]."""

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
    "Contrat de travail à durée déterminée. "
    "Article 1 : Le présent contrat est conclu pour une durée de six mois. "
    "Article 2 : La rémunération mensuelle brute est fixée à 2500 euros."
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
# T1 — DELETE returns 204 for an existing dossier
# ---------------------------------------------------------------------------


def test_delete_dossier_returns_204(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.delete(f"/v1/dossiers/{stored_dossier_id}")
    assert response.status_code == 204


# ---------------------------------------------------------------------------
# T2 — After DELETE, GET /v1/dossiers/{id}/status returns 404
# ---------------------------------------------------------------------------


def test_delete_dossier_then_status_returns_404(
    client: TestClient, stored_dossier_id: str
) -> None:
    client.delete(f"/v1/dossiers/{stored_dossier_id}")
    response = client.get(f"/v1/dossiers/{stored_dossier_id}/status")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# T3 — After DELETE, GET /v1/results/{id} returns 404
# ---------------------------------------------------------------------------


def test_delete_dossier_then_result_returns_404(
    client: TestClient, stored_dossier_id: str
) -> None:
    client.delete(f"/v1/dossiers/{stored_dossier_id}")
    response = client.get(f"/v1/results/{stored_dossier_id}")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# T4 — After DELETE, dossier is absent from GET /v1/dossiers list
# ---------------------------------------------------------------------------


def test_delete_dossier_absent_from_list(
    client: TestClient, stored_dossier_id: str
) -> None:
    client.delete(f"/v1/dossiers/{stored_dossier_id}")
    list_response = client.get("/v1/dossiers")
    assert list_response.status_code == 200
    dossier_ids = [d["dossier_id"] for d in list_response.json()["dossiers"]]
    assert stored_dossier_id not in dossier_ids


# ---------------------------------------------------------------------------
# T5 — DELETE unknown dossier returns 404
# ---------------------------------------------------------------------------


def test_delete_unknown_dossier_returns_404(client: TestClient) -> None:
    response = client.delete("/v1/dossiers/nonexistent-dossier-id")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# T6 — DELETE unknown dossier detail message
# ---------------------------------------------------------------------------


def test_delete_unknown_dossier_detail(client: TestClient) -> None:
    response = client.delete("/v1/dossiers/unknown-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "dossier not found"


# ---------------------------------------------------------------------------
# T7 — Deleting one dossier does not affect others
# ---------------------------------------------------------------------------


def test_delete_one_dossier_leaves_others_intact(client: TestClient) -> None:
    r1 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    r2 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})
    assert r1.status_code == 200
    assert r2.status_code == 200
    id1 = r1.json()["record_id"]
    id2 = r2.json()["record_id"]

    client.delete(f"/v1/dossiers/{id1}")

    list_response = client.get("/v1/dossiers")
    assert list_response.status_code == 200
    dossier_ids = [d["dossier_id"] for d in list_response.json()["dossiers"]]
    assert id1 not in dossier_ids
    assert id2 in dossier_ids


# ---------------------------------------------------------------------------
# T8 — Double DELETE returns 404 on second call
# ---------------------------------------------------------------------------


def test_delete_twice_returns_404_on_second(
    client: TestClient, stored_dossier_id: str
) -> None:
    first = client.delete(f"/v1/dossiers/{stored_dossier_id}")
    assert first.status_code == 204
    second = client.delete(f"/v1/dossiers/{stored_dossier_id}")
    assert second.status_code == 404


# ---------------------------------------------------------------------------
# T9 — After DELETE all dossiers, list is empty
# ---------------------------------------------------------------------------


def test_delete_all_dossiers_empties_list(client: TestClient) -> None:
    r1 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    r2 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})
    id1 = r1.json()["record_id"]
    id2 = r2.json()["record_id"]

    client.delete(f"/v1/dossiers/{id1}")
    client.delete(f"/v1/dossiers/{id2}")

    list_response = client.get("/v1/dossiers")
    assert list_response.json()["dossiers"] == []


# ---------------------------------------------------------------------------
# T10 — DELETE response body is empty (204 No Content)
# ---------------------------------------------------------------------------


def test_delete_dossier_empty_response_body(
    client: TestClient, stored_dossier_id: str
) -> None:
    response = client.delete(f"/v1/dossiers/{stored_dossier_id}")
    assert response.status_code == 204
    assert response.content == b""
