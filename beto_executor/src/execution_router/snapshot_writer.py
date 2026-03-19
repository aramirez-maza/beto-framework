"""
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

SnapshotWriter — BETO v4.4 context snapshot persistence.

Writes the four declared snapshot types to .beto/snapshots/:
  LC — LOCAL_EXECUTION_CONTEXT  (per paso, all routes)
  CS — CYCLE_CONTEXT_SNAPSHOT   (after paso 4, PARTIAL/FULL only)
  AQ — ACTIVE_OQ_SET            (after paso 6, PARTIAL/FULL only)
  MS — MATERIALIZATION_SCOPE    (after paso 9, PARTIAL/FULL only)

LIGHT path only generates LC snapshots — no Capa B.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


class SnapshotWriter:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

    Generates snapshot IDs for BETO v4.4 execution efficiency layer.
    One instance per cycle. Counters are per-prefix and per-instance.

    Phase 3: no longer writes snapshot JSON files.  ID generation and counter
    resume-safety are preserved; the caller (MotorRazonamiento._emit_snapshots)
    is responsible for writing each snapshot to SQLite via SnapshotDBWriter.
    """

    def __init__(self, beto_dir: Path, ciclo_id: str) -> None:
        # BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG (storage path OQ-2)
        # BETO-TRACE: BETO_V45.SEC8.DECISION.SNAPSHOT_COUNTER_RESUME_SAFE
        # BETO-TRACE: BETO_V45.SEC8.DECISION.SQLITE_SOLE_BACKEND
        self.beto_dir = beto_dir
        self.ciclo_id = ciclo_id
        # Initialize counters from SQLite so resumed cycles never reuse IDs.
        # Falls back to 0 if the DB is absent or the query fails.
        self._counters: dict[str, int] = {p: 0 for p in ("LC", "CS", "AQ", "MS")}
        db_path = beto_dir / "beto.db"
        if db_path.exists():
            try:
                from persistence.connection import get_connection
                conn = get_connection(beto_dir)
                try:
                    for prefix in ("LC", "CS", "AQ", "MS"):
                        rows = conn.execute(
                            "SELECT snapshot_id FROM snapshots "
                            "WHERE cycle_id = ? AND snapshot_id LIKE ?",
                            (ciclo_id, f"{prefix}-%"),
                        ).fetchall()
                        if rows:
                            max_n = max(
                                int(r["snapshot_id"].split("-")[-1])
                                for r in rows
                                if r["snapshot_id"].split("-")[-1].isdigit()
                            )
                            self._counters[prefix] = max_n
                finally:
                    conn.close()
            except Exception:
                pass  # Counters stay at 0 — safe for first use

    # ─── Public API ───────────────────────────────────────────────────────────

    def write_lc_snapshot(
        self,
        paso: int,
        artefactos: list[str],
        route_type: str,
    ) -> str:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

        LOCAL_EXECUTION_CONTEXT snapshot — written after every paso.
        All routes: LIGHT, PARTIAL, FULL.
        Returns snapshot_id.
        """
        sid = self._next_id("LC")
        return sid

    def write_cs_snapshot(
        self,
        paso: int,
        cycle_dir: Path,
        route_type: str,
    ) -> str:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

        CYCLE_CONTEXT_SNAPSHOT — written after paso 4 (Gate G-2).
        PARTIAL and FULL paths only.
        Returns snapshot_id.
        """
        sid = self._next_id("CS")
        return sid

    def write_aq_snapshot(
        self,
        paso: int,
        cycle_dir: Path,
        route_type: str,
    ) -> str:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

        ACTIVE_OQ_SET snapshot — written after paso 6 (cierre asistido).
        PARTIAL and FULL paths only.
        Returns snapshot_id.
        """
        sid = self._next_id("AQ")
        return sid

    def write_ms_snapshot(
        self,
        paso: int,
        cycle_dir: Path,
        route_type: str,
    ) -> str:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

        MATERIALIZATION_SCOPE snapshot — written after paso 9.
        PARTIAL and FULL paths only.
        Returns snapshot_id.
        """
        sid = self._next_id("MS")
        return sid

    # ─── Internal helpers ─────────────────────────────────────────────────────

    def _next_id(self, prefix: str) -> str:
        self._counters[prefix] += 1
        return f"{prefix}-{datetime.now(timezone.utc).year}-{self._counters[prefix]:04d}"
