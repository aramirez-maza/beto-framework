"""
BETO-TRACE: BETO_GATES.SEC1.INTENT.RESOLVE_GATE
BETO-TRACE: BETO_GATES.SEC6.MODEL.RETROCESO_TABLE
BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G1
BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G2
BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G3
BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G4
BETO-TRACE: BETO_GATES.SEC8.DECISION.G3_JUSTIFICATION_REQUIRED
"""

import re


class BETOGapEscalado(Exception):
    """
    BETO-TRACE: BETO_GATES.SEC8.DECISION.G3_JUSTIFICATION_REQUIRED
    Se lanza cuando G-3 es rechazado sin justificación clara de retroceso.
    """
    pass


def determinar_paso_retroceso(gate_id: str, justificacion: str) -> int:
    """
    BETO-TRACE: BETO_GATES.SEC6.MODEL.RETROCESO_TABLE
    BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G1
    BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G2
    BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G3
    BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G4

    Aplica la tabla de retroceso declarada:
    G-1 → Paso 1
    G-2 → Paso 2
    G-3 → paso indicado en justificación del operador
    G-4 → Paso 10 (archivo rechazado)

    Lanza BETOGapEscalado si G-3 sin justificación clara.
    """
    if gate_id == "G-1":
        # BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G1
        return 1

    if gate_id == "G-2":
        # BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G2
        return 2

    if gate_id == "G-4":
        # BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G4
        return 10

    if gate_id == "G-3":
        # BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G3
        # BETO-TRACE: BETO_GATES.SEC8.DECISION.G3_JUSTIFICATION_REQUIRED
        paso = _extraer_paso_de_justificacion(justificacion)
        if paso is None:
            raise BETOGapEscalado(
                f"G-3 rechazado con justificación ambigua: '{justificacion}'. "
                "No es posible determinar el paso de retroceso. "
                "Se requiere nueva declaración del operador."
            )
        return paso

    raise ValueError(f"Gate ID no reconocido: '{gate_id}'")


def _extraer_paso_de_justificacion(justificacion: str) -> int | None:
    """
    BETO-TRACE: BETO_GATES.SEC8.DECISION.RETROCESO_G3

    Extrae el número de paso de la justificación del operador.
    Busca patrones como 'paso 5', 'step 3', 'paso: 7', etc.
    Retorna None si no hay indicación clara.
    """
    if not justificacion:
        return None

    patterns = [
        r"paso\s*[:\-]?\s*(\d+)",
        r"step\s*[:\-]?\s*(\d+)",
        r"p(\d+)",
        r"\b(\d+)\b",
    ]

    texto = justificacion.lower()
    for pattern in patterns:
        match = re.search(pattern, texto)
        if match:
            num = int(match.group(1))
            if 0 <= num <= 10:
                return num

    return None
