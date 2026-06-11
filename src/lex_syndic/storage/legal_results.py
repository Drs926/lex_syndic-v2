"""Generic in-memory store for legal analysis results [LEX-026 / LEX-032 / LEX-047].

Storage is intentionally decoupled from interface types (DEC-039).
The caller is responsible for storing and retrieving correctly typed objects.
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryLegalResultStore(Generic[T]):
    """Session-scoped generic store. No disk writes. No interface dependency."""

    def __init__(self) -> None:
        self._records: dict[str, T] = {}
        self._counter: int = 0

    def save(self, result: T) -> str:
        self._counter += 1
        record_id = f"result-{self._counter:04d}"
        self._records[record_id] = result
        return record_id

    def get(self, record_id: str) -> T | None:
        return self._records.get(record_id)

    def list_ids(self) -> tuple[str, ...]:
        return tuple(self._records.keys())

    def delete(self, record_id: str) -> bool:
        """Remove a record by id. Returns True if deleted, False if not found."""
        if record_id in self._records:
            del self._records[record_id]
            return True
        return False

    def clear(self) -> None:
        self._records.clear()
        self._counter = 0
