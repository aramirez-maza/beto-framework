# PHASE 3 - ALERT EMISSION

## 1. PURPOSE
Emit a local console alert and persist the alert event to a local alerts file whenever a repeated pattern detection is received.
This phase exists to make recurrent errors locally visible and durable without external integrations.

---

## 2. INPUT CONTRACT
- Input source: previous phase output
- Input format expectations:
  - repeated pattern detections
- Mandatory fields or properties:
  - matched pattern string
  - count satisfying threshold N
  - configured time window context
  - local alerts file path
- Traceability requirements:
  - preserve the matched pattern string in the emitted alert
  - preserve count and time window context
  - preserve enough linkage to source detections for auditability

---

## 3. OUTPUT CONTRACT
- Output artifacts produced:
  - local console alert
  - persisted alert event in the local alerts file
- Output format expectations:
  - console alert is local
  - alerts file is append-only plain text
- Output guarantees required by global invariants:
  - each persisted alert corresponds to one repeated pattern detection
  - persisted alerts do not require external services
  - alerts preserve pattern, count, and time-window context

---

## 4. PHASE RULES
- The phase only consumes repeated pattern detections produced by Phase 2.
- The phase must emit a local console alert for each valid repeated pattern detection.
- The phase must append each valid repeated pattern detection to the local alerts file.
- The phase must not send email or contact external services.
- The phase must preserve the matched pattern, count, and time-window context in the alert output.
- The phase must not modify monitored log files.

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
- Each repeated pattern detection includes a matched pattern string.
- Each repeated pattern detection includes a count meeting threshold N.
- The local alerts file path is available for persistence.

Output validation checks
- A console alert is emitted locally for each valid repeated pattern detection.
- A corresponding persisted alert event is appended to the local alerts file.
- The persisted alert carries pattern, count, and time-window context.

Failure handling policy
- If console emission fails, mark the alert attempt as failed for this phase.
- If the local alerts file cannot be written, stop delivery of the persisted alert output.
- If required alert context is missing, do not emit a valid alert.
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
- The same repeated detection is emitted more than once in close succession.
- The alerts file path exists but is not writable.
- The alerts file path does not yet exist.
- A detection includes a pattern and count but lacks usable time-window context.
- Console output is available but file persistence fails.

---

## 7. PROCESS STEPS (NO CODE)
1. Receive one repeated pattern detection from Phase 2. [→ local console alert]
2. Build the local alert content using the matched pattern, count, and time-window context. [→ local console alert]
3. Emit the alert locally in console. [→ local console alert]
4. Append the alert event to the local alerts file as plain text. [→ persisted alert event in the local alerts file]
5. Preserve linkage between the persisted alert and the repeated pattern detection that originated it. [→ persisted alert event in the local alerts file]

---

## 8. HANDOFF TO NEXT PHASE
- No subsequent phase is declared in BETO_CORE Section 7.
- Downstream materialization can assume that alert outputs are local only.
- Downstream materialization can assume that persisted alerts are append-only plain text.
- Downstream materialization must not assume external delivery channels.

---

## END OF DOCUMENT
