"""
BETO Persistence Layer — v4.5

Transversal persistence layer for BETO_EXECUTOR. Manages SQLite storage
for cycles, routing decisions, snapshots, OQs, gate decisions, artifacts,
and model calls.

Connection rule: callers obtain a connection via get_connection(beto_dir)
and close it when done. No shared long-lived connection is propagated
through the system.
"""

from .connection import get_connection
from .schema import init_db

__all__ = ["get_connection", "init_db"]
