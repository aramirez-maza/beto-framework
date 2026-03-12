"""
BETO-TRACE: BETO_EXECUTOR.SEC1.INTENT.AUTOMATION_PIPELINE
BETO-TRACE: BETO_EXECUTOR.SEC6.MODEL.MOTOR_RAZONAMIENTO
BETO-TRACE: BETO_EXECUTOR.SEC6.MODEL.MOTOR_CODIGO
BETO-TRACE: BETO_EXECUTOR.SEC6.MODEL.GATES_OPERADOR
BETO-TRACE: BETO_EXECUTOR.SEC6.MODEL.GESTOR_CICLO
BETO-TRACE: BETO_EXECUTOR.SEC6.MODEL.HANDOFF
BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_1_INPUT_ELIGIBILITY
BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_2_SPEC_PIPELINE
BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_3_MATERIALIZATION
BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.TWO_MOTORS
BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.GATES_NON_NEGOTIABLE
"""

import shutil
from pathlib import Path

from openai import OpenAI

from gestor_ciclo.gestor import GestorCiclo
from gestor_ciclo.state_manager import StateManager
from gestor_ciclo.state_reader import StateReader
from gates_operador.decision_capturer import capturar_opcion_duplicado
from gates_operador.gates import GatesOperador
from motor_codigo.motor import MotorCodigo
from motor_razonamiento.motor import MotorRazonamiento


