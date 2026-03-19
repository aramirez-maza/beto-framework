# BETO FAQ

---

## 1. "What does BETO do that good engineering discipline can't?"

A senior engineer will ask this immediately. Careful specifications, architecture reviews, and human oversight can also reduce the silent completion problem — so why does BETO exist?

BETO does not try to replace engineering discipline. What it introduces is a **structural constraint on AI-assisted generation** — not a cultural practice or a checklist.

The difference is mechanical:

Without BETO, the problem is: *"hope the model doesn't invent something."* That hope depends on model behavior, prompt quality, and reviewer attention — all variable.

With BETO, the problem becomes: *"make invention structurally impossible."* An undeclared element cannot be materialized. It is not a violation to be caught in review — it is a state that blocks execution before generation happens.

BETO detects what was not declared, converts it into an explicit registered event, and blocks its materialization. That happens at the point of generation, not after. No engineering process applied after the fact achieves the same guarantee, because the silent completion has already occurred.

---

## 2. "What stops the model from just declaring things on its own?"

An engineer will think: *"Can't the model mark everything as DECLARED and keep going?"*

In BETO, **only the operator can declare.** The model can infer, propose, and suggest — but it cannot change the epistemic state of an element. State transitions have defined authorities:

| Transition | Authority |
|---|---|
| → `DECLARED` | Operator only |
| → `NOT_STATED` | Executor (when element cannot be inferred) or Operator (explicit rejection) |
| → `INFERRED` | Model — authorized only in Steps 0–1, before Gate G-1 |

After G-1 — the first human gate — the inference frontier is closed. Any new element the model introduces that was not declared becomes a `BETO_GAP` event automatically. The executor cannot resolve it silently; it either derives it from the declared System Intent (logged and justified) or escalates to the operator and halts.

The model's authority ends at proposal. The operator's authority is the only one that enables materialization.

---

## 3. "What happens if the operator declares something wrong?"

This is the most important question. No system can guarantee the human is right.

BETO does not try to guarantee the correctness of the design. It guarantees something different: **complete traceability of how the system was authorized to exist.**

If the operator declares an incorrect field type, a wrong constraint, or a behavior that does not match the actual requirement — BETO will produce a fully traceable system that correctly implements the wrong thing. TRACE_VERIFIED does not mean functionally correct.

What BETO changes is the nature of the error:

- Without BETO: the error may be invisible — buried in a silent completion, mixed with model inventions, unattributable to any specific decision
- With BETO: the error is explicit, localized to a specific operator declaration at a specific gate, and traceable from the failing line of code back to the decision that authorized it

BETO eliminates invisible errors. It does not eliminate human errors. The difference is that a traceable error can be found, attributed, and corrected. An invisible one cannot.

→ For the full breakdown of guarantees and limits: [claims-and-boundaries.md](claims-and-boundaries.md)

---

→ Ready to run? [quickstart.md](quickstart.md)
→ How it works under the hood: [architecture.md](architecture.md)
