"""Acceptance tests for GET /v1/dossiers/{dossier_id}/status [LEX-043].

Proves end-to-end: POST /v1/analyze followed by GET /v1/dossiers/{id}/status
returns the correct lightweight juridical status of a dossier.
"""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from lex_syndic.api.fastapi_app import app

ACCORD_TEXT = """
ACCORD D'ENTREPRISE RELATIF À L'ORGANISATION DU TRAVAIL ET AU TEMPS DE REPOS

Entre la société DUPONT & ASSOCIÉS SAS, dont le siège social est situé
12 rue de la République, 75001 Paris, représentée par M. Jean Dupont,
Directeur Général, d'une part,

Et les organisations syndicales représentatives au sein de l'entreprise,
d'autre part,

Il a été convenu et arrêté ce qui suit :

Article 1 — Champ d'application
Le présent accord s'applique à l'ensemble des salariés de la société
DUPONT & ASSOCIÉS SAS, quelle que soit la nature de leur contrat de travail
(CDI, CDD, temps plein ou temps partiel), à l'exclusion des cadres dirigeants
au sens de l'article L. 3111-2 du Code du travail.

Article 2 — Durée du travail et aménagement du temps
La durée hebdomadaire de travail est fixée à trente-cinq heures pour
l'ensemble du personnel non-cadre. Les heures supplémentaires effectuées
au-delà de cette durée sont compensées conformément aux dispositions
légales en vigueur.

Article 3 — Durée et entrée en vigueur
Le présent accord est conclu pour une durée indéterminée. Il entre en vigueur
le 1er janvier 2026.

Fait à Paris, le 15 novembre 2025.
"""


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Scenario 1 — full end-to-end: analyze then query dossier status
# ---------------------------------------------------------------------------


def test_dossier_status_after_analyze(client: TestClient) -> None:
    """Submitting an accord then querying its dossier status returns 200
    with the correct juridical_status, alert_level, recommended_action."""
    post_response = client.post(
        "/v1/analyze",
        json={"text": ACCORD_TEXT, "title": "Accord DUPONT test"},
    )
    assert post_response.status_code == 200
    post_data = post_response.json()
    dossier_id = post_data["record_id"]
    assert dossier_id != ""

    status_response = client.get(f"/v1/dossiers/{dossier_id}/status")
    assert status_response.status_code == 200

    data = status_response.json()
    assert data["dossier_id"] == dossier_id
    assert data["juridical_status"] != ""
    assert data["alert_level"] != ""
    assert data["recommended_action"] != ""
    assert "report_text" not in data, "status endpoint must not expose report_text"


# ---------------------------------------------------------------------------
# Scenario 2 — status is consistent with the full result
# ---------------------------------------------------------------------------


def test_dossier_status_consistent_with_full_result(client: TestClient) -> None:
    """GET /v1/dossiers/{id}/status is a strict subset of GET /v1/results/{id}."""
    post_response = client.post("/v1/analyze", json={"text": ACCORD_TEXT})
    assert post_response.status_code == 200
    dossier_id = post_response.json()["record_id"]

    status_response = client.get(f"/v1/dossiers/{dossier_id}/status")
    result_response = client.get(f"/v1/results/{dossier_id}")

    assert status_response.status_code == 200
    assert result_response.status_code == 200

    status_data = status_response.json()
    result_data = result_response.json()

    assert status_data["juridical_status"] == result_data["decision_status"]
    assert status_data["alert_level"] == result_data["alert_level"]
    assert status_data["recommended_action"] == result_data["recommended_action"]


# ---------------------------------------------------------------------------
# Scenario 3 — unknown dossier_id returns 404 with detail
# ---------------------------------------------------------------------------


def test_dossier_status_not_found(client: TestClient) -> None:
    response = client.get("/v1/dossiers/dossier-unknown-9999/status")
    assert response.status_code == 404
    assert response.json()["detail"] == "dossier not found"


# ---------------------------------------------------------------------------
# Scenario 4 — multiple dossiers are independent
# ---------------------------------------------------------------------------


def test_multiple_dossiers_have_independent_statuses(client: TestClient) -> None:
    id1 = client.post("/v1/analyze", json={"text": ACCORD_TEXT}).json()["record_id"]
    id2 = client.post("/v1/analyze", json={"text": ACCORD_TEXT}).json()["record_id"]
    assert id1 != id2

    r1 = client.get(f"/v1/dossiers/{id1}/status")
    r2 = client.get(f"/v1/dossiers/{id2}/status")
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["dossier_id"] == id1
    assert r2.json()["dossier_id"] == id2
