# OQ_RESPONSE_EXECUTABLE
## BETO Framework v4.3 — Operational Semantic Closure Layer

**Template version:** 4.3.0
**Propósito:** Registrar la respuesta a una OQ crítica con evidencia de ejecutabilidad operativa.
Este artefacto reemplaza la respuesta de texto libre simple para OQs de tipo
OQ_POLICY, OQ_EXECUTION, OQ_EXCEPTION, OQ_DATA_SEMANTICS.

---

## IDENTIFICACIÓN

- **OQ_ID:** <!-- OQ-<N> -->
- **OQ_TYPE:** <!-- OQ_CONFIG | OQ_POLICY | OQ_EXECUTION | OQ_EXCEPTION | OQ_DATA_SEMANTICS | OQ_INTERFACE | OQ_OBSERVABILITY -->
- **Texto de la OQ:** <!-- Texto original de la pregunta -->
- **Criticidad:** <!-- CRÍTICA | NO_CRÍTICA -->
- **BETO_CORE origen:** <!-- nombre del artefacto BETO_CORE donde vive la OQ -->

---

## RESPUESTA DECLARADA

```
[Texto completo de la respuesta]
```

---

## EXECUTION_READINESS_CHECK

### Campos obligatorios de cierre ejecutable

| Campo              | Declarado | Valor / Descripción                           |
|--------------------|-----------|-----------------------------------------------|
| **alcance**        | SÍ / NO   | ¿Sobre qué aplica exactamente esta respuesta? |
| **trigger**        | SÍ / NO   | ¿Cuándo aplica? ¿Qué lo activa?              |
| **input**          | SÍ / NO   | ¿Qué datos o condiciones recibe?             |
| **output**         | SÍ / NO   | ¿Qué produce o decide?                       |
| **constraint**     | SÍ / NO   | ¿Qué restricciones duras aplican?            |
| **fallback**       | SÍ / NO   | ¿Qué ocurre si no se puede aplicar?          |
| **exception**      | SÍ / NO   | ¿Qué casos de excepción existen?             |
| **trazabilidad**   | SÍ / NO   | ¿Hay ID de trazabilidad asignable?           |

### Resultado del check

- **Resultado:** <!-- PASS_EXECUTABLE | PASS_WITH_LIMITS | FAIL_EXECUTIONAL_GAP -->
- **Justificación:**

```
[Razonamiento explícito de por qué se asignó este resultado]
```

---

## ESTADO FINAL DE LA OQ

- **execution_state:** <!-- DECLARED_EXECUTABLE | DECLARED_WITH_LIMITS | DECLARED_RAW -->
- **ambigüedad_residual:** <!-- descripción de ambigüedad aceptada, o "ninguna" -->
- **límites_aceptados:** <!-- descripción de límites operativos aceptados, o "ninguno" -->
- **BETO_GAP_EXECUTIONAL:** <!-- ID del gap si aplica, o "no aplica" -->
- **requestion_count:** <!-- 0 | 1 | 2 (máximo = max_operational_requestions) -->

---

## HISTORIAL DE REPREGUNTAS (si aplica)

### Repregunta 1 (si se realizó)

- **Motivo:** <!-- Por qué fue necesaria la repregunta -->
- **Respuesta obtenida:** <!-- Texto de la respuesta a la repregunta -->
- **Impacto en execution_state:** <!-- Cómo cambió el estado -->

### Repregunta 2 (si se realizó — máximo permitido)

- **Motivo:** <!-- Por qué fue necesaria la segunda repregunta -->
- **Respuesta obtenida:** <!-- Texto de la respuesta -->
- **Impacto en execution_state:** <!-- Estado final tras esta repregunta -->

> **Nota:** max_operational_requestions = 2. Si después de 2 repreguntas el estado
> sigue siendo DECLARED_RAW, la OQ queda bloqueante hasta nueva declaración del operador.

---

## TRAZABILIDAD

- **Generado en paso BETO:** <!-- Paso 6 — CIERRE_ASISTIDO_OPERATIVO -->
- **Evaluado por:** <!-- BETO_ASSISTED | HUMAN -->
- **Timestamp:** <!-- UTC ISO 8601 -->
- **unit_id (si BETO_PARALELO):** <!-- ID de la unidad, o "raíz" -->
- **trace_id:** <!-- ID de trazabilidad del ciclo -->
