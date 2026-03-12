"""
BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.MATERIALIZATION_PLAN
BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.PLAN_BUILDER
BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.NO_UNDECLARED_FILES
"""

from dataclasses import dataclass, field


@dataclass
class EntradaPlan:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC4.UNIT.ARCHIVO_MATERIALIZACION
    Entrada del plan de materialización para un archivo de código.
    """
    orden: int
    nodo: str
    nombre_archivo: str
    beto_core_origen: str
    trace_registry_ref: str
    # Símbolos principales del archivo: clase(s) y/o funciones a implementar
    stub_symbols: str = ""
    # IDs BETO-TRACE directamente relevantes para este archivo específico
    primary_ids: list = field(default_factory=list)


# BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.MATERIALIZATION_PLAN
# BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.NO_UNDECLARED_FILES
# Plan fijo derivado del MANIFEST_PROYECTO.md, ordenado por dependencias.
PLAN_MATERIALIZACION: list[EntradaPlan] = [

    # — Núcleo: GESTOR_CICLO —
    EntradaPlan(
        orden=1, nodo="GESTOR_CICLO",
        nombre_archivo="gestor_ciclo/duplicate_detector.py",
        beto_core_origen="BETO_CORE_GESTOR_CICLO.md",
        trace_registry_ref="TRACE_REGISTRY_GESTOR_CICLO.md",
        stub_symbols="funcs: compute_idea_raw_hash(idea_raw: str) -> str, find_duplicate(idea_raw: str, cycle_output_dir: Path) -> dict | None",
        primary_ids=[
            "BETO_GESTOR.SEC1.INTENT.DUPLICATE_DETECTION",
            "BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_COMPARISON",
            "BETO_GESTOR.SEC3.INPUT.IDEA_RAW",
            "BETO_GESTOR.SEC3.OUTPUT.DUPLICATE_RESULT",
            "BETO_GESTOR.SEC6.MODEL.DUPLICATE_DETECTOR",
            "BETO_GESTOR.SEC8.DECISION.DUPLICATE_SHA256",
        ],
    ),
    EntradaPlan(
        orden=2, nodo="GESTOR_CICLO",
        nombre_archivo="gestor_ciclo/gestor.py",
        beto_core_origen="BETO_CORE_GESTOR_CICLO.md",
        trace_registry_ref="TRACE_REGISTRY_GESTOR_CICLO.md",
        stub_symbols="class GestorCiclo: __init__(cycle_output_dir), crear_ciclo(idea_raw) -> dict, crear_ciclo_nuevo_ignorando_duplicado(idea_raw) -> str, _persist(ciclo_id, state), get_cycle_dir(ciclo_id) -> Path",
        primary_ids=[
            "BETO_GESTOR.SEC1.INTENT.CICLO_ID_GENERATION",
            "BETO_GESTOR.SEC1.INTENT.CYCLE_STATE_PERSISTENCE",
            "BETO_GESTOR.SEC1.INTENT.DUPLICATE_DETECTION",
            "BETO_GESTOR.SEC2.BOUNDARY.CICLO_ID_CREATION",
            "BETO_GESTOR.SEC2.BOUNDARY.INITIAL_STATE_PERSISTENCE",
            "BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_COMPARISON",
            "BETO_GESTOR.SEC2.BOUNDARY.RESUME_NEW_OPTION",
            "BETO_GESTOR.SEC3.INPUT.IDEA_RAW",
            "BETO_GESTOR.SEC3.OUTPUT.CICLO_ID",
            "BETO_GESTOR.SEC3.OUTPUT.INITIAL_STATE",
            "BETO_GESTOR.SEC3.OUTPUT.DUPLICATE_RESULT",
            "BETO_GESTOR.SEC6.MODEL.CICLO_CREATOR",
            "BETO_GESTOR.SEC7.PHASE.PHASE_1_CREACION_CICLO",
            "BETO_GESTOR.SEC8.DECISION.CICLO_ID_UUID",
            "BETO_GESTOR.SEC8.DECISION.DUPLICATE_SHA256",
            "BETO_GESTOR.SEC8.DECISION.JSON_BACKEND",
            "BETO_GESTOR.SEC8.DECISION.FINALIZED_ON_DISK",
        ],
    ),
    EntradaPlan(
        orden=3, nodo="GESTOR_CICLO",
        nombre_archivo="gestor_ciclo/state_manager.py",
        beto_core_origen="BETO_CORE_GESTOR_CICLO.md",
        trace_registry_ref="TRACE_REGISTRY_GESTOR_CICLO.md",
        stub_symbols="class StateManager: __init__(cycle_output_dir), aplicar_evento(ciclo_id, tipo_evento, payload), marcar_finalizado(ciclo_id), _read(ciclo_id) -> dict, _persist(ciclo_id, state)",
        primary_ids=[
            "BETO_GESTOR.SEC1.INTENT.STATE_SERIALIZATION",
            "BETO_GESTOR.SEC1.INTENT.CYCLE_STATE_PERSISTENCE",
            "BETO_GESTOR.SEC2.BOUNDARY.STATE_UPDATES",
            "BETO_GESTOR.SEC2.BOUNDARY.GATE_DECISION_REGISTRATION",
            "BETO_GESTOR.SEC3.INPUT.UPDATE_EVENT",
            "BETO_GESTOR.SEC3.OUTPUT.CURRENT_STATE",
            "BETO_GESTOR.SEC4.FIELD.TIPO_EVENTO",
            "BETO_GESTOR.SEC4.FIELD.PAYLOAD",
            "BETO_GESTOR.SEC5.INVARIANT.NON_DESTRUCTIVE",
            "BETO_GESTOR.SEC5.INVARIANT.CICLO_ID_IMMUTABLE",
            "BETO_GESTOR.SEC5.INVARIANT.IDEA_RAW_IMMUTABLE",
            "BETO_GESTOR.SEC6.MODEL.STATE_UPDATER",
            "BETO_GESTOR.SEC7.PHASE.PHASE_2_GESTION_ESTADO",
            "BETO_GESTOR.SEC8.DECISION.NON_DESTRUCTIVE_UPDATES",
            "BETO_GESTOR.SEC8.DECISION.WRITE_BEFORE_CONFIRM",
            "BETO_GESTOR.SEC8.DECISION.JSON_BACKEND",
        ],
    ),
    EntradaPlan(
        orden=4, nodo="GESTOR_CICLO",
        nombre_archivo="gestor_ciclo/state_reader.py",
        beto_core_origen="BETO_CORE_GESTOR_CICLO.md",
        trace_registry_ref="TRACE_REGISTRY_GESTOR_CICLO.md",
        stub_symbols="class StateReader: __init__(cycle_output_dir), leer(ciclo_id) -> dict, resolver_reanudacion(ciclo_id) -> dict, _read(ciclo_id) -> dict",
        primary_ids=[
            "BETO_GESTOR.SEC1.INTENT.RESUMPTION",
            "BETO_GESTOR.SEC2.BOUNDARY.STATE_READ",
            "BETO_GESTOR.SEC2.BOUNDARY.RESUMPTION_HANDOVER",
            "BETO_GESTOR.SEC3.INPUT.READ_REQUEST",
            "BETO_GESTOR.SEC3.INPUT.RESUME_REQUEST",
            "BETO_GESTOR.SEC3.OUTPUT.CURRENT_STATE",
            "BETO_GESTOR.SEC3.OUTPUT.RESUME_STATE",
            "BETO_GESTOR.SEC6.MODEL.RESUMPTION_HANDLER",
            "BETO_GESTOR.SEC7.PHASE.PHASE_3_LECTURA_REANUDACION",
            "BETO_GESTOR.SEC8.DECISION.MOTOR_BY_STEP",
            "BETO_GESTOR.SEC8.DECISION.RESUME_POINTS_AT_GATES",
            "BETO_GESTOR.SEC8.DECISION.CURRENT_STATE_ONLY",
        ],
    ),

    # — GATES_OPERADOR —
    EntradaPlan(
        orden=5, nodo="GATES_OPERADOR",
        nombre_archivo="gates_operador/cli_presenter.py",
        beto_core_origen="BETO_CORE_GATES_OPERADOR.md",
        trace_registry_ref="TRACE_REGISTRY_GATES_OPERADOR.md",
        stub_symbols="funcs: presentar_gate(señal: dict), presentar_gap(gap: dict)",
        primary_ids=[
            "BETO_GATES.SEC1.INTENT.PRESENT_GATE_INFO",
            "BETO_GATES.SEC1.INTENT.PRESENT_BETO_GAP",
            "BETO_GATES.SEC2.BOUNDARY.CLI_PRESENTATION",
            "BETO_GATES.SEC2.BOUNDARY.GAP_PRESENTATION",
            "BETO_GATES.SEC3.OUTPUT.OPERATOR_DECISION",
            "BETO_GATES.SEC6.MODEL.CLI_INTERFACE",
            "BETO_GATES.SEC6.MODEL.GAP_PRESENTER",
            "BETO_GATES.SEC7.PHASE.PHASE_2_PRESENTACION_CAPTURA",
            "BETO_GATES.SEC8.DECISION.CLI_STDIN_STDOUT",
        ],
    ),
    EntradaPlan(
        orden=6, nodo="GATES_OPERADOR",
        nombre_archivo="gates_operador/decision_capturer.py",
        beto_core_origen="BETO_CORE_GATES_OPERADOR.md",
        trace_registry_ref="TRACE_REGISTRY_GATES_OPERADOR.md",
        stub_symbols="funcs: capturar_decision(gate_id: str) -> dict, capturar_resolucion_gap(gap_id: str) -> dict, capturar_opcion_duplicado() -> str",
        primary_ids=[
            "BETO_GATES.SEC1.INTENT.CAPTURE_OPERATOR_DECISION",
            "BETO_GATES.SEC2.BOUNDARY.DECISION_CAPTURE",
            "BETO_GATES.SEC3.INPUT.CLI_STDIN",
            "BETO_GATES.SEC3.OUTPUT.OPERATOR_DECISION",
            "BETO_GATES.SEC3.OUTPUT.OPERATOR_JUSTIFICATION",
            "BETO_GATES.SEC3.OUTPUT.GAP_RESOLUTION_DECLARATION",
            "BETO_GATES.SEC5.INVARIANT.OPERATOR_DECISION_IMMUTABLE",
            "BETO_GATES.SEC5.INVARIANT.NO_AUTO_APPROVAL",
            "BETO_GATES.SEC7.PHASE.PHASE_2_PRESENTACION_CAPTURA",
            "BETO_GATES.SEC8.DECISION.CLI_STDIN_STDOUT",
            "BETO_GATES.SEC8.DECISION.GATE_SUSPEND_WITHOUT_TIMEOUT",
        ],
    ),
    EntradaPlan(
        orden=7, nodo="GATES_OPERADOR",
        nombre_archivo="gates_operador/retroceso_resolver.py",
        beto_core_origen="BETO_CORE_GATES_OPERADOR.md",
        trace_registry_ref="TRACE_REGISTRY_GATES_OPERADOR.md",
        stub_symbols="class BETOGapEscalado(Exception); funcs: determinar_paso_retroceso(gate_id: str, justificacion: str) -> int, _extraer_paso_de_justificacion(justificacion: str) -> int | None",
        primary_ids=[
            "BETO_GATES.SEC2.BOUNDARY.RETROCESO_DETERMINATION",
            "BETO_GATES.SEC3.OUTPUT.RETROCESO_SIGNAL",
            "BETO_GATES.SEC6.MODEL.RETROCESO_TABLE",
            "BETO_GATES.SEC8.DECISION.RETROCESO_G1",
            "BETO_GATES.SEC8.DECISION.RETROCESO_G2",
            "BETO_GATES.SEC8.DECISION.RETROCESO_G3",
            "BETO_GATES.SEC8.DECISION.RETROCESO_G4",
            "BETO_GATES.SEC8.DECISION.G3_JUSTIFICATION_REQUIRED",
        ],
    ),
    EntradaPlan(
        orden=8, nodo="GATES_OPERADOR",
        nombre_archivo="gates_operador/gates.py",
        beto_core_origen="BETO_CORE_GATES_OPERADOR.md",
        trace_registry_ref="TRACE_REGISTRY_GATES_OPERADOR.md",
        stub_symbols="class GatesOperador: __init__(state_manager), procesar_gate(ciclo_id, señal: dict) -> dict, _validar_señal(señal: dict)",
        primary_ids=[
            "BETO_GATES.SEC1.INTENT.OPERATOR_GATE_MANAGEMENT",
            "BETO_GATES.SEC1.INTENT.RESOLVE_GATE",
            "BETO_GATES.SEC2.BOUNDARY.GATE_SIGNAL_RECEPTION",
            "BETO_GATES.SEC2.BOUNDARY.SIGNAL_VALIDATION",
            "BETO_GATES.SEC2.BOUNDARY.GATE_STATE_REGISTRATION",
            "BETO_GATES.SEC2.BOUNDARY.SIGNAL_EMISSION",
            "BETO_GATES.SEC3.INPUT.GATE_SIGNAL",
            "BETO_GATES.SEC3.INPUT.CICLO_ID",
            "BETO_GATES.SEC3.OUTPUT.CONTINUATION_SIGNAL",
            "BETO_GATES.SEC3.OUTPUT.RETROCESO_SIGNAL",
            "BETO_GATES.SEC3.OUTPUT.GATE_STATE_REGISTERED",
            "BETO_GATES.SEC4.UNIT.GATE_EVENT",
            "BETO_GATES.SEC6.MODEL.SIGNAL_RECEIVER",
            "BETO_GATES.SEC7.PHASE.PHASE_1_RECEPCION_SEÑAL",
            "BETO_GATES.SEC7.PHASE.PHASE_3_RESOLUCION_GATE",
            "BETO_GATES.SEC8.DECISION.GATES_G1_G2_G3_G4",
        ],
    ),

    # — MOTOR_RAZONAMIENTO —
    EntradaPlan(
        orden=9, nodo="MOTOR_RAZONAMIENTO",
        nombre_archivo="motor_razonamiento/context_builder.py",
        beto_core_origen="BETO_CORE_MOTOR_RAZONAMIENTO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_RAZONAMIENTO.md",
        stub_symbols="funcs: construir_contexto(paso: int, idea_raw: str, cycle_dir: Path) -> str, artefactos_requeridos_para_paso(paso: int) -> list[str]",
        primary_ids=[
            "BETO_MOTOR_RAZ.SEC6.MODEL.CONTEXT_BUILDER",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.PASOS_2_9_PIPELINE",
            "BETO_MOTOR_RAZ.SEC4.FIELD.LLM_CONTEXT",
            "BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP",
            "BETO_MOTOR_RAZ.SEC3.INPUT.IDEA_RAW",
            "BETO_MOTOR_RAZ.SEC3.INPUT.CICLO_ID",
            "BETO_MOTOR_RAZ.SEC3.INPUT.CYCLE_DIRECTORY",
        ],
    ),
    EntradaPlan(
        orden=10, nodo="MOTOR_RAZONAMIENTO",
        nombre_archivo="motor_razonamiento/artifact_writer.py",
        beto_core_origen="BETO_CORE_MOTOR_RAZONAMIENTO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_RAZONAMIENTO.md",
        stub_symbols="class ArtifactWriter: __init__(cycle_dir: Path), escribir(nombre: str, contenido: str, paso: int), artefactos_existentes() -> list[str], verificar_artefactos_paso(paso: int) -> bool",
        primary_ids=[
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.ARTIFACT_WRITE",
            "BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_CORE_DRAFT",
            "BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_SYSTEM_GRAPH",
            "BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_CORES_CLOSED",
            "BETO_MOTOR_RAZ.SEC3.OUTPUT.PHASE_DOCUMENTS",
            "BETO_MOTOR_RAZ.SEC3.OUTPUT.MANIFESTS_REGISTRIES",
            "BETO_MOTOR_RAZ.SEC6.MODEL.ARTIFACT_REGISTRY",
            "BETO_MOTOR_RAZ.SEC8.DECISION.ARTIFACTS_TO_CYCLE_DIR",
            "BETO_MOTOR_RAZ.SEC5.INVARIANT.NON_DESTRUCTIVE",
        ],
    ),
    EntradaPlan(
        orden=11, nodo="MOTOR_RAZONAMIENTO",
        nombre_archivo="motor_razonamiento/step_executor.py",
        beto_core_origen="BETO_CORE_MOTOR_RAZONAMIENTO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_RAZONAMIENTO.md",
        stub_symbols="class StepExecutor: __init__(client, model), ejecutar_paso(paso: int, context: str) -> str; funcs: _separar_artefactos(raw_output: str) -> list[dict]",
        primary_ids=[
            "BETO_MOTOR_RAZ.SEC1.INTENT.EXECUTE_BETO_STEPS_0_9",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.PASO0_ELIGIBILITY",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.PASO1_CORE_DRAFT",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.PASOS_2_9_PIPELINE",
            "BETO_MOTOR_RAZ.SEC4.UNIT.PASO_EJECUCION",
            "BETO_MOTOR_RAZ.SEC4.FIELD.PASO_ID",
            "BETO_MOTOR_RAZ.SEC4.FIELD.ARTEFACTO_GENERADO",
            "BETO_MOTOR_RAZ.SEC4.FIELD.ESTADO_PASO",
            "BETO_MOTOR_RAZ.SEC6.MODEL.STEP_SEQUENCER",
            "BETO_MOTOR_RAZ.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE",
            "BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP",
        ],
    ),
    EntradaPlan(
        orden=12, nodo="MOTOR_RAZONAMIENTO",
        nombre_archivo="motor_razonamiento/motor.py",
        beto_core_origen="BETO_CORE_MOTOR_RAZONAMIENTO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_RAZONAMIENTO.md",
        stub_symbols="class MotorRazonamiento: __init__(ciclo_id, idea_raw, cycle_dir, client, model, state_manager, gates_operador), ejecutar(paso_inicio: int) -> Path, _verificar_y_emitir_handoff() -> Path",
        primary_ids=[
            "BETO_MOTOR_RAZ.SEC1.INTENT.EXECUTE_BETO_STEPS_0_9",
            "BETO_MOTOR_RAZ.SEC1.INTENT.PRODUCE_CLOSED_SPEC",
            "BETO_MOTOR_RAZ.SEC1.INTENT.GATE_SIGNALING",
            "BETO_MOTOR_RAZ.SEC1.INTENT.HANDOFF_TO_CODE",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.GATE_SIGNAL_G1",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.GATE_SIGNAL_G2",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.GATE_SIGNAL_G3",
            "BETO_MOTOR_RAZ.SEC2.BOUNDARY.HANDOFF_SIGNAL",
            "BETO_MOTOR_RAZ.SEC3.INPUT.GATE_DECISION",
            "BETO_MOTOR_RAZ.SEC3.INPUT.RETROCESO_SIGNAL",
            "BETO_MOTOR_RAZ.SEC3.OUTPUT.HANDOFF_PATH",
            "BETO_MOTOR_RAZ.SEC6.MODEL.GATE_PAUSER",
            "BETO_MOTOR_RAZ.SEC6.MODEL.RETROCESO_HANDLER",
            "BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_1_INICIO_CICLO",
            "BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_2_PIPELINE",
            "BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_3_HANDOFF",
            "BETO_MOTOR_RAZ.SEC8.DECISION.GATES_G1_G2_G3",
        ],
    ),

    # — MOTOR_CODIGO —
    EntradaPlan(
        orden=13, nodo="MOTOR_CODIGO",
        nombre_archivo="motor_codigo/handoff_reader.py",
        beto_core_origen="BETO_CORE_MOTOR_CODIGO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_CODIGO.md",
        stub_symbols="class HandoffReader: __init__(handoff_path), validar() -> tuple[bool, list[str]], leer_artefacto(nombre: str) -> str, leer_trace_registry(nombre_nodo: str) -> str, leer_beto_core(nombre_nodo: str) -> str",
        primary_ids=[
            "BETO_MOTOR_COD.SEC1.INTENT.OPERATE_ON_CLOSED_SPEC",
            "BETO_MOTOR_COD.SEC2.BOUNDARY.HANDOFF_READ",
            "BETO_MOTOR_COD.SEC2.BOUNDARY.ARTIFACT_VALIDATION",
            "BETO_MOTOR_COD.SEC3.INPUT.HANDOFF_PATH",
            "BETO_MOTOR_COD.SEC3.INPUT.BETO_CORES",
            "BETO_MOTOR_COD.SEC3.INPUT.TRACE_REGISTRIES",
            "BETO_MOTOR_COD.SEC6.MODEL.HANDOFF_READER",
            "BETO_MOTOR_COD.SEC7.PHASE.PHASE_1_LECTURA_HANDOFF",
        ],
    ),
    EntradaPlan(
        orden=14, nodo="MOTOR_CODIGO",
        nombre_archivo="motor_codigo/plan_builder.py",
        beto_core_origen="BETO_CORE_MOTOR_CODIGO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_CODIGO.md",
        stub_symbols="@dataclass class EntradaPlan: orden, nodo, nombre_archivo, beto_core_origen, trace_registry_ref, stub_symbols, primary_ids; funcs: obtener_plan() -> list[EntradaPlan]",
        primary_ids=[
            "BETO_MOTOR_COD.SEC2.BOUNDARY.MATERIALIZATION_PLAN",
            "BETO_MOTOR_COD.SEC4.UNIT.ARCHIVO_MATERIALIZACION",
            "BETO_MOTOR_COD.SEC4.FIELD.NOMBRE_ARCHIVO",
            "BETO_MOTOR_COD.SEC4.FIELD.BETO_CORE_ORIGEN",
            "BETO_MOTOR_COD.SEC4.FIELD.TRACE_REGISTRY_REF",
            "BETO_MOTOR_COD.SEC5.INVARIANT.NO_UNDECLARED_FILES",
            "BETO_MOTOR_COD.SEC6.MODEL.PLAN_BUILDER",
        ],
    ),
    EntradaPlan(
        orden=15, nodo="MOTOR_CODIGO",
        nombre_archivo="motor_codigo/trace_verifier.py",
        beto_core_origen="BETO_CORE_MOTOR_CODIGO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_CODIGO.md",
        stub_symbols="funcs: extraer_trace_ids(texto: str) -> list[str], extraer_ids_autorizados_de_registry(registry_content: str) -> set[str], verificar_archivo(codigo, registry_content, nombre_archivo) -> dict, verificar_preservacion(scaffold, codigo_final, nombre_archivo) -> dict",
        primary_ids=[
            "BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION",
            "BETO_MOTOR_COD.SEC4.FIELD.BETO_TRACE_IDS",
            "BETO_MOTOR_COD.SEC4.FIELD.ESTADO_ARCHIVO",
            "BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED",
            "BETO_MOTOR_COD.SEC6.MODEL.TRACE_VERIFIER",
        ],
    ),
    EntradaPlan(
        orden=16, nodo="MOTOR_CODIGO",
        nombre_archivo="motor_codigo/file_generator.py",
        beto_core_origen="BETO_CORE_MOTOR_CODIGO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_CODIGO.md",
        stub_symbols="funcs: _strip_code_fences(text: str) -> str; class FileGenerator: __init__(code_client, code_model), generar(entrada, idea_raw, beto_core, trace_registry) -> tuple[str, str], _build_scaffold_from_manifest(entrada, trace_registry) -> str, _implementar_scaffold(entrada, scaffold, idea_raw, beto_core, trace_registry) -> str",
        primary_ids=[
            "BETO_MOTOR_COD.SEC2.BOUNDARY.CODE_GENERATION",
            "BETO_MOTOR_COD.SEC6.MODEL.FILE_GENERATOR",
            "BETO_MOTOR_COD.SEC6.MODEL.CONTEXT_PER_FILE",
            "BETO_MOTOR_COD.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE",
            "BETO_MOTOR_COD.SEC8.DECISION.CODE_MODEL_CONFIGURABLE",
            "BETO_MOTOR_COD.SEC8.DECISION.CONTEXT_PER_FILE",
        ],
    ),
    EntradaPlan(
        orden=17, nodo="MOTOR_CODIGO",
        nombre_archivo="motor_codigo/motor.py",
        beto_core_origen="BETO_CORE_MOTOR_CODIGO.md",
        trace_registry_ref="TRACE_REGISTRY_MOTOR_CODIGO.md",
        stub_symbols="class MotorCodigo: __init__(ciclo_id, handoff_path, output_dir, code_client, code_model, state_manager, gates_operador, g4_configurado), ejecutar() -> Path, _registrar_gap(entrada, detalle), _entrega(archivos_trace_verified) -> Path",
        primary_ids=[
            "BETO_MOTOR_COD.SEC1.INTENT.EXECUTE_PASO10",
            "BETO_MOTOR_COD.SEC1.INTENT.PRODUCE_TRACE_VERIFIED_FILES",
            "BETO_MOTOR_COD.SEC2.BOUNDARY.CODE_GENERATION",
            "BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION",
            "BETO_MOTOR_COD.SEC2.BOUNDARY.GATE_G4_OPTIONAL",
            "BETO_MOTOR_COD.SEC2.BOUNDARY.FINALIZATION_SIGNAL",
            "BETO_MOTOR_COD.SEC3.OUTPUT.MATERIALIZED_FILES",
            "BETO_MOTOR_COD.SEC3.OUTPUT.FINALIZATION_SIGNAL",
            "BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED",
            "BETO_MOTOR_COD.SEC7.PHASE.PHASE_1_LECTURA_HANDOFF",
            "BETO_MOTOR_COD.SEC7.PHASE.PHASE_2_MATERIALIZACION",
            "BETO_MOTOR_COD.SEC7.PHASE.PHASE_3_ENTREGA",
            "BETO_MOTOR_COD.SEC8.DECISION.TRACE_VERIFIED_GATE",
            "BETO_MOTOR_COD.SEC8.DECISION.G4_OPTIONAL",
        ],
    ),

    # — ROOT —
    EntradaPlan(
        orden=18, nodo="ROOT",
        nombre_archivo="orquestador/root.py",
        beto_core_origen="BETO_CORE_DRAFT.md",
        trace_registry_ref="TRACE_REGISTRY_BETO_EXECUTOR.md",
        stub_symbols="class BETOExecutorRoot: __init__(config: dict), ejecutar(idea_raw: str) -> Path, _reanudar(ciclo_id: str, idea_raw: str) -> Path",
        primary_ids=[
            "BETO_EXECUTOR.SEC1.INTENT.AUTOMATION_PIPELINE",
            "BETO_EXECUTOR.SEC2.BOUNDARY.IDEA_RAW_RECEPTION",
            "BETO_EXECUTOR.SEC2.BOUNDARY.SPEC_PIPELINE",
            "BETO_EXECUTOR.SEC2.BOUNDARY.MATERIALIZATION",
            "BETO_EXECUTOR.SEC2.BOUNDARY.DUPLICATE_DETECTION",
            "BETO_EXECUTOR.SEC3.INPUT.IDEA_RAW",
            "BETO_EXECUTOR.SEC3.INPUT.SYSTEM_CONFIG",
            "BETO_EXECUTOR.SEC3.OUTPUT.MATERIALIZED_SYSTEM",
            "BETO_EXECUTOR.SEC4.UNIT.CICLO_BETO",
            "BETO_EXECUTOR.SEC6.MODEL.MOTOR_RAZONAMIENTO",
            "BETO_EXECUTOR.SEC6.MODEL.MOTOR_CODIGO",
            "BETO_EXECUTOR.SEC6.MODEL.GATES_OPERADOR",
            "BETO_EXECUTOR.SEC6.MODEL.GESTOR_CICLO",
            "BETO_EXECUTOR.SEC6.MODEL.HANDOFF",
            "BETO_EXECUTOR.SEC7.PHASE.PHASE_1_INPUT_ELIGIBILITY",
            "BETO_EXECUTOR.SEC7.PHASE.PHASE_2_SPEC_PIPELINE",
            "BETO_EXECUTOR.SEC7.PHASE.PHASE_3_MATERIALIZATION",
            "BETO_EXECUTOR.SEC8.DECISION.TWO_MOTORS",
            "BETO_EXECUTOR.SEC8.DECISION.GATES_NON_NEGOTIABLE",
            "BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE",
            "BETO_EXECUTOR.SEC8.DECISION.HANDOFF_CYCLE_DIRECTORY",
        ],
    ),
    EntradaPlan(
        orden=19, nodo="ROOT",
        nombre_archivo="main.py",
        beto_core_origen="BETO_CORE_DRAFT.md",
        trace_registry_ref="TRACE_REGISTRY_BETO_EXECUTOR.md",
        stub_symbols="funcs: main() — CLI entry point: parsea argumentos (--idea, --idea-file, --config, --cycle-dir, --reasoning-model, --code-model, --litellm-url, --api-key, --g4), construye config dict, instancia BETOExecutorRoot y llama ejecutar(idea_raw)",
        primary_ids=[
            "BETO_EXECUTOR.SEC2.BOUNDARY.IDEA_RAW_RECEPTION",
            "BETO_EXECUTOR.SEC3.INPUT.IDEA_RAW",
            "BETO_EXECUTOR.SEC3.INPUT.SYSTEM_CONFIG",
            "BETO_EXECUTOR.SEC8.DECISION.OPERATOR_CLI_STDIN_STDOUT",
            "BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE",
        ],
    ),
]


def obtener_plan(handoff_path=None) -> list[EntradaPlan]:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.PLAN_BUILDER
    BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.NO_UNDECLARED_FILES

    Construye el plan de materialización.
    Si handoff_path contiene MANIFEST_PROYECTO.md, lo lee dinámicamente.
    Fallback: plan hardcodeado del BETO_EXECUTOR.
    """
    if handoff_path is not None:
        from pathlib import Path
        manifest = Path(handoff_path) / "MANIFEST_PROYECTO.md"
        if manifest.exists():
            plan = _build_dynamic_plan(manifest, Path(handoff_path))
            if plan:
                print(f"[Plan] Dinámico: {len(plan)} archivos desde MANIFEST_PROYECTO.md")
                return plan
            print("[Plan] MANIFEST_PROYECTO.md encontrado pero no parseable — usando plan hardcodeado")
    return sorted(PLAN_MATERIALIZACION, key=lambda e: e.orden)


