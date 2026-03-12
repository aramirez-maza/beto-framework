"""
BETO-TRACE: BETO_MOTOR_RAZ.SEC2.BOUNDARY.ARTIFACT_WRITE
BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_CORE_DRAFT
BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.ARTIFACTS_TO_CYCLE_DIR
"""

import re
from pathlib import Path


# BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_CORE_DRAFT
# BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_SYSTEM_GRAPH
# BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.BETO_CORES_CLOSED
# BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.PHASE_DOCUMENTS
# BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.MANIFESTS_REGISTRIES
ARTEFACTOS_POR_PASO: dict[int, list[str]] = {
    0: ["PASO_0_EVALUACION.md"],
    1: ["BETO_CORE_DRAFT.md"],
    2: ["BETO_CORE_INTERVIEW_COMPLETED.md"],
    3: ["STRUCTURAL_CLASSIFICATION_REGISTRY.md"],
    4: ["BETO_SYSTEM_GRAPH.md"],
    5: [
        "BETO_CORE_MOTOR_RAZONAMIENTO.md",
        "BETO_CORE_MOTOR_CODIGO.md",
        "BETO_CORE_GATES_OPERADOR.md",
        "BETO_CORE_GESTOR_CICLO.md",
    ],
    6: ["CIERRE_ASISTIDO.md"],
    7: [
        "PHASE_ROOT_1_INPUT_ELIGIBILITY.md",
        "PHASE_ROOT_2_SPECIFICATION_PIPELINE.md",
        "PHASE_ROOT_3_MATERIALIZATION.md",
        "PHASE_MOTOR_RAZ_1_INICIO_CICLO.md",
        "PHASE_MOTOR_RAZ_2_PIPELINE.md",
        "PHASE_MOTOR_RAZ_3_HANDOFF.md",
        "PHASE_MOTOR_COD_1_LECTURA_HANDOFF.md",
        "PHASE_MOTOR_COD_2_MATERIALIZACION.md",
        "PHASE_MOTOR_COD_3_ENTREGA.md",
        "PHASE_GATES_OP_1_RECEPCION_SEÑAL.md",
        "PHASE_GATES_OP_2_PRESENTACION_CAPTURA.md",
        "PHASE_GATES_OP_3_RESOLUCION_GATE.md",
        "PHASE_GESTOR_1_CREACION_CICLO.md",
        "PHASE_GESTOR_2_GESTION_ESTADO.md",
        "PHASE_GESTOR_3_LECTURA_REANUDACION.md",
    ],
    8: [
        "MANIFEST_BETO_EXECUTOR.md",
        "TRACE_REGISTRY_BETO_EXECUTOR.md",
        "MANIFEST_MOTOR_RAZONAMIENTO.md",
        "TRACE_REGISTRY_MOTOR_RAZONAMIENTO.md",
        "MANIFEST_MOTOR_CODIGO.md",
        "TRACE_REGISTRY_MOTOR_CODIGO.md",
        "MANIFEST_GATES_OPERADOR.md",
        "TRACE_REGISTRY_GATES_OPERADOR.md",
        "MANIFEST_GESTOR_CICLO.md",
        "TRACE_REGISTRY_GESTOR_CICLO.md",
    ],
    9: ["MANIFEST_PROYECTO.md"],
}


# ---------------------------------------------------------------------------
# Resolución dinámica de artefactos para pasos 5, 7 y 8
# ---------------------------------------------------------------------------

def _beto_cores_from_graph(cycle_dir: Path) -> list[str]:
    """
    Lee BETO_SYSTEM_GRAPH.md y extrae los 'Associated BETO_CORE target'
    de los nodos hijos (PARALLEL y SUBBETO). Excluye ROOT (usa BETO_CORE_DRAFT).
    """
    graph = cycle_dir / "BETO_SYSTEM_GRAPH.md"
    if not graph.exists():
        return []
    content = graph.read_text(encoding="utf-8")
    seen: set[str] = set()
    cores: list[str] = []
    for m in re.finditer(r"Associated BETO_CORE target:\s+(BETO_CORE_\S+?)(?:\.md)?(?:\s|$|\()", content):
        name = m.group(1)
        if not name.endswith(".md"):
            name = name + ".md"
        if name == "BETO_CORE_DRAFT.md":
            continue
        if name not in seen:
            seen.add(name)
            cores.append(name)
    return cores


def _system_slug_from_graph(cycle_dir: Path) -> str:
    """Extrae 'System name' del METADATA de BETO_SYSTEM_GRAPH. Fallback: ROOT."""
    graph = cycle_dir / "BETO_SYSTEM_GRAPH.md"
    if graph.exists():
        content = graph.read_text(encoding="utf-8")
        m = re.search(r"System name:\s*(.+)", content)
        if m:
            nombre = m.group(1).strip()
            slug = re.sub(r"[^A-Za-z0-9]+", "_", nombre).upper().strip("_")
            if slug:
                return slug[:30]
    return "ROOT"


