"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.GATE_WRITER

Writes gate decisions to SQLite.
Hook integration deferred to Phase 2 (requires changes to gates_operador/gates.py).
Writer is declared here so it can be called when ready.
"""

from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection


class GateWriter:
    """Writes human gate decisions (G-1, G-2, G-2B, G-3, G-4) to SQLite."""

    @staticmethod
    def write(
        beto_dir: Path,
        cycle_id: str,
        gate: str,
        decision: str,
        paso: int,
        operator_notes: str = "",
    ) -> None:
        """
        Insert a gate decision record.

        gate: 'G-1' | 'G-2' | 'G-2B' | 'G-3' | 'G-4'
        decision: 'APPROVED' | 'APPROVED_WITH_LIMITS' | 'REJECTED'
        """
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO gate_decisions (
                        cycle_id, gate, decision, paso, operator_notes, decided_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cycle_id,
                        gate,
                        decision,
                        paso,
                        operator_notes,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
        finally:
            conn.close()
