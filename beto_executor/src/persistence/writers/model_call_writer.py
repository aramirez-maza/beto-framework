"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.MODEL_CALL_WRITER

Writes model call records to SQLite.
Hook integration deferred to Phase 2 (requires changes to step_executor.py).
Writer is declared here so it can be called when ready.
"""

from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection


class ModelCallWriter:
    """Writes LLM model call records to SQLite."""

    @staticmethod
    def write(
        beto_dir: Path,
        cycle_id: str,
        paso: int,
        call_type: str,
        model_used: str,
        call_label: str = "",
        route_type: str = "",
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        latency_ms: int | None = None,
        started_at: str | None = None,
        completed_at: str | None = None,
    ) -> int:
        """
        Insert a model call record. Returns the new row id.

        call_type: 'REASONING' | 'CODE'
        """
        now = datetime.now(timezone.utc).isoformat()
        conn = get_connection(beto_dir)
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO model_calls (
                        cycle_id, paso, call_type, model_used,
                        input_tokens, output_tokens, latency_ms,
                        route_type, call_label, started_at, completed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cycle_id,
                        paso,
                        call_type,
                        model_used,
                        input_tokens,
                        output_tokens,
                        latency_ms,
                        route_type,
                        call_label,
                        started_at or now,
                        completed_at,
                    ),
                )
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def complete(
        beto_dir: Path,
        row_id: int,
        input_tokens: int | None = None,
        output_tokens: int | None = None,
        latency_ms: int | None = None,
    ) -> None:
        """Update a model call record with completion data."""
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    UPDATE model_calls
                    SET input_tokens  = COALESCE(?, input_tokens),
                        output_tokens = COALESCE(?, output_tokens),
                        latency_ms    = COALESCE(?, latency_ms),
                        completed_at  = ?
                    WHERE id = ?
                    """,
                    (
                        input_tokens,
                        output_tokens,
                        latency_ms,
                        datetime.now(timezone.utc).isoformat(),
                        row_id,
                    ),
                )
        finally:
            conn.close()
