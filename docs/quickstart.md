# BETO Quickstart

BETO Protocol can be executed manually, via the **BETO Executor** (the reference implementation), or via the **BETO Skill** (a Claude integration path). This guide covers the two automated paths.

The Executor runs the full protocol deterministically with structural validation at each gate. The Skill runs it conversationally in Claude Code or Claude.ai with no infrastructure required. Both execute the same 11-step protocol and respect the same three human gates.

If you want to understand the protocol before running anything, start with [docs/architecture.md](architecture.md).

---

## Executor Quickstart (Reference Implementation)

The automated pipeline runs the full BETO Protocol deterministically with two LLM backends. Since v4.4, the Executor automatically selects the execution path (LIGHT / PARTIAL / FULL) based on the complexity of each sub-problem before running Steps 0–9.

### Prerequisites

- Python 3.11+
- An OpenAI-compatible API endpoint (tested with Claude Sonnet via LiteLLM)
- Optional: a local code model for Step 10 (tested with Qwen-Coder via vLLM)

### Setup

```bash
cd beto_executor/src
pip install openai
```

The Executor takes all configuration as CLI flags — no environment variables required.

### Run

```bash
python3 main.py \
  --idea "your idea here" \
  --reasoning-model claude-sonnet-4-6 \
  --code-model qwen-coder \
  --litellm-url http://localhost:8000 \
  --api-key local \
  --cycle-dir ./cycles \
  --templates-dir ../../skills/beto-framework/references
```

Or pass the idea from a file:

```bash
python3 main.py \
  --idea-file /path/to/idea.txt \
  --reasoning-model claude-sonnet-4-6 \
  --code-model qwen-coder \
  --litellm-url http://localhost:8000 \
  --api-key local \
  --cycle-dir ./cycles \
  --templates-dir ../../skills/beto-framework/references
```

**Key flags:**

| Flag | Description | Default |
|------|-------------|---------|
| `--idea` | IDEA_RAW as a string | — |
| `--idea-file` | Path to a text file with the IDEA_RAW | — |
| `--reasoning-model` | LLM for Steps 0–9 | `gpt-4o` |
| `--code-model` | LLM for Step 10 | `gpt-4o` |
| `--litellm-url` | LiteLLM gateway base URL | `http://localhost:8000` |
| `--api-key` | API key for the gateway | `none` |
| `--cycle-dir` | Output directory for cycles | `./cycles` |
| `--templates-dir` | Path to BETO framework templates | none (degraded mode) |
| `--g4` | Enable optional Gate G-4 | off |

The Executor runs Steps 0–9 with the reasoning motor, pauses at each gate (G-1, G-2, G-3) for your approval, then runs Step 10 with the code motor.

### What you will see at startup

```
[ROOT] Ruta inicial: BETO_FULL_PATH (score=31.0)
[Motor Razonamiento] Ejecutando Paso 0...
```

The first line is the v4.4 routing decision — the Executor evaluates the complexity of your idea and selects the execution path automatically before any LLM call. This decision is recorded as a `ROUTING_DECISION_RECORD` in `<cycle-dir>/<cycle-id>/.beto/routing/decisions/`.

### Expected result

A cycle directory under `--cycle-dir` containing:

- All BETO specification artifacts: `PASO_0_EVALUACION.md`, `BETO_CORE_DRAFT.md`, `BETO_SYSTEM_GRAPH.md`, `CIERRE_ASISTIDO_OPERATIVO.md`, `MANIFEST_PROYECTO.md`
- Source files with full BETO-TRACE annotations and a verified TRACE_REGISTRY
- A `.beto/` directory with v4.4 operational artifacts:
  - `.beto/routing/decisions/` — ROUTING_DECISION_RECORD for every routing decision
  - `.beto/snapshots/` — context snapshots (LC, CS, AQ, MS) per execution path
  - `.beto/project_index.json` — artifact index generated at handoff

### Common failure points

**Gate rejection requires manual rollback.** If you reject at a gate, the Executor does not automatically regenerate. You will need to restart the relevant step manually or resume from the last approved state.