def _build_dynamic_plan(manifest_path, handoff_path) -> list[EntradaPlan]:
    """
    Lee MANIFEST_PROYECTO.md y construye el plan dinámicamente.
    Soporta dos formatos:
    - Tabla sección 1.2: una fila por archivo (todo-list style)
    - Tablas WAVE: múltiples archivos por fila en columna "Archivos" (v2 style)
    """
    import re

    content = manifest_path.read_text(encoding="utf-8")

    # Estrategia: extraer todos los paths de código del documento
    # Soporta tablas sección 1.2 (una fila/archivo) y tablas WAVE (múltiples por fila)
    archivos_vistos = []
    seen = set()

    for line in content.split("\n"):
        if not "|" in line and not "`" in line:
            continue
        # Saltar líneas de header de tabla
        if re.match(r"\s*\|[-\s|]+\|\s*$", line):
            continue
        # Extraer todos los paths con extensión dentro de backticks
        for m in re.finditer(r"`([^`]+\.(py|yaml|yml|toml|json|html|css|js|md|txt|cfg|ini))`", line):
            nombre = m.group(1)
            # Saltar si parece artefacto BETO (todo caps o empieza con BETO/TRACE/MANIFEST/PHASE)
            if re.match(r"(BETO_|TRACE_|MANIFEST_|PHASE_|PASO_|CIERRE)", nombre):
                continue
            # Saltar headers
            if nombre.lower() in ("archivo", "file", "archivos", "files"):
                continue
            if nombre not in seen:
                seen.add(nombre)
                # Intentar extraer nodo de la misma fila
                cols = [c.strip() for c in line.split("|") if c.strip()]
                nodo = ""
                for col in cols:
                    if re.search(r"P-\d+|N-\d+", col):
                        nodo = re.search(r"P-\d+[\.\d]*|N-\d+", col).group(0)
                        break
                archivos_vistos.append({"nombre": nombre, "nodo": nodo, "desc": ""})

    if not archivos_vistos:
        # Estrategia 2: derivar archivos Python desde BETO_COREs listados en SECCIÓN 8
        archivos_vistos = _derivar_desde_seccion8(content)
        if not archivos_vistos:
            return []

    # Descubrir BETO_COREs y TRACE_REGISTRYs disponibles
    beto_cores = sorted(p.name for p in handoff_path.glob("BETO_CORE_*.md"))
    registries = sorted(p.name for p in handoff_path.glob("TRACE_REGISTRY_*.md"))

    # Índice del plan hardcodeado para recuperar stub_symbols cuando el archivo coincide
    hardcoded_index = {e.nombre_archivo: e for e in PLAN_MATERIALIZACION}

    plan = []
    for i, f in enumerate(archivos_vistos, 1):
        nombre = f["nombre"]
        nodo = f["nodo"]

        # Si el archivo coincide exactamente con el plan hardcodeado, usar sus metadatos ricos
        if nombre in hardcoded_index:
            entrada = hardcoded_index[nombre]
            plan.append(EntradaPlan(
                orden=i,
                nodo=entrada.nodo,
                nombre_archivo=nombre,
                beto_core_origen=entrada.beto_core_origen,
                trace_registry_ref=entrada.trace_registry_ref,
                stub_symbols=entrada.stub_symbols,
                primary_ids=entrada.primary_ids,
            ))
            continue

        # Sistema distinto al executor: asignar BETO_CORE y TRACE_REGISTRY por nombre
        beto_core = _match_artifact(nombre, nodo, beto_cores, "BETO_CORE_DRAFT.md")
        trace_reg = _match_artifact(nombre, nodo, registries, registries[0] if registries else "")

        plan.append(EntradaPlan(
            orden=i,
            nodo=nodo,
            nombre_archivo=nombre,
            beto_core_origen=beto_core,
            trace_registry_ref=trace_reg,
            stub_symbols="",   # LLM implementa libremente desde BETO_CORE
            primary_ids=[],    # Sin BETO-TRACE forzado para sistemas externos
        ))

    return plan


