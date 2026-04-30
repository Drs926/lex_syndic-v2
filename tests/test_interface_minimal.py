"""Tests for MIG-010A minimal interface module."""

import importlib

from lex_syndic.interface import InterfaceRequest, InterfaceResponse, handle_request


def test_interface_package_importable() -> None:
    module = importlib.import_module("lex_syndic.interface")
    assert module is not None


def test_create_minimal_request() -> None:
    request = InterfaceRequest(query="analyse")

    assert request.query == "analyse"
    assert request.payload is None


def test_create_minimal_response() -> None:
    response = InterfaceResponse(status="ok", message="request accepted")

    assert response.status == "ok"
    assert response.message == "request accepted"
    assert response.data == {}


def test_handle_empty_request_returns_stable_response() -> None:
    response = handle_request(InterfaceRequest())

    assert response == InterfaceResponse(
        status="empty",
        message="empty query",
        data={"query": "", "payload": {}},
    )


def test_handle_non_empty_request_returns_stable_response() -> None:
    response = handle_request(
        InterfaceRequest(query="  analyse  ", payload={"kind": "demo"})
    )

    assert response == InterfaceResponse(
        status="ok",
        message="request accepted",
        data={"query": "analyse", "payload": {"kind": "demo"}},
    )


def test_response_status_is_deterministic() -> None:
    request = InterfaceRequest(query="analyse")

    assert handle_request(request).status == "ok"
    assert handle_request(request).status == "ok"


def test_response_message_is_deterministic() -> None:
    request = InterfaceRequest(query="")

    assert handle_request(request).message == "empty query"
    assert handle_request(request).message == "empty query"


def test_response_data_is_stable() -> None:
    request = InterfaceRequest(query="demo", payload={"b": 2, "a": 1})

    assert handle_request(request).data == {
        "query": "demo",
        "payload": {"b": 2, "a": 1},
    }


def test_interface_module_has_no_retrieval_dependency() -> None:
    import lex_syndic.interface.core as core_module

    public_names = [name for name in dir(core_module) if "retrieval" in name.lower()]
    assert public_names == []


def test_interface_module_has_no_storage_dependency() -> None:
    import lex_syndic.interface.core as core_module

    public_names = [name for name in dir(core_module) if "storage" in name.lower()]
    assert public_names == []


def test_interface_module_has_no_report_dependency() -> None:
    import lex_syndic.interface.core as core_module

    public_names = [name for name in dir(core_module) if "report" in name.lower()]
    assert public_names == []
