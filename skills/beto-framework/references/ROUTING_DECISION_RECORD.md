# ROUTING_DECISION_RECORD
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_1_ROUTING_TEMPLATES -->

---

## Propósito

Registro trazable de cada decisión de routing tomada por el EXECUTION_ROUTER. Toda decisión de selección de ruta debe quedar documentada aquí. No existe decisión de routing silenciosa.

---

## Formato de registro

```yaml
routing_decision:
  decision_id: RD-{{YYYY-NNNN}}          # ID único: año + número secuencial
  timestamp: "{{ISO_8601}}"              # Fecha y hora UTC
  cycle_id: "{{ciclo_id}}"              # ID del ciclo BETO activo
  unit_id: "{{unit_id | null}}"         # ID de unidad si aplica (BETO_PARALELO)
  step_context: "{{paso_beto}}"         # Paso BETO en que ocurre la decisión

  subproblem_description: |
    {{descripción del subproblema evaluado}}

  complexity_evaluation:
    num_outputs: {{int}}
    num_entities: {{int}}
    num_dependencies: {{int}}
    ambiguity_level: {{0|1|2|3}}
    need_for_graph: {{0|1}}
    oq_critical_count: {{int}}
    cross_module_scope: {{0|1}}
    lifecycle_scope: {{0|1}}
    raw_score: {{float}}                 # Suma ponderada calculada
    weights_used: "v4.4_defaults"        # Versión de pesos usada (o nombre de config custom)

  route_selected: "{{BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH}}"

  context_layers_authorized:
    layer_a: true                        # STABLE_CORE_CONTEXT siempre incluida
    layer_b: {{true|false}}             # CYCLE_CONTEXT — requerida para PARTIAL y FULL
    layer_b_scope: "{{minimal|full}}"   # Alcance del CYCLE_CONTEXT incluido
    layer_c: {{true|false}}             # LOCAL_EXECUTION_CONTEXT — siempre incluida

  snapshots_applied:
    - snapshot_id: "{{id}}"
      snapshot_type: "{{tipo}}"
      validity_state: "{{VALID|INVALIDATED}}"

  executor_assigned: "{{nombre_del_subejecutor}}"

  trace_anchor: "{{BETO_V44.SEC<N>.<TIPO>.<ELEMENTO>}}"

  justification: |
    {{justificación de la decisión de routing — derivada de complexity_score y contexto del ciclo}}
```

---

## Registro activo de decisiones

<!-- Las decisiones se añaden a esta sección durante la ejecución del ciclo -->

| decision_id | timestamp | cycle_id | subproblem | route_selected | raw_score |
|------------|-----------|----------|-----------|----------------|-----------|
| (vacío — sin decisiones registradas en este template) | | | | | |

---

## Instrucciones de llenado

1. Completar todos los campos del bloque YAML para cada decisión
2. Añadir una fila al registro activo de decisiones (tabla resumen)
3. Nunca dejar `route_selected` sin valor
4. El campo `justification` debe derivar explícitamente de la IDEA_RAW o del BETO_CORE activo
5. Si el decision_id ya existe (re-evaluación), añadir una nueva entrada con sufijo `-REV1`, `-REV2`, etc.

---

## Relación con otros artefactos

- Si la decisión fue promovida: ver ROUTE_PROMOTION_RECORD
- Snapshots aplicados: ver CYCLE_CONTEXT_SNAPSHOT
- Log de performance de la llamada: ver EXECUTION_PERFORMANCE_LOG
- Plan de la llamada al modelo: ver MODEL_CALL_PLAN
