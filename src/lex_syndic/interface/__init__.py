
"""Minimal interface API for MIG-010A."""

from .core import InterfaceRequest, InterfaceResponse, handle_request

__all__ = ["InterfaceRequest", "InterfaceResponse", "handle_request"]
