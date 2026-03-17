"""
BETO-TRACE: BETO_GESTOR.SEC1.INTENT.STATE_SERIALIZATION
BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_2_GESTION_ESTADO
BETO-TRACE: BETO_GESTOR.SEC8.DECISION.NON_DESTRUCTIVE_UPDATES
"""

import json
from datetime import datetime, timezone
from pathlib import Path


# BETO-TRACE: BETO_GESTOR.SEC4.FIELD.TIPO_EVENTO
VALID_EVENT_TYPES = {
    "ACTUALIZAR_PASO",
    "REGISTRAR_ARTEFACTO",
    "REGISTRAR_DECISION",
    "REGISTRAR_GAP",
    # OSC events — BETO v4.3 (Operational Semantic Closure Layer)
    # Ref: actualizacion_beto.md §17 — Eventos nuevos
    "BETO_EXECUTIONAL_REQUESTION",          # Repregunta operativa sobre OQ crítica
    "BETO_GAP_EXECUTIONAL",                 # Gap execucional detectado (respuesta existe pero insuficiente)
    "BETO_DECLARATION_PROMOTED_TO_EXECUTABLE",  # OQ promovida a DECLARED_EXECUTABLE
    "BETO_DECLARATION_ACCEPTED_WITH_LIMITS",    # OQ aceptada como DECLARED_WITH_LIMITS
    "REGISTRAR_G2B_RESULT",                 # Resultado del gate G-2B (Operational Readiness Gate)
}


