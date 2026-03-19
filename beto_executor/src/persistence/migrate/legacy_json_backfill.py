"""
BETO-TRACE: BETO_V45.SEC7.PHASE.PHASE_4_LEGACY_BACKFILL

Legacy JSON → SQLite backfill for BETO v4.5.

migrate_project(beto_dir) scans the standard BETO directory layout for legacy
JSON artifacts and populates the SQLite DB so the system can operate in
SQLite-only mode.

Idempotent: uses INSERT OR IGNORE throughout — safe to call multiple times.

Usage:
    from persistence.migrate.legacy_json_backfill import migrate_project
    report = migrate_project(Path(".beto"))
    print(report.summary())

Layout assumed:
    beto_dir/                     — .beto directory
        beto.db                   — created here if missing
        routing/decisions/*.json  — legacy ROUTING_DECISION_RECORD files
        routing/promotions/*.json — legacy ROUTE_PROMOTION_RECORD files
        snapshots/*.json          — legacy snapshot files
        project_index.json        — legacy PROJECT_INDEX
    beto_dir/../BETO_STATE.json   — cycle + OQ state (cycle_dir = beto_dir.parent)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


# ─── Report ───────────────────────────────────────────────────────────────────

@dataclass
class BackfillReport:
    beto_dir: Path
    cycles_written: int = 0
    routing_decisions_written: int = 0
    route_promotions_written: int = 0
    snapshots_written: int = 0
    oqs_written: int = 0
    artifacts_written: int = 0
    gate_decisions_written: int = 0
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"[BACKFILL] {self.beto_dir}",
            f"  cycles:            {self.cycles_written}",
            f"  routing_decisions: {self.routing_decisions_written}",
            f"  route_promotions:  {self.route_promotions_written}",
            f"  snapshots:         {self.snapshots_written}",
            f"  open_questions:    {self.oqs_written}",
            f"  artifacts:         {self.artifacts_written}",
            f"  gate_decisions:    {self.gate_decisions_written}",
        ]
        if self.warnings:
            lines.append(f"  warnings ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"    • {w}")
        return "\n".join(lines)


# ─── Public API ────────────────────────────────────────────────────────────────

def migrate_project(beto_dir: Path) -> BackfillReport:
    """
    Migrate legacy JSON artifacts to SQLite for the BETO project at beto_dir.

    - If beto.db does not exist, initialises it via init_db().
    - Reads legacy JSON from the filesystem and populates DB tables.
    - Idempotent: existing rows are silently skipped (INSERT OR IGNORE).

    Returns a BackfillReport with counts and any warnings encountered.
    """
    from persistence.schema import init_db

    report = BackfillReport(beto_dir=beto_dir)

    if not (beto_dir / "beto.db").exists():
        init_db(beto_dir)

    cycle_dir = beto_dir.parent
    beto_state_path = cycle_dir / "BETO_STATE.json"
    cycle_id: str | None = None

    # ── 1. Cycle + OQs + gates from BETO_STATE.json ───────────────────────────
    if beto_state_path.exists():
        try:
            state = json.loads(beto_state_path.read_text(encoding="utf-8"))
            cycle_id = state.get("ciclo_id") or state.get("cycle_id")
            if not cycle_id:
                report.warnings.append(
                    "BETO_STATE.json: missing ciclo_id/cycle_id — cycle skipped"
                )
            else:
                from persistence.writers.cycle_writer import CycleWriter
                project_dir = cycle_dir.parent if cycle_dir.parent != cycle_dir else cycle_dir
                project_id = CycleWriter.ensure_project(beto_dir, project_dir)

                _backfill_cycle(beto_dir, project_id, cycle_id, state, cycle_dir, report)
                _backfill_oqs(beto_dir, cycle_id, state, report)
                _backfill_gates(beto_dir, cycle_id, state, report)
        except Exception as exc:
            report.warnings.append(f"BETO_STATE.json: {type(exc).__name__}: {exc}")
    else:
        report.warnings.append("BETO_STATE.json not found — cycle and OQ backfill skipped")

    # ── 2. Routing decisions ───────────────────────────────────────────────────
    decisions_dir = beto_dir / "routing" / "decisions"
    if decisions_dir.exists():
        for jf in sorted(decisions_dir.glob("*.json")):
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                _backfill_routing_decision(beto_dir, data, report)
            except Exception as exc:
                report.warnings.append(f"{jf.name}: {type(exc).__name__}: {exc}")

    # ── 3. Route promotions ────────────────────────────────────────────────────
    promotions_dir = beto_dir / "routing" / "promotions"
    if promotions_dir.exists():
        for jf in sorted(promotions_dir.glob("*.json")):
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                _backfill_route_promotion(beto_dir, data, report)
            except Exception as exc:
                report.warnings.append(f"{jf.name}: {type(exc).__name__}: {exc}")

    # ── 4. Snapshots ───────────────────────────────────────────────────────────
    snapshots_dir = beto_dir / "snapshots"
    if snapshots_dir.exists():
        for jf in sorted(snapshots_dir.glob("*.json")):
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                _backfill_snapshot(beto_dir, data, report)
            except Exception as exc:
                report.warnings.append(f"{jf.name}: {type(exc).__name__}: {exc}")

    # ── 5. Artifacts from project_index.json ──────────────────────────────────
    index_path = beto_dir / "project_index.json"
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
            meta = index.get("index_metadata", {})
            cycle_id_idx = meta.get("cycle_id")
            if cycle_id_idx:
                _backfill_artifacts(
                    beto_dir, cycle_id_idx, index.get("entries", []), cycle_dir, report
                )
        except Exception as exc:
            report.warnings.append(f"project_index.json: {type(exc).__name__}: {exc}")

    # ── 6. Validate ────────────────────────────────────────────────────────────
    _validate(beto_dir, cycle_id, report)

    return report


# ─── Internal helpers ─────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _changes(conn) -> int:
    return conn.execute("SELECT changes()").fetchone()[0]


def _backfill_cycle(
    beto_dir: Path,
    project_id: str,
    cycle_id: str,
    state: dict,
    cycle_dir: Path,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    idea_raw = (
        state.get("idea_original")
        or state.get("idea_raw")
        or "[imported from legacy backfill]"
    )
    paso_actual = state.get("paso_actual", 0)
    route_type = state.get("current_route_type") or state.get("route_mode") or ""
    status = state.get("status", "COMPLETED")
    system_intent = state.get("system_intent", "")
    system_name = state.get("system_name", "")
    system_boundaries = json.dumps({
        "in": state.get("system_boundaries_in", []),
        "out": state.get("system_boundaries_out", []),
    }, ensure_ascii=False)
    stable_decisions = json.dumps(state.get("stable_decisions", []), ensure_ascii=False)
    now = _now()

    conn = get_connection(beto_dir)
    try:
        with conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO cycles (
                    cycle_id, project_id, idea_raw, created_at, status, paso_actual,
                    route_type, cycle_dir, updated_at,
                    system_intent, system_name, system_boundaries, stable_decisions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cycle_id, project_id, idea_raw, now, status, paso_actual,
                    route_type, str(cycle_dir), now,
                    system_intent, system_name, system_boundaries, stable_decisions,
                ),
            )
            report.cycles_written += _changes(conn)
    finally:
        conn.close()


def _backfill_oqs(
    beto_dir: Path,
    cycle_id: str,
    state: dict,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    conn = get_connection(beto_dir)
    try:
        written = 0
        with conn:
            for oq in state.get("oqs_abiertas", []):
                oq_id = oq.get("id", "")
                if not oq_id:
                    continue
                conn.execute(
                    """
                    INSERT OR IGNORE INTO open_questions (
                        oq_id, cycle_id, texto, oq_type, critical, estado,
                        execution_state, readiness_check, requestion_count, paso_registrada
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        oq_id, cycle_id,
                        oq.get("texto", ""),
                        oq.get("oq_type", "NOT_CLASSIFIED"),
                        1 if oq.get("critical") else 0,
                        "ABIERTA",
                        oq.get("execution_state", "PENDING"),
                        oq.get("execution_readiness_check", "NOT_EVALUATED"),
                        oq.get("requestion_count", 0),
                        0,
                    ),
                )
                written += _changes(conn)

            for oq in state.get("oqs_cerradas", []):
                oq_id = oq.get("id", "")
                if not oq_id:
                    continue
                conn.execute(
                    """
                    INSERT OR IGNORE INTO open_questions (
                        oq_id, cycle_id, texto, oq_type, critical, estado,
                        modo_cierre, resolucion, execution_state, readiness_check,
                        requestion_count, paso_registrada
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        oq_id, cycle_id,
                        oq.get("texto", ""),
                        oq.get("oq_type", "NOT_CLASSIFIED"),
                        1 if oq.get("critical") else 0,
                        "CERRADA",
                        oq.get("modo_cierre", ""),
                        oq.get("resolucion", ""),
                        oq.get("execution_state", "DECLARED_EXECUTABLE"),
                        oq.get("execution_readiness_check", "PASS_EXECUTABLE"),
                        oq.get("requestion_count", 0),
                        0,
                    ),
                )
                written += _changes(conn)

        report.oqs_written += written
    finally:
        conn.close()


def _backfill_gates(
    beto_dir: Path,
    cycle_id: str,
    state: dict,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    gates = state.get("decisiones_gate", [])
    if not gates:
        return

    conn = get_connection(beto_dir)
    try:
        written = 0
        now = _now()
        with conn:
            for g in gates:
                gate = g.get("gate_id") or g.get("gate")
                decision = g.get("decision")
                if not gate or not decision or decision == "PENDIENTE":
                    continue
                conn.execute(
                    """
                    INSERT OR IGNORE INTO gate_decisions (
                        cycle_id, gate, decision, paso, operator_notes, decided_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cycle_id, gate, decision,
                        g.get("paso", 0),
                        g.get("operator_notes") or g.get("notas"),
                        now,
                    ),
                )
                written += _changes(conn)
        report.gate_decisions_written += written
    finally:
        conn.close()


