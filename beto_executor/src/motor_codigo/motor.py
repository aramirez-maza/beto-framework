"""
BETO-TRACE: BETO_MOTOR_COD.SEC1.INTENT.EXECUTE_PASO10
BETO-TRACE: BETO_MOTOR_COD.SEC1.INTENT.PRODUCE_TRACE_VERIFIED_FILES
BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_1_LECTURA_HANDOFF
BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_2_MATERIALIZACION
BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_3_ENTREGA
BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.TRACE_VERIFIED_GATE
BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.G4_OPTIONAL
"""

from pathlib import Path

from openai import OpenAI

from .file_generator import FileGenerator
from .handoff_reader import HandoffReader
from .plan_builder import obtener_plan
from .trace_injector import TraceInjector
import ast as _ast

from .trace_verifier import (
    ESTADO_BETO_GAP,
    ESTADO_TRACE_VERIFIED,
    verificar_preservacion,
)


def _dedup_module_strings(code: str) -> str:
    """
    Elimina string literals duplicados al nivel del módulo.

    El LLM a veces reproduce el docstring de módulo dos veces
    (una al inicio, otra entre los imports y la primera definición).
    Esta función conserva solo el primero, eliminando los demás.
    """
    try:
        tree = _ast.parse(code)
    except SyntaxError:
        return code

    # Recolectar nodos Expr(Constant(str)) al nivel del módulo
    duplicates = []
    seen_first = False
    for node in _ast.iter_child_nodes(tree):
        if (
            isinstance(node, _ast.Expr)
            and isinstance(node.value, _ast.Constant)
            and isinstance(node.value.value, str)
        ):
            if not seen_first:
                seen_first = True  # conservar el primero
            else:
                duplicates.append(node)

    if not duplicates:
        return code

    lines = code.split("\n")
    # Eliminar de abajo hacia arriba para no desplazar índices
    duplicates.sort(key=lambda n: -n.lineno)
    for node in duplicates:
        start = node.lineno - 1  # 0-indexed
        end = node.end_lineno    # exclusive
        # Absorber líneas en blanco precedentes
        while start > 0 and not lines[start - 1].strip():
            start -= 1
        lines[start:end] = []

    return "\n".join(lines)


import re as _re
_BETO_TRACE_LINE = _re.compile(r"^(\s*BETO-TRACE:\s+\S+)\s*$")


def _dedup_trace_ids_in_code(code: str) -> str:
    """
    Elimina líneas BETO-TRACE duplicadas dentro de cualquier docstring.

    El LLM a veces mezcla IDs inventados con IDs reales en el mismo
    docstring, y el inyector añade los reales encima — resultando en
    duplicados dentro del mismo docstring. Esta función conserva solo
    la primera aparición de cada ID en cada docstring.
    """
    lines = code.split("\n")
    result = []
    in_docstring = False
    quote_char = None
    seen_ids_in_docstring: set = set()

    for line in lines:
        stripped = line.strip()

        if not in_docstring:
            # Detectar apertura de docstring (triple comillas)
            for q in ('"""', "'''"):
                if stripped.startswith(q):
                    in_docstring = True
                    quote_char = q
                    seen_ids_in_docstring = set()
                    # Comprobar si también cierra en la misma línea
                    rest = stripped[len(q):]
                    if rest.endswith(q) and len(rest) >= len(q):
                        in_docstring = False  # docstring de una línea
                    break
            result.append(line)
        else:
            # Dentro de un docstring: deduplicar IDs BETO-TRACE
            m = _BETO_TRACE_LINE.match(line)
            if m:
                trace_id = line.strip().split()[-1]  # el ID es la última palabra
                if trace_id in seen_ids_in_docstring:
                    continue  # descartar duplicado
                seen_ids_in_docstring.add(trace_id)
            # Detectar cierre del docstring
            if quote_char in stripped and not stripped.startswith(quote_char):
                in_docstring = False
            elif stripped == quote_char or stripped.endswith(quote_char):
                in_docstring = False
            result.append(line)

    return "\n".join(result)


