# BETO Verification

This document explains what verification means in BETO, what it checks, what it does not check, and what can still go wrong after verification passes.

---

## Why Verification Exists in BETO

The core problem BETO addresses is silent completion: an LLM generating elements that were not authorized by the operator. Verification is the mechanism that closes the loop — it confirms that every element in a delivered artifact has a trace back to an operator-authorized decision.

Without verification, the BETO protocol produces governance artifacts but cannot confirm that the generated code actually respects the trace contract. Verification makes the traceability claim checkable, not just asserted.

---

## TRACE_VERIFIED

`TRACE_VERIFIED` is the status assigned to a source file after it passes the trace verification check. It means:

- Every BETO-TRACE annotation in the file references an ID that exists in the approved `TRACE_REGISTRY` for that node
- No BETO-TRACE annotation references an ID that was not authorized by the operator at G-3

A file that is `TRACE_VERIFIED` has a complete chain of custody:

```
Every annotated line
    → references a BETO-TRACE ID
    → that ID exists in the TRACE_REGISTRY
    → that TRACE_REGISTRY was approved by the operator at G-3
    → that approval references a BETO_CORE section
    → that section was approved at G-1 or G-2
    → that approval traces back to the original IDEA_RAW
```

`TRACE_VERIFIED` is a binary status. A file either passes or does not. There is no partial verification.

---

## Structural Invariants

The Executor enforces the following structural invariants at gates through 29 deterministic checks (read-only, no LLM):

**At G-1 (7 checks):**
- BETO_CORE_DRAFT contains a SYSTEM_INTENT section
- At least one DECLARED element is present
- Open Questions are registered with explicit NOT_STATED status
- No materialization directives appear before G-1 approval
- The IDEA_RAW is referenced
- The inference frontier is explicitly closed
- The document structure matches the BETO_CORE_TEMPLATE

**At G-2 (16 checks):**
- The BETO_SYSTEM_GRAPH contains exactly one ROOT node
- All non-ROOT nodes are classified as PARALLEL or SUBBETO
- No node appears in the graph that was not registered in the STRUCTURAL_CLASSIFICATION_REGISTRY
- All edges use authorized types (FUNCTIONAL_BRANCH, STRUCTURAL_REFINEMENT, DECLARED_DEPENDENCY)
- No node introduced after G-1 appears in the graph
- The graph status section is present and complete
- The "Ready to generate BETO_CORE children" field is explicitly YES
- The BETO_CORE_INTERVIEW_COMPLETED covers all 12 sections
- Open Questions from G-1 are accounted for (resolved or carried as NOT_STATED)
- Additional checks on section completeness and reference integrity

**At G-3 (6 checks):**
- MANIFEST_PROYECTO references every node from the approved BETO_SYSTEM_GRAPH
- Every TRACE_REGISTRY entry has a corresponding BETO_CORE section reference
- All Open Questions are in SUCCESS_CLOSED state or formally declared as known limits
- CIERRE_ASISTIDO is present and complete
- The materialization plan covers all authorized nodes
- No node appears in the manifest that was not in the approved graph

---

## Traceability Invariants

Beyond structural checks, BETO enforces traceability invariants throughout the cycle:

**Invariant 1 — Closed inference frontier.**
After G-1, no element may be introduced via `INFERRED` state. Every new element must be `DECLARED` (resolved Open Question) or `NOT_STATED` (confirmed unknown).

**Invariant 2 — Registry completeness.**
Every BETO-TRACE ID in a source file must have a pre-existing entry in the TRACE_REGISTRY. IDs cannot be invented in the code motor step.

**Invariant 3 — No undeclared nodes.**
No node may appear in Steps 5–10 that was not present in the G-2-approved BETO_SYSTEM_GRAPH. The graph topology is frozen at G-2.

**Invariant 4 — No resolved Open Question without operator attribution.**
A NOT_STATED element cannot transition to DECLARED without an explicit operator declaration. The cycle records which gate or CIERRE_ASISTIDO step produced the resolution.

---

## What Can Still Fail After Verification Passes

`TRACE_VERIFIED` does not mean the system is correct. The following failures remain possible even after a full BETO cycle with 100% trace verification:

**Incorrect operator declarations.**
If the operator declared a field with the wrong type, a constraint that is too permissive, or a behavior that does not match the actual requirement — BETO will produce a fully traceable, TRACE_VERIFIED system that implements the wrong thing correctly.

**Incomplete specifications.**
BETO ensures that what was declared is traceable. It does not ensure that what was declared is sufficient. A BETO_CORE that omits edge cases, error states, or boundary conditions will produce a TRACE_VERIFIED system that fails those cases at runtime.

**LLM implementation errors.**
The code motor generates code that implements the scaffold defined by BETO-TRACE IDs. The generated code may contain bugs, incorrect logic, or off-by-one errors that are functionally wrong while being structurally compliant with the trace contract.

**Conversational execution drift (Skill).**
In Skill execution, the model may miss steps, compress artifacts, or fail to register BETO_GAP events in long or complex cycles. The Skill does not run the 29-check structural validator. A TRACE_VERIFIED claim from a Skill-executed cycle requires the operator to have actively enforced gate compliance throughout the session.

**External dependency failures.**
BETO governs the specification and materialization of the system's own elements. It does not govern the behavior of external APIs, libraries, or services that the system depends on. A DECLARED dependency on an external service does not guarantee that service behaves as expected.

---

## Verifying a Delivered File Manually

To manually verify a source file against its TRACE_REGISTRY:

1. Locate the `TRACE_REGISTRY_<NODE>.md` file for the node that produced the source file
2. Extract all BETO-TRACE IDs from the source file (pattern: `BETO-TRACE: <ID>`)
3. Confirm that each extracted ID appears in the TRACE_REGISTRY
4. Confirm that no ID in the source file is absent from the TRACE_REGISTRY

Any ID present in the source file but absent from the TRACE_REGISTRY is an unauthorized element. The file is not TRACE_VERIFIED.

See a complete verified example: [examples/gastos_personales/](../examples/gastos_personales/)
