# BETO × Evo2 — Preguntas Frecuentes / FAQ

> Checklist de preguntas técnicas respondidas sobre la integración BETO-EVO2.
> Estado del sistema: **v1.1** — tres fixes de resiliencia aplicados post-publicación inicial.

---

## 1. Transporte / API

**¿Qué endpoint exacto está usando BETO para llamar a Evo2 vía NIM?**

`https://health.api.nvidia.com/v1/biology/arc/evo2-40b/generate`

Verificado con corrida real (latencia: 10,645 ms, `TRACE_VERIFIED`).

---

**¿El modelo (arc/evo2-7b o arc/evo2-40b) está parametrizado o hardcodeado?**

Parametrizado via `NIM_ENDPOINTS` — un dict con entradas para 1B, 7B, 20B y 40B. El operador declara el tamano en el intent y el sistema selecciona el endpoint correspondiente. Sin embargo, hoy NIM solo publica el endpoint 40B, por lo que todos apuntan al mismo. Cuando NIM diferencie endpoints por tamano, solo se actualiza el dict — sin cambios en el pipeline.

---

**¿La autenticación usa correctamente la variable de entorno?**

Sí. `os.environ.get("NVIDIA_API_KEY")` con fallback a parametro CLI `--hf-token`. El header enviado es:

```
Authorization: Bearer {NVIDIA_API_KEY}
```

Verificado en corrida real con clave de produccion.

---

**¿La capa de transporte está separada en funciones (headers, payload, request)?**

`headers` y `payload` son dicts separados. El payload tiene su propia funcion publica `build_nim_payload()` compartida entre `GateManager` y `Evo2Adapter`. La llamada HTTP vive en `_call_nim()`. No existe una clase `Transport` o `HttpClient` independiente — candidato para v2 si se agrega arquitectura multi-proveedor.

---

## 2. Mapeo semántico (Intent → Payload Evo2)

**¿Dónde se transforma el intent epistemológico en el payload que Evo2 recibe?**

En `build_nim_payload(critical: CriticalParameters)` — funcion publica en `evo2_adapter.py`. Recibe los parametros ya validados y aprobados por el operador y construye el JSON NIM. La misma funcion es usada por `GateManager` para el preview en Gate-C, garantizando que lo que el operador aprueba es exactamente lo que se envia.

---

**¿El payload para Evo2 es textual o estructurado?**

Estructurado. JSON con campos tipados:

```json
{
  "sequence":    "ATGGATTTATCTGC...",
  "num_tokens":  256,
  "temperature": 0.7,
  "top_k":       4,
  "top_p":       0
}
```

---

**¿BETO valida que el task corresponda al formato que Evo2 espera?**

Sí, con tres caminos declarados:
- `GENERATION` → `sequence` + `num_tokens` → NIM API ✅
- `SCORING` → `enable_sampled_probs: true` → NIM API ✅
- `EMBEDDING` → `ModelError` explícito: *"requiere instalacion local de Evo2 — NIM no expone embeddings"* ✅

---

**¿El seed, constraints y organism se integran correctamente en el prompt?**

- `seed_sequence` → campo `sequence` del payload NIM ✅
- `excluded_motifs` → filtro post-generacion via `_filter_motifs()` (NIM no acepta este parametro nativo) ✅
- `organism` y `bio_function` → van al `_beto_context` y al `epistemic_manifest` — son trazabilidad BETO, no parametros NIM ⚠️

---

## 3. Gobernanza epistemológica

**¿Dónde se aplican los "epistemic gates" antes de llamar a Evo2?**

En `GateManager`, tres gates secuenciales e irrompibles:

| Gate | Que presenta | Que bloquea |
|------|-------------|-------------|
| Gate-A | Topologia del pipeline y tipo de tarea | Rechazo del operador |
| Gate-B | Los 8 parametros con estado epistemico | Rechazo o modificacion pendiente |
| Gate-C | Payload JSON exacto con `payload_hash` | Rechazo del operador |

