# MODEL_CALL_PLAN
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS -->

---

## Propósito

Define, governa y loguea cada llamada al modelo de lenguaje dentro del executor BETO. Toda llamada al modelo debe estar gobernada por un MODEL_CALL_PLAN. El plan debe ejecutarse, no solo documentarse. Queda logueado para auditoría.

---

## Formato (híbrido JSON+Markdown)

### Cabecera (campos obligatorios — JSON)

```json
{
  "call_id": "MCP-{{YYYY-NNNN}}",
  "timestamp": "{{ISO_8601}}",
  "cycle_id": "{{ciclo_id}}",
  "unit_id": "{{unit_id | null}}",
  "route_type": "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}",
  "executor_type": "{{nombre_del_subejecutor_que_llama}}",
  "purpose": "{{propósito declarado de la llamada — una oración}}",
  "input_artifacts": [
    {"artifact": "{{nombre}}", "trace_id": "{{id}}", "role": "{{context|template|source}}"}
  ],
  "context_layers_used": {
    "layer_a": true,
    "layer_b": {{true|false}},
    "layer_b_scope": "{{minimal|full|unit_only}}",
    "layer_c": true,
    "layer_c_snapshot_id": "{{LC-id}}"
  },
  "snapshot_set_used": ["{{CS-id}}", "{{AQ-id}}", "{{LC-id}}", "{{MS-id}}"],
  "expected_output": "{{descripción del output esperado}}",
  "expected_output_artifact": "{{nombre del artefacto esperado}}",
  "model_class": "{{reasoning|coding|fast|local}}",
  "cache_eligibility": {
    "prefix_cacheable": {{true|false}},
    "semantic_cacheable": {{true|false}},
    "operational_cacheable": {{true|false}},
    "cache_key": "{{clave de cache si aplica | null}}"
  },
  "trace_anchor": "{{BETO_V44.SEC<N>.<TIPO>.<ELEMENTO>}}",
  "escalation_policy": "{{HALT_ON_BETO_GAP | CONTINUE_WITH_LOG | PROMOTE_ROUTE}}",
  "fallback_strategy": "{{descripción del fallback si la llamada falla o el output no satisface}}",
  "estimated_context_tokens": {{int | null}},
  "call_status": "{{PLANNED | EXECUTING | COMPLETED | FAILED}}"
}
```

### Cuerpo descriptivo (corto — Markdown)

```markdown
## Descripción de la llamada

**¿Qué debe hacer el modelo en esta llamada?**
{{descripción del subproblema específico — sin inferencias, sin expansión de scope}}

**¿Por qué se necesita esta llamada ahora?**
{{justificación en el contexto del paso BETO actual}}

**¿Qué contexto global se está excluyendo deliberadamente y por qué?**
{{lista de contexto excluido — esto confirma que se aplica la regla de contexto mínimo}}

## Criterios de aceptación del output

{{lista de condiciones que debe cumplir el output para ser aceptado como válido}}

## Si el output no satisface los criterios

{{qué debe hacer el executor: re-llamar, registrar BETO_GAP, promover ruta, haltar}}
```

---

## Registro de llamadas del ciclo

<!-- Las llamadas completadas se registran en esta tabla para auditoría -->

| call_id | timestamp | route_type | executor_type | purpose | call_status |
|---------|-----------|-----------|--------------|---------|------------|
| (vacío — sin llamadas en este template) | | | | | |

---

## Política de cache por tipo de llamada

### PREFIX_CACHE
Aplica a: instructivo completo, reglas nucleares BETO, templates invariantes, prefijos estables del sistema.
Estrategia: Estas piezas son el prefijo fijo que todos los contextos comparten. Se pueden colocar al inicio del contexto para aprovechar prefix caching del proveedor.

### SEMANTIC_CACHE
Aplica a: BETO_CORE cerrado (SUCCESS_CLOSED), BETO_SYSTEM_GRAPH validado, manifests cerrados, contracts cerrados.
Estrategia: Una vez que un artefacto semántico está cerrado, su contenido es inmutable para el ciclo activo y puede cachearse como bloque reutilizable.

### OPERATIONAL_CACHE
Aplica a: Snapshots activos y válidos, últimos diffs, scope de materialización actual, outputs recientes, decisiones de ruta recientes.
Estrategia: Se invalida cuando el estado operativo cambia (ver reglas de invalidación de cada snapshot).

**Regla:** La caché no puede reemplazar autoridad semántica. Solo acelera reutilización de contexto ya autorizado.

---

## Instrucciones de uso

1. Crear MODEL_CALL_PLAN antes de cada llamada al modelo
2. Completar todos los campos de la cabecera JSON
3. Verificar que todos los snapshots en `snapshot_set_used` estén en estado VALID
4. Ejecutar la llamada
5. Actualizar `call_status` a COMPLETED o FAILED
6. Registrar en la tabla de auditoría del ciclo
7. Si FAILED: ejecutar `fallback_strategy` declarada

---

## Compatibilidad

- Compatible con cualquier proveedor de modelo (agnóstico de proveedor)
- Compatible con modelos locales y API remota
- El field `model_class` es descriptivo — no está atado a un proveedor específico
