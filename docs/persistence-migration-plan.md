# BETO Persistence Migration Plan — JSON → SQLite

**Status:** APPROVED
**Target version:** v4.5
**Date:** 2026-03-18

---

## Objective

Migrate BETO's primary persistence from scattered JSON files to a local SQLite database, without breaking the current executor, maintaining backward compatibility, and enabling a progressive transition.

---

## Guiding Principle

During the transition:

- SQLite is introduced first as an operational replica
- SQLite then becomes the source of truth
- JSON files do not disappear immediately
- JSON moves from active persistence to materialized views or on-demand exports

---

## Primary Architectural Decision

The new persistence layer does **not** live inside `execution_router/`. It stores more than routing — it stores cycles, snapshots, OQs, gates, artifacts, model calls, and derived indexes.

Persistence moves to a **transversal layer** of the executor:

```
beto_executor/
  persistence/
    __init__.py
    schema.py
    connection.py
    queries.py
    writers/
      __init__.py
      cycle_writer.py
      routing_writer.py
      snapshot_writer.py
      oq_writer.py
      gate_writer.py
      model_call_writer.py
      artifact_writer.py
      project_index_reader.py
    readers/
      __init__.py
      state_reader.py
      cycle_reader.py
      artifact_reader.py
    migrate/
      __init__.py
      legacy_json_backfill.py
```

---

## Design Rule — Connection Management

A live SQLite connection must **not** be propagated through the entire system as a shared dependency.

Instead:
- `root.py` initializes the database
- Each writer or reader obtains a connection via `get_connection(beto_dir)`
- Or receives a small factory/repository
- The connection is not treated as a global long-lived shared state

This reduces coupling, improves testability, and avoids lifecycle fragility.

---

## Source of Truth by Phase

| Phase | JSON | SQLite |
|---|---|---|
| Phase 1 | Source of truth | Operational replica |
| Phase 2 | Materialized view (`BETO_STATE.json`) | Source of truth for state |
| Phase 3 | Export/debug/on-demand | Full runtime source of truth |
| Phase 4 | Absorbed (legacy backfill complete) | Sole backend |

---

## SQLite Schema

