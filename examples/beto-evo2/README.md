# BETO × Evo2 — First Epistemic Governance Integration for a DNA Language Model

> **"Evo2 knows how to fold DNA. BETO decides if it should, under what constraints, and leaves a record of who authorized it."**

---

## What This Is

This is the **first documented integration of BETO Framework with a foundation model in the life sciences domain** — specifically with [Evo2](https://github.com/ArcInstitute/evo2) (Arc Institute), the state-of-the-art DNA language model capable of modeling and designing genomic sequences across all domains of life, published in *Nature* (2026).

**The problem it solves:** Evo2 is extraordinarily capable — but like all LLMs, it silently completes missing information. Ask it to generate a sequence without declaring organism, biosafety level, or sampling parameters, and it will generate anyway, inferring what you didn't say. The result is a genomic sequence with no traceable decision record. In computational biology, this is not just a software problem — it is a **reproducibility and biosafety problem**.

**BETO-EVO2** wraps Evo2 with full epistemic governance: every critical parameter must be `DECLARED` by the operator before any model call is executed. `NOT_STATED` blocks execution. Zero silent completions.

---

## The Result — A Real Evo2 Run

This is not a mock. This is a real call to Evo2-7B via NVIDIA NIM API, governed end-to-end by BETO Protocol v4.4.

```json
{
  "trace_id":     "BETO-EVO2-20260320-92B0AA3C",
  "trace_status": "TRACE_VERIFIED",
  "model_used":   "evo2-7B",
  "latency_ms":   10645,
  "spec_hash":    "4ea572f3d9856b9c",
  "evo2_output":  "GTCCAATTTGGTATTTTTCTACCATGTATTTTTTTTATTTTTTTTTATTTCCATTATATTAACAAGTTTTTTTATTATTATTATTTATCTTTTATTAGTTTGCAACTTATTAAAGAGCCT...",
  "epistemic_summary": {
    "DECLARED":   8,
    "NOT_STATED": 0,
    "INFERRED":   0
  }
}
```

The full verified trace is at [`resultado_real.json`](resultado_real.json).

---

## How It Was Born

This integration was not pre-planned. It emerged from a single informal sentence:

> *"si que BETO use a EVO2 como un wraper o si me das una idea clara de como BETO podria audar a EVO2, me entiendes? poniendo a BETO primero"*

BETO Protocol v4.4 was then executed on that raw idea — following all 11 steps, three human gates (G-1, G-2, G-3), and zero silent completions — producing the full specification and the working system you see here.

**The insight that made it work:** BETO and Evo2 share the exact same core problem from opposite directions.

```
Software without BETO:
  LLM silently completes architecture, schemas, contracts
  without declaring what it invented vs. what was declared.

Evo2 without BETO:
  LLM silently completes organism, biosafety, sampling parameters
  without declaring what it inferred vs. what the scientist specified.
```

Same pattern. Different domain. The symbiosis was discovered, not engineered.

---

## Architecture

```
Operator / Scientist
        │
        │  raw genomic intent (natural language)
        ▼
┌─────────────────────────────────────────────────────────┐
│                     BETO-EVO2                           │
│                                                         │
│  ┌──────────────────┐    ┌──────────────────────────┐  │
│  │ BETOSpec Engine  │    │      GateManager          │  │
│  │                  │───►│                          │  │
│  │ Classifies every │    │ Gate-A: topology          │  │
│  │ parameter as     │    │ Gate-B: full spec review  │  │
│  │ DECLARED /       │    │ Gate-C: exact NIM payload │  │
│  │ NOT_STATED /     │    │                          │  │
│  │ INFERRED         │    │ Blocks on any rejection   │  │
│  └──────────────────┘    └────────────┬─────────────┘  │
│                                       │ GateApprovalRecord│
│                          ┌────────────▼─────────────┐  │
│                          │      Evo2Adapter          │  │
│                          │                          │  │
│                          │ NVIDIA NIM API            │  │
│                          │ health.api.nvidia.com     │  │
│                          │ /v1/biology/arc/evo2-40b  │  │
│                          │ /generate                 │  │
│                          │                          │  │
│                          │ Executes ONLY with        │  │
│                          │ complete gate record      │  │
│                          └────────────┬─────────────┘  │
│                                       │ RawEvo2Response │
│                          ┌────────────▼─────────────┐  │
│                          │      TraceLogger          │  │
│                          │                          │  │
│                          │ TRACE_ID (unique)         │  │
│                          │ epistemic_manifest        │  │
│                          │ SQLite persistence        │  │
│                          │ TRACE_VERIFIED            │  │
│                          └──────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
        │
        ▼
  AuthorizedEvo2Result
  (TRACE_VERIFIED — every parameter traceable to a human decision)
```

---

## The 8 Critical Parameters

Every one of these must be `DECLARED` before any Evo2 call. `NOT_STATED` = execution blocked.

| Parameter | Why Critical |
|-----------|-------------|
| `organism` | Determines biological context and applicable safety protocols |
| `bio_function` | Defines the functional target — must be operator-authorized |
| `sequence_length` | Directly affects model behavior and reproducibility |
| `biosafety_level` | BSL-1 through BSL-4 — no default is acceptable |
| `evo2_model_size` | 1B / 7B / 20B / 40B — affects quality, cost, reproducibility |
| `sampling_temp` | Inference parameter — undeclared temperature = silent choice |
| `top_k` | Sampling constraint — undeclared = unauditable diversity |
| `excluded_motifs` | Sequences that must not appear in output — `[]` is a valid declaration |

---

## The Three Gates

Before any call reaches Evo2, the operator must approve three checkpoints:

```
Gate-A — Topology
  "Here is the pipeline that will run and the task type. Approve?"

Gate-B — Full Specification
  "Here are all 8 declared parameters with their values and epistemic states.
   You may modify any. Approve?"

Gate-C — Exact Evo2 Payload
  "This is the exact JSON that will be sent to NVIDIA NIM API.
   payload_hash: 8c9dc6c0499cf7a9
   Nothing will change after this approval. Authorize?"
```

No call is made without `gate_c.approved = True`.

---

## Real Run Output — Gate-B

```
╔══════════════════════════════════════════════╗
║  BETO-EVO2 — GATE B: ESPECIFICACION         ║
╚══════════════════════════════════════════════╝

  ✓ organism             = 'Homo sapiens'                 [DECLARED]
  ✓ bio_function         = 'modular BRCA1 expression'     [DECLARED]
  ✓ sequence_length      = 256                            [DECLARED]
  ✓ biosafety_level      = BSL-2                          [DECLARED]
  ✓ evo2_model_size      = 7B                             [DECLARED]
  ✓ sampling_temp        = 0.7                            [DECLARED]
  ✓ top_k                = 4                              [DECLARED]
  ✓ excluded_motifs      = []                             [DECLARED]
```

---

## Real Run Output — Gate-C

```
╔══════════════════════════════════════════════╗
║  BETO-EVO2 — GATE C: PAYLOAD EXACTO EVO2   ║
╚══════════════════════════════════════════════╝

{
    "sequence":   "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGT",
    "num_tokens": 256,
    "temperature": 0.7,
    "top_k": 4,
    "top_p": 0
}

  payload_hash: 8c9dc6c0499cf7a9
  Nothing will change after this approval.
```

---

## Why This Matters for Science

### Reproducibility
Every run produces a `spec_hash` that encodes all declared parameters. The same hash = the same experiment. No more *"we used standard parameters"* in Methods sections.

### Biosafety Auditability
```sql
-- Who authorized this BSL-3 sequence generation?
SELECT operator_id, timestamp
FROM gate_approvals
WHERE trace_id = 'BETO-EVO2-20260320-92B0AA3C'
  AND gate_id = 'gate_c';
-- → aramirez | 2026-03-20T14:32:11Z
```

### Publication-Ready Trace
The `epistemic_manifest` from every run can be attached as supplementary material to a paper, proving that no parameter was silently inferred by the model.

### Zero Silent Completions
```
Evo2 without BETO:  organism? → model assumes
                    biosafety? → model ignores
                    temperature? → model defaults silently

Evo2 with BETO:     organism? NOT_STATED → BLOCKED
                    biosafety? NOT_STATED → BLOCKED
                    temperature? NOT_STATED → BLOCKED
```

---

## Quick Start

```bash
# 1. Install
cd examples/beto-evo2/beto_evo2
pip install requests

# 2. Set NVIDIA NIM API key (get it free at build.nvidia.com)
export NVIDIA_API_KEY="nvapi-your-key-here"

# 3. Run (interactive mode — BETO guides you through every gate)
python3 main.py --interactive --operator-id "your_id"

# 4. Run (declarative — all parameters in one line)
python3 main.py \
  --intent "organism: Homo sapiens, function: modular BRCA1 expression, \
            256bp, BSL-2, 7B, temperature: 0.7, top_k: 4, excluded_motifs: []" \
  --task GENERATION \
  --seed "ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAAAATCTTAGAGT" \
  --operator-id "your_id" \
  --output result.json

# 5. Export audit trail
python3 main.py --export-registry
```

**No NVIDIA key?** The system runs in simulation mode automatically — full BETO governance pipeline, gates, SQLite persistence, and TRACE_VERIFIED output, without calling the API.

---

## Files

```
beto-evo2/
├── README.md                    ← you are here
├── resultado_real.json          ← real Evo2-7B output, TRACE_VERIFIED
└── beto_evo2/
    ├── main.py                  ← CLI entry point + pipeline orchestrator
    ├── models.py                ← all shared data types (GenomicRequest, ParameterMap, ...)
    ├── beto_spec_engine.py      ← Phase 1: epistemic parameter classification
    ├── gate_manager.py          ← Phase 2: Gate-A / Gate-B / Gate-C workflow
    ├── evo2_adapter.py          ← Phase 3: authorized NVIDIA NIM API interface
    ├── trace_logger.py          ← Phase 4: TRACE_ID + SQLite + TRACE_VERIFIED
    ├── requirements.txt         ← requests>=2.31.0 (stdlib only otherwise)
    └── db/
        └── schema.sql           ← 4-table SQLite schema, WAL mode
```

---

## BETO Specification

This system was fully specified using BETO Protocol v4.4 before a single line of code was written.

- **Complexity score:** 9 → `BETO_PARTIAL_PATH`
- **Nodes:** 1 ROOT + 4 PARALLEL + 0 SUBBETO
- **DECLARED elements:** 47 (operator) + 12 (BETO_ASSISTED)
- **BETO_GAPs:** 0
- **Open Questions at G-3:** 0
- **TRACE_REGISTRY entries:** 52
- **Status at materialization:** `APPROVED_EXECUTABLE`

The full BETO specification (BETO_CORE_DRAFT, System Graph, Phase Documents, Manifests) was generated interactively using the BETO Skill in Claude Code.

---

## Epistemic Guarantee

```
Every genomic sequence generated by this system is traceable
to a human decision. No parameter was silently chosen by the model.
No call was made without operator authorization.
Every result carries a TRACE_ID, a spec_hash, and a complete
epistemic_manifest — permanently stored in SQLite.

DECLARED:   8 / 8 critical parameters
NOT_STATED: 0
INFERRED:   0
Status:     TRACE_VERIFIED
```

---

## About BETO Framework

[BETO Framework](https://github.com/aramirez-maza/beto-framework) is an epistemic governance protocol for LLM-assisted software specification and materialization. It formalizes the distinction between operator-declared specifications and model-inferred assumptions, ensuring all generated artifacts remain traceable and auditable.

> *BETO formalizes the ignorance of an AI.*
> *It materializes raw semantic intent into fully traceable, auditable software.*

**Author:** Alberto Ramírez · **License:** MIT · **Version:** 4.5.0

---

*This example represents the first application of BETO to the life sciences domain —
bridging epistemic governance and genomic foundation models.*
