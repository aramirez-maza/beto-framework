"""
BETO-TRACE: BETO_V45.SEC8.DECISION.DUAL_WRITE_PARITY

Parity validation: detect JSON records that are not in SQLite.

Phase 1 semantics: both JSON and SQLite were written; divergences in
either direction were reported.

Phase 3 semantics: JSON files are no longer written at runtime.  The
expected state is "DB has records, JSON has none".  Only records present
in JSON but absent from DB represent a real problem (something was written
to JSON but the DB write was missed).  Records present only in DB are the
correct Phase 3 state and are NOT reported as divergences.

Usage:
    from persistence.parity_check import check_parity, ParityReport
    report = check_parity(beto_dir, cycle_id)
    if not report.is_clean:
        print(report.summary())
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from .connection import get_connection


@dataclass
class ParityReport:
    cycle_id: str
    divergences: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.divergences) == 0

    def summary(self) -> str:
        if self.is_clean:
            return f"[PARITY] {self.cycle_id}: OK — JSON and SQLite are in sync"
        lines = [f"[PARITY] {self.cycle_id}: {len(self.divergences)} divergence(s) found"]
        for d in self.divergences:
            lines.append(f"  • {d}")
        return "\n".join(lines)


def check_parity(beto_dir: Path, cycle_id: str) -> ParityReport:
    """
    Compare JSON files against SQLite for a given cycle.
    Checks: routing_decisions, route_promotions, snapshots.

    Returns a ParityReport. Call report.summary() to print results.
    """
    report = ParityReport(cycle_id=cycle_id)

    _check_routing_decisions(beto_dir, cycle_id, report)
    _check_route_promotions(beto_dir, cycle_id, report)
    _check_snapshots(beto_dir, cycle_id, report)

    return report


# ─── Checks ───────────────────────────────────────────────────────────────────

def _check_routing_decisions(beto_dir: Path, cycle_id: str, report: ParityReport) -> None:
    decisions_dir = beto_dir / "routing" / "decisions"
    json_ids = _read_json_ids(decisions_dir)

    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT decision_id FROM routing_decisions WHERE cycle_id = ?", (cycle_id,)
        ).fetchall()
    finally:
        conn.close()

    db_ids = {row["decision_id"] for row in rows}

    only_json = json_ids - db_ids

    for rid in sorted(only_json):
        report.divergences.append(f"routing_decision {rid}: in JSON only (missing from DB)")


def _check_route_promotions(beto_dir: Path, cycle_id: str, report: ParityReport) -> None:
    promotions_dir = beto_dir / "routing" / "promotions"
    json_ids = _read_json_ids(promotions_dir)

    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT promotion_id FROM route_promotions WHERE cycle_id = ?", (cycle_id,)
        ).fetchall()
    finally:
        conn.close()

    db_ids = {row["promotion_id"] for row in rows}

    only_json = json_ids - db_ids

    for rid in sorted(only_json):
        report.divergences.append(f"route_promotion {rid}: in JSON only (missing from DB)")


def _check_snapshots(beto_dir: Path, cycle_id: str, report: ParityReport) -> None:
    snapshots_dir = beto_dir / "snapshots"
    json_ids = _read_json_ids(snapshots_dir)

    conn = get_connection(beto_dir)
    try:
        rows = conn.execute(
            "SELECT snapshot_id FROM snapshots WHERE cycle_id = ?", (cycle_id,)
        ).fetchall()
    finally:
        conn.close()

    db_ids = {row["snapshot_id"] for row in rows}

    only_json = json_ids - db_ids

    for sid in sorted(only_json):
        report.divergences.append(f"snapshot {sid}: in JSON only (missing from DB)")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _read_json_ids(directory: Path) -> set[str]:
    """Return the set of JSON filename stems (without extension) from a directory."""
    if not directory.exists():
        return set()
    return {f.stem for f in directory.glob("*.json")}
