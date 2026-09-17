"""Acceptance tests for the complete dossier deletion lifecycle [LEX-048]."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from lex_syndic.api.fastapi_app import app

PRIMARY_TEXT = (
    "Accord d'entreprise relatif au télétravail. "
    "Article 1 : Le télétravail est mis en place conformément aux dispositions légales. "
    "Article 2 : Les salariés peuvent exercer leurs fonctions en télétravail deux jours par semaine."
)

SECONDARY_TEXT = (
    "Contrat de travail à durée déterminée. "
    "Article 1 : Le présent contrat est conclu pour une durée de six mois. "
    "Article 2 : La rémunération mensuelle brute est fixée à 2500 euros."
)


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def _analyze(client: TestClient, text: str, title: str) -> str:
    response = client.post("/v1/analyze", json={"text": text, "title": title})
    assert response.status_code == 200
    record_id = response.json()["record_id"]
    assert record_id
    return record_id


def _listed_ids(client: TestClient) -> set[str]:
    response = client.get("/v1/dossiers")
    assert response.status_code == 200
    return {item["dossier_id"] for item in response.json()["dossiers"]}


def test_delete_dossier_end_to_end_preserves_other_dossier(client: TestClient) -> None:
    target_id = _analyze(client, PRIMARY_TEXT, "Accord télétravail")
    survivor_id = _analyze(client, SECONDARY_TEXT, "Contrat CDD")
    assert target_id != survivor_id

    before_ids = _listed_ids(client)
    assert target_id in before_ids
    assert survivor_id in before_ids
    assert client.get(f"/v1/dossiers/{target_id}/status").status_code == 200
    assert client.get(f"/v1/results/{target_id}").status_code == 200

    delete_response = client.delete(f"/v1/dossiers/{target_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    after_ids = _listed_ids(client)
    assert target_id not in after_ids
    assert survivor_id in after_ids

    deleted_status = client.get(f"/v1/dossiers/{target_id}/status")
    assert deleted_status.status_code == 404
    assert deleted_status.json()["detail"] == "dossier not found"

    deleted_result = client.get(f"/v1/results/{target_id}")
    assert deleted_result.status_code == 404
    assert deleted_result.json()["detail"] == "record not found"

    assert client.get(f"/v1/dossiers/{survivor_id}/status").status_code == 200
    assert client.get(f"/v1/results/{survivor_id}").status_code == 200


def test_client_lifespan_starts_with_empty_store(client: TestClient) -> None:
    assert _listed_ids(client) == set()
