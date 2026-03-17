BETO_CORE_INTERVIEW

Rol: Especialista en Ingeniería de Requerimientos / OIM
Propósito: Elicitación, normalización y validación rigurosa de información necesaria para construir un BETO_CORE.md conforme a BETO_CORE_TEMPLATE.md, garantizando materialización sin inferencias no autorizadas y con gobernanza semántica explícita.

INSTRUCCIONES GENERALES

Las preguntas deben responderse en orden.

Se aceptan exclusivamente las respuestas:

no declarado

ninguno declarado (solo si el humano afirma explícitamente “no hay”)

NO inferir

NO asumir

NO completar

NO optimizar

Toda ausencia de información debe quedar registrada explícitamente.

El objetivo de la entrevista es eliminar ambigüedad operativa, no forzar decisiones técnicas.

Este documento puede ser respondido por:

un humano

un LLM en modo elicitación

un sistema híbrido

SECCIÓN 1 — SYSTEM INTENT

(Alimenta: BETO_CORE → Sección 1)

P1.1 — Propósito fundamental

¿Qué debe existir cuando este sistema esté resuelto?

¿Qué problema específico deja de existir?

P1.2 — Criterio de éxito observable

¿Cómo sabrás que el sistema cumple su objetivo?

Describe entre una y tres capacidades observables que indiquen que el sistema es usable y satisfactorio.

P1.3 — Naturaleza del sistema

¿El sistema está orientado exclusivamente a exploración y consulta o debe producir salidas persistentes reutilizables?

SECCIÓN 2 — SYSTEM BOUNDARIES

(Alimenta: BETO_CORE → Sección 2)

P2.1 — Alcance explícito

¿Qué funciones o capacidades están claramente dentro del alcance del sistema?

P2.2 — Fuera de alcance explícito

¿Qué cosas NO hará el sistema, aunque puedan parecer relacionadas o tentadoras?

P2.3 — Exclusiones operativas

Enumera explícitamente exclusiones operativas (optimización, edición de datos, simulación física, integraciones externas, autenticación, multiusuario, etc.).

Si no se conocen, responder no declarado.

SECCIÓN 3 — INPUTS AND OUTPUTS

(Alimenta: BETO_CORE → Sección 3)

P3.1 — Inputs principales

¿Qué entradas recibe el sistema?

Describe origen, tipo y forma general.

P3.2 — Outputs principales

¿Qué produce el sistema como resultado?

Describe los outputs en términos funcionales, no técnicos.

P3.3 — Contrato mínimo del input
Responder solo lo que se conozca con certeza:

¿El archivo o entrada tiene encabezado?

Separador utilizado (coma, punto y coma, barra vertical, tab, otro, no declarado)

Encoding (UTF-8, Latin-1, otro, no declarado)

¿El formato del campo Fecha es estable?

¿Cómo se representan valores vacíos o faltantes?

Si algún aspecto del contrato del input no se declara aquí, el sistema no puede asumirlo.

P3.4 — Contrato de salida ejecutable

¿Cómo debe ejecutarse o consumirse la salida para considerarse entregada?

Abrir archivo local

Servicio local + URL

Otro

no declarado

P3.5 — Persistencia de la salida

¿El sistema debe generar artefactos persistentes reutilizables entre ejecuciones?

P3.6 — CANDIDATOS A SUB-BETO POR INPUTS (RECURSIVIDAD CONTROLADA)

Para cada input declarado en P3.1:

a) ¿Está completamente especificado en esta entrevista?

sí / no

b) Si no, clasificar el input como una sola:

primitivo

estándar externo

implementable directo

complejo con incertidumbre propia

c) Si es estándar externo, indicar el estándar (o no declarado).

d) Si es complejo con incertidumbre propia, registrar:

Candidato Sub-BETO: <nombre del input> (Origen: Sección 3)

SECCIÓN 4 — CORE UNIT OF PROCESSING

(Alimenta: BETO_CORE → Sección 4)

P4.1 — Unidad atómica

¿Cuál es la unidad mínima que procesa el sistema?

P4.2 — Campos esenciales

¿Qué campos son imprescindibles para que la unidad pueda procesarse?

P4.3 — Campos de trazabilidad

¿Qué campos deben preservarse siempre para consulta o auditoría?

P4.4 — Unicidad

¿Existe un campo o combinación de campos que identifique de forma única a la unidad?

P4.5 — Política de duplicados