def _backfill_routing_decision(
    beto_dir: Path,
    data: dict,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    decision_id = data.get("decision_id")
    cycle_id = data.get("cycle_id")
    if not decision_id or not cycle_id:
        return

    complexity = data.get("complexity_breakdown")
    context = data.get("context_layers")

    conn = get_connection(beto_dir)
    try:
        with conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO routing_decisions (
                    decision_id, cycle_id, route_selected, raw_score,
                    complexity_breakdown, context_layers, justification,
                    executor_assigned, trace_anchor, step_context, subproblem_desc,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    decision_id, cycle_id,
                    data.get("route_selected", ""),
                    data.get("raw_score", 0.0),
                    json.dumps(complexity) if isinstance(complexity, (dict, list)) else complexity,
                    json.dumps(context) if isinstance(context, (dict, list)) else context,
                    data.get("justification"),
                    data.get("executor_assigned"),
                    data.get("trace_anchor"),
                    data.get("step_context"),
                    data.get("subproblem_desc") or data.get("subproblem_description"),
                    data.get("created_at") or _now(),
                ),
            )
            report.routing_decisions_written += _changes(conn)
    finally:
        conn.close()


def _backfill_route_promotion(
    beto_dir: Path,
    data: dict,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    promotion_id = data.get("promotion_id")
    cycle_id = data.get("cycle_id")
    if not promotion_id or not cycle_id:
        return

    triggers = data.get("triggers")

    conn = get_connection(beto_dir)
    try:
        with conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO route_promotions (
                    promotion_id, cycle_id, original_decision_id,
                    promotion_transition, new_route, triggers, trigger_description,
                    operator_notification, operator_notification_text,
                    trace_anchor, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    promotion_id, cycle_id,
                    data.get("original_decision_id"),
                    data.get("promotion_transition", ""),
                    data.get("new_route", ""),
                    json.dumps(triggers) if isinstance(triggers, (dict, list)) else triggers,
                    data.get("trigger_description"),
                    1 if data.get("operator_notification") else 0,
                    data.get("operator_notification_text"),
                    data.get("trace_anchor"),
                    data.get("created_at") or _now(),
                ),
            )
            report.route_promotions_written += _changes(conn)
    finally:
        conn.close()


