# IMPLEMENTATION_CONTRACT — {{BETO_NAME}}

## 1. PURPOSE
Freeze the minimum structural projection from approved PHASE documents to materialization.

This artifact is optional.
It is only generated when PHASE documents alone do not reduce structural variability enough.

It does NOT:
- replace BETO_CORE
- replace PHASE
- redefine system intent
- introduce new outputs
- introduce new phases

---

## 2. ACTIVATION BASIS
State why this IMPLEMENTATION_CONTRACT exists.

Allowed activation reasons:
- multiple files per phase
- shared contracts between phases
- more than one non-trivial materializable output
- fine-grained dependencies between components inside one BETO
- real risk of structural variability between valid implementations

If none apply, this artifact must not exist.

---

## 3. AUTHORIZED STRUCTURAL UNITS
List only the files, modules, directories, or structural units authorized for materialization.

For each unit include:
- Name
- Type
- Declared purpose
- Owning phase or component

STRICT RULE:
- Do NOT define behavior here.
- Do NOT duplicate PHASE logic.

---

## 4. SHARED CONTRACTS
List only the shared contracts relevant to structural coordination between units.

Include:
- Contract name
- Producer
- Consumer
- Why it is structurally relevant

If none: `None declared`

---

## 5. FINE-GRAINED DEPENDENCIES
List only dependencies between authorized structural units that matter for build order or structural integrity.

For each dependency include:
- From
- To
- Reason

If none: `None declared`

---

## 6. MATERIALIZATION ORDER
Freeze the fine-grained order of materialization only where needed.

Format:
1. [unit or group]
2. [unit or group]
3. [unit or group]

If no finer order than PHASE is needed:
`No finer order declared`

---

## 7. STRUCTURAL LIMITS
State the implementation limits this artifact enforces.

Examples of allowed content:
- no files outside the listed units
- no implicit shared modules
- no undeclared contract carriers

STRICT RULE:
- Limits must constrain structure, not semantics.

---

## 8. TRACEABILITY REFERENCES
Reference the BETO authority that justifies this artifact.

Include:
- BETO_CORE sections used
- PHASE documents used
- TRACE_REGISTRY entries most directly related

---

## 9. MATERIALIZATION HANDOFF
State what materialization may safely assume because this artifact exists.

Include:
- structural units frozen
- ownership frozen
- dependency order frozen where declared
- what still remains outside this artifact and must not be assumed

---

## END OF DOCUMENT
