# Pending Improvements — BETO Executor

Improvements identified during empirical cycles, pending implementation.

---

## [IMPROVEMENT-001] Auto-generate README.md and requirements.txt in Paso 10

**Identified during:** duplicate_file_finder cycle (2026-03-19)
**Priority:** Medium

**Problem:**
The Motor de Código (Paso 10) generates source files with full BETO-TRACE annotations
but does not generate `README.md` or `requirements.txt`. These are added manually
after the cycle, outside BETO governance — meaning they carry no BETO-TRACE and are
not declared in the MANIFEST_PROYECTO.

**Proposed solution:**
Paso 10 should generate two additional artifacts as part of the scaffold:
- `README.md` — derived from MANIFEST_PROYECTO: system name, purpose, components,
  usage instructions, requirements
- `requirements.txt` — derived from declared external dependencies in BETO_CORE
  (SEC: dependencies/constraints); stdlib-only systems get an annotated empty file

Both should be included in the MANIFEST_PROYECTO template under a declared
`OPERATIONAL_ARTIFACTS` section and carry BETO-TRACE IDs.

**Scope:** Motor de Código scaffold builder + MANIFEST_PROYECTO template