¿Cómo deben tratarse?

Mostrar todos

Consolidar

no declarado

P4.6 — CANDIDATOS A SUB-BETO POR COMPONENTES (RECURSIVIDAD CONTROLADA)

Para cada campo o componente:

a) ¿Es tipo primitivo? (sí / no)
b) Si no, ¿existe estándar externo completo? (sí / no)
c) Si no, ¿es implementable sin ambigüedad? (sí / no)
d) Si no →
Candidato Sub-BETO: <nombre del componente> (Origen: Sección 4)

SECCIÓN 5 — GLOBAL INVARIANTS (BETO RULES)

(Alimenta: BETO_CORE → Sección 5)

P5.1 — Reglas no negociables

Enumera reglas que el sistema no puede violar bajo ninguna circunstancia.

P5.2 — Señalización de aproximaciones

¿Toda representación aproximada debe indicarse explícitamente como tal?

P5.3 — Invariantes de trazabilidad

¿El registro completo debe estar siempre disponible para consulta bajo demanda?

SECCIÓN 6 — CONCEPTUAL MODEL

(Alimenta: BETO_CORE → Sección 6)

P6.1 — Conceptos principales

Enumera los conceptos clave del sistema y su significado mínimo.

P6.2 — Definición de interacción

¿Qué debe ocurrir al interactuar con un elemento?

P6.3 — CANDIDATOS A BETO_PARALELO (INDEPENDENCIA FUNCIONAL)

Para cada concepto o capacidad identificada en P6.1:

a) ¿Puede este componente desarrollarse por un equipo independiente
   conociendo únicamente su propósito, inputs, outputs y contratos,
   sin necesidad de conocer la lógica interna de los demás componentes?
   (sí / no / no declarado)

b) Si sí:
   Candidato BETO_PARALELO: <nombre del componente> (Origen: Sección 6)

Nota: La clasificación formal PARALLEL vs SUBBETO ocurre en el
Paso 3 del BETO_INSTRUCTIVO. Esta pregunta solo registra candidatos.

P6.4 — CANDIDATOS A SUB-BETO POR CONCEPTOS (RECURSIVIDAD CONTROLADA)

Para cada concepto:

a) ¿Está definido con precisión operacional suficiente? (sí / no)
b) Si no, clasificar:

definible por estándar externo

definible por contrato interno

no declarado

c) Si requiere contrato interno →
Candidato Sub-BETO: <concepto> (Origen: Sección 6)

SECCIÓN 7 — PHASE ARCHITECTURE

(Alimenta: BETO_CORE → Sección 7)

P7.1 — Fases del sistema

¿Qué fases existen según la idea del sistema?

P7.2 — Distribución de capacidades

¿Interacción y búsqueda pertenecen a la misma fase o a fases separadas?

SECCIÓN 8 — STABLE TECHNICAL DECISIONS

(Alimenta: BETO_CORE → Sección 8)

P8.1 — Decisiones técnicas confirmadas

Enumera decisiones técnicas ya tomadas.

Etiquetar cada una como:

Confirmed

Proposed

P8.2 — Restricciones de entorno

¿Existen restricciones de entorno (offline, SO, regulación, etc.)?

SECCIÓN 9 — CURRENT SYSTEM STATE

(Alimenta: BETO_CORE → Sección 9)

P9.1 — Estado de ejecución requerido

Phase completed

Phase in progress

P9.2 — Política de cierre de incertidumbre

¿Cómo se tratan incertidumbres no críticas?

SECCIÓN 10 — RISKS AND CONSTRAINTS

(Alimenta: BETO_CORE → Sección 10)

P10.1 — Riesgos conocidos

Enumera riesgos explícitos.

P10.2 — Restricciones conocidas

Enumera restricciones duras.

P10.3 — Expectativa de usabilidad

¿Debe mantenerse usable con el volumen esperado?

P10.4 — Estrategias de degradación permitidas

¿Se permiten agregación, filtrado, etc.?

SECCIÓN 11 — SUB-BETO GOVERNANCE (DECISIÓN CENTRAL)

REGLA OBLIGATORIA DE EVALUACIÓN:
El razonamiento de cada condición debe documentarse explícitamente.
Un registro que solo declara la conclusión sin razonamiento
es INCOMPLETO y no válido para auditoría BETO.
La Condición 3 requiere tabla de ambigüedades evaluadas.
Los candidatos RECHAZADOS deben documentar riesgo de absorción.

