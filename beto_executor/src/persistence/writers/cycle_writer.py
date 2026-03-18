"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.CYCLE_WRITER

Writes project and cycle records to SQLite.
Replaces the {ciclo_id}.json role as source of truth (Phase 2+).
In Phase 1: dual-write replica.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection


class CycleWriter:
    """Writes project and cycle state to the DB."""

    @staticmethod
    def ensure_project(beto_dir: Path, project_dir: Path) -> str:
        """
        Register the project if not already known. Returns project_id.
        project_id is a stable hash of the project_dir path.
        """
        project_id = hashlib.sha1(str(project_dir).encode()).hexdigest()[:16]
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO projects (project_id, project_dir, created_at, db_version)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        project_id,
                        str(project_dir),
                        datetime.now(timezone.utc).isoformat(),
                        "4.5.0",
                    ),
                )
        finally:
            conn.close()
        return project_id

    @staticmethod
    def write_cycle(
        beto_dir: Path,
        project_id: str,
        cycle_id: str,
        idea_raw: str,
        cycle_dir: Path,
        route_type: str = "",
        complexity_score: float | None = None,
        reasoning_model: str = "",
        code_model: str = "",
        g4_configured: bool = False,
    ) -> None:
        """
        Insert or update cycle record. Safe to call multiple times
        (ON CONFLICT updates mutable fields).
        """
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO cycles (
                        cycle_id, project_id, idea_raw, created_at,
                        status, paso_actual, route_type, complexity_score,
                        cycle_dir, reasoning_model, code_model, g4_configured, updated_at
                    ) VALUES (?, ?, ?, ?, 'IN_PROGRESS', 0, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(cycle_id) DO UPDATE SET
                        route_type       = excluded.route_type,
                        complexity_score = excluded.complexity_score,
                        updated_at       = excluded.updated_at
                    """,
                    (
                        cycle_id,
                        project_id,
                        idea_raw,
                        now,
                        route_type,
                        complexity_score,
                        str(cycle_dir),
                        reasoning_model,
                        code_model,
                        1 if g4_configured else 0,
                        now,
                    ),
                )
        finally:
            conn.close()

    @staticmethod
    def update_paso(beto_dir: Path, cycle_id: str, paso: int) -> None:
        """Update paso_actual for an in-progress cycle."""
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    "UPDATE cycles SET paso_actual = ?, updated_at = ? WHERE cycle_id = ?",
                    (paso, datetime.now(timezone.utc).isoformat(), cycle_id),
                )
        finally:
            conn.close()

    @staticmethod
    def mark_completed(beto_dir: Path, cycle_id: str) -> None:
        """Mark a cycle as COMPLETED."""
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    "UPDATE cycles SET status = 'COMPLETED', updated_at = ? WHERE cycle_id = ?",
                    (datetime.now(timezone.utc).isoformat(), cycle_id),
                )
        finally:
            conn.close()
