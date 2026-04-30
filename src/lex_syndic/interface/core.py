"""Deterministic local interface helpers for MIG-010A."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class InterfaceRequest:
    """One minimal structured interface request."""

    query: str = ""
    payload: dict[str, object] | None = None


@dataclass(frozen=True)
class InterfaceResponse:
    """One minimal structured interface response."""

    status: str = ""
    message: str = ""
    data: dict[str, object] = field(default_factory=dict)


def handle_request(request: InterfaceRequest) -> InterfaceResponse:
    """Handle a request locally with deterministic output."""

    normalized_query = request.query.strip()
    normalized_payload = dict(request.payload or {})

    if not normalized_query:
        return InterfaceResponse(
            status="empty",
            message="empty query",
            data={"query": "", "payload": normalized_payload},
        )

    return InterfaceResponse(
        status="ok",
        message="request accepted",
        data={"query": normalized_query, "payload": normalized_payload},
    )
