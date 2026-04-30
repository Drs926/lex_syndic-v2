"""Deterministic in-memory storage for MIG-008A."""

from __future__ import annotations


class InMemoryStore:
    """Minimal key/value store with stable insertion order."""

    def __init__(self) -> None:
        self._items: dict[str, object] = {}

    def add(self, key: str, value: object) -> None:
        self._items[key] = value

    def get(self, key: str) -> object | None:
        return self._items.get(key)

    def list_keys(self) -> list[str]:
        return list(self._items.keys())

    def list_values(self) -> list[object]:
        return list(self._items.values())

    def clear(self) -> None:
        self._items.clear()
