# BETO CORE CONTEXT
Version: 4.2
Last update: 2026-03-15T00:00:00Z

## 1. SYSTEM INTENT

Create a lightweight monitoring tool for Linux administrators that continuously reads text log files from a configurable directory and detects repeated error patterns.
The system exists to surface recurrent operational problems quickly without requiring heavy observability platforms.
Its purpose is to identify when the same error appears more than a configured threshold inside a configured time window.
When that condition is met, the system must emit a local console alert and persist the alert event to a local alerts file.

## 2. SYSTEM BOUNDARIES

In scope

- Run on Linux
- Monitor text log files inside a configurable directory
- Read log files continuously
- Detect repeated simple error patterns
- Compare repeated occurrences against a configured threshold N inside a configured time window
- Emit local alerts in console
- Persist alert events to a local alerts file

Out of scope

- Sending emails
- Connecting to external services
- Advanced analytics
- Machine learning or AI-based analysis
- Monitoring all system logs automatically outside the configured directory
- Heavy observability stacks such as ELK or Splunk

## 3. INPUTS AND OUTPUTS

Inputs

- A configurable directory path in Linux containing text log files
- Log lines read continuously from files inside that directory
- A configured repetition threshold N
- A configured time window for repeated detection
- A local alerts file path for persisted alert events

The system must treat log contents as plain text unless a stricter structure is explicitly declared later.

Outputs

- A local console alert when a repeated error pattern crosses the configured threshold inside the configured time window
- A persisted alert event written to a local alerts file

## 4. CORE UNIT OF PROCESSING

The atomic unit processed by the system is a single log line interpreted as a candidate error event.
A candidate error event is a line containing the textual marker `ERROR`.

Fields required for processing, exactly as explicitly stated or implied:

- Raw log line content
- Detection timestamp associated with the observed event
- Extracted error pattern string used for repetition comparison, defined initially as the literal text after the `ERROR` marker

Traceability fields that must never be lost across phases:

- Source log file path
- Detection timestamp
- Matched pattern string

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

The system is centered on four key concepts:

- Log source: the configurable directory and the text log files observed within it
- Candidate error event: a log line that is eligible for repetition tracking
- Repeated error pattern: the normalized pattern string used to group repeated error events
- Alert event: the local record emitted when a repeated error pattern crosses the configured threshold inside the configured time window

The system reads from log sources, interprets qualifying lines as candidate error events, groups them by repeated error pattern across time, and produces alert events when the configured repetition condition is satisfied.

## 7. PHASE ARCHITECTURE

| Phase | Name | Purpose | Input | Output |
|------:|------|---------|-------|--------|
| 1 | Log Monitoring | Continuously read text log files from the configured directory and surface candidate error events | Configured directory path and log file contents | Candidate error events |
| 2 | Repetition Detection | Group candidate error events by repeated pattern and evaluate threshold N inside the configured time window | Candidate error events, threshold N, time window | Repeated pattern detections |
| 3 | Alert Emission | Emit a local console alert and persist the alert event to a local alerts file | Repeated pattern detections | Console alert and persisted alert event |

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

- Confirmed: The runtime target is Linux only
- Confirmed: The monitored inputs are text log files inside a configurable directory
- Confirmed: Alerting is local only through console output and a local alerts file
- Confirmed: Repetition detection is governed by a configurable threshold N and a configurable time window
- Confirmed: A candidate error event is determined by presence of the textual marker `ERROR` in the log line
- Confirmed: Initial pattern equality is determined by literal comparison of the text after the `ERROR` marker
- Confirmed: The alerts file is a local append-only text file
- Confirmed: The implementation uses Python standard library only
- Confirmed: The materialized project file `materialized/pyproject.toml` declares the package entrypoint
- Confirmed: The materialized file `materialized/src/repeated_log_monitor/config.py` defines runtime configuration input parsing
- Confirmed: The materialized file `materialized/src/repeated_log_monitor/models.py` defines the event and alert data contracts
- Confirmed: The materialized file `materialized/src/repeated_log_monitor/monitor.py` implements continuous log monitoring and rotation-aware file tracking
- Confirmed: The materialized file `materialized/src/repeated_log_monitor/detector.py` implements threshold and time-window repetition detection
- Confirmed: The materialized file `materialized/src/repeated_log_monitor/alerts.py` implements console alert rendering and append-only alert persistence
- Confirmed: The materialized file `materialized/src/repeated_log_monitor/main.py` orchestrates configuration, monitoring, detection, and alert emission

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
- **OQ-1**: What exact rule determines that a log line is an error candidate and not just any line from the monitored files?
  parent_oq: NONE
  section_origin: Sección 3 del BETO_CORE_INTERVIEW
  status: CLOSED
  resolution: A line is treated as a candidate error event when it contains the textual marker `ERROR`.
  source: BETO_ASSISTED
- **OQ-2**: How should the system define sameness for a repeated error pattern when two lines differ in timestamps, IDs, or variable fragments?
  parent_oq: NONE
  section_origin: Sección 4 del BETO_CORE_INTERVIEW
  status: CLOSED
  resolution: Initial sameness is defined by literal comparison of the text that appears after the `ERROR` marker, without advanced normalization.
  source: BETO_ASSISTED
- **OQ-3**: What exact file path and serialization format should be used for the persisted alerts file?
  parent_oq: NONE
  section_origin: Sección 3 del BETO_CORE_INTERVIEW
  status: CLOSED
  resolution: The persisted alerts target is a local alerts file whose content is append-only plain text; the exact path remains configuration-driven within the local system boundary.
  source: BETO_ASSISTED
- **OQ-4**: How should the system behave when monitored log files rotate, are truncated, or new files appear inside the configured directory?
  parent_oq: NONE
  section_origin: Sección 7 del BETO_CORE_INTERVIEW
  status: CLOSED
  resolution: The system must continue monitoring the configured directory, detect new files that appear there, and reset local read position coherently when a monitored file is replaced or truncated.
  source: BETO_ASSISTED

Do NOT resolve open questions in this document.

BETO_GAP LOG:
Registrar aquí cada BETO_GAP detectado durante la ejecución del proceso.
Un BETO_GAP ocurre cuando el ejecutor detecta que algo necesario
no fue declarado en este BETO_CORE. Ver REGLA BETO_GAP en BETO_INSTRUCTIVO.

Formato de cada BETO_GAP:
- **BETO_GAP-1**: The system intent requires repeated pattern detection, but the normalization rule for determining whether two error lines represent the same pattern is not yet declared.
  fase_origen: Paso 1 del proceso BETO donde emergió
  derivable_del_intent: SÍ
  resolución: BETO_ASSISTED
  justificación: The example and the explicit simplicity constraint authorize an initial literal matching rule on the text after the `ERROR` marker without introducing advanced analysis.
  estado: RESOLVED

## 10. RISKS AND CONSTRAINTS

- The system is constrained to Linux environments
- The system is constrained to local text log files inside a configurable directory
- The system must remain lightweight and must not depend on heavy observability platforms
- The system must not rely on external services, email delivery, advanced analytics, or AI models
- If pattern equivalence is underspecified, repeated detections may be inconsistent with the operator's intended notion of the same error
- If logs do not use the textual marker `ERROR`, relevant failures may remain outside the declared detection rule
