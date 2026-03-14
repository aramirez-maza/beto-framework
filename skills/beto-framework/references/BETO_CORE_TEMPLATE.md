# BETO CORE CONTEXT
Version: 4.2
Last update: {{UTC_TIMESTAMP}}

## 1. SYSTEM INTENT

State clearly and concisely the purpose of the system.
Describe what problem it solves and for whom.
Focus strictly on intent, not on implementation, technology, or execution details.
Limit this section to a maximum of five lines.

## 2. SYSTEM BOUNDARIES

In scope

List explicitly the responsibilities, capabilities, and behaviors that the system
is allowed to perform, as implied directly by the system idea.

Out of scope

List explicitly the responsibilities, capabilities, or behaviors that the system
must never assume, including any form of inference, assumption, or behavior
not grounded in explicit input.

## 3. INPUTS AND OUTPUTS

Inputs

Describe the expected inputs to the system.
If specific formats, structures, or fields are explicitly defined by the idea,
they must be listed here.
If not explicitly defined, describe inputs at a high level without inventing structure.

The system must treat inputs as opaque unless explicitly defined otherwise.

Outputs

Describe the final outputs produced by the system.
Only outputs declared in this section are considered valid system outputs.
Do not introduce intermediate or implicit outputs.

## 4. CORE UNIT OF PROCESSING

Describe the atomic unit processed by the system.

This section MUST include:
- Identity of the unit being processed
- Fields required for processing, exactly as explicitly stated or implied
- Traceability fields that must never be lost across phases

Do NOT invent fields, types, validations, ranges, or optionality.
If uncertainty exists, it must be surfaced as an open question in Section 9.

## 5. GLOBAL INVARIANTS (BETO RULES)

The following rules must never be violated during system evolution:

- No invention of information
- Non-destructive processing
- Absolute traceability across all phases
- Clear and explicit contracts between phases
- Semantic and epistemic consistency

ESTADOS EPISTÉMICOS AUTORIZADOS:
- DECLARED: información explícitamente presente en IDEA_RAW,
  templates del framework, o respuesta explícita del operador.
- NOT_STATED: información ausente — bloquea ejecución, reportar.
- INFERRED: prohibido a partir del cierre del Paso 1.
  Autorizado exclusivamente en el PROMPT_CANONICO (Pasos 0 y 1
  combinados como frontera de expansión controlada).
  La frontera se cierra cuando el operador aprueba el BETO_CORE_DRAFT.
  Usar INFERRED fuera de esta ventana equivale a invención no declarada.

These invariants apply globally and override any phase-specific behavior.

INVARIANTE DE INICIATIVA CONTROLADA:
La iniciativa del ejecutor para expandir el universo de la
solución existe exclusivamente durante el Paso 0 y el Paso 1
combinados como frontera de expansión controlada.
La frontera se cierra cuando el operador aprueba el BETO_CORE_DRAFT.
A partir de ese cierre, ningún componente de este sistema puede
existir sin una decisión DECLARED que autorice su existencia.
La ausencia de declaración no es autorización implícita.
Lo "obvio" no es DECLARED.
Las "buenas prácticas" no son DECLARED.
Los gaps detectados durante la ejecución se registran como
BETO_GAP y se resuelven según la REGLA BETO_GAP del INSTRUCTIVO.

INVARIANTE DE TRAZABILIDAD SEMÁNTICA:
Toda declaración DECLARED en las Secciones 1 a 8 de este
BETO_CORE, y toda OQ resuelta en Sección 9, genera
exactamente un ID de trazabilidad autorizado.
Ese ID debe registrarse en TRACE_REGISTRY_<name>.md
durante el Paso 6.
Ningún código generado en el Paso 8 puede usar un ID
de trazabilidad que no exista en ese registro.
La forma autorizada del ID es:
  BETO_<NOMBRE_SISTEMA>.SEC<N>.<TIPO>.<ELEMENTO>
donde:
  NOMBRE_SISTEMA = nombre del BETO en mayúsculas (ej: CLI)
  N = número de sección (1 al 10)
  TIPO = categoría del elemento según tabla en BETO_INSTRUCTIVO
         sección REGLA TRACE_REGISTRY
  ELEMENTO = slug del elemento declarado, en mayúsculas
