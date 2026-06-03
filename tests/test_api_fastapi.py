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
