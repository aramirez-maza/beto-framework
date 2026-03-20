-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.executions
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.parameters
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.gate_approvals
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.results
-- BETO-EVO2 — Schema SQLite v1.0
-- WAL mode declarado (OQ-T02 DECLARED [BETO_ASSISTED])
-- 4 tablas, sin dependencias externas, Python stdlib

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Registro principal de ejecuciones autorizadas
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.executions
CREATE TABLE IF NOT EXISTS executions (
    trace_id    TEXT PRIMARY KEY,           -- BETO-EVO2-{YYYYMMDD}-{UUID4}
    timestamp   TEXT NOT NULL,              -- ISO 8601 UTC
    operator_id TEXT NOT NULL,
    spec_hash   TEXT NOT NULL,              -- SHA256[:16] de parametros DECLARED
    task_type   TEXT,                       -- GENERATION | SCORING | EMBEDDING
    status      TEXT NOT NULL               -- TRACE_VERIFIED | FAILED
);

-- Parametros con estado epistemico por ejecucion
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.parameters
CREATE TABLE IF NOT EXISTS parameters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id        TEXT NOT NULL REFERENCES executions(trace_id) ON DELETE CASCADE,
    param_name      TEXT NOT NULL,
    value           TEXT,                   -- JSON serializado
    epistemic_state TEXT NOT NULL,          -- DECLARED | NOT_STATED | INFERRED
    source          TEXT NOT NULL           -- operator_input | BETO_ASSISTED | NOT_STATED
);

-- Registro de aprobaciones del operador en cada gate
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.gate_approvals
CREATE TABLE IF NOT EXISTS gate_approvals (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id     TEXT NOT NULL REFERENCES executions(trace_id) ON DELETE CASCADE,
    gate_id      TEXT NOT NULL,             -- gate_a | gate_b | gate_c
    timestamp    TEXT NOT NULL,             -- ISO 8601 UTC de la aprobacion
    operator_id  TEXT NOT NULL,
    payload_hash TEXT                       -- solo en gate_c
);

-- Resultado de Evo2 por ejecucion autorizada
-- BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.results
CREATE TABLE IF NOT EXISTS results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id    TEXT NOT NULL REFERENCES executions(trace_id) ON DELETE CASCADE,
    raw_output  TEXT,                       -- secuencia | score | embedding JSON
    output_type TEXT,                       -- GENERATION | SCORING | EMBEDDING
    model_used  TEXT,                       -- ArcInstitute/evo2-{size}
    latency_ms  INTEGER                     -- tiempo de llamada a Evo2 API
);

-- Indices para consultas de auditoria
CREATE INDEX IF NOT EXISTS idx_params_trace    ON parameters(trace_id);
CREATE INDEX IF NOT EXISTS idx_gates_trace     ON gate_approvals(trace_id);
CREATE INDEX IF NOT EXISTS idx_results_trace   ON results(trace_id);
CREATE INDEX IF NOT EXISTS idx_exec_operator   ON executions(operator_id);
CREATE INDEX IF NOT EXISTS idx_exec_timestamp  ON executions(timestamp);