Cada candidato SubBETO debe evaluarse usando la siguiente estructura OBLIGATORIA:

### C-XX: <Nombre del candidato>

**Condición 1 — No es primitivo:**
Evaluación: ✅ / ❌
Razón: <texto obligatorio — mínimo 1 oración>

**Condición 2 — Sin estándar externo completo:**
Evaluación: ✅ / ❌
Razón: <texto obligatorio — mínimo 1 oración>

**Condición 3 — No implementable directo sin ambigüedad:**
Evaluación: ✅ / ❌
Ambigüedades evaluadas:
  | Ambigüedad identificada | Bloquea diseño estructural | Razón |
  |------------------------|---------------------------|-------|
  | <descripción>          | SÍ / NO                   | <texto> |
Conclusión Condición 3: <texto — por qué pasa o falla>

**Condición 4 — Tiene OQ propia:**
Evaluación: ✅ / ❌
OQ identificada: <texto — o "ninguna" si falla>

**DECISIÓN FINAL: APROBADO / RECHAZADO**
Razón consolidada: <síntesis de las 4 condiciones>

[Solo si RECHAZADO — obligatorio:]
Riesgo de absorción: BAJO / MEDIO / ALTO
Descripción del riesgo: <qué complejidad absorbe el BETO raíz>
Mitigación declarada: <cómo el BETO raíz gestiona esa complejidad>

P11.1 — Lista consolidada de candidatos

Candidatos a SubBETO (complejidad propia — evaluados en P11.2):
Consolidar candidatos de P3.6, P4.6 y P6.4
Si no hay: ninguno declarado

Candidatos a BETO_PARALELO (independencia funcional — clasificados en Paso 3 del BETO_INSTRUCTIVO):
Consolidar candidatos de P6.3
Si no hay: ninguno declarado

Nota: La clasificación formal PARALLEL vs SUBBETO ocurre en el
Paso 3 del BETO_INSTRUCTIVO mediante la Regla de Clasificación
Estructural. La entrevista solo registra y consolida candidatos.

P11.2 — Evaluación formal de terminación
Para cada candidato:

¿Es primitivo? → PARAR

¿Tiene estándar externo completo? → PARAR

¿Es implementable directo? → PARAR

¿Tiene Open Questions propias?

NO → PARAR

SÍ → APROBAR Sub-BETO

P11.3 — Regla canónica de creación de Sub-BETO

Un Sub-BETO se crea si y solo si:

No es primitivo

No tiene estándar externo suficiente

No es implementable directo

Tiene al menos una Open Question propia

P11.4 — Registro de Sub-BETOs aprobados
Para cada uno:

Nombre: BETO_CORE_<nombre>

Relación: Hijo del BETO_CORE principal

Alcance: cerrar ambigüedad sin inventar

Entrada: definida por el padre

Salida: contrato completo reutilizable

P11.5 — Protección contra optimización infinita
Confirmar:

Suficiencia

No perfección

Declarativo

Responder: Confirmado o no declarado.

SECCIÓN 12 — PASE DE CONSISTENCIA

(No elicita información nueva — verifica coherencia interna de las
respuestas de las Secciones 1 a 11)

REGLA: Si se detecta contradicción, el ejecutor registra el conflicto
y solicita resolución al operador antes de generar el BETO_CORE_DRAFT.
Un BETO_CORE generado con contradicciones no resueltas tiene estado INVÁLIDO.

P12.1 — Consistencia Scope → Outputs
¿Cada output declarado en P3.2 está justificado por al menos un elemento
de P2.1 (In scope)?
Si algún output no tiene respaldo en el scope declarado → registrar conflicto.

P12.2 — Consistencia Inputs → Core Unit
¿La unidad de procesamiento declarada en P4.1 es derivable de los
inputs declarados en P3.1?
Si no hay relación declarable entre ambos → registrar conflicto.

P12.3 — Consistencia Candidates → Sección 11
¿Todos los candidatos registrados en P3.6, P4.6 y P6.4 aparecen
en la lista consolidada de P11.1?
Si falta algún candidato en la consolidación → registrar omisión.

P12.4 — Consistencia Phases → Outputs
¿Cada fase declarada en P7.1 contribuye a al menos un output de P3.2?
Una fase sin output asociado es candidata a BETO_GAP.

