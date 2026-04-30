"""Tests for MIG-008A minimal in-memory storage."""

import importlib

from lex_syndic.storage import InMemoryStore


def test_storage_package_importable() -> None:
    module = importlib.import_module("lex_syndic.storage")
    assert module is not None


def test_create_empty_store() -> None:
    store = InMemoryStore()

    assert store.list_keys() == []
    assert store.list_values() == []


def test_add_and_get_item() -> None:
    store = InMemoryStore()
    payload = {"kind": "document", "id": "doc-1"}

    store.add("doc-1", payload)

    assert store.get("doc-1") == payload


def test_get_unknown_key_returns_none() -> None:
    store = InMemoryStore()

    assert store.get("unknown") is None


def test_key_order_is_deterministic() -> None:
    store = InMemoryStore()
    store.add("b", 2)
    store.add("a", 1)

    assert store.list_keys() == ["b", "a"]


def test_value_order_is_deterministic() -> None:
    store = InMemoryStore()
    store.add("first", {"id": 1})
    store.add("second", {"id": 2})

    assert store.list_values() == [{"id": 1}, {"id": 2}]


def test_clear_resets_store() -> None:
    store = InMemoryStore()
    store.add("doc-1", "value")

    store.clear()

    assert store.list_keys() == []
    assert store.list_values() == []
    assert store.get("doc-1") is None


def test_storage_has_no_retrieval_dependency() -> None:
    import lex_syndic.storage.memory as memory_module

    public_names = [name for name in dir(memory_module) if "retrieval" in name.lower()]
    assert public_names == []
