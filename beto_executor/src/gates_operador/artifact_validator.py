"""
BETO-TRACE: BETO_GATES.SEC1.INTENT.OPERATOR_GATE_MANAGEMENT
BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.CLI_PRESENTATION

Validador estructural de artefactos BETO en gates.

READ-ONLY. No modifica artefactos. No dispara re-generación.
Verifica que los artefactos generados en cada paso siguen
la estructura formal definida por los templates del framework.

Regla ANTI-LOOP: si la validación falla, el operador ve los gaps
y decide si rechaza el gate (retroceso) o aprueba con deuda conocida.
El validador nunca toma decisiones ni dispara re-generación automática.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckResult:
    nombre: str
    passed: bool
    detalle: str = ""


@dataclass
class ValidationReport:
    gate_id: str
    artefacto: str
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def total(self) -> int:
        return len(self.checks)

    @property
    def aprobados(self) -> int:
        return sum(1 for c in self.checks if c.passed)


# ---------------------------------------------------------------------------
# Checks individuales — cada uno es determinista, sin LLM
# ---------------------------------------------------------------------------

def _check_secciones_numeradas(contenido: str, n: int, prefijo: str = "##") -> CheckResult:
    """Verifica que existan n secciones numeradas del 1 al n."""
    encontradas = []
    for i in range(1, n + 1):
        patron = rf"{re.escape(prefijo)}\s+{i}[\.\s]"
        if re.search(patron, contenido):
            encontradas.append(i)
    faltantes = [i for i in range(1, n + 1) if i not in encontradas]
    passed = len(faltantes) == 0
    detalle = f"Secciones encontradas: {len(encontradas)}/{n}" + (
        f" — Faltantes: {faltantes}" if faltantes else ""
    )
    return CheckResult(f"{n} secciones numeradas ({prefijo})", passed, detalle)


def _check_subseccion(contenido: str, patron: str, nombre: str) -> CheckResult:
    """Verifica que una subsección o texto específico esté presente."""
    found = bool(re.search(patron, contenido, re.IGNORECASE))
    return CheckResult(
        nombre,
        found,
        "Presente" if found else "NO encontrado — posible gap estructural",
    )


def _check_sin_fail_en_bloque(contenido: str, inicio_patron: str, nombre: str) -> CheckResult:
    """
    Verifica que en el bloque que comienza con inicio_patron no haya
    ninguna línea con 'FAIL'. Útil para checklists de topology y validación.
    """
    lineas = contenido.split("\n")
    en_bloque = False
    fails_encontrados = []

    for linea in lineas:
        if re.search(inicio_patron, linea, re.IGNORECASE):
            en_bloque = True
        if en_bloque and re.search(r'\bFAIL\b', linea, re.IGNORECASE):
            # Excluir líneas que afirman ausencia de FAILs
            if not re.search(r'(ningún|no\s+exist|0\s+fail|sin\s+fail|no\s+hay)', linea, re.IGNORECASE):
                fails_encontrados.append(linea.strip())

    passed = len(fails_encontrados) == 0
    detalle = "Sin FAIL detectados" if passed else f"FAILs encontrados: {fails_encontrados}"
    return CheckResult(nombre, passed, detalle)


def _check_texto_presente(contenido: str, texto: str, nombre: str) -> CheckResult:
    found = texto.lower() in contenido.lower()
    return CheckResult(
        nombre,
        found,
        "Presente" if found else f"'{texto}' NO encontrado",
    )


# ---------------------------------------------------------------------------
# Validadores por gate
# ---------------------------------------------------------------------------

def _validar_g1(cycle_dir: Path) -> list[ValidationReport]:
    """G-1: Valida BETO_CORE_DRAFT.md"""
    reports = []

    # --- BETO_CORE_DRAFT.md ---
    ruta = cycle_dir / "BETO_CORE_DRAFT.md"
    report = ValidationReport(gate_id="G-1", artefacto="BETO_CORE_DRAFT.md")

    if not ruta.exists():
        report.checks.append(CheckResult("Archivo existe", False, "Archivo no encontrado"))
        reports.append(report)
        return reports

    contenido = ruta.read_text(encoding="utf-8")

    report.checks.append(_check_secciones_numeradas(contenido, 10))
    report.checks.append(_check_subseccion(
        contenido, r"BETO_GAP\s+LOG", "BETO_GAP LOG presente"
    ))
    report.checks.append(_check_subseccion(
        contenido, r"OQ-\d+", "Al menos una OQ en formato OQ-N"
    ))
    report.checks.append(_check_subseccion(
        contenido, r"SYSTEM INTENT", "Sección SYSTEM INTENT presente"
    ))
    report.checks.append(_check_subseccion(
        contenido, r"SYSTEM BOUNDARIES", "Sección SYSTEM BOUNDARIES presente"
    ))
    report.checks.append(_check_subseccion(
        contenido, r"PHASE ARCHITECTURE", "Sección PHASE ARCHITECTURE presente"
    ))
    report.checks.append(_check_subseccion(
        contenido, r"STABLE TECHNICAL DECISIONS", "Sección STABLE TECHNICAL DECISIONS presente"
    ))

    reports.append(report)
    return reports


def _validar_g2(cycle_dir: Path) -> list[ValidationReport]:
    """G-2: Valida BETO_CORE_INTERVIEW_COMPLETED.md y BETO_SYSTEM_GRAPH.md"""
    reports = []

    # --- BETO_CORE_INTERVIEW_COMPLETED.md ---
    ruta_int = cycle_dir / "BETO_CORE_INTERVIEW_COMPLETED.md"
    report_int = ValidationReport(gate_id="G-2", artefacto="BETO_CORE_INTERVIEW_COMPLETED.md")

    if not ruta_int.exists():
        report_int.checks.append(CheckResult("Archivo existe", False, "Archivo no encontrado"))
    else:
        c = ruta_int.read_text(encoding="utf-8")
        report_int.checks.append(_check_subseccion(c, r"SECCI[ÓO]N\s+6|P6\.", "SECCIÓN 6 presente"))
        report_int.checks.append(_check_subseccion(c, r"P6\.3", "P6.3 candidatos BETO_PARALELO presente"))
        report_int.checks.append(_check_subseccion(c, r"SECCI[ÓO]N\s+11|P11\.", "SECCIÓN 11 SubBETO Governance presente"))
        report_int.checks.append(_check_subseccion(c, r"P11\.2", "P11.2 evaluación formal presente"))
        report_int.checks.append(_check_subseccion(c, r"Condici[oó]n\s+1", "Condición 1 evaluada"))
        report_int.checks.append(_check_subseccion(c, r"Condici[oó]n\s+2", "Condición 2 evaluada"))
        report_int.checks.append(_check_subseccion(c, r"Condici[oó]n\s+3", "Condición 3 evaluada"))
        report_int.checks.append(_check_subseccion(c, r"Condici[oó]n\s+4", "Condición 4 evaluada"))
        report_int.checks.append(_check_subseccion(c, r"SECCI[ÓO]N\s+12|PASE\s+DE\s+CONSISTENCIA", "SECCIÓN 12 Pase de Consistencia presente"))
        report_int.checks.append(_check_subseccion(c, r"P12\.\d", "Checks P12.x presentes"))
        report_int.checks.append(_check_subseccion(
            c, r"(ninguno|LIMPIO|conflicts?\s*=\s*0|Conflictos\s+detectados:\s*ninguno)",
            "Cierre de consistencia sin conflictos"
        ))

    reports.append(report_int)

    # --- BETO_SYSTEM_GRAPH.md ---
    ruta_graph = cycle_dir / "BETO_SYSTEM_GRAPH.md"
    report_graph = ValidationReport(gate_id="G-2", artefacto="BETO_SYSTEM_GRAPH.md")

    if not ruta_graph.exists():
        report_graph.checks.append(CheckResult("Archivo existe", False, "Archivo no encontrado"))
    else:
        c = ruta_graph.read_text(encoding="utf-8")
        report_graph.checks.append(_check_subseccion(
            c, r"Graph status:\s+VALIDATED", "Graph status = VALIDATED"
        ))
        report_graph.checks.append(_check_sin_fail_en_bloque(
            c, r"TOPOLOGY CONSTRAINTS|10\.\s+TOPOLOGY", "Topology checklist sin FAIL"
        ))
        report_graph.checks.append(_check_subseccion(
            c, r"Ready to generate BETO_CORE children:\s+YES",
            "Listo para generar BETO_CORE hijos"
        ))
        report_graph.checks.append(_check_subseccion(c, r"NODE REGISTRY", "NODE REGISTRY presente"))
        report_graph.checks.append(_check_subseccion(c, r"EDGE REGISTRY", "EDGE REGISTRY presente"))

    reports.append(report_graph)
    return reports


def _validar_g3(cycle_dir: Path) -> list[ValidationReport]:
    """G-3: Valida MANIFEST_PROYECTO.md"""
    reports = []

    ruta = cycle_dir / "MANIFEST_PROYECTO.md"
    report = ValidationReport(gate_id="G-3", artefacto="MANIFEST_PROYECTO.md")

    if not ruta.exists():
        report.checks.append(CheckResult("Archivo existe", False, "Archivo no encontrado"))
        reports.append(report)
        return reports

    c = ruta.read_text(encoding="utf-8")

    report.checks.append(_check_subseccion(c, r"SECCI[ÓO]N\s+1\b", "SECCIÓN 1 presente"))
    report.checks.append(_check_subseccion(c, r"SECCI[ÓO]N\s+13\b", "SECCIÓN 13 presente (13 secciones)"))
    report.checks.append(_check_sin_fail_en_bloque(
        c, r"SECCI[ÓO]N\s+10|VALIDACI[ÓO]N\s+ESTRUCTURAL", "Sección 10 validación sin FAIL"
    ))
    report.checks.append(_check_texto_presente(
        c, "CONSISTENT", "Sección 11 muestra CONSISTENT"
    ))
    report.checks.append(_check_subseccion(
        c, r"Ready for materialization:\s*YES|Listo para materializar",
        "Listo para materialización"
    ))
    report.checks.append(_check_texto_presente(
        c, "VALIDATED", "BETO_SYSTEM_GRAPH referenciado como VALIDATED"
    ))

    reports.append(report)
    return reports


# ---------------------------------------------------------------------------
# Entrada pública
# ---------------------------------------------------------------------------

VALIDADORES = {
    "G-1": _validar_g1,
    "G-2": _validar_g2,
    "G-3": _validar_g3,
}


def validar_artefactos_gate(gate_id: str, cycle_dir: Path) -> list[ValidationReport]:
    """
    Ejecuta la validación estructural correspondiente al gate indicado.
    READ-ONLY. No modifica nada.

    Retorna lista de ValidationReport (uno por artefacto validado).
    Si el gate no tiene validador declarado, retorna lista vacía.
    """
    validador = VALIDADORES.get(gate_id)
    if validador is None:
        return []
    return validador(cycle_dir)


def presentar_reporte_validacion(reports: list[ValidationReport]) -> None:
    """
    Muestra el reporte de validación estructural por consola.
    Se llama ANTES de solicitar la decisión al operador.
    """
    if not reports:
        return

    print()
    print("=" * 60)
    print("  VALIDACIÓN ESTRUCTURAL DE ARTEFACTOS")
    print("  (read-only — el operador decide)")
    print("=" * 60)

    for report in reports:
        total = report.total
        aprobados = report.aprobados
        estado = "✓ PASS" if report.passed else "✗ GAPS DETECTADOS"
        print(f"\n  [{estado}] {report.artefacto} ({aprobados}/{total})")
        print("  " + "-" * 56)
        for check in report.checks:
            icono = "  ✓" if check.passed else "  ✗"
            print(f"{icono}  {check.nombre}")
            if not check.passed:
                print(f"       → {check.detalle}")

    todos_pass = all(r.passed for r in reports)
    print()
    if todos_pass:
        print("  ► Validación estructural: PASS completo")
    else:
        print("  ► Validación estructural: HAY GAPS — revise antes de aprobar")
        print("  ► El operador puede aprobar igualmente (deuda declarada)")
    print("=" * 60)