```sql
-- Projects: one row per project root
CREATE TABLE projects (
    project_id   TEXT PRIMARY KEY,
    project_dir  TEXT NOT NULL UNIQUE,
    created_at   TEXT NOT NULL,
    db_version   TEXT NOT NULL DEFAULT '4.5.0'
);

-- Cycles: source of truth for cycle state (replaces {ciclo_id}.json)
CREATE TABLE cycles (
    cycle_id         TEXT PRIMARY KEY,
    project_id       TEXT NOT NULL REFERENCES projects(project_id),
    idea_raw         TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    status           TEXT NOT NULL,        -- IN_PROGRESS | COMPLETED | ABORTED
    paso_actual      INTEGER NOT NULL DEFAULT 0,
    route_type       TEXT,                 -- BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH
    complexity_score REAL,
    cycle_dir        TEXT NOT NULL,
    reasoning_model  TEXT,
    code_model       TEXT,
    g4_configured    INTEGER DEFAULT 0,
    updated_at       TEXT NOT NULL
);

-- Routing decisions (replaces .beto/routing/decisions/*.json)
CREATE TABLE routing_decisions (
    decision_id          TEXT PRIMARY KEY,   -- RD-2026-0001
    cycle_id             TEXT NOT NULL REFERENCES cycles(cycle_id),
    route_selected       TEXT NOT NULL,
    raw_score            REAL NOT NULL,
    complexity_breakdown TEXT,              -- JSON blob
    context_layers       TEXT,             -- JSON blob
    justification        TEXT,
    executor_assigned    TEXT,
    trace_anchor         TEXT,
    created_at           TEXT NOT NULL,
    UNIQUE(cycle_id, decision_id)
);

-- Route promotions (replaces .beto/routing/promotions/*.json)
CREATE TABLE route_promotions (
    promotion_id           TEXT PRIMARY KEY,  -- RP-2026-0001
    cycle_id               TEXT NOT NULL REFERENCES cycles(cycle_id),
    original_decision_id   TEXT REFERENCES routing_decisions(decision_id),
    promotion_transition   TEXT NOT NULL,     -- LIGHT_TO_PARTIAL | LIGHT_TO_FULL | PARTIAL_TO_FULL
    new_route              TEXT NOT NULL,
    triggers               TEXT,             -- JSON blob
    trigger_description    TEXT,
    operator_notification  INTEGER DEFAULT 0,
    operator_notification_text TEXT,
    trace_anchor           TEXT,
    created_at             TEXT NOT NULL
);

-- Snapshots (replaces .beto/snapshots/*.json)
CREATE TABLE snapshots (
    snapshot_id    TEXT PRIMARY KEY,         -- LC-2026-0001, CS-2026-0001, etc.
    cycle_id       TEXT NOT NULL REFERENCES cycles(cycle_id),
    snapshot_type  TEXT NOT NULL,            -- LOCAL_EXECUTION_CONTEXT | CYCLE_CONTEXT_SNAPSHOT | ACTIVE_OQ_SET | MATERIALIZATION_SCOPE
    paso           INTEGER NOT NULL,
    route_type     TEXT NOT NULL,
    validity_state TEXT NOT NULL DEFAULT 'VALID',  -- VALID | INVALIDATED
    payload        TEXT NOT NULL,            -- JSON blob
    created_at     TEXT NOT NULL,
    invalidated_at TEXT,
    invalidated_by TEXT                      -- promotion_id that invalidated it
);

-- Open Questions (replaces oqs_abiertas/oqs_cerradas in BETO_STATE)
CREATE TABLE open_questions (
    oq_id            TEXT NOT NULL,
    cycle_id         TEXT NOT NULL REFERENCES cycles(cycle_id),
    texto            TEXT NOT NULL,
    oq_type          TEXT NOT NULL,
    critical         INTEGER NOT NULL,
    estado           TEXT NOT NULL,          -- ABIERTA | CERRADA
    modo_cierre      TEXT,                   -- BETO_ASSISTED | HUMAN
    resolucion       TEXT,
    execution_state  TEXT NOT NULL DEFAULT 'PENDING',
    readiness_check  TEXT NOT NULL DEFAULT 'NOT_EVALUATED',
    requestion_count INTEGER NOT NULL DEFAULT 0,
    paso_registrada  INTEGER NOT NULL,
    paso_cerrada     INTEGER,
    PRIMARY KEY (oq_id, cycle_id)
);

-- BETO_GAPs (replaces gaps_activos in BETO_STATE)
CREATE TABLE beto_gaps (
    gap_id        TEXT PRIMARY KEY,
    cycle_id      TEXT NOT NULL REFERENCES cycles(cycle_id),
    elemento      TEXT NOT NULL,
    resolucion    TEXT NOT NULL,             -- BETO_ASSISTED | ESCALATED
    justificacion TEXT,
    paso          INTEGER NOT NULL,
    created_at    TEXT NOT NULL
);

-- Gate decisions (replaces decisiones_gate in BETO_STATE)
CREATE TABLE gate_decisions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id     TEXT NOT NULL REFERENCES cycles(cycle_id),
    gate         TEXT NOT NULL,              -- G-1 | G-2 | G-2B | G-3 | G-4
    decision     TEXT NOT NULL,             -- APPROVED | APPROVED_WITH_LIMITS | REJECTED
    paso         INTEGER NOT NULL,
    operator_notes TEXT,
    decided_at   TEXT NOT NULL
);

-- Artifacts (replaces project_index.json entries)
CREATE TABLE artifacts (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id       TEXT NOT NULL REFERENCES cycles(cycle_id),
    file_path      TEXT NOT NULL,
    file_name      TEXT NOT NULL,
    file_type      TEXT NOT NULL,
    role           TEXT NOT NULL,
    route_relevance TEXT NOT NULL,
    paso_generado  INTEGER,
    v43_compatible INTEGER DEFAULT 1,
    trace_ids      TEXT,                     -- JSON array
    updated_at     TEXT NOT NULL,
    UNIQUE(cycle_id, file_path)
);

-- Model calls (replaces model_call_log in BETO_STATE)
CREATE TABLE model_calls (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id     TEXT NOT NULL REFERENCES cycles(cycle_id),
    paso         INTEGER NOT NULL,
    call_type    TEXT NOT NULL,              -- REASONING | CODE
    model_used   TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    latency_ms   INTEGER,
    route_type   TEXT,
    call_label   TEXT,
    started_at   TEXT NOT NULL,
    completed_at TEXT
);

-- Key indexes
CREATE INDEX idx_cycles_project ON cycles(project_id);
CREATE INDEX idx_routing_decisions_cycle ON routing_decisions(cycle_id);
CREATE INDEX idx_snapshots_cycle_type ON snapshots(cycle_id, snapshot_type);
CREATE INDEX idx_snapshots_validity ON snapshots(cycle_id, validity_state);
CREATE INDEX idx_oqs_cycle_estado ON open_questions(cycle_id, estado);
CREATE INDEX idx_oqs_critical ON open_questions(cycle_id, critical, estado);
CREATE INDEX idx_artifacts_cycle ON artifacts(cycle_id);
CREATE INDEX idx_model_calls_cycle_paso ON model_calls(cycle_id, paso);
CREATE INDEX idx_gate_decisions_cycle ON gate_decisions(cycle_id);
```