OQs resueltas usan el formato: OQ-<N>
Un ID que no siga este formato no es un ID autorizado.

## 6. CONCEPTUAL MODEL

Provide a human-readable conceptual model of the system.
Describe the key concepts and their relationships at an abstract level.

Do NOT include:
- Technical implementation details
- Execution logic
- Algorithms
- Code-level descriptions

## 7. PHASE ARCHITECTURE

| Phase | Name | Purpose | Input | Output |
|------:|------|---------|-------|--------|
| 1 | TBD | TBD | TBD | TBD |

This table defines the complete and authoritative phase architecture of the system.

The system MUST define at least one phase.
The system MAY define multiple phases (N), depending solely on what is explicitly implied
by the system idea.
No phases may be added, removed, or inferred beyond what the idea justifies.

Rules:
- Phases must start at Phase 1
- Phase numbers must be sequential
- Each phase must define a clear input and output contract
- If the system is simple, a single generic phase is acceptable

Each phase may be expanded into a detailed document, but this table remains
the single source of truth for phase structure.

## 8. STABLE TECHNICAL DECISIONS

List technical decisions that affect the system.

Each decision MUST be explicitly labeled as one of:
- Confirmed: A decision that is fixed and must not change
- Proposed: A decision under consideration but not yet immutable

Do NOT invent technical decisions not implied by the system idea.

Nota de trazabilidad:
Cada decisión técnica declarada en esta sección genera un ID
de la forma BETO_<NOMBRE>.SEC8.<SLUG_DECISIÓN>.
El slug debe ser único dentro de este BETO_CORE y descriptivo
del elemento técnico declarado (ej: LITELLM_GATEWAY, CLI_FRAMEWORK).
Decisiones marcadas como Proposed no generan ID autorizado
hasta que sean promovidas a Confirmed en el cierre asistido.

## 9. CURRENT SYSTEM STATE

Phase completed: 0

Phase in progress: 1

Open questions:

CAMPO parent_oq — OBLIGATORIO para OQs de SubBETOs:
  - OQ delegada desde BETO_CORE padre → declarar OQ de origen
  - OQ nueva emergida en la formalización del SubBETO → NONE
  - OQ del BETO_CORE raíz → NONE

CAMPO source con valor DELEGATED_TO_<subbeto>:
  La OQ no se resolvió en este BETO_CORE sino que fue
  delegada formalmente al SubBETO indicado.
  El SubBETO es responsable de cerrarla con parent_oq declarado.

Formato de cada OQ (usar para todas las Open Questions):
- **OQ-<ID>**: <texto de la pregunta>
  parent_oq: OQ-<N> (BETO_CORE_<nombre del padre>) | NONE
  section_origin: <sección del BETO_CORE_INTERVIEW que la generó>
  status: OPEN | CLOSED
  resolution: <texto de la resolución si está CLOSED>
  source: HUMAN | BETO_ASSISTED | DELEGATED_TO_<nombre_subbeto>

Do NOT resolve open questions in this document.

BETO_GAP LOG:
Registrar aquí cada BETO_GAP detectado durante la ejecución del proceso.
Un BETO_GAP ocurre cuando el ejecutor detecta que algo necesario
no fue declarado en este BETO_CORE. Ver REGLA BETO_GAP en BETO_INSTRUCTIVO.

Formato de cada BETO_GAP:
- **BETO_GAP-<ID>**: <descripción del gap detectado>
  fase_origen: Paso <N> del proceso BETO donde emergió
  derivable_del_intent: SÍ | NO
  resolución: BETO_ASSISTED | ESCALADO | PENDIENTE
  justificación: <por qué es derivable del SYSTEM INTENT, o por qué requiere operador>
  estado: OPEN | RESOLVED

Si no existen BETO_GAPs: ninguno declarado

## 10. RISKS AND CONSTRAINTS

List known risks and hard constraints explicitly implied by the system idea.

Do NOT include:
- Speculative risks
- Hypothetical future scenarios
- Assumptions not grounded in explicit input