def _backfill_snapshot(
    beto_dir: Path,
    data: dict,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    snapshot_id = data.get("snapshot_id")
    cycle_id = data.get("cycle_id")
    if not snapshot_id or not cycle_id:
        return

    payload = data.get("payload") or data.get("context") or {}

    conn = get_connection(beto_dir)
    try:
        with conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO snapshots (
                    snapshot_id, cycle_id, snapshot_type, paso, route_type,
                    validity_state, payload, created_at,
                    invalidated_at, invalidated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id, cycle_id,
                    data.get("snapshot_type", "LOCAL_EXECUTION_CONTEXT"),
                    data.get("paso", 0),
                    data.get("route_type", ""),
                    data.get("validity_state", "VALID"),
                    json.dumps(payload, ensure_ascii=False) if isinstance(payload, (dict, list)) else str(payload),
                    data.get("created_at") or _now(),
                    data.get("invalidated_at"),
                    data.get("invalidated_by"),
                ),
            )
            report.snapshots_written += _changes(conn)
    finally:
        conn.close()


def _backfill_artifacts(
    beto_dir: Path,
    cycle_id: str,
    entries: list[dict],
    cycle_dir: Path,
    report: BackfillReport,
) -> None:
    from persistence.connection import get_connection

    conn = get_connection(beto_dir)
    try:
        written = 0
        with conn:
            for entry in entries:
                file_name = entry.get("file", "")
                # Only index plain markdown files; synthetic paths (`.beto/...`) are skipped
                if not file_name or not file_name.endswith(".md") or "/" in file_name:
                    continue
                file_path = str(cycle_dir / file_name)
                trace_ids = entry.get("trace_ids_authorized")
                conn.execute(
                    """
                    INSERT OR IGNORE INTO artifacts (
                        cycle_id, file_path, file_name, file_type, role,
                        route_relevance, paso_generado, v43_compatible,
                        trace_ids, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cycle_id, file_path, file_name,
                        entry.get("file_type", "OTHER"),
                        entry.get("role", "documentation"),
                        entry.get("route_relevance", "ALL_ROUTES"),
                        None,
                        1,
                        json.dumps(trace_ids) if trace_ids else None,
                        entry.get("last_updated") or _now(),
                    ),
                )
                written += _changes(conn)
        report.artifacts_written += written
    finally:
        conn.close()


def _validate(beto_dir: Path, cycle_id: str | None, report: BackfillReport) -> None:
    from persistence.connection import get_connection

    conn = get_connection(beto_dir)
    try:
        cycles = conn.execute("SELECT COUNT(*) FROM cycles").fetchone()[0]
        if cycles == 0:
            report.warnings.append("Validation: no cycles in DB after backfill")

        if cycle_id:
            oqs = conn.execute(
                "SELECT COUNT(*) FROM open_questions WHERE cycle_id = ?", (cycle_id,)
            ).fetchone()[0]
            snaps = conn.execute(
                "SELECT COUNT(*) FROM snapshots WHERE cycle_id = ?", (cycle_id,)
            ).fetchone()[0]
            if oqs == 0 and report.oqs_written == 0:
                report.warnings.append(
                    "Validation: no OQs in DB — BETO_STATE.json may lack OQ data"
                )
            if snaps == 0 and report.snapshots_written == 0:
                report.warnings.append(
                    "Validation: no snapshots in DB — legacy .beto/snapshots/ may be absent"
                )
    finally:
        conn.close()
