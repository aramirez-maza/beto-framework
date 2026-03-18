# EXECUTION_ROUTER
## BETO v4.4 — Execution Efficiency and Routing Layer
<!-- BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_1_ROUTING_TEMPLATES -->

---

## Propósito

El EXECUTION_ROUTER es el orquestador central de ejecución de BETO v4.4. Evalúa la complejidad del subproblema actual mediante la función de complejidad declarada y selecciona uno de tres caminos de ejecución internos. Todas las decisiones de routing son trazables y ninguna puede ser silenciosa.

---

## Función de complejidad

```
complexity_score =
  w1 * num_outputs +
  w2 * num_entities +
  w3 * num_dependencies +
  w4 * ambiguity_level +
  w5 * need_for_graph +
  w6 * oq_critical_count +
  w7 * cross_module_scope +
  w8 * lifecycle_scope
```

### Factores

| Factor | Descripción | Rango |
|--------|-------------|-------|
| num_outputs | Número de artefactos de salida esperados | 0–N |
| num_entities | Número de entidades, módulos o componentes identificados | 0–N |
| num_dependencies | Número de dependencias relevantes | 0–N |
| ambiguity_level | Nivel de ambigüedad semántica | 0, 1, 2, 3 |
| need_for_graph | ¿Se requiere BETO_SYSTEM_GRAPH? | 0 o 1 |
| oq_critical_count | Número de OQs críticas detectadas | 0–N |
| cross_module_scope | ¿La tarea toca múltiples módulos o unidades? | 0 o 1 |
| lifecycle_scope | ¿La tarea exige múltiples pasos formales BETO? | 0 o 1 |

### Pesos por defecto (BETO v4.4 — configurables, defaults fijos y trazables)

| Peso | Valor | Factor |
|------|-------|--------|
| w1 | 1 | num_outputs |
| w2 | 1 | num_entities |
| w3 | 1 | num_dependencies |
| w4 | 2 | ambiguity_level |
| w5 | 3 | need_for_graph |
| w6 | 2 | oq_critical_count |
| w7 | 2 | cross_module_scope |
| w8 | 2 | lifecycle_scope |

### Umbrales de routing (configurables, defaults fijos)

| Rango | Ruta seleccionada |
|-------|-------------------|
| 0 – 5 | BETO_LIGHT_PATH |
| 6 – 12 | BETO_PARTIAL_PATH |
| 13 + | BETO_FULL_PATH |

---

## Rutas de ejecución

### BETO_LIGHT_PATH
**Para:** Tareas simples, de una sola pieza, con salida puntual. Sin necesidad de graph, manifests completos ni múltiples OQs críticas.
**Absorbe:** Tareas antes delegadas a un skill externo — ahora dentro del executor unificado bajo las mismas reglas nucleares BETO.
**Restricciones:**
- No puede inventar alcance
- No puede ignorar trazabilidad cuando esta aplique
- No puede generar artefactos incompatibles con el núcleo
- No puede cargar graph, manifests globales ni artefactos estructurales no requeridos
- Si detecta una OQ crítica no absorbible localmente → PROMOVER a BETO_PARTIAL_PATH o BETO_FULL_PATH

### BETO_PARTIAL_PATH
**Para:** Tareas medianas o localizadas dentro de un ciclo BETO ya existente. Cierre, validación o generación de artefactos puntuales sin reconstrucción completa.
**Restricciones:**
- Puede cargar CYCLE_CONTEXT pero no todo el graph completo salvo que sea necesario
- Si el scope se vuelve multiunidad → PROMOVER a BETO_FULL_PATH

### BETO_FULL_PATH
**Para:** Sistemas completos, ideas nuevas, arquitectura, generación de graph, manifests, phases, materialización integral o múltiples unidades con alta complejidad.
**Sin restricciones de carga de contexto** — usa el BETO_CORE completo.

---

## Protocolo de ejecución

El EXECUTION_ROUTER opera como orquestador único. Los subejecutores no pueden llamarse entre sí sin pasar por el orquestador.

### Subejecutores declarados

| Subejecutor | Responsabilidad |
|-------------|----------------|
| eligibility_executor | Evaluación PASO_0 — elegibilidad semántica |
| interview_executor | PASO_2 — entrevista estructural |
| closure_executor | PASO_6 — cierre asistido operativo |
| osc_executor | Evaluación OSC local por OQ crítica o unidad |
| materialization_executor | PASO_10 — materialización de artefactos |
| verification_executor | Verificación TRACE_VERIFIED post-materialización |
| beto_light_executor | Ejecución BETO_LIGHT_PATH |
| beto_partial_executor | Ejecución BETO_PARTIAL_PATH |
| beto_full_executor | Ejecución BETO_FULL_PATH |
| route_promotion_evaluator | Evaluación de condiciones de promoción de ruta |

### Contrato de cada llamada a subejecutor

**Input del subejecutor:**
```
input_contract:         descripción del subproblema
authorized_context:     contexto mínimo autorizado (capas A+B+C según aplique)
execution_scope:        alcance local del subproblema
required_output_artifact: artefacto de salida esperado
route_type:             BETO_LIGHT_PATH | BETO_PARTIAL_PATH | BETO_FULL_PATH
current_snapshot_set:   snapshots activos y válidos aplicables al tramo
```

**Output del subejecutor:**
```
output_artifact:        artefacto producido
updated_state_delta:    delta de estado a aplicar
trace_log:              registro de trazabilidad
detected_gaps:          BETO_GAPs detectados durante la ejecución
next_step_suggestion:   sugerencia para el orquestador
route_reassessment:     nueva evaluación de ruta si aplica (NINGUNA | PROMOVER_A_PARTIAL | PROMOVER_A_FULL)
```

---

## Regla de promoción de ruta

Si durante una ejecución se detecta cualquiera de las siguientes condiciones:
- Apareció una OQ crítica no absorbible localmente
- Se requiere graph no cargado
- Se requiere manifest nuevo
- El scope se volvió multiunidad
- La ambigüedad superó el umbral permitido para el modo actual
- La tarea ya no puede resolverse sin reconstrucción de autoridad estructural

Entonces el route_promotion_evaluator debe registrar:
- LIGHT → PARTIAL: si el subproblema puede cerrarse con CYCLE_CONTEXT
- PARTIAL → FULL: si el subproblema requiere graph o reconstrucción global
- LIGHT → FULL: si aplica directamente

**Toda promoción debe quedar registrada en ROUTE_PROMOTION_RECORD. No existe promoción silenciosa.**

---

## Instrucciones de uso

```
1. Evaluar complexity_score del subproblema usando la función declarada
2. Comparar contra umbrales para seleccionar route_type
3. Registrar decisión en ROUTING_DECISION_RECORD (ver template)
4. Construir authorized_context según capas A+B+C requeridas por route_type
5. Invocar subejecutor apropiado con el contrato completo
6. Si route_reassessment != NINGUNA → ejecutar ROUTE_PROMOTION_RECORD y re-ejecutar
7. Loguear llamada en EXECUTION_PERFORMANCE_LOG
```

---

## Compatibilidad

- Compatible con BETO v4.3 y OSC Layer
- Los ciclos v4.3 existentes no requieren modificación
- El routing es una optimización interna — no altera el significado de ningún paso BETO
