# BETO-TRACE: BETO-EVO2.SEC6.COMP.TraceLogger
# BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase4_AuditoriaTrazabilidad
"""
BETO-EVO2 — TraceLogger
Genera TRACE_ID unico, construye epistemic_manifest, persiste en SQLite,
retorna AuthorizedEvo2Result con TRACE_VERIFIED.
Garantia: ningun resultado sale del sistema sin TRACE_VERIFIED.
"""

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from models import (
    AuthorizedEvo2Result,
    EpistemicState,
    GateApprovalRecord,
    ParameterMap,
    RawEvo2Response,
    TraceStatus,
)


class TraceLogger:
    """
    BETO-TRACE: BETO-EVO2.SEC6.COMP.TraceLogger
    Propietario de la persistencia SQLite y del epistemic_manifest.
    """

    def __init__(self, db_path: str = "beto_evo2.db"):
        self._db_path = Path(db_path)
        self._init_db()

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.TraceLogger.generate_trace_id
    def generate_trace_id(self) -> str:
        """
        Formato declarado: BETO-EVO2-{YYYYMMDD}-{UUID4}
        OQ-T01 DECLARED [BETO_ASSISTED]
        """
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        unique = uuid.uuid4().hex[:8].upper()
        return f"BETO-EVO2-{date_str}-{unique}"

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.TraceLogger.build_manifest
    def build_manifest(
        self,
        param_map: ParameterMap,
        gate_record: GateApprovalRecord,
        evo2_response: RawEvo2Response,
    ) -> dict:
        """
        Construye el epistemic_manifest completo.
        Cada parametro aparece con su valor y estado epistemico.
        BETO-TRACE: BETO-EVO2.SEC4.FIELD.epistemic_manifest
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-10
        """
        manifest = {
            "protocol":          "BETO-EVO2 v1.0",
            "task_type":         param_map.task_type.value if param_map.task_type else None,
            "operator_id":       param_map.operator_id,
            "parameters":        {},
            "gate_approvals": {
                "gate_a": self._gate_to_dict(gate_record.gate_a),
                "gate_b": self._gate_to_dict(gate_record.gate_b),
                "gate_c": self._gate_to_dict(gate_record.gate_c),
            },
            "model_used":        evo2_response.model_used,
            "payload_hash":      evo2_response.payload_hash,
            "latency_ms":        evo2_response.latency_ms,
            "epistemic_summary": {
                "declared":   0,
                "not_stated": 0,
                "inferred":   0,
            },
        }

        for param_name, entry in param_map.parameters.items():
            manifest["parameters"][param_name] = {
                "value":           entry.value,
                "epistemic_state": entry.epistemic_state.value,
                "source":          entry.source,
            }
            if entry.epistemic_state == EpistemicState.DECLARED:
                manifest["epistemic_summary"]["declared"] += 1
            elif entry.epistemic_state == EpistemicState.NOT_STATED:
                manifest["epistemic_summary"]["not_stated"] += 1
            else:
                manifest["epistemic_summary"]["inferred"] += 1

        return manifest

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.TraceLogger.persist
    def persist(
        self,
        trace_id: str,
        param_map: ParameterMap,
        gate_record: GateApprovalRecord,
        evo2_response: RawEvo2Response,
        manifest: dict,
    ) -> str:
        """
        Persiste en SQLite (4 tablas, WAL mode).
        OQ-T02 DECLARED [BETO_ASSISTED].
        BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.executions
        BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.parameters
        BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.gate_approvals
        BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.results
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-08
        """
        spec_hash = self._compute_spec_hash(param_map)

        with sqlite3.connect(self._db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")

            # executions
            conn.execute(
                """
                INSERT INTO executions
                (trace_id, timestamp, operator_id, spec_hash, task_type, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    trace_id,
                    datetime.now(timezone.utc).isoformat(),
                    param_map.operator_id,
                    spec_hash,
                    param_map.task_type.value if param_map.task_type else None,
                    "TRACE_VERIFIED",
                ),
            )

            # parameters
            for param_name, entry in param_map.parameters.items():
                conn.execute(
                    """
                    INSERT INTO parameters
                    (trace_id, param_name, value, epistemic_state, source)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        trace_id,
                        param_name,
                        json.dumps(entry.value),
                        entry.epistemic_state.value,
                        entry.source,
                    ),
                )

            # gate_approvals
            for gate_id, gate_data in [
                ("gate_a", gate_record.gate_a),
                ("gate_b", gate_record.gate_b),
                ("gate_c", gate_record.gate_c),
            ]:
                if gate_data:
                    conn.execute(
                        """
                        INSERT INTO gate_approvals
                        (trace_id, gate_id, timestamp, operator_id, payload_hash)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            trace_id,
                            gate_id,
                            gate_data.timestamp,
                            gate_data.operator_id,
                            gate_record.payload_hash if gate_id == "gate_c" else "",
                        ),
                    )

            # results
            output_val = evo2_response.output
            if isinstance(output_val, list):
                output_val = json.dumps(output_val)
            elif isinstance(output_val, float):
                output_val = str(output_val)

            conn.execute(
                """
                INSERT INTO results
                (trace_id, raw_output, output_type, model_used, latency_ms)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    trace_id,
                    output_val,
                    param_map.task_type.value if param_map.task_type else "UNKNOWN",
                    evo2_response.model_used,
                    evo2_response.latency_ms,
                ),
            )

            conn.commit()

        return spec_hash

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.TraceLogger.verify
    def verify(self, trace_id: str) -> bool:
        """
        Verifica que el registro existe en SQLite.
        Retorna True solo si la verificacion es exitosa.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-07
        """
        with sqlite3.connect(self._db_path) as conn:
            row = conn.execute(
                "SELECT status FROM executions WHERE trace_id = ?", (trace_id,)
            ).fetchone()
            return row is not None and row[0] == "TRACE_VERIFIED"

    def build_result(
        self,
        trace_id: str,
        spec_hash: str,
        evo2_response: RawEvo2Response,
        gate_record: GateApprovalRecord,
        manifest: dict,
    ) -> AuthorizedEvo2Result:
        """
        Construye el resultado final. Solo se emite si verify() == True.
        BETO-TRACE: BETO-EVO2.SEC4.MODEL.AuthorizedEvo2Result
        """
        if not self.verify(trace_id):
            raise RuntimeError(
                f"BETO-GAP [ESCALATED]: TRACE_VERIFIED fallido para {trace_id}. "
                "El resultado no puede ser entregado."
            )

        return AuthorizedEvo2Result(
            trace_id=trace_id,
            evo2_output=evo2_response.output,
            spec_hash=spec_hash,
            gate_approvals={
                "gate_a": self._gate_to_dict(gate_record.gate_a),
                "gate_b": self._gate_to_dict(gate_record.gate_b),
                "gate_c": self._gate_to_dict(gate_record.gate_c),
            },
            epistemic_manifest=manifest,
            trace_status=TraceStatus.TRACE_VERIFIED,
            model_used=evo2_response.model_used,
            latency_ms=evo2_response.latency_ms,
        )

    def persist_failed(
        self,
        trace_id: str,
        param_map: ParameterMap,
        gate_record: GateApprovalRecord,
        error_msg: str,
    ) -> str:
        """
        Persiste spec y gates aunque Evo2 haya fallado.
        Garantia BETO: las decisiones del operador quedan registradas
        independientemente del resultado del modelo.
        Status: FAILED — distinguible de TRACE_VERIFIED.
        """
        spec_hash = self._compute_spec_hash(param_map)

        with sqlite3.connect(self._db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")

            conn.execute(
                """
                INSERT OR IGNORE INTO executions
                (trace_id, timestamp, operator_id, spec_hash, task_type, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    trace_id,
                    datetime.now(timezone.utc).isoformat(),
                    param_map.operator_id,
                    spec_hash,
                    param_map.task_type.value if param_map.task_type else None,
                    f"FAILED: {error_msg[:200]}",
                ),
            )

            for param_name, entry in param_map.parameters.items():
                conn.execute(
                    """
                    INSERT OR IGNORE INTO parameters
                    (trace_id, param_name, value, epistemic_state, source)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        trace_id,
                        param_name,
                        json.dumps(entry.value),
                        entry.epistemic_state.value,
                        entry.source,
                    ),
                )

            for gate_id, gate_data in [
                ("gate_a", gate_record.gate_a),
                ("gate_b", gate_record.gate_b),
                ("gate_c", gate_record.gate_c),
            ]:
                if gate_data:
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO gate_approvals
                        (trace_id, gate_id, timestamp, operator_id, payload_hash)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            trace_id,
                            gate_id,
                            gate_data.timestamp,
                            gate_data.operator_id,
                            gate_record.payload_hash if gate_id == "gate_c" else "",
                        ),
                    )

            conn.commit()

        return spec_hash

    def export_trace_registry(self, output_path: str = "TRACE_REGISTRY.json") -> None:
        """
        Exporta el TRACE_REGISTRY completo a JSON.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-07
        """
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                "SELECT trace_id, timestamp, operator_id, task_type, status FROM executions"
            ).fetchall()

        registry = [
            {
                "trace_id":    r[0],
                "timestamp":   r[1],
                "operator_id": r[2],
                "task_type":   r[3],
                "status":      r[4],
            }
            for r in rows
        ]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({"beto_evo2_trace_registry": registry}, f, indent=2)

        print(f"[BETO-EVO2] TRACE_REGISTRY exportado: {output_path} ({len(registry)} entradas)")

    def _init_db(self) -> None:
        """
        Inicializa schema SQLite. OQ-T02 DECLARED [BETO_ASSISTED].
        BETO-TRACE: BETO-EVO2.SEC4.SCHEMA.SQLite.executions
        """
        schema_path = Path(__file__).parent / "db" / "schema.sql"
        if schema_path.exists():
            ddl = schema_path.read_text(encoding="utf-8")
        else:
            ddl = self._inline_schema()

        with sqlite3.connect(self._db_path) as conn:
            conn.executescript(ddl)

    def _inline_schema(self) -> str:
        """Schema de respaldo si db/schema.sql no esta disponible."""
        return """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS executions (
            trace_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            operator_id TEXT NOT NULL,
            spec_hash TEXT NOT NULL,
            task_type TEXT,
            status TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT NOT NULL REFERENCES executions(trace_id),
            param_name TEXT NOT NULL,
            value TEXT,
            epistemic_state TEXT NOT NULL,
            source TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS gate_approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT NOT NULL REFERENCES executions(trace_id),
            gate_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            operator_id TEXT NOT NULL,
            payload_hash TEXT
        );
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT NOT NULL REFERENCES executions(trace_id),
            raw_output TEXT,
            output_type TEXT,
            model_used TEXT,
            latency_ms INTEGER
        );
        """

    def _compute_spec_hash(self, param_map: ParameterMap) -> str:
        spec = {
            k: str(v.value)
            for k, v in param_map.parameters.items()
            if v.epistemic_state == EpistemicState.DECLARED
        }
        return hashlib.sha256(
            json.dumps(spec, sort_keys=True).encode()
        ).hexdigest()[:16]

    def _gate_to_dict(self, gate) -> dict | None:
        if gate is None:
            return None
        return {
            "approved":    gate.approved,
            "timestamp":   gate.timestamp,
            "operator_id": gate.operator_id,
        }
