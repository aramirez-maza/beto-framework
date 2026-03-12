"""
BETO-TRACE: BETO_GESTOR.SEC1.INTENT.DUPLICATE_DETECTION
BETO-TRACE: BETO_GESTOR.SEC8.DECISION.DUPLICATE_SHA256
BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_COMPARISON
"""

import hashlib
import json
from pathlib import Path


def compute_idea_raw_hash(idea_raw: str) -> str:
    """
    BETO-TRACE: BETO_GESTOR.SEC8.DECISION.DUPLICATE_SHA256
    Calcula el hash SHA-256 de IDEA_RAW normalizada (strip + colapso de espacios).
    Previene falsos negativos por diferencias de whitespace irrelevantes.
    """
    normalized = " ".join(idea_raw.split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def find_duplicate(idea_raw_hash: str, cycle_output_dir: Path) -> dict | None:
    """
    BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_COMPARISON
    BETO-TRACE: BETO_GESTOR.SEC5.INVARIANT.CICLO_ID_IMMUTABLE

    Busca en cycle_output_dir un ciclo existente cuyo idea_raw_hash coincida
    y cuyo estado_ciclo no sea 'FINALIZADO'.

    Retorna el estado del ciclo previo si se encuentra duplicado, o None.
    """
    if not cycle_output_dir.exists():
        return None

    for json_file in cycle_output_dir.glob("*.json"):
        try:
            state = json.loads(json_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        if (
            state.get("idea_raw_hash") == idea_raw_hash
            and state.get("estado_ciclo") != "FINALIZADO"
        ):
            return state

    return None