Sin `gate_c.approved = True`, `Evo2Adapter.execute()` lanza `RuntimeError: BETO-GAP [ESCALATED]`.

---

**¿BETO rechaza solicitudes con parámetros críticos faltantes?**

Sí. `BETOSpecEngine` detecta `NOT_STATED` en cualquiera de los 8 parametros criticos y los agrega a `blocking_gaps`. El pipeline entra en un loop interactivo hasta que el operador declara todos. `is_executable = True` solo cuando `blocking_gaps == []`.

---

**¿Se genera el manifest epistemológico antes de la llamada, después, o ambos?**

Despues de Evo2 para runs exitosos — incluye el output del modelo en el manifest. Para runs fallidos (post-fix v1.1): `persist_failed()` guarda spec y gate approvals en SQLite con `status: FAILED`, pero sin output de Evo2.

---

**¿Qué hace BETO si Evo2 devuelve algo que viola constraints?**

`excluded_motifs` → `_filter_motifs()` post-generacion → si detecta un motivo prohibido lanza `ModelError` → `BETO_GAP [ESCALATED]` al operador. Para violaciones de longitud: no aplica en la practica — NIM genera exactamente `num_tokens` tokens por diseno.

---

## 4. Trazabilidad / Logging

**¿Cada request a Evo2 queda registrado con request_id, operator_id, modelo, intent y constraints?**

Sí. SQLite con 4 tablas:

```
executions    → trace_id, timestamp, operator_id, spec_hash, task_type, status
parameters    → los 8 parametros con epistemic_state y source
gate_approvals → timestamps de aprobacion por gate con operator_id
results       → raw_output, model_used, latency_ms
```

---

**¿Se guarda el payload enviado y la respuesta cruda de Evo2?**

- Respuesta cruda: ✅ tabla `results`
- Payload enviado: ⚠️ solo el `payload_hash` en `gate_approvals`. El JSON completo del payload no se persiste — pendiente para v1.2.

---

**¿El manifest epistemológico se almacena junto con la llamada?**

Se descompone en las 4 tablas SQLite. Para obtener el manifest completo en un solo objeto: usar `--output resultado.json` al ejecutar. Una columna `manifest_json` unificada es pendiente para v1.2.

---

**¿Evo2 usa el mismo pipeline de logging que otros proveedores?**

No existe arquitectura multi-proveedor todavia. Evo2 es el unico proveedor implementado. Candidato para v2.

---

## 5. Manejo de errores y límites

**¿Qué hace BETO si Evo2 devuelve 429, 5xx o timeout?**

*(Corregido en v1.1)*

| Codigo | Clasificacion | Comportamiento |
|--------|--------------|----------------|
| 429 | `RATE_LIMITED` | Retorna mensaje con `Retry-After` en segundos. Sin reintento automatico. |
| 503/504/502 | `FAILED_REMOTE` | 1 reintento automatico. Si persiste, retorna error con trace preservado. |
| Timeout | `FAILED_REMOTE` | Igual que 5xx. |
| 4xx otros | `BETO_GAP [ESCALATED]` | Sin reintento. Operador debe revisar especificacion. |

---

**¿Existe un modo DRY_RUN?**

*(Agregado en v1.1)*

Sí. Flag `--dry-run`:

```bash
python3 main.py --intent "..." --dry-run
```

Ejecuta Fases 1 y 2 completas (BETOSpec + 3 gates), muestra el payload exacto que se enviaria a NIM y el `spec_hash`. Cero creditos NIM consumidos.

---

**¿Los errores remotos se clasifican?**

*(Mejorado en v1.1)*

Cuatro clasificaciones:
- `RATE_LIMITED` — 429, esperar `Retry-After`
- `FAILED_REMOTE` — red/timeout tras reintentos agotados
- `BETO_GAP [ESCALATED]` — error de modelo, spec requiere revision
- `TRACE_VERIFIED` — exito

---

**¿Se conserva el manifest incluso si la llamada falla?**

