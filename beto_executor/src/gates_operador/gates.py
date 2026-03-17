"""
BETO-TRACE: BETO_GATES.SEC1.INTENT.OPERATOR_GATE_MANAGEMENT
BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_1_RECEPCION_SEÑAL
BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_2_PRESENTACION_CAPTURA
BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_3_RESOLUCION_GATE
BETO-TRACE: BETO_GATES.SEC5.INVARIANT.OPERATOR_DECISION_IMMUTABLE
BETO-TRACE: BETO_GATES.SEC5.INVARIANT.NO_AUTO_APPROVAL
"""

from datetime import datetime, timezone

from pathlib import Path

from .artifact_validator import presentar_reporte_validacion, validar_artefactos_gate
from .cli_presenter import presentar_gap, presentar_gate
from .decision_capturer import capturar_decision, capturar_resolucion_gap
from .retroceso_resolver import BETOGapEscalado, determinar_paso_retroceso

# BETO-TRACE: BETO_GATES.SEC8.DECISION.GATES_G1_G2_G2B_G3_G4
# G-2B: Operational Readiness Gate — BETO v4.3 (actualizacion_beto.md §13)
# Pregunta: ¿Las declaraciones críticas son ejecutables sin inferencias relevantes?
# Resultados: APPROVED_EXECUTABLE | APPROVED_WITH_LIMITS | BLOCKED_BY_EXECUTIONAL_GAPS
# G-2B se evalúa después del EXECUTION_READINESS_CHECK en el Paso 6 (CIERRE_ASISTIDO_OPERATIVO).
# En BETO_PARALELO: se evalúa por unidad, NO bloquea globalmente.
GATES_DECLARADOS = {"G-1", "G-2", "G-2B", "G-3", "G-4"}


