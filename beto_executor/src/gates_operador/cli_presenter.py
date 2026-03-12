"""
BETO-TRACE: BETO_GATES.SEC1.INTENT.PRESENT_GATE_INFO
BETO-TRACE: BETO_GATES.SEC1.INTENT.PRESENT_BETO_GAP
BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.CLI_PRESENTATION
BETO-TRACE: BETO_GATES.SEC8.DECISION.CLI_STDIN_STDOUT
"""


def presentar_gate(gate_info: dict, cycle_dir=None) -> None:
    """
    BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.CLI_PRESENTATION
    BETO-TRACE: BETO_GATES.SEC8.DECISION.CLI_STDIN_STDOUT

    Presenta la información del gate al operador via CLI stdout.
    Si cycle_dir está disponible, muestra el contenido del artefacto.
    """
    from pathlib import Path

    print()
    print("=" * 60)
    print(f"  GATE {gate_info['paso_origen']}")
    print("=" * 60)
    print(f"  Motor emisor : {gate_info['motor_origen']}")
    print(f"  Artefacto    : {gate_info['artefacto_generado']}")
    print("-" * 60)

    if cycle_dir:
        ruta = Path(cycle_dir) / gate_info["artefacto_generado"]
        if ruta.exists():
            contenido = ruta.read_text(encoding="utf-8")
            print()
            print(contenido)
            print("-" * 60)
        else:
            print(f"  [AVISO] Artefacto no encontrado en: {ruta}")
            print("-" * 60)


def presentar_gap(beto_gap: str | list) -> None:
    """
    BETO-TRACE: BETO_GATES.SEC1.INTENT.PRESENT_BETO_GAP
    BETO-TRACE: BETO_GATES.SEC2.BOUNDARY.GAP_PRESENTATION
    BETO-TRACE: BETO_GATES.SEC8.DECISION.GAP_PRESENTED_AT_GATE

    Presenta el BETO_GAP al operador ANTES de solicitar la decisión principal.
    El componente NO propone resolución del gap.
    """
    print()
    print("  *** BETO_GAP [ESCALADO] ADJUNTO ***")
    print("-" * 60)
    if isinstance(beto_gap, list):
        for i, gap in enumerate(beto_gap, 1):
            print(f"  Gap {i}: {gap}")
    else:
        print(f"  {beto_gap}")
    print("-" * 60)
    print("  Declare su resolución para este gap antes de continuar.")
    print()