*(Corregido en v1.1)*

Sí. El `TRACE_ID` se genera **antes** de llamar a Evo2. Si el modelo falla por cualquier razon, `persist_failed()` guarda spec + gate approvals en SQLite con `status: FAILED`. El operador recibe su `TRACE_ID` y puede auditar sus decisiones aunque el modelo haya fallado. Esta correccion restaura la garantia central de BETO: *toda decision del operador es trazable, independientemente del resultado del modelo.*

---

## 6. Coherencia entre modelos (7B vs 40B)

**¿El modelo se selecciona por configuración o argumento CLI?**

Por declaracion del operador en el intent (`7B`, `40B`, etc.) — sin default. BETOSpec lo extrae y lo muestra en Gate-B para confirmacion explicita.

---

**¿BETO registra en el manifest qué modelo Evo2 se usó?**

Sí. Campo `model_used` en `AuthorizedEvo2Result`, en tabla `results` de SQLite, y en `epistemic_manifest`.

---

**¿Hay diferencias de longitud o formato entre 7B y 40B que BETO deba manejar?**

No manejadas activamente. El payload es identico para todos los tamanos. Si NIM diferencia comportamiento por modelo en el futuro, BETO no lo abstrae actualmente.

---

**¿El usuario puede cambiar de modelo sin romper el pipeline?**

Sí. Declara otro tamano en el intent — `NIM_ENDPOINTS` lo mapea al endpoint correspondiente. El pipeline no tiene logica especifica por tamano de modelo.

---

## 7. Arquitectura general

**¿Evo2 está implementado como un "provider" más dentro de BETO?**

No todavia. No existe interfaz `Provider` abstracta. Evo2 es el unico proveedor implementado. Una arquitectura `BETO-BioModels` con soporte para AlphaFold, ESM-3 u otros modelos biologicos requeriria un nuevo ciclo BETO completo — candidato para v2.

---

**¿La integración evita casos especiales o código duplicado?**

Sí. `build_nim_payload()` es una funcion publica compartida — usada por `GateManager` para el preview en Gate-C y por `Evo2Adapter` para la llamada real. Un solo punto de verdad para el payload, garantizando que el hash que aprueba el operador corresponde exactamente al payload enviado.

---

**¿El wrapper epistemológico funciona igual para Evo2 que para otros modelos?**

No aplica todavia — arquitectura de un solo proveedor. Diseñado para ser extensible cuando se especifique v2.

---

**¿BETO nunca permite llamadas "en crudo" a Evo2 sin pasar por gobernanza?**

Garantia absoluta. `Evo2Adapter.execute()` verifica `gate_record.is_complete()` como primera instruccion. Sin las 3 gates aprobadas lanza:

```
RuntimeError: BETO-GAP [ESCALATED]: GateApprovalRecord incompleto.
Las 3 gates deben ser aprobadas por el operador antes de ejecutar.
```

No existe ningun bypass, modo de emergencia, ni llamada directa al API sin pasar por gobernanza.

---

## Pendientes (v1.2 / v2)

| # | Item | Prioridad | Version |
|---|------|-----------|---------|
| 1 | Payload JSON completo persistido en SQLite | Baja | v1.2 |
| 2 | Endpoints diferenciados por tamano de modelo | Externa (depende de NIM) | Cuando NIM lo publique |
| 3 | Arquitectura multi-proveedor (`BETO-BioModels`) | Alta para crecimiento | v2 — nuevo ciclo BETO |

---

## Historial de versiones

| Version | Cambios |
|---------|---------|
| v1.0 | Publicacion inicial — pipeline completo, corrida real Evo2-7B, TRACE_VERIFIED |
| v1.1 | Fix 429 Rate Limit, Fix manifest en fallo (`persist_failed`), DRY_RUN mode |

---

*Preguntas adicionales: abrir un Issue o Discussion en el repositorio.*
*BETO Framework: https://github.com/aramirez-maza/beto-framework*
