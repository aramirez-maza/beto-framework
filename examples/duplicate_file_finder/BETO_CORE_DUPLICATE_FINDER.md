# BETO_CORE_DUPLICATE_DETECTOR.md

```
Version: 4.2
Last update: 2025-01-31T00:00:00Z
Parent node: GRAPH.ROOT
Graph node: GRAPH.DUPLICATE_DETECTOR
Node type: PARALLEL
Parent edge type: FUNCTIONAL_BRANCH
Upstream dependency: GRAPH.HASHER (DECLARED_DEPENDENCY)
Downstream dependency: GRAPH.SPACE_CALCULATOR (DECLARED_DEPENDENCY)
```

---

## 1. SYSTEM INTENT

The Duplicate Detector receives a collection of File Entries, each carrying a file path, a file size, and a content hash, and groups them by identical content hash. Any group whose membership count is greater than or equal to two represents a confirmed set of duplicate files. The system retains only those groups and discards all singleton entries. Its sole purpose is to produce the authoritative collection of Duplicate Groups that feeds the Space Calculator.

---

## 2. SYSTEM BOUNDARIES

**In scope**

- Accept as input the complete collection of File Entries produced by the Hasher (file_path, file_size, content_hash)
- Group File Entries by content_hash as the sole grouping key
- Retain exclusively groups whose membership count is greater than or equal to two (cardinalidad ≥ 2)
- Discard all File Entries whose content_hash maps to a singleton group (exactly one member)
- Produce for each retained group: the content_hash value, the list of file_paths belonging to the group, and the group_size (file size in bytes shared by all members, derived from file_size of any member in the group, which is identical for all members by definition of content hash equality)
- Preserve file_path and content_hash without modification from input to output
- Emit the complete collection of Duplicate Groups as output

**Out of scope**

- Computing or assigning content_hash values — this is the exclusive responsibility of GRAPH.HASHER
- Computing recoverable space per group or total recoverable space — this is the exclusive responsibility of GRAPH.SPACE_CALCULATOR
- Reading file contents from the filesystem
- Any modification, deletion, or movement of files
- Resolving or validating file paths
- Filtering by file size, file type, or any criterion other than content_hash equality
- Handling symbolic links or permission errors — these are resolved upstream by GRAPH.SCANNER
- Any scheduling, automation, or background execution
- Any behavior not directly implied by grouping by content_hash and filtering by cardinality

---

## 3. INPUTS AND OUTPUTS

**Inputs**

- A collection of File Entries produced by the Hasher phase (GRAPH.HASHER)
- Each File Entry contains exactly three fields as declared in the BETO_CORE_DRAFT and the BETO_SYSTEM_GRAPH:
  - `file_path`: the absolute or relative path of the file within the scanned directory tree
  - `file_size`: the size of the file in bytes
  - `content_hash`: the hash value computed from the full content of the file

The collection is treated as an unordered set. The system must not assume any ordering of the input entries.

The system must treat the collection as complete upon receipt. No streaming, partial processing, or incremental input is declared.

**Outputs**

- A collection of Duplicate Groups
- Each Duplicate Group contains exactly three fields as declared in the BETO_CORE_DRAFT and the BETO_SYSTEM_GRAPH:
  - `content_hash`: the hash value shared by all members of the group
  - `file_paths`: the list of file_path values belonging to the group (minimum two members)
  - `group_size`: the file size in bytes shared by all members of the group

- Only groups with two or more File Entries are present in the output collection
- Singleton File Entries (unique content_hash) are absent from the output collection
- The output collection may be empty if no duplicate groups exist
- The ordering of groups within the collection and of file_paths within each group is not declared (captured as OQ-1)

---

## 4. CORE UNIT OF PROCESSING

The atomic unit processed by the Duplicate Detector is a **File Entry** on input and a **Duplicate Group** on output.

**Input unit — File Entry:**

| Field | Description | Traceability |
|-------|-------------|-------------|
| `file_path` | Absolute or relative path of the discovered file | Must be preserved without modification from Hasher input to Duplicate Group output |
| `file_size` | Size of the file in bytes | Must be preserved and propagated as `group_size` in the output Duplicate Group |
| `content_hash` | Hash value computed from the full file content; serves as the sole grouping key | Must be bound to the exact `file_path` from which it was computed; must not be reassigned |

