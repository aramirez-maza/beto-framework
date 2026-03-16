# PHASE {{PHASE_NUM}} - {{PHASE_NAME}}

## 1. PURPOSE
Derived strictly from BETO_CORE Section 7.

Explain the phase purpose in 1–8 lines, adjusted to phase complexity.
The purpose must:
- Be traceable to the system intent
- Not introduce new objectives
- Not reinterpret previous phases

---

## 2. INPUT CONTRACT
Derived strictly from BETO_CORE Section 7 and BETO_CORE Sections 3–5.

Specify ONLY what is explicitly declared or unavoidable for this phase.

Include:
- Input source (previous phase, external source, manual input)
- Input format expectations (ONLY if explicitly stated in BETO_CORE)
- Mandatory fields or properties (ONLY if explicitly stated)
- Traceability requirements (IDs, lineage, provenance)

STRICT RULE:
- If any required input detail is missing or unclear, it MUST be declared as an unresolved dependency.
- If the dependency exists in BETO_CORE Section 9, reference it explicitly.
- If the dependency does NOT exist in BETO_CORE, mark it locally as:
  `Unresolved: <description>`
- Do NOT infer, assume, normalize, or invent input structure.
- Do NOT update BETO_CORE during phase generation.

---

## 3. OUTPUT CONTRACT
Derived strictly from BETO_CORE Section 7 and BETO_CORE Sections 3–5.

Specify ONLY guarantees required by this phase.

Include:
- Output artifact(s) produced by this phase
- Output format expectations (ONLY if explicitly stated in BETO_CORE)
- Output guarantees required by global invariants

STRICT RULE:
- If output format, structure, or guarantees are not explicitly stated, they MUST remain abstract.
- Any unresolved output definition MUST be deferred or marked as unresolved.
- Do NOT invent artifacts, formats, or guarantees.

---

## 4. PHASE RULES
Write 3–15 enforceable and testable rules specific to this phase,
adjusted to phase complexity.

Rules MUST:
- Be directly derived from BETO_CORE invariants or this phase’s purpose
- Be verifiable without external assumptions
- Not introduce new scope, features, or integrations
- Not contradict other phases or global constraints

Rules MUST NOT:
- Assume missing input structure
- Imply future phases’ responsibilities
- Encode implementation details

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
Define validation checks required to ensure correctness and invariants.

Include:
- Input validation checks (1–10 bullets, adjusted to complexity)
- Output validation checks (1–10 bullets)
- Failure handling policy (1–8 bullets)

Failure handling policy MUST:
- Define the default behavior for this phase (stop, continue, mark)
- Specify exceptions ONLY if explicitly required
- Be consistent with global invariants

STRICT RULE:
- Every validation MUST be justifiable from the Input Contract, Output Contract, or Global Invariants.
- If a validation cannot be justified, it MUST NOT be added.
- Do NOT introduce domain-generic or “best practice” validations.
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
List 3–20 edge cases relevant to this phase, adjusted to complexity.

Edge cases MUST:
- Be directly implied by declared inputs, outputs, or invariants
- Represent realistic boundary or failure conditions
- Be observable without speculative assumptions

STRICT RULE:
- Do NOT include speculative, generic, or domain-assumed edge cases.
- If an edge case depends on missing information, mark it as unresolved.

---

## 7. PROCESS STEPS (NO CODE)
Describe the logical flow of the phase as numbered steps (3–25 steps),
adjusted to phase complexity.

Rules:
- NO pseudocode
- NO implementation details
- NO technology references

Steps MUST:
- Respect the Input Contract
- Enforce Phase Rules
- Lead deterministically to the Output Contract
- Each step MUST declare which Output Contract element (Section 3) it contributes to.
  Format: [→ <output artifact or guarantee declared in Section 3>]
  A step with no linkable Output Contract element must be justified explicitly
  or removed. An unjustified unlinked step is a candidate BETO_GAP.

---

## 8. HANDOFF TO NEXT PHASE
Define what the next phase can safely assume after this phase completes.

Include 2–12 bullets describing:
- Guaranteed properties of the output
- What has been validated
- What remains unresolved and MUST NOT be assumed

STRICT RULE:
- Do NOT redefine the next phase’s purpose.
- Do NOT close Open Questions unless they were blocking this phase.

---

## 9. IMPLEMENTATION_CONTRACT STATUS
Declare whether this phase requires an IMPLEMENTATION_CONTRACT.

Allowed values:
- Required
- Not required

If `Required`, include:
- Reason for activation
- Reference to `IMPLEMENTATION_CONTRACT_<name>.md`
- Which structural ambiguity remains unresolved by this PHASE document alone

If `Not required`, include:
- Brief justification that this PHASE document is sufficient for materialization governance

STRICT RULE:
- Do NOT embed the implementation contract contents here.
- This section only records whether the extra layer is required for this phase.
- A simple system may mark every phase as `Not required`.

---

## END OF DOCUMENT
