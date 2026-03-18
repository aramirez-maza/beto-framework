# CHANGELOG

All notable changes to the BETO Framework are documented here.

Format: `[version] — date — description`

---

## [4.4.0] — 2026-03-18

**BETO Framework v4.4 — Execution Efficiency and Routing Layer**

Major extension: adds internal routing, stratified context, persistent snapshots, and adaptive execution modes. BETO no longer requires a separate external skill surface for simple tasks — they are absorbed into the unified executor.

**Internal routing system:**
- `complexity_score` function with 8 weighted factors and deterministic thresholds
- Three execution paths: `BETO_LIGHT_PATH` (0–5), `BETO_PARTIAL_PATH` (6–12), `BETO_FULL_PATH` (13+)
- Default weights: w1=1, w2=1, w3=1, w4=2, w5=3, w6=2, w7=2, w8=2 (configurable, fixed defaults)
- `ROUTING_DECISION_RECORD` — every routing decision is traceable, no silent decisions
- `ROUTE_PROMOTION_RECORD` — every route promotion is traceable (LIGHT→PARTIAL→FULL)

**Stratified context (3 layers):**
- Layer A: STABLE_CORE_CONTEXT — instructions, rules, invariant templates (prefix-cacheable)
- Layer B: CYCLE_CONTEXT — active BETO_CORE, current step, active OQs, routing state
- Layer C: LOCAL_EXECUTION_CONTEXT — current file, diff, template, phase, OQ for sub-problem
- Rule: every model call uses only the minimum required context (A + minimal B + C)

**Persistent snapshots:**
- `CYCLE_CONTEXT_SNAPSHOT` — cycle state at a point in time
- `ACTIVE_OQ_SET` — compact set of OQs relevant to the current tramo
- `LOCAL_EXECUTION_CONTEXT` — sub-problem specific context
- `MATERIALIZATION_SCOPE` — exact scope of what to materialize in a tramo
- All stored in `.beto/snapshots/` — invalidation rules formally defined

**Operational artifacts:**
- `MODEL_CALL_PLAN` — governs, executes, and logs every model call; includes cache eligibility and fallback strategy
- `PROJECT_INDEX` (JSON, schema: `PROJECT_INDEX_SCHEMA.json`) — persistent artifact index in `.beto/project_index.json`; auto-updated by executor; manual reindex available
- `EXECUTION_PERFORMANCE_LOG` — audit log of every model call; enables efficiency analysis

**Execution mode policy:**
- `EXECUTION_MODE_POLICY.md` — canonical definition of what each mode can and cannot do
- 10 declared sub-executors under unified executor authority
- Sub-executors cannot call each other without passing through the orchestrator

**3-level cache strategy:**
- PREFIX_CACHE: instructions, rules, invariant templates
- SEMANTIC_CACHE: closed BETO_COREs, validated graphs, closed manifests
- OPERATIONAL_CACHE: active snapshots, recent diffs, recent outputs, routing decisions

**OSC local evaluation (BETO v4.3 compatibility):**
- EXECUTION_READINESS_CHECK applied per OQ or per unit (not globally blocking)
- G-2B result registered per unit in BETO_PARALELO
- BETO_LIGHT_PATH triggers local OSC evaluation or promotes route if OQ is not closeable locally

**12 new rules in BETO_INSTRUCTIVO.md:**
- REGLA EXECUTION_PATH_SELECTION
- REGLA MINIMAL_CONTEXT_EXECUTION
- REGLA CONTEXT_STRATIFICATION
- REGLA SNAPSHOT_INVALIDATION
- REGLA MODEL_CALL_GOVERNANCE
- REGLA LOCAL_OSC_EVALUATION
- REGLA INCREMENTAL_MATERIALIZATION
- REGLA PROJECT_INDEX_PERSISTENCE
- REGLA NO_SEPARATE_SKILL_SURFACE
- REGLA ROUTE_PROMOTION
- REGLA LIGHT_MODE_SCOPE_CONTROL
- REGLA EXECUTOR_UNIFICATION

