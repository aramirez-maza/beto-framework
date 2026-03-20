# BETO-TRACE: BETO-EVO2.SEC6.COMP.GateManager
# BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase2_GobiernodeGates
"""
BETO-EVO2 — GateManager
Orquesta las 3 gates de gobernanza antes de cada llamada a Evo2.
Ningun gate puede ser saltado. El operador tiene veto absoluto en cada uno.
"""

import hashlib
import json
from datetime import datetime, timezone

from evo2_adapter import build_nim_payload
from models import (
    CriticalParameters,
    EpistemicState,
    GateApprovalRecord,
    GateRecord,
    ParameterMap,
    TaskType,
)


class GateManager:
    """
    BETO-TRACE: BETO-EVO2.SEC6.COMP.GateManager
    Garantia: sin GateApprovalRecord.is_complete() == True,
              Evo2Adapter no puede recibir parametros.
    """

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.GateManager.present_gate_a
    def present_gate_a(
        self,
        param_map: ParameterMap,
        operator_id: str,
    ) -> tuple[GateApprovalRecord, bool]:
        """
        Gate-A: presenta topologia del sistema y tipo de tarea.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-03
        """
        record = GateApprovalRecord()

        print(self._format_gate_a(param_map))
        decision = input("Gate-A — Aprobar topologia? [s/n]: ").strip().lower()
        approved = decision in ("s", "si", "yes", "y")

        record.gate_a = GateRecord(
            approved=approved,
            timestamp=self._now(),
            operator_id=operator_id,
            notes=f"decision={decision}",
        )

        return record, approved

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.GateManager.present_gate_b
    def present_gate_b(
        self,
        param_map: ParameterMap,
        record: GateApprovalRecord,
        operator_id: str,
    ) -> tuple[GateApprovalRecord, bool, CriticalParameters | None]:
        """
        Gate-B: presenta todos los parametros declarados para revision.
        Permite modificaciones — si modifica, BETOSpec re-valida externamente.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-04
        OQ-G02: modificacion permitida, Gate-B se re-presenta.
        """
        print(self._format_gate_b(param_map))
        decision = input(
            "Gate-B — Aprobar especificacion? [s/n/m (modificar)]: "
        ).strip().lower()

        if decision in ("m", "modificar", "modify"):
            record.modifications.append(f"Modificacion solicitada en {self._now()}")
            return record, False, None  # caller debe re-validar con BETOSpec

        approved = decision in ("s", "si", "yes", "y")

        record.gate_b = GateRecord(
            approved=approved,
            timestamp=self._now(),
            operator_id=operator_id,
            notes=f"decision={decision}",
        )

        if not approved:
            return record, False, None

        critical = self._build_critical_params(param_map)
        return record, True, critical

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.GateManager.present_gate_c
    def present_gate_c(
        self,
        critical: CriticalParameters,
        record: GateApprovalRecord,
        operator_id: str,
    ) -> tuple[GateApprovalRecord, bool]:
        """
        Gate-C: presenta el payload exacto que se enviara a Evo2.
        El operador ve exactamente lo que el modelo recibira.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-05
        """
        # Hash calculado SOLO sobre el payload NIM real (sin _beto_context)
        # para que coincida con la verificacion en Evo2Adapter
        nim_payload = build_nim_payload(critical)
        payload_hash = hashlib.sha256(
            json.dumps(nim_payload, sort_keys=True).encode()
        ).hexdigest()[:16]
        # Preview completo (con contexto BETO) solo para visualizacion del operador
        payload = self._build_payload_preview(critical)

        record.payload_hash = payload_hash
        print(self._format_gate_c(payload, payload_hash))

        decision = input("Gate-C — Autorizar llamada a Evo2? [s/n]: ").strip().lower()
        approved = decision in ("s", "si", "yes", "y")

        record.gate_c = GateRecord(
            approved=approved,
            timestamp=self._now(),
            operator_id=operator_id,
            notes=f"payload_hash={payload_hash}",
        )

        return record, approved

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.GateManager.record_approval
    def record_approval(self, record: GateApprovalRecord) -> dict:
        """Serializa GateApprovalRecord para audit trail."""
        return {
            "gate_a": self._gate_to_dict(record.gate_a),
            "gate_b": self._gate_to_dict(record.gate_b),
            "gate_c": self._gate_to_dict(record.gate_c),
            "payload_hash": record.payload_hash,
            "modifications": record.modifications,
            "is_complete": record.is_complete(),
        }

    def _build_critical_params(self, param_map: ParameterMap) -> CriticalParameters:
        """
        Construye CriticalParameters solo si todos estan DECLARED.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-09
        """
        if not param_map.is_executable:
            raise RuntimeError(
                "BETO-GAP [ESCALATED]: ParameterMap no es ejecutable. "
                f"Parametros bloqueantes: {param_map.blocking_gaps}"
            )

        p = param_map.parameters
        return CriticalParameters(
            organism=p["organism"].value,
            bio_function=p["bio_function"].value,
            sequence_length=p["sequence_length"].value,
            biosafety_level=p["biosafety_level"].value,
            evo2_model_size=p["evo2_model_size"].value,
            sampling_temp=p["sampling_temp"].value,
            top_k=p["top_k"].value,
            excluded_motifs=p["excluded_motifs"].value,
            task_type=param_map.task_type,
            seed_sequence=param_map.seed_sequence,
        )

    def _build_payload_preview(self, critical: CriticalParameters) -> dict:
        """
        Payload exacto que se enviara a NIM API.
        Usa build_nim_payload para garantizar coherencia con Evo2Adapter.
        Los campos de gobernanza (organism, biosafety_level, etc.) son
        BETO-declarados pero no se envian a NIM — son del epistemic_manifest.
        """
        nim = build_nim_payload(critical)
        # Agregar contexto de gobernanza solo para visualizacion en Gate-C
        preview = dict(nim)
        preview["_beto_context"] = {
            "model":           f"evo2-{critical.evo2_model_size.value}",
            "task_type":       critical.task_type.value,
            "organism":        critical.organism,
            "bio_function":    critical.bio_function,
            "biosafety_level": critical.biosafety_level.value,
            "excluded_motifs": critical.excluded_motifs,
            "nota":            "Los campos _beto_context NO se envian a NIM. Son trazabilidad BETO.",
        }
        return preview

    def _format_gate_a(self, param_map: ParameterMap) -> str:
        return (
            "\n"
            "╔══════════════════════════════════════════════╗\n"
            "║  BETO-EVO2 — GATE A: TOPOLOGIA DEL SISTEMA  ║\n"
            "╚══════════════════════════════════════════════╝\n"
            "\n"
            f"  Tarea:     {param_map.task_type.value if param_map.task_type else 'NOT_STATED'}\n"
            f"  Operador:  {param_map.operator_id}\n"
            "\n"
            "  Pipeline declarado:\n"
            "    BETOSpec Engine\n"
            "      → GateManager\n"
            "        → Evo2Adapter\n"
            "          → TraceLogger\n"
            "\n"
            "  Modelo Evo2 seleccionado por operador (no inferido).\n"
            "  Acceso via Hugging Face API (declarado OQ-05).\n"
        )

    def _format_gate_b(self, param_map: ParameterMap) -> str:
        lines = [
            "",
            "╔══════════════════════════════════════════════╗",
            "║  BETO-EVO2 — GATE B: ESPECIFICACION         ║",
            "╚══════════════════════════════════════════════╝",
            "",
            "  Parametros declarados (todos deben ser DECLARED):",
            "",
        ]
        for name, entry in param_map.parameters.items():
            state_icon = "✓" if entry.epistemic_state == EpistemicState.DECLARED else "✗"
            lines.append(
                f"  {state_icon} {name:<20} = {entry.value!r:<30} [{entry.epistemic_state.value}]"
            )
        lines += [
            "",
            f"  Secuencia seed: {param_map.seed_sequence or '(ninguna)'}",
            "",
            "  Puede escribir 'm' para modificar parametros.",
        ]
        return "\n".join(lines)

    def _format_gate_c(self, payload: dict, payload_hash: str) -> str:
        payload_str = json.dumps(payload, indent=4, ensure_ascii=False)
        return (
            "\n"
            "╔══════════════════════════════════════════════╗\n"
            "║  BETO-EVO2 — GATE C: PAYLOAD EXACTO EVO2   ║\n"
            "╚══════════════════════════════════════════════╝\n"
            "\n"
            "  Esta es la llamada exacta que se enviara a Evo2 API:\n"
            "\n"
            f"{payload_str}\n"
            "\n"
            f"  payload_hash: {payload_hash}\n"
            "\n"
            "  Ningun parametro sera modificado despues de esta aprobacion.\n"
        )

    def _gate_to_dict(self, gate: GateRecord | None) -> dict | None:
        if gate is None:
            return None
        return {
            "approved":    gate.approved,
            "timestamp":   gate.timestamp,
            "operator_id": gate.operator_id,
            "notes":       gate.notes,
        }

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
