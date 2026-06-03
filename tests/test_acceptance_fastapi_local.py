"""Acceptance tests for the FastAPI local HTTP API [LEX-035].

Proves end-to-end behaviour of the FastAPI app defined in LEX-034:
- health check
- analysis of a realistic French accord d'entreprise
- retrieval of a stored result by record_id
- doc routes are not exposed
- validation rejects empty / whitespace-only text
"""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from lex_syndic.api.fastapi_app import app

# ---------------------------------------------------------------------------
# Realistic French legal text — accord d'entreprise with >= 3 articles
# ---------------------------------------------------------------------------
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
légales en vigueur. Un planning prévisionnel mensuel est communiqué aux
salariés au moins deux semaines à l'avance afin de garantir une organisation
optimale des équipes.

Article 3 — Repos quotidien et hebdomadaire
Conformément aux articles L. 3131-1 et L. 3132-1 du Code du travail, chaque
salarié bénéficie d'un repos quotidien d'au moins onze heures consécutives
et d'un repos hebdomadaire d'au moins vingt-quatre heures consécutives
auxquelles s'ajoutent les onze heures de repos quotidien. Aucune dérogation
à ces dispositions ne peut être accordée sans l'accord préalable de
l'inspection du travail compétente.

Article 4 — Durée et entrée en vigueur
Le présent accord est conclu pour une durée indéterminée. Il entre en vigueur
le 1er janvier 2026 et peut être révisé ou dénoncé dans les conditions prévues
par le Code du travail.

Fait à Paris, le 15 novembre 2025.

Pour la société DUPONT & ASSOCIÉS SAS :   M. Jean Dupont, Directeur Général
Pour le syndicat CGT :                    Mme Marie Martin, Déléguée syndicale
Pour le syndicat CFDT :                   M. Paul Bernard, Délégué syndical
"""


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# Scenario 1 — health check
# ---------------------------------------------------------------------------

def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Scenario 2 — POST /v1/analyze with realistic accord d'entreprise
# ---------------------------------------------------------------------------

def test_analyze_accord_returns_required_fields(client: TestClient) -> None:
    assert len(ACCORD_TEXT) >= 200, "ACCORD_TEXT must be at least 200 chars"

    response = client.post("/v1/analyze", json={"text": ACCORD_TEXT})
    assert response.status_code == 200

    data = response.json()
    assert "record_id" in data
    assert "decision_status" in data
    assert "alert_level" in data
    assert "report_text" in data
    assert "recommended_action" in data

    assert data["record_id"] != "", "record_id must be non-empty"
    assert data["decision_status"] != "", "decision_status must be non-empty"
    assert data["report_text"] != "", "report_text must be non-empty"


# ---------------------------------------------------------------------------
# Scenario 3 — GET /v1/results/{record_id} after POST /v1/analyze
# ---------------------------------------------------------------------------

def test_get_result_matches_analyze_response(client: TestClient) -> None:
    post_response = client.post("/v1/analyze", json={"text": ACCORD_TEXT})
    assert post_response.status_code == 200
    post_data = post_response.json()
    record_id = post_data["record_id"]

    get_response = client.get(f"/v1/results/{record_id}")
    assert get_response.status_code == 200

    get_data = get_response.json()
    assert get_data["record_id"] == record_id
    assert "decision_status" in get_data
    assert "alert_level" in get_data
    assert "report_text" in get_data
    assert "recommended_action" in get_data


# ---------------------------------------------------------------------------
# Scenario 4 — doc routes must return 404
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
def test_doc_routes_not_exposed(client: TestClient, path: str) -> None:
    response = client.get(path)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Scenario 5 — empty / whitespace-only text returns 422
# ---------------------------------------------------------------------------

def test_analyze_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": ""})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_analyze_whitespace_only_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": "   \t\n  "})
    assert response.status_code == 422
    assert "detail" in response.json()