class GatesOperador:
    """
    BETO-TRACE: BETO_GATES.SEC1.INTENT.OPERATOR_GATE_MANAGEMENT
    BETO-TRACE: BETO_GATES.SEC6.MODEL.STATE_REGISTRAR

    Gestiona el ciclo completo de un evento de gate:
    recepción → presentación → captura → resolución.
    """

    def __init__(self, state_manager, cycle_dir=None):
        self.state_manager = state_manager
        self.cycle_dir = cycle_dir

    def procesar_gate(self, ciclo_id: str, señal: dict) -> dict:
        """
        BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_1_RECEPCION_SEÑAL
        BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_2_PRESENTACION_CAPTURA
        BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_3_RESOLUCION_GATE

        Procesa un evento de gate completo. Retorna la señal de resolución.

        señal: { paso_origen, motor_origen, artefacto_generado, beto_gap_adjunto }

        Retorna:
            { decision, paso_retroceso_si_aplica, resolucion_gap_si_aplica,
              señal_tipo: 'CONTINUACION' | 'RETROCESO' }
        """
        # — PHASE 1: Recepción y validación —
        # BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_1_RECEPCION_SEÑAL
        self._validar_señal(señal)
        paso_origen = señal["paso_origen"]

        # Registro inicial en Gestor de Ciclo: estado PENDIENTE
        self.state_manager.aplicar_evento(
            ciclo_id,
            "REGISTRAR_DECISION",
            {
                "gate_id": paso_origen,
                "decision": "PENDIENTE",
                "justificacion_opcional": "",
                "paso_retroceso_si_aplica": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        # — PHASE 2: Presentación y Captura —
        # BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_2_PRESENTACION_CAPTURA
        presentar_gate(señal, cycle_dir=self.cycle_dir)

        # Validación estructural del artefacto — READ-ONLY
        # BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.CLI_PRESENTATION
        if self.cycle_dir:
            reports = validar_artefactos_gate(paso_origen, Path(self.cycle_dir))
            presentar_reporte_validacion(reports)

        resolucion_gap = ""
        beto_gap = señal.get("beto_gap_adjunto")

        if beto_gap:
            # BETO-TRACE: BETO_GATES.SEC8.DECISION.GAP_PRESENTED_AT_GATE
            presentar_gap(beto_gap)
            resolucion_gap = capturar_resolucion_gap()

        captura = capturar_decision(paso_origen)
        # BETO-TRACE: BETO_GATES.SEC5.INVARIANT.OPERATOR_DECISION_IMMUTABLE
        decision = captura["decision"]
        justificacion = captura["justificacion_opcional"]

        # — PHASE 3: Resolución —
        # BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_3_RESOLUCION_GATE
        paso_retroceso = None
        señal_tipo = "CONTINUACION"

        if decision == "rechazado":
            try:
                paso_retroceso = determinar_paso_retroceso(paso_origen, justificacion)
                señal_tipo = "RETROCESO"
            except BETOGapEscalado as e:
                # G-3 sin justificación clara → BETO_GAP [ESCALADO], volver a Phase 2
                print(f"\n  BETO_GAP [ESCALADO]: {e}")
                print("  Por favor, proporcione una justificación con el paso de retroceso.")
                return self.procesar_gate(ciclo_id, señal)  # re-presentar gate

        # Registrar resolución del gap si había
        if resolucion_gap:
            self.state_manager.aplicar_evento(
                ciclo_id,
                "REGISTRAR_GAP",
                {
                    "gap_id": f"gap-{paso_origen}-{ciclo_id[:8]}",
                    "descripcion": str(beto_gap),
                    "tipo": "ESCALADO",
                    "paso": _gate_a_paso_num(paso_origen),
                    "estado": "RESUELTO",
                    "resolucion": resolucion_gap,
                },
            )

        # Actualizar decisión del gate: PENDIENTE → APROBADO | RECHAZADO
        # BETO-TRACE: BETO_GATES.SEC3.OUTPUT.GATE_STATE_REGISTERED
        self.state_manager.aplicar_evento(
            ciclo_id,
            "REGISTRAR_DECISION",
            {
                "gate_id": paso_origen,
                "decision": decision,
                "justificacion_opcional": justificacion,
                "paso_retroceso_si_aplica": paso_retroceso,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        print(f"\n  Gate {paso_origen}: {decision.upper()}")
        if paso_retroceso is not None:
            print(f"  Retroceso al Paso {paso_retroceso}")
        print()

        return {
            "decision": decision,
            "paso_retroceso_si_aplica": paso_retroceso,
            "resolucion_gap_si_aplica": resolucion_gap,
            "señal_tipo": señal_tipo,
        }

    def _validar_señal(self, señal: dict) -> None:
        """
        BETO-TRACE: BETO_GATES.SEC7.PHASE.PHASE_1_RECEPCION_SEÑAL
        BETO-TRACE: BETO_GATES.SEC4.FIELD.PASO_ORIGEN
        BETO-TRACE: BETO_GATES.SEC4.FIELD.MOTOR_ORIGEN
        """
        requeridos = {"paso_origen", "motor_origen", "artefacto_generado"}
        faltantes = requeridos - set(señal.keys())
        if faltantes:
            raise ValueError(f"Señal de gate incompleta. Campos faltantes: {faltantes}")

        if señal["paso_origen"] not in GATES_DECLARADOS:
            raise ValueError(
                f"paso_origen '{señal['paso_origen']}' no es un gate declarado. "
                f"Gates válidos: {GATES_DECLARADOS}"
            )

        motores_validos = {"MOTOR_RAZONAMIENTO", "MOTOR_CODIGO"}
        if señal["motor_origen"] not in motores_validos:
            raise ValueError(
                f"motor_origen '{señal['motor_origen']}' no es válido. "
                f"Motores válidos: {motores_validos}"
            )


def _gate_a_paso_num(gate_id: str) -> int:
    # G-2B es el subgate de Operational Readiness dentro del Paso 6
    # (CIERRE_ASISTIDO_OPERATIVO — BETO v4.3)
    return {"G-1": 1, "G-2": 4, "G-2B": 6, "G-3": 9, "G-4": 10}.get(gate_id, 0)
