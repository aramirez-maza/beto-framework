# BETO Architecture

BETO has three components with distinct scopes. Understanding the separation matters before reading the technical detail.

---

## The Three Layers

### BETO Protocol

The governance rules. Eleven steps, three human gates, formal epistemic states, and two key mechanisms (BETO_GAP and TRACE_REGISTRY). This is the core of the framework — a specification of *how* LLM-assisted software development must proceed to produce auditable output. It can be executed manually, via the Executor, or via the Skill.

### BETO Executor

The reference implementation of the Protocol. An automated Python pipeline with two LLM backends: a reasoning motor for Steps 0–9 (specification pipeline) and a code motor for Step 10 (materialization). The Executor adds deterministic structural validation at each gate — 29 checks without LLM involvement — and a BETO_STATE engine that maintains compact epistemic context across the cycle.

### BETO Skill

A Claude integration path that runs the Protocol conversationally in Claude Code or Claude.ai. No infrastructure required. The Skill loads all BETO templates on demand from `skills/beto-framework/references/`. Human gate behavior is preserved: the Skill pauses at G-1, G-2, and G-3 and waits for operator approval.

The Skill reduces entry friction but does not include the deterministic structural validator of the Executor.

---

## The Protocol: 11 Steps

| Step | Artifact | Gate | Purpose |
|---|---|---|---|
| 0 | `PASO_0_EVALUACION.md` | — | Semantic eligibility — is the idea viable without invention? |
| 1 | `BETO_CORE_DRAFT.md` | **G-1** | Root specification — bounded inference frontier |
| 2 | `BETO_CORE_INTERVIEW_COMPLETED.md` | — | 12-section structural interview to close Open Questions |
| 3 | `STRUCTURAL_CLASSIFICATION_REGISTRY.md` | — | Formal node classification: PARALLEL vs SUBBETO |
| 4 | `BETO_SYSTEM_GRAPH.md` | **G-2** | Topology freeze — 9 validations, operator approval required |
| 5 | BETO_CORE children | — | One specification per authorized node |
| 6 | `CIERRE_ASISTIDO.md` | — | Assisted closure — all Open Questions resolved to SUCCESS_CLOSED |
| 7 | `PHASE_*.md` | — | Phase documents per node |
| 8 | `MANIFEST_*.md` + `TRACE_REGISTRY_*.md` | — | Inventories and authorized ID catalogues |
| 9 | `MANIFEST_PROYECTO.md` | **G-3** | Complete project manifest |
| 10 | Source files | — | LLM-generated code with BETO-TRACE annotations, verified |
| 11 | `FRAMEWORK_FEEDBACK.md` + `OPERATIONAL_LESSONS.md` | — | Formal learning snapshot after first production operation |

---

## Epistemic States

Every element of a system carries exactly one state at any point in the cycle:

| State | Meaning | Effect |
|---|---|---|
| `DECLARED` | Explicitly defined by the operator | Enables execution |
| `NOT_STATED` | Not declared; cannot be inferred | Blocks execution — registered as Open Question |
| `INFERRED` | Derived by the model from context | Authorized only in Steps 0–1. Prohibited after G-1 |

`INFERRED` is not permanent. It must convert to `DECLARED` (operator confirms) or `NOT_STATED` (operator rejects) before the cycle proceeds past G-1. After G-1, the only authorized states are `DECLARED` and `NOT_STATED`.

---

## BETO_GAP Protocol

When the executor encounters an element that would require unauthorized inference, it triggers a `BETO_GAP`. There are exactly two outcomes:

- **`BETO_GAP [RESOLVED: BETO_ASSISTED]`** — The gap is derivable from the declared System Intent. The executor resolves it, logs the justification, and continues.
- **`BETO_GAP [ESCALATED]`** — The gap cannot be resolved without new operator input. Execution halts. The operator must decide.

There is no third outcome. Every undeclared element becomes a traceable event.

---

## TRACE_REGISTRY and BETO-TRACE

Every specification cycle produces a `TRACE_REGISTRY`: a catalogue of authorized traceability IDs in the pattern:

```
SYSTEM_NAME.SEC<N>.<TYPE>.<ELEMENT>
```

Every line of generated code is annotated with a `BETO-TRACE` ID drawn from this registry. An ID not in the registry is unauthorized — the file cannot be delivered.

This creates a complete chain of custody:

```
Source code line
    → BETO-TRACE annotation
    → TRACE_REGISTRY entry
    → BETO_CORE specification section
    → Operator gate decision
    → Original intent
```

---

## Human Gates

Three gates give the operator full authority at critical decision points. Gates are non-bypassable. The operator's decision is final.

**G-1** (after Step 1) — Approves the root specification. Closes the inference frontier. After G-1, no new inference is permitted.

**G-2** (after Step 4) — Approves the system topology. Freezes the node structure before individual specifications are generated. No node can appear in Steps 5–10 that was not authorized here.

**G-3** (after Step 9) — Approves the complete project manifest before code generation. Every TRACE_REGISTRY ID that will appear in source files must be present in the approved manifest.

---

## Node Taxonomy

BETO organizes system components into three formal node types:

**ROOT** — The single structural trunk. Generated from the IDEA_RAW. Exactly one per system. Defines System Intent, boundaries, invariants, and capability map.

**PARALLEL** — Born from functional independence. Can be specified using only external contracts — without knowledge of other nodes' internals. Suitable for independent development.

**SUBBETO** — Born from structural ambiguity. Requires knowledge of its parent's internal structure to be correctly specified. Represents vertical decomposition.

The classification is enforced through a formal semantic independence test: *Can this component's specification be written knowing only its external contracts, without looking inside any other component?* Yes → PARALLEL. No → SUBBETO.

---

## BETO_STATE Engine (Executor)

The Executor maintains a live epistemic context document — `BETO_STATE.json` — updated after each step. It is injected as the first message in each LLM call from Step 2 onward.

BETO_STATE captures: system intent, declared boundaries, STDs, Open Questions (all states), node classifications, gate decisions, and BETO_GAP events.

This produces a 60–70% reduction in context size compared to injecting full artifacts in multi-node cycles, without losing the epistemic continuity needed for correct specification.

---

## Executor Architecture

```
src/
├── main.py                          ← CLI entry point
├── orquestador/root.py              ← Full cycle orchestration
├── motor_razonamiento/
│   ├── motor.py                     ← Steps 0–9 loop
│   ├── step_executor.py             ← LLM calls (split-call for Steps 2 and 4)
│   └── context_builder.py          ← BETO_STATE + templates + artifacts per step
├── motor_codigo/                    ← Step 10: scaffold + code generation
├── gates_operador/
│   ├── gates.py                     ← Full gate cycle
│   └── artifact_validator.py       ← 29 deterministic checks, no LLM, read-only
├── gestor_ciclo/state_reader.py     ← Resume from paso_actual
└── beto_state/                      ← Schema, extractor, writer
```

Key architectural decisions:

- **Split-call generation** for Steps 2 and 4: large documents are generated in two calls to guarantee tail sections are never truncated
- **Scaffold-based code generation**: the system builds a Python scaffold with BETO-TRACE IDs; the code motor implements each module while preserving the trace contract
- **Deterministic structural validation**: 29 checks at gates, no LLM involvement, read-only — the validator never triggers regeneration
- **Anti-loop rule**: gate rejection requires manual operator action; the Executor never auto-retries
