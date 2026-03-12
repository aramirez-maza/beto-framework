# BETO Framework

> **BETO formalizes the ignorance of an AI.**

BETO is an epistemic governance protocol for LLM-assisted software specification and materialization. It enforces a formal boundary between what the operator has declared and what the model has assumed — preventing the silent completion problem that makes AI-generated software unauditable.

**Version:** 4.2 (March 2026)
**Author:** Alberto Ramírez

---

## The Problem

When you ask a Large Language Model to design or build a software system, it does not acknowledge what it does not know. It *completes* — inventing fields because they seem reasonable, assuming architectures because they are conventional, generating code that handles the average case but was never authorized by you.

This is not a model defect. Completion is the core function of LLMs. The defect is architectural: modern development workflows have no formal mechanism to distinguish **what you declared** from **what the model invented**. The result is:

- Specifications that do things nobody asked for
- Data contracts with no traceable origin
- Code that cannot be audited from requirement to line
- Epistemic debt that compounds with every AI-assisted sprint

BETO solves this at the point of generation — not after.

---

## What BETO Is

BETO is a complete, formally specified 11-step protocol that governs every phase of LLM-assisted software development, from initial idea to delivered, traceable code.

It introduces three core mechanisms:

### 1. Epistemic States
Every element of a system carries one of three states:

| State | Meaning | Effect |
|---|---|---|
| `DECLARED` | Explicitly defined by the operator | Enables execution |
| `NOT_STATED` | Not declared; cannot be inferred | Blocks execution — registered as Open Question |
| `INFERRED` | Derived by the model | Authorized only in Steps 0–1. Prohibited after first operator approval |

An element in `NOT_STATED` cannot be materialized. It must be declared by the operator — or formally registered as a known limit of the system.

### 2. BETO_GAP Protocol
When the executor encounters an element that would require unauthorized inference, it triggers a `BETO_GAP`:

- **Derivable from System Intent** → `BETO_GAP [RESOLVED: BETO_ASSISTED]` — logged, justified, continues
- **Not derivable** → `BETO_GAP [ESCALATED]` — mandatory halt, operator must decide

There is no silent resolution. Every undeclared element becomes a traceable event.

### 3. TRACE_REGISTRY + BETO-TRACE Annotations
Every specification generates a `TRACE_REGISTRY`: a catalogue of authorized traceability IDs in the pattern:

```
SYSTEM_NAME.SEC<N>.<TYPE>.<ELEMENT>
```

Every line of generated code is annotated with a `BETO-TRACE` ID drawn from this registry. An ID not in the registry is unauthorized — the file cannot be delivered.

This creates a complete chain of custody:

```
Source code line
    → BETO-TRACE annotation
    → TRACE_REGISTRY entry
    → BETO_CORE section
    → Operator gate decision
    → Original intent
```

---

## The 11-Step Process

| Step | Artifact | Purpose |
|---|---|---|
| 0 | `PASO_0_EVALUACION.md` | Semantic eligibility — is the idea viable without invention? |
| 1 | `BETO_CORE_DRAFT.md` | Root specification — bounded inference frontier |
| 2 | `BETO_CORE_INTERVIEW_COMPLETED.md` | 12-section structural interview to close Open Questions |
| 3 | `STRUCTURAL_CLASSIFICATION_REGISTRY.md` | Formal classification: PARALLEL vs SUBBETO |
| 4 | `BETO_SYSTEM_GRAPH.md` | Topology freeze — 9 validations, operator approval required |
| 5 | BETO_CORE children | One spec per authorized node |
| 6 | `CIERRE_ASISTIDO.md` | Assisted closure — all OQs resolved to SUCCESS_CLOSED |
| 7 | `PHASE_*.md` | Phase documents per node |
| 8 | `MANIFEST_*.md` + `TRACE_REGISTRY_*.md` | Inventories and authorized ID catalogues |
| 9 | `MANIFEST_PROYECTO.md` | Complete project manifest |
| 10 | Source files | LLM-generated code with BETO-TRACE annotations, verified |
| 11 | `FRAMEWORK_FEEDBACK.md` + `OPERATIONAL_LESSONS.md` | Formal learning snapshot after first production operation |

Three **human gates** (G-1, G-2, G-3) give the operator full authority over topology before expansion, specification before materialization, and manifest before code generation. Gates are non-bypassable. The operator's decision is final.

---

## Node Taxonomy

BETO organizes system components into three formal node types:

**ROOT** — The single structural trunk. Generated from the IDEA_RAW. Exactly one per system.

**PARALLEL** — Born from functional independence. Can be specified using only external contracts. Developed by an independent team without knowledge of other nodes' internals.

**SUBBETO** — Born from structural ambiguity. Requires knowledge of its parent's internal structure to be specified correctly.

The classification is enforced through a formal **semantic independence test** — not a judgment call.

---

## Repository Structure