**Output unit — Duplicate Group:**

| Field | Description | Derivation |
|-------|-------------|------------|
| `content_hash` | The shared hash value of the group | Carried directly from the input File Entries' `content_hash` field |
| `file_paths` | The list of all `file_path` values whose File Entry shares this `content_hash` | Aggregated from input File Entries; minimum two elements |
| `group_size` | The file size in bytes shared by all members | Carried from `file_size` of any member of the group; all members share the same value by content hash equality |

**Traceability fields that must never be lost across phases:**

- `file_path`: must be preserved from the input File Entry through to the `file_paths` list of the output Duplicate Group without modification
- `content_hash`: must be carried from the input File Entry to the `content_hash` field of the output Duplicate Group without modification and without reassignment
- `group_size`: must be traceable to the `file_size` of the originating File Entry; it must not be computed independently

**Grouping invariant:**

Every File Entry present in the input collection must be evaluated. No File Entry may be silently dropped without either being placed into a Duplicate Group (if its content_hash has cardinality ≥ 2) or being discarded as a singleton (if its content_hash has cardinality = 1). Silent loss of File Entries is a traceability violation.

---

## 5. GLOBAL INVARIANTS (BETO RULES)

The following rules must never be violated during system evolution:

- No invention of information
- Non-destructive processing
- Absolute traceability across all phases
- Clear and explicit contracts between phases
- Semantic and epistemic consistency

**ESTADOS EPISTÉMICOS AUTORIZADOS:**
- DECLARED: información explícitamente presente en IDEA_RAW, templates del framework, o respuesta explícita del operador.
- NOT_STATED: información ausente — bloquea ejecución, reportar.
- INFERRED: prohibido a partir del cierre del Paso 1. Autorizado exclusivamente en el PROMPT_CANONICO (Pasos 0 y 1 combinados como frontera de expansión controlada). La frontera se cierra cuando el operador aprueba el BETO_CORE_DRAFT. Usar INFERRED fuera de esta ventana equivale a invención no declarada.

These invariants apply globally and override any phase-specific behavior.

**INVARIANTE DE INICIATIVA CONTROLADA:**
La iniciativa del ejecutor para expandir el universo de la solución existe exclusivamente durante el Paso 0 y el Paso 1 combinados como frontera de expansión controlada. La frontera se cierra cuando el operador aprueba el BETO_CORE_DRAFT. A partir de ese cierre, ningún componente de este sistema puede existir sin una decisión DECLARED que autorice su existencia. La ausencia de declaración no es autorización implícita. Lo "obvio" no es DECLARED. Las "buenas prácticas" no son DECLARED. Los gaps detectados durante la ejecución se registran como BETO_GAP y se resuelven según la REGLA BETO_GAP del INSTRUCTIVO.

**INVARIANTE DE TRAZABILIDAD SEMÁNTICA:**
Toda declaración DECLARED en las Secciones 1 a 8 de este BETO_CORE, y toda OQ resuelta en Sección 9, genera exactamente un ID de trazabilidad autorizado. Ese ID debe registrarse en TRACE_REGISTRY_DUPLICATE_DETECTOR.md durante el Paso 6. Ningún código generado en el Paso 8 puede usar un ID de trazabilidad que no exista en ese registro. La forma autorizada del ID es:
```
BETO_DUPLICATE_DETECTOR.SEC<N>.<TIPO>.<ELEMENTO>
```
donde:
- `NOMBRE_SISTEMA` = `DUPLICATE_DETECTOR`
- `N` = número de sección (1 al 10)
- `TIPO` = categoría del elemento según tabla en BETO_INSTRUCTIVO sección REGLA TRACE_REGISTRY
- `ELEMENTO` = slug del elemento declarado, en mayúsculas

OQs resueltas usan el formato: `OQ-<N>`
Un ID que no siga este formato no es un ID autorizado.

---

## 6. CONCEPTUAL MODEL

