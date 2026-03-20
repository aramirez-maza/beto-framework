#!/usr/bin/env python3
# BETO-TRACE: BETO-EVO2.ROOT.SYSTEM.Intent
# BETO-TRACE: BETO-EVO2.SEC5.RF.RF-01
# BETO-TRACE: BETO-EVO2.SEC5.RF.RF-06
"""
BETO-EVO2 — Entry Point
Wrapper de gobernanza epistemica BETO sobre Evo2.

Garantia del sistema:
  - Ningun parametro genomico critico puede ser inferido silenciosamente.
  - Ninguna llamada a Evo2 se ejecuta sin los 3 gates aprobados por el operador.
  - Todo resultado sale con TRACE_VERIFIED y epistemic_manifest completo.

Uso:
  python main.py --intent "diseña una secuencia que module BRCA1 en Homo sapiens,
                           BSL-2, 512bp, temp 0.7, top_k 4, excluded_motifs [],
                           modelo 7B" --task GENERATION --operator-id "scientist_01"

  python main.py --interactive   # modo interactivo guiado
  python main.py --export-registry  # exportar TRACE_REGISTRY.json
"""

import argparse
import json
import sys
from pathlib import Path

from beto_spec_engine import BETOSpecEngine
from evo2_adapter import Evo2Adapter
from gate_manager import GateManager
from models import AuthorizedEvo2Result, GenomicRequest, TaskType
from trace_logger import TraceLogger


# BETO-TRACE: BETO-EVO2.SEC6.METHOD.BETOSpecEngine.parse
# BETO-TRACE: BETO-EVO2.SEC6.METHOD.GateManager.present_gate_a
# BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.execute
# BETO-TRACE: BETO-EVO2.SEC6.METHOD.TraceLogger.persist
def run_pipeline(
    request: GenomicRequest,
    hf_token: str | None = None,
    db_path: str = "beto_evo2.db",
) -> AuthorizedEvo2Result:
    """
    Pipeline BETO-EVO2 completo.
    BETO-TRACE: BETO-EVO2.ROOT.SYSTEM.Intent
    Las 4 fases se ejecutan en secuencia estricta.
    """
    spec_engine  = BETOSpecEngine()
    gate_manager = GateManager()
    evo2_adapter = Evo2Adapter(nvidia_api_key=hf_token)
    trace_logger = TraceLogger(db_path=db_path)

    print("\n" + "=" * 54)
    print("  BETO-EVO2 — Gobernanza Epistemica sobre Evo2")
    print("  Protocolo: BETO v4.4 | Zero silent completions")
    print("=" * 54)

    # ── FASE 1: Especificacion Epistemica ─────────────────────
    # BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase1_EspecificacionEpistemica
    print("\n[FASE 1] Especificacion epistemica de parametros...\n")
    param_map = spec_engine.parse(request)

    # Si hay parametros NOT_STATED: presentar al operador y recolectar
    while not param_map.is_executable:
        print(spec_engine.format_gap_report(param_map))
        print("Declare los parametros faltantes (uno por linea).")
        print("Formato: nombre_parametro = valor")
        print("Escriba 'cancelar' para abortar.\n")

        line = input("> ").strip()
        if line.lower() in ("cancelar", "cancel", "exit", "quit"):
            print("[BETO-EVO2] Ciclo cancelado por el operador.")
            sys.exit(0)

        if "=" in line:
            parts = line.split("=", 1)
            param_name = parts[0].strip()
            value = parts[1].strip()
            try:
                param_map = spec_engine.apply_operator_declaration(param_map, param_name, value)
                print(f"  ✓ {param_name} declarado como DECLARED.")
            except ValueError as e:
                print(f"  ✗ Error: {e}")
        else:
            print("  Formato no reconocido. Use: nombre_parametro = valor")

    print("\n  Todos los parametros criticos: DECLARED")
    print(f"  Parametros bloqueantes: 0")

    # ── FASE 2: Gobierno de Gates ──────────────────────────────
    # BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase2_GobiernodeGates
    print("\n[FASE 2] Gobierno de gates...\n")

    gate_record, approved_a = gate_manager.present_gate_a(param_map, request.operator_id)
    if not approved_a:
        print("[BETO-EVO2] Gate-A rechazado por el operador. Ciclo terminado.")
        sys.exit(0)

    critical = None
    while critical is None:
        gate_record, approved_b, critical = gate_manager.present_gate_b(
            param_map, gate_record, request.operator_id
        )
        if not approved_b and critical is None:
            # Modificacion solicitada — recolectar cambios
            print("\nIngrese modificaciones (formato: nombre_parametro = valor).")
            print("Escriba 'listo' cuando termine.\n")
            while True:
                line = input("> ").strip()
                if line.lower() in ("listo", "done", "ok"):
                    break
                if "=" in line:
                    parts = line.split("=", 1)
                    pname = parts[0].strip()
                    pval = parts[1].strip()
                    try:
                        param_map = spec_engine.apply_operator_declaration(param_map, pname, pval)
                        print(f"  ✓ {pname} actualizado.")
                    except ValueError as e:
                        print(f"  ✗ Error: {e}")
        elif not approved_b:
            print("[BETO-EVO2] Gate-B rechazado por el operador. Ciclo terminado.")
            sys.exit(0)

    gate_record, approved_c = gate_manager.present_gate_c(
        critical, gate_record, request.operator_id
    )
    if not approved_c:
        print("[BETO-EVO2] Gate-C rechazado por el operador. Ciclo terminado.")
        sys.exit(0)

    print("\n  Gates A, B, C: APROBADOS por el operador.")

    # ── FASE 3: Ejecucion Autorizada ───────────────────────────
    # BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase3_EjecucionAutorizada
    print("\n[FASE 3] Ejecutando Evo2 (parametros autorizados)...\n")

    evo2_response = evo2_adapter.execute(critical, gate_record)

    if evo2_response.error:
        print(f"\n[BETO-EVO2] Error en Evo2: {evo2_response.error}")
        print("El ciclo se interrumpe. El operador debe revisar la especificacion.")
        sys.exit(1)

    print(f"  Modelo:    {evo2_response.model_used}")
    print(f"  Latencia:  {evo2_response.latency_ms} ms")
    print(f"  Hash:      {evo2_response.payload_hash}")

    # ── FASE 4: Auditoria y Trazabilidad ───────────────────────
    # BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase4_AuditoriaTrazabilidad
    print("\n[FASE 4] Generando trazabilidad...\n")

    trace_id = trace_logger.generate_trace_id()
    manifest  = trace_logger.build_manifest(param_map, gate_record, evo2_response)
    spec_hash = trace_logger.persist(trace_id, param_map, gate_record, evo2_response, manifest)

    result = trace_logger.build_result(
        trace_id, spec_hash, evo2_response, gate_record, manifest
    )

    print(f"  TRACE_ID:  {result.trace_id}")
    print(f"  SPEC_HASH: {result.spec_hash}")
    print(f"  Estado:    {result.trace_status.value}")
    print(f"\n  Resumen epistemico:")
    summary = manifest.get("epistemic_summary", {})
    print(f"    DECLARED:   {summary.get('declared', 0)}")
    print(f"    NOT_STATED: {summary.get('not_stated', 0)}")
    print(f"    INFERRED:   {summary.get('inferred', 0)}")
    print()

    return result


