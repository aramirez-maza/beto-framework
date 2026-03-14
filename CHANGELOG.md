# CHANGELOG

All notable changes to the BETO Framework are documented here.

Format: `[version] — date — description`

---

## [4.2.2] — 2026-03-14

**Documentation: structural refactor**

- `README.md` rewritten as landing page — problem, core idea, three-layer overview, guarantees, explicit limits, documentation map
- `docs/` layer created with five new files: `quickstart.md`, `architecture.md`, `claims-and-boundaries.md`, `verification.md`, `faq.md`
- `docs/related-work.md` added — positions BETO against existing approaches
- `CHANGELOG.md` added
- Hierarchy enforced throughout: Protocol → Executor (reference implementation) → Skill (integration path)
- `DOCUMENTACION_OFICIAL_BETO.md` and `BETO_INSTRUCTIVO.md` preserved intact as full reference documents

---

## [4.2.2] — 2026-03-14

**BETO Skill — Assisted Mode override evaluation + version display**

- Override evaluation rule added: when operator overrides a BETO_ASSISTED resolution, Skill evaluates scope consistency before accepting — triggers `BETO_GAP [ESCALATED]` if override introduces external dependencies or scope expansion
- Version display added at session start: `BETO Skill v4.2.1 — github.com/...`
- Update instructions added: operators can check installed version and update via `cp -r`

---

## [4.2.1] — 2026-03-13

**BETO Skill + gastos_personales example**

- `skills/beto-framework/` added — Claude Skill for interactive BETO protocol execution in Claude Code and Claude.ai; no infrastructure required
- `skills/beto-framework/references/` — all BETO templates bundled for on-demand loading
- `examples/gastos_personales/` added — complete BETO v4.2 cycle: personal expense tracker; 3 TRACE_VERIFIED Python files, 30 authorized IDs, 0 silent completions

---

## [4.2.0] — 2026-03-12

**Public release — BETO Framework v4.2**

- Initial public repository release
- `DOCUMENTACION_OFICIAL_BETO.md` — complete framework reference (Spanish)
- `BETO_INSTRUCTIVO.md` — operational executor protocol (11 steps, 11 rules)
- `framework/` — 12 formal BETO templates (BETO_CORE, BETO_SYSTEM_GRAPH, PHASE, MANIFEST, TRACE_REGISTRY, GENERATOR_RULES, FRAMEWORK_FEEDBACK, OPERATIONAL_LESSONS, PROMPT_CANONICO)
- `beto_executor/src/` — automated pipeline; reasoning motor (Steps 0–9, Claude Sonnet) + code motor (Step 10, Qwen-Coder); BETO_STATE engine; 29-check deterministic structural validator
- `examples/beto_executor_self_specification/` — BETO specifying its own executor; 5 nodes, 14 TRACE_VERIFIED files, 0 silent completions
- `research/BETO_Framework_Technical_Article.md` — technical manuscript; available as preprint on SSRN (Abstract ID: 6411618)
- MIT License

---

## Pre-release development (2022–2026)

BETO was developed privately over four years before the v4.2 public release. The following milestones are recorded for historical completeness:

- **2022** — Initial formalization of the silent completion problem and the three-state epistemic model (DECLARED / NOT_STATED / INFERRED)
- **2023** — BETO_GAP protocol defined; first complete manual execution of the 11-step process
- **2024** — TRACE_REGISTRY mechanism introduced; first empirical cycle (Dev Assistant, 6 nodes, 11 files, 100% TRACE_VERIFIED)
- **2025** — BETO Artifact Evaluator cycle (11 nodes, 18 files); node taxonomy formalized (ROOT / PARALLEL / SUBBETO); semantic independence test established; BETO_EXECUTOR development begins
- **Early 2026** — BETO_EXECUTOR self-specification cycle completed (5 nodes, 14 files); BETO_STATE engine implemented; v4.2 stabilized for public release
