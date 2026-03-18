# ROUTE_PROMOTION_RECORD
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_1_ROUTING_TEMPLATES -->

---

## Propósito

Registro trazable de toda promoción de ruta ocurrida durante la ejecución de un ciclo BETO. Una promoción de ruta ocurre cuando la ruta seleccionada inicialmente (LIGHT o PARTIAL) ya no puede resolver el subproblema sin reconstrucción de autoridad estructural. Toda promoción debe registrarse aquí — no existe promoción silenciosa.

---

## Formato de registro

```yaml
route_promotion:
  promotion_id: RP-{{YYYY-NNNN}}         # ID único: año + número secuencial
  timestamp: "{{ISO_8601}}"              # Fecha y hora UTC
  cycle_id: "{{ciclo_id}}"              # ID del ciclo BETO activo
  unit_id: "{{unit_id | null}}"         # ID de unidad si aplica (BETO_PARALELO)
  original_decision_id: "{{RD-id}}"     # ID de la ROUTING_DECISION original que se promueve

  promotion_transition: "{{LIGHT_TO_PARTIAL | PARTIAL_TO_FULL | LIGHT_TO_FULL}}"

  trigger_conditions:
    oq_critical_unabsorbable: {{true|false}}   # OQ crítica no absorbible localmente
    graph_required: {{true|false}}              # Se requiere BETO_SYSTEM_GRAPH no cargado
    manifest_new_required: {{true|false}}       # Se requiere manifest nuevo
    scope_became_multiunit: {{true|false}}      # El scope se volvió multiunidad
    ambiguity_exceeded_threshold: {{true|false}} # Ambigüedad superó umbral permitido
    structural_authority_required: {{true|false}} # Requiere reconstrucción de autoridad estructural

  trigger_description: |
    {{descripción explícita de qué disparó la promoción — qué se detectó y cuándo}}

  new_route: "{{BETO_PARTIAL_PATH | BETO_FULL_PATH}}"

  context_expansion_required:
    layer_b_added: {{true|false}}               # CYCLE_CONTEXT añadido
    layer_b_expanded: {{true|false}}            # CYCLE_CONTEXT expandido a scope completo
    snapshots_invalidated:
      - snapshot_id: "{{id}}"
        reason: "{{razón de invalidación}}"
    new_snapshots_required:
      - snapshot_type: "{{tipo}}"
        reason: "{{razón}}"

  impact_on_current_execution: |
    {{descripción del impacto: qué trabajo ya realizado es válido, qué debe rehacerse}}

  trace_anchor: "{{BETO_V44.SEC<N>.<TIPO>.<ELEMENTO>}}"

  operator_notification_required: {{true|false}}  # Si la promoción requiere notificar al operador
  operator_notification_text: |
    {{texto de notificación si aplica — vacío si false}}
```

---

## Registro activo de promociones

| promotion_id | timestamp | cycle_id | transition | trigger | new_route |
|-------------|-----------|----------|-----------|---------|-----------|
| (vacío — sin promociones en este template) | | | | | |

---

## Instrucciones de llenado

1. Completar TODOS los campos — ninguno puede omitirse
2. `trigger_conditions` debe tener al menos un campo en `true`
3. `trigger_description` debe ser específica: qué artefacto, qué OQ o qué condición disparó la promoción
4. `impact_on_current_execution` debe describir qué trabajo puede reutilizarse
5. Si la promoción requiere notificación al operador, el texto debe ser claro y no contener inferencias

---

## Relación con otros artefactos

- Decisión original que se promueve: ver ROUTING_DECISION_RECORD con el original_decision_id
- Nuevo contexto requerido: ver CYCLE_CONTEXT_SNAPSHOT
- Si la promoción llegó a BETO_FULL_PATH: cargar graph completo y MANIFEST_PROYECTO
