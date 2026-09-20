"""HTTP error contract tests for FastAPI v1 [LEX-050]."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from lex_syndic.api.fastapi_app import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_analyze_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": ""})

    assert response.status_code == 422
    assert response.json() == {"detail": "text must not be empty"}


def test_analyze_whitespace_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": " \t\r\n "})

    assert response.status_code == 422
    assert response.json() == {"detail": "text must not be empty"}


def test_analyze_too_long_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/analyze", json={"text": "a" * 50001})

    assert response.status_code == 422
    assert response.json() == {"detail": "text exceeds maximum length"}


def test_result_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/v1/results/unknown-record")

    assert response.status_code == 404
    assert response.json() == {"detail": "record not found"}


def test_dossier_status_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/v1/dossiers/unknown-dossier/status")

    assert response.status_code == 404
    assert response.json() == {"detail": "dossier not found"}


def test_dossier_delete_not_found_returns_404(client: TestClient) -> None:
    response = client.delete("/v1/dossiers/unknown-dossier")

    assert response.status_code == 404
    assert response.json() == {"detail": "dossier not found"}


def test_analyze_unexpected_submit_analysis_exception_returns_500(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    internal_message = "database credentials leaked in exception"

    def raise_unexpected_error(*args: object, **kwargs: object) -> object:
        raise RuntimeError(internal_message)

    monkeypatch.setattr(
        "lex_syndic.api.fastapi_app.submit_analysis",
        raise_unexpected_error,
    )

    response = client.post("/v1/analyze", json={"text": "Article 1 : contenu."})

    assert response.status_code == 500
    assert response.json() == {"detail": "internal error"}
    assert internal_message not in response.text
