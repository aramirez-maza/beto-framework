"""
BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION
BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED
BETO-TRACE: BETO_MOTOR_COD.SEC4.FIELD.BETO_TRACE_IDS
BETO-TRACE: BETO_MOTOR_COD.SEC4.FIELD.ESTADO_ARCHIVO
"""

import re


# BETO-TRACE: BETO_MOTOR_COD.SEC4.FIELD.BETO_TRACE_IDS
BETO_TRACE_PATTERN = re.compile(
    r"BETO-TRACE:\s*([A-Z][A-Z0-9_-]*\.SEC\d+\.\w+\.\w+)"
)

# BETO-TRACE: BETO_MOTOR_COD.SEC4.FIELD.ESTADO_ARCHIVO
ESTADO_TRACE_VERIFIED = "TRACE_VERIFIED"
ESTADO_BETO_GAP = "BETO_GAP"
ESTADO_WARNED = "WARNED"


def extraer_trace_ids(texto: str) -> list[str]:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC4.FIELD.BETO_TRACE_IDS
    Extrae todos los BETO-TRACE IDs de un texto (código o scaffold).
    """
    return BETO_TRACE_PATTERN.findall(texto)


def extraer_ids_autorizados_de_registry(registry_content: str) -> set[str]:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION
    Extrae los IDs autorizados del TRACE_REGISTRY (formato Markdown tabla).
    """
    pattern = re.compile(r"(BETO[-_][\w-]+\.SEC\d+\.\w+\.\w+)")
    return set(pattern.findall(registry_content))


def verificar_archivo(
    codigo: str,
    registry_content: str,
    nombre_archivo: str,
) -> dict:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION
    BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED

    Verifica existencia: todos los IDs en el código deben estar en el TRACE_REGISTRY.
    Retorna estado TRACE_VERIFIED | BETO_GAP.
    """
    ids_en_codigo = extraer_trace_ids(codigo)
    ids_autorizados = extraer_ids_autorizados_de_registry(registry_content)

    if not ids_en_codigo:
        return {
            "estado": ESTADO_TRACE_VERIFIED,
            "ids_encontrados": [],
            "ids_no_registrados": [],
            "detalle": f"'{nombre_archivo}' sin anotaciones BETO-TRACE (best-effort — ver TRACE_REGISTRY).",
        }

    ids_no_registrados = [i for i in ids_en_codigo if i not in ids_autorizados]

    if ids_no_registrados:
        return {
            "estado": ESTADO_BETO_GAP,
            "ids_encontrados": ids_en_codigo,
            "ids_no_registrados": ids_no_registrados,
            "detalle": (
                f"'{nombre_archivo}': IDs no registrados: {ids_no_registrados}"
            ),
        }

    return {
        "estado": ESTADO_TRACE_VERIFIED,
        "ids_encontrados": ids_en_codigo,
        "ids_no_registrados": [],
        "detalle": f"'{nombre_archivo}': {len(ids_en_codigo)} IDs verificados.",
    }


def verificar_preservacion(
    scaffold: str,
    codigo_final: str,
    nombre_archivo: str,
) -> dict:
    """
    BETO-TRACE: BETO_MOTOR_COD.SEC2.BOUNDARY.TRACE_VERIFICATION
    BETO-TRACE: BETO_MOTOR_COD.SEC5.INVARIANT.TRACE_VERIFIED_REQUIRED

    Verifica preservación: cada ID presente en el scaffold debe seguir
    presente en el código final generado por el motor de código.

    Detecta IDs que qwen-coder eliminó, movió o corrompió.
    Retorna estado TRACE_VERIFIED | BETO_GAP con detalle de pérdidas.
    """
    ids_en_scaffold = set(extraer_trace_ids(scaffold))
    ids_en_codigo = set(extraer_trace_ids(codigo_final))

    if not ids_en_scaffold:
        # Si el scaffold no tenía IDs, no hay nada que preservar — caer a verificación básica
        return {
            "estado": ESTADO_WARNED,
            "ids_scaffold": [],
            "ids_perdidos": [],
            "detalle": f"'{nombre_archivo}': scaffold sin BETO-TRACE IDs. Verificación de preservación omitida.",
        }

    ids_perdidos = sorted(ids_en_scaffold - ids_en_codigo)

    if ids_perdidos:
        return {
            "estado": ESTADO_BETO_GAP,
            "ids_scaffold": sorted(ids_en_scaffold),
            "ids_perdidos": ids_perdidos,
            "detalle": (
                f"'{nombre_archivo}': {len(ids_perdidos)} IDs del scaffold no preservados "
                f"en el código final: {ids_perdidos}"
            ),
        }

    return {
        "estado": ESTADO_TRACE_VERIFIED,
        "ids_scaffold": sorted(ids_en_scaffold),
        "ids_perdidos": [],
        "detalle": (
            f"'{nombre_archivo}': preservación completa — "
            f"{len(ids_en_scaffold)} IDs del scaffold presentes en código final."
        ),
    }
