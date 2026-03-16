# PHASE 2 - REPETITION DETECTION

## 1. PURPOSE
Group candidate error events by repeated pattern and evaluate whether the configured threshold N is exceeded within the configured time window.
This phase exists to transform candidate events into repeated pattern detections without introducing advanced analytics or normalization outside the declared rule.

---

## 2. INPUT CONTRACT
- Input source: previous phase output plus declared configuration values
- Input format expectations:
  - candidate error events
  - configured threshold N
  - configured time window
- Mandatory fields or properties:
  - raw log line content
  - detection timestamp
  - derivable pattern string from text after `ERROR`
- Traceability requirements:
  - preserve source lineage from the monitored file
  - preserve detection timestamps used in the count
  - preserve the matched pattern string used for grouping

---

## 3. OUTPUT CONTRACT
- Output artifact produced: repeated pattern detections
- Output format expectations:
  - abstract repeated-detection result tied to one matched pattern
- Output guarantees required by global invariants:
  - each detection is tied to a literal matched pattern
  - each detection is justified by a count greater than or equal to N inside the declared time window
  - each detection preserves traceability to its observed events

---

## 4. PHASE RULES
- Pattern equality is determined by literal comparison of the text after the `ERROR` marker.
- The phase only counts candidate events received from Phase 1.
- The phase only evaluates counts against the configured threshold N.
- The phase only evaluates counts inside the configured time window.
- The phase must not apply advanced normalization, analytics, or machine learning.
- The phase must preserve the matched pattern string used to justify the detection.
- This phase may not write the alerts file directly.

REGLA DE FASE — NO-INICIATIVA:
Esta fase no puede producir outputs no declarados en la
Sección 3 (Output Contract) de este documento.
La iniciativa del ejecutor para proponer o expandir
outputs fue válida únicamente en el Paso 0 (PROMPT_CANONICO).
Si durante la ejecución de esta fase emerge la necesidad
de un output no declarado → registrar como BETO_GAP
y aplicar la REGLA BETO_GAP del BETO_INSTRUCTIVO.
No producir. No asumir autorización implícita.
Lo no declarado en el Output Contract no existe para esta fase.

REGLA DE FASE — TRACE_REGISTRY:
Cada construct de código producido por esta fase debe tener
una anotación BETO-TRACE inmediatamente anterior que declare
un ID registrado en el TRACE_REGISTRY del BETO_CORE
que define esta fase.
El ID debe referenciar la sección y el elemento específico
del BETO_CORE que autoriza la existencia de ese construct.
No es válido referenciar el ID de otra fase o de otro BETO_CORE
como autorización para un construct de esta fase.
Un construct sin ID registrado es un construct no autorizado.

---

## 5. VALIDATIONS
Input validation checks
- Threshold N is available as a configured value.
- The time window is available as a configured value.
- Each candidate event has a detection timestamp.
- Each candidate event has derivable text after `ERROR`.

Output validation checks
- Each repeated pattern detection is associated with one literal matched pattern.
- Each repeated pattern detection is backed by a count that meets or exceeds N.
- Each repeated pattern detection is backed by events occurring inside the configured time window.

Failure handling policy
- If threshold N is missing, stop this phase.
- If the time window is missing, stop this phase.
- If an event lacks the data needed for literal comparison, do not count it as a valid repeated detection input.
- TRACE_REGISTRY CHECK: Para cada construct en el output,
  verificar que su ID de BETO-TRACE existe en el
  TRACE_REGISTRY de este BETO_CORE.
  Si el ID no existe → BETO_GAP [ESCALADO] obligatorio.
  Si el ID existe pero corresponde a otra sección →
    BETO_WARNING emitido, construct marcado como WARNED.
  Si todos los IDs están verificados →
    archivo con estado TRACE_VERIFIED.

---

## 6. EDGE CASES
- The same pattern appears fewer than N times inside the window.
- The same pattern appears N times but across a period longer than the configured window.
- Two lines share `ERROR` but differ in the text after the marker.
- A candidate event arrives without enough post-`ERROR` text to derive a pattern string.
- Events from different source files produce the same literal pattern string.

---

## 7. PROCESS STEPS (NO CODE)
1. Receive candidate error events together with threshold N and the configured time window. [→ repeated pattern detections]
2. Derive the matched pattern string from the literal text after `ERROR` for each event. [→ repeated pattern detections]
3. Group events by matched pattern string. [→ repeated pattern detections]
4. Count occurrences per pattern inside the configured time window. [→ repeated pattern detections]
5. Emit a repeated pattern detection only for patterns meeting or exceeding threshold N. [→ repeated pattern detections]

---

## 8. HANDOFF TO NEXT PHASE
- The next phase can assume that each detection refers to one literal matched pattern.
- The next phase can assume that each detection met the configured threshold N.
- The next phase can assume that each detection occurred within the configured time window.
- The next phase can assume that detections preserve event lineage and timestamps.
- The next phase must not assume any advanced classification beyond literal repetition.

---

## END OF DOCUMENT
