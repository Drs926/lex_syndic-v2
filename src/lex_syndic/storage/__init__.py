
"""Minimal storage API for MIG-008A."""

from .memory import InMemoryStore
from .legal_results import InMemoryLegalResultStore

__all__ = ["InMemoryStore", "InMemoryLegalResultStore"]