```
beto-framework/
│
├── README.md                          ← This file
├── DOCUMENTACION_OFICIAL_BETO.md      ← Complete official documentation
├── BETO_INSTRUCTIVO.md                ← Operational protocol (11 steps + 11 rules)
│
├── framework/                         ← All 12 formal templates
│   ├── BETO_CORE_TEMPLATE.md
│   ├── BETO_CORE_INTERVIEW.md
│   ├── BETO_SYSTEM_GRAPH_TEMPLATE.md
│   ├── PHASE_TEMPLATE.md
│   ├── MANIFEST_BETO_TEMPLATE.md
│   ├── MANIFEST_PROYECTO_TEMPLATE.md
│   ├── FRAMEWORK_FEEDBACK_TEMPLATE.md
│   ├── OPERATIONAL_LESSONS_TEMPLATE.md
│   ├── GENERATOR_RULES_TEMPLATE.md
│   └── PROMPT_CANONICO_DE_ELICITACION.md
│
├── beto_executor/                     ← Automated implementation of BETO
│   └── src/                           ← Python source code
│       ├── main.py                    ← CLI entry point
│       ├── orquestador/               ← Full cycle orchestration
│       ├── motor_razonamiento/        ← Steps 0–9 (reasoning motor)
│       ├── motor_codigo/              ← Step 10 (code generation motor)
│       ├── gates_operador/            ← Human gate interaction + structural validation
│       ├── gestor_ciclo/              ← Cycle state management
│       └── beto_state/                ← Live epistemic context engine
│
├── research/
│   └── BETO_Framework_Technical_Article.md   ← Technical article (manuscript)
│
└── examples/
    └── beto_executor_self_specification/      ← Complete cycle: BETO specifying itself
        ├── PASO_0_EVALUACION.md
        ├── BETO_CORE_DRAFT.md
        ├── BETO_SYSTEM_GRAPH.md
        ├── CIERRE_ASISTIDO.md
        ├── MANIFEST_PROYECTO.md
        └── GENERATOR_RULES_BETO_EXECUTOR.md
```

---

## BETO_EXECUTOR

`beto_executor/` is the automated pipeline that runs the complete BETO Framework using two LLM backends:

- **Reasoning motor** — Steps 0–9: Calls an OpenAI-compatible API (tested with Claude Sonnet)
- **Code motor** — Step 10: Calls a local code model (tested with Qwen-Coder via vLLM)

Key engineering decisions:
- **Two-call generation** for large documents (Steps 2 and 4) to guarantee tail sections are never truncated
- **Scaffold-based code generation**: system builds a Python scaffold with BETO-TRACE IDs; the code model implements the module while preserving the trace contract
- **BETO_STATE engine**: a live JSON document injected as the first message in each LLM call, providing compact epistemic context without full artifact injection (~60–70% context reduction in multi-node cycles)
- **Deterministic structural validation** at each gate: 29 checks, no LLM, read-only

### Running BETO_EXECUTOR

```bash
# Requirements: Python 3.11+, OpenAI-compatible API, optional local code model
cd beto_executor/src
pip install openai

# Set your API endpoint and key
export OPENAI_API_BASE="http://localhost:8000/v1"   # or your API endpoint
export OPENAI_API_KEY="your-key"

python main.py "Your idea here"
```

The executor will run the full specification pipeline, pausing at each human gate for your approval.

---

## Empirical Results

Three systems have been fully specified and materialized under BETO v4.2:

| System | Nodes | Source Files | TRACE_VERIFIED | Silent Completions |
|---|---|---|---|---|
| Dev Assistant | 6 | 11 | 11/11 (100%) | 0 |
| BETO Artifact Evaluator | 11 | 18 | 18/18 (100%) | 0 |
| BETO_EXECUTOR (self) | 5 | 14 | 14/14 (100%) | 0 |

Every generated element in all three systems is traceable to an operator-authorized specification decision. No element was silently completed.

---

## The Formal Claim

BETO makes one formal claim:

> A system specified under BETO cannot contain an element that was not either (a) explicitly declared by the operator, or (b) formally registered as unknown and blocking — with the operator notified.

This is enforced structurally, not through prompt engineering or model compliance. It is guaranteed by the protocol, not by the model's behavior.

---

## Status and Roadmap

**Current:** BETO v4.2 — stable, field-tested, private repository

**Planned:**
- [ ] Public release and open-source launch
- [ ] Academic publication (manuscript in `research/`)
- [ ] Multilingual support (language-aware artifact generation)
- [ ] BETO_INTAKE: multimodal admission layer (diagrams, audio, documents → IDEA_RAW)

---

## License

MIT License — Copyright (c) 2026 Alberto Ramírez

Free to use, copy, modify, and distribute — with one requirement:
**the copyright notice and author attribution must be preserved in all copies.**

See [LICENSE](LICENSE) for full terms.

---

## Author

**Alberto Ramírez**
Creator and sole implementer of the BETO Framework
Four years of development: 2022–2026

*"BETO formalizes the ignorance of an AI."*
