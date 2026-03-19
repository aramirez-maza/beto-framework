"""
BETO-TRACE: BETO_EXECUTOR.SEC2.BOUNDARY.IDEA_RAW_RECEPTION
BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.IDEA_RAW
BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.SYSTEM_CONFIG
BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.OPERATOR_CLI_STDIN_STDOUT
BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE
"""

import argparse
import json
import sys
from pathlib import Path

from orquestador.root import BETOExecutorRoot


def main():
    """
    BETO-TRACE: BETO_EXECUTOR.SEC2.BOUNDARY.IDEA_RAW_RECEPTION
    BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.OPERATOR_CLI_STDIN_STDOUT

    Punto de entrada CLI de BETO_EXECUTOR.
    Recibe la IDEA_RAW y la configuración del sistema y lanza el pipeline.
    """
    parser = argparse.ArgumentParser(
        description="BETO_EXECUTOR — Automatización del proceso BETO Framework v4.2",
    )

    # BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.IDEA_RAW
    parser.add_argument(
        "--idea",
        type=str,
        help="IDEA_RAW como string. Si no se provee, se lee desde stdin.",
    )
    parser.add_argument(
        "--idea-file",
        type=str,
        help="Ruta a un archivo de texto con la IDEA_RAW.",
    )

    # BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.SYSTEM_CONFIG
    # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Ruta a un archivo JSON con la configuración del sistema.",
    )
    parser.add_argument(
        "--cycle-dir",
        type=str,
        default="./cycles",
        help="Directorio base para los ciclos BETO. Default: ./cycles",
    )
    parser.add_argument(
        "--reasoning-model",
        type=str,
        default="gpt-4o",
        help="Modelo LLM para razonamiento (Pasos 0–9). Default: gpt-4o",
    )
    parser.add_argument(
        "--code-model",
        type=str,
        default="gpt-4o",
        help="Modelo LLM para código (Paso 10). Default: gpt-4o",
    )
    parser.add_argument(
        "--litellm-url",
        type=str,
        default="http://localhost:8000",
        help="Base URL del LiteLLM gateway. Default: http://localhost:8000",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default="none",
        help="API key para el LLM. Default: none (para LiteLLM local)",
    )
    parser.add_argument(
        "--g4",
        action="store_true",
        default=False,
        help="Activar gate G-4 opcional (revisión final del operador).",
    )
    parser.add_argument(
        "--templates-dir",
        type=str,
        default=None,
        help="Directorio con los templates del framework BETO "
             "(BETO_CORE_TEMPLATE.md, BETO_CORE_INTERVIEW.md, etc.). "
             "Si no se provee, el motor opera sin templates en contexto.",
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        default=False,
        help="Modo test: aprueba automáticamente todos los gates (G-1, G-2, G-3). "
             "No usar en producción.",
    )

    args = parser.parse_args()

    # Resolución de IDEA_RAW
    # BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.IDEA_RAW
    if args.idea:
        idea_raw = args.idea
    elif args.idea_file:
        idea_raw = Path(args.idea_file).read_text(encoding="utf-8")
    else:
        print("Ingrese la IDEA_RAW (termine con Ctrl+D en Unix / Ctrl+Z en Windows):")
        idea_raw = sys.stdin.read()

    idea_raw = idea_raw.strip()
    if not idea_raw:
        print("Error: IDEA_RAW vacía. Provea una idea de sistema de software.", file=sys.stderr)
        sys.exit(1)

    # Construcción de configuración
    # BETO-TRACE: BETO_EXECUTOR.SEC3.INPUT.SYSTEM_CONFIG
    config: dict = {
        "cycle_output_dir": args.cycle_dir,
        "reasoning_model": args.reasoning_model,
        "code_model": args.code_model,
        "litellm_base_url": args.litellm_url,
        "api_key": args.api_key,
        "g4_configurado": args.g4,
        "templates_dir": args.templates_dir,
        "auto_approve": args.auto_approve,
    }

    if args.config:
        config_from_file = json.loads(Path(args.config).read_text(encoding="utf-8"))
        config.update(config_from_file)

    # BETO-TRACE: BETO_EXECUTOR.SEC8.DECISION.LLM_MODELS_CONFIGURABLE
    print(f"[BETO_EXECUTOR] Reasoning model : {config['reasoning_model']}")
    print(f"[BETO_EXECUTOR] Code model      : {config['code_model']}")
    print(f"[BETO_EXECUTOR] LiteLLM URL     : {config['litellm_base_url']}")
    print(f"[BETO_EXECUTOR] Cycle dir       : {config['cycle_output_dir']}")
    print(f"[BETO_EXECUTOR] Gate G-4        : {'activado' if config['g4_configurado'] else 'no configurado'}")

    executor = BETOExecutorRoot(config)

    try:
        output_dir = executor.ejecutar(idea_raw)
        print(f"\n[BETO_EXECUTOR] Pipeline completado.")
        print(f"[BETO_EXECUTOR] Sistema materializado en: {output_dir}")
        sys.exit(0)
    except RuntimeError as e:
        print(f"\n[BETO_EXECUTOR] Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[BETO_EXECUTOR] Ciclo interrumpido por el operador.", file=sys.stderr)
        print("[BETO_EXECUTOR] Estado PENDIENTE persistido. Reanudable.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
