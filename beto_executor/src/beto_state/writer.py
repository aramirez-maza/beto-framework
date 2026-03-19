"""
BETOStateWriter — orquesta la actualización de BETO_STATE.json después de cada paso.

Estrategia por paso:
  Paso 0-1: solo ciclo_id + paso_actual (aún no hay artefactos ricos)
  Paso 2:   agrega system_intent, boundaries, STDs, OQs (desde BETO_CORE_DRAFT)
  Paso 4:   agrega nodos (desde BETO_SYSTEM_GRAPH)
  Paso 5:   enriquece nodos con intent de sus BETO_COREs hijos
  Paso 6:   agrega OQs cerradas (desde CIERRE_ASISTIDO)
  Paso 7+:  carga gates desde SQLite

Phase 4 (v4.5): SQLite-only mode.
  - Estado inicial cargado desde SQLite (no desde BETO_STATE.json).
  - Si beto.db no existe, se crea automáticamente con init_db().
  - BETO_STATE.json se renderiza siempre desde SQLite.
  - Sin fallback — cualquier fallo en el render propaga la excepción.
"""

from __future__ import annotations
import json as _json
import sys
from datetime import datetime, timezone
from pathlib import Path

from .schema import BETOState, NodoBETO, OQ
from .extractor import (
    extract_from_beto_core_draft,
    extract_from_beto_system_graph,
    extract_from_cierre_asistido,
    extract_node_intent,
)

BETO_STATE_FILENAME = "BETO_STATE.json"


