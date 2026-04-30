"""Deterministic in-memory lexical retrieval for MIG-007A."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import re
from typing import Iterable

from lex_syndic.legal.models import Clause, LegalDocument

_TOKEN_PATTERN = re.compile(r"[0-9A-Za-zÀ-ÿ]+", re.UNICODE)


@dataclass(frozen=True)
class RetrievalMatch:
    """One deterministic lexical retrieval result."""

    item_id: str
    item_type: str
    score: int
    matched_terms: tuple[str, ...]


@dataclass(frozen=True)
class _IndexedItem:
    item_id: str
    item_type: str
    position: int
    term_frequencies: Counter[str]


def _tokenize(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in _TOKEN_PATTERN.findall(text))


def _extract_item_metadata(item: LegalDocument | Clause) -> tuple[str, str, str]:
    if isinstance(item, LegalDocument):
        return item.document_id or "", "document", item.text
    if isinstance(item, Clause):
        return item.clause_id or "", "clause", item.content
    raise TypeError(f"Unsupported retrieval item type: {type(item)!r}")


class LexicalRetrievalIndex:
    """Minimal lexical retrieval index with deterministic ranking."""

    def __init__(self, items: Iterable[LegalDocument | Clause]) -> None:
        indexed_items: list[_IndexedItem] = []
        inverted_index: dict[str, list[int]] = defaultdict(list)

        for position, item in enumerate(items):
            item_id, item_type, text = _extract_item_metadata(item)
            term_frequencies = Counter(_tokenize(text))
            indexed_item = _IndexedItem(
                item_id=item_id,
                item_type=item_type,
                position=position,
                term_frequencies=term_frequencies,
            )
            indexed_items.append(indexed_item)
            for term in sorted(term_frequencies):
                inverted_index[term].append(position)

        self._items = tuple(indexed_items)
        self._inverted_index = {
            term: tuple(positions) for term, positions in inverted_index.items()
        }

    def search(self, query: str, limit: int | None = None) -> tuple[RetrievalMatch, ...]:
        query_terms = tuple(sorted(set(_tokenize(query))))
        if not query_terms:
            return ()

        candidate_positions: set[int] = set()
        for term in query_terms:
            candidate_positions.update(self._inverted_index.get(term, ()))

        if not candidate_positions:
            return ()

        results: list[RetrievalMatch] = []
        for position in sorted(candidate_positions):
            indexed_item = self._items[position]
            matched_terms = tuple(
                term for term in query_terms if indexed_item.term_frequencies.get(term, 0) > 0
            )
            score = sum(indexed_item.term_frequencies[term] for term in matched_terms)
            if score <= 0:
                continue
            results.append(
                RetrievalMatch(
                    item_id=indexed_item.item_id,
                    item_type=indexed_item.item_type,
                    score=score,
                    matched_terms=matched_terms,
                )
            )

        results.sort(
            key=lambda result: (
                -result.score,
                result.item_id,
                result.item_type,
            )
        )
        if limit is not None:
            results = results[:limit]
        return tuple(results)
