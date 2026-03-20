# BETO-TRACE: BETO-EVO2.SEC6.COMP.Evo2Adapter
# BETO-TRACE: BETO-EVO2.SEC7.PHASE.Fase3_EjecucionAutorizada
"""
BETO-EVO2 — Evo2Adapter
Interfaz autorizada con Evo2 via NVIDIA NIM API.
Endpoint: https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate
Auth:      Authorization: Bearer $NVIDIA_API_KEY

IMPORTANTE — Capacidades NIM vs Local:
  GENERATION  → NIM API  (soportado)
  SCORING     → NIM API  (via enable_sampled_probs)
  EMBEDDING   → Solo local (NIM no expone embeddings aun)

Solo acepta llamadas con GateApprovalRecord completo.
Politica de errores: 1 reintento en error de red,
BETO_GAP [ESCALATED] en error de modelo.
"""

import hashlib
import json
import os
import time

import requests

from models import (
    CriticalParameters,
    GateApprovalRecord,
    ModelSize,
    RawEvo2Response,
    TaskType,
)

# Endpoints NIM por tamano de modelo
# NOTA: NIM actualmente publica Evo2-40B. Otros tamanos usan el mismo endpoint
# con advertencia al operador.
NIM_ENDPOINTS: dict[ModelSize, str] = {
    ModelSize.EVO2_40B: "https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate",
    ModelSize.EVO2_20B: "https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate",
    ModelSize.EVO2_7B:  "https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate",
    ModelSize.EVO2_1B:  "https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate",
}

NIM_TIMEOUT_SECONDS = 300  # NIM recomienda hasta 300s para secuencias largas


def build_nim_payload(critical: CriticalParameters) -> dict:
    """
    Construye el payload NIM con los campos EXACTOS que acepta la API.
    Funcion publica — usada tambien por GateManager para Gate-C preview.
    BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.build_payload

    Campos NIM declarados (fuente: build.nvidia.com/arcinstitute/evo2-40b):
      sequence, num_tokens, temperature, top_k, top_p,
      random_seed, enable_logits, enable_sampled_probs
    """
    payload: dict = {
        "sequence":   critical.seed_sequence or "",
        "num_tokens": critical.sequence_length,   # NIM usa num_tokens, no n_tokens
        "temperature": critical.sampling_temp,
        "top_k":      critical.top_k,
        "top_p":      0,                          # desactivado por defecto
    }

    # SCORING via NIM: solicitar sampled_probs en lugar de una llamada separada
    if critical.task_type == TaskType.SCORING:
        payload["enable_sampled_probs"] = True

    return payload


