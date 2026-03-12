"""
BETO-TRACE: BETO_GESTOR.SEC1.INTENT.CYCLE_STATE_PERSISTENCE
BETO-TRACE: BETO_GESTOR.SEC1.INTENT.CICLO_ID_GENERATION
BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_1_CREACION_CICLO
BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
BETO-TRACE: BETO_GESTOR.SEC8.DECISION.CICLO_ID_UUID
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .duplicate_detector import compute_idea_raw_hash, find_duplicate


class GestorCiclo:
    """
    BETO-TRACE: BETO_GESTOR.SEC1.INTENT.CYCLE_STATE_PERSISTENCE
    BETO-TRACE: BETO_GESTOR.SEC6.MODEL.CICLO_CREATOR

    Gestiona el estado persistente de los ciclos BETO.
    Backend: archivos JSON en cycle_output_dir ({ciclo_id}.json).
    """

    def __init__(self, cycle_output_dir: str | Path):
        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
        self.cycle_output_dir = Path(cycle_output_dir)
        self.cycle_output_dir.mkdir(parents=True, exist_ok=True)

    def crear_ciclo(self, idea_raw: str) -> dict:
        """
        BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_1_CREACION_CICLO
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.CICLO_ID_UUID
        BETO-TRACE: BETO_GESTOR.SEC5.INVARIANT.IDEA_RAW_IMMUTABLE

        Genera ciclo_id UUID, detecta duplicados, crea y persiste estado inicial.

        Retorna:
            dict con keys: ciclo_id, duplicate (None o estado previo)
        """
        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.DUPLICATE_SHA256
        idea_raw_hash = compute_idea_raw_hash(idea_raw)

        # BETO-TRACE: BETO_GESTOR.SEC2.BOUNDARY.DUPLICATE_COMPARISON
        duplicate = find_duplicate(idea_raw_hash, self.cycle_output_dir)
        if duplicate:
            return {"ciclo_id": None, "duplicate": duplicate}

        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.CICLO_ID_UUID
        ciclo_id = str(uuid.uuid4())

        # BETO-TRACE: BETO_GESTOR.SEC3.OUTPUT.INITIAL_STATE
        state = {
            "ciclo_id": ciclo_id,
            "idea_raw_hash": idea_raw_hash,
            "idea_raw": idea_raw,
            "paso_actual": 0,
            "artefactos": [],
            "decisiones_gate": [],
            "beto_gaps": [],
            "estado_ciclo": "EN_PROGRESO",
            "timestamp_creacion": datetime.now(timezone.utc).isoformat(),
        }

        # BETO-TRACE: BETO_GESTOR.SEC8.DECISION.WRITE_BEFORE_CONFIRM
        self._persist(ciclo_id, state)

        return {"ciclo_id": ciclo_id, "duplicate": None}

    def crear_ciclo_nuevo_ignorando_duplicado(self, idea_raw: str) -> str:
        """
        BETO-TRACE: BETO_GESTOR.SEC7.PHASE.PHASE_1_CREACION_CICLO
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.CICLO_ID_UUID

        Crea un ciclo nuevo aunque exista un duplicado (operador eligió 'nuevo').
        El ciclo previo no es modificado.
        """
        ciclo_id = str(uuid.uuid4())
        idea_raw_hash = compute_idea_raw_hash(idea_raw)

        state = {
            "ciclo_id": ciclo_id,
            "idea_raw_hash": idea_raw_hash,
            "idea_raw": idea_raw,
            "paso_actual": 0,
            "artefactos": [],
            "decisiones_gate": [],
            "beto_gaps": [],
            "estado_ciclo": "EN_PROGRESO",
            "timestamp_creacion": datetime.now(timezone.utc).isoformat(),
        }

        self._persist(ciclo_id, state)
        return ciclo_id

    def _persist(self, ciclo_id: str, state: dict) -> None:
        """
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.WRITE_BEFORE_CONFIRM
        """
        path = self.cycle_output_dir / f"{ciclo_id}.json"
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_cycle_dir(self) -> Path:
        """
        BETO-TRACE: BETO_GESTOR.SEC8.DECISION.JSON_BACKEND
        """
        return self.cycle_output_dir
