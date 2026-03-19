# TRACE_REGISTRY_DUPLICATE_FINDER.md

## METADATA

```
Registry name:           TRACE_REGISTRY_DUPLICATE_FINDER
System name:             DUPLICATE_FINDER
Source BETO_CORE:        BETO_CORE_DUPLICATE_FINDER.md
Registry version:        1.0.0
Generation timestamp:    2025-01-31T00:00:00Z
Pattern:                 BETO_DUPLICATE_FINDER.SEC<N>.<TIPO>.<ELEMENTO>
```

---

## AUTHORIZED ID CATALOG

---

### SECTION 1 — SYSTEM INTENT

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC1.INTENT.CLI_TOOL | INTENT | CLI_TOOL | A CLI tool is the system being created |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.RECURSIVE_SCAN | INTENT | RECURSIVE_SCAN | The tool scans a target directory recursively |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.CONTENT_HASH_DETECTION | INTENT | CONTENT_HASH_DETECTION | Duplicate identification is performed by comparing content hashes |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.REPORT_GENERATION | INTENT | REPORT_GENERATION | The tool produces a report as its primary output |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.DUPLICATE_GROUPS | INTENT | DUPLICATE_GROUPS | The report exposes duplicate groups |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.FILE_PATHS | INTENT | FILE_PATHS | The report exposes file paths belonging to each group |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.RECOVERABLE_SPACE | INTENT | RECOVERABLE_SPACE | The report exposes total recoverable disk space |
| BETO_DUPLICATE_FINDER.SEC1.INTENT.LOCAL_FILESYSTEM | INTENT | LOCAL_FILESYSTEM | The system operates on a local filesystem |

---

### SECTION 2 — SYSTEM BOUNDARIES

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC2.INSCOPE.ACCEPT_TARGET_DIR | INSCOPE | ACCEPT_TARGET_DIR | Accept a target directory as input from the command line |
| BETO_DUPLICATE_FINDER.SEC2.INSCOPE.RECURSIVE_TRAVERSAL | INSCOPE | RECURSIVE_TRAVERSAL | Traverse the target directory recursively |
| BETO_DUPLICATE_FINDER.SEC2.INSCOPE.COMPUTE_CONTENT_HASH | INSCOPE | COMPUTE_CONTENT_HASH | Compute a content hash for each discovered file |
| BETO_DUPLICATE_FINDER.SEC2.INSCOPE.GROUP_BY_HASH | INSCOPE | GROUP_BY_HASH | Group files that share an identical content hash |
| BETO_DUPLICATE_FINDER.SEC2.INSCOPE.CALCULATE_RECOVERABLE_SPACE | INSCOPE | CALCULATE_RECOVERABLE_SPACE | Calculate the total recoverable space represented by duplicate files |
| BETO_DUPLICATE_FINDER.SEC2.INSCOPE.GENERATE_REPORT | INSCOPE | GENERATE_REPORT | Generate a report containing duplicate groups, file paths per group, and total recoverable space |
| BETO_DUPLICATE_FINDER.SEC2.OUTSCOPE.NO_DELETION | OUTSCOPE | NO_DELETION | Deletion or modification of any file is out of scope |
| BETO_DUPLICATE_FINDER.SEC2.OUTSCOPE.NO_DEDUPLICATION | OUTSCOPE | NO_DEDUPLICATION | Deduplication or any destructive action on the filesystem is out of scope |
| BETO_DUPLICATE_FINDER.SEC2.OUTSCOPE.NO_REMOTE_PATHS | OUTSCOPE | NO_REMOTE_PATHS | Scanning remote or network-mounted paths is out of scope unless explicitly declared |
| BETO_DUPLICATE_FINDER.SEC2.OUTSCOPE.NO_SYMLINK_RESOLUTION | OUTSCOPE | NO_SYMLINK_RESOLUTION | Resolution of symbolic links, hard links, or special files is out of scope unless explicitly declared |
| BETO_DUPLICATE_FINDER.SEC2.OUTSCOPE.NO_SCHEDULING | OUTSCOPE | NO_SCHEDULING | Scheduling, automation, or background execution is out of scope |

---

