# Example: Gastos Personales (Personal Expense Tracker)

A complete BETO v4.2 specification cycle — from IDEA_RAW to working Python code.

## IDEA_RAW

> *"Quiero un sistema para registrar y consultar mis gastos personales por categoría"*

## Cycle Summary

| Step | Artifact | Status |
|---|---|---|
| 0 | Semantic eligibility | GO |
| 1 | BETO_CORE_DRAFT | Approved at G-1 |
| 2 | BETO_CORE_INTERVIEW_COMPLETED | Complete |
| 3 | STRUCTURAL_CLASSIFICATION_REGISTRY | 2 PARALLEL nodes |
| 4 | BETO_SYSTEM_GRAPH | VALIDATED — approved at G-2 |
| 5 | BETO_CORE children | 2 nodes — SUCCESS_CLOSED |
| 6 | CIERRE_ASISTIDO | All OQs resolved |
| 7 | Phase documents | 4 phase docs |
| 8 | MANIFEST + TRACE_REGISTRY | 30 authorized IDs |
| 9 | MANIFEST_PROYECTO | Approved at G-3 |
| 10 | Source files | TRACE_VERIFIED |

## System Graph

```
ROOT: GASTOS_PERSONALES
  ├── FUNCTIONAL_BRANCH → GASTOS_REGISTRO  (PARALLEL)
  └── FUNCTIONAL_BRANCH → GASTOS_CONSULTA  (PARALLEL)
```

## Materialization Results

| File | BETO_CORE | Status |
|---|---|---|
| `registro.py` | GASTOS_REGISTRO | TRACE_VERIFIED |
| `consulta.py` | GASTOS_CONSULTA | TRACE_VERIFIED |
| `main.py` | GASTOS_PERSONALES (ROOT) | TRACE_VERIFIED |

**TRACE_VERIFIED: 3/3 — Silent completions: 0**

## Usage

```bash
# Register an expense
python3 main.py registrar 45.50 Comida 2026-03-13 --descripcion "Lunch"

# Consult all expenses
python3 main.py consultar

# Filter by category
python3 main.py consultar --categoria Comida

# Filter by date range
python3 main.py consultar --desde 2026-03-01 --hasta 2026-03-31
```

## Open Questions Resolved

| OQ | Question | Resolution |
|---|---|---|
| OQ-1 | Where to persist data? | Local JSON file (`gastos.json`) — DECLARED |
| OQ-2 | User interface? | CLI — DECLARED |

## How This Was Generated

This example was produced using the **BETO Framework Claude Skill** — the
`skills/beto-framework/` package in this repository. The complete specification
cycle was run interactively with Claude Code following the BETO v4.2 protocol.

To reproduce: install the skill and run:

```
"corre BETO en esta idea: Quiero un sistema para registrar y consultar mis gastos personales por categoría"
```
