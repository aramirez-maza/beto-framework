"""
BETO-TRACE: BETO_GESTOR.SEC1.INTENT.RESUMPTION
BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_3_LECTURA_REANUDACION
BETO-TRACE: BETO_GESTOR.SEC8.DECISION.RESUME_POINTS_AT_GATES
BETO-TRACE: BETO_GESTOR.SEC8.DECISION.MOTOR_BY_STEP
"""

import json
from pathlib import Path


class StateReader:
    """
    BETO-TRACE: BETO_GESTOR.SEC6.MODEL.RESUMPTION_HANDLER
    BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_3_LECTURA_REANUDACION

    Atiende solicitudes de lectura de estado y reanudación.
    Solo lectura — no modifica el estado del ciclo.
    """

    def __init__(self, cycle_output_dir: str | Path):
        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
        self.cycle_output_dir = Path(cycle_output_dir)

    def leer(self, ciclo_id: str) -> dict:
        """
        BETO-TRACE: BETO_GESTOR.SEC3.OUTPUT.CURRENT_STATE
        Retorna el estado corriente del ciclo sin modificarlo.
        Válido también para ciclos FINALIZADOS (para auditoría).
        """
        state = self._read(ciclo_id)
        return state

    def resolver_reanudacion(self, ciclo_id: str) -> dict:
        """
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.RESUME_POINTS_AT_GATES
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.MOTOR_BY_STEP
        BETO-TRACE: BETO_GESTOR.SEC3.OUTPUT.RESUME_STATE

        Determina el punto de reanudación y el motor destino.
        Puntos de reanudación = puntos de gate (último gate APROBADO).
        Motor: Pasos 0-9 → MOTOR_RAZONAMIENTO; Paso 10 → MOTOR_CODIGO.
        """
        state = self._read(ciclo_id)

        if state.get("estado_ciclo") == "FINALIZADO":
            raise ValueError(
                f"Ciclo {ciclo_id} está FINALIZADO. No es reanudable."
            )

        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.RESUME_POINTS_AT_GATES
        decisiones = state.get("decisiones_gate", [])
        aprobadas = [d for d in decisiones if d.get("decision") == "aprobado"]

        if not aprobadas:
            # Sin gates aprobados: reanudar desde el último paso registrado
            paso_reanudacion = state.get("paso_actual", 0)
        else:
            # Último gate aprobado — el paso siguiente a ese gate es el punto de reanudación
            ultimo_aprobado = aprobadas[-1]
            gate_id = ultimo_aprobado.get("gate_id", "")
            paso_reanudacion = _paso_post_gate(gate_id)

        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.MOTOR_BY_STEP
        # Override: si paso_actual >= 10 el Motor Código ya inició — ir directo aunque
        # G-3 no esté en decisiones_gate (proceso interrumpido antes de persistir el gate)
        if state.get("paso_actual", 0) >= 10:
            motor_destino = "MOTOR_CODIGO"
            paso_reanudacion = 10
        elif paso_reanudacion <= 9:
            motor_destino = "MOTOR_RAZONAMIENTO"
        else:
            motor_destino = "MOTOR_CODIGO"

        return {
            "ciclo_id": ciclo_id,
            "paso_reanudacion": paso_reanudacion,
            "motor_destino": motor_destino,
            "estado_ciclo_completo": state,
        }

    def _read(self, ciclo_id: str) -> dict:
        path = self.cycle_output_dir / f"{ciclo_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Ciclo no encontrado: {ciclo_id}")
        return json.loads(path.read_text(encoding="utf-8"))


def _paso_post_gate(gate_id: str) -> int:
    """
    BETO-TRACE: BETO_GESTOR.SEC8.DECISION.RESUME_POINTS_AT_GATES
    Retorna el primer paso a ejecutar después de un gate aprobado.
    G-1 aprobado → continuar desde Paso 2
    G-2 aprobado → continuar desde Paso 5
    G-3 aprobado → continuar desde Paso 10
    G-4 aprobado → ciclo terminado (no hay paso siguiente)
    """
    mapping = {
        "G-1": 2,
        "G-2": 5,
        "G-3": 10,
        "G-4": 11,
    }
    return mapping.get(gate_id, 0)
