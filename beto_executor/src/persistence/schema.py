"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC8.DECISION.SQLITE_STDLIB_NO_DEPS

SQLite schema for BETO persistence layer v4.5.
All tables created here. init_db() is idempotent — safe to call at every
cycle start.
"""

import sqlite3
from pathlib import Path

# ─── Schema version ───────────────────────────────────────────────────────────

SCHEMA_VERSION = "4.5.0"

# ─── DDL ──────────────────────────────────────────────────────────────────────

_TABLES = [
    # Schema version tracking
    """
    CREATE TABLE IF NOT EXISTS schema_version (
        version     TEXT NOT NULL,
        applied_at  TEXT NOT NULL
    )
    """,

    # Projects: one row per project root (identified by cycle_output_dir)
    """
    CREATE TABLE IF NOT EXISTS projects (
        project_id   TEXT PRIMARY KEY,
        project_dir  TEXT NOT NULL UNIQUE,
        created_at   TEXT NOT NULL,
        db_version   TEXT NOT NULL DEFAULT '4.5.0'
    )
    """,

    # Cycles: source of truth for cycle state (replaces {ciclo_id}.json)
    """
    CREATE TABLE IF NOT EXISTS cycles (
        cycle_id         TEXT PRIMARY KEY,
        project_id       TEXT NOT NULL REFERENCES projects(project_id),
        idea_raw         TEXT NOT NULL,
        created_at       TEXT NOT NULL,
        status           TEXT NOT NULL DEFAULT 'IN_PROGRESS',
        paso_actual      INTEGER NOT NULL DEFAULT 0,
        route_type       TEXT,
        complexity_score REAL,
        cycle_dir        TEXT NOT NULL,
        reasoning_model  TEXT,
        code_model       TEXT,
        g4_configured    INTEGER NOT NULL DEFAULT 0,
        updated_at       TEXT NOT NULL
    )
    """,

    # Routing decisions (dual-write alongside .beto/routing/decisions/*.json)
    """
    CREATE TABLE IF NOT EXISTS routing_decisions (
        decision_id          TEXT PRIMARY KEY,
        cycle_id             TEXT NOT NULL REFERENCES cycles(cycle_id),
        route_selected       TEXT NOT NULL,
        raw_score            REAL NOT NULL,
        complexity_breakdown TEXT,
        context_layers       TEXT,
        justification        TEXT,
        executor_assigned    TEXT,
        trace_anchor         TEXT,
        step_context         TEXT,
        subproblem_desc      TEXT,
        created_at           TEXT NOT NULL
    )
    """,

    # Route promotions (dual-write alongside .beto/routing/promotions/*.json)
    """
    CREATE TABLE IF NOT EXISTS route_promotions (
        promotion_id              TEXT PRIMARY KEY,
        cycle_id                  TEXT NOT NULL REFERENCES cycles(cycle_id),
        original_decision_id      TEXT REFERENCES routing_decisions(decision_id),
        promotion_transition      TEXT NOT NULL,
        new_route                 TEXT NOT NULL,
        triggers                  TEXT,
        trigger_description       TEXT,
        operator_notification     INTEGER NOT NULL DEFAULT 0,
        operator_notification_text TEXT,
        trace_anchor              TEXT,
        created_at                TEXT NOT NULL
    )
    """,

    # Snapshots (dual-write alongside .beto/snapshots/*.json)
    """
    CREATE TABLE IF NOT EXISTS snapshots (
        snapshot_id    TEXT PRIMARY KEY,
        cycle_id       TEXT NOT NULL REFERENCES cycles(cycle_id),
        snapshot_type  TEXT NOT NULL,
        paso           INTEGER NOT NULL,
        route_type     TEXT NOT NULL,
        validity_state TEXT NOT NULL DEFAULT 'VALID',
        payload        TEXT NOT NULL,
        created_at     TEXT NOT NULL,
        invalidated_at TEXT,
        invalidated_by TEXT
    )
    """,

    # Open Questions (synced from BETO_STATE after each paso update)
    """
    CREATE TABLE IF NOT EXISTS open_questions (
        oq_id            TEXT NOT NULL,
        cycle_id         TEXT NOT NULL REFERENCES cycles(cycle_id),
        texto            TEXT NOT NULL,
        oq_type          TEXT NOT NULL DEFAULT 'NOT_CLASSIFIED',
        critical         INTEGER NOT NULL DEFAULT 0,
        estado           TEXT NOT NULL DEFAULT 'ABIERTA',
        modo_cierre      TEXT,
        resolucion       TEXT,
        execution_state  TEXT NOT NULL DEFAULT 'PENDING',
        readiness_check  TEXT NOT NULL DEFAULT 'NOT_EVALUATED',
        requestion_count INTEGER NOT NULL DEFAULT 0,
        paso_registrada  INTEGER NOT NULL DEFAULT 0,
        paso_cerrada     INTEGER,
        PRIMARY KEY (oq_id, cycle_id)
    )
    """,

    # BETO_GAPs
    """
    CREATE TABLE IF NOT EXISTS beto_gaps (
        gap_id        TEXT PRIMARY KEY,
        cycle_id      TEXT NOT NULL REFERENCES cycles(cycle_id),
        elemento      TEXT NOT NULL,
        resolucion    TEXT NOT NULL,
        justificacion TEXT,
        paso          INTEGER NOT NULL,
        created_at    TEXT NOT NULL
    )
    """,

    # Gate decisions
    """
    CREATE TABLE IF NOT EXISTS gate_decisions (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_id       TEXT NOT NULL REFERENCES cycles(cycle_id),
        gate           TEXT NOT NULL,
        decision       TEXT NOT NULL,
        paso           INTEGER NOT NULL,
        operator_notes TEXT,
        decided_at     TEXT NOT NULL
    )
    """,

    # Artifacts (synced from artifact registration events)
    """
    CREATE TABLE IF NOT EXISTS artifacts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_id        TEXT NOT NULL REFERENCES cycles(cycle_id),
        file_path       TEXT NOT NULL,
        file_name       TEXT NOT NULL,
        file_type       TEXT NOT NULL DEFAULT 'OTHER',
        role            TEXT NOT NULL DEFAULT 'documentation',
        route_relevance TEXT NOT NULL DEFAULT 'ALL_ROUTES',
        paso_generado   INTEGER,
        v43_compatible  INTEGER NOT NULL DEFAULT 1,
        trace_ids       TEXT,
        updated_at      TEXT NOT NULL,
        UNIQUE(cycle_id, file_path)
    )
    """,

    # Model calls
    """
    CREATE TABLE IF NOT EXISTS model_calls (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle_id      TEXT NOT NULL REFERENCES cycles(cycle_id),
        paso          INTEGER NOT NULL,
        call_type     TEXT NOT NULL,
        model_used    TEXT NOT NULL,
        input_tokens  INTEGER,
        output_tokens INTEGER,
        latency_ms    INTEGER,
        route_type    TEXT,
        call_label    TEXT,
        started_at    TEXT NOT NULL,
        completed_at  TEXT
    )
    """,
]

# ─── Column migrations ────────────────────────────────────────────────────────
# ADD COLUMN uses try/except because SQLite has no IF NOT EXISTS for ALTER TABLE.
# Safe to run on every init — failures mean the column already exists.
_MIGRATIONS = [
    "ALTER TABLE cycles ADD COLUMN system_intent TEXT DEFAULT ''",
    "ALTER TABLE cycles ADD COLUMN system_name TEXT DEFAULT ''",
    "ALTER TABLE cycles ADD COLUMN system_boundaries TEXT DEFAULT '{}'",
    "ALTER TABLE cycles ADD COLUMN stable_decisions TEXT DEFAULT '[]'",
]

_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_cycles_project ON cycles(project_id)",
    "CREATE INDEX IF NOT EXISTS idx_routing_decisions_cycle ON routing_decisions(cycle_id)",
    "CREATE INDEX IF NOT EXISTS idx_snapshots_cycle_type ON snapshots(cycle_id, snapshot_type)",
    "CREATE INDEX IF NOT EXISTS idx_snapshots_validity ON snapshots(cycle_id, validity_state)",
    "CREATE INDEX IF NOT EXISTS idx_oqs_cycle_estado ON open_questions(cycle_id, estado)",
    "CREATE INDEX IF NOT EXISTS idx_oqs_critical ON open_questions(cycle_id, critical, estado)",
    "CREATE INDEX IF NOT EXISTS idx_artifacts_cycle ON artifacts(cycle_id)",
    "CREATE INDEX IF NOT EXISTS idx_model_calls_cycle_paso ON model_calls(cycle_id, paso)",
    "CREATE INDEX IF NOT EXISTS idx_gate_decisions_cycle ON gate_decisions(cycle_id)",
]


# ─── Public API ────────────────────────────────────────────────────────────────

def init_db(beto_dir: Path) -> Path:
    """
    Initialize the BETO SQLite database at beto_dir/beto.db.
    Idempotent — safe to call on every cycle start.
    Returns the path to the database file.
    """
    from .connection import get_connection

    beto_dir.mkdir(parents=True, exist_ok=True)
    db_path = beto_dir / "beto.db"

    conn = get_connection(beto_dir)
    try:
        with conn:
            for ddl in _TABLES:
                conn.execute(ddl)
            for idx in _INDEXES:
                conn.execute(idx)
            for migration in _MIGRATIONS:
                try:
                    conn.execute(migration)
                except Exception:
                    pass  # Column already exists

            # Record schema version if not already present
            existing = conn.execute("SELECT version FROM schema_version").fetchone()
            if existing is None:
                from datetime import datetime, timezone
                conn.execute(
                    "INSERT INTO schema_version (version, applied_at) VALUES (?, ?)",
                    (SCHEMA_VERSION, datetime.now(timezone.utc).isoformat()),
                )
    finally:
        conn.close()

    return db_path
