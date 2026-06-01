"""Minimal in-memory store for LegalAnalysisWithReportResponse [LEX-026]."""

from __future__ import annotations

from lex_syndic.interface.report_handler import LegalAnalysisWithReportResponse


class InMemoryLegalResultStore:
    """Session-scoped store for legal analysis results. No disk writes."""

    def __init__(self) -> None:
        self._records: dict[str, LegalAnalysisWithReportResponse] = {}
        self._counter: int = 0

    def save(self, result: LegalAnalysisWithReportResponse) -> str:
        self._counter += 1
        record_id = f"result-{self._counter:04d}"
        self._records[record_id] = result
        return record_id

    def get(self, record_id: str) -> LegalAnalysisWithReportResponse | None:
        return self._records.get(record_id)

    def list_ids(self) -> tuple[str, ...]:
        return tuple(self._records.keys())

    def clear(self) -> None:
        self._records.clear()
        self._counter = 0
