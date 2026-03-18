# MATERIALIZATION_SCOPE
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT -->

---

## Propósito

Define y delimita exactamente qué debe materializarse en el tramo actual de ejecución. Permite al materialization_executor operar con scope local sin recomponer el sistema entero. Es el contrato de límite entre lo que se materializa ahora y lo que se materializa en tramos posteriores.

---

## Formato (híbrido JSON+Markdown)

### Cabecera (metadata — JSON)

```json
{
  "snapshot_id": "MS-{{YYYY-NNNN}}",
  "snapshot_type": "MATERIALIZATION_SCOPE",
  "cycle_id": "{{ciclo_id}}",
  "unit_id": "{{unit_id | null}}",
  "phase": {{número_de_fase}},
  "timestamp": "{{ISO_8601}}",
  "validity_state": "VALID | INVALIDATED",
  "route_type": "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}",
  "version": "{{4.4.0}}",
  "source_artifacts": ["{{BETO_CORE o PHASE_DOC fuente}}"],
  "trace_references": ["{{ids BETO autorizados para este scope}}"],
  "total_artifacts_in_scope": {{int}},
  "artifacts_completed": {{int}},
  "artifacts_pending": {{int}}
}
```

### Cuerpo (scope de materialización — Markdown)

```markdown
## Artefactos en scope para este tramo

| # | Artefacto | Tipo | Operación | Estado | TRACE_ID |
|---|----------|------|-----------|--------|---------|
| 1 | {{nombre_artefacto}} | {{TEMPLATE|CODE|DOC|RULE}} | {{CREAR|ACTUALIZAR|VERIFICAR}} | {{PENDING|IN_PROGRESS|COMPLETE|TRACE_VERIFIED}} | {{BETO_X.SEC<N>.<TIPO>.<ELEMENTO>}} |

## Artefactos explícitamente fuera de scope en este tramo

{{lista de artefactos declarados como fuera del scope actual — esto previene scope creep}}

## Dependencias del tramo

{{lista de artefactos que DEBEN existir antes de que este scope pueda ejecutarse}}

## Criterios de compleción del tramo

{{lista de condiciones que deben cumplirse para declarar este scope como completo}}

## Contexto de materialización necesario (Capa C relevante)

- Template: {{template activo}}
- Contract: {{implementation contract si aplica}}
- Trace Registry: {{TRACE_REGISTRY asociado}}
- Phase: {{Phase document asociado}}

## Verificación post-materialización

Para cada artefacto generado:
- [ ] BETO-TRACE anotado con ID del TRACE_REGISTRY
- [ ] ID verificado contra TRACE_REGISTRY (TRACE_VERIFIED)
- [ ] v43_compatibility declarada
- [ ] Sin inferencias no autorizadas en el contenido
```

---

## Separación razonamiento / materialización

Este scope SOLO aplica a la fase de materialización. No carga contexto de razonamiento global salvo que exista un bloqueo formal declarado. Si durante la materialización se detecta un bloqueo que requiere razonamiento adicional:

1. Detener la materialización del artefacto bloqueado
2. Registrar el bloqueo en `detected_gaps` del output del subejecutor
3. El orquestador decide si volver a razonamiento o continuar con otros artefactos en scope

---

## Reglas de invalidación

El MATERIALIZATION_SCOPE debe invalidarse si:
1. El artefacto fuente (BETO_CORE o PHASE_DOC) fue modificado
2. Un artefacto de dependencia no pudo materializarse
3. El route_type cambió por promoción
4. Se detectó un BETO_GAP que modifica el scope

---

## Instrucciones de uso

1. Generar MATERIALIZATION_SCOPE antes de iniciar cada phase de materialización
2. Declarar explícitamente qué está fuera de scope — esto previene scope creep
3. Actualizar `artifacts_completed` y `artifacts_pending` al completar cada artefacto
4. Almacenar en `.beto/snapshots/` con nombre `{{snapshot_id}}.md`