---

## Phase 1 — SQLite Dual-Write (Safe Introduction)

**Goal:** Add DB layer without breaking any existing behavior.

**New files:**
- `persistence/schema.py`
- `persistence/connection.py`
- `persistence/queries.py`
- `persistence/writers/cycle_writer.py`
- `persistence/writers/routing_writer.py`
- `persistence/writers/snapshot_writer.py`
- `persistence/writers/oq_writer.py`
- `persistence/writers/gate_writer.py`
- `persistence/writers/model_call_writer.py`
- `persistence/writers/artifact_writer.py`

**Behavior:**
- Existing JSON writers continue working unchanged
- New SQLite writers write in parallel
- No changes to existing public interfaces
- JSON remains source of truth
- SQLite acts as operational replica

**Entry point:** In `orquestador/root.py`, after creating `.beto/`:
- Call `init_db(beto_dir)`
- Do NOT pass a live connection through the system
- Pass `beto_dir` or a persistence factory to modules that write state

**Minimum tables in this phase:** `projects`, `cycles`, `routing_decisions`, `snapshots`, `open_questions`, `gate_decisions`, `model_calls`, `artifacts`

**Mandatory parity validation:** A validation check must compare JSON and DB for critical objects:
- routing decisions
- route promotions
- snapshots
- OQs
- gate decisions

This detects divergences while both backends coexist.

**Expected result:** BETO works exactly as before. All relevant state is replicated in SQLite. JSON ↔ DB consistency can be verified. Migration risk is significantly reduced.

---

## Phase 2 — BETO_STATE Rendered from SQLite

**Goal:** Convert `BETO_STATE.json` into a materialized view generated from the database.

**Modified file:** `beto_state/writer.py`

**Change:** The writer stops constructing state from scattered JSON and instead:
1. Reads current state from SQLite
2. Renders `BETO_STATE.json`
3. Continues writing the file (for LLM compatibility and debugging)

**Reconstruction rules (explicit, not implicit):**

| Field | Source |
|---|---|
| Current cycle | `cycles` table |
| Active artifacts | `artifacts` marked as current |
| Open OQs | `open_questions` where `estado = 'ABIERTA'` |
| Gate decisions | Most recent decision per gate in `gate_decisions` |
| Active route | `cycles.route_type` or last effective routing decision |
| Active snapshots | Last valid snapshot per type in `snapshots` |
| Project index | Derived view from `artifacts` + `cycles` |

**Expected result:** SQLite becomes the state source of truth. `BETO_STATE.json` continues to exist. LLMs are not broken. The file becomes a materialized view.

---

## Phase 3 — Remove JSON as Runtime Persistence

**Goal:** Remove JSON from the active operational flow. Preserve export capability.

**Modified files:**
- `execution_router/router.py`
- `execution_router/snapshot_writer.py`
- `execution_router/project_index_writer.py`

**Removed runtime writes:**
- `.beto/routing/decisions/*.json`
- `.beto/routing/promotions/*.json`
- `.beto/snapshots/*.json` (as primary persistence)
- `project_index.json` (as source of truth)

**Important:** The capability to generate these JSON files is NOT removed. Only their role as the active backend is removed.

**New behavior:**
- Routing lives in DB
- Snapshots live in DB
- Project index lives in DB or is derived from DB
- JSON is generated only on-demand when an external tool or human process requires it

**`ProjectIndexWriter` → `ProjectIndexReader` / `ProjectIndexExporter`:**
- Queries the DB
- Generates `project_index.json` only when requested

