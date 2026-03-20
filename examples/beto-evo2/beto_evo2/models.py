# BETO-TRACE: BETO-EVO2.SEC4.MODEL.GenomicRequest
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.ParameterMap
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.CriticalParameters
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.GateApprovalRecord
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.RawEvo2Response
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.AuthorizedEvo2Result
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.ParameterEntry
"""
BETO-EVO2 — Data Models
Todos los tipos compartidos entre componentes del pipeline.
Propietario: models.py (fuente unica de verdad para tipos)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# BETO-TRACE: BETO-EVO2.SEC4.FIELD.biosafety_level
class BiosafetylLevel(str, Enum):
    BSL1 = "BSL-1"
    BSL2 = "BSL-2"
    BSL3 = "BSL-3"
    BSL4 = "BSL-4"


# BETO-TRACE: BETO-EVO2.SEC5.RF.RF-01
class TaskType(str, Enum):
    GENERATION = "GENERATION"
    SCORING    = "SCORING"
    EMBEDDING  = "EMBEDDING"


class ModelSize(str, Enum):
    EVO2_1B  = "1B"
    EVO2_7B  = "7B"
    EVO2_20B = "20B"
    EVO2_40B = "40B"


class EpistemicState(str, Enum):
    DECLARED   = "DECLARED"
    NOT_STATED = "NOT_STATED"
    INFERRED   = "INFERRED"


class TraceStatus(str, Enum):
    TRACE_VERIFIED = "TRACE_VERIFIED"
    PENDING        = "PENDING"
    FAILED         = "FAILED"


# ---------------------------------------------------------------------------
# BETO-TRACE: BETO-EVO2.SEC4.MODEL.GenomicRequest
@dataclass
class GenomicRequest:
    """
    Entrada al sistema desde el operador.
    Ningun campo es completado por inferencia.
    """
    raw_intent:    str
    task_type:     TaskType
    operator_id:   str
    seed_sequence: str | None = None


# BETO-TRACE: BETO-EVO2.SEC4.MODEL.ParameterEntry
@dataclass
class ParameterEntry:
    """Un parametro con su estado epistemico y fuente."""
    value:           Any
    epistemic_state: EpistemicState
    source:          str  # "operator_input" | "BETO_ASSISTED" | "NOT_STATED"


# BETO-TRACE: BETO-EVO2.SEC4.MODEL.ParameterMap
@dataclass
class ParameterMap:
    """
    Resultado de BETOSpecEngine.
    is_executable = True solo si blocking_gaps esta vacio.
    """
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.organism
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.bio_function
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.sequence_length
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.biosafety_level
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.evo2_model_size
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.sampling_temp
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.top_k
    # BETO-TRACE: BETO-EVO2.SEC4.FIELD.excluded_motifs
    parameters:    dict[str, ParameterEntry] = field(default_factory=dict)
    blocking_gaps: list[str]                 = field(default_factory=list)
    is_executable: bool                      = False
    task_type:     TaskType | None           = None
    seed_sequence: str | None               = None
    operator_id:   str                      = ""

    # Los 8 parametros criticos declarados — BETO-TRACE: BETO-EVO2.SEC5.RF.RF-02
    CRITICAL_PARAMS: list[str] = field(default_factory=lambda: [
        "organism",
        "bio_function",
        "sequence_length",
        "biosafety_level",
        "evo2_model_size",
        "sampling_temp",
        "top_k",
        "excluded_motifs",
    ])


# BETO-TRACE: BETO-EVO2.SEC4.MODEL.CriticalParameters
@dataclass
class CriticalParameters:
    """
    Todos los parametros DECLARED, listos para Evo2Adapter.
    Solo se construye si ParameterMap.is_executable == True
    y GateApprovalRecord.gate_b esta aprobado.
    """
    organism:        str
    bio_function:    str
    sequence_length: int
    biosafety_level: BiosafetylLevel
    evo2_model_size: ModelSize
    sampling_temp:   float
    top_k:           int
    excluded_motifs: list[str]
    task_type:       TaskType
    seed_sequence:   str | None = None


# BETO-TRACE: BETO-EVO2.SEC4.MODEL.GateApprovalRecord
@dataclass
class GateRecord:
    approved:     bool
    timestamp:    str
    operator_id:  str
    notes:        str = ""


@dataclass
class GateApprovalRecord:
    """
    Registro de aprobaciones del operador en las 3 gates.
    Requerido por Evo2Adapter y TraceLogger.
    """
    gate_a:       GateRecord | None = None  # topologia
    gate_b:       GateRecord | None = None  # especificacion
    gate_c:       GateRecord | None = None  # payload exacto
    payload_hash: str               = ""
    modifications: list[str]        = field(default_factory=list)

    def is_complete(self) -> bool:
        # BETO-TRACE: BETO-EVO2.SEC5.RF.RF-06
        return (
            self.gate_a is not None and self.gate_a.approved and
            self.gate_b is not None and self.gate_b.approved and
            self.gate_c is not None and self.gate_c.approved
        )


# BETO-TRACE: BETO-EVO2.SEC4.MODEL.RawEvo2Response
@dataclass
class RawEvo2Response:
    """Respuesta cruda de Evo2 API antes de auditoria."""
    output:       str | float | list
    model_used:   str
    payload_hash: str
    latency_ms:   int
    error:        str | None = None


# BETO-TRACE: BETO-EVO2.SEC4.MODEL.AuthorizedEvo2Result
@dataclass
class AuthorizedEvo2Result:
    """
    Resultado final del pipeline. Solo se emite con TRACE_VERIFIED.
    BETO-TRACE: BETO-EVO2.SEC4.FIELD.trace_id
    BETO-TRACE: BETO-EVO2.SEC4.FIELD.spec_hash
    BETO-TRACE: BETO-EVO2.SEC4.FIELD.epistemic_manifest
    """
    trace_id:           str
    evo2_output:        str | float | list
    spec_hash:          str
    gate_approvals:     dict
    epistemic_manifest: dict
    trace_status:       TraceStatus = TraceStatus.TRACE_VERIFIED
    model_used:         str         = ""
    latency_ms:         int         = 0
