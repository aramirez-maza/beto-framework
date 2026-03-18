"""
BETO_STATE schema — dataclasses + JSON serialization.
All fields are optional-safe: missing data yields empty strings/lists,
never raises. extraction_warnings captures what couldn't be extracted.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json


@dataclass
class NodoBETO:
    """Representa un nodo del BETO_SYSTEM_GRAPH."""
    id: str
    tipo: str          # ROOT | PARALLEL | SUBBETO | INTERNAL
    beto_core: str     # nombre del archivo BETO_CORE asociado
    intent: str = ""   # extracto de SEC1 del BETO_CORE hijo, si ya existe


@dataclass
class OQ:
    """Open Question — abierta o cerrada.

    Campos OSC (BETO v4.3 — Operational Semantic Closure Layer):
      oq_type:           OQ_CONFIG | OQ_POLICY | OQ_EXECUTION | OQ_EXCEPTION |
                         OQ_DATA_SEMANTICS | OQ_INTERFACE | OQ_OBSERVABILITY | NOT_CLASSIFIED
      critical:          True si la OQ impacta comportamiento, decisión, flujo, tiempo,
                         política, conflicto, excepción, datos, interfaces, riesgo,
                         observabilidad o fallback.
      execution_state:   DECLARED_EXECUTABLE | DECLARED_WITH_LIMITS | DECLARED_RAW | PENDING
      execution_readiness_check: PASS_EXECUTABLE | PASS_WITH_LIMITS | FAIL_EXECUTIONAL_GAP | NOT_EVALUATED
      requestion_count:  número de repreguntas realizadas (máximo = 2)
    """
    id: str
    texto: str
    modo_cierre: str = ""    # BETO_ASSISTED | HUMAN | vacío si abierta
    resolucion: str = ""     # resumen de la resolución
    # OSC fields — BETO v4.3
    oq_type: str = "NOT_CLASSIFIED"   # tipología operativa
    critical: bool = False             # es OQ crítica
    execution_state: str = "PENDING"  # estado de ejecutabilidad
    execution_readiness_check: str = "NOT_EVALUATED"  # resultado del check
    requestion_count: int = 0         # repreguntas realizadas (max 2)


@dataclass
class BETOState:
    """
    Estado epistémico completo del ciclo en un momento dado.
    Generado y actualizado por BETOStateWriter después de cada paso.
    """
    ciclo_id: str
    paso_actual: int

    # Identidad del sistema
    system_name: str = ""
    system_intent: str = ""
    system_boundaries_in: list[str] = field(default_factory=list)
    system_boundaries_out: list[str] = field(default_factory=list)
    stable_decisions: list[str] = field(default_factory=list)

    # Estructura del sistema
    nodos: list[NodoBETO] = field(default_factory=list)

    # Open Questions
    oqs_abiertas: list[OQ] = field(default_factory=list)
    oqs_cerradas: list[OQ] = field(default_factory=list)

    # Gaps y gates
    gaps_activos: list[dict] = field(default_factory=list)
    decisiones_gate: list[dict] = field(default_factory=list)

    # OSC — Operational Semantic Closure (BETO v4.3)
    # Campos nuevos para la capa de cierre operativo semántico
    executional_gap_count: int = 0           # número de BETO_GAP_EXECUTIONAL activos
    requestion_history: list[dict] = field(default_factory=list)  # historial de repreguntas
    operational_residue: list[dict] = field(default_factory=list) # ambigüedad residual aceptada
    accepted_limits: list[dict] = field(default_factory=list)     # límites operativos declarados
    # Resultados del gate G-2B (Operational Readiness Gate)
    g2b_result: str = ""   # APPROVED_EXECUTABLE | APPROVED_WITH_LIMITS | BLOCKED_BY_EXECUTIONAL_GAPS | PENDING

    # Auditoría de extracción
    extraction_warnings: list[str] = field(default_factory=list)
    generado_en_paso: int = 0
    timestamp: str = ""

    # Routing & Efficiency fields — BETO v4.4 (Execution Efficiency and Routing Layer)
    # All new fields have safe defaults — backward-compatible with v4.3 state files.

    # Active routing state
    current_route_type: str = ""         # BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH | ""
    last_routing_decision_id: str = ""   # ID of the last ROUTING_DECISION_RECORD (RD-YYYY-NNNN)
    route_promotion_count: int = 0       # Number of route promotions in this cycle
    last_promotion_id: str = ""          # ID of the last ROUTE_PROMOTION_RECORD (RP-YYYY-NNNN)

    # Snapshot tracking
    active_snapshots: list[dict] = field(default_factory=list)
    # Each entry: {"snapshot_id": "CS-...", "snapshot_type": "...", "validity_state": "VALID|INVALIDATED"}
    invalidated_snapshots: list[dict] = field(default_factory=list)

    # PROJECT_INDEX
    project_index_path: str = ""         # Path to .beto/project_index.json
    project_index_last_updated: str = "" # ISO 8601 timestamp

    # MODEL_CALL_PLAN log (summary — full entries in EXECUTION_PERFORMANCE_LOG)
    model_call_count: int = 0            # Total model calls in this cycle
    model_call_log: list[dict] = field(default_factory=list)
    # Each entry: {"call_id": "MCP-...", "route_type": "...", "call_status": "..."}

    # Routing decision registry (summary — full records in .beto/routing/)
    routing_decisions: list[dict] = field(default_factory=list)
    # Each entry: {"decision_id": "RD-...", "route_selected": "...", "raw_score": float}
    route_promotions: list[dict] = field(default_factory=list)
    # Each entry: {"promotion_id": "RP-...", "transition": "...", "trigger": "..."}

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    def to_context_block(self) -> str:
        """
        Formatea BETO_STATE como bloque de texto para inyección en el contexto LLM.
        Texto estructurado — más legible que JSON para el LLM.
        """
        lines = [
            f"BETO_STATE — Ciclo {self.ciclo_id} | Paso actual: {self.paso_actual}",
            f"Sistema: {self.system_name}",
            "",
        ]

        if self.system_intent:
            lines += ["## SYSTEM INTENT", self.system_intent.strip(), ""]

        if self.system_boundaries_in or self.system_boundaries_out:
            lines.append("## SYSTEM BOUNDARIES")
            if self.system_boundaries_in:
                lines.append("In scope:")
                for item in self.system_boundaries_in:
                    lines.append(f"  - {item}")
            if self.system_boundaries_out:
                lines.append("Out of scope:")
                for item in self.system_boundaries_out:
                    lines.append(f"  - {item}")
            lines.append("")

        if self.stable_decisions:
            lines.append("## STABLE TECHNICAL DECISIONS")
            for d in self.stable_decisions:
                lines.append(f"  - {d}")
            lines.append("")

        if self.nodos:
            lines.append("## NODOS DEL SISTEMA")
            for n in self.nodos:
                intent_part = f" | intent: {n.intent[:80]}..." if n.intent else ""
                lines.append(f"  [{n.tipo}] {n.id} → {n.beto_core}{intent_part}")
            lines.append("")

        if self.oqs_abiertas:
            lines.append("## OQs ABIERTAS")
            for oq in self.oqs_abiertas:
                lines.append(f"  {oq.id}: {oq.texto[:120]}")
            lines.append("")

        if self.oqs_cerradas:
            lines.append("## OQs CERRADAS")
            for oq in self.oqs_cerradas:
                modo = f" [{oq.modo_cierre}]" if oq.modo_cierre else ""
                res = f" → {oq.resolucion[:80]}" if oq.resolucion else ""
                lines.append(f"  {oq.id}{modo}{res}")
            lines.append("")

        if self.gaps_activos:
            lines.append("## GAPS ACTIVOS")
            # Mostrar máximo 10 gaps — suficiente para que el LLM tenga conciencia de deuda
            for g in self.gaps_activos[:10]:
                lines.append(f"  {g.get('gap_id', '?')}: {g.get('descripcion', '')[:100]}")
            if len(self.gaps_activos) > 10:
                lines.append(f"  ... y {len(self.gaps_activos) - 10} gaps adicionales")
            lines.append("")

        if self.decisiones_gate:
            lines.append("## DECISIONES DE GATE")
            seen = {}
            for d in self.decisiones_gate:
                gate = d.get("gate_id", "?")
                dec = d.get("decision", "?")
                if dec != "PENDIENTE":
                    seen[gate] = dec
            for gate, dec in seen.items():
                lines.append(f"  {gate}: {dec}")
            lines.append("")

        # OSC summary — BETO v4.3
        if self.executional_gap_count > 0 or self.g2b_result:
            lines.append("## OSC — OPERATIONAL SEMANTIC CLOSURE (BETO v4.3)")
            if self.g2b_result:
                lines.append(f"  Gate G-2B: {self.g2b_result}")
            if self.executional_gap_count > 0:
                lines.append(f"  BETO_GAP_EXECUTIONAL activos: {self.executional_gap_count}")
            if self.accepted_limits:
                lines.append(f"  Límites aceptados (DECLARED_WITH_LIMITS): {len(self.accepted_limits)}")
            if self.operational_residue:
                lines.append(f"  Ambigüedad residual registrada: {len(self.operational_residue)}")
            lines.append("")

        # OQs con ejecución crítica
        oqs_raw = [oq for oq in self.oqs_abiertas if getattr(oq, "execution_state", "") == "DECLARED_RAW"]
        if oqs_raw:
            lines.append("## OQs BLOQUEANTES (DECLARED_RAW — requieren EXECUTION_READINESS_CHECK)")
            for oq in oqs_raw:
                lines.append(f"  {oq.id} [{getattr(oq, 'oq_type', '?')}]: {oq.texto[:100]}")
            lines.append("")

        if self.extraction_warnings:
            lines.append("## EXTRACTION WARNINGS (campos no extraídos — ver artefacto completo)")
            for w in self.extraction_warnings:
                lines.append(f"  ⚠ {w}")
            lines.append("")

        # Routing state — BETO v4.4
        if self.current_route_type or self.route_promotion_count > 0:
            lines.append("## ROUTING STATE (BETO v4.4)")
            if self.current_route_type:
                lines.append(f"  Ruta activa: {self.current_route_type}")
            if self.last_routing_decision_id:
                lines.append(f"  Última decisión: {self.last_routing_decision_id}")
            if self.route_promotion_count > 0:
                lines.append(f"  Promociones de ruta: {self.route_promotion_count}")
            if self.last_promotion_id:
                lines.append(f"  Última promoción: {self.last_promotion_id}")
            if self.model_call_count > 0:
                lines.append(f"  Llamadas al modelo: {self.model_call_count}")
            active_valid = [s for s in self.active_snapshots if s.get("validity_state") == "VALID"]
            if active_valid:
                lines.append(f"  Snapshots activos válidos: {len(active_valid)}")
            lines.append("")

        return "\n".join(lines)