class MotorCodigo:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC1.INTENT.EXECUTE_PASO10
    BETO-TRACE: BETO_MOTOR_COD.SEC1.INTENT.PRODUCE_TRACE_VERIFIED_FILES

    Ejecuta el Paso 10: materialización con scaffold del sistema +
    implementación por motor de código + verificación de preservación.

    Reanudable: archivos ya escritos en disco se omiten.
    Solo re-materializa archivos con GAP (no presentes en output_dir).
    Los Pasos 0-9 nunca se re-ejecutan desde aquí.
    """

    def __init__(
        self,
        ciclo_id: str,
        handoff_path: Path,
        output_dir: Path,
        code_client: OpenAI,
        code_model: str,
        state_manager,
        gates_operador,
        g4_configurado: bool = False,
    ):
        # BETO-TRACE: BETO_MOTOR_COD.SEC3.INPUT.HANDOFF_PATH
        self.ciclo_id = ciclo_id
        self.handoff_path = handoff_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state_manager = state_manager
        self.gates = gates_operador
        # BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.G4_OPTIONAL
        self.g4_configurado = g4_configurado

        self.handoff_reader = HandoffReader(handoff_path)
        self.trace_injector = TraceInjector()
        # BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.LLM_API_OPENAI_COMPATIBLE
        self.file_generator = FileGenerator(
            code_client=code_client,
            code_model=code_model,
        )

    def _cargar_generator_rules(self) -> None:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED

        Carga y valida GENERATOR_RULES_BETO_EXECUTOR.md antes de materializar.
        Verifica existencia del artefacto y presencia mínima de las 4 reglas.
        Falla temprano con RuntimeError si el artefacto está ausente o incompleto.
        """
        rules_path = self.handoff_path / "GENERATOR_RULES_BETO_EXECUTOR.md"

        if not rules_path.exists():
            raise RuntimeError(
                f"GENERATOR_RULES ausente: {rules_path}\n"
                "El Motor de Código no puede ejecutar sin su artefacto de gobierno. "
                "(RULE_003: GENERATOR_RULES_ARE_MANDATORY)"
            )

        contenido = rules_path.read_text(encoding="utf-8")
        reglas_requeridas = ["RULE_001", "RULE_002", "RULE_003", "RULE_004"]
        faltantes = [r for r in reglas_requeridas if r not in contenido]

        if faltantes:
            raise RuntimeError(
                f"GENERATOR_RULES incompleto: faltan {faltantes} en {rules_path}\n"
                "El artefacto existe pero no contiene las reglas mínimas obligatorias."
            )

        print(f"[Motor Código] GENERATOR_RULES: OK ({len(reglas_requeridas)} reglas verificadas)")

    def ejecutar(self) -> Path:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_1_LECTURA_HANDOFF
        BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_2_MATERIALIZACION
        BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_3_ENTREGA
        """
        # — PHASE 1: Lectura del Handoff —
        ok, faltantes = self.handoff_reader.validar()
        if not ok:
            raise RuntimeError(
                f"Handoff inválido. Artefactos faltantes: {faltantes}"
            )

        # Verificar governance del generador antes de cualquier llamada al modelo
        self._cargar_generator_rules()

        # Registrar inicio de Paso 10 — permite reanudación correcta si el proceso falla
        self.state_manager.aplicar_evento(
            self.ciclo_id, "ACTUALIZAR_PASO", {"paso_actual": 10}
        )

        idea_raw = self.handoff_reader.leer_artefacto("BETO_CORE_DRAFT.md")
        plan = obtener_plan(self.handoff_path)
        print(f"[Motor Código] Plan: {len(plan)} archivos. Scaffold: sistema. Implementación: código.")

        archivos_trace_verified = []
        archivos_con_gap = []

        # — PHASE 2: Materialización por Archivo —
        for entrada in plan:
            ruta_archivo = self.output_dir / entrada.nombre_archivo

            # Reanudar: saltar archivos ya materializados en disco
            if ruta_archivo.exists():
                print(f"[Motor Código] ({entrada.orden}/{len(plan)}) {entrada.nombre_archivo} — ya en disco, saltando.")
                archivos_trace_verified.append(entrada.nombre_archivo)
                continue

            print(f"[Motor Código] ({entrada.orden}/{len(plan)}) {entrada.nombre_archivo}")

            beto_core = self.handoff_reader.leer_artefacto(entrada.beto_core_origen)
            trace_registry = self.handoff_reader.leer_artefacto(entrada.trace_registry_ref)

            # Paso A: scaffold del sistema (sin LLM)
            # BETO-TRACE: BETO_MOTOR_COD.SEC6.MODEL.CONTEXT_PER_FILE
            print(f"  → scaffold (sistema)...")
            scaffold, codigo_final = self.file_generator.generar(
                entrada, idea_raw, beto_core, trace_registry
            )
            print(f"  → implementación (código)...")

            # DEBUG: guardar scaffold y codigo_final a disco para inspección
            debug_dir = self.output_dir.parent / "debug"
            debug_dir.mkdir(exist_ok=True)
            safe_name = entrada.nombre_archivo.replace("/", "_")
            (debug_dir / f"{safe_name}.scaffold.py").write_text(scaffold, encoding="utf-8")
            (debug_dir / f"{safe_name}.codigo_pre_inject.py").write_text(codigo_final, encoding="utf-8")

            # Paso B: inyección mecánica de BETO-TRACE del scaffold (no-op con nuevo scaffold)
            codigo_final = self.trace_injector.inject(scaffold, codigo_final)

            # Paso B2: eliminar docstrings de módulo duplicados y deduplicar IDs
            codigo_final = _dedup_module_strings(codigo_final)
            codigo_final = _dedup_trace_ids_in_code(codigo_final)

            # Paso C: validación de sintaxis Python (solo archivos .py)
            if entrada.nombre_archivo.endswith(".py"):
                try:
                    _ast.parse(codigo_final)
                except SyntaxError as e:
                    detalle = f"SyntaxError en output del LLM: {e}"
                    self._registrar_gap(entrada, detalle)
                    archivos_con_gap.append({
                        "nombre": entrada.nombre_archivo,
                        "tipo": "syntax",
                        "detalle": detalle,
                    })
                    continue

            # Paso D: verificación de preservación (scaffold → código final)
            # BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION
            resultado_verificacion = verificar_preservacion(scaffold, codigo_final, entrada.nombre_archivo)

            if resultado_verificacion["estado"] == ESTADO_BETO_GAP:
                detalle = resultado_verificacion["detalle"]
                self._registrar_gap(entrada, detalle)
                archivos_con_gap.append({
                    "nombre": entrada.nombre_archivo,
                    "tipo": "verificacion",
                    "detalle": detalle,
                })
                continue

            # TRACE_VERIFIED: escribir archivo
            # BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.CODE_GENERATION
            ruta_archivo.parent.mkdir(parents=True, exist_ok=True)
            ruta_archivo.write_text(codigo_final, encoding="utf-8")

            archivos_trace_verified.append(entrada.nombre_archivo)
            n_ids = len(resultado_verificacion.get("ids_scaffold", []))
            estado_label = resultado_verificacion["estado"]
            print(f"  → {estado_label} ({n_ids} IDs preservados)")

            self.state_manager.aplicar_evento(
                self.ciclo_id,
                "REGISTRAR_ARTEFACTO",
                {
                    "paso": 10,
                    "nombre_artefacto": entrada.nombre_archivo,
                    "ruta_artefacto": str(ruta_archivo),
                    "estado": ESTADO_TRACE_VERIFIED,
                },
            )

        if archivos_con_gap:
            raise RuntimeError(
                f"Materialización incompleta. {len(archivos_con_gap)} archivo(s) con BETO_GAP "
                f"(reanudable — los {len(archivos_trace_verified)} archivos ya en disco no se repetirán):\n"
                + "\n".join(
                    f"  [{a['tipo']}] {a['nombre']}: {a['detalle']}"
                    for a in archivos_con_gap
                )
            )

        # — PHASE 3: Entrega —
        return self._entrega(archivos_trace_verified)

    def _registrar_gap(self, entrada, detalle: str) -> None:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED
        """
        print(f"  → BETO_GAP [ESCALADO]: {detalle}")
        self.state_manager.aplicar_evento(
            self.ciclo_id,
            "REGISTRAR_GAP",
            {
                "gap_id": f"gap-paso10-{entrada.nombre_archivo}",
                "descripcion": detalle,
                "tipo": "ESCALADO",
                "paso": 10,
                "estado": "PENDIENTE",
            },
        )

    def _entrega(self, archivos_trace_verified: list[str]) -> Path:
        """
        BETO-TRACE: BETO_MOTOR_COD.SEC7.PHASE.PHASE_3_ENTREGA
        BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.G4_OPTIONAL
        BETO-TRACE: BETO_MOTOR_COD.SEC3.OUTPUT.FINALIZATION_SIGNAL
        """
        # BETO-TRACE: BETO_MOTOR_COD.SEC8.DECISION.G4_OPTIONAL
        if self.g4_configurado:
            señal = {
                "paso_origen": "G-4",
                "motor_origen": "MOTOR_CODIGO",
                "artefacto_generado": (
                    f"{len(archivos_trace_verified)} archivos TRACE_VERIFIED en {self.output_dir}"
                ),
                "beto_gap_adjunto": None,
            }
            resultado = self.gates.procesar_gate(self.ciclo_id, señal)
            if resultado["señal_tipo"] == "RETROCESO":
                raise RuntimeError(
                    "G-4 rechazado. Regenerar archivos rechazados y reinvocar entrega."
                )

        # BETO-TRACE: BETO_MOTOR_COD.SEC3.OUTPUT.FINALIZATION_SIGNAL
        self.state_manager.aplicar_evento(
            self.ciclo_id, "ACTUALIZAR_PASO", {"paso_actual": 10}
        )

        print(
            f"[Motor Código] Materialización completa: "
            f"{len(archivos_trace_verified)} archivos TRACE_VERIFIED."
        )
        print(f"[Motor Código] Output: {self.output_dir}")
        return self.output_dir
