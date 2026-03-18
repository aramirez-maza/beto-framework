# ACTIVE_OQ_SET
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT -->

---

## Propósito

Registro compacto del conjunto de Open Questions activas y relevantes para el tramo actual de ejecución. Permite al subejecutor operar con las OQs exactamente necesarias sin cargar todo el BETO_CORE. Se invalida cuando cualquier OQ del conjunto cambia de estado.

---

## Formato (híbrido JSON+Markdown)

### Cabecera (metadata — JSON)

```json
{
  "snapshot_id": "AQ-{{YYYY-NNNN}}",
  "snapshot_type": "ACTIVE_OQ_SET",
  "cycle_id": "{{ciclo_id}}",
  "unit_id": "{{unit_id | null}}",
  "timestamp": "{{ISO_8601}}",
  "validity_state": "VALID | INVALIDATED",
  "route_type": "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}",
  "version": "{{4.4.0}}",
  "source_artifacts": ["{{BETO_CORE asociado}}"],
  "trace_references": ["{{ids BETO}}"],
  "oq_count": {{int}},
  "critical_oq_count": {{int}}
}
```

### Cuerpo (OQs activas — Markdown)

```markdown
## OQs activas en este tramo

### OQs críticas

| ID | Texto | Tipo | Estado ejecutabilidad | Execution Readiness |
|----|-------|------|----------------------|---------------------|
| OQ-N | {{texto}} | {{OQ_TYPE}} | {{DECLARED_EXECUTABLE|DECLARED_WITH_LIMITS|DECLARED_RAW}} | {{PASS_EXECUTABLE|PASS_WITH_LIMITS|FAIL_EXECUTIONAL_GAP}} |

### OQs no críticas activas

| ID | Texto | Tipo | Estado |
|----|-------|------|--------|
| OQ-N | {{texto}} | {{OQ_TYPE}} | {{OPEN|CLOSED}} |

### OQs cerradas relevantes para el tramo

| ID | Resolución | Fuente |
|----|-----------|--------|
| OQ-N | {{resumen de resolución}} | {{BETO_ASSISTED|HUMAN}} |
```

---

## Reglas de invalidación

El ACTIVE_OQ_SET debe invalidarse si:
1. Una OQ del conjunto cambia de estado (OPEN → CLOSED, PENDING → DECLARED_EXECUTABLE, etc.)
2. Se añade una nueva OQ crítica al ciclo
3. El BETO_CORE fuente fue modificado
4. El route_type del tramo cambió por promoción

---

## Instrucciones de uso

1. Generar ACTIVE_OQ_SET al inicio de cada tramo que tenga OQs relevantes
2. Incluir SOLO las OQs relevantes para el subproblema actual — no cargar todas las OQs del ciclo si no aplican
3. Verificar validity_state antes de usar
4. Almacenar en `.beto/snapshots/` con nombre `{{snapshot_id}}.md`

---

## Relación con otros artefactos

- Ciclo de contexto: ver CYCLE_CONTEXT_SNAPSHOT
- Evaluación OSC: las OQs críticas con DECLARED_RAW requieren EXECUTION_READINESS_CHECK (BETO v4.3)
- Si una OQ crítica no puede cerrarse localmente: registrar en ROUTE_PROMOTION_RECORD
