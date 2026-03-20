# BETO-TRACE: BETO-EVO2.SEC6.COMP.BETOSpecEngine
# BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase1_EspecificacionEpistemica
"""
BETO-EVO2 — BETOSpec Engine
Parsea GenomicRequest y clasifica epistemicamente los 8 parametros criticos.
Ningun parametro critico puede ser INFERRED. NOT_STATED bloquea el pipeline.
"""

import json
import re
from typing import Any

from models import (
    BiosafetylLevel,
    EpistemicState,
    GenomicRequest,
    ModelSize,
    ParameterEntry,
    ParameterMap,
    TaskType,
)


class BETOSpecEngine:
    """
    BETO-TRACE: BETO-EVO2.SEC6.COMP.BETOSpecEngine
    Responsabilidad: clasificacion epistemica de parametros genomicos.
    Garantia: cero inferencias silenciosas sobre parametros criticos.
    """

    # BETO-TRACE: BETO-EVO2.SEC5.RF.RF-01
    CRITICAL_PARAMS: list[str] = [
        "organism",
        "bio_function",
        "sequence_length",
        "biosafety_level",
        "evo2_model_size",
        "sampling_temp",
        "top_k",
        "excluded_motifs",
    ]

    # Patrones de extraccion declarados — OQ-B01 DECLARED [BETO_ASSISTED]
    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.BETOSpecEngine.parse
    _PATTERNS: dict[str, list[str]] = {
        "organism": [
            r"organism[:\s]+([A-Za-z\s]+)",
            r"in\s+([A-Za-z\s]+)\s+cells?",
            r"([Hh]uman|[Mm]ouse|[Ee]coli|[Ss]accharomyces|[Aa]rabidopsis)",
        ],
        "bio_function": [
            r"function[:\s]+(.+?)(?:\.|,|$)",
            r"modulate[s]?\s+(.+?)(?:\.|,|$)",
            r"express(?:ion)?\s+of\s+(.+?)(?:\.|,|$)",
            r"target[:\s]+([A-Z0-9]+)",
        ],
        "sequence_length": [
            r"(\d+)\s*(?:bp|base\s*pairs?|nucleotides?)",
            r"length[:\s]+(\d+)",
        ],
        "biosafety_level": [
            r"BSL-?([1-4])",
            r"biosafety\s+level\s+([1-4])",
        ],
        "evo2_model_size": [
            r"evo2[-_\s]*(1B|7B|20B|40B)",
            r"model[:\s]*(1B|7B|20B|40B)",
            r"\b(1B|7B|20B|40B)\b",
        ],
        "sampling_temp": [
            r"temp(?:erature)?[:\s]+([\d.]+)",
            r"temperature[:\s]+([\d.]+)",
        ],
        "top_k": [
            r"top[_\s-]?k[:\s]+(\d+)",
            r"\bk[:\s]+(\d+)",
        ],
        "excluded_motifs": [
            r"exclude[d]?\s+motifs?[:\s]+\[([^\]]+)\]",
            r"forbidden[:\s]+\[([^\]]+)\]",
            r"excluded_motifs[:\s]+\[([^\]]+)\]",
            r"excluded_motifs[:\s]+\[\]",  # lista vacia declarada explicitamente
        ],
    }

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.BETOSpecEngine.parse
    def parse(self, request: GenomicRequest) -> ParameterMap:
        """
        Punto de entrada principal.
        Extrae parametros de raw_intent y los clasifica epistemicamente.
        """
        raw = request.raw_intent
        extracted = self._extract_from_text(raw)
        param_map = self._classify(extracted, request)
        return param_map

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.BETOSpecEngine.classify
    def _extract_from_text(self, raw_intent: str) -> dict[str, Any]:
        """
        Extraccion via patrones regex declarados.
        OQ-B01: extraccion estructurada con validacion contra 8 campos.
        """
        extracted: dict[str, Any] = {}

        for param, patterns in self._PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, raw_intent, re.IGNORECASE)
                if match:
                    raw_value = match.group(1) if match.lastindex else ""
                    parsed = self._parse_value(param, raw_value.strip(), raw_intent)
                    if parsed is not None:
                        extracted[param] = parsed
                        break

        return extracted

    def _parse_value(self, param: str, raw_value: str, full_text: str) -> Any:
        """Convierte el valor extraido al tipo declarado."""
        try:
            if param == "sequence_length":
                return int(raw_value)
            if param == "sampling_temp":
                return float(raw_value)
            if param == "top_k":
                return int(raw_value)
            if param == "biosafety_level":
                return BiosafetylLevel(f"BSL-{raw_value}")
            if param == "evo2_model_size":
                return ModelSize(raw_value.upper())
            if param == "excluded_motifs":
                # Lista vacia declarada explicitamente
                if "[]" in full_text and "excluded" in full_text.lower():
                    return []
                # Lista con elementos
                items = [m.strip().strip("'\"") for m in raw_value.split(",")]
                return [i for i in items if i]
            return raw_value
        except (ValueError, KeyError):
            return None

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.BETOSpecEngine.classify
    def _classify(self, extracted: dict[str, Any], request: GenomicRequest) -> ParameterMap:
        """
        Asigna estado epistemico a cada parametro critico.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-02
        """
        parameters: dict[str, ParameterEntry] = {}
        blocking_gaps: list[str] = []

        for param in self.CRITICAL_PARAMS:
            if param in extracted and extracted[param] is not None:
                parameters[param] = ParameterEntry(
                    value=extracted[param],
                    epistemic_state=EpistemicState.DECLARED,
                    source="operator_input",
                )
            else:
                # NOT_STATED — bloquea ejecucion
                # BETO-TRACE: BETO-EVO2.SEC5.RF.RF-02
                parameters[param] = ParameterEntry(
                    value=None,
                    epistemic_state=EpistemicState.NOT_STATED,
                    source="NOT_STATED",
                )
                blocking_gaps.append(param)

        is_executable = len(blocking_gaps) == 0

        return ParameterMap(
            parameters=parameters,
            blocking_gaps=blocking_gaps,
            is_executable=is_executable,
            task_type=request.task_type,
            seed_sequence=request.seed_sequence,
            operator_id=request.operator_id,
        )

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.BETOSpecEngine.detect_gaps
    def detect_gaps(self, param_map: ParameterMap) -> list[str]:
        """Retorna lista de parametros bloqueantes NOT_STATED."""
        return param_map.blocking_gaps

    def apply_operator_declaration(
        self,
        param_map: ParameterMap,
        param_name: str,
        value: Any,
    ) -> ParameterMap:
        """
        Permite al operador declarar un parametro NOT_STATED.
        Re-evalua is_executable despues de cada declaracion.
        OQ-G02: modificacion en Gate-B — BETOSpec re-valida.
        """
        # BETO-TRACE: BETO-EVO2.SEC5.RF.RF-09
        if param_name not in self.CRITICAL_PARAMS:
            raise ValueError(f"Parametro no reconocido: {param_name}")

        parsed = self._parse_value(param_name, str(value), str(value))
        if parsed is None:
            raise ValueError(f"Valor invalido para {param_name}: {value}")

        param_map.parameters[param_name] = ParameterEntry(
            value=parsed,
            epistemic_state=EpistemicState.DECLARED,
            source="operator_input",
        )

        if param_name in param_map.blocking_gaps:
            param_map.blocking_gaps.remove(param_name)

        param_map.is_executable = len(param_map.blocking_gaps) == 0
        return param_map

    def format_gap_report(self, param_map: ParameterMap) -> str:
        """
        Presenta al operador los parametros bloqueantes de forma clara.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-02
        """
        if param_map.is_executable:
            return "Todos los parametros criticos estan DECLARED. Pipeline desbloqueado."

        lines = [
            "",
            "BETO-EVO2 — PARAMETROS BLOQUEANTES (NOT_STATED)",
            "=" * 52,
            "Los siguientes parametros son criticos y no han sido declarados.",
            "Debe declararlos antes de continuar. No se infieren.",
            "",
        ]
        descriptions = {
            "organism":        "Organismo objetivo (ej. Homo sapiens, E. coli K12)",
            "bio_function":    "Funcion biologica objetivo (ej. 'modular expresion de BRCA1')",
            "sequence_length": "Longitud en pares de bases (ej. 512)",
            "biosafety_level": "Nivel de bioseguridad: BSL-1 | BSL-2 | BSL-3 | BSL-4",
            "evo2_model_size": "Tamano del modelo Evo2: 1B | 7B | 20B | 40B",
            "sampling_temp":   "Temperatura de sampling (ej. 0.7)",
            "top_k":           "Top-K de sampling (ej. 4)",
            "excluded_motifs": "Motivos excluidos. Si ninguno: [] (lista vacia declarada)",
        }
        for gap in param_map.blocking_gaps:
            lines.append(f"  [{gap}]")
            lines.append(f"    {descriptions.get(gap, 'Declarar valor.')}")
            lines.append("")

        return "\n".join(lines)
