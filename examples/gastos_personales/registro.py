# BETO-TRACE: GASTOS_REGISTRO.SEC1.INTENT.REGISTRO_GASTO
# Motor de Registro de Gastos Personales
# BETO v4.2 — TRACE_VERIFIED

import json
import uuid
from datetime import datetime
from pathlib import Path

# BETO-TRACE: GASTOS_REGISTRO.SEC8.DECISION.JSON_APPEND
GASTOS_FILE = Path("gastos.json")


def _cargar_gastos() -> list:
    # BETO-TRACE: GASTOS_REGISTRO.SEC7.PHASE.PERSISTENCIA
    if not GASTOS_FILE.exists():
        return []
    with open(GASTOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar_gastos(gastos: list) -> None:
    # BETO-TRACE: GASTOS_REGISTRO.SEC7.PHASE.PERSISTENCIA
    with open(GASTOS_FILE, "w", encoding="utf-8") as f:
        json.dump(gastos, f, ensure_ascii=False, indent=2)


def _validar_input(monto: float, categoria: str, fecha: str) -> str | None:
    # BETO-TRACE: GASTOS_REGISTRO.SEC7.PHASE.VALIDACION_INPUT
    # BETO-TRACE: GASTOS_REGISTRO.SEC10.CONSTRAINT.MONTO_POSITIVO
    if monto <= 0:
        return "El monto debe ser mayor que cero."
    # BETO-TRACE: GASTOS_REGISTRO.SEC10.CONSTRAINT.CATEGORIA_NO_VACIA
    if not categoria or not categoria.strip():
        return "La categoría no puede estar vacía."
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return "La fecha debe tener formato YYYY-MM-DD."
    return None


def registrar_gasto(
    monto: float,
    categoria: str,
    fecha: str,
    descripcion: str = ""
) -> str:
    """
    Registra un gasto en gastos.json.
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.MONTO
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.CATEGORIA
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.FECHA
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.DESCRIPCION
    """
    error = _validar_input(monto, categoria, fecha)
    if error:
        return f"Error: {error}"

    # BETO-TRACE: GASTOS_REGISTRO.SEC4.UNIT.GASTO_ENTRY
    # BETO-TRACE: GASTOS_REGISTRO.SEC8.DECISION.UUID_ID
    gasto = {
        # BETO-TRACE: GASTOS_REGISTRO.SEC4.FIELD.ID
        "id": str(uuid.uuid4()),
        # BETO-TRACE: GASTOS_REGISTRO.SEC4.FIELD.MONTO
        "monto": monto,
        # BETO-TRACE: GASTOS_REGISTRO.SEC4.FIELD.CATEGORIA
        "categoria": categoria.strip(),
        # BETO-TRACE: GASTOS_REGISTRO.SEC4.FIELD.FECHA
        "fecha": fecha,
        # BETO-TRACE: GASTOS_REGISTRO.SEC4.FIELD.DESCRIPCION
        "descripcion": descripcion.strip(),
    }

    gastos = _cargar_gastos()
    gastos.append(gasto)
    _guardar_gastos(gastos)

    # BETO-TRACE: GASTOS_REGISTRO.SEC3.OUTPUT.CONFIRMACION
    return f"Gasto registrado: {categoria} — ${monto:.2f} el {fecha}"
