# BETO Quickstart

BETO Protocol can be executed manually, via the **BETO Executor** (the reference implementation), or via the **BETO Skill** (a Claude integration path). This guide covers the two automated paths.

The Executor runs the full protocol deterministically with structural validation at each gate. The Skill runs it conversationally in Claude Code or Claude.ai with no infrastructure required. Both execute the same 11-step protocol and respect the same three human gates.

If you want to understand the protocol before running anything, start with [docs/architecture.md](architecture.md).

---

## Executor Quickstart (Reference Implementation)

The automated pipeline runs the full BETO Protocol deterministically with two LLM backends.

### Prerequisites

- Python 3.11+
- An OpenAI-compatible API endpoint (tested with Claude Sonnet via LiteLLM)
- Optional: a local code model for Step 10 (tested with Qwen-Coder via vLLM)

### Setup

```bash
cd beto_executor/src
pip install openai

export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="your-key"
```

### Run

```bash
python main.py "Your idea here"
```

The Executor runs Steps 0–9 with the reasoning motor, pauses at each gate (G-1, G-2, G-3) for your approval, then runs Step 10 with the code motor.

### Expected result

A cycle directory under `src/cycles/` containing all BETO artifacts (PASO_0, BETO_CORE_DRAFT, BETO_SYSTEM_GRAPH, CIERRE_ASISTIDO, MANIFEST_PROYECTO, source files) with full BETO-TRACE annotations and a verified TRACE_REGISTRY.

### Common failure points

**Gate rejection requires manual rollback.** If you reject at a gate, the Executor does not automatically regenerate. You will need to restart the relevant step manually or resume from the last approved state.

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

