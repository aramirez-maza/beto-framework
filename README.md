# BETO Framework

> **BETO formalizes the ignorance of an AI.**

BETO is an epistemic governance protocol for LLM-assisted software specification and materialization. It enforces a formal boundary between what the operator has declared and what the model has assumed — preventing the silent completion problem that makes AI-generated software unauditable.

**Version:** 4.2 (March 2026) · **Author:** Alberto Ramírez · **License:** MIT

---

## Why BETO Exists

When you ask an LLM to design or build a software system, it does not acknowledge what it does not know. It *completes* — inventing fields because they seem reasonable, assuming architectures because they are conventional, generating code that handles the average case but was never authorized by you.

This is not a model defect. Completion is the core function of LLMs. The defect is architectural: there is no formal mechanism to distinguish **what you declared** from **what the model invented**. The result is specifications that do things nobody asked for, data contracts with no traceable origin, and code that cannot be audited from requirement to line.

BETO converts that gap into a traceable event — not after the fact, but at the point of generation.

---

## Core Idea

Every element of a system carries one of three epistemic states:

| State | Meaning | Effect |
|---|---|---|
| `DECLARED` | Explicitly defined by the operator | Enables execution |
| `NOT_STATED` | Not declared; cannot be inferred | Blocks execution — registered as Open Question |
| `INFERRED` | Derived by the model | Authorized only in Steps 0–1. Prohibited after first operator approval |

An element in `NOT_STATED` cannot be materialized. It must be declared by the operator — or formally registered as a known limit of the system. There is no silent resolution.

---

## What BETO Includes

BETO has three components with distinct purposes:

**BETO Protocol** — The 11-step governance process, from raw idea to traceable code. Defines the epistemic rules, the BETO_GAP event protocol, the TRACE_REGISTRY mechanism, and the three human gates (G-1, G-2, G-3) that give the operator full authority over topology, specification, and materialization. This is the core of the framework — the others implement it.

**BETO Executor** — An automated Python pipeline that runs the full BETO Protocol using two LLM backends: a reasoning motor (Steps 0–9, tested with Claude Sonnet) and a code motor (Step 10, tested with Qwen-Coder via vLLM). Requires Python 3.11+, an OpenAI-compatible API, and optionally a local code model.

**BETO Skill** — A Claude Skill that runs the complete BETO Protocol interactively in Claude Code or Claude.ai with no infrastructure required. The lowest-friction entry point to BETO.

---

## How to Use BETO

The three components are independent — you can use any of them alone. But they work best in sequence:

```
IDEA_RAW
  → BETO Skill      — explore the protocol conversationally,
                       mature the idea, discover Open Questions
                       before they become blockers
  → BETO Executor   — materialize with deterministic guarantees,
                       structural validation, and full TRACE_VERIFIED delivery
```

The Skill is not a prerequisite for the Executor. But users who run the Skill first arrive at the Executor with a clearer idea, fewer surprises at the gates, and a schema already thought through.

Both execute the same protocol. The difference is the execution environment.

## Quickstart

BETO Protocol can be executed manually, via the Executor (the reference implementation), or via the Skill (a Claude integration). See the full guide for both automated paths:

→ **[docs/quickstart.md](docs/quickstart.md)**

---

## What BETO Guarantees

- Every element in a delivered system is traceable to an operator-authorized specification decision
- Every undeclared element becomes a registered, blocking event — not a silent assumption
- No code is generated for elements in `NOT_STATED` state
- Every human gate decision is recorded and non-bypassable
- The three empirical cycles produced 43 source files with 100% TRACE_VERIFIED delivery and zero silent completions

---

## What BETO Does Not Guarantee

- Correctness of the operator's declarations — BETO governs the *process*, not the *quality* of the decisions
- Mathematical proof of software correctness — "formal" in BETO means structural formalization of the authorized design universe, not formal verification in the PL/TLA+ sense
- That conversational execution (Skill) provides the same deterministic guarantees as the automated pipeline (Executor)

→ Full bounds: **[docs/claims-and-boundaries.md](docs/claims-and-boundaries.md)**