class BETOStateWriter:
    """
    Actualiza BETO_STATE.json en el cycle_dir después de cada paso.
    Thread-safe no requerido — BETO_EXECUTOR es single-process.

    Phase 4 (v4.5): SQLite-only mode.
      - Estado inicial leído desde SQLite (ciclo, OQs, gates).
      - Si beto.db no existe: auto-creado con init_db().
      - Siempre raises en fallo de render — sin fallback.
      - Nodos y campos OSC se re-extraen de markdown en cada paso.
    """

    def __init__(self, cycle_dir: Path, ciclo_id: str):
        self.cycle_dir = cycle_dir
        self.ciclo_id = ciclo_id
        self.state_path = cycle_dir / BETO_STATE_FILENAME
        self._beto_dir = cycle_dir / ".beto"

    def update(self, paso: int) -> BETOState:
        """
        Carga el estado desde SQLite, aplica las extracciones del paso,
        escribe BETO_STATE.json renderizado desde SQLite. Retorna el BETOState.
        """
        state = self._load_or_create(paso)
        state.paso_actual = paso
        state.generado_en_paso = paso
        state.timestamp = datetime.now(timezone.utc).isoformat()

        warnings = state.extraction_warnings

        # — Paso 1+: extraer desde BETO_CORE_DRAFT —
        if paso >= 1:
            self._update_from_beto_core_draft(state, warnings)

        # — Paso 4+: extraer nodos desde BETO_SYSTEM_GRAPH —
        if paso >= 4:
            self._update_from_beto_system_graph(state, warnings)

        # — Paso 5+: enriquecer nodos con intent de sus BETO_COREs hijos —
        if paso >= 5:
            self._enrich_node_intents(state, warnings)

        # — Paso 6+: OQs cerradas desde CIERRE_ASISTIDO / CIERRE_ASISTIDO_OPERATIVO —
        if paso >= 6:
            self._update_from_cierre_asistido(state, warnings)
            self._update_osc_from_executional_gap_registry(state, warnings)

        # — Siempre: gates desde SQLite —
        self._load_gates_from_db(state)

        # Deduplicar warnings
        state.extraction_warnings = list(dict.fromkeys(warnings))

        # Phase 4: push to DB + render from SQLite (auto-creates DB, raises on failure)
        self._attempt_phase4_render(state, paso)

        return state

    # ── Phase 4 core ───────────────────────────────────────────────────────────

    def _attempt_phase4_render(self, state: BETOState, paso: int) -> None:
        """
        SQLite-only render:
          1. Auto-create beto.db if absent.
          2. Push extracted state to SQLite (non-fatal push warning on failure).
          3. Render BETO_STATE.json from SQLite — raises on any failure.
        """
        if not (self._beto_dir / "beto.db").exists():
            from persistence.schema import init_db
            init_db(self._beto_dir)

        self._push_to_db(state, paso)
        self._do_phase4_render(state)  # raises on failure — no try/except

    def _push_to_db(self, state: BETOState, paso: int) -> None:
        """
        Push system-info and OQ state to SQLite.
        Non-fatal — logs to stderr on failure; render step may use prior DB data.
        """
        try:
            from persistence.writers.cycle_writer import CycleWriter
            from persistence.writers.oq_writer import OQWriter
            from dataclasses import asdict

            system_boundaries = _json.dumps(
                {"in": state.system_boundaries_in, "out": state.system_boundaries_out},
                ensure_ascii=False,
            )
            stable_decisions = _json.dumps(state.stable_decisions, ensure_ascii=False)

            CycleWriter.update_system_info(
                beto_dir=self._beto_dir,
                cycle_id=self.ciclo_id,
                system_intent=state.system_intent,
                system_name=state.system_name,
                system_boundaries=system_boundaries,
                stable_decisions=stable_decisions,
            )

            oq_writer = OQWriter(self._beto_dir, self.ciclo_id)
            oq_writer.sync_from_dicts(
                oqs_abiertas=[asdict(oq) for oq in state.oqs_abiertas],
                oqs_cerradas=[asdict(oq) for oq in state.oqs_cerradas],
                paso=paso,
            )
        except Exception as exc:
            print(
                f"[BETO_STATE] WARNING reason_code=DB_PUSH_FAILED "
                f"cycle={self.ciclo_id} exc={type(exc).__name__}: {exc}",
                file=sys.stderr,
            )

    def _do_phase4_render(self, state: BETOState) -> None:
        """
        Render BETO_STATE.json from SQLite, supplemented with markdown-extracted
        fields not yet tracked in SQLite (nodos, OSC fields, extraction_warnings).

        Raises on any failure — caller owns no fallback.
        """
        from persistence.readers.state_reader import build_state_payload
        from dataclasses import asdict

        payload = build_state_payload(self._beto_dir, self.ciclo_id)

        # Supplement SQLite payload with fields extracted from markdown
        payload["nodos"] = [asdict(n) for n in state.nodos]
        payload["executional_gap_count"] = state.executional_gap_count
        payload["requestion_history"] = state.requestion_history
        payload["operational_residue"] = state.operational_residue
        payload["accepted_limits"] = state.accepted_limits
        payload["g2b_result"] = state.g2b_result
        payload["extraction_warnings"] = state.extraction_warnings

        self.state_path.write_text(
            _json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ── State loading ──────────────────────────────────────────────────────────

    def _load_or_create(self, paso: int) -> BETOState:
        """Load cycle state from SQLite. Returns empty BETOState if DB or cycle absent."""
        db_path = self._beto_dir / "beto.db"
        if not db_path.exists():
            return BETOState(ciclo_id=self.ciclo_id, paso_actual=paso)

        try:
            from persistence.queries import get_cycle, get_open_oqs, get_closed_oqs

            cycle = get_cycle(self._beto_dir, self.ciclo_id)
            if cycle is None:
                return BETOState(ciclo_id=self.ciclo_id, paso_actual=paso)

            try:
                boundaries = _json.loads(cycle.get("system_boundaries") or "{}")
            except Exception:
                boundaries = {}
            try:
                stable_decisions = _json.loads(cycle.get("stable_decisions") or "[]")
            except Exception:
                stable_decisions = []

            open_oq_rows = get_open_oqs(self._beto_dir, self.ciclo_id)
            closed_oq_rows = get_closed_oqs(self._beto_dir, self.ciclo_id)

            return BETOState(
                ciclo_id=self.ciclo_id,
                paso_actual=cycle.get("paso_actual", paso),
                system_name=cycle.get("system_name") or "",
                system_intent=cycle.get("system_intent") or "",
                system_boundaries_in=boundaries.get("in", []),
                system_boundaries_out=boundaries.get("out", []),
                stable_decisions=stable_decisions,
                nodos=[],          # Re-extracted from markdown
                oqs_abiertas=[_row_to_oq(r) for r in open_oq_rows],
                oqs_cerradas=[_row_to_oq(r) for r in closed_oq_rows],
                gaps_activos=[],   # No GapWriter — acceptable for Phase 4
                decisiones_gate=[], # Loaded via _load_gates_from_db
            )
        except Exception:
            return BETOState(ciclo_id=self.ciclo_id, paso_actual=paso)

    def _load_gates_from_db(self, state: BETOState) -> None:
        """
        Load gate decisions from SQLite into state.decisiones_gate.
        Replaces _update_from_state_json (which read from Gestor de Ciclo JSON).
        Non-fatal — on failure, decisiones_gate stays as loaded from _load_or_create.
        """
        db_path = self._beto_dir / "beto.db"
        if not db_path.exists():
            return
        try:
            from persistence.queries import get_gate_decisions
            rows = get_gate_decisions(self._beto_dir, self.ciclo_id)
            state.decisiones_gate = [
                {
                    "gate_id": r["gate"],
                    "decision": r["decision"],
                    "paso": r["paso"],
                    "operator_notes": r.get("operator_notes"),
                    "decided_at": r.get("decided_at"),
                }
                for r in rows
            ]
        except Exception:
            pass

    # ── File I/O ───────────────────────────────────────────────────────────────

    def _read_artifact(self, nombre: str) -> str | None:
        ruta = self.cycle_dir / nombre
        if ruta.exists():
            return ruta.read_text(encoding="utf-8")
        return None

    # ── Extraction helpers ─────────────────────────────────────────────────────

    def _update_from_beto_core_draft(self, state: BETOState, warnings: list[str]) -> None:
        content = self._read_artifact("BETO_CORE_DRAFT.md")
        if not content:
            warnings.append("BETO_CORE_DRAFT.md no encontrado en cycle_dir")
            return

        data = extract_from_beto_core_draft(content, warnings)

        if data["system_name"] and not state.system_name:
            state.system_name = data["system_name"]
        if data["system_intent"]:
            state.system_intent = data["system_intent"]
        if data["system_boundaries_in"]:
            state.system_boundaries_in = data["system_boundaries_in"]
        if data["system_boundaries_out"]:
            state.system_boundaries_out = data["system_boundaries_out"]
        if data["stable_decisions"]:
            state.stable_decisions = data["stable_decisions"]

        existing_oq_ids = {oq.id for oq in state.oqs_abiertas} | {oq.id for oq in state.oqs_cerradas}
        for oq in data["oqs_abiertas"]:
            if oq.id not in existing_oq_ids:
                state.oqs_abiertas.append(oq)
                existing_oq_ids.add(oq.id)
        for oq in data["oqs_cerradas"]:
            if oq.id not in existing_oq_ids:
                state.oqs_cerradas.append(oq)
                existing_oq_ids.add(oq.id)
            elif oq.id in {o.id for o in state.oqs_abiertas}:
                state.oqs_abiertas = [o for o in state.oqs_abiertas if o.id != oq.id]
                state.oqs_cerradas.append(oq)

    def _update_from_beto_system_graph(self, state: BETOState, warnings: list[str]) -> None:
        content = self._read_artifact("BETO_SYSTEM_GRAPH.md")
        if not content:
            warnings.append("BETO_SYSTEM_GRAPH.md no encontrado en cycle_dir")
            return

        data = extract_from_beto_system_graph(content, warnings)

        if data["system_name"]:
            state.system_name = data["system_name"]

        if data["nodos"]:
            existing_intents = {n.id: n.intent for n in state.nodos if n.intent}
            state.nodos = data["nodos"]
            for n in state.nodos:
                if n.id in existing_intents:
                    n.intent = existing_intents[n.id]

    def _enrich_node_intents(self, state: BETOState, warnings: list[str]) -> None:
        for nodo in state.nodos:
            if nodo.intent or not nodo.beto_core:
                continue
            content = self._read_artifact(nodo.beto_core)
            if content:
                intent = extract_node_intent(content)
                if intent:
                    nodo.intent = intent
                else:
                    warnings.append(f"Nodo {nodo.id}: no se extrajo intent de {nodo.beto_core}")

    def _update_from_cierre_asistido(self, state: BETOState, warnings: list[str]) -> None:
        content = self._read_artifact("CIERRE_ASISTIDO_OPERATIVO.md")
        if not content:
            content = self._read_artifact("CIERRE_ASISTIDO.md")
        if not content:
            warnings.append(
                "CIERRE_ASISTIDO_OPERATIVO.md (ni CIERRE_ASISTIDO.md) no encontrado en cycle_dir"
            )
            return

        data = extract_from_cierre_asistido(content, warnings)
        oqs_cierre = data.get("oqs_cerradas_cierre", [])

        existing_cerradas = {oq.id: oq for oq in state.oqs_cerradas}
        abiertas_ids = {oq.id for oq in state.oqs_abiertas}

        for oq in oqs_cierre:
            if oq.id in existing_cerradas:
                existing = existing_cerradas[oq.id]
                if not existing.modo_cierre:
                    existing.modo_cierre = oq.modo_cierre
                if not existing.resolucion:
                    existing.resolucion = oq.resolucion
            else:
                state.oqs_cerradas.append(oq)
                if oq.id in abiertas_ids:
                    state.oqs_abiertas = [o for o in state.oqs_abiertas if o.id != oq.id]

    def _update_osc_from_executional_gap_registry(
        self, state: BETOState, warnings: list[str]
    ) -> None:
        import re

        intent_map = self._read_artifact("EXECUTION_INTENT_MAP.md")
        if intent_map:
            g2b_match = re.search(
                r"\*\*Resultado:\*\*\s*(APPROVED_EXECUTABLE|APPROVED_WITH_LIMITS|BLOCKED_BY_EXECUTIONAL_GAPS)",
                intent_map,
            )
            if g2b_match and not state.g2b_result:
                state.g2b_result = g2b_match.group(1)

        gap_registry = self._read_artifact("EXECUTIONAL_GAP_REGISTRY.md")
        if gap_registry:
            active_gaps = re.findall(r"DECLARED_RAW", gap_registry)
            count = len(active_gaps)
            if count > 0 or state.executional_gap_count == 0:
                state.executional_gap_count = count

        cierre_op = self._read_artifact("CIERRE_ASISTIDO_OPERATIVO.md")
        if not cierre_op:
            cierre_op = self._read_artifact("CIERRE_ASISTIDO.md")

        if cierre_op:
            for oq in state.oqs_cerradas:
                oq_id = oq.id
                exec_match = re.search(
                    rf"{re.escape(oq_id)}.*?execution_state:\s*(DECLARED_EXECUTABLE|DECLARED_WITH_LIMITS|DECLARED_RAW)",
                    cierre_op,
                    re.DOTALL,
                )
                if exec_match:
                    oq.execution_state = exec_match.group(1)

            with_limits_count = len(re.findall(r"DECLARED_WITH_LIMITS", cierre_op))
            if with_limits_count > len(state.accepted_limits):
                import_ts = ""
                try:
                    import_ts = datetime.now(timezone.utc).isoformat()
                except Exception:
                    pass
                if not state.accepted_limits:
                    state.accepted_limits = [
                        {
                            "source": "CIERRE_ASISTIDO_OPERATIVO",
                            "count": with_limits_count,
                            "timestamp": import_ts,
                        }
                    ]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _row_to_oq(r: dict) -> OQ:
    """Convert a DB open_questions row to an OQ dataclass."""
    return OQ(
        id=r.get("oq_id", ""),
        texto=r.get("texto", ""),
        modo_cierre=r.get("modo_cierre") or "",
        resolucion=r.get("resolucion") or "",
        oq_type=r.get("oq_type", "NOT_CLASSIFIED"),
        critical=bool(r.get("critical", 0)),
        execution_state=r.get("execution_state", "PENDING"),
        execution_readiness_check=r.get("readiness_check", "NOT_EVALUATED"),
        requestion_count=r.get("requestion_count", 0),
    )