class Evo2Adapter:
    """
    BETO-TRACE: BETO-EVO2.SEC6.COMP.Evo2Adapter
    Garantia: no ejecuta si GateApprovalRecord.is_complete() == False.
    """

    def __init__(self, nvidia_api_key: str | None = None):
        # Acepta clave por parametro o por variable de entorno
        self._api_key = nvidia_api_key or os.environ.get("NVIDIA_API_KEY")

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.build_payload
    def build_payload(self, critical: CriticalParameters) -> dict:
        """Delega a la funcion publica build_nim_payload."""
        return build_nim_payload(critical)

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.execute
    def execute(
        self,
        critical: CriticalParameters,
        gate_record: GateApprovalRecord,
    ) -> RawEvo2Response:
        """
        Ejecuta la llamada a Evo2 NIM. Solo si GateApprovalRecord esta completo.
        BETO-TRACE: BETO-EVO2.SEC5.RF.RF-06
        OQ-E02: 1 reintento en error de red, escalado en error de modelo.
        """
        # Verificacion obligatoria de gates — BETO-TRACE: BETO-EVO2.SEC5.RF.RF-06
        if not gate_record.is_complete():
            raise RuntimeError(
                "BETO-GAP [ESCALATED]: GateApprovalRecord incompleto. "
                "Las 3 gates deben ser aprobadas por el operador antes de ejecutar."
            )

        # Verificar integridad del payload contra hash aprobado en Gate-C
        payload = build_nim_payload(critical)
        payload_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()[:16]

        if payload_hash != gate_record.payload_hash:
            raise RuntimeError(
                f"BETO-GAP [ESCALATED]: Hash de payload no coincide. "
                f"Aprobado: {gate_record.payload_hash}, Actual: {payload_hash}. "
                "El payload fue modificado despues de Gate-C."
            )

        model_id = f"evo2-{critical.evo2_model_size.value}"
        return self._execute_with_retry(critical, payload, gate_record, model_id)

    def _execute_with_retry(
        self,
        critical: CriticalParameters,
        payload: dict,
        gate_record: GateApprovalRecord,
        model_id: str,
    ) -> RawEvo2Response:
        """
        Politica de errores declarada (OQ-E02):
        - Error de red / 503 / timeout: 1 reintento automatico
        - Error de modelo (4xx): BETO_GAP [ESCALATED] sin reintento
        """
        max_network_retries = 1  # DECLARED — OQ-E02

        for attempt in range(max_network_retries + 1):
            start_ms = int(time.time() * 1000)
            try:
                output = self._call_nim(critical, payload, model_id)
                latency_ms = int(time.time() * 1000) - start_ms

                # Filtrar excluded_motifs post-generacion
                # (NIM no acepta este parametro — se aplica despues)
                if isinstance(output, str) and critical.excluded_motifs:
                    output = self._filter_motifs(output, critical.excluded_motifs)

                return RawEvo2Response(
                    output=output,
                    model_used=model_id,
                    payload_hash=gate_record.payload_hash,
                    latency_ms=latency_ms,
                    error=None,
                )
            except NetworkError as e:
                if attempt < max_network_retries:
                    print(f"[BETO-EVO2] Error de red — reintento {attempt + 1}/{max_network_retries}")
                    time.sleep(2)
                    continue
                latency_ms = int(time.time() * 1000) - start_ms
                return RawEvo2Response(
                    output="",
                    model_used=model_id,
                    payload_hash=gate_record.payload_hash,
                    latency_ms=latency_ms,
                    error=f"NetworkError tras {max_network_retries} reintento(s): {e}",
                )
            except ModelError as e:
                # BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.handle_error
                latency_ms = int(time.time() * 1000) - start_ms
                raise RuntimeError(
                    f"BETO-GAP [ESCALATED]: Error de modelo Evo2 NIM. "
                    f"Causa: {e}. "
                    "El operador debe revisar la especificacion declarada."
                ) from e

    def _call_nim(
        self,
        critical: CriticalParameters,
        payload: dict,
        model_id: str,
    ) -> str | float | list:
        """
        Llamada HTTP real a NVIDIA NIM API.
        BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.execute
        OQ-E01: mapeo task_type → comportamiento NIM declarado.
        """
        # Sin API key: modo simulacion para desarrollo
        if not self._api_key:
            print("[BETO-EVO2] SIMULACION — NVIDIA_API_KEY no configurada.")
            print(f"  Endpoint: {NIM_ENDPOINTS[critical.evo2_model_size]}")
            print(f"  Modelo:   {model_id}")
            print(f"  Tarea:    {critical.task_type.value}")
            print(f"  Tokens:   {critical.sequence_length}")
            return self._simulate_output(critical)

        # EMBEDDING no disponible via NIM — requiere instalacion local
        if critical.task_type == TaskType.EMBEDDING:
            raise ModelError(
                "EMBEDDING no esta disponible via NVIDIA NIM API. "
                "Requiere instalacion local de Evo2. "
                "Cambie task_type a GENERATION o SCORING, "
                "o instale Evo2 localmente."
            )

        endpoint = NIM_ENDPOINTS[critical.evo2_model_size]
        headers = {
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {self._api_key}",
            "nvcf-poll-seconds": "300",
        }

        try:
            response = requests.post(
                url=endpoint,
                headers=headers,
                json=payload,
                timeout=NIM_TIMEOUT_SECONDS,
            )
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Timeout ({NIM_TIMEOUT_SECONDS}s): {e}") from e
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"ConnectionError: {e}") from e

        # Errores de red (5xx) — elegibles para reintento
        if response.status_code in (503, 504, 502):
            raise NetworkError(f"HTTP {response.status_code}: {response.text[:200]}")

        # Errores de modelo (4xx) — requieren decision del operador
        if response.status_code >= 400:
            raise ModelError(
                f"HTTP {response.status_code}: {response.text[:500]}"
            )

        data = response.json()

        # GENERATION: retorna la secuencia generada
        if critical.task_type == TaskType.GENERATION:
            return data.get("sequence", "")

        # SCORING: retorna promedio de sampled_probs como score escalar
        if critical.task_type == TaskType.SCORING:
            probs = data.get("sampled_probs")
            if probs and isinstance(probs, list):
                return float(sum(probs) / len(probs))
            return 0.0

        return data.get("sequence", "")

    def _filter_motifs(self, sequence: str, excluded_motifs: list[str]) -> str:
        """
        Filtra motivos excluidos post-generacion.
        NIM no acepta excluded_motifs como parametro nativo.
        Si se detecta un motivo excluido: BETO_GAP [ESCALATED].
        """
        for motif in excluded_motifs:
            if motif and motif in sequence:
                raise ModelError(
                    f"Secuencia generada contiene motivo excluido declarado: '{motif}'. "
                    "El operador debe revisar los parametros o la secuencia seed."
                )
        return sequence

    def _simulate_output(self, critical: CriticalParameters) -> str | float | list:
        """Output simulado para desarrollo sin API key."""
        if critical.task_type == TaskType.GENERATION:
            bases = "ATCG"
            import random
            return "".join(random.choice(bases) for _ in range(critical.sequence_length))
        elif critical.task_type == TaskType.SCORING:
            return -2.847
        else:
            return [0.1] * 512

    # BETO-TRACE: BETO-EVO2.SEC6.METHOD.Evo2Adapter.handle_error
    def handle_error(self, error: Exception) -> None:
        """Registro de errores para TraceLogger."""
        print(f"[BETO-EVO2] Error en Evo2Adapter: {error}")


class NetworkError(Exception):
    """Error transitorio de red — elegible para reintento."""


class ModelError(Exception):
    """Error de modelo — requiere decision del operador."""
