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
    """Open Question — abierta o cerrada."""
    id: str
    texto: str
    modo_cierre: str = ""    # BETO_ASSISTED | HUMAN | vacío si abierta
    resolucion: str = ""     # resumen de la resolución


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

    # Auditoría de extracción
    extraction_warnings: list[str] = field(default_factory=list)
    generado_en_paso: int = 0
    timestamp: str = ""

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

        if self.extraction_warnings:
            lines.append("## EXTRACTION WARNINGS (campos no extraídos — ver artefacto completo)")
            for w in self.extraction_warnings:
                lines.append(f"  ⚠ {w}")
            lines.append("")

        return "\n".join(lines)
