"""
BETO-TRACE: BETO_MOTOR_COD.SEC1.INTENT.OPERATE_ON_CLOSED_SPEC
BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.HANDOFF_READ
BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.ARTIFACT_VALIDATION
BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_1_LECTURA_HANDOFF
"""

from pathlib import Path


# BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.BETO_CORES
# BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.PHASE_DOCUMENTS
# BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.TRACE_REGISTRIES
ARTEFACTOS_REQUERIDOS_HANDOFF = [
    # BETO_COREs
    "BETO_CORE_DRAFT.md",
    "BETO_CORE_MOTOR_RAZONAMIENTO.md",
    "BETO_CORE_MOTOR_CODIGO.md",
    "BETO_CORE_GATES_OPERADOR.md",
    "BETO_CORE_GESTOR_CICLO.md",
    # TRACE_REGISTRYs
    "TRACE_REGISTRY_BETO_EXECUTOR.md",
    "TRACE_REGISTRY_MOTOR_RAZONAMIENTO.md",
    "TRACE_REGISTRY_MOTOR_CODIGO.md",
    "TRACE_REGISTRY_GATES_OPERADOR.md",
    "TRACE_REGISTRY_GESTOR_CICLO.md",
    # Plan de materialización
    "MANIFEST_PROYECTO.md",
]


class HandoffReader:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.HANDOFF_READER
    BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_1_LECTURA_HANDOFF

    Lee y valida los artefactos de especificación desde el directorio del ciclo.
    """

    def __init__(self, handoff_path: str | Path):
        # BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.HANDOFF_PATH
        self.cycle_dir = Path(handoff_path)

    def validar(self) -> tuple[bool, list[str]]:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.ARTIFACT_VALIDATION
        Verifica que los artefactos mínimos del handoff existen.
        Para sistemas genéricos: BETO_CORE_DRAFT, MANIFEST_PROYECTO,
        y al menos un TRACE_REGISTRY. No verifica nombres específicos de nodos.
        """
        faltantes = []

        # Artefactos fijos siempre requeridos
        for nombre in ["BETO_CORE_DRAFT.md", "MANIFEST_PROYECTO.md"]:
            if not (self.cycle_dir / nombre).exists():
                faltantes.append(nombre)

        # Al menos un TRACE_REGISTRY debe existir
        registries = list(self.cycle_dir.glob("TRACE_REGISTRY_*.md"))
        if not registries:
            faltantes.append("TRACE_REGISTRY_*.md (ninguno encontrado)")

        return len(faltantes) == 0, faltantes

    def leer_artefacto(self, nombre: str) -> str:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.HANDOFF_READ
        Lee un artefacto del directorio del ciclo.
        """
        ruta = self.cycle_dir / nombre
        if not ruta.exists():
            raise FileNotFoundError(f"Artefacto no encontrado en handoff: {nombre}")
        return ruta.read_text(encoding="utf-8")

    def leer_trace_registry(self, nombre_nodo: str) -> str:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.TRACE_REGISTRIES
        Lee el TRACE_REGISTRY para un nodo dado.
        nombre_nodo: 'BETO_EXECUTOR' | 'MOTOR_RAZONAMIENTO' | etc.
        """
        nombre_archivo = f"TRACE_REGISTRY_{nombre_nodo}.md"
        return self.leer_artefacto(nombre_archivo)

    def leer_beto_core(self, nombre_nodo: str) -> str:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.BETO_CORES
        Lee el BETO_CORE para un nodo dado.
        """
        mapa = {
            "BETO_EXECUTOR": "BETO_CORE_DRAFT.md",
            "MOTOR_RAZONAMIENTO": "BETO_CORE_MOTOR_RAZONAMIENTO.md",
            "MOTOR_CODIGO": "BETO_CORE_MOTOR_CODIGO.md",
            "GATES_OPERADOR": "BETO_CORE_GATES_OPERADOR.md",
            "GESTOR_CICLO": "BETO_CORE_GESTOR_CICLO.md",
        }
        nombre_archivo = mapa.get(nombre_nodo)
        if not nombre_archivo:
            raise ValueError(f"Nodo desconocido: {nombre_nodo}")
        return self.leer_artefacto(nombre_archivo)
