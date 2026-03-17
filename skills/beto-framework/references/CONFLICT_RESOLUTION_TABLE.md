# CONFLICT_RESOLUTION_TABLE
## BETO Framework v4.3 — Operational Semantic Closure Layer

**Template version:** 4.3.0
**Propósito:** Registrar resoluciones de conflictos operativos detectados durante el
EXECUTION_READINESS_CHECK. Un conflicto operativo ocurre cuando dos o más declaraciones
críticas producen comportamiento inconsistente bajo las mismas condiciones de entrada.

---

## METADATA

- **Sistema:** <!-- nombre del sistema -->
- **Ciclo BETO:** <!-- ciclo_id -->
- **Paso de generación:** 6 — CIERRE_ASISTIDO_OPERATIVO
- **Fecha:** <!-- UTC ISO 8601 -->

---

## RESUMEN

| Métrica                         | Valor |
|---------------------------------|-------|
| Conflictos detectados           |       |
| Conflictos resueltos            |       |
| Conflictos pendientes           |       |
| Conflictos absorbidos como límite |    |

---

## REGISTRO DE CONFLICTOS

### CONFLICT-001 — [Título descriptivo]

**Tipo de conflicto:**
<!-- POLICY_COLLISION | TEMPORAL_AMBIGUITY | SCOPE_OVERLAP | PRIORITY_UNDEFINED | FALLBACK_MISSING | OTRO -->

**OQs involucradas:**
- OQ-XXX: [texto resumido]
- OQ-YYY: [texto resumido]

**Descripción del conflicto:**
```
[Descripción precisa de qué condición activa el conflicto y por qué las
declaraciones son incompatibles o producen comportamiento no determinístico]
```

**Escenario de conflicto:**
```
Condición:  [condición de entrada que activa el conflicto]
Declaración A aplica: [OQ-XXX dice X]
Declaración B aplica: [OQ-YYY dice Y]
Resultado sin resolución: [comportamiento no determinístico]
```

**Resolución:**
- **Modo:** <!-- BETO_ASSISTED | HUMAN | ACCEPTED_AS_LIMIT -->
- **Regla de precedencia declarada:**

```
[Regla explícita que resuelve el conflicto sin ambigüedad]
Ejemplo: "Si condición A y condición B aplican simultáneamente,
          OQ-XXX tiene precedencia sobre OQ-YYY."
```

- **Ejecutabilidad resultante:** <!-- DECLARED_EXECUTABLE | DECLARED_WITH_LIMITS -->
- **Justificación de la resolución:**
```
[Por qué esta resolución es coherente con el SYSTEM INTENT]
```

---

<!-- Repetir bloque CONFLICT-NNN para cada conflicto detectado -->

---

## CONFLICTOS ABSORBIDOS COMO LÍMITE OPERATIVO

Conflictos donde la ambigüedad es tolerable y se acepta como DECLARED_WITH_LIMITS.

| CONFLICT_ID | Condición de conflicto | Límite aceptado | Riesgo declarado |
|-------------|----------------------|----------------|-----------------|
|             |                      |                |                 |

> Si no hay conflictos absorbidos, registrar: **ninguno declarado**

---

## CONFLICTOS PENDIENTES (BLOQUEANTES)

Conflictos que no pudieron resolverse y generan BETO_GAP_EXECUTIONAL.

| CONFLICT_ID | Descripción | GAP_ID generado | Condición de desbloqueo |
|-------------|-------------|-----------------|------------------------|
|             |             |                 |                        |

> Si no hay conflictos pendientes, registrar: **ninguno declarado**

---

## TRAZABILIDAD

- **trace_id:** <!-- ID de trazabilidad del ciclo -->
- **unit_id (si BETO_PARALELO):** <!-- ID de la unidad, o "raíz" -->
