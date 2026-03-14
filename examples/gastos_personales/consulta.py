# BETO-TRACE: GASTOS_CONSULTA.SEC1.INTENT.CONSULTA_GASTOS
# Motor de Consulta de Gastos Personales
# BETO v4.2 — TRACE_VERIFIED

import json
from datetime import datetime
from pathlib import Path

GASTOS_FILE = Path("gastos.json")


def _cargar_gastos() -> list:
    # BETO-TRACE: GASTOS_CONSULTA.SEC8.DECISION.CARGA_MEMORIA
    if not GASTOS_FILE.exists():
        return []
    with open(GASTOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def consultar_gastos(
    categoria: str = None,
    fecha_inicio: str = None,
    fecha_fin: str = None
) -> dict:
    """
    Filtra gastos y retorna lista + resumen por categoría.
    BETO-TRACE: GASTOS_CONSULTA.SEC4.UNIT.CONSULTA_FILTRO
    BETO-TRACE: GASTOS_CONSULTA.SEC3.INPUT.FILTRO_CATEGORIA
    BETO-TRACE: GASTOS_CONSULTA.SEC3.INPUT.FILTRO_FECHA_INICIO
    BETO-TRACE: GASTOS_CONSULTA.SEC3.INPUT.FILTRO_FECHA_FIN
    """
    # BETO-TRACE: GASTOS_CONSULTA.SEC7.PHASE.CARGA_FILTRADO
    gastos = _cargar_gastos()
    filtrados = []

    for g in gastos:
        if categoria and g["categoria"].lower() != categoria.lower():
            continue
        if fecha_inicio:
            if datetime.strptime(g["fecha"], "%Y-%m-%d") < datetime.strptime(fecha_inicio, "%Y-%m-%d"):
                continue
        if fecha_fin:
            if datetime.strptime(g["fecha"], "%Y-%m-%d") > datetime.strptime(fecha_fin, "%Y-%m-%d"):
                continue
        filtrados.append(g)

    # BETO-TRACE: GASTOS_CONSULTA.SEC7.PHASE.AGREGACION_DISPLAY
    # BETO-TRACE: GASTOS_CONSULTA.SEC4.UNIT.RESULTADO_CONSULTA
    resumen = {}
    for g in filtrados:
        cat = g["categoria"]
        resumen[cat] = resumen.get(cat, 0.0) + g["monto"]

    # BETO-TRACE: GASTOS_CONSULTA.SEC3.OUTPUT.LISTA_GASTOS
    # BETO-TRACE: GASTOS_CONSULTA.SEC3.OUTPUT.RESUMEN_TOTALES
    return {"gastos": filtrados, "resumen": resumen}


def formatear_resultado(resultado: dict) -> str:
    # BETO-TRACE: GASTOS_CONSULTA.SEC8.DECISION.DISPLAY_TABLA_CLI
    gastos = resultado["gastos"]
    resumen = resultado["resumen"]

    if not gastos:
        return "No se encontraron gastos con los filtros aplicados."

    lineas = []
    lineas.append(f"{'Fecha':<12} {'Categoría':<20} {'Monto':>10}  Descripción")
    lineas.append("-" * 60)
    for g in gastos:
        desc = g["descripcion"] or "-"
        lineas.append(f"{g['fecha']:<12} {g['categoria']:<20} ${g['monto']:>9.2f}  {desc}")

    lineas.append("-" * 60)
    lineas.append("TOTALES POR CATEGORÍA:")
    for cat, total in resumen.items():
        lineas.append(f"  {cat:<20} ${total:.2f}")

    return "\n".join(lineas)
