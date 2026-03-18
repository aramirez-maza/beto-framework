"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.QUERY_LAYER

Common read queries for BETO SQLite persistence.
All functions follow the same pattern:
  - Accept beto_dir as first argument
  - Open connection, query, close connection
  - Return plain Python dicts/lists (not sqlite3.Row objects)
"""

from pathlib import Path

from .connection import get_connection


def get_cycle(beto_dir: Path, cycle_id: str) -> dict | None:
    """Return the cycle record or None if not found."""
    conn = get_connection(beto_dir)
    try:
        row = conn.execute(
            "SELECT * FROM cycles WHERE cycle_id = ?", (cycle_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_open_oqs(beto_dir: Path, cycle_id: str, critical_only: bool = False) -> list[dict]:
    """Return all open OQs for a cycle, optionally filtered to critical only."""
    sql = "SELECT * FROM open_questions WHERE cycle_id = ? AND estado = 'ABIERTA'"
    params: list = [cycle_id]
    if critical_only:
        sql += " AND critical = 1"
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_closed_oqs(beto_dir: Path, cycle_id: str) -> list[dict]:
    """Return all closed OQs with their resolution mode."""
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT * FROM open_questions WHERE cycle_id = ? AND estado = 'CERRADA'",
            (cycle_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_active_snapshots(beto_dir: Path, cycle_id: str) -> list[dict]:
    """Return all valid (non-invalidated) snapshots for a cycle."""
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            """
            SELECT snapshot_id, snapshot_type, paso, route_type, created_at
            FROM snapshots
            WHERE cycle_id = ? AND validity_state = 'VALID'
            ORDER BY paso, snapshot_type
            """,
            (cycle_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_routing_decisions(beto_dir: Path, cycle_id: str) -> list[dict]:
    """Return all routing decisions for a cycle in order."""
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT * FROM routing_decisions WHERE cycle_id = ? ORDER BY created_at",
            (cycle_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_artifacts(beto_dir: Path, cycle_id: str, route_relevance: str | None = None) -> list[dict]:
    """
    Return artifacts for a cycle, optionally filtered by route_relevance.
    Pass route_relevance='ALL_ROUTES' to exclude LIGHT_ONLY artifacts.
    """
    sql = "SELECT * FROM artifacts WHERE cycle_id = ?"
    params: list = [cycle_id]
    if route_relevance:
        sql += " AND route_relevance = ?"
        params.append(route_relevance)
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_gate_decisions(beto_dir: Path, cycle_id: str) -> list[dict]:
    """Return all gate decisions for a cycle."""
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT * FROM gate_decisions WHERE cycle_id = ? ORDER BY decided_at",
            (cycle_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_all_cycles(beto_dir: Path) -> list[dict]:
    """Return all cycles across all projects (for cross-cycle querying)."""
    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT cycle_id, idea_raw, status, route_type, complexity_score, created_at FROM cycles ORDER BY created_at"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
