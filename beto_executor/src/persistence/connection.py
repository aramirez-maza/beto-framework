"""
BETO-TRACE: BETO_V45.SEC8.DECISION.SQLITE_CONNECTION_PER_OPERATION

Connection factory for BETO SQLite persistence.

Rule: callers obtain a connection, use it, and close it.
No shared long-lived connection is propagated through the system.
This avoids threading issues and lifecycle fragility.
"""

import sqlite3
from pathlib import Path


def get_connection(beto_dir: Path) -> sqlite3.Connection:
    """
    Open and return a SQLite connection to beto_dir/beto.db.

    Settings applied:
      - WAL journal mode: safe concurrent reads while executor writes
      - Foreign keys: enforced
      - Row factory: sqlite3.Row for dict-like access

    Caller is responsible for closing the connection.
    Use as a context manager for automatic transaction handling:

        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(...)
        finally:
            conn.close()
    """
    db_path = beto_dir / "beto.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