### SECTION 3 — INPUTS AND OUTPUTS

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC3.INPUT.TARGET_DIRECTORY_PATH | INPUT | TARGET_DIRECTORY_PATH | A single target directory path provided as a CLI argument |
| BETO_DUPLICATE_FINDER.SEC3.INPUT.RECURSIVE_FILE_SET | INPUT | RECURSIVE_FILE_SET | All files reachable by recursive traversal of the target directory |
| BETO_DUPLICATE_FINDER.SEC3.OUTPUT.REPORT_ARTIFACT | OUTPUT | REPORT_ARTIFACT | A report artifact is the declared output of the system |
| BETO_DUPLICATE_FINDER.SEC3.OUTPUT.REPORT_DUPLICATE_GROUPS | OUTPUT | REPORT_DUPLICATE_GROUPS | The report contains one or more duplicate groups |
| BETO_DUPLICATE_FINDER.SEC3.OUTPUT.REPORT_FILE_PATHS_PER_GROUP | OUTPUT | REPORT_FILE_PATHS_PER_GROUP | For each group the report contains the list of file paths sharing the same content hash |
| BETO_DUPLICATE_FINDER.SEC3.OUTPUT.REPORT_TOTAL_RECOVERABLE_SPACE | OUTPUT | REPORT_TOTAL_RECOVERABLE_SPACE | The report contains the total recoverable disk space across all duplicate groups |
| BETO_DUPLICATE_FINDER.SEC3.OQ.REPORT_FORMAT | OQ | REPORT_FORMAT | Report format, delivery channel, and structure are not declared — captured as OQ-6 |

---

### SECTION 4 — CORE UNIT OF PROCESSING

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC4.UNIT.FILE_ENTRY | UNIT | FILE_ENTRY | The atomic unit processed by the system is a discovered file entry |
| BETO_DUPLICATE_FINDER.SEC4.FIELD.FILE_PATH | FIELD | FILE_PATH | file_path: absolute or relative path of the file within the scanned directory tree |
| BETO_DUPLICATE_FINDER.SEC4.FIELD.CONTENT_HASH | FIELD | CONTENT_HASH | content_hash: hash value computed from the full content of the file, used as grouping key |
| BETO_DUPLICATE_FINDER.SEC4.FIELD.FILE_SIZE | FIELD | FILE_SIZE | file_size: size of the file in bytes, required to compute recoverable space per group |
| BETO_DUPLICATE_FINDER.SEC4.INVARIANT.FILE_PATH_PRESERVED | INVARIANT | FILE_PATH_PRESERVED | file_path must be preserved from discovery through reporting without modification |
| BETO_DUPLICATE_FINDER.SEC4.INVARIANT.CONTENT_HASH_BOUND | INVARIANT | CONTENT_HASH_BOUND | content_hash must be bound to the exact file_path from which it was computed and must not be reassigned |
| BETO_DUPLICATE_FINDER.SEC4.OQ.HASHING_ALGORITHM | OQ | HASHING_ALGORITHM | The hashing algorithm is not declared — captured as OQ-1 |
| BETO_DUPLICATE_FINDER.SEC4.OQ.SIZE_PREFILTER | OQ | SIZE_PREFILTER | Whether a pre-filter by file size before hashing is implied is not declared — captured as OQ-2 |
| BETO_DUPLICATE_FINDER.SEC4.OQ.ZERO_BYTE_FILES | OQ | ZERO_BYTE_FILES | Whether zero-byte files are included or excluded is not declared — captured as OQ-3 |
| BETO_DUPLICATE_FINDER.SEC4.OQ.SYMLINK_TRAVERSAL | OQ | SYMLINK_TRAVERSAL | Whether symbolic links are followed during traversal is not declared — captured as OQ-4 |

---

### SECTION 5 — GLOBAL INVARIANTS

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC5.INVARIANT.NO_INVENTION | INVARIANT | NO_INVENTION | No invention of information |
| BETO_DUPLICATE_FINDER.SEC5.INVARIANT.NON_DESTRUCTIVE | INVARIANT | NON_DESTRUCTIVE | Non-destructive processing |
| BETO_DUPLICATE_FINDER.SEC5.INVARIANT.ABSOLUTE_TRACEABILITY | INVARIANT | ABSOLUTE_TRACEABILITY | Absolute traceability across all phases |
| BETO_DUPLICATE_FINDER.SEC5.INVARIANT.EXPLICIT_CONTRACTS | INVARIANT | EXPLICIT_CONTRACTS | Clear and explicit contracts between phases |
| BETO_DUPLICATE_FINDER.SEC5.INVARIANT.SEMANTIC_CONSISTENCY | INVARIANT | SEMANTIC_CONSISTENCY | Semantic and epistemic consistency |

---

