"""
BETO-TRACE: BETO_MOTOR_RAZ.SEC1.INTENT.EXECUTE_BETO_STEPS_0_9
BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_1_INICIO_CICLO
BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_2_PIPELINE
BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_3_HANDOFF
BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.GATE_PAUSER
BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.RETROCESO_HANDLER
"""

from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

from .artifact_writer import ArtifactWriter
from .step_executor import StepExecutor
from beto_state.writer import BETOStateWriter


# BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.GATES_G1_G2_G3
GATE_EN_PASO: dict[int, str] = {
    1: "G-1",
    4: "G-2",
    9: "G-3",
}


class MotorRazonamiento:
    """
    BETO-TRACE: BETO_MOTOR_RAZ.SEC1.INTENT.EXECUTE_BETO_STEPS_0_9
    BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.STEP_SEQUENCER

    Ejecuta los Pasos 0–9 del framework BETO via LLM de razonamiento.
    Pausa en gates G-1, G-2, G-3 y espera señal de continuación o retroceso.
    """

    def __init__(
        self,
        ciclo_id: str,
        idea_raw: str,
        cycle_dir: Path,
        client: OpenAI,
        model: str,
        state_manager,
        gates_operador,
        templates_dir: Path | None = None,
    ):
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC3.INPUT.IDEA_RAW
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC3.INPUT.CICLO_ID
        self.ciclo_id = ciclo_id
        self.idea_raw = idea_raw
        self.cycle_dir = cycle_dir
        self.state_manager = state_manager
        self.gates = gates_operador

        self.artifact_writer = ArtifactWriter(cycle_dir)
        self.step_executor = StepExecutor(client, model, self.artifact_writer, templates_dir)
        self.beto_state_writer = BETOStateWriter(cycle_dir, ciclo_id)

    def ejecutar(self, paso_inicio: int = 0) -> Path:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_1_INICIO_CICLO
        BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_2_PIPELINE

        Ejecuta el pipeline de Pasos 0–9 desde paso_inicio.
        Retorna la ruta del directorio del ciclo (handoff).
        """
        paso = paso_inicio

        while paso <= 9:
            print(f"[Motor Razonamiento] Ejecutando Paso {paso}...")

            # BETO-TRACE: BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION
            artefactos = self.step_executor.ejecutar_paso(paso, self.idea_raw)

            # Registrar artefactos en Gestor de Ciclo
            # BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.ARTIFACT_REGISTRY
            for nombre in artefactos:
                self.state_manager.aplicar_evento(
                    self.ciclo_id,
                    "REGISTRAR_ARTEFACTO",
                    {
                        "paso": paso,
                        "nombre_artefacto": nombre,
                        "ruta_artefacto": str(self.cycle_dir / nombre),
                        "estado": "GENERADO",
                    },
                )

            self.state_manager.aplicar_evento(
                self.ciclo_id,
                "ACTUALIZAR_PASO",
                {"paso_actual": paso},
            )

            print(f"[Motor Razonamiento] Paso {paso} completado: {artefactos}")

            # Actualizar BETO_STATE con el conocimiento acumulado hasta este paso
            try:
                self.beto_state_writer.update(paso)
            except Exception as e:
                print(f"[BETO_STATE] Warning: update falló en paso {paso} — {e} (no bloquea)")

            # BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.GATES_G1_G2_G3
            # BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.GATE_PAUSER
            if paso in GATE_EN_PASO:
                gate_id = GATE_EN_PASO[paso]
                artefacto_principal = artefactos[0] if artefactos else f"Paso {paso}"

                señal = {
                    "paso_origen": gate_id,
                    "motor_origen": "MOTOR_RAZONAMIENTO",
                    "artefacto_generado": artefacto_principal,
                    "beto_gap_adjunto": None,
                }

                resultado = self.gates.procesar_gate(self.ciclo_id, señal)

                if resultado["señal_tipo"] == "RETROCESO":
                    # BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.RETROCESO_HANDLER
                    paso_retroceso = resultado["paso_retroceso_si_aplica"]
                    print(f"[Motor Razonamiento] Retroceso al Paso {paso_retroceso}")
                    paso = paso_retroceso
                    continue

                # Aprobado — continuar al siguiente paso
            paso += 1

        # — PHASE 3: Handoff —
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_3_HANDOFF
        return self._verificar_y_emitir_handoff()

    def _verificar_y_emitir_handoff(self) -> Path:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_3_HANDOFF
        BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.HANDOFF_PATH
        BETO-TRACE: BETO_MOTOR_RAZ.SEC1.INTENT.HANDOFF_TO_CODE

        Verifica que todos los artefactos de Pasos 0–9 están presentes
        y emite la señal de handoff (ruta del directorio del ciclo).
        """
        todos_presentes = True
        faltantes_total = []

        for paso in range(0, 10):
            _, faltantes = self.artifact_writer.verificar_artefactos_paso(paso)
            if faltantes:
                todos_presentes = False
                faltantes_total.extend(faltantes)

        if not todos_presentes:
            raise RuntimeError(
                f"Handoff fallido. Artefactos faltantes: {faltantes_total}"
            )

        print(f"[Motor Razonamiento] Handoff emitido: {self.cycle_dir}")
        return self.cycle_dir