P12.5 — Consistencia Technical Decisions → Scope
¿Cada decisión técnica de P8.1 tiene respaldo en al menos un elemento
de P2.1 (In scope)?
Una decisión técnica sin respaldo en el scope declarado es candidata a BETO_GAP.

CIERRE DE CONSISTENCIA:
Conflictos detectados: <lista o "ninguno">
Si conflictos > 0: resolver con el operador antes de generar BETO_CORE_DRAFT.
Si conflictos = 0: BETO_CORE_INTERVIEW COMPLETO — proceder al Paso 1.

---

SECCIÓN 13 — CLASIFICACIÓN DE OQs (OPERATIONAL SEMANTIC CLOSURE — BETO v4.3)

(No elicita información nueva — clasifica las OQs de Sección 9 para el
EXECUTION_READINESS_CHECK del Paso 6)

REGLA: Esta sección es obligatoria para todos los BETO_CORE.
Las OQs de tipo OQ_POLICY, OQ_EXECUTION, OQ_EXCEPTION, OQ_DATA_SEMANTICS
NO pueden cerrarse con texto libre simple en el Paso 6.
Deben producir un OQ_RESPONSE_EXECUTABLE.md con EXECUTION_READINESS_CHECK completo.

P13.1 — Tipología de cada OQ

Para cada OQ declarada en Sección 9 (P9.1), asignar exactamente uno de:

OQ_CONFIG
    Aplica a: parámetros de configuración, valores umbral, timeouts, límites numéricos.
    Ejemplo: "¿Cuál es el timeout máximo de espera?"

OQ_POLICY
    Aplica a: reglas de negocio, comportamiento bajo condiciones específicas,
    prioridades de decisión, criterios de aceptación.
    Ejemplo: "¿Qué ocurre si dos reglas de prioridad aplican simultáneamente?"

OQ_EXECUTION
    Aplica a: flujo de ejecución, secuencia de pasos, condiciones de activación,
    triggers, orquestación de componentes.
    Ejemplo: "¿Cuándo se activa el componente de validación?"

OQ_EXCEPTION
    Aplica a: manejo de errores, casos de borde, comportamiento de fallback,
    recuperación ante fallos.
    Ejemplo: "¿Qué hace el sistema si el archivo de entrada no existe?"

OQ_DATA_SEMANTICS
    Aplica a: significado de campos, interpretación de valores, formatos de datos,
    convenciones de representación.
    Ejemplo: "¿Qué significa 'estado activo' para una orden?"

OQ_INTERFACE
    Aplica a: contratos de entrada/salida, formatos de intercambio, APIs,
    protocolos de comunicación entre componentes.
    Ejemplo: "¿En qué formato emite el sistema alertas al exterior?"

OQ_OBSERVABILITY
    Aplica a: logging, métricas, trazas, monitoreo, capacidades de diagnóstico.
    Ejemplo: "¿Qué eventos deben registrarse en el log de auditoría?"

Formato de clasificación:
OQ-<ID>: <OQ_TYPE> | Crítica: SÍ/NO | Texto breve de la OQ

P13.2 — Identificación de OQs críticas

Una OQ es crítica si impacta alguno de:
- comportamiento del sistema
- lógica de decisión
- flujo
- tiempo
- políticas
- conflictos
- excepciones
- datos
- interfaces
- riesgo
- observabilidad
- fallback

Listar todas las OQs críticas identificadas:
<lista de OQ-IDs clasificadas como críticas, o "ninguna">

P13.3 — OQs que requieren EXECUTION_READINESS_CHECK

Por regla BETO v4.3, deben procesarse con OQ_RESPONSE_EXECUTABLE.md:
- Toda OQ crítica de tipo OQ_POLICY
- Toda OQ crítica de tipo OQ_EXECUTION
- Toda OQ crítica de tipo OQ_EXCEPTION
- Toda OQ crítica de tipo OQ_DATA_SEMANTICS

Listar OQs que requerirán OQ_RESPONSE_EXECUTABLE en el Paso 6:
<lista de OQ-IDs, o "ninguna">

CIERRE DE CLASIFICACIÓN OSC:
OQs clasificadas: <N>
OQs críticas identificadas: <N>
OQs que requieren EXECUTION_READINESS_CHECK: <N>
Nota: El EXECUTION_READINESS_CHECK se ejecuta en el Paso 6 (CIERRE_ASISTIDO_OPERATIVO).

---

CIERRE