**Expected result:** SQLite is the sole runtime persistence. JSON is an export/compatibility/inspection format.

---

## Phase 4 — Legacy Project Backfill

**Goal:** Migrate existing projects that still live only in JSON.

**New module:** `persistence/migrate/legacy_json_backfill.py`

**Work:**
- Read existing JSON structures
- Populate SQLite with those records
- Mark projects as migrated
- Validate minimum integrity
- Allow safe retries

**Minimum validations:**
- Count of cycles migrated
- Count of snapshots migrated
- Count of OQs migrated
- Count of gate decisions migrated
- Presence of main artifacts
- Identifier consistency

**Expected result:** No two separate worlds exist. Old projects are inside the SQLite backend. The transition is complete and uniform.

---

## Files to Create / Modify

### New files
- `persistence/__init__.py`
- `persistence/schema.py`
- `persistence/connection.py`
- `persistence/queries.py`
- `persistence/writers/__init__.py`
- `persistence/writers/cycle_writer.py`
- `persistence/writers/routing_writer.py`
- `persistence/writers/snapshot_writer.py`
- `persistence/writers/oq_writer.py`
- `persistence/writers/gate_writer.py`
- `persistence/writers/model_call_writer.py`
- `persistence/writers/artifact_writer.py`
- `persistence/writers/project_index_reader.py`
- `persistence/readers/__init__.py`
- `persistence/readers/state_reader.py`
- `persistence/readers/cycle_reader.py`
- `persistence/readers/artifact_reader.py`
- `persistence/migrate/__init__.py`
- `persistence/migrate/legacy_json_backfill.py`

### Modified files
- `orquestador/root.py`
- `motor_razonamiento/motor.py`
- `execution_router/router.py`
- `execution_router/snapshot_writer.py`
- `beto_state/writer.py`
- `execution_router/project_index_writer.py`

---

## Compatibility Guarantees

- **Zero new dependencies** — `sqlite3` is Python stdlib
- **WAL mode enabled** — safe concurrent reads while executor writes
- **v4.3 backward compatibility** — if a component does not use the DB layer, the system must not break
- **`{ciclo_id}.json`** (gestor_ciclo) can be migrated to `cycles` table without breaking `StateReader`'s public interface

---

## Mandatory Technical Rules

**Rule 1:** The DB layer does not belong to the router. It is a transversal layer of the executor.

**Rule 2:** Do not share a live SQLite connection through the entire system. Use `get_connection(beto_dir)` or factories/repositories.

**Rule 3:** Phase 1 must include JSON ↔ DB parity verification for critical objects.

**Rule 4:** Phase 2 must define exactly how `BETO_STATE.json` is reconstructed from the DB.

**Rule 5:** Phase 3 does not delete JSON as a useful format — only removes it as runtime persistence.

**Rule 6:** An explicit backfill must exist for legacy projects.

---

## Key Queries Enabled

```sql
-- Open critical OQs in this cycle
SELECT oq_id, texto FROM open_questions
WHERE cycle_id = ? AND estado = 'ABIERTA' AND critical = 1;

-- What decisions were BETO_ASSISTED vs HUMAN
SELECT oq_id, modo_cierre, resolucion FROM open_questions
WHERE cycle_id = ? AND estado = 'CERRADA';

-- What cycle generated a given artifact
SELECT c.cycle_id, c.idea_raw, a.paso_generado
FROM artifacts a JOIN cycles c USING(cycle_id)
WHERE a.file_name = 'BETO_SYSTEM_GRAPH.md';

-- Active valid snapshots for a cycle
SELECT snapshot_id, snapshot_type, paso FROM snapshots
WHERE cycle_id = ? AND validity_state = 'VALID'
ORDER BY paso, snapshot_type;

-- Route selected per cycle across the project
SELECT cycle_id, route_selected, raw_score FROM routing_decisions
ORDER BY created_at;

-- Artifacts relevant for PARTIAL and FULL routes
SELECT file_name, file_type FROM artifacts
WHERE cycle_id = ? AND route_relevance != 'LIGHT_ONLY';
```

---

## Recommended Execution Order

1. Phase 1 — Dual-write introduction
2. Phase 2 — BETO_STATE from DB
3. Phase 3 — Remove JSON as runtime
4. Phase 4 — Legacy backfill

Do not skip Phase 4. Without it the migration is operationally incomplete.
