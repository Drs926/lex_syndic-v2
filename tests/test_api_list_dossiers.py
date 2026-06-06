"""Unit tests for GET /v1/dossiers — list dossiers endpoint [LEX-044]."""

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


# ---------------------------------------------------------------------------
# T1 — GET /v1/dossiers returns 200
# ---------------------------------------------------------------------------


def test_list_dossiers_returns_200(client: TestClient) -> None:
    response = client.get("/v1/dossiers")
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# T2 — Empty list when no dossier in memory
# ---------------------------------------------------------------------------


def test_list_dossiers_empty_when_no_record(client: TestClient) -> None:
    response = client.get("/v1/dossiers")
    assert response.status_code == 200
    data = response.json()
    assert "dossiers" in data
    assert data["dossiers"] == []


# ---------------------------------------------------------------------------
# T3 — After POST /v1/analyze, GET /v1/dossiers contains the dossier
# ---------------------------------------------------------------------------


def test_list_dossiers_contains_created_dossier(client: TestClient) -> None:
    post_response = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert post_response.status_code == 200
    record_id = post_response.json()["record_id"]

    list_response = client.get("/v1/dossiers")
    assert list_response.status_code == 200
    dossiers = list_response.json()["dossiers"]

    dossier_ids = [d["dossier_id"] for d in dossiers]
    assert record_id in dossier_ids


# ---------------------------------------------------------------------------
# T4 — Each item contains dossier_id, juridical_status, alert_level, recommended_action
# ---------------------------------------------------------------------------


def test_list_dossiers_item_shape(client: TestClient) -> None:
    client.post("/v1/analyze", json={"text": SAMPLE_TEXT})

    response = client.get("/v1/dossiers")
    assert response.status_code == 200
    dossiers = response.json()["dossiers"]
    assert len(dossiers) >= 1

    required_keys = {"dossier_id", "juridical_status", "alert_level", "recommended_action"}
    for item in dossiers:
        assert required_keys.issubset(item.keys()), (
            f"Missing keys in item {item}. Expected {required_keys}, got {set(item.keys())}"
        )


# ---------------------------------------------------------------------------
# T5 — report_text is absent from every item
# ---------------------------------------------------------------------------


def test_list_dossiers_no_report_text(client: TestClient) -> None:
    client.post("/v1/analyze", json={"text": SAMPLE_TEXT})

    response = client.get("/v1/dossiers")
    assert response.status_code == 200
    for item in response.json()["dossiers"]:
        assert "report_text" not in item, (
            "report_text must not be exposed by GET /v1/dossiers"
        )


# ---------------------------------------------------------------------------
# T6 — Consistency with GET /v1/dossiers/{dossier_id}/status
# ---------------------------------------------------------------------------


def test_list_dossiers_consistent_with_status_endpoint(client: TestClient) -> None:
    post_response = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    assert post_response.status_code == 200
    dossier_id = post_response.json()["record_id"]

    list_response = client.get("/v1/dossiers")
    assert list_response.status_code == 200
    dossier_item = next(
        (d for d in list_response.json()["dossiers"] if d["dossier_id"] == dossier_id),
        None,
    )
    assert dossier_item is not None

    status_response = client.get(f"/v1/dossiers/{dossier_id}/status")
    assert status_response.status_code == 200
    status_data = status_response.json()

    assert dossier_item["juridical_status"] == status_data["juridical_status"]
    assert dossier_item["alert_level"] == status_data["alert_level"]
    assert dossier_item["recommended_action"] == status_data["recommended_action"]


# ---------------------------------------------------------------------------
# T7 — Multiple dossiers are listed independently
# ---------------------------------------------------------------------------


def test_list_dossiers_multiple_independent(client: TestClient) -> None:
    r1 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    r2 = client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})
    assert r1.status_code == 200
    assert r2.status_code == 200

    id1 = r1.json()["record_id"]
    id2 = r2.json()["record_id"]
    assert id1 != id2

    list_response = client.get("/v1/dossiers")
    assert list_response.status_code == 200
    dossiers = list_response.json()["dossiers"]
    dossier_ids = [d["dossier_id"] for d in dossiers]

    assert id1 in dossier_ids
    assert id2 in dossier_ids
    assert len(dossiers) == 2


# ---------------------------------------------------------------------------
# T8 — Count grows with each analysis
# ---------------------------------------------------------------------------


def test_list_dossiers_count_grows(client: TestClient) -> None:
    list_0 = client.get("/v1/dossiers")
    assert list_0.json()["dossiers"] == []

    client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
    list_1 = client.get("/v1/dossiers")
    assert len(list_1.json()["dossiers"]) == 1

    client.post("/v1/analyze", json={"text": SAMPLE_TEXT_2})
    list_2 = client.get("/v1/dossiers")
    assert len(list_2.json()["dossiers"]) == 2


# ---------------------------------------------------------------------------
# T9 — Response root key is "dossiers" (not "results" or "records")
# ---------------------------------------------------------------------------


def test_list_dossiers_root_key_is_dossiers(client: TestClient) -> None:
    response = client.get("/v1/dossiers")
    assert response.status_code == 200
    data = response.json()
    assert "dossiers" in data
    assert "results" not in data
    assert "records" not in data


# ---------------------------------------------------------------------------
# T10 — dossier_id values match record_id returned by analyze
# ---------------------------------------------------------------------------


def test_list_dossiers_ids_match_analyze_record_ids(client: TestClient) -> None:
    record_ids = set()
    for _ in range(3):
        r = client.post("/v1/analyze", json={"text": SAMPLE_TEXT})
        assert r.status_code == 200
        record_ids.add(r.json()["record_id"])

    list_response = client.get("/v1/dossiers")
    assert list_response.status_code == 200
    listed_ids = {d["dossier_id"] for d in list_response.json()["dossiers"]}

    assert record_ids == listed_ids