def _phases_from_graph(cycle_dir: Path) -> list[str]:
    """
    Deriva nombres de documentos de fase para nodos ROOT y PARALLEL.
    Convención: PHASE_{SLUG}_{N}.md con N en 1..3.
    SUBBETOs no reciben phase docs independientes.
    """
    graph = cycle_dir / "BETO_SYSTEM_GRAPH.md"
    if not graph.exists():
        return []
    content = graph.read_text(encoding="utf-8")

    root_slug = _system_slug_from_graph(cycle_dir)
    fases = [f"PHASE_{root_slug}_{n}.md" for n in range(1, 4)]

    # Extraer nodos PARALLEL con su BETO_CORE target
    blocks = re.split(r"(?=Node ID:)", content)
    for block in blocks:
        if not re.search(r"Node type:\s+PARALLEL", block):
            continue
        m = re.search(r"Associated BETO_CORE target:\s+(BETO_CORE_\S+?)(?:\.md)?(?:\s|$|\()", block)
        if m:
            slug = m.group(1).removeprefix("BETO_CORE_").removesuffix(".md")
            fases.extend([f"PHASE_{slug}_{n}.md" for n in range(1, 4)])

    return fases


def _manifests_from_paso5(cycle_dir: Path) -> list[str]:
    """
    Lee los BETO_CORE_*.md generados en Paso 5 (ya presentes en cycle_dir)
    y deriva pares MANIFEST_*.md + TRACE_REGISTRY_*.md.
    Incluye el ROOT desde el slug del sistema.
    """
    excluir = {"BETO_CORE_DRAFT", "BETO_CORE_INTERVIEW_COMPLETED"}
    cores = sorted(
        p.name for p in cycle_dir.glob("BETO_CORE_*.md")
        if p.stem not in excluir
    )
    if not cores:
        return []

    root_slug = _system_slug_from_graph(cycle_dir)
    resultado = [f"MANIFEST_{root_slug}.md", f"TRACE_REGISTRY_{root_slug}.md"]
    for core in cores:
        slug = core.removeprefix("BETO_CORE_").removesuffix(".md")
        resultado.append(f"MANIFEST_{slug}.md")
        resultado.append(f"TRACE_REGISTRY_{slug}.md")
    return resultado


def obtener_artefactos_paso(paso: int, cycle_dir: Path | None = None) -> list[str]:
    """
    Retorna la lista de artefactos para un paso dado.
    Para pasos 5, 7 y 8, deriva dinámicamente desde el grafo/artefactos del ciclo.
    Fallback: lista estática de ARTEFACTOS_POR_PASO.
    """
    if cycle_dir is not None:
        if paso == 5:
            dinamicos = _beto_cores_from_graph(cycle_dir)
            if dinamicos:
                return dinamicos
        elif paso == 7:
            dinamicos = _phases_from_graph(cycle_dir)
            if dinamicos:
                return dinamicos
        elif paso == 8:
            dinamicos = _manifests_from_paso5(cycle_dir)
            if dinamicos:
                return dinamicos
    return ARTEFACTOS_POR_PASO.get(paso, [])


class ArtifactWriter:
    """
    BETO-TRACE: BETO_MOTOR_RAZ.SEC2.BOUNDARY.ARTIFACT_WRITE
    BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.ARTIFACTS_TO_CYCLE_DIR

    Escribe artefactos generados en el directorio del ciclo.
    """

    def __init__(self, cycle_dir: Path):
        self.cycle_dir = cycle_dir
        self.cycle_dir.mkdir(parents=True, exist_ok=True)

    def escribir(self, nombre: str, contenido: str) -> Path:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC8.DECISION.ARTIFACTS_TO_CYCLE_DIR
        Escribe el contenido en {cycle_dir}/{nombre}.
        Retorna la ruta del archivo escrito.
        """
        ruta = self.cycle_dir / nombre
        ruta.write_text(contenido, encoding="utf-8")
        return ruta

    def artefactos_existentes(self, paso: int) -> list[str]:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC3.OUTPUT.HANDOFF_PATH
        Retorna los artefactos del paso que ya existen en el directorio.
        """
        esperados = obtener_artefactos_paso(paso, self.cycle_dir)
        return [n for n in esperados if (self.cycle_dir / n).exists()]

    def verificar_artefactos_paso(self, paso: int) -> tuple[list[str], list[str]]:
        """
        BETO-TRACE: BETO_MOTOR_RAZ.SEC7.PHASE.PHASE_3_HANDOFF
        Retorna (presentes, faltantes) para los artefactos del paso.
        """
        esperados = obtener_artefactos_paso(paso, self.cycle_dir)
        presentes = [n for n in esperados if (self.cycle_dir / n).exists()]
        faltantes = [n for n in esperados if n not in presentes]
        return presentes, faltantes
