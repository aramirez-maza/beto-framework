"""
BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.CONTEXT_BUILDER
BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP
BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_CONTEXT_PER_STEP
"""

from pathlib import Path


# BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP
# Artefactos requeridos por paso. No es política global acumulativa.
ARTEFACTOS_POR_PASO: dict[int, list[str]] = {
    0: [],                                     # Solo IDEA_RAW
    1: [],                                     # Solo IDEA_RAW
    2: ["BETO_CORE_DRAFT.md"],
    3: ["BETO_CORE_DRAFT.md", "BETO_CORE_INTERVIEW_COMPLETED.md"],
    4: ["BETO_CORE_DRAFT.md", "BETO_CORE_INTERVIEW_COMPLETED.md",
        "STRUCTURAL_CLASSIFICATION_REGISTRY.md"],
    5: ["BETO_CORE_DRAFT.md", "BETO_SYSTEM_GRAPH.md"],
    6: ["BETO_CORE_DRAFT.md", "BETO_SYSTEM_GRAPH.md",
        "BETO_CORE_MOTOR_RAZONAMIENTO.md", "BETO_CORE_MOTOR_CODIGO.md",
        "BETO_CORE_GATES_OPERADOR.md", "BETO_CORE_GESTOR_CICLO.md"],
    7: ["BETO_CORE_DRAFT.md", "BETO_SYSTEM_GRAPH.md",
        "BETO_CORE_MOTOR_RAZONAMIENTO.md", "BETO_CORE_MOTOR_CODIGO.md",
        "BETO_CORE_GATES_OPERADOR.md", "BETO_CORE_GESTOR_CICLO.md",
        "CIERRE_ASISTIDO.md"],
    8: ["BETO_CORE_DRAFT.md", "BETO_SYSTEM_GRAPH.md",
        "BETO_CORE_MOTOR_RAZONAMIENTO.md", "BETO_CORE_MOTOR_CODIGO.md",
        "BETO_CORE_GATES_OPERADOR.md", "BETO_CORE_GESTOR_CICLO.md"],
    9: ["BETO_CORE_DRAFT.md", "BETO_SYSTEM_GRAPH.md",
        "BETO_CORE_MOTOR_RAZONAMIENTO.md", "BETO_CORE_MOTOR_CODIGO.md",
        "BETO_CORE_GATES_OPERADOR.md", "BETO_CORE_GESTOR_CICLO.md"],
}

# Templates del framework BETO requeridos por paso.
# El LLM necesita ver la estructura exacta del template para saber
# qué formato y secciones debe generar en cada artefacto de salida.
TEMPLATES_POR_PASO: dict[int, list[str]] = {
    0: ["PROMPT_CANONICO_DE_ELICITACION.md"],
    1: ["PROMPT_CANONICO_DE_ELICITACION.md", "BETO_CORE_TEMPLATE.md"],
    2: ["BETO_CORE_INTERVIEW.md"],
    3: ["BETO_INSTRUCTIVO.md"],
    4: ["BETO_SYSTEM_GRAPH_TEMPLATE.md"],
    5: ["BETO_CORE_TEMPLATE.md"],
    6: ["BETO_CORE_TEMPLATE.md"],
    7: ["PHASE_TEMPLATE.md"],
    8: ["MANIFEST_BETO_TEMPLATE.md"],
    9: ["MANIFEST_PROYECTO_TEMPLATE.md"],
}


def construir_contexto(
    paso: int,
    idea_raw: str,
    cycle_dir: Path,
    templates_dir: Path | None = None,
    route_type: str = "",
) -> list[dict]:
    """
    BETO-TRACE: BETO_MOTOR_RAZ.SEC6.MODEL.CONTEXT_BUILDER
    BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

    Construye el contexto LLM para el paso dado.
    Orden: BETO_STATE (si existe) → templates del framework → IDEA_RAW → artefactos del ciclo.
    BETO_STATE es un resumen epistémico acumulado — reduce tokens en pasos avanzados.
    Los artefactos completos se mantienen (modo paralelo — BETO_STATE no reemplaza aún).
    NO es global acumulativo.

    v4.4 — Context stratification (REGLA CONTEXT_STRATIFICATION):
      BETO_LIGHT_PATH  → Capa B omitida (BETO_STATE no inyectado)
      BETO_PARTIAL_PATH → Capa B minimal (BETO_STATE inyectado)
      BETO_FULL_PATH   → Capa B full (BETO_STATE inyectado — comportamiento existente)
    """
    mensajes = []

    # BETO_STATE: contexto epistémico destilado — Capa B
    # BETO_LIGHT_PATH omite Capa B (REGLA MINIMAL_CONTEXT_EXECUTION — BETO v4.4)
    # Para "" (sin routing declarado) se mantiene el comportamiento previo (compatible)
    _load_beto_state = (
        paso >= 2
        and route_type != "BETO_LIGHT_PATH"
    )

    if _load_beto_state:
        beto_state_path = cycle_dir / "BETO_STATE.json"
        if beto_state_path.exists():
            try:
                from beto_state.schema import BETOState
                import json, dataclasses
                raw = json.loads(beto_state_path.read_text(encoding="utf-8"))
                # Reconstruir y formatear como bloque de texto
                from beto_state.writer import BETOStateWriter
                _writer = BETOStateWriter.__new__(BETOStateWriter)
                _writer.cycle_dir = cycle_dir
                _writer.ciclo_id = raw.get("ciclo_id", "")
                _writer.state_path = beto_state_path
                state = _writer._load_or_create(paso)
                bloque = state.to_context_block()
                if bloque.strip():
                    mensajes.append({
                        "role": "user",
                        "content": f"BETO_STATE — resumen epistémico del ciclo en curso:\n\n{bloque}"
                    })
            except Exception:
                pass  # BETO_STATE no crítico — falla silenciosa

    # Templates del framework: la estructura que el LLM debe seguir
    if templates_dir is not None:
        for nombre_template in TEMPLATES_POR_PASO.get(paso, []):
            ruta = templates_dir / nombre_template
            if ruta.exists():
                contenido = ruta.read_text(encoding="utf-8")
                mensajes.append({
                    "role": "user",
                    "content": f"FRAMEWORK TEMPLATE — {nombre_template}:\n\n{contenido}"
                })

    # IDEA_RAW siempre es parte del contexto
    # BETO-TRACE: BETO_MOTOR_RAZ.SEC3.INPUT.IDEA_RAW
    mensajes.append({
        "role": "user",
        "content": f"IDEA_RAW:\n\n{idea_raw}"
    })

    # Artefactos del ciclo: lo generado en pasos anteriores
    artefactos = ARTEFACTOS_POR_PASO.get(paso, [])
    for nombre in artefactos:
        ruta = cycle_dir / nombre
        if ruta.exists():
            contenido = ruta.read_text(encoding="utf-8")
            mensajes.append({
                "role": "user",
                "content": f"ARTEFACTO {nombre}:\n\n{contenido}"
            })

    return mensajes


def artefactos_requeridos_para_paso(paso: int) -> list[str]:
    """
    BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.CONTEXT_PER_STEP
    Retorna la lista de artefactos requeridos para un paso dado.
    """
    return list(ARTEFACTOS_POR_PASO.get(paso, []))