**9 new state manager events:**
- `ROUTING_DECISION_REGISTERED`, `ROUTE_PROMOTED`, `SNAPSHOT_CREATED`, `SNAPSHOT_INVALIDATED`
- `PROJECT_INDEX_UPDATED`, `REINDEX_PROJECT_INDEX`, `MODEL_CALL_PLANNED`, `MODEL_CALL_COMPLETED`
- `PERFORMANCE_LOG_ENTRY`

**11 new templates** (in `framework/` and `skills/beto-framework/references/`):
- EXECUTION_ROUTER.md, ROUTING_DECISION_RECORD.md, ROUTE_PROMOTION_RECORD.md, EXECUTION_MODE_POLICY.md
- CYCLE_CONTEXT_SNAPSHOT.md, ACTIVE_OQ_SET.md, LOCAL_EXECUTION_CONTEXT.md, MATERIALIZATION_SCOPE.md
- MODEL_CALL_PLAN.md, PROJECT_INDEX_SCHEMA.json, EXECUTION_PERFORMANCE_LOG.md

**New executor module:**
- `beto_executor/src/execution_router/` — router.py, complexity_scorer.py, path_registry.py
- `beto_executor/src/beto_state/schema.py` — extended with RouteDecision, ContextSnapshot, ProjectIndexEntry, ModelCallPlan, RoutingState dataclasses
- `beto_executor/src/gestor_ciclo/state_manager.py` — 9 new v4.4 events added

**SKILL.md updated to v4.4.0:**
- Routing documentation, v4.4 template references, What's new section

**DOCUMENTACION_OFICIAL_BETO.md:** Section 15 added — complete v4.4 documentation

**Compatibility:** All v4.3 artifacts remain valid. All new schema fields have safe defaults. No existing field was removed or renamed.

---

## [4.3.0] — 2026-03-17

**BETO Framework v4.3 — Operational Semantic Closure (OSC) Layer**

Major extension: adds a new control layer over the quality of declared responses.
BETO v4.2 blocked what was NOT_STATED. BETO v4.3 also validates what IS declared.

**New states (refine DECLARED):**
- `DECLARED_RAW` — response exists but is not operationally sufficient
- `DECLARED_EXECUTABLE` — response is implementable without relevant inferences
- `DECLARED_WITH_LIMITS` — response is usable with accepted controlled ambiguity

**New gap type:**
- `BETO_GAP_EXECUTIONAL` — response exists but is insufficient for consistent execution
  (complements, does NOT replace, BETO_GAP)

**EXECUTION_READINESS_CHECK:**
- Mandatory validator for critical OQs
- Evaluates 8 fields: alcance, trigger, input, output, constraint, fallback, exception, trazabilidad
- Results: PASS_EXECUTABLE | PASS_WITH_LIMITS | FAIL_EXECUTIONAL_GAP

**OQ Type classification (mandatory):**
- 7 types: OQ_CONFIG | OQ_POLICY | OQ_EXECUTION | OQ_EXCEPTION | OQ_DATA_SEMANTICS | OQ_INTERFACE | OQ_OBSERVABILITY
- OQ_POLICY, OQ_EXECUTION, OQ_EXCEPTION, OQ_DATA_SEMANTICS cannot close with free text

**Step 6 upgraded — CIERRE_ASISTIDO_OPERATIVO:**
- Promotes critical OQs to executable states
- Generates EXECUTION_INTENT_MAP.md and EXECUTIONAL_GAP_REGISTRY.md
- Anti-perfectionism policy: max_operational_requestions = 2

**New gate G-2B — Operational Readiness Gate:**
- APPROVED_EXECUTABLE | APPROVED_WITH_LIMITS | BLOCKED_BY_EXECUTIONAL_GAPS
- Evaluated per unit in BETO_PARALELO — does NOT block globally

**5 new templates:**
- `OQ_RESPONSE_EXECUTABLE.md`
- `EXECUTION_INTENT_MAP.md`
- `CONFLICT_RESOLUTION_TABLE.md`
- `AMBIGUITY_RESIDUE_REPORT.md`
- `EXECUTIONAL_GAP_REGISTRY.md`