class StateManager:
    """
    BETO-TRACE: BETO_GESTOR.SEC6.MODEL.STATE_UPDATER
    BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_2_GESTION_ESTADO

    Único punto de escritura autorizado sobre el estado de un ciclo activo.
    Actualiza el estado JSON corriente de manera no destructiva.
    """

    def __init__(self, cycle_output_dir: str | Path):
        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
        self.cycle_output_dir = Path(cycle_output_dir)

    def aplicar_evento(self, ciclo_id: str, tipo_evento: str, payload: dict) -> None:
        """
        BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_2_GESTION_ESTADO
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.NON_DESTRUCTIVE_UPDATES
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.WRITE_BEFORE_CONFIRM

        Aplica un evento de actualización al estado del ciclo y lo persiste.
        """
        if tipo_evento not in VALID_EVENT_TYPES:
            raise ValueError(
                f"Tipo de evento no declarado: '{tipo_evento}'. "
                f"Tipos válidos: {sorted(VALID_EVENT_TYPES)}"
            )

        state = self._read(ciclo_id)

        # BETO-TRACE: BETO_GESTOR.SEC5.INVARIANT.NON_DESTRUCTIVE
        if state.get("estado_ciclo") == "FINALIZADO":
            raise ValueError(
                f"Ciclo {ciclo_id} tiene estado FINALIZADO. No actualizable."
            )

        # BETO-TRACE: BETO_GESTOR.SEC5.INVARIANT.CICLO_ID_IMMUTABLE
        # BETO-TRACE: BETO_GESTOR.SEC5.INVARIANT.IDEA_RAW_IMMUTABLE
        # Los campos inmutables nunca se tocan — solo se actualizan los mutables.

        if tipo_evento == "ACTUALIZAR_PASO":
            # BETO-TRACE: BETO_GESTOR.SEC3.INPUT.UPDATE_EVENT
            state["paso_actual"] = payload["paso_actual"]

        elif tipo_evento == "REGISTRAR_ARTEFACTO":
            # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.NON_DESTRUCTIVE_UPDATES
            nombre = payload["nombre_artefacto"]
            existing = next(
                (a for a in state["artefactos"] if a["nombre_artefacto"] == nombre),
                None,
            )
            if existing:
                existing.update(payload)
            else:
                state["artefactos"].append(dict(payload))

        elif tipo_evento == "REGISTRAR_DECISION":
            # BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.GATE_DECISION_REGISTRATION
            state["decisiones_gate"].append(dict(payload))
            if payload.get("paso_retroceso_si_aplica") is not None:
                state["paso_actual"] = payload["paso_retroceso_si_aplica"]

        elif tipo_evento == "REGISTRAR_GAP":
            gap_id = payload.get("gap_id")
            existing = next(
                (g for g in state["beto_gaps"] if g.get("gap_id") == gap_id),
                None,
            )
            if existing:
                existing.update(payload)
            else:
                state["beto_gaps"].append(dict(payload))

        # — OSC Events — BETO v4.3 (Operational Semantic Closure Layer) —
        # Ref: actualizacion_beto.md §17

        elif tipo_evento == "BETO_GAP_EXECUTIONAL":
            # Registra un gap execucional: respuesta existe pero es operativamente insuficiente
            # payload: { gap_id, oq_id, oq_type, descripcion, impacto, unit_id?, trace_id? }
            gap_id = payload.get("gap_id")
            if "beto_gaps_execucionales" not in state:
                state["beto_gaps_execucionales"] = []
            existing = next(
                (g for g in state["beto_gaps_execucionales"] if g.get("gap_id") == gap_id),
                None,
            )
            if existing:
                existing.update(payload)
            else:
                state["beto_gaps_execucionales"].append(dict(payload))
            # Actualizar contador
            state["executional_gap_count"] = len(state["beto_gaps_execucionales"])

        elif tipo_evento == "BETO_EXECUTIONAL_REQUESTION":
            # Registra una repregunta operativa sobre una OQ crítica
            # payload: { oq_id, oq_type, pregunta, respuesta?, requestion_number, unit_id?, trace_id? }
            if "requestion_history" not in state:
                state["requestion_history"] = []
            state["requestion_history"].append(dict(payload))

        elif tipo_evento == "BETO_DECLARATION_PROMOTED_TO_EXECUTABLE":
            # Registra la promoción de una OQ a DECLARED_EXECUTABLE
            # payload: { oq_id, oq_type, justificacion, unit_id?, trace_id? }
            if "osc_promotions" not in state:
                state["osc_promotions"] = []
            state["osc_promotions"].append({
                **payload,
                "execution_state": "DECLARED_EXECUTABLE",
                "execution_readiness_check": "PASS_EXECUTABLE",
            })

        elif tipo_evento == "BETO_DECLARATION_ACCEPTED_WITH_LIMITS":
            # Registra la aceptación de una OQ con límites operativos (DECLARED_WITH_LIMITS)
            # payload: { oq_id, oq_type, limites_aceptados, ambiguedad_residual, unit_id?, trace_id? }
            if "accepted_limits" not in state:
                state["accepted_limits"] = []
            state["accepted_limits"].append({
                **payload,
                "execution_state": "DECLARED_WITH_LIMITS",
                "execution_readiness_check": "PASS_WITH_LIMITS",
            })

        elif tipo_evento == "REGISTRAR_G2B_RESULT":
            # Registra el resultado del gate G-2B (Operational Readiness Gate)
            # payload: { result, justificacion, oqs_bloqueantes?, unit_id?, trace_id? }
            # result: APPROVED_EXECUTABLE | APPROVED_WITH_LIMITS | BLOCKED_BY_EXECUTIONAL_GAPS
            state["g2b_result"] = payload.get("result", "")
            state["g2b_justificacion"] = payload.get("justificacion", "")
            if payload.get("unit_id"):
                # En BETO_PARALELO, el resultado es local a la unidad
                if "g2b_por_unidad" not in state:
                    state["g2b_por_unidad"] = {}
                state["g2b_por_unidad"][payload["unit_id"]] = {
                    "result": payload.get("result", ""),
                    "justificacion": payload.get("justificacion", ""),
                    "oqs_bloqueantes": payload.get("oqs_bloqueantes", []),
                }
            # Registrar también como decisión de gate para compatibilidad
            state["decisiones_gate"].append({
                "gate_id": "G-2B",
                "decision": payload.get("result", ""),
                "justificacion_opcional": payload.get("justificacion", ""),
                "paso_retroceso_si_aplica": None,
                "timestamp": payload.get("timestamp", ""),
                "unit_id": payload.get("unit_id", ""),
            })

        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.WRITE_BEFORE_CONFIRM
        self._persist(ciclo_id, state)

    def marcar_finalizado(self, ciclo_id: str) -> None:
        """
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.FINALIZED_ON_DISK
        Marca el ciclo como FINALIZADO. Los ciclos finalizados se mantienen en disco.
        """
        state = self._read(ciclo_id)
        state["estado_ciclo"] = "FINALIZADO"
        state["timestamp_finalizacion"] = datetime.now(timezone.utc).isoformat()
        self._persist(ciclo_id, state)

    def _read(self, ciclo_id: str) -> dict:
        path = self.cycle_output_dir / f"{ciclo_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Ciclo no encontrado: {ciclo_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _persist(self, ciclo_id: str, state: dict) -> None:
        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
        path = self.cycle_output_dir / f"{ciclo_id}.json"
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