def _derivar_desde_seccion8(content: str) -> list[dict]:
    """
    Estrategia 2: cuando no hay .py en backticks, extrae BETO_CORE_*.md de SECCIÓN 8
    y deriva rutas Python usando la convención: BETO_CORE_X.md → x/x.py
    """
    import re

    # Localizar SECCIÓN 8
    m = re.search(r"(?i)SECCI[ÓO]N\s+8", content)
    if not m:
        return []

    seccion8 = content[m.start():]
    # Limitar al bloque de sección 8 (hasta siguiente ## SECCIÓN o final)
    next_sec = re.search(r"\n##\s+SECCI", seccion8[10:])
    if next_sec:
        seccion8 = seccion8[:next_sec.start() + 10]

    # Extraer referencias a BETO_CORE_*.md (excluir BETO_CORE_DRAFT.md = ROOT)
    cores_encontrados = []
    seen = set()
    for m in re.finditer(r"BETO_CORE_([A-Z0-9_]+)\.md", seccion8):
        slug_upper = m.group(1)
        if slug_upper in ("DRAFT",):
            continue
        if slug_upper not in seen:
            seen.add(slug_upper)
            slug = slug_upper.lower()
            python_path = f"{slug}/{slug}.py"
            cores_encontrados.append({"nombre": python_path, "nodo": slug_upper, "desc": ""})

    return cores_encontrados


def _match_artifact(nombre_archivo: str, nodo: str, candidates: list, fallback: str) -> str:
    """
    Elige el artefacto (BETO_CORE o TRACE_REGISTRY) más afín al archivo dado.
    Estrategia: match por slug en nombre del archivo o nodo. Fallback al primer candidato.
    """
    if not candidates:
        return fallback
    nombre_lower = nombre_archivo.lower().replace("/", "_").replace(".", "_")
    nodo_lower = nodo.lower()
    for cand in candidates:
        slug = cand.lower().replace("beto_core_", "").replace("trace_registry_", "").replace(".md", "")
        if slug in nombre_lower or slug in nodo_lower:
            return cand
    # Preferir no-DRAFT si hay opciones
    non_draft = [c for c in candidates if "DRAFT" not in c.upper()]
    return non_draft[0] if non_draft else candidates[0]