def main() -> None:
    # BETO-TRACE: BETO-EVO2.ROOT.SYSTEM.Intent
    parser = argparse.ArgumentParser(
        description="BETO-EVO2: Gobernanza epistemica BETO sobre Evo2"
    )
    parser.add_argument(
        "--intent",
        type=str,
        help="Descripcion de la solicitud genomica (texto libre)",
    )
    parser.add_argument(
        "--task",
        type=str,
        choices=["GENERATION", "SCORING", "EMBEDDING"],
        default="GENERATION",
        help="Tipo de tarea Evo2 (debe ser DECLARED por el operador)",
    )
    parser.add_argument(
        "--operator-id",
        type=str,
        default="operator_001",
        help="Identificador del operador cientifico",
    )
    parser.add_argument(
        "--seed",
        type=str,
        default=None,
        help="Secuencia semilla (opcional segun tarea)",
    )
    parser.add_argument(
        "--hf-token",
        type=str,
        default=None,
        help="Token de Hugging Face para Evo2 API",
    )
    parser.add_argument(
        "--db",
        type=str,
        default="beto_evo2.db",
        help="Ruta al archivo SQLite de persistencia",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Modo interactivo: guia al operador paso a paso",
    )
    parser.add_argument(
        "--export-registry",
        action="store_true",
        help="Exportar TRACE_REGISTRY.json y salir",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Guardar resultado en archivo JSON",
    )

    args = parser.parse_args()

    # Exportar registry sin ejecutar pipeline
    if args.export_registry:
        logger = TraceLogger(db_path=args.db)
        logger.export_trace_registry()
        sys.exit(0)

    # Modo interactivo
    if args.interactive or not args.intent:
        print("\nBETO-EVO2 — Modo interactivo")
        print("Describe tu solicitud genomica. El sistema detectara parametros automaticamente.")
        print("Los parametros no encontrados seran solicitados explicitamente.\n")
        args.intent = input("Solicitud genomica: ").strip()
        if not args.intent:
            print("Solicitud vacia. Abortando.")
            sys.exit(1)

    request = GenomicRequest(
        raw_intent=args.intent,
        task_type=TaskType(args.task),
        operator_id=args.operator_id,
        seed_sequence=args.seed,
    )

    result = run_pipeline(
        request=request,
        hf_token=args.hf_token,
        db_path=args.db,
    )

    if args.output:
        output_data = {
            "trace_id":           result.trace_id,
            "evo2_output":        result.evo2_output,
            "spec_hash":          result.spec_hash,
            "trace_status":       result.trace_status.value,
            "model_used":         result.model_used,
            "latency_ms":         result.latency_ms,
            "epistemic_manifest": result.epistemic_manifest,
        }
        Path(args.output).write_text(
            json.dumps(output_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"[BETO-EVO2] Resultado guardado en: {args.output}")
    else:
        print("\nResultado Evo2:")
        output = result.evo2_output
        if isinstance(output, str) and len(output) > 120:
            print(f"  {output[:120]}...")
        else:
            print(f"  {output}")


if __name__ == "__main__":
    main()
