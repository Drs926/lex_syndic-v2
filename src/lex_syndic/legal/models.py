"""Canonical legal model placeholders for LEX_SYNDIC_V2."""

from dataclasses import dataclass
from typing import Optional

@dataclass
class LegalDocument:
    document_id: Optional[str] = None

@dataclass
class Clause:
    clause_id: Optional[str] = None

@dataclass
class LegalReference:
    reference_id: Optional[str] = None

@dataclass
class ComparisonResult:
    result_id: Optional[str] = None