The Duplicate Detector occupies the third position in the five-phase pipeline of the Duplicate File Finder CLI. It acts as a semantic filter and aggregator: it receives a flat collection of individually characterized File Entries and transforms it into a structured collection of Duplicate Groups.

The central concept is **content equivalence**: two or more files are considered duplicates if and only if they share an identical content_hash value. The Duplicate Detector does not interpret, validate, or question the content_hash it receives; it treats it as an opaque key whose equality is the sole criterion for grouping.

The transformation has two logical steps:

1. **Aggregation**: All File Entries sharing the same content_hash are collected into a candidate group. The result of this step is a set of candidate groups, each indexed by a unique content_hash, each containing one or more File Entries.

2. **Filtration**: Any candidate group containing exactly one File Entry is a singleton and represents a unique file in the scanned tree. Singletons carry no duplicate information and are discarded. Only candidate groups with two or more File Entries survive filtration and become confirmed Duplicate Groups.

The output Duplicate Group is a minimal, self-contained record: it names the shared hash (content_hash), enumerates the affected paths (file_paths), and carries the shared file size (group_size). The group_size is not a computed value; it is the propagation of the file_size field that was identical across all members by the definition of content hash equality.

The Duplicate Detector has no awareness of the filesystem, no knowledge of how hashes were computed, and no knowledge of how recoverable space will be derived. It operates entirely within the domain of structured data transformation. It is semantically complete with the input collection it receives and the output collection it emits.

**Key relationships:**

- A File Entry belongs to exactly one content_hash equivalence class
- A Duplicate Group corresponds to exactly one content_hash equivalence class with cardinality ≥ 2
- Every file_path in the input collection appears exactly once in the output: either within a Duplicate Group's file_paths list, or discarded as a singleton
- The output collection may be empty (zero Duplicate Groups) if every content_hash in the input maps to a singleton; this is a valid and complete result

---

## 7. PHASE ARCHITECTURE

| Phase | Name | Purpose | Input | Output |
|------:|------|---------|-------|--------|
| 1 | Aggregation | Collect all File Entries into candidate groups indexed by content_hash | Complete collection of File Entries (file_path, file_size, content_hash) | Collection of candidate groups, each indexed by content_hash, each containing one or more File Entries |
| 2 | Filtration | Discard singleton candidate groups; retain only groups with cardinality ≥ 2 | Collection of candidate groups | Collection of confirmed Duplicate Groups (content_hash, [file_paths], group_size) |

This table defines the complete and authoritative phase architecture of the Duplicate Detector component.

**Note on phase contract:**
Phase 1 and Phase 2 are internal logical phases of this component. Their boundary is the candidate group collection, which is an internal artifact. The only externally contracted output of this component is the output of Phase 2: the confirmed Duplicate Group collection. The input to Phase 1 is the only externally contracted input.

---

## 8. STABLE TECHNICAL DECISIONS

- **Grouping key**: Confirmed — the sole grouping key is `content_hash`. No other field (file name, file size, path, modification date) participates in the grouping criterion. This is directly declared in IDEA_RAW ("detects duplicate files by content hash") and in the BETO_CORE_DRAFT (Section 4, Section 6).

- **Cardinality threshold for duplicate confirmation**: Confirmed — a group is confirmed as a Duplicate Group if and only if it contains two or more File Entries (cardinality ≥ 2). Groups with exactly one member are singletons and are discarded. This is declared in the BETO_CORE_DRAFT (Section 6, Section 7 Phase 3) and in the BETO_SYSTEM_GRAPH (Node GRAPH.DUPLICATE_DETECTOR purpose field).

- **group_size derivation**: Confirmed — `group_size` is derived from the `file_size` field of any member of the group. All members of a group share the same `file_size` by the definition of content hash equality: identical content produces identical hash, and identical content implies identical size. This derivation is declared in the BETO_SYSTEM_GRAPH (CAND-03 classification trace) and in Section 4 of this document.

- **Non-destructive execution**: Confirmed — the component must never modify, delete, or move any file. Inherited from BETO_CORE_DRAFT Section 8 global constraint.

- **No filesystem access**: Confirmed — the Duplicate Detector operates exclusively on the structured data collection it receives as input. It must not access the filesystem directly. File content reading is the responsibility of GRAPH.HASHER upstream.

