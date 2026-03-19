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
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

from gestor_ciclo.gestor import GestorCiclo
from gestor_ciclo.state_manager import StateManager
from gestor_ciclo.state_reader import StateReader
from gates_operador.decision_capturer import capturar_opcion_duplicado
from gates_operador.gates import GatesOperador
from motor_codigo.motor import MotorCodigo
from motor_razonamiento.motor import MotorRazonamiento
from execution_router import ExecutionRouter, ComplexityFactors
from persistence import init_db
from persistence.writers.cycle_writer import CycleWriter


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
        self.auto_approve = config.get("auto_approve", False)
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
        gates = GatesOperador(state_manager, cycle_dir=cycle_dir, auto_approve=self.auto_approve)

        # — v4.4: Initial routing at cycle start —
        # BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
        # BETO-TRACE: BETO_V44.SEC9.ROUTING_DECISION.RECORD
        beto_dir = cycle_dir / ".beto"

        # — v4.5: Initialize SQLite persistence layer —
        # BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
        # BETO-TRACE: BETO_V45.SEC8.DECISION.CYCLE_BEFORE_ROUTING_FK
        # Cycle row is written BEFORE execution_router.route() so that the FK
        # on routing_decisions(cycle_id) is satisfied when the dual-write fires.
        try:
            init_db(beto_dir)
            project_id = CycleWriter.ensure_project(beto_dir, self.cycle_output_dir)
            CycleWriter.write_cycle(
                beto_dir=beto_dir,
                project_id=project_id,
                cycle_id=ciclo_id,
                idea_raw=idea_raw,
                cycle_dir=cycle_dir,
                reasoning_model=self.reasoning_model,
                code_model=self.code_model,
                g4_configured=self.g4_configurado,
            )
        except Exception as e:
            print(f"[PERSISTENCE] Warning: DB init/cycle write failed — {e} (continuing without DB)")
            project_id = None

        execution_router = ExecutionRouter(cycle_id=ciclo_id, beto_dir=beto_dir)
        initial_factors = self._estimate_complexity_factors(idea_raw)
        routing_decision = execution_router.route(
            factors=initial_factors,
            subproblem_description=idea_raw[:200],
            step_context="paso_0_eligibility",
            executor_assigned="eligibility_executor",
            trace_anchor=f"{ciclo_id}.SEC1.INTENT.CYCLE_START",
            justification=(
                "Initial routing at cycle start — heuristic estimate from idea_raw. "
                "May be promoted during execution if scope expands."
            ),
        )
        route_type = routing_decision.route_selected.value
        print(f"[ROOT] Ruta inicial: {route_type} (score={routing_decision.raw_score:.1f})")

        # Update cycle with route info now that routing is resolved
        if project_id is not None:
            try:
                CycleWriter.write_cycle(
                    beto_dir=beto_dir,
                    project_id=project_id,
                    cycle_id=ciclo_id,
                    idea_raw=idea_raw,
                    cycle_dir=cycle_dir,
                    route_type=route_type,
                    complexity_score=routing_decision.raw_score,
                    reasoning_model=self.reasoning_model,
                    code_model=self.code_model,
                    g4_configured=self.g4_configurado,
                )
            except Exception as e:
                print(f"[PERSISTENCE] Warning: cycle route update failed — {e}")

        state_manager.aplicar_evento(
            ciclo_id,
            "ROUTING_DECISION_REGISTERED",
            {
                "decision_id": routing_decision.decision_id,
                "route_selected": route_type,
                "raw_score": routing_decision.raw_score,
                "step_context": "paso_0_eligibility",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

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
            execution_router=execution_router,
            route_type=route_type,
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
        if not _src_rules.exists():
            raise RuntimeError(
                f"GENERATOR_RULES ausente: {_src_rules}\n"
                "Coloca GENERATOR_RULES_BETO_EXECUTOR.md en beto_executor/ antes de ejecutar. (RULE_003)"
            )
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
        gates = GatesOperador(state_manager, cycle_dir=cycle_dir, auto_approve=self.auto_approve)

        if motor_destino == "MOTOR_RAZONAMIENTO":
            # v4.4 — restore routing context for resumed cycle
            beto_dir = cycle_dir / ".beto"
            # v4.5 — ensure DB is initialized. Write cycle row BEFORE routing
            # so the FK on routing_decisions(cycle_id) is satisfied.
            try:
                init_db(beto_dir)
                project_id = CycleWriter.ensure_project(beto_dir, self.cycle_output_dir)
                CycleWriter.write_cycle(
                    beto_dir=beto_dir,
                    project_id=project_id,
                    cycle_id=ciclo_id,
                    idea_raw=idea_raw,
                    cycle_dir=cycle_dir,
                    reasoning_model=self.reasoning_model,
                    code_model=self.code_model,
                    g4_configured=self.g4_configurado,
                )
            except Exception as e:
                print(f"[PERSISTENCE] Warning: DB init failed on resume — {e}")
                project_id = None
            execution_router = ExecutionRouter(cycle_id=ciclo_id, beto_dir=beto_dir)
            initial_factors = self._estimate_complexity_factors(idea_raw)
            routing_decision = execution_router.route(
                factors=initial_factors,
                subproblem_description=idea_raw[:200],
                step_context=f"paso_{paso_reanudacion}_reanudacion",
                executor_assigned="eligibility_executor",
                trace_anchor=f"{ciclo_id}.SEC1.INTENT.CYCLE_RESUME",
                justification=(
                    f"Routing restored at cycle resumption from paso {paso_reanudacion}."
                ),
            )
            route_type = routing_decision.route_selected.value
            print(f"[ROOT] Ruta reanudada: {route_type} (score={routing_decision.raw_score:.1f})")
            # Update cycle with resolved route info
            if project_id is not None:
                try:
                    CycleWriter.write_cycle(
                        beto_dir=beto_dir,
                        project_id=project_id,
                        cycle_id=ciclo_id,
                        idea_raw=idea_raw,
                        cycle_dir=cycle_dir,
                        route_type=route_type,
                        complexity_score=routing_decision.raw_score,
                        reasoning_model=self.reasoning_model,
                        code_model=self.code_model,
                        g4_configured=self.g4_configurado,
                    )
                except Exception as e:
                    print(f"[PERSISTENCE] Warning: cycle route update failed on resume — {e}")

            motor_raz = MotorRazonamiento(
                ciclo_id=ciclo_id,
                idea_raw=idea_raw,
                cycle_dir=cycle_dir,
                client=self.client,
                model=self.reasoning_model,
                state_manager=state_manager,
                gates_operador=gates,
                templates_dir=self.templates_dir,
                execution_router=execution_router,
                route_type=route_type,
            )
            handoff_path = motor_raz.ejecutar(paso_inicio=paso_reanudacion)
        else:
            handoff_path = cycle_dir

        # Copiar GENERATOR_RULES al cycle_dir (auditabilidad + RULE_003)
        _src_rules = Path(__file__).parent.parent.parent / "GENERATOR_RULES_BETO_EXECUTOR.md"
        if not _src_rules.exists():
            raise RuntimeError(
                f"GENERATOR_RULES ausente: {_src_rules}\n"
                "Coloca GENERATOR_RULES_BETO_EXECUTOR.md en beto_executor/ antes de ejecutar. (RULE_003)"
            )
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

    def _estimate_complexity_factors(self, idea_raw: str) -> ComplexityFactors:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
        BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_THRESHOLDS

        Heuristic estimation of complexity factors from idea_raw text.
        This is a conservative estimate at cycle start — may be promoted via
        ROUTE_PROMOTED during execution if scope expands (REGLA ROUTE_PROMOTION).

        Not an invention: the BETO_FULL_PATH executor always runs the full
        11-step protocol. The routing controls which context layers are loaded
        and which snapshots are generated — not whether steps are skipped.
        """
        text = idea_raw.lower()

        # ─── Signals ───────────────────────────────────────────────────────────
        # Single-artifact signals (→ LIGHT)
        single_keywords = {
            "función", "funcion", "function", "método", "metodo", "method",
            "clase", "class", "script", "archivo", "file",
        }
        # Modification signals (→ PARTIAL)
        modification_keywords = {
            "agrega", "añade", "aniade", "modifica", "actualiza", "integra",
            "add", "append", "update", "modify", "integrate", "extend",
            "logging", "log", "logs",
        }
        # Multi-component signals (→ FULL)
        system_keywords = {
            "sistema", "system", "arquitectura", "architecture",
            "múltiples", "multiples", "múltiple", "multiple",
            "componentes", "components", "módulos", "modulos", "modules",
            "simulación", "simulacion", "simulation",
        }

        is_single = any(k in text for k in single_keywords)
        is_modification = any(k in text for k in modification_keywords)
        is_system = any(k in text for k in system_keywords)

        # Prefer: system > modification > single
        if is_system:
            is_single = False
            is_modification = False
        elif is_modification:
            is_single = False

        # ─── Factor estimation ─────────────────────────────────────────────────
        if is_single and not is_modification and not is_system:
            # LIGHT candidate
            num_outputs = 1
            num_entities = 1
            num_dependencies = 0
            ambiguity_level = 1
            need_for_graph = 0
            oq_critical_count = 0
            cross_module_scope = 0
            lifecycle_scope = 0
        elif is_modification and not is_system:
            # PARTIAL candidate
            num_outputs = 3
            num_entities = 1
            num_dependencies = 3
            ambiguity_level = 1
            need_for_graph = 0
            oq_critical_count = 1
            cross_module_scope = 0
            lifecycle_scope = 0
        else:
            # FULL candidate (default — conservative)
            num_outputs = 5
            num_entities = 5
            num_dependencies = 4
            ambiguity_level = 2
            need_for_graph = 1
            oq_critical_count = 3
            cross_module_scope = 1
            lifecycle_scope = 1

        return ComplexityFactors(
            num_outputs=num_outputs,
            num_entities=num_entities,
            num_dependencies=num_dependencies,
            ambiguity_level=ambiguity_level,
            need_for_graph=need_for_graph,
            oq_critical_count=oq_critical_count,
            cross_module_scope=cross_module_scope,
            lifecycle_scope=lifecycle_scope,
        )