---

## Documentation

| Document | Purpose |
|---|---|
| [docs/quickstart.md](docs/quickstart.md) | Minimum reproducible path to run BETO |
| [docs/architecture.md](docs/architecture.md) | The three layers, 11-step cycle, key concepts |
| [docs/claims-and-boundaries.md](docs/claims-and-boundaries.md) | What "formal" means in BETO; guarantees and limits |
| [docs/verification.md](docs/verification.md) | TRACE_VERIFIED, structural invariants, failure modes |
| [docs/faq.md](docs/faq.md) | Three questions every engineer asks first |
| [docs/related-work.md](docs/related-work.md) | How BETO relates to existing tools and practices |
| [DOCUMENTACION_OFICIAL_BETO.md](DOCUMENTACION_OFICIAL_BETO.md) | Complete reference (Spanish) |
| [BETO_INSTRUCTIVO.md](BETO_INSTRUCTIVO.md) | Operational executor protocol (LLM-facing) |

---

## Repository Structure

```
beto-framework/
├── README.md
├── DOCUMENTACION_OFICIAL_BETO.md    ← Complete reference documentation
├── BETO_INSTRUCTIVO.md              ← Operational protocol (LLM executor instructions)
├── docs/                            ← Structured documentation for new users
│   ├── quickstart.md
│   ├── architecture.md
│   ├── claims-and-boundaries.md
│   ├── verification.md
│   ├── faq.md
│   └── related-work.md
├── framework/                       ← 12 formal BETO templates
├── beto_executor/                   ← Automated pipeline (Python)
│   └── src/
│       ├── main.py
│       ├── orquestador/
│       ├── motor_razonamiento/
│       ├── motor_codigo/
│       ├── gates_operador/
│       ├── gestor_ciclo/
│       └── beto_state/
├── skills/
│   └── beto-framework/              ← Claude Skill (install in Claude Code)
│       ├── SKILL.md
│       └── references/
├── examples/
│   ├── gastos_personales/           ← Complete cycle: personal expense tracker
│   └── beto_executor_self_specification/  ← Complete cycle: BETO specifying itself
└── research/
    └── BETO_Framework_Technical_Article.md  ← SSRN preprint (Abstract ID: 6411618)
```

---

## Examples

Two complete BETO cycles are included as reference:

- **[examples/gastos_personales/](examples/gastos_personales/)** — Personal expense tracker. 3 TRACE_VERIFIED Python files, 30 authorized IDs, 0 silent completions.
- **[examples/beto_executor_self_specification/](examples/beto_executor_self_specification/)** — BETO specifying its own executor. 5 nodes, 14 files, 100% TRACE_VERIFIED.

---

## Theoretical Foundation

The framework is grounded in a formal technical manuscript that defines the silent completion problem, positions BETO against existing governance approaches, and reports the empirical results of three complete specification cycles.

**BETO Framework: An Epistemic Governance Protocol for LLM-Assisted Software Specification**
Alberto Ramírez — Version 1.0, March 2026
Preprint: [SSRN Abstract ID: 6411618](https://ssrn.com/abstract=6411618)
Full text: [research/BETO_Framework_Technical_Article.md](research/BETO_Framework_Technical_Article.md)

---

## Status

**Current:** BETO v4.2 — stable, field-tested, public repository (March 2026)

**Empirical record:**

| System | Nodes | Source Files | TRACE_VERIFIED | Silent Completions |
|---|---|---|---|---|
| Dev Assistant | 6 | 11 | 11/11 (100%) | 0 |
| BETO Artifact Evaluator | 11 | 18 | 18/18 (100%) | 0 |
| BETO_EXECUTOR (self) | 5 | 14 | 14/14 (100%) | 0 |

**Roadmap:**
- [ ] Academic publication (manuscript in `research/`)
- [ ] Multilingual support
- [ ] BETO_INTAKE: multimodal admission layer

---

## License

MIT License — Copyright (c) 2026 Alberto Ramírez

Free to use, copy, modify, and distribute with attribution preserved.
See [LICENSE](LICENSE) for full terms.
