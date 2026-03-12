"""
Script de prueba aislada del Motor Código (Paso 10).

Instancia MotorCodigo directamente — sin correr Pasos 0-9.
Handoff: outputs/beto_executor/ (artefactos del propio BETO_EXECUTOR).
Output:  src/test_output/ (directorio nuevo — genera realmente).

Uso:
    python3 test_paso10.py --code-model qwen-coder [--api-key KEY] [--litellm-url URL]
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

from gates_operador.gates import GatesOperador
from gestor_ciclo.state_manager import StateManager
from motor_codigo.motor import MotorCodigo


# Ruta base: outputs/beto_executor/ — tiene todos los artefactos del handoff
HANDOFF_PATH = Path(__file__).parent.parent
TEST_CYCLES_DIR = Path(__file__).parent / "test_cycles"
TEST_OUTPUT_DIR = Path(__file__).parent / "test_output"


def crear_ciclo_prueba(cycles_dir: Path, ciclo_id: str) -> None:
    """Crea un JSON de ciclo mínimo para que StateManager pueda operar."""
    cycles_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "ciclo_id": ciclo_id,
        "idea_raw_hash": "test",
        "idea_raw": "BETO_EXECUTOR — prueba directa de Paso 10",
        "paso_actual": 9,
        "artefactos": [],
        "decisiones_gate": [],
        "beto_gaps": [],
        "estado_ciclo": "EN_PROGRESO",
        "timestamp_creacion": datetime.now(timezone.utc).isoformat(),
    }
    (cycles_dir / f"{ciclo_id}.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Prueba directa del Motor Código (Paso 10) — sin Pasos 0-9."
    )
    parser.add_argument("--code-model", type=str, required=True,
                        help="Nombre del modelo de código en LiteLLM (ej: qwen-coder)")
    parser.add_argument("--api-key", type=str, default="none",
                        help="API key para LiteLLM. Default: none")
    parser.add_argument("--litellm-url", type=str, default="http://localhost:8000",
                        help="Base URL del LiteLLM gateway. Default: http://localhost:8000")
    args = parser.parse_args()

    # Verificar que el handoff tiene los artefactos requeridos
    print(f"[test_paso10] Handoff path : {HANDOFF_PATH}")
    print(f"[test_paso10] Output dir   : {TEST_OUTPUT_DIR}")
    print(f"[test_paso10] Code model   : {args.code_model}")
    print(f"[test_paso10] LiteLLM URL  : {args.litellm_url}")

    if TEST_OUTPUT_DIR.exists() and any(TEST_OUTPUT_DIR.iterdir()):
        print(f"\n[test_paso10] AVISO: {TEST_OUTPUT_DIR} ya existe y tiene contenido.")
        print("[test_paso10] Los archivos ya presentes serán saltados (resume).")
        resp = input("[test_paso10] ¿Continuar? [s/N]: ").strip().lower()
        if resp != "s":
            print("[test_paso10] Cancelado.")
            sys.exit(0)

    # Crear ciclo de prueba
    ciclo_id = str(uuid.uuid4())
    crear_ciclo_prueba(TEST_CYCLES_DIR, ciclo_id)
    print(f"\n[test_paso10] Ciclo prueba: {ciclo_id}")

    # Clientes y dependencias
    code_client = OpenAI(base_url=args.litellm_url, api_key=args.api_key)
    state_manager = StateManager(TEST_CYCLES_DIR)
    gates = GatesOperador(state_manager)

    motor = MotorCodigo(
        ciclo_id=ciclo_id,
        handoff_path=HANDOFF_PATH,
        output_dir=TEST_OUTPUT_DIR,
        code_client=code_client,
        code_model=args.code_model,
        state_manager=state_manager,
        gates_operador=gates,
        g4_configurado=False,
    )

    try:
        output_dir = motor.ejecutar()
        print(f"\n[test_paso10] Paso 10 completado.")
        print(f"[test_paso10] Archivos en: {output_dir}")
    except RuntimeError as e:
        print(f"\n[test_paso10] Error en Paso 10: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