- **Output ordering**: NOT DECLARED — the ordering of Duplicate Groups within the output collection, and the ordering of file_paths within each Duplicate Group, are not specified in IDEA_RAW or the BETO_CORE_DRAFT. Captured as OQ-1. Label: Proposed (pending operator declaration or resolution within this BETO_CORE child).

- **Programming language or runtime**: NOT DECLARED — inherited from OQ-5 of the BETO_CORE_DRAFT. Not resolvable within this BETO_CORE child. Captured as OQ-2 (delegated from parent OQ-5). Label: Proposed (pending operator declaration in BETO_CORE_DUPLICATE_FINDER root).

---

## 9. CURRENT SYSTEM STATE

Phase completed: 0

Phase in progress: 1

**Open questions:**

- **OQ-1**: What ordering, if any, is required for Duplicate Groups within the output collection and for file_paths within each Duplicate Group (e.g., groups ordered by group size descending, by number of duplicates descending, or unordered; file_paths ordered alphabetically, by path depth, or unordered)?
  parent_oq: NONE
  section_origin: Section 3 / Section 8
  oq_type: OQ_POLICY
  critical: NO
  execution_state: DECLARED_WITH_LIMITS
  status: OPEN
  resolution: none
  source: BETO_ASSISTED
  execution_readiness_check: PASS_WITH_LIMITS

- **OQ-2**: In which programming language or runtime must this component be implemented?
  parent_oq: OQ-5 (BETO_CORE_DUPLICATE_FINDER)
  section_origin: Section 8
  oq_type: OQ_CONFIG
  critical: SÍ
  execution_state: PENDING
  status: OPEN
  resolution: none
  source: DELEGATED_TO_DUPLICATE_DETECTOR
  execution_readiness_check: FAIL_EXECUTIONAL_GAP

**BETO_GAP LOG:**

Si no existen BETO_GAPs: ninguno declarado

---

## 10. RISKS AND CONSTRAINTS

- **Risk R-1 — Empty input collection**: The Hasher may produce an empty File Entry collection if the Scanner found no files. The Duplicate Detector must handle an empty input gracefully and emit an empty Duplicate Group collection as a valid and complete result. No error or abort behavior is declared for this case.

- **Risk R-2 — All entries are singletons**: The input collection may contain File Entries where every content_hash maps to exactly one file. In this case, all candidate groups are discarded at the filtration phase and the output is an empty Duplicate Group collection. This is a valid result and must not be treated as an error.

- **Risk R-3 — Hash collision propagation**: If the upstream Hasher produces a hash collision (two files with different content yielding the same hash), the Duplicate Detector will group those files as duplicates. The Duplicate Detector has no mechanism to detect or correct collisions; it treats content_hash as an authoritative equivalence key. The risk severity is inherited from OQ-1 of the BETO_CORE_DRAFT (algorithm selection) and is not manageable within this component's scope.

- **Risk R-4 — Large input collections**: A very large File Entry collection may result in high memory usage during the aggregation phase. No performance requirements or memory limits are declared in IDEA_RAW or the BETO_CORE_DRAFT.

- **Constraint C-1 — Non-destructive execution**: The component must never modify, delete, or move any file. Hard constraint inherited from BETO_CORE_DRAFT Section 8.

- **Constraint C-2 — Completeness of grouping**: Every File Entry in the input collection must be evaluated. Silent loss of any File Entry is a traceability violation per the Grouping Invariant declared in Section 4.

- **Constraint C-3 — Sole grouping key**: The grouping criterion is exclusively content_hash equality. No secondary grouping criterion may be introduced without an explicit DECLARED authorization.

- **Constraint C-4 — No filesystem access**: This component must not access the filesystem. All data required for processing is present in the input collection. Direct filesystem access would violate the phase contract with GRAPH.HASHER.

- **Constraint C-5 — Output contract completeness**: Every Duplicate Group in the output collection must contain all three declared fields: content_hash, file_paths (minimum two elements), and group_size. Omitting any field constitutes an incomplete output and a contract violation with GRAPH.SPACE_CALCULATOR.