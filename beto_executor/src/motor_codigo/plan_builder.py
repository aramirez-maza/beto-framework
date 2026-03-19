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
    Builds a cross-module-aware materialization plan from MANIFEST_PROYECTO.md
    and TRACE_REGISTRY files.

    Improvement over the original version:
    - Parses SEC4.FIELD entries → identifies shared data model (e.g. FileEntry)
    - Parses SEC6.COMPONENT entries → derives module interface specs
    - Parses SEC7.PHASE entries → extracts input/output contracts
    - Assigns shared model ownership to the first producer module
    - Injects import stubs into all consumer modules
    - Result: LLM receives explicit interface contracts per file, preventing
      shared type duplication across modules.
    """
    content = manifest_path.read_text(encoding="utf-8")

    # --- Phase 1: Extract file list ---
    archivos_vistos = _extract_files_from_manifest(content)
    if not archivos_vistos:
        archivos_vistos = _derivar_desde_seccion8(content)
    if not archivos_vistos:
        return []

    # --- Phase 2: Discover artifacts ---
    beto_cores = sorted(p.name for p in handoff_path.glob("BETO_CORE_*.md"))
    registry_paths = sorted(handoff_path.glob("TRACE_REGISTRY_*.md"))
    registry_names = [p.name for p in registry_paths]

    # Executor self-spec shortcut
    hardcoded_index = {e.nombre_archivo: e for e in PLAN_MATERIALIZACION}

    # --- Phase 3: Parse TRACE_REGISTRY entries ---
    all_entries: dict = {}
    for reg_path in registry_paths:
        try:
            all_entries.update(_parse_registry_entries(reg_path.read_text(encoding="utf-8")))
        except Exception:
            pass
    all_ids: set = set(all_entries.keys())

    # Group by section type
    sec4_fields = {id_: d for id_, d in all_entries.items() if ".SEC4.FIELD." in id_}
    sec6 = {id_: d for id_, d in all_entries.items()
            if ".SEC6.COMPONENT." in id_ or ".SEC6.MODEL." in id_}
    sec7 = {id_: d for id_, d in all_entries.items() if ".SEC7.PHASE." in id_}

    # --- Phase 4: Identify shared data model from fields + components ---
    shared_model = _identify_shared_model(sec4_fields, sec6)

    # --- Phase 5: Find which file owns the shared model ---
    if shared_model:
        owner_file = _find_shared_model_owner(archivos_vistos, sec6, sec7, shared_model)
        shared_model["owner_file"] = owner_file

    # --- Phase 6: Assemble plan with cross-module awareness ---
    plan = []
    for i, f in enumerate(archivos_vistos, 1):
        nombre = f["nombre"]
        nodo = f.get("nodo", "")

        # Executor self-spec: use rich hardcoded metadata
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

        beto_core = _match_artifact(nombre, nodo, beto_cores, "BETO_CORE_DRAFT.md")
        trace_reg = _match_artifact(nombre, nodo, registry_names,
                                    registry_names[0] if registry_names else "")

        is_owner = bool(shared_model and shared_model.get("owner_file") == nombre)
        stub = _build_stub_symbols(nombre, sec6, sec7, shared_model, is_owner, all_ids)
        primary = _select_primary_ids_dynamic(nombre, all_ids)

        plan.append(EntradaPlan(
            orden=i,
            nodo=nodo,
            nombre_archivo=nombre,
            beto_core_origen=beto_core,
            trace_registry_ref=trace_reg,
            stub_symbols=stub,
            primary_ids=primary,
        ))

    return plan


# ---------------------------------------------------------------------------
# Registry parser
# ---------------------------------------------------------------------------

def _parse_registry_entries(content: str) -> dict:
    """
    Parse a TRACE_REGISTRY.md and extract all ID entries.

    Format (inside ``` code blocks):
      ID: SYSTEM.SECn.TYPE.ELEMENT
        Source section: ...
        Declaration: text that may span
                     multiple lines
        Input:  text  (SEC7 only)
        Output: text  (SEC7 only)
        Status: ...

    Returns: {id_string: {declaration, input, output}}
    """
    import re

    entries: dict = {}
    code_blocks = re.findall(r"```[^\n]*\n(.*?)```", content, re.DOTALL)
    for block in code_blocks:
        parts = re.split(r"(?m)^ID:\s+", block)
        for part in parts[1:]:
            lines = part.strip().split("\n")
            if not lines:
                continue
            id_ = lines[0].strip()
            # IDs have no spaces; skip malformed lines
            if not id_ or " " in id_:
                continue
            data: dict = {"declaration": "", "input": "", "output": ""}
            current_key = None
            current_val: list = []

            for line in lines[1:]:
                stripped = line.strip()
                if not stripped:
                    continue
                lc = stripped.lower()
                if lc.startswith("declaration:"):
                    if current_key:
                        data[current_key] = " ".join(current_val).strip()
                    current_key = "declaration"
                    current_val = [stripped[12:].strip()]
                elif lc.startswith("input:"):
                    if current_key:
                        data[current_key] = " ".join(current_val).strip()
                    current_key = "input"
                    current_val = [stripped[6:].strip()]
                elif lc.startswith("output:"):
                    if current_key:
                        data[current_key] = " ".join(current_val).strip()
                    current_key = "output"
                    current_val = [stripped[7:].strip()]
                elif (lc.startswith("status:") or lc.startswith("source section:")
                      or lc.startswith("traceability") or lc.startswith("oq reference:")):
                    if current_key:
                        data[current_key] = " ".join(current_val).strip()
                    current_key = None
                    current_val = []
                elif current_key is not None:
                    current_val.append(stripped)

            if current_key:
                data[current_key] = " ".join(current_val).strip()
            entries[id_] = data

    return entries


# ---------------------------------------------------------------------------
# Shared model identification
# ---------------------------------------------------------------------------

def _identify_shared_model(sec4_fields: dict, sec6: dict) -> "dict | None":
    """
    Identify the shared data model from SEC4.FIELD and SEC6 entries.

    - SEC4.FIELD entries define the fields of the core unit of processing
    - A SEC6 component ending in _ENTRY, _RECORD, _ITEM etc. names the class
    - Returns: {class_name, fields, component_id, owner_file} or None
    """
    import re

    if not sec4_fields:
        return None

    # Field names from SEC4.FIELD IDs
    fields = [id_.split(".")[-1].lower() for id_ in sorted(sec4_fields.keys())]
    if not fields:
        return None

    # Look for a data-structure SEC6 component to derive class name
    data_struct_pat = re.compile(r"(_ENTRY|_RECORD|_ITEM|_UNIT|_OBJECT|_ENTITY|_NODE|_STRUCT)$")
    class_name = None
    struct_comp_id = None
    for id_ in sec6:
        element = id_.split(".")[-1]
        if data_struct_pat.search(element):
            class_name = "".join(w.capitalize() for w in element.split("_"))
            struct_comp_id = id_
            break

    if class_name is None:
        # Derive from first field: file_path → FileEntry
        first = fields[0].split("_")[0].capitalize() if fields else "Data"
        class_name = f"{first}Entry"

    return {
        "class_name": class_name,
        "fields": fields,
        "component_id": struct_comp_id,
        "owner_file": None,  # filled by _find_shared_model_owner
    }


_STOP_WORDS = {
    "a", "an", "the", "of", "in", "for", "to", "and", "or", "is", "its",
    "by", "that", "each", "any", "as", "on", "at", "be", "are", "with",
    "from", "this", "it", "not", "more", "than", "one", "only", "all",
    "has", "have", "can", "no", "into", "their", "which",
}


def _decl_tokens(text: str) -> set:
    """Extract meaningful lowercase tokens from a declaration/description text."""
    import re
    tokens = set(re.findall(r"[a-z]+", text.lower()))
    return tokens - _STOP_WORDS


def _camel_split(name: str) -> list:
    """Split a CamelCase name into lowercase tokens. 'FileEntry' → ['file', 'entry']."""
    import re
    return [t.lower() for t in re.findall(r"[A-Z][a-z]*", name) if len(t) > 2]


def _find_shared_model_owner(
    archivos_vistos: list, sec6: dict, sec7: dict, shared_model: dict
) -> "str | None":
    """
    Find which file defines (owns) the shared data model.

    Strategy:
    1. Find the SEC6 component whose declaration (a) mentions the model AND (b)
       contains a production verb ("produces", "creates", "generates", "output").
       This component is the producer/owner.
    2. Match that component slug to a file.
    3. Fallback: first phase that produces the model → match to file by full
       declaration-text overlap between phase and component declarations.
    4. Final fallback: first file that slug-matches a non-data-struct component.
    """
    import re

    # Split CamelCase class name into searchable tokens ("FileEntry" → ["file", "entry"])
    name_tokens = _camel_split(shared_model["class_name"])
    if not name_tokens:
        name_tokens = [t for t in re.findall(r"[a-z]+", shared_model["class_name"].lower()) if len(t) > 3]

    produce_verbs = {"produces", "produce", "creates", "create", "generates", "generate", "output", "outputs"}
    data_struct_pat = re.compile(r"(_ENTRY|_RECORD|_ITEM|_UNIT|_OBJECT|_ENTITY)$")

    # Step 1: Find the SEC6 component that PRODUCES the shared model
    # Criterion: declaration mentions the model tokens AND a production verb
    best_comp_el: "str | None" = None
    best_score = 0
    for comp_id, comp_data in sec6.items():
        comp_el = comp_id.split(".")[-1]
        if data_struct_pat.search(comp_el):
            continue
        decl = comp_data.get("declaration", "").lower()
        tokens = _decl_tokens(decl)
        mentions_model = any(tok in decl for tok in name_tokens)
        mentions_produce = bool(tokens & produce_verbs)
        if mentions_model and mentions_produce:
            score = sum(1 for tok in name_tokens if tok in decl)
            if score > best_score:
                best_score = score
                best_comp_el = comp_el

    if best_comp_el:
        owner = _match_component_slug_to_file(best_comp_el, archivos_vistos)
        if owner:
            return owner

    # Step 2: Fallback — find producing phase, then match phase to component by
    # full declaration-text overlap
    producing: list = []
    for phase_id, phase_data in sec7.items():
        out_text = phase_data.get("output", "").lower()
        decl_text = phase_data.get("declaration", "").lower()
        if any(tok in out_text or tok in decl_text for tok in name_tokens):
            el = phase_id.split(".")[-1]
            m = re.search(r"(\d+)", el)
            order = int(m.group(1)) if m else 99
            producing.append((order, phase_data, el))

    if producing:
        producing.sort(key=lambda x: x[0])
        first_phase_data = producing[0][1]
        phase_tokens = _decl_tokens(
            first_phase_data.get("declaration", "") + " " +
            first_phase_data.get("output", "")
        )
        # Find SEC6 component with highest declaration-text overlap with this phase
        best_comp_el = None
        best_overlap = 0
        for comp_id, comp_data in sec6.items():
            comp_el = comp_id.split(".")[-1]
            if data_struct_pat.search(comp_el):
                continue
            comp_tokens = _decl_tokens(comp_data.get("declaration", ""))
            overlap = len(phase_tokens & comp_tokens)
            if overlap > best_overlap:
                best_overlap = overlap
                best_comp_el = comp_el

        if best_comp_el:
            owner = _match_component_slug_to_file(best_comp_el, archivos_vistos)
            if owner:
                return owner

    # Final fallback: first file that slug-matches any processing component
    for f in archivos_vistos:
        base = f["nombre"].split("/")[-1].replace(".py", "").upper()
        for comp_id in sec6:
            el = comp_id.split(".")[-1]
            if data_struct_pat.search(el):
                continue
            if el == base or base in el or el in base:
                return f["nombre"]

    return archivos_vistos[0]["nombre"] if archivos_vistos else None


def _match_component_slug_to_file(component_element: str, archivos_vistos: list) -> "str | None":
    """Match a component name (e.g., SCANNER) to a file path by slug overlap."""
    import re
    data_struct_pat = re.compile(r"(_ENTRY|_RECORD|_ITEM|_UNIT|_OBJECT|_ENTITY)$")
    if data_struct_pat.search(component_element):
        return None
    for f in archivos_vistos:
        base = f["nombre"].split("/")[-1].replace(".py", "").upper()
        if base == component_element or component_element in base or base in component_element:
            return f["nombre"]
    return None


# ---------------------------------------------------------------------------
# Stub builder
# ---------------------------------------------------------------------------

def _build_stub_symbols(
    nombre: str,
    sec6: dict,
    sec7: dict,
    shared_model: "dict | None",
    is_owner: bool,
    all_ids: set,
) -> str:
    """
    Build a rich stub_symbols string with cross-module awareness.

    Output example:
    "import: from scanner.scanner import FileEntry; class DuplicateDetector: detect(entries: list[FileEntry]) -> dict"
    """
    parts: list = []
    base = nombre.split("/")[-1].replace(".py", "").upper()
    is_entry_point = base in ("MAIN", "APP", "CLI", "RUN", "ENTRYPOINT", "__MAIN__")

    # --- 1. Shared model: define (owner) or import (consumer) ---
    if shared_model:
        class_name = shared_model["class_name"]
        owner_file = shared_model.get("owner_file")
        if is_owner:
            fields = ", ".join(shared_model["fields"])
            parts.append(f"@dataclass class {class_name}: {fields}")
        elif not is_entry_point and owner_file:
            # Check if this file's phase uses the shared model as input
            if _file_phase_uses_model(base, sec6, sec7, shared_model):
                owner_module = owner_file.replace("/", ".").replace(".py", "")
                parts.append(f"import: from {owner_module} import {class_name}")

    # --- 2. Derive class/function stub from SEC6 + SEC7 ---
    if is_entry_point:
        parts.append("funcs: main() \u2014 CLI entry point: parse args, orchestrate pipeline, emit report")
    else:
        comp_stub = _derive_stub_from_component_and_phases(base, sec6, sec7, shared_model)
        if comp_stub:
            parts.append(comp_stub)

    return "; ".join(parts)


def _file_phase_uses_model(
    base: str, sec6: dict, sec7: dict, shared_model: dict
) -> bool:
    """Return True if this file's matching phase has the shared model in its input."""
    import re

    # Split "FileEntry" → ["file", "entry"] so we can match "file entries" in declarations
    name_tokens = _camel_split(shared_model["class_name"])
    if not name_tokens:
        name_tokens = [t for t in re.findall(r"[a-z]+", shared_model["class_name"].lower()) if len(t) > 3]
    data_struct_pat = re.compile(r"(_ENTRY|_RECORD|_ITEM|_UNIT|_OBJECT|_ENTITY)$")

    # Find the matching SEC6 component for this file
    best_comp_id: "str | None" = None
    best_score = 0
    for comp_id in sec6:
        el = comp_id.split(".")[-1]
        if data_struct_pat.search(el):
            continue
        score = 10 if el == base else (len(base) if base in el else (len(el) if el in base else 0))
        if score > best_score:
            best_score = score
            best_comp_id = comp_id

    if not best_comp_id:
        return False

    # Find the phase that best matches this component using full declaration text
    comp_decl = sec6[best_comp_id].get("declaration", "")
    comp_tokens = _decl_tokens(comp_decl + " " + base.replace("_", " "))
    best_phase: "dict | None" = None
    best_overlap = 0
    for phase_id, phase_data in sec7.items():
        phase_tokens = _decl_tokens(
            phase_data.get("declaration", "") + " " + phase_data.get("input", "")
        )
        overlap = len(comp_tokens & phase_tokens)
        if overlap > best_overlap:
            best_overlap = overlap
            best_phase = phase_data

    if best_phase:
        inp = best_phase.get("input", "").lower()
        return any(tok in inp for tok in name_tokens)
    return False


def _derive_stub_from_component_and_phases(
    base: str, sec6: dict, sec7: dict, shared_model: "dict | None"
) -> str:
    """
    Derive a stub_symbols fragment (class or funcs) from SEC6 component + SEC7 phase.

    base: uppercase base name of the file, e.g. SCANNER, DUPLICATE_DETECTOR
    Returns: e.g. "class Scanner: scan(directory: str) -> list[FileEntry]"
    or "" if no suitable component is found.

    Phase matching uses full declaration-text overlap (not element-token overlap)
    so that vocabulary-mismatched names (SCANNER ↔ DISCOVERY) resolve correctly.
    """
    import re

    class_hint = shared_model["class_name"] if shared_model else "Entry"
    data_struct_pat = re.compile(r"(_ENTRY|_RECORD|_ITEM|_UNIT|_OBJECT|_ENTITY)$")

    # --- Find best matching SEC6 component by slug ---
    best_comp_id: "str | None" = None
    best_score = 0
    for comp_id in sec6:
        el = comp_id.split(".")[-1]
        if data_struct_pat.search(el):
            continue
        score = 0
        if el == base:
            score = 10
        elif base in el:
            score = len(base)
        elif el in base:
            score = len(el)
        if score > best_score:
            best_score = score
            best_comp_id = comp_id

    if not best_comp_id:
        # No matching SEC6 component — fall back to phase name matching
        # e.g. hasher.py → HASHING phase
        base_tokens = _decl_tokens(base.replace("_", " "))
        best_phase: "dict | None" = None
        best_overlap = 0
        for phase_id, phase_data in sec7.items():
            ph_el_tokens = _decl_tokens(phase_id.split(".")[-1].replace("_", " "))
            overlap = len(base_tokens & ph_el_tokens)
            if overlap > best_overlap:
                best_overlap = overlap
                best_phase = phase_data
        if best_phase and best_overlap > 0:
            inp = best_phase.get("input", "").lower()
            out = best_phase.get("output", "").lower()
            method = _infer_method_name(base)
            input_sig = _infer_input_sig(inp, class_hint)
            output_type = _infer_output_type(out, class_hint)
            return f"funcs: {method}({input_sig}) -> {output_type}"
        return ""  # Unknown file type — let LLM infer from BETO_CORE

    comp_el = best_comp_id.split(".")[-1]
    class_name = "".join(w.capitalize() for w in comp_el.split("_"))

    # --- Find matching SEC7 phase using full declaration-text overlap ---
    # Component declaration + file base → match against all phase text
    comp_decl = sec6[best_comp_id].get("declaration", "")
    comp_text_tokens = _decl_tokens(comp_decl + " " + comp_el.replace("_", " "))

    best_phase = None
    best_overlap = 0
    for phase_id, phase_data in sec7.items():
        phase_text = " ".join([
            phase_data.get("declaration", ""),
            phase_data.get("input", ""),
            phase_data.get("output", ""),
        ])
        phase_tokens = _decl_tokens(phase_text)
        overlap = len(comp_text_tokens & phase_tokens)
        if overlap > best_overlap:
            best_overlap = overlap
            best_phase = phase_data

    method = _infer_method_name(comp_el)

    # Derive input/output primarily from the COMPONENT DECLARATION (reliable)
    # Fall back to phase input/output text only as secondary source
    comp_decl_lower = comp_decl.lower()
    phase_inp = best_phase.get("input", "").lower() if best_phase else ""
    phase_out = best_phase.get("output", "").lower() if best_phase else ""

    input_sig = _infer_input_sig_from_decl(comp_decl_lower, phase_inp, class_hint)
    output_type = _infer_output_type_from_decl(comp_decl_lower, phase_out, class_hint)

    return f"class {class_name}: {method}({input_sig}) -> {output_type}"


def _infer_input_sig_from_decl(comp_decl: str, phase_inp: str, class_hint: str) -> str:
    """
    Derive a Python input signature from the component declaration (primary)
    and phase input text (fallback). Component declaration is more precise
    because it describes what the component *accepts*.
    """
    # Component-level signals (highest priority)
    if "traverse" in comp_decl or ("directory" in comp_decl and "file entr" not in comp_decl.split("traverses")[0] if "traverses" in comp_decl else "directory" in comp_decl and "file entr" not in comp_decl[:comp_decl.find("directory")]):
        return "directory: str"
    if "receives the collection" in comp_decl or ("receives" in comp_decl and "group" in comp_decl):
        return "groups: dict, total_bytes: int"
    if "groups" in comp_decl and "file entr" in comp_decl and "duplicate" not in comp_decl[:comp_decl.find("file entr")]:
        return f"entries: list[{class_hint}]"
    if "derives the recoverable" in comp_decl or ("space" in comp_decl and "group" in comp_decl):
        return "groups: dict"
    # Phase input fallback
    return _infer_input_sig(phase_inp, class_hint)


def _infer_output_type_from_decl(comp_decl: str, phase_out: str, class_hint: str) -> str:
    """
    Derive a Python return type from the component declaration (primary)
    and phase output text (fallback).
    """
    if "produces" in comp_decl and "file entr" in comp_decl:
        return f"list[{class_hint}]"
    if "final output artifact" in comp_decl or "report" in comp_decl:
        return "str"
    if "recoverable space" in comp_decl or ("space" in comp_decl and "group" in comp_decl):
        return "tuple[dict, int]"
    if "groups" in comp_decl and "duplicate" in comp_decl:
        return "dict"
    # Phase output fallback
    return _infer_output_type(phase_out, class_hint)


def _infer_method_name(comp_el: str) -> str:
    """Derive a Python method name from a component/file name."""
    comp_lower = comp_el.lower()
    if "scan" in comp_lower:
        return "scan"
    if "hash" in comp_lower:
        return "compute_hash"
    if "detect" in comp_lower or "group" in comp_lower:
        return "detect"
    if "calculat" in comp_lower:
        return "calculate"
    if "compos" in comp_lower or "report" in comp_lower or "generat" in comp_lower:
        return "compose"
    return "process"


def _infer_input_sig(inp_text: str, class_hint: str) -> str:
    """Derive a Python input signature string from a phase input description."""
    inp = inp_text.lower()
    if ("dir" in inp or "path" in inp) and "file entr" not in inp:
        return "directory: str"
    if "file entr" in inp or class_hint.lower() in inp or ("collection" in inp and "group" not in inp):
        return f"entries: list[{class_hint}]"
    if "annotated" in inp:
        return "groups: dict, total_bytes: int"
    if "group" in inp:
        return "groups: dict"
    return "data"


def _infer_output_type(out_text: str, class_hint: str) -> str:
    """Derive a Python return type annotation from a phase output description."""
    out = out_text.lower()
    if "file entr" in out or class_hint.lower() in out:
        return f"list[{class_hint}]"
    if "total" in out and "byte" in out:
        return "tuple[dict, int]"
    if "report" in out or "artifact" in out:
        return "str"
    if "group" in out:
        return "dict"
    return "dict"


# ---------------------------------------------------------------------------
# Primary ID selection (avoids circular import with file_generator.py)
# ---------------------------------------------------------------------------

def _select_primary_ids_dynamic(nombre: str, all_ids: set, max_ids: int = 12) -> list:
    """
    Select the most relevant BETO-TRACE IDs for a file from the full registry.
    Mirrors the logic in file_generator._seleccionar_ids_para_archivo.
    """
    import re

    base = re.sub(r"\.\w+$", "", nombre.split("/")[-1])
    tokens = [t.upper() for t in re.split(r"[_\-]", base) if len(t) > 2]

    scored: list = []
    for id_ in all_ids:
        parts = id_.split(".")
        elemento = parts[-1] if len(parts) >= 4 else ""
        seccion = parts[1] if len(parts) >= 2 else ""
        score = 0
        for tok in tokens:
            if tok in elemento or tok in seccion:
                score += 2
        if "SEC1" in id_:
            score += 1
        if "SEC6" in id_ or "SEC7" in id_:
            score += 1
        scored.append((score, id_))

    scored.sort(key=lambda x: (-x[0], x[1]))
    selected = [id_ for _, id_ in scored[:max_ids]]
    if not any("SEC1" in id_ for id_ in selected):
        intent_ids = [id_ for _, id_ in scored if "SEC1" in id_]
        if intent_ids:
            selected = intent_ids[:2] + selected[:max_ids - 2]
    return sorted(selected)


def _extract_files_from_manifest(content: str) -> list[dict]:
    """
    Extract Python/config file paths declared in MANIFEST_PROYECTO.md.
    Supports table rows with backtick-quoted file names.
    """
    import re

    archivos_vistos: list = []
    seen: set = set()
    for line in content.split("\n"):
        if "|" not in line and "`" not in line:
            continue
        if re.match(r"\s*\|[-\s|]+\|\s*$", line):
            continue
        for m in re.finditer(r"`([^`]+\.(py|yaml|yml|toml|json|html|css|js|md|txt|cfg|ini))`", line):
            nombre = m.group(1)
            if re.match(r"(BETO_|TRACE_|MANIFEST_|PHASE_|PASO_|CIERRE)", nombre):
                continue
            if nombre.lower() in ("archivo", "file", "archivos", "files"):
                continue
            if nombre not in seen:
                seen.add(nombre)
                cols = [c.strip() for c in line.split("|") if c.strip()]
                nodo = ""
                for col in cols:
                    if re.search(r"P-\d+|N-\d+", col):
                        nodo = re.search(r"P-\d+[\.\d]*|N-\d+", col).group(0)
                        break
                archivos_vistos.append({"nombre": nombre, "nodo": nodo, "desc": ""})
    return archivos_vistos


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
