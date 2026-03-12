"""
BETOStateWriter — orquesta la actualización de BETO_STATE.json después de cada paso.

Estrategia por paso:
  Paso 0-1: solo ciclo_id + paso_actual (aún no hay artefactos ricos)
  Paso 2:   agrega system_intent, boundaries, STDs, OQs (desde BETO_CORE_DRAFT)
  Paso 4:   agrega nodos (desde BETO_SYSTEM_GRAPH)
  Paso 5:   enriquece nodos con intent de sus BETO_COREs hijos
  Paso 6:   agrega OQs cerradas (desde CIERRE_ASISTIDO)
  Paso 7+:  actualiza gaps y decisiones de gate desde state JSON

Siempre lee el BETO_STATE.json existente y lo actualiza incrementalmente.
Nunca borra información previamente extraída — solo agrega o actualiza.
"""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path

from .schema import BETOState, NodoBETO, OQ
from .extractor import (
    extract_from_beto_core_draft,
    extract_from_beto_system_graph,
    extract_from_cierre_asistido,
    extract_from_state_json,
    extract_node_intent,
)

BETO_STATE_FILENAME = "BETO_STATE.json"


class BETOStateWriter:
    """
    Actualiza BETO_STATE.json en el cycle_dir después de cada paso.
    Thread-safe no requerido — BETO_EXECUTOR es single-process.
    """

    def __init__(self, cycle_dir: Path, ciclo_id: str):
        self.cycle_dir = cycle_dir
        self.ciclo_id = ciclo_id
        self.state_path = cycle_dir / BETO_STATE_FILENAME

    def update(self, paso: int) -> BETOState:
        """
        Lee el estado actual, aplica las extracciones correspondientes al paso,
        escribe BETO_STATE.json actualizado. Retorna el BETOState resultante.
        """
        state = self._load_or_create(paso)
        state.paso_actual = paso
        state.generado_en_paso = paso
        state.timestamp = datetime.now(timezone.utc).isoformat()

        warnings = state.extraction_warnings

        # — Paso 1+: extraer desde BETO_CORE_DRAFT —
        if paso >= 1:
            self._update_from_beto_core_draft(state, warnings)

        # — Paso 4+: extraer nodos desde BETO_SYSTEM_GRAPH —
        if paso >= 4:
            self._update_from_beto_system_graph(state, warnings)

        # — Paso 5+: enriquecer nodos con intent de sus BETO_COREs hijos —
        if paso >= 5:
            self._enrich_node_intents(state, warnings)

        # — Paso 6+: OQs cerradas desde CIERRE_ASISTIDO —
        if paso >= 6:
            self._update_from_cierre_asistido(state, warnings)

        # — Siempre: gaps y gates desde state JSON —
        self._update_from_state_json(state, warnings)

        # Deduplicar warnings
        state.extraction_warnings = list(dict.fromkeys(warnings))

        self._save(state)
        return state

    # ------------------------------------------------------------------

    def _load_or_create(self, paso: int) -> BETOState:
        if self.state_path.exists():
            try:
                import json, dataclasses
                raw = json.loads(self.state_path.read_text(encoding="utf-8"))
                # Reconstruir dataclasses desde dict
                nodos = [NodoBETO(**n) for n in raw.get("nodos", [])]
                oqs_a = [OQ(**o) for o in raw.get("oqs_abiertas", [])]
                oqs_c = [OQ(**o) for o in raw.get("oqs_cerradas", [])]
                return BETOState(
                    ciclo_id=raw.get("ciclo_id", self.ciclo_id),
                    paso_actual=raw.get("paso_actual", paso),
                    system_name=raw.get("system_name", ""),
                    system_intent=raw.get("system_intent", ""),
                    system_boundaries_in=raw.get("system_boundaries_in", []),
                    system_boundaries_out=raw.get("system_boundaries_out", []),
                    stable_decisions=raw.get("stable_decisions", []),
                    nodos=nodos,
                    oqs_abiertas=oqs_a,
                    oqs_cerradas=oqs_c,
                    gaps_activos=raw.get("gaps_activos", []),
                    decisiones_gate=raw.get("decisiones_gate", []),
                    extraction_warnings=raw.get("extraction_warnings", []),
                    generado_en_paso=raw.get("generado_en_paso", 0),
                    timestamp=raw.get("timestamp", ""),
                )
            except Exception:
                pass  # Si falla la carga, crear desde cero
        return BETOState(ciclo_id=self.ciclo_id, paso_actual=paso)

    def _save(self, state: BETOState) -> None:
        self.state_path.write_text(state.to_json(), encoding="utf-8")

    def _read_artifact(self, nombre: str) -> str | None:
        ruta = self.cycle_dir / nombre
        if ruta.exists():
            return ruta.read_text(encoding="utf-8")
        return None

    # ------------------------------------------------------------------

    def _update_from_beto_core_draft(self, state: BETOState, warnings: list[str]) -> None:
        content = self._read_artifact("BETO_CORE_DRAFT.md")
        if not content:
            warnings.append("BETO_CORE_DRAFT.md no encontrado en cycle_dir")
            return

        data = extract_from_beto_core_draft(content, warnings)

        # Solo actualizar si hay datos — nunca sobreescribir con vacío
        if data["system_name"] and not state.system_name:
            state.system_name = data["system_name"]
        if data["system_intent"]:
            state.system_intent = data["system_intent"]
        if data["system_boundaries_in"]:
            state.system_boundaries_in = data["system_boundaries_in"]
        if data["system_boundaries_out"]:
            state.system_boundaries_out = data["system_boundaries_out"]
        if data["stable_decisions"]:
            state.stable_decisions = data["stable_decisions"]

        # OQs: merge sin duplicar por ID
        existing_oq_ids = {oq.id for oq in state.oqs_abiertas} | {oq.id for oq in state.oqs_cerradas}
        for oq in data["oqs_abiertas"]:
            if oq.id not in existing_oq_ids:
                state.oqs_abiertas.append(oq)
                existing_oq_ids.add(oq.id)
        for oq in data["oqs_cerradas"]:
            if oq.id not in existing_oq_ids:
                state.oqs_cerradas.append(oq)
                existing_oq_ids.add(oq.id)
            # Si estaba abierta, moverla a cerradas
            elif oq.id in {o.id for o in state.oqs_abiertas}:
                state.oqs_abiertas = [o for o in state.oqs_abiertas if o.id != oq.id]
                state.oqs_cerradas.append(oq)

    def _update_from_beto_system_graph(self, state: BETOState, warnings: list[str]) -> None:
        content = self._read_artifact("BETO_SYSTEM_GRAPH.md")
        if not content:
            warnings.append("BETO_SYSTEM_GRAPH.md no encontrado en cycle_dir")
            return

        data = extract_from_beto_system_graph(content, warnings)

        if data["system_name"] and not state.system_name:
            state.system_name = data["system_name"]
        elif data["system_name"]:
            # El grafo tiene el nombre canónico — tiene precedencia
            state.system_name = data["system_name"]

        if data["nodos"]:
            # Reemplazar lista de nodos con la del grafo (fuente de verdad)
            # Preservar intents ya extraídos
            existing_intents = {n.id: n.intent for n in state.nodos if n.intent}
            state.nodos = data["nodos"]
            for n in state.nodos:
                if n.id in existing_intents:
                    n.intent = existing_intents[n.id]

    def _enrich_node_intents(self, state: BETOState, warnings: list[str]) -> None:
        """Lee cada BETO_CORE hijo disponible y extrae su intent."""
        for nodo in state.nodos:
            if nodo.intent or not nodo.beto_core:
                continue
            content = self._read_artifact(nodo.beto_core)
            if content:
                intent = extract_node_intent(content)
                if intent:
                    nodo.intent = intent
                else:
                    warnings.append(f"Nodo {nodo.id}: no se extrajo intent de {nodo.beto_core}")

    def _update_from_cierre_asistido(self, state: BETOState, warnings: list[str]) -> None:
        content = self._read_artifact("CIERRE_ASISTIDO.md")
        if not content:
            warnings.append("CIERRE_ASISTIDO.md no encontrado en cycle_dir")
            return

        data = extract_from_cierre_asistido(content, warnings)
        oqs_cierre = data.get("oqs_cerradas_cierre", [])

        existing_cerradas = {oq.id: oq for oq in state.oqs_cerradas}
        abiertas_ids = {oq.id for oq in state.oqs_abiertas}

        for oq in oqs_cierre:
            if oq.id in existing_cerradas:
                # Enriquecer con modo y resolución si están vacíos
                existing = existing_cerradas[oq.id]
                if not existing.modo_cierre:
                    existing.modo_cierre = oq.modo_cierre
                if not existing.resolucion:
                    existing.resolucion = oq.resolucion
            else:
                state.oqs_cerradas.append(oq)
                # Remover de abiertas si estaba allí
                if oq.id in abiertas_ids:
                    state.oqs_abiertas = [o for o in state.oqs_abiertas if o.id != oq.id]

    def _update_from_state_json(self, state: BETOState, warnings: list[str]) -> None:
        """Lee el JSON del Gestor de Ciclo para gates y gaps."""
        json_path = self.cycle_dir.parent / f"{self.ciclo_id}.json"
        if not json_path.exists():
            # Fallback: buscar en cycle_dir
            candidates = list(self.cycle_dir.parent.glob(f"{self.ciclo_id}*.json"))
            if not candidates:
                return
            json_path = candidates[0]

        content = json_path.read_text(encoding="utf-8")
        data = extract_from_state_json(content, warnings)

        state.decisiones_gate = data["decisiones_gate"]
        state.gaps_activos = data["gaps_activos"]
