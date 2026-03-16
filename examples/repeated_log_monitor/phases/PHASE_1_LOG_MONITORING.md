# PHASE 1 - LOG MONITORING

## 1. PURPOSE
Continuously read text log files from the configured directory and surface candidate error events.
This phase exists to transform raw monitored log activity into traceable candidate events without modifying the source logs.
Its purpose is fully derived from BETO_CORE Section 7 and the system intent of lightweight local monitoring.

---

## 2. INPUT CONTRACT
- Input source: external source from the configured Linux directory containing text log files
- Input format expectations: text log lines; no stronger file structure is declared
- Mandatory fields or properties:
  - configured directory path
  - log line content
  - local alerts file path as declared system input
- Traceability requirements:
  - source log file path must be preserved
  - detection timestamp must be preserved
  - matched pattern string must remain derivable from the line

---

## 3. OUTPUT CONTRACT
- Output artifact produced: candidate error events
- Output format expectations:
  - abstract event stream of candidate log events
- Output guarantees required by global invariants:
  - each candidate event originates from a monitored file in the configured directory
  - source logs remain unmodified
  - each candidate event preserves source path and detection timestamp

---

## 4. PHASE RULES
- The phase only reads files inside the configured directory.
- The phase must not modify, truncate, rename, or delete monitored log files.
- A line becomes a candidate error event only if it contains the textual marker `ERROR`.
- The phase must preserve source file path for every candidate event.
- The phase must preserve detection timestamp for every candidate event.
- The phase must preserve enough raw content to derive the matched pattern string.
- This phase may not emit alerts directly.

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
- The configured directory path exists.
- The configured directory path is inside a Linux-accessible filesystem context.
- Monitored files are treated as text inputs only.

Output validation checks
- Every emitted candidate event originated from a file inside the configured directory.
- Every emitted candidate event contains a preserved source file path.
- Every emitted candidate event contains a preserved detection timestamp.

Failure handling policy
- If the configured directory cannot be read, stop this phase.
- If an individual file cannot be read, skip that file and continue monitoring others only if the system can still preserve invariants.
- If traceability fields cannot be preserved for an event, that event must not be emitted as a valid candidate.
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
- The configured directory exists but contains no log files.
- A monitored file exists but produces no new lines.
- A monitored line does not contain `ERROR`.
- A new file appears inside the configured directory during monitoring.
- A monitored file is replaced or truncated during monitoring.

---

## 7. PROCESS STEPS (NO CODE)
1. Read the configured directory path and enumerate monitorable text log files. [→ candidate error events]
2. Observe new lines emitted by files in the configured directory. [→ candidate error events]
3. For each observed line, determine whether it contains the textual marker `ERROR`. [→ candidate error events]
4. For each qualifying line, preserve source path and detection timestamp. [→ candidate error events]
5. Emit the resulting candidate error event stream to the next phase. [→ candidate error events]

---

## 8. HANDOFF TO NEXT PHASE
- The next phase can assume that each input event came from the configured directory.
- The next phase can assume that each input event is backed by a source file path.
- The next phase can assume that each input event is backed by a detection timestamp.
- The next phase can assume that only lines containing `ERROR` were promoted to candidate events.
- The next phase must not assume any normalization beyond literal text availability.

---

## END OF DOCUMENT
