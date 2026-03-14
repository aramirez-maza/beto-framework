# BETO Claims and Boundaries

This document defines precisely what BETO guarantees, what it does not, and what the word "formal" means in this context. Read this before citing BETO's properties in any technical or evaluative context.

---

## What BETO Means by "Formal"

BETO uses the word "formal" in a specific, bounded sense. It does **not** mean:

- Mathematical proof of software correctness
- Formal verification in the tradition of TLA+, Coq, or Isabelle
- Static analysis guarantees over generated code
- Completeness proof that no element was missed

BETO means **structural formalization of the authorized design universe**:

- Every element that enters the materialization pipeline has an explicit authorization trace
- Every element that was not authorized is either blocked (registered as an Open Question) or escalated to the operator as a BETO_GAP event
- The boundary between *declared by the operator* and *invented by the model* is made structurally explicit and recorded

"Formal" in BETO is a claim about **traceability and governance process**, not about logical completeness or runtime correctness.

---

## What BETO Guarantees

The following claims are directly sustained by the protocol design and the empirical record:

**1. No silent completion.**
Every element that a BETO cycle materializes is traceable to an operator-authorized specification decision. If an element cannot be traced to a DECLARED state in an approved BETO_CORE, it cannot be materialized.

**2. Every undeclared element becomes a registered event.**
An element in `NOT_STATED` state does not disappear or get silently resolved. It becomes a blocking Open Question that must be resolved by the operator before the cycle proceeds.

**3. Human gates are non-bypassable.**
G-1, G-2, and G-3 are structural halts. The cycle cannot proceed without explicit operator approval at each gate. The operator's decision is the authority — not the model's judgment.

**4. The TRACE_REGISTRY is the materialization contract.**
A source file whose BETO-TRACE annotations reference IDs not in the approved TRACE_REGISTRY is unauthorized and cannot be delivered. This is enforced by the verification step, not by convention.

**5. The empirical record is verifiable.**
Three systems have been fully specified and materialized under BETO v4.2: 43 source files, 100% TRACE_VERIFIED, 0 silent completions. The artifacts are in this repository and can be independently inspected.

---

## What BETO Does Not Guarantee

**1. Correctness of the operator's declarations.**
BETO governs the *process* by which decisions are made and recorded. It does not evaluate whether the operator's declarations are correct, complete, or wise. A poorly specified system produced under BETO is still a poorly specified system — it is just transparently poorly specified.

**2. Correctness of LLM-generated code.**
BETO guarantees traceability of what was authorized, not correctness of the implementation. Generated code may contain bugs, edge cases, or incorrect logic — the TRACE_VERIFIED status confirms authorization, not functional correctness.

**3. Mathematical or logical completeness.**
BETO does not claim that the set of DECLARED elements in a BETO_CORE is the complete and necessary set for a correct system. Completeness is the operator's responsibility. BETO ensures that whatever is declared is traceable, and whatever is not declared is blocked.

**4. Equivalent guarantees across all execution modes.**
The Executor (reference implementation) includes 29 deterministic structural checks at each gate that run without LLM involvement. The Skill (Claude integration path) executes the protocol conversationally and does not include this validator. Conversational execution can drift if the session is long or if the operator does not enforce the gate structure. BETO Protocol compliance in Skill execution depends on the discipline of the operator and the session continuity of the model.

**5. Adoption or community validation.**
BETO v4.2 was made public in March 2026. There is no external adoption record at this time beyond the three cycles produced by its author. The framework is field-tested in its development environment, not yet in external production.

---

## Why This Distinction Matters

The most common misreading of BETO is to treat it as a correctness framework: "if I use BETO, my software is correct." That is not the claim.

BETO is an **accountability framework**: "if I use BETO, I know exactly what was decided, who decided it, and what was deliberately left undecided."

This distinction matters because:

- A system can be fully TRACE_VERIFIED and still fail in production due to incorrect operator decisions
- A system can pass all BETO gates and still have incomplete specifications for edge cases
- BETO does not replace testing, code review, or domain expertise — it makes the specification process auditable so those activities have a clear baseline

The value of BETO is not that it makes software correct. The value is that it makes the gap between intent and implementation visible, traceable, and attributed.

---

## The Formal Claim, Precisely Stated

> A system specified under BETO cannot contain an element that was not either (a) explicitly declared by the operator, or (b) formally registered as unknown and blocking — with the operator notified.

This claim holds when:
- The full 11-step protocol is executed without gate bypass
- Open Questions are not dismissed without resolution
- BETO-TRACE annotations in source files are verified against the approved TRACE_REGISTRY before delivery

This claim is **not** about what the operator declared being correct. It is about the boundary between declared and undeclared being structurally enforced and recorded.
