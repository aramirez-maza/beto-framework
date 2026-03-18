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

import json
from datetime import datetime, timezone
from pathlib import Path


class SnapshotWriter:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

    Writes context snapshots for BETO v4.4 execution efficiency layer.
    One instance per cycle. Counters are per-prefix and per-instance.
    """

    def __init__(self, beto_dir: Path, ciclo_id: str) -> None:
        # BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG (storage path OQ-2)
        # BETO-TRACE: BETO_V45.SEC8.DECISION.SNAPSHOT_COUNTER_RESUME_SAFE
        self.beto_dir = beto_dir
        self.ciclo_id = ciclo_id
        self.snapshots_dir = beto_dir / "snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        # Initialize counters from existing files so resumed cycles never reuse IDs.
        # E.g. if LC-2026-0003.json exists, the next LC counter starts at 4.
        self._counters: dict[str, int] = {}
        for prefix in ("LC", "CS", "AQ", "MS"):
            existing = list(self.snapshots_dir.glob(f"{prefix}-*.json"))
            if existing:
                max_n = max(
                    int(f.stem.split("-")[-1])
                    for f in existing
                    if f.stem.split("-")[-1].isdigit()
                )
                self._counters[prefix] = max_n
            else:
                self._counters[prefix] = 0

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
        self._write(sid, {
            "snapshot_id": sid,
            "snapshot_type": "LOCAL_EXECUTION_CONTEXT",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ciclo_id": self.ciclo_id,
            "paso": paso,
            "route_type": route_type,
            "artifacts_generated": artefactos,
            "validity_state": "VALID",
        })
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
        artifacts = sorted(f.name for f in cycle_dir.glob("*.md") if f.is_file())
        self._write(sid, {
            "snapshot_id": sid,
            "snapshot_type": "CYCLE_CONTEXT_SNAPSHOT",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ciclo_id": self.ciclo_id,
            "paso": paso,
            "route_type": route_type,
            "artifacts_in_scope": artifacts,
            "beto_state_captured": (cycle_dir / "BETO_STATE.json").exists(),
            "validity_state": "VALID",
        })
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
        oqs_abiertas: list = []
        beto_state_path = cycle_dir / "BETO_STATE.json"
        if beto_state_path.exists():
            try:
                state = json.loads(beto_state_path.read_text(encoding="utf-8"))
                oqs_abiertas = state.get("oqs_abiertas", [])
            except Exception:
                pass
        self._write(sid, {
            "snapshot_id": sid,
            "snapshot_type": "ACTIVE_OQ_SET",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ciclo_id": self.ciclo_id,
            "paso": paso,
            "route_type": route_type,
            "oqs_abiertas_count": len(oqs_abiertas),
            "oqs_abiertas": oqs_abiertas,
            "validity_state": "VALID",
        })
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
        artifacts = sorted(f.name for f in cycle_dir.glob("*.md") if f.is_file())
        self._write(sid, {
            "snapshot_id": sid,
            "snapshot_type": "MATERIALIZATION_SCOPE",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ciclo_id": self.ciclo_id,
            "paso": paso,
            "route_type": route_type,
            "scope_artifacts": artifacts,
            "manifest_present": (cycle_dir / "MANIFEST_PROYECTO.md").exists(),
            "validity_state": "VALID",
        })
        return sid

    # ─── Internal helpers ─────────────────────────────────────────────────────

    def _next_id(self, prefix: str) -> str:
        self._counters[prefix] += 1
        return f"{prefix}-{datetime.now(timezone.utc).year}-{self._counters[prefix]:04d}"

    def _write(self, snapshot_id: str, data: dict) -> None:
        path = self.snapshots_dir / f"{snapshot_id}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