**4 new OSC events registered in state_manager:**
- `BETO_EXECUTIONAL_REQUESTION`
- `BETO_GAP_EXECUTIONAL`
- `BETO_DECLARATION_PROMOTED_TO_EXECUTABLE`
- `BETO_DECLARATION_ACCEPTED_WITH_LIMITS`
- `REGISTRAR_G2B_RESULT`

**BETOState schema extended (backward-compatible):**
- `executional_gap_count`, `requestion_history`, `operational_residue`, `accepted_limits`, `g2b_result`

**OQ dataclass extended:**
- `oq_type`, `critical`, `execution_state`, `execution_readiness_check`, `requestion_count`

**BETO_PARALELO compatibility:**
- OSC is local per unit — blocked unit does not block others
- G-2B evaluated per unit with `unit_id` + `trace_id` on all OSC events

**BETO_CORE_INTERVIEW.md:**
- Section 13 added: OQ classification (OSC) — mandatory for all BETO_CORE

**BETO_CORE_TEMPLATE.md:**
- OQ format extended with: `oq_type`, `critical`, `execution_state`, `execution_readiness_check`

**SKILL.md:**
- Updated to v4.3.0
- OSC states, OQ types, soft detection patterns documented
- Step 6 updated with full CIERRE_ASISTIDO_OPERATIVO protocol

**BETO_INSTRUCTIVO.md:**
- OSC rules appended: OSC_ESTADOS, OSC_CIERRE_CRITICO, OSC_OQ_TYPE, OSC_EXECUTION_READINESS_CHECK,
  OSC_BETO_GAP_EXECUTIONAL, OSC_ANTI_PERFECCIONISMO, OSC_CIERRE_ASISTIDO_OPERATIVO,
  OSC_GATE_G2B, OSC_PARALELO, OSC_EVENTOS, OSC acceptance criteria

**DOCUMENTACION_OFICIAL_BETO.md:**
- Section 14 added: complete OSC documentation

**Compatibility:** All v4.2 artifacts remain valid. All new OSC fields have safe defaults.

---

## [4.2.4] — 2026-03-15

**BETO Skill — BETO_GAP detail in Gate Status Summary**

- Gate Status Summary at G-2 and G-3 now lists each BETO_GAP by TRACE_ID and status when count > 0
- Format: `→ [TRACE_ID] [ESCALATED | RESOLVED: BETO_ASSISTED]` — one line per gap, indented below the count
- If BETO_GAPs = 0, format unchanged — no visual noise in clean cycles
- Operator can now audit which gaps exist and their resolution state without opening the artifact
- Version bumped to 4.2.4

---

## [4.2.3] — 2026-03-15

**BETO Skill — Gate Status Summary**

- Gate Status Summary added before each human gate (G-1, G-2, G-3)
- Summary displays: cycle name, current step, declared elements, BETO_ASSISTED count, OPERATOR overrides, BETO_GAPs, node count (G-2/G-3), authorized files and IDs (G-3)
- Provides cycle context snapshot before the operator reviews each artifact — reduces cognitive load and prevents drift in long sessions
- `docs/quickstart.md` updated to mention Gate Status Summary
- Version bumped to 4.2.3

---

## [4.2.2] — 2026-03-14

**Documentation: structural refactor + BETO Skill override evaluation**

- `README.md` rewritten as landing page — problem, core idea, three-layer overview, guarantees, explicit limits, documentation map
- `docs/` layer created with five new files: `quickstart.md`, `architecture.md`, `claims-and-boundaries.md`, `verification.md`, `faq.md`
- `docs/related-work.md` added — positions BETO against existing approaches
- `CHANGELOG.md` added
- Hierarchy enforced throughout: Protocol → Executor (reference implementation) → Skill (integration path)
- `DOCUMENTACION_OFICIAL_BETO.md` and `BETO_INSTRUCTIVO.md` preserved intact as full reference documents
- Override evaluation rule added to Skill: when operator overrides a BETO_ASSISTED resolution, Skill evaluates scope consistency before accepting — triggers `BETO_GAP [ESCALATED]` if override introduces external dependencies or scope expansion
- Version display added at Skill session start: `BETO Skill v4.2.2 — github.com/...`
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
