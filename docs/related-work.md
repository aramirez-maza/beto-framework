# BETO and Related Work

This document positions BETO relative to existing approaches. It answers the question: *"What does BETO do that existing tools and practices don't?"*

The short answer is that existing approaches address adjacent problems — documentation, behavior, validation — but none operate as a structural constraint on what an LLM can generate during the specification and materialization process. BETO's contribution is not a better prompt or a smarter review step. It is a governance layer that operates at the point of generation.

---

## The Problem Space

BETO targets one specific failure mode: **silent completion** — an LLM filling underdetermined regions of a software specification with plausible content, without flagging that this content was not authorized by the operator. The consequences are:

- Specifications that do things nobody declared
- Data contracts with no traceable origin
- Code that cannot be audited from requirement to line
- Epistemic debt that compounds with every AI-assisted sprint

The key property of silent completion is that it is invisible. Standard review processes cannot reliably detect it because reviewers cannot distinguish between what was declared and what the model invented — that distinction was never recorded.

---

## Existing Approaches and Their Limits

### Prompt Engineering and Structured Prompting

Practices such as chain-of-thought prompting, system-level instructions, and structured output formats guide model behavior through natural language. They reduce the frequency of silent completion but provide no formal enforcement. If the model deviates, there is no detection mechanism — only hope that the reviewer notices. The boundary between declared and invented is not recorded; it is inferred by the reviewer after the fact.

**BETO's difference:** The boundary is structurally enforced and recorded before generation. An undeclared element cannot be materialized regardless of what the model produces.

### LangChain / LangGraph and Orchestration Frameworks

These frameworks govern the *flow* of LLM calls — routing, chaining, memory, and tool use. They solve the problem of multi-step LLM pipelines. They do not govern the *epistemic content* of what is generated within each step. An orchestrated pipeline can still silently complete specifications; it does so in a structured and repeatable way.

**BETO's difference:** BETO governs what the model is authorized to produce, not how calls are routed. It operates on the semantic content of specifications, not on the control flow between LLM calls.

### AI-Assisted Code Generation (Copilot, Cursor, and similar)

Code generation tools produce code from partial context. They do not have a specification governance layer — they complete from whatever context is available. The gap between what was intended and what was generated is the responsibility of the developer to detect through review.

**BETO's difference:** BETO does not replace code generation. It governs what is *authorized* before the code generator runs. The code motor in BETO_EXECUTOR receives a scaffold with pre-authorized BETO-TRACE IDs — it implements only what was declared, not what it infers from context.

### Architecture Decision Records (ADRs)

ADRs document decisions after they are made. They are a valuable practice for traceability but are applied post-hoc — the decision happened, and then it was written down. They do not prevent the generation of elements that were never decided. They also rely on engineer discipline to maintain: a missed ADR leaves no detectable trace.

**BETO's difference:** BETO enforces the recording of decisions *before* materialization. An element that was never declared cannot be materialized — there is no post-hoc recording required because the decision gate precedes the generation gate.

### OpenAPI and Contract Specifications

OpenAPI and similar standards define formal contracts for external interfaces. They govern the shape of inputs and outputs between services. They do not govern the internal design decisions that produce those interfaces, and they do not operate on the process by which an LLM generates the system that implements them.

**BETO's difference:** BETO governs the full specification and materialization pipeline — from raw idea through topology, through individual component specifications, to source code. External contracts are a downstream artifact of the BETO cycle, not its input.

### Test-Driven Development (TDD)

TDD validates behavior post-implementation. It is highly effective at catching implementation errors and at forcing clear interfaces. It does not prevent silent scope expansion during specification — a system can pass all its tests and still contain elements that were never declared by the operator, because those elements were never described in the test requirements either.

**BETO's difference:** BETO prevents scope expansion during specification, not during implementation. TDD and BETO are complementary: BETO governs what is authorized to exist; TDD validates that what was authorized was correctly implemented.

### Constitutional AI and Model-Level Constraints

Constitutional AI and similar alignment techniques establish behavioral constraints at the model training or inference level. They govern what a model will and will not produce in general. They cannot enforce domain-specific, project-specific epistemic rules — they operate on model-level behavior, not on the specific declaration space of a particular system.

**BETO's difference:** BETO operates above the model, not inside it. It works with any LLM that produces text. Its constraints are defined by the operator's declarations, not by model alignment.

### Model-Driven Engineering (MDE)

MDE provides formal model-to-code transformations from complete, formally specified models. It is rigorous and traceable — but it assumes the model is already complete and correct before transformation begins. It does not govern the process of creating that model, and it was not designed for the LLM-assisted context where the model is a participant in generating the specification.

**BETO's difference:** BETO governs the creation of the specification itself. It is a meta-protocol for the process that produces the artifact that MDE would then transform.

---

## Summary Positioning

| Approach | Governs generation? | Structural enforcement? | Records declared/undeclared boundary? |
|---|---|---|---|
| Prompt engineering | Behavioral only | No | No |
| LangChain / LangGraph | Control flow only | No | No |
| Code generation tools | No | No | No |
| ADRs | No (post-hoc) | No | Partially |
| OpenAPI | Interface only | No | No |
| TDD | Post-implementation | No | No |
| Constitutional AI | Model-level only | Behavioral | No |
| MDE | Post-specification | Yes (transformation) | No |
| **BETO** | **Yes — at point of generation** | **Yes — structural** | **Yes — full trace** |

---

## What BETO Does Not Claim

BETO does not claim to replace any of the above. Testing, architecture documentation, contract specifications, and code review remain necessary. BETO adds one thing that none of the above provide: a formal record of the boundary between what was declared by the operator and what was not — enforced structurally, before materialization, with every undeclared element either blocked or escalated.

The full academic treatment of BETO's relationship to related work is in the technical manuscript: [research/BETO_Framework_Technical_Article.md](../research/BETO_Framework_Technical_Article.md) (SSRN Abstract ID: 6411618).
