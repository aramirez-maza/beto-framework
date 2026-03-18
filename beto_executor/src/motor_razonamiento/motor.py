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
        execution_router=None,
        route_type: str = "",
    ):
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC3.INPUT.IDEA_RAW
        # BETO-TRACE: BETO_MOTOR_RAZ.SEC3.INPUT.CICLO_ID
        self.ciclo_id = ciclo_id
        self.idea_raw = idea_raw
        self.cycle_dir = cycle_dir
        self.state_manager = state_manager
        self.gates = gates_operador

        # BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
        # execution_router and route_type are optional — backward compatible with v4.3.
        # When provided, snapshots and PROJECT_INDEX are generated automatically.
        self.execution_router = execution_router
        self.route_type = route_type

        self.artifact_writer = ArtifactWriter(cycle_dir)
        self.step_executor = StepExecutor(client, model, self.artifact_writer, templates_dir)
        self.beto_state_writer = BETOStateWriter(cycle_dir, ciclo_id)

        # v4.4 operational artifacts — only active when execution_router is provided
        if self.execution_router is not None:
            from execution_router.snapshot_writer import SnapshotWriter
            from execution_router.project_index_writer import ProjectIndexWriter
            beto_dir = cycle_dir / ".beto"
            self._snapshot_writer = SnapshotWriter(beto_dir=beto_dir, ciclo_id=ciclo_id)
            self._project_index_writer = ProjectIndexWriter(beto_dir=beto_dir, ciclo_id=ciclo_id)
            # v4.5 dual-write writers
            from persistence.writers.snapshot_writer import SnapshotDBWriter
            from persistence.writers.oq_writer import OQWriter
            from persistence.writers.artifact_writer import ArtifactDBWriter
            self._snapshot_db_writer = SnapshotDBWriter(beto_dir=beto_dir, ciclo_id=ciclo_id)
            self._oq_writer = OQWriter(beto_dir=beto_dir, cycle_id=ciclo_id)
            self._artifact_db_writer = ArtifactDBWriter(beto_dir=beto_dir, cycle_id=ciclo_id)
        else:
            self._snapshot_writer = None
            self._project_index_writer = None
            self._snapshot_db_writer = None
            self._oq_writer = None
            self._artifact_db_writer = None

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
            # BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
            artefactos = self.step_executor.ejecutar_paso(paso, self.idea_raw, self.route_type)

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
                # v4.5 dual-write — artifact to DB
                if self._artifact_db_writer is not None:
                    try:
                        self._artifact_db_writer.write(
                            file_path=str(self.cycle_dir / nombre),
                            paso=paso,
                        )
                    except Exception as e:
                        print(f"[PERSISTENCE] Warning: artifact DB write failed for {nombre} — {e}")

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

            # v4.5 dual-write — sync OQs from BETO_STATE to DB
            if self._oq_writer is not None:
                try:
                    beto_state_path = self.cycle_dir / "BETO_STATE.json"
                    self._oq_writer.sync_from_beto_state(beto_state_path, paso)
                except Exception as e:
                    print(f"[PERSISTENCE] Warning: OQ sync failed at paso {paso} — {e}")

            # v4.4 — Snapshot generation (REGLA SNAPSHOT_INVALIDATION)
            # BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT
            if self._snapshot_writer is not None:
                self._emit_snapshots(paso, artefactos)

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
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS

        Verifica que todos los artefactos de Pasos 0–9 están presentes
        y emite la señal de handoff (ruta del directorio del ciclo).

        v4.4: Generates PROJECT_INDEX after successful verification.
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

        # v4.4 — Generate PROJECT_INDEX at handoff point
        # BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS
        if self._project_index_writer is not None:
            try:
                index_path = self._project_index_writer.write(
                    self.cycle_dir,
                    updated_by="materialization_executor",
                )
                self.state_manager.aplicar_evento(
                    self.ciclo_id,
                    "PROJECT_INDEX_UPDATED",
                    {
                        "project_index_path": str(index_path),
                        "updated_by": "materialization_executor",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                )
                print(f"[Motor Razonamiento] PROJECT_INDEX generado: {index_path}")
            except Exception as e:
                print(f"[PROJECT_INDEX] Warning: generación falló — {e} (no bloquea handoff)")

        print(f"[Motor Razonamiento] Handoff emitido: {self.cycle_dir}")
        return self.cycle_dir

    def _emit_snapshots(self, paso: int, artefactos: list[str]) -> None:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

        Emit context snapshots for the completed paso.
        Snapshot strategy per route_type and paso:
          LC — all pasos, all routes
          CS — after paso 4 (Gate G-2), PARTIAL/FULL only
          AQ — after paso 6 (cierre asistido), PARTIAL/FULL only
          MS — after paso 9 (pre-handoff), PARTIAL/FULL only
        """
        now = datetime.now(timezone.utc).isoformat()
        is_partial_or_full = self.route_type in ("BETO_PARTIAL_PATH", "BETO_FULL_PATH")

        # LC snapshot — always, all routes
        lc_id = self._snapshot_writer.write_lc_snapshot(paso, artefactos, self.route_type)
        self.state_manager.aplicar_evento(
            self.ciclo_id,
            "SNAPSHOT_CREATED",
            {
                "snapshot_id": lc_id,
                "snapshot_type": "LOCAL_EXECUTION_CONTEXT",
                "route_type": self.route_type,
                "timestamp": now,
            },
        )
        # v4.5 dual-write
        if self._snapshot_db_writer is not None:
            try:
                self._snapshot_db_writer.write(
                    snapshot_id=lc_id,
                    snapshot_type="LOCAL_EXECUTION_CONTEXT",
                    paso=paso,
                    route_type=self.route_type,
                    payload={"artifacts_generated": artefactos},
                )
            except Exception as e:
                print(f"[PERSISTENCE] Warning: LC snapshot DB write failed at paso {paso} — {e}")

        # CS snapshot — after paso 4, PARTIAL/FULL only
        if paso == 4 and is_partial_or_full:
            cs_id = self._snapshot_writer.write_cs_snapshot(paso, self.cycle_dir, self.route_type)
            self.state_manager.aplicar_evento(
                self.ciclo_id,
                "SNAPSHOT_CREATED",
                {
                    "snapshot_id": cs_id,
                    "snapshot_type": "CYCLE_CONTEXT_SNAPSHOT",
                    "route_type": self.route_type,
                    "timestamp": now,
                },
            )
            # v4.5 dual-write
            if self._snapshot_db_writer is not None:
                try:
                    artifacts_in_scope = sorted(
                        f.name for f in self.cycle_dir.glob("*.md") if f.is_file()
                    )
                    self._snapshot_db_writer.write(
                        snapshot_id=cs_id,
                        snapshot_type="CYCLE_CONTEXT_SNAPSHOT",
                        paso=paso,
                        route_type=self.route_type,
                        payload={
                            "artifacts_in_scope": artifacts_in_scope,
                            "beto_state_captured": (self.cycle_dir / "BETO_STATE.json").exists(),
                        },
                    )
                except Exception as e:
                    print(f"[PERSISTENCE] Warning: CS snapshot DB write failed — {e}")

        # AQ snapshot — after paso 6, PARTIAL/FULL only
        if paso == 6 and is_partial_or_full:
            aq_id = self._snapshot_writer.write_aq_snapshot(paso, self.cycle_dir, self.route_type)
            self.state_manager.aplicar_evento(
                self.ciclo_id,
                "SNAPSHOT_CREATED",
                {
                    "snapshot_id": aq_id,
                    "snapshot_type": "ACTIVE_OQ_SET",
                    "route_type": self.route_type,
                    "timestamp": now,
                },
            )
            # v4.5 dual-write
            if self._snapshot_db_writer is not None:
                try:
                    import json as _json
                    beto_state_path = self.cycle_dir / "BETO_STATE.json"
                    oqs_abiertas = []
                    if beto_state_path.exists():
                        state = _json.loads(beto_state_path.read_text(encoding="utf-8"))
                        oqs_abiertas = state.get("oqs_abiertas", [])
                    self._snapshot_db_writer.write(
                        snapshot_id=aq_id,
                        snapshot_type="ACTIVE_OQ_SET",
                        paso=paso,
                        route_type=self.route_type,
                        payload={"oqs_abiertas_count": len(oqs_abiertas)},
                    )
                except Exception as e:
                    print(f"[PERSISTENCE] Warning: AQ snapshot DB write failed — {e}")

        # MS snapshot — after paso 9, PARTIAL/FULL only
        if paso == 9 and is_partial_or_full:
            ms_id = self._snapshot_writer.write_ms_snapshot(paso, self.cycle_dir, self.route_type)
            self.state_manager.aplicar_evento(
                self.ciclo_id,
                "SNAPSHOT_CREATED",
                {
                    "snapshot_id": ms_id,
                    "snapshot_type": "MATERIALIZATION_SCOPE",
                    "route_type": self.route_type,
                    "timestamp": now,
                },
            )
            # v4.5 dual-write
            if self._snapshot_db_writer is not None:
                try:
                    scope_artifacts = sorted(
                        f.name for f in self.cycle_dir.glob("*.md") if f.is_file()
                    )
                    self._snapshot_db_writer.write(
                        snapshot_id=ms_id,
                        snapshot_type="MATERIALIZATION_SCOPE",
                        paso=paso,
                        route_type=self.route_type,
                        payload={
                            "scope_artifacts": scope_artifacts,
                            "manifest_present": (self.cycle_dir / "MANIFEST_PROYECTO.md").exists(),
                        },
                    )
                except Exception as e:
                    print(f"[PERSISTENCE] Warning: MS snapshot DB write failed — {e}")
