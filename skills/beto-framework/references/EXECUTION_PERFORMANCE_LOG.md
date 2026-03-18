# EXECUTION_PERFORMANCE_LOG
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS -->

---

## Propósito

Registro de auditoría de todas las llamadas al modelo realizadas durante un ciclo BETO. Permite analizar la eficiencia del routing, detectar patrones de carga contextual excesiva y auditar el uso de rutas. No es autoridad semántica — es un log operativo.

---

## Formato de cada entrada de log

```json
{
  "entry_id": "PL-{{YYYY-NNNN}}",
  "call_id": "{{MCP-id correlacionado}}",
  "cycle_id": "{{ciclo_id}}",
  "unit_id": "{{unit_id | null}}",
  "timestamp": "{{ISO_8601}}",
  "route_type": "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}",
  "executor_type": "{{nombre_del_subejecutor}}",
  "latency_ms": {{int | null}},
  "tokens_input": {{int | null}},
  "tokens_output": {{int | null}},
  "model_class": "{{reasoning|coding|fast|local}}",
  "cache_hit": {
    "prefix_cache": {{true|false}},
    "semantic_cache": {{true|false}},
    "operational_cache": {{true|false}}
  },
  "trace_anchor": "{{BETO_V44.SEC<N>.<TIPO>.<ELEMENTO>}}",
  "call_status": "{{COMPLETED|FAILED|PROMOTED}}",
  "promotion_occurred": {{true|false}},
  "promotion_id": "{{RP-id | null}}",
  "output_artifact": "{{nombre del artefacto producido | null}}",
  "gaps_detected": {{int}},
  "context_tokens_estimated": {{int | null}},
  "notes": "{{notas opcionales de auditoría}}"
}
```

---

## Log activo del ciclo

| entry_id | timestamp | call_id | route_type | executor_type | latency_ms | cache_hit | call_status |
|---------|-----------|---------|-----------|--------------|-----------|---------|------------|
| (vacío — sin entradas en este template) | | | | | | | |

---

## Métricas agregadas (calcular al final del ciclo)

```markdown
## Resumen de eficiencia del ciclo {{ciclo_id}}

| Métrica | Valor |
|---------|-------|
| Total llamadas | 0 |
| Llamadas LIGHT_PATH | 0 |
| Llamadas PARTIAL_PATH | 0 |
| Llamadas FULL_PATH | 0 |
| Promociones de ruta | 0 |
| Promedio tokens_input | — |
| Promedio tokens_output | — |
| Promedio latency_ms | — |
| Hits prefix cache | 0 |
| Hits semantic cache | 0 |
| Hits operational cache | 0 |
| Llamadas con BETO_GAP detectado | 0 |
| Llamadas fallidas | 0 |
```

---

## Instrucciones de uso

1. Crear una entrada por cada llamada al modelo completada
2. Correlacionar con el MODEL_CALL_PLAN mediante `call_id`
3. Si la llamada fue promovida (route cambió durante ejecución): `call_status = PROMOTED`, `promotion_id = RP-id`
4. Calcular métricas agregadas al finalizar el ciclo
5. Almacenar en `.beto/logs/execution_performance_{{ciclo_id}}.md`

---

## Uso para análisis de eficiencia

Este log permite detectar:
- Subproblemas clasificados en FULL_PATH que podrían resolverse como PARTIAL o LIGHT (optimización de umbrales)
- Llamadas con token count muy alto que podrían beneficiarse de mejor estratificación de contexto
- Patrones de promoción de ruta repetidos (indica posible ajuste de umbrales de complejidad)
- Cache miss frecuentes (indica que los snapshots se están invalidando más de lo necesario)