**`--templates-dir` is strongly recommended.** Without it, the Executor runs in degraded mode: the LLM does not receive BETO framework templates as context and output quality will vary. Point it to `skills/beto-framework/references/` in this repository.

**Step 10 requires a code model.** The reasoning motor (Steps 0–9) uses any OpenAI-compatible API. Step 10 is optimized for a local code model. If you don't have one, Step 10 can be run with the same reasoning model, but output quality may vary.

**Context limits on complex systems.** The BETO_STATE engine reduces context by 60–70% compared to full artifact injection, but very large systems (10+ nodes) may still approach token limits on Step 2 and Step 4. The Executor handles this with split-call generation for those steps.

---

## Skill Quickstart (Claude Integration)

### Prerequisites

- Claude Code (CLI) or Claude.ai
- No additional infrastructure required

### Setup

```bash
cp -r skills/beto-framework ~/.claude/skills/
```

That is the complete installation. The Skill and all its reference templates are now available in your Claude session.

### Run BETO on an idea

In Claude Code or Claude.ai:

```
run BETO on this idea: [your idea]
```

or in Spanish:

```
corre BETO en esta idea: [tu idea]
```

### What to expect

BETO runs 11 steps. Three of them pause and require your decision:

**Gate G-1 (after Step 1):** You will first see a Gate Status Summary — cycle name, step, elements declared, OQs resolved, overrides, and BETO_GAPs. Then you will see a `BETO_CORE_DRAFT` — the root specification of your system. BETO will show you what it declared, what it inferred, and what it could not determine (Open Questions). You must either approve or reject. If you reject, BETO stops. If there are Open Questions, BETO will ask you to resolve them before proceeding.

**Gate G-2 (after Step 4):** You will first see a Gate Status Summary — cycle name, step, node count, and BETO_GAPs. If any BETO_GAPs exist, each is listed by TRACE_ID and resolution status (`ESCALATED` or `RESOLVED: BETO_ASSISTED`) so you can review them before opening the artifact. Then you will see the `BETO_SYSTEM_GRAPH` — the frozen topology of your system: all nodes, their types (ROOT / PARALLEL / SUBBETO), and their relationships. This is the last point before BETO generates individual specifications for each node. Approve or reject.

**Gate G-3 (after Step 9):** You will first see a Gate Status Summary — node count, authorized files, TRACE_REGISTRY ID count, assisted/operator resolutions, and BETO_GAPs. If any BETO_GAPs exist, each is listed by TRACE_ID and resolution status. Then you will see the `MANIFEST_PROYECTO` — the complete project manifest listing every authorized component, every TRACE_REGISTRY ID, and the full materialization plan. Approve to authorize code generation.

After G-3 approval, BETO produces source files annotated with BETO-TRACE IDs.

### Expected result

A set of source files where every function, field, and module is annotated with a BETO-TRACE ID that maps back to an operator-authorized specification decision. No element in the output was silently invented by the model.

### How to inspect the result

Check that every BETO-TRACE annotation in the generated files has a corresponding entry in the `TRACE_REGISTRY`. Any ID not in the registry is unauthorized.

Example annotation in Python:
```python
def registrar_gasto(monto: float, categoria: str, fecha: str) -> str:
    """
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.MONTO
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.CATEGORIA
    BETO-TRACE: GASTOS_REGISTRO.SEC3.INPUT.FECHA
    """
```

See the full working example: [examples/gastos_personales/](../examples/gastos_personales/)

### Common failure points

**The Skill drifts from the protocol mid-cycle.** In conversational execution, the model may occasionally compress or skip steps in long cycles. If you notice a step was skipped, name it explicitly: "we haven't done Step 3 yet — please execute it now."

**Open Questions are not resolved before G-1.** BETO will not proceed past G-1 if there are unresolved Open Questions that require your decision. You must answer them — or explicitly declare them as known limits of the system.

**The idea is rejected at Step 0.** BETO applies a semantic eligibility test before starting. Vague ideas are accepted. Ideas with no semantic core (empty directives, incoherent descriptions) are not. If your idea is rejected, refine it with a clearer intent.

