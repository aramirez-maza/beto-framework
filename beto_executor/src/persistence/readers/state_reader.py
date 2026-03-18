"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC7.PHASE.PHASE_2_STATE_READER

build_state_payload — canonical assembler for BETO_STATE.json Phase 2 format.

Reads from SQLite and returns a dict that represents the authoritative cycle
state.  Includes legacy aliases (ciclo_id, paso_actual, oqs_abiertas, etc.)
so that context_builder.py and _load_or_create() continue to work unchanged.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection
from persistence.queries import (
    get_cycle,
    get_open_oqs,
    get_closed_oqs,
    get_active_snapshots,
    get_routing_decisions,
    get_route_promotions,
    get_artifacts,
    get_latest_gates,
)
from persistence.schema import SCHEMA_VERSION


# ─── OQ row → legacy-compatible dict ─────────────────────────────────────────

def _oq_row_to_legacy(row: dict) -> dict:
    """Convert a DB row from open_questions to the legacy OQ dict format."""
    return {
        "id": row.get("oq_id", ""),
        "texto": row.get("texto", ""),
        "modo_cierre": row.get("modo_cierre") or "",
        "resolucion": row.get("resolucion") or "",
        "oq_type": row.get("oq_type", "NOT_CLASSIFIED"),
        "critical": bool(row.get("critical", 0)),
        "execution_state": row.get("execution_state", "PENDING"),
        "execution_readiness_check": row.get("readiness_check", "NOT_EVALUATED"),
        "requestion_count": row.get("requestion_count", 0),
    }


# ─── Public API ───────────────────────────────────────────────────────────────

def build_state_payload(beto_dir: Path, cycle_id: str) -> dict:
    """
    Assemble the canonical BETO_STATE Phase 2 payload from SQLite.

    Returns a dict with:
      - All Phase 2 canonical fields (cycle_id, project_id, route_mode, …)
      - Legacy aliases preserved for backward compatibility:
          ciclo_id  = cycle_id
          paso_actual = current_step
          oqs_abiertas = open_questions (legacy format)
          oqs_cerradas = resolved_questions (legacy format)

    Raises ValueError if the cycle is not found in the DB.
    """
    cycle = get_cycle(beto_dir, cycle_id)
    if cycle is None:
        raise ValueError(f"Cycle '{cycle_id}' not found in DB at {beto_dir}")

    open_oq_rows = get_open_oqs(beto_dir, cycle_id)
    closed_oq_rows = get_closed_oqs(beto_dir, cycle_id)
    snapshots = get_active_snapshots(beto_dir, cycle_id)
    decisions = get_routing_decisions(beto_dir, cycle_id)
    promotions = get_route_promotions(beto_dir, cycle_id)
    artifacts = get_artifacts(beto_dir, cycle_id)
    gates = get_latest_gates(beto_dir, cycle_id)

    # Parse JSON-serialised columns from cycles table
    try:
        system_boundaries = json.loads(cycle.get("system_boundaries") or "{}")
    except (json.JSONDecodeError, TypeError):
        system_boundaries = {}
    try:
        stable_decisions = json.loads(cycle.get("stable_decisions") or "[]")
    except (json.JSONDecodeError, TypeError):
        stable_decisions = []

    open_questions = [_oq_row_to_legacy(r) for r in open_oq_rows]
    resolved_questions = [_oq_row_to_legacy(r) for r in closed_oq_rows]
    current_step = cycle.get("paso_actual", 0)

    return {
        # ── Phase 2 canonical fields ────────────────────────────────────────
        "project_id": cycle.get("project_id", ""),
        "cycle_id": cycle_id,
        "cycle_number": None,
        "protocol_version": "4.5",
        "executor_version": "4.5.0",
        "status": cycle.get("status", "IN_PROGRESS"),
        "current_step": current_step,
        "route_mode": cycle.get("route_type") or "",
        "idea_original": cycle.get("idea_raw", ""),
        "system_intent": cycle.get("system_intent") or "",
        "system_name": cycle.get("system_name") or "",
        "system_boundaries": system_boundaries,
        "stable_decisions": stable_decisions,
        "open_questions": open_questions,
        "resolved_questions": resolved_questions,
        "snapshots": snapshots,
        "routing": {
            "decisions": decisions,
            "promotions": promotions,
        },
        "artifacts": artifacts,
        "gates": gates,
        "metadata": {
            "rendered_from": "sqlite",
            "rendered_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": SCHEMA_VERSION,
        },
        # ── Legacy aliases (backward compat) ───────────────────────────────
        # context_builder.py reads ciclo_id; _load_or_create reads paso_actual
        # and oqs_abiertas / oqs_cerradas.
        "ciclo_id": cycle_id,
        "paso_actual": current_step,
        "oqs_abiertas": open_questions,
        "oqs_cerradas": resolved_questions,
    }
