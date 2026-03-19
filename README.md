# BETO Framework

> **BETO formalizes the ignorance of an AI.**

BETO is an epistemic governance protocol that materializes raw semantic intent into fully traceable, auditable software. It enforces a formal boundary between what the operator has declared and what the model has assumed — preventing the silent completion problem that makes AI-generated software unauditable.

**Version:** 4.5.0 (March 2026) · **Author:** Alberto Ramírez · **License:** MIT

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

**BETO Executor** — An automated Python pipeline that runs the full BETO Protocol. Includes an internal routing layer (v4.4) that selects the appropriate execution mode based on sub-problem complexity — `BETO_LIGHT_PATH` for simple tasks, `BETO_PARTIAL_PATH` for localized work within an existing cycle, and `BETO_FULL_PATH` for complete systems and architecture. Uses a reasoning motor (Steps 0–9, tested with Claude Sonnet) and a code motor (Step 10, tested with Qwen-Coder via vLLM). Requires Python 3.11+, an OpenAI-compatible API, and optionally a local code model.

**BETO Skill** — A Claude Skill that runs the complete BETO Protocol interactively in Claude Code or Claude.ai with no infrastructure required. Since v4.4, simple tasks are absorbed directly by the executor's internal light mode — no separate external surface is needed. The lowest-friction entry point to BETO.

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

---

## v4.4 — Execution Efficiency and Routing Layer

BETO v4.4 optimizes *how* BETO executes internally without changing *what* BETO means. The 11-step protocol, the no-invention rules, and full traceability are unchanged.

**What v4.4 adds:**

- **Internal routing** — before each sub-problem, a deterministic `complexity_score` function selects the appropriate execution mode:
  - `BETO_LIGHT_PATH` (score 0–5) — simple tasks, pointwise output, no graph needed
  - `BETO_PARTIAL_PATH` (score 6–12) — localized work within an existing cycle
  - `BETO_FULL_PATH` (score 13+) — complete systems, architecture, full materialization

- **Stratified context** — every model call receives only the minimum required context: a stable core layer (rules, invariant templates), a cycle layer (active BETO_CORE, current step), and a local layer (current sub-problem). No global context dump per call.

- **Persistent snapshots** — cycle state is captured between calls so the executor does not reconstruct the full context on every tramo. Snapshots are invalidated automatically when their source artifacts change.

- **Simple task absorption** — `BETO_LIGHT_PATH` handles tasks that previously required a separate external skill surface, keeping them inside the unified executor under the same epistemic rules.

- **PROJECT_INDEX** — a persistent artifact index (`.beto/project_index.json`) that locates artifacts without repeated global exploration. *(v4.5: generated on demand from SQLite — not a runtime source of truth.)*

- **MODEL_CALL_PLAN** — every model call is governed, logged, and auditable via `EXECUTION_PERFORMANCE_LOG`.

All routing decisions and route promotions (LIGHT→PARTIAL→FULL) are traceable — no silent routing. Full specification in `framework/EXECUTION_ROUTER.md` and `BETO_INSTRUCTIVO.md`.

---

## v4.5 — SQLite Persistence Layer

BETO v4.5 completes the migration of all runtime persistence from scattered JSON files to a local SQLite database. The Executor now operates with SQLite as the sole source of truth for cycle state, routing decisions, snapshots, OQs, gate decisions, and artifacts.

**What v4.5 changes in the Executor:**

- **Transversal persistence layer** (`persistence/`) — 11 tables, WAL mode, per-operation connections, no shared state, no external dependencies (sqlite3 stdlib only)
- **Canonical state assembler** — `build_state_payload(beto_dir, cycle_id)` renders `BETO_STATE.json` from SQLite; the file is a projection, not a store
- **SQLite-only writer** — `BETOStateWriter` auto-creates the database if absent, loads prior state from SQLite on resume, and raises immediately on render failure — no fallback, no silent degradation
- **Gate persistence** — `GateWriter` connected in the reasoning motor; every gate decision is stored with timestamp and cycle linkage
- **Legacy backfill** — `migrate_project(beto_dir)` migrates existing JSON-based projects to SQLite; idempotent, non-destructive
- **JSON routing/snapshot writes eliminated** — `.beto/routing/decisions/`, `.beto/routing/promotions/`, `.beto/snapshots/` are no longer written at runtime

**What v4.5 does not change:**

The BETO Protocol, the 11-step process, all formal templates, human gates, epistemic states, and the BETO_STATE.json interface for external consumers — all unchanged. v4.4 artifacts remain fully valid.

---

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
├── CHANGELOG.md
├── docs/                            ← Structured documentation for new users
│   ├── quickstart.md
│   ├── architecture.md
│   ├── claims-and-boundaries.md
│   ├── verification.md
│   ├── faq.md
│   └── related-work.md
├── framework/                       ← 23 formal BETO templates
│   ├── (12 core templates — v4.2/v4.3)
│   └── (11 routing & efficiency templates — v4.4)
├── beto_executor/                   ← Automated pipeline (Python)
│   └── src/
│       ├── main.py
│       ├── persistence/             ← v4.5: transversal SQLite layer
│       │   ├── schema.py, connection.py, queries.py
│       │   ├── writers/             ← cycle, routing, snapshot, oq, gate, artifact
│       │   ├── readers/             ← state_reader (build_state_payload)
│       │   └── migrate/             ← legacy_json_backfill
│       ├── execution_router/        ← v4.4: internal routing layer
│       ├── orquestador/
│       ├── motor_razonamiento/
│       ├── motor_codigo/
│       ├── gates_operador/
│       ├── gestor_ciclo/
│       └── beto_state/
├── skills/
│   └── beto-framework/              ← Claude Skill (install in Claude Code)
│       ├── SKILL.md
│       └── references/              ← All BETO templates, including v4.4
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

**Current:** BETO v4.5.0 — SQLite Persistence Layer (March 2026)

**Version history:**

| Version | Date | Change |
|---------|------|--------|
| v4.5.0 | 2026-03-18 | SQLite Persistence Layer — sole runtime backend, canonical state assembler, legacy backfill, JSON writes eliminated |
| v4.4.0 | 2026-03-18 | Execution Efficiency and Routing Layer — internal routing, stratified context, snapshots, PROJECT_INDEX, MODEL_CALL_PLAN, simple task absorption |
| v4.3.0 | 2026-03-17 | Operational Semantic Closure (OSC) Layer — DECLARED_EXECUTABLE states, EXECUTION_READINESS_CHECK, Gate G-2B |
| v4.2.0 | 2026-03-12 | Public release — 11-step protocol, BETO_EXECUTOR, BETO Skill |

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
