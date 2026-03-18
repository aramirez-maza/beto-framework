# CYCLE_CONTEXT_SNAPSHOT
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT -->

---

## Propósito

Captura persistente del estado del ciclo BETO en un momento específico, para ser reutilizada en llamadas posteriores sin necesidad de reconstruir el contexto global. Un snapshot es una fuente operativa de contexto — no es autoridad semántica. La autoridad semántica sigue residiendo en BETO_CORE, graph, manifests y contracts.

---

## Formato de snapshot (híbrido JSON+Markdown)

### Cabecera (metadata estructurada — JSON)

```json
{
  "snapshot_id": "CS-{{YYYY-NNNN}}",
  "snapshot_type": "CYCLE_CONTEXT_SNAPSHOT",
  "cycle_id": "{{ciclo_id}}",
  "unit_id": "{{unit_id | null}}",
  "timestamp": "{{ISO_8601}}",
  "validity_state": "VALID | INVALIDATED",
  "invalidation_reason": "{{razón si INVALIDATED | null}}",
  "route_type": "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}",
  "version": "{{versión del framework: 4.4.0}}",
  "source_artifacts": [
    {"artifact": "{{nombre}}", "trace_id": "{{id}}", "version": "{{v}}"}
  ],
  "trace_references": ["{{BETO_V44.SEC<N>.<TIPO>.<ELEMENTO>}}"],
  "promotion_state": "{{NONE | PROMOTED_TO_PARTIAL | PROMOTED_TO_FULL}}",
  "snapshot_dependencies": ["{{CS-id del que depende si aplica}}"]
}
```

### Cuerpo (contenido interpretativo — Markdown)

```markdown
## BETO_CORE activo

**Sistema:** {{system_name}}
**Versión:** {{version}}
**Paso actual:** {{paso_actual}} de 11
**Estado del ciclo:** {{ACTIVO | GATE_PENDIENTE | MATERIALIZACIÓN}}

## Intención del sistema (extracto)

{{extracto de Section 1 del BETO_CORE — máximo 3 líneas}}

## Boundaries activos (resumen)

**In scope (key items):**
{{lista de los 3-5 items más relevantes del scope activo}}

**Out of scope (restricciones críticas):**
{{lista de las 2-3 restricciones más importantes}}

## OQs activas en este tramo

{{ver ACTIVE_OQ_SET asociado — referencia por snapshot_id}}

## Decisiones técnicas estables relevantes

{{lista de las decisiones técnicas que impactan el tramo actual}}

## Path de ejecución seleccionado

- Ruta: {{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}
- Decisión de routing: {{RD-id}}
- Última promoción: {{RP-id | NINGUNA}}

## Última acción materializada

{{descripción del último artefacto generado o acción completada}}
```

---

## Reglas de invalidación

Un snapshot debe invalidarse (cambiar `validity_state` a `INVALIDATED`) si cambia cualquiera de estos elementos:

1. El BETO_CORE autorizado del ciclo activo
2. Una OQ activa contenida en el snapshot
3. La phase o contract asociado
4. Una unidad estructural relevante
5. Un artefacto fuente declarado como autoridad en `source_artifacts`
6. El `route_type` del tramo actual (por promoción)
7. El `promotion_state` de la ruta

**Un snapshot invalidado no puede usarse para resolver subproblemas — debe regenerarse.**

---

## Instrucciones de uso

1. Crear un CYCLE_CONTEXT_SNAPSHOT al inicio de cada tramo de ejecución
2. Incluir el snapshot_id en el MODEL_CALL_PLAN correspondiente
3. Verificar validity_state antes de usar un snapshot existente
4. Si el snapshot está INVALIDADO: regenerar antes de continuar
5. Almacenar en `.beto/snapshots/` con nombre `{{snapshot_id}}.md`

---

## Relación con otros artefactos

- OQs activas en el tramo: ver ACTIVE_OQ_SET
- Plan de la llamada: ver MODEL_CALL_PLAN
- Decisión de routing aplicada: ver ROUTING_DECISION_RECORD
- Scope de materialización: ver MATERIALIZATION_SCOPE
