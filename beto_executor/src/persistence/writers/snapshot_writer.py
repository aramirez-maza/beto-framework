"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.SNAPSHOT_WRITER

Dual-write for context snapshots (LC, CS, AQ, MS).
Called from MotorRazonamiento._emit_snapshots() alongside the existing
execution_router.snapshot_writer JSON writes.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection


class SnapshotDBWriter:
    """Writes snapshots to SQLite alongside the existing JSON snapshot writer."""

    def __init__(self, beto_dir: Path, cycle_id: str) -> None:
        self.beto_dir = beto_dir
        self.cycle_id = cycle_id

    def write(
        self,
        snapshot_id: str,
        snapshot_type: str,
        paso: int,
        route_type: str,
        payload: dict,
    ) -> None:
        """
        Persist a snapshot record to the snapshots table.

        snapshot_id: e.g. 'LC-2026-0001'  (matches the JSON filename stem)
        snapshot_type: LOCAL_EXECUTION_CONTEXT | CYCLE_CONTEXT_SNAPSHOT |
                       ACTIVE_OQ_SET | MATERIALIZATION_SCOPE
        payload: the same dict written to the JSON snapshot file
        """
        conn = get_connection(self.beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO snapshots (
                        snapshot_id, cycle_id, snapshot_type, paso,
                        route_type, validity_state, payload, created_at
                    ) VALUES (?, ?, ?, ?, ?, 'VALID', ?, ?)
                    """,
                    (
                        snapshot_id,
                        self.cycle_id,
                        snapshot_type,
                        paso,
                        route_type,
                        json.dumps(payload, ensure_ascii=False),
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
        finally:
            conn.close()

    def invalidate(self, snapshot_id: str, invalidated_by: str) -> None:
        """Mark a snapshot as INVALIDATED (e.g. after a route promotion)."""
        conn = get_connection(self.beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    UPDATE snapshots
                    SET validity_state = 'INVALIDATED',
                        invalidated_at = ?,
                        invalidated_by = ?
                    WHERE snapshot_id = ?
                    """,
                    (
                        datetime.now(timezone.utc).isoformat(),
                        invalidated_by,
                        snapshot_id,
                    ),
                )
        finally:
            conn.close()
