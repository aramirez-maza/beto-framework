# LOCAL_EXECUTION_CONTEXT
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT -->

---

## Propósito

Captura del contexto puntual de un subproblema específico. Es la Capa C del sistema de contexto estratificado. Contiene solo lo necesario para resolver el subproblema local sin cargar el contexto global del ciclo. Toda llamada al modelo debe incluir LOCAL_EXECUTION_CONTEXT como mínimo.

---

## Definición de capas de contexto (referencia)

| Capa | Nombre | Contenido | Requerida en |
|------|--------|-----------|-------------|
| A | STABLE_CORE_CONTEXT | Versión del instructivo, reglas nucleares BETO, reglas OSC, templates invariantes, contratos base | Todas las llamadas |
| B | CYCLE_CONTEXT | IDEA_RAW o artefacto raíz, BETO_CORE vigente, paso actual, OQs activas, estado del ciclo | PARTIAL y FULL |
| C | LOCAL_EXECUTION_CONTEXT | Este documento — archivo actual, diff, template, phase, contract, OQ, trace registry local, scope de materialización local | Todas las llamadas |

---

## Formato (híbrido JSON+Markdown)

### Cabecera (metadata — JSON)

```json
{
  "snapshot_id": "LC-{{YYYY-NNNN}}",
  "snapshot_type": "LOCAL_EXECUTION_CONTEXT",
  "cycle_id": "{{ciclo_id}}",
  "unit_id": "{{unit_id | null}}",
  "timestamp": "{{ISO_8601}}",
  "validity_state": "VALID | INVALIDATED",
  "route_type": "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}",
  "version": "{{4.4.0}}",
  "step_context": "{{paso_beto_actual}}",
  "executor_type": "{{nombre_del_subejecutor}}",
  "source_artifacts": ["{{artefacto fuente relevante}}"],
  "trace_references": ["{{ids BETO}}"],
  "snapshot_dependencies": ["{{CS-id o AQ-id que aplica}}"]
}
```

### Cuerpo (contexto local — Markdown)

```markdown
## Subproblema actual

**Descripción:** {{descripción del subproblema puntual}}
**Objetivo:** {{qué debe producir el subejecutor}}

## Archivo actual (si aplica)

**Archivo:** {{path del archivo que se está procesando}}
**Diff relevante:** {{diff compacto si aplica — omitir si no hay cambios}}

## Template en uso (si aplica)

**Template:** {{nombre del template activo}}
**Sección relevante:** {{sección o campo específico del template}}

## Phase en curso (si aplica)

**Phase:** {{número y nombre de la phase}}
**Input declarado:** {{input del contract de phase}}
**Output esperado:** {{output del contract de phase}}

## Contract en uso (si aplica)

**Contract:** {{nombre del implementation contract}}
**Campos relevantes:** {{campos del contract aplicables al subproblema}}

## OQ relevante (si aplica)

**OQ:** {{ID y texto de la OQ que se está trabajando}}
**Estado actual:** {{estado de ejecutabilidad}}

## Trace Registry local

| ID | Elemento | Tipo |
|----|---------|------|
| {{BETO_X.SEC<N>.<TIPO>.<ELEMENTO>}} | {{descripción}} | {{tipo}} |

## Scope de materialización local

**Artefacto a generar:** {{nombre del artefacto}}
**Tipo de operación:** {{CREAR | ACTUALIZAR | VERIFICAR}}
**Dependencias locales:** {{lista de dependencias para esta operación puntual}}
```

---

## Reglas de invalidación

El LOCAL_EXECUTION_CONTEXT debe invalidarse si:
1. El artefacto fuente del subproblema cambió
2. La OQ activa contenida en el contexto cambió de estado
3. La phase o contract asociado fue modificado
4. El route_type cambió por promoción
5. El snapshot del que depende fue invalidado

---

## Regla de contexto mínimo (BETO v4.4)

Toda llamada al modelo debe incluir exclusivamente:

```
STABLE_CORE_CONTEXT (Capa A)
+
CYCLE_CONTEXT mínimo requerido (Capa B — solo si route_type ≠ LIGHT)
+
LOCAL_EXECUTION_CONTEXT específico del subproblema (Capa C — siempre)
```

No se permite enviar contexto global completo si el subproblema puede resolverse localmente sin pérdida de autoridad semántica.

---

## Instrucciones de uso

1. Crear un LOCAL_EXECUTION_CONTEXT para cada subproblema antes de invocar al modelo
2. Incluir SOLO el contenido relevante para el subproblema — omitir secciones que no aplican
3. Almacenar en `.beto/snapshots/` con nombre `{{snapshot_id}}.md`
4. Incluir el snapshot_id en MODEL_CALL_PLAN bajo `snapshot_set_used`
