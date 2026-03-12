"""
BETO-TRACE: BETO_GATES.SEC1.INTENT.CAPTURE_OPERATOR_DECISION
BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.DECISION_CAPTURE
BETO-TRACE: BETO_GATES.SEC8.DECISION.GATE_SUSPEND_WITHOUT_TIMEOUT
"""


def capturar_decision(paso_origen: str) -> dict:
    """
    BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.DECISION_CAPTURE
    BETO-TRACE: BETO_GATES.SEC8.DECISION.GATE_SUSPEND_WITHOUT_TIMEOUT
    BETO-TRACE: BETO_GATES.SEC3.OUTPUT.OPERATOR_DECISION

    Captura la decisión del operador via stdin.
    El sistema espera sin timeout hasta recibir una respuesta válida.
    Única respuesta válida: 'aprobado' o 'rechazado'.
    """
    while True:
        print()
        raw = input("  Decisión [aprobado/rechazado]: ").strip().lower()
        if raw in ("aprobado", "rechazado"):
            decision = raw
            break
        print(f"  Respuesta inválida: '{raw}'. Ingrese 'aprobado' o 'rechazado'.")

    justificacion = ""
    resolucion_gap = ""

    if decision == "rechazado":
        # BETO-TRACE: BETO_GATES.SEC8.DECISION.G3_JUSTIFICATION_REQUIRED
        if paso_origen == "G-3":
            while True:
                j = input("  Justificación (obligatoria para G-3): ").strip()
                if j:
                    justificacion = j
                    break
                print("  La justificación es obligatoria para G-3.")
        else:
            j = input("  Justificación (opcional): ").strip()
            justificacion = j

    return {
        "decision": decision,
        "justificacion_opcional": justificacion,
    }


def capturar_resolucion_gap() -> str:
    """
    BETO-TRACE: BETO_GATES.SEC3.OUTPUT.GAP_RESOLUTION_DECLARATION
    BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.GAP_PRESENTATION

    Captura la declaración del operador sobre la resolución del gap.
    El componente no propone resolución — solo registra la declaración.
    """
    print()
    declaracion = input("  Su declaración sobre este gap: ").strip()
    return declaracion


def capturar_opcion_duplicado() -> str:
    """
    BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.RESUME_NEW_OPTION

    Captura la decisión del operador ante un duplicado detectado.
    Opciones: 'reanudar' o 'nuevo'.
    """
    while True:
        raw = input("  Opción [reanudar/nuevo]: ").strip().lower()
        if raw in ("reanudar", "nuevo"):
            return raw
        print(f"  Opción inválida: '{raw}'. Ingrese 'reanudar' o 'nuevo'.")
