"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.OQ_WRITER

Syncs Open Questions from BETO_STATE.json to SQLite after each paso update.
In Phase 1: SQLite is a replica. In Phase 2: SQLite becomes the source of truth.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection


class OQWriter:
    """Syncs OQ state from BETO_STATE.json into the open_questions table."""

    def __init__(self, beto_dir: Path, cycle_id: str) -> None:
        self.beto_dir = beto_dir
        self.cycle_id = cycle_id

    def sync_from_beto_state(self, beto_state_path: Path, paso: int) -> int:
        """
        Read OQs from the just-written BETO_STATE.json and upsert to DB.
        Returns the number of OQ rows upserted.

        Uses INSERT OR REPLACE so successive calls are idempotent.
        """
        if not beto_state_path.exists():
            return 0

        try:
            state = json.loads(beto_state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return 0

        oqs_abiertas = state.get("oqs_abiertas", [])
        oqs_cerradas = state.get("oqs_cerradas", [])
        count = 0

        conn = get_connection(self.beto_dir)
        try:
            with conn:
                for oq in oqs_abiertas:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO open_questions (
                            oq_id, cycle_id, texto, oq_type, critical,
                            estado, modo_cierre, resolucion,
                            execution_state, readiness_check, requestion_count,
                            paso_registrada, paso_cerrada
                        ) VALUES (?, ?, ?, ?, ?, 'ABIERTA', NULL, NULL, ?, ?, ?, ?, NULL)
                        """,
                        (
                            oq.get("id", ""),
                            self.cycle_id,
                            oq.get("texto", ""),
                            oq.get("oq_type", "NOT_CLASSIFIED"),
                            1 if oq.get("critical") else 0,
                            oq.get("execution_state", "PENDING"),
                            oq.get("execution_readiness_check", "NOT_EVALUATED"),
                            oq.get("requestion_count", 0),
                            paso,
                        ),
                    )
                    count += 1

                for oq in oqs_cerradas:
                    conn.execute(
                        """
                        INSERT OR REPLACE INTO open_questions (
                            oq_id, cycle_id, texto, oq_type, critical,
                            estado, modo_cierre, resolucion,
                            execution_state, readiness_check, requestion_count,
                            paso_registrada, paso_cerrada
                        ) VALUES (?, ?, ?, ?, ?, 'CERRADA', ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            oq.get("id", ""),
                            self.cycle_id,
                            oq.get("texto", ""),
                            oq.get("oq_type", "NOT_CLASSIFIED"),
                            1 if oq.get("critical") else 0,
                            oq.get("modo_cierre", ""),
                            oq.get("resolucion", ""),
                            oq.get("execution_state", "PENDING"),
                            oq.get("execution_readiness_check", "NOT_EVALUATED"),
                            oq.get("requestion_count", 0),
                            paso,  # paso_registrada — best estimate for closed OQs
                            paso,  # paso_cerrada
                        ),
                    )
                    count += 1
        finally:
            conn.close()

        return count
