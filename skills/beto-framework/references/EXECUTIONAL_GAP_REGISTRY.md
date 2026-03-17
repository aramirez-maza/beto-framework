# EXECUTIONAL_GAP_REGISTRY
## BETO Framework v4.3 — Operational Semantic Closure Layer

**Template version:** 4.3.0
**Propósito:** Registro centralizado de todos los BETO_GAP_EXECUTIONAL del ciclo.
Un BETO_GAP_EXECUTIONAL ocurre cuando una OQ tiene respuesta (no es NOT_STATED)
pero esa respuesta es insuficiente para ejecución consistente sin inferencias relevantes.

**Relación con BETO_GAP clásico:**
- BETO_GAP: la respuesta no existe (NOT_STATED)
- BETO_GAP_EXECUTIONAL: la respuesta existe pero no es operativamente suficiente
- No se sustituyen — se complementan

---

## METADATA

- **Sistema:** <!-- nombre del sistema -->
- **Ciclo BETO:** <!-- ciclo_id -->
- **Paso de generación:** 6 — CIERRE_ASISTIDO_OPERATIVO
- **Fecha:** <!-- UTC ISO 8601 -->

---

## RESUMEN

| Métrica                              | Valor |
|--------------------------------------|-------|
| BETO_GAP_EXECUTIONAL totales         |       |
| Bloqueantes (impiden materialización) |      |
| No bloqueantes (degradan calidad)    |       |
| Resueltos en este ciclo              |       |
| Pendientes para siguiente ciclo      |       |

---

## REGISTRO DE BETO_GAP_EXECUTIONAL

### BETO_GAP_EX-001

**OQ_ID afectada:** OQ-XXX
**OQ_TYPE:** <!-- OQ_CONFIG | OQ_POLICY | OQ_EXECUTION | OQ_EXCEPTION | OQ_DATA_SEMANTICS | OQ_INTERFACE | OQ_OBSERVABILITY -->

**Respuesta existente (el problema no es ausencia de respuesta):**
```
[Transcripción de la respuesta declarada que es insuficiente]
```

**Por qué no es ejecutable:**
```
[Descripción precisa de qué hace que esta respuesta sea insuficiente:
- contiene patrones blandos: "alto", "bajo", "adecuado", "estándar", "rápido",
  "importante", "cuando sea necesario", "según convenga", "si aplica"
- no declara trigger: cuándo aplica
- no declara input: sobre qué aplica
- no declara output: qué produce
- no declara constraint: qué restricciones
- no declara fallback: qué si falla
- no declara excepción: casos de borde
- otro: [descripción]]
```

**Campos ausentes del EXECUTION_READINESS_CHECK:**
- [ ] alcance
- [ ] trigger
- [ ] input
- [ ] output
- [ ] constraint
- [ ] fallback
- [ ] exception
- [ ] trazabilidad

**Impacto en materialización:**
- **Bloqueante:** <!-- SÍ | NO -->
- **Descripción del impacto:**
```
[Qué comportamiento del sistema queda sin determinar]
```

**Repreguntas realizadas:**
- **Repregunta 1:** <!-- texto o "no realizada" -->
  - Resultado: <!-- respuesta obtenida o "sin respuesta suficiente" -->
- **Repregunta 2:** <!-- texto o "no realizada" -->
  - Resultado: <!-- respuesta obtenida o "sin respuesta suficiente" -->

**Estado final:**
- **execution_state de la OQ:** DECLARED_RAW
- **Estado del gap:** <!-- ACTIVO | RESUELTO_PARCIALMENTE | RESUELTO -->
- **Resolución posible sin operador:** <!-- SÍ (derivable del SYSTEM INTENT) | NO (requiere operador) -->

**Evento registrado:** BETO_EXECUTIONAL_REQUESTION (si se realizaron repreguntas)

---

<!-- Repetir bloque BETO_GAP_EX-NNN para cada gap execucional -->

---

## GAPS EXECUCIONALES RESUELTOS

Gaps que se resolvieron durante el CIERRE_ASISTIDO_OPERATIVO.

| GAP_ID | OQ_ID | Método de resolución | execution_state final |
|--------|-------|---------------------|-----------------------|
|        |       | BETO_ASSISTED / HUMAN / REQUESTION | DECLARED_EXECUTABLE / DECLARED_WITH_LIMITS |

> Si no hay gaps resueltos, registrar: **ninguno declarado**

---

## GAPS EXECUCIONALES PENDIENTES (BLOQUEANTES)

Gaps que requieren acción del operador antes de materializar.

| GAP_ID | OQ_ID | Descripción del bloqueo | Acción requerida del operador |
|--------|-------|------------------------|------------------------------|
|        |       |                        |                              |

> Si no hay gaps pendientes, registrar: **ninguno declarado**

---

## COMPATIBILIDAD BETO_PARALELO

Cuando el sistema tiene nodos BETO_PARALELO, los gaps son locales a cada unidad.

| unit_id | GAP_IDs locales | Impacto en otras unidades | Estado de la unidad |
|---------|----------------|--------------------------|---------------------|
|         |                | NINGUNO (aislado)        | EXECUTABLE / WITH_LIMITS / BLOCKED |

**Regla aplicada:** Un BETO_GAP_EXECUTIONAL en una unidad no bloquea globalmente.
Solo bloquea el avance de la unidad que lo contiene.

> Si el sistema es monolítico (sin BETO_PARALELO), registrar: **no aplica**

---

## EVENTOS EMITIDOS

| Evento | Timestamp | OQ_ID | unit_id | trace_id |
|--------|-----------|-------|---------|----------|
| BETO_EXECUTIONAL_REQUESTION | | | | |
| BETO_GAP_EXECUTIONAL | | | | |
| BETO_DECLARATION_PROMOTED_TO_EXECUTABLE | | | | |
| BETO_DECLARATION_ACCEPTED_WITH_LIMITS | | | | |

---

## TRAZABILIDAD

- **trace_id:** <!-- ID de trazabilidad del ciclo -->
- **Referencia a BETO_GAP clásico (si hay gaps relacionados):**
  - <!-- lista de BETO_GAP IDs que complementan estos gaps execucionales, o "ninguno" -->