### SECTION 6 — CONCEPTUAL MODEL

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC6.COMPONENT.SCANNER | COMPONENT | SCANNER | Scanner traverses the directory tree and produces a flat collection of File Entries |
| BETO_DUPLICATE_FINDER.SEC6.COMPONENT.DUPLICATE_DETECTOR | COMPONENT | DUPLICATE_DETECTOR | Duplicate Detector groups File Entries by content hash; groups with more than one entry are duplicates |
| BETO_DUPLICATE_FINDER.SEC6.COMPONENT.SPACE_CALCULATOR | COMPONENT | SPACE_CALCULATOR | Space Calculator derives recoverable space per group: file_size × (total copies minus one) |
| BETO_DUPLICATE_FINDER.SEC6.COMPONENT.REPORT_COMPOSER | COMPONENT | REPORT_COMPOSER | Report Composer receives duplicate groups and space calculation and produces the final output artifact |
| BETO_DUPLICATE_FINDER.SEC6.CONSTRAINT.REPORT_ONLY_SIDE_EFFECT | CONSTRAINT | REPORT_ONLY_SIDE_EFFECT | The only persistent side effect of the system is the report; the scanned filesystem is never modified |

---

### SECTION 7 — PHASE ARCHITECTURE

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC7.PHASE.DISCOVERY | PHASE | DISCOVERY | Phase 1: Recursively traverse the target directory and produce the complete set of File Entries with path and size |
| BETO_DUPLICATE_FINDER.SEC7.PHASE.HASHING | PHASE | HASHING | Phase 2: Compute the content hash for each File Entry |
| BETO_DUPLICATE_FINDER.SEC7.PHASE.GROUPING | PHASE | GROUPING | Phase 3: Group File Entries by content hash; retain only groups with more than one member |
| BETO_DUPLICATE_FINDER.SEC7.PHASE.SPACE_CALCULATION | PHASE | SPACE_CALCULATION | Phase 4: Compute recoverable space per group and total recoverable space across all groups |
| BETO_DUPLICATE_FINDER.SEC7.PHASE.REPORT_GENERATION | PHASE | REPORT_GENERATION | Phase 5: Compose and emit the final report from the annotated duplicate groups |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE1_INPUT | CONTRACT | PHASE1_INPUT | Phase 1 input: target directory path (CLI argument) |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE1_OUTPUT | CONTRACT | PHASE1_OUTPUT | Phase 1 output: collection of File Entries (path, size) |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE2_INPUT | CONTRACT | PHASE2_INPUT | Phase 2 input: collection of File Entries (path, size) |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE2_OUTPUT | CONTRACT | PHASE2_OUTPUT | Phase 2 output: collection of File Entries (path, size, content_hash) |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE3_INPUT | CONTRACT | PHASE3_INPUT | Phase 3 input: collection of File Entries (path, size, content_hash) |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE3_OUTPUT | CONTRACT | PHASE3_OUTPUT | Phase 3 output: collection of Duplicate Groups (content_hash, [file_paths], group_size) |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE4_INPUT | CONTRACT | PHASE4_INPUT | Phase 4 input: collection of Duplicate Groups |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE4_OUTPUT | CONTRACT | PHASE4_OUTPUT | Phase 4 output: Duplicate Groups annotated with recoverable_bytes; total_recoverable_bytes |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE5_INPUT | CONTRACT | PHASE5_INPUT | Phase 5 input: annotated Duplicate Groups; total_recoverable_bytes |
| BETO_DUPLICATE_FINDER.SEC7.CONTRACT.PHASE5_OUTPUT | CONTRACT | PHASE5_OUTPUT | Phase 5 output: report artifact |

---

### SECTION 8 — STABLE TECHNICAL DECISIONS

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC8.DECISION.CLI_ARGUMENT_INTERFACE | DECISION | CLI_ARGUMENT_INTERFACE | The system exposes a CLI that accepts at minimum a target directory path as an argument — CONFIRMED |
| BETO_DUPLICATE_FINDER.SEC8.DECISION.NON_DESTRUCTIVE_EXECUTION | DECISION | NON_DESTRUCTIVE_EXECUTION | The system must never modify, delete, or move any file during execution — CONFIRMED |
| BETO_DUPLICATE_FINDER.SEC8.OQ.LANGUAGE_RUNTIME | OQ | LANGUAGE_RUNTIME | No programming language or runtime is specified — captured as OQ-5 |
| BETO_DUPLICATE_FINDER.SEC8.OQ.HASHING_ALGORITHM | OQ | HASHING_ALGORITHM | The hashing algorithm is not specified — captured as OQ-1 (cross-reference Section 4) |
| BETO_DUPLICATE_FINDER.SEC8.OQ.REPORT_OUTPUT_FORMAT | OQ | REPORT_OUTPUT_FORMAT | Report output format and delivery channel are not specified — captured as OQ-6 |