class BETOExecutorRoot:
    """
    BETO-TRACE: BETO_EXECUTOR.SEC1.INTENT.AUTOMATION_PIPELINE
    BETO-TRACE: BETO_EXECUTOR.SEC4.UNIT.CICLO_BETO

    Orquestador ROOT de BETO_EXECUTOR.
    Coordina el pipeline completo: Pasos 0–9 (Motor Razonamiento) →
    G-3 → Paso 10 (Motor Código) → FINALIZADO.
    """

    def __init__(self, config: dict):
        """
        BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.SYSTEM_CONFIG
        BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
        BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE
        BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.PERSISTENCE_JSON_CYCLE_DIR

        config keys:
            cycle_output_dir: str — directorio base para los ciclos
            reasoning_model: str — modelo LLM para razonamiento (Pasos 0-9 + scaffolds)
            code_model: str — modelo LLM para código (implementa scaffolds)
            litellm_base_url: str — base URL del LiteLLM gateway
            api_key: str — API key para el gateway (master key de LiteLLM)
            g4_configurado: bool — activar gate G-4 opcional (default: False)
            code_output_subdir: str — subdirectorio para código generado (default: 'src')
        """
        self.cycle_output_dir = Path(config["cycle_output_dir"])

        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE
        self.reasoning_model = config["reasoning_model"]
        self.code_model = config["code_model"]
        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.G4_OPTIONAL
        self.g4_configurado = config.get("g4_configurado", False)
        self.code_output_subdir = config.get("code_output_subdir", "src")

        # Directorio de templates del framework BETO
        # Si no se declara, el motor funciona sin templates (modo degradado)
        templates_dir_raw = config.get("templates_dir")
        self.templates_dir = Path(templates_dir_raw) if templates_dir_raw else None

        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
        # Un único cliente apunta al gateway — LiteLLM rutea por model name
        self.client = OpenAI(
            base_url=config.get("litellm_base_url", "http://localhost:8000"),
            api_key=config.get("api_key", "none"),
        )
        # Mismo cliente para ambos motores — el routing es responsabilidad del gateway
        self.reasoning_client = self.client
        self.code_client = self.client

    def ejecutar(self, idea_raw: str) -> Path:
        """
        BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_1_INPUT_ELIGIBILITY
        BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_2_SPEC_PIPELINE
        BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_3_MATERIALIZATION
        BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.IDEA_RAW
        BETO-TRACE: BETO_EXECUTOR.SEC4.FIELD.IDEA_RAW

        Ejecuta el pipeline BETO completo sobre la IDEA_RAW.
        Retorna el directorio con el sistema materializado.
        """
        # — PHASE 1: Input & Eligibility —
        # BETO-TRACE: BETO_EXECUTOR.SEC2.BOUNDARY.IDEA_RAW_RECEPTION
        print("[ROOT] Iniciando ciclo BETO_EXECUTOR")
        print(f"[ROOT] IDEA_RAW: {idea_raw[:80]}{'...' if len(idea_raw) > 80 else ''}")

        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.PERSISTENCE_JSON_CYCLE_DIR
        gestor = GestorCiclo(self.cycle_output_dir)
        resultado_creacion = gestor.crear_ciclo(idea_raw)

        if resultado_creacion["duplicate"] is not None:
            # BETO-TRACE: BETO_EXECUTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION
            dup = resultado_creacion["duplicate"]
            print(f"\n[ROOT] Ciclo duplicado detectado: {dup['ciclo_id']} (Paso {dup['paso_actual']})")
            opcion = capturar_opcion_duplicado()

            if opcion == "reanudar":
                return self._reanudar(dup["ciclo_id"], idea_raw)
            else:
                ciclo_id = gestor.crear_ciclo_nuevo_ignorando_duplicado(idea_raw)
        else:
            ciclo_id = resultado_creacion["ciclo_id"]

        # BETO-TRACE: BETO_EXECUTOR.SEC4.FIELD.CICLO_ID
        print(f"[ROOT] Ciclo iniciado: {ciclo_id}")

        cycle_dir = self.cycle_output_dir / ciclo_id
        cycle_dir.mkdir(parents=True, exist_ok=True)

        state_manager = StateManager(self.cycle_output_dir)
        gates = GatesOperador(state_manager, cycle_dir=cycle_dir)

        # — PHASE 2: Specification Pipeline (Pasos 0–9) —
        # BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_2_SPEC_PIPELINE
        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.TWO_MOTORS
        motor_raz = MotorRazonamiento(
            ciclo_id=ciclo_id,
            idea_raw=idea_raw,
            cycle_dir=cycle_dir,
            client=self.client,
            model=self.reasoning_model,
            state_manager=state_manager,
            gates_operador=gates,
            templates_dir=self.templates_dir,
        )

        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.GATES_NON_NEGOTIABLE
        # G-1, G-2, G-3 son gestionados internamente por MotorRazonamiento
        handoff_path = motor_raz.ejecutar(paso_inicio=0)

        # — PHASE 3: Materialization (Paso 10) —
        # BETO-TRACE: BETO_EXECUTOR.SEC7.PHASE.PHASE_3_MATERIALIZATION
        # BETO-TRACE: BETO_EXECUTOR.SEC6.MODEL.HANDOFF
        print(f"[ROOT] Handoff recibido: {handoff_path}")
        # Copiar GENERATOR_RULES al cycle_dir (auditabilidad + RULE_003)
        _src_rules = Path(__file__).parent.parent.parent / "GENERATOR_RULES_BETO_EXECUTOR.md"
        if _src_rules.exists():
            shutil.copy2(_src_rules, handoff_path / "GENERATOR_RULES_BETO_EXECUTOR.md")

        output_dir = cycle_dir / self.code_output_subdir


        motor_cod = MotorCodigo(
            ciclo_id=ciclo_id,
            handoff_path=handoff_path,
            output_dir=output_dir,
            code_client=self.code_client,
            code_model=self.code_model,
            state_manager=state_manager,
            gates_operador=gates,
            g4_configurado=self.g4_configurado,
        )

        result_dir = motor_cod.ejecutar()

        # Marcar ciclo como FINALIZADO
        # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.FINALIZED_CYCLES_ON_DISK
        state_manager.marcar_finalizado(ciclo_id)
        print(f"[ROOT] Ciclo {ciclo_id} FINALIZADO.")
        print(f"[ROOT] Sistema materializado en: {result_dir}")

        return result_dir

    def _reanudar(self, ciclo_id: str, idea_raw: str) -> Path:
        """
        BETO-TRACE: BETO_EXECUTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION
        BETO-TRACE: BETO_GESTOR.SEC1.INTENT.RESUMPTION

        Reanuda un ciclo interrumpido desde su punto de gate.
        """
        state_reader = StateReader(self.cycle_output_dir)
        info = state_reader.resolver_reanudacion(ciclo_id)

        paso_reanudacion = info["paso_reanudacion"]
        motor_destino = info["motor_destino"]
        print(f"[ROOT] Reanudando ciclo {ciclo_id} desde Paso {paso_reanudacion} ({motor_destino})")

        cycle_dir = self.cycle_output_dir / ciclo_id
        state_manager = StateManager(self.cycle_output_dir)
        gates = GatesOperador(state_manager, cycle_dir=cycle_dir)

        if motor_destino == "MOTOR_RAZONAMIENTO":
            motor_raz = MotorRazonamiento(
                ciclo_id=ciclo_id,
                idea_raw=idea_raw,
                cycle_dir=cycle_dir,
                client=self.client,
                model=self.reasoning_model,
                state_manager=state_manager,
                gates_operador=gates,
                templates_dir=self.templates_dir,
            )
            handoff_path = motor_raz.ejecutar(paso_inicio=paso_reanudacion)
        else:
            handoff_path = cycle_dir

        # Copiar GENERATOR_RULES al cycle_dir (auditabilidad + RULE_003)
        _src_rules = Path(__file__).parent.parent.parent / "GENERATOR_RULES_BETO_EXECUTOR.md"
        if _src_rules.exists():
            shutil.copy2(_src_rules, handoff_path / "GENERATOR_RULES_BETO_EXECUTOR.md")

        output_dir = cycle_dir / self.code_output_subdir
        motor_cod = MotorCodigo(
            ciclo_id=ciclo_id,
            handoff_path=handoff_path,
            output_dir=output_dir,
            code_client=self.code_client,
            code_model=self.code_model,
            state_manager=state_manager,
            gates_operador=gates,
            g4_configurado=self.g4_configurado,
        )

        result_dir = motor_cod.ejecutar()
        state_manager.marcar_finalizado(ciclo_id)
        return result_dir