---

### SECTION 9 — CURRENT SYSTEM STATE (OPEN QUESTIONS)

| ID | Type | Element | OQ status | Critical |
|----|------|---------|-----------|---------|
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-1 | OQ | OQ-1 | OPEN | SÍ |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-2 | OQ | OQ-2 | OPEN | NO |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-3 | OQ | OQ-3 | OPEN | NO |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-4 | OQ | OQ-4 | OPEN | SÍ |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-5 | OQ | OQ-5 | OPEN | SÍ |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-6 | OQ | OQ-6 | OPEN | SÍ |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-7 | OQ | OQ-7 | OPEN | NO |
| BETO_DUPLICATE_FINDER.SEC9.OQ.OQ-8 | OQ | OQ-8 | OPEN | SÍ |

---

### SECTION 10 — RISKS AND CONSTRAINTS

| ID | Type | Element | Declaration summary |
|----|------|---------|-------------------|
| BETO_DUPLICATE_FINDER.SEC10.RISK.PERMISSION_ERRORS | RISK | PERMISSION_ERRORS | R-1: Files or subdirectories with restricted read permissions may cause incomplete scan results or crashes |
| BETO_DUPLICATE_FINDER.SEC10.RISK.HASH_COLLISION | RISK | HASH_COLLISION | R-2: Any hashing algorithm carries theoretical collision risk; severity depends on OQ-1 resolution |
| BETO_DUPLICATE_FINDER.SEC10.RISK.LARGE_DIRECTORY_TREES | RISK | LARGE_DIRECTORY_TREES | R-3: Very large directory trees may cause high memory usage and long execution times |
| BETO_DUPLICATE_FINDER.SEC10.CONSTRAINT.NON_DESTRUCTIVE | CONSTRAINT | NON_DESTRUCTIVE | C-1: The system must never modify, delete, or move any file — hard constraint |
| BETO_DUPLICATE_FINDER.SEC10.CONSTRAINT.RECURSIVE_SCOPE | CONSTRAINT | RECURSIVE_SCOPE | C-2: The system must scan the entire subtree rooted at the target directory; partial traversal is invalid |
| BETO_DUPLICATE_FINDER.SEC10.CONSTRAINT.REPORT_COMPLETENESS | CONSTRAINT | REPORT_COMPLETENESS | C-3: The report must include all three declared output elements: duplicate groups, file paths per group, and total recoverable space |

---

## ID COUNT SUMMARY

```
Section 1  — SYSTEM INTENT:              8 IDs
Section 2  — SYSTEM BOUNDARIES:         11 IDs
Section 3  — INPUTS AND OUTPUTS:         7 IDs
Section 4  — CORE UNIT OF PROCESSING:   10 IDs
Section 5  — GLOBAL INVARIANTS:          5 IDs
Section 6  — CONCEPTUAL MODEL:           5 IDs
Section 7  — PHASE ARCHITECTURE:        15 IDs
Section 8  — STABLE TECHNICAL DECISIONS: 5 IDs
Section 9  — OPEN QUESTIONS:             8 IDs
Section 10 — RISKS AND CONSTRAINTS:      6 IDs

TOTAL AUTHORIZED IDs:                   80
```

---

## AUTHORIZATION RULE

Ningún código generado en el Paso 8 puede usar un ID de trazabilidad
que no figure en este registro. Todo ID referenciado en artefactos
derivados debe coincidir exactamente con la forma declarada en este
catálogo. La adición de nuevos IDs requiere actualización de este
registro antes de su uso.

---

## CHANGELOG

```
2025-01-31T00:00:00Z  Registry created from BETO_CORE_DUPLICATE_FINDER.md
2025-01-31T00:00:00Z  Section 1 populated: 8 IDs
2025-01-31T00:00:00Z  Section 2 populated: 11 IDs
2025-01-31T00:00:00Z  Section 3 populated: 7 IDs
2025-01-31T00:00:00Z  Section 4 populated: 10 IDs
2025-01-31T00:00:00Z  Section 5 populated: 5 IDs
2025-01-31T00:00:00Z  Section 6 populated: 5 IDs
2025-01-31T00:00:00Z  Section 7 populated: 15 IDs
2025-01-31T00:00:00Z  Section 8 populated: 5 IDs
2025-01-31T00:00:00Z  Section 9 populated: 8 IDs
2025-01-31T00:00:00Z  Section 10 populated: 6 IDs
2025-01-31T00:00:00Z  Total: 80 authorized IDs
2025-01-31T00:00:00Z  Registry status: COMPLETE
```