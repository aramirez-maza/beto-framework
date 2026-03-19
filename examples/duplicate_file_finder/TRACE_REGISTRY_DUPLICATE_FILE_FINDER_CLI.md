# TRACE_REGISTRY_DUPLICATE_FILE_FINDER_CLI.md

## METADATA

```
Registry name:         TRACE_REGISTRY_DUPLICATE_FILE_FINDER_CLI.md
System name:           DUPLICATE_FILE_FINDER_CLI
Source BETO_CORE:      BETO_CORE_DUPLICATE_FINDER.md
Generation timestamp:  2025-01-31T00:00:00Z
Registry version:      1.0.0
Registry status:       DRAFT
```

---

## AUTHORITY RULE

Todo ID registrado en este documento fue derivado de una declaración
DECLARED presente en las Secciones 1 a 10 del BETO_CORE_DUPLICATE_FINDER.md,
o de una OQ registrada en la Sección 9 del mismo documento.

Formato autorizado:

```
BETO_DUPLICATE_FILE_FINDER_CLI.SEC<N>.<TIPO>.<ELEMENTO>
```

Ningún código generado en el Paso 8 puede usar un ID de trazabilidad
que no exista en este registro.

---

## TIPO CATALOG

```
INTENT       Declaración de propósito o intención del sistema
BOUNDARY     Declaración de alcance: in scope o out of scope
INPUT        Elemento de entrada declarado
OUTPUT       Elemento de salida declarado
FIELD        Campo del core unit of processing
INVARIANT    Regla global que nunca puede violarse
EPISTEMIC    Estado epistémico autorizado
COMPONENT    Componente del modelo conceptual
PHASE        Fase de la arquitectura de fases
DECISION     Decisión técnica estable
RISK         Riesgo declarado
CONSTRAINT   Restricción declarada
OQ           Open question registrada
```

---

## SECTION 1 — SYSTEM INTENT

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.CLI_TOOL
  Source section: Section 1
  Declaration: A CLI tool that scans a target directory recursively,
               identifies duplicate files by comparing their content
               hashes, and produces a report that exposes duplicate
               groups, the file paths belonging to each group, and
               the total recoverable disk space.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC1.INTENT.TARGET_USERS
  Source section: Section 1
  Declaration: The system serves users who need to detect and quantify
               file duplication within a local filesystem.
  Status: DECLARED
```

---

## SECTION 2 — SYSTEM BOUNDARIES

### In Scope

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.ACCEPT_TARGET_DIR
  Source section: Section 2 — In scope
  Declaration: Accept a target directory as input from the command line.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.RECURSIVE_TRAVERSAL
  Source section: Section 2 — In scope
  Declaration: Traverse the target directory recursively.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.COMPUTE_CONTENT_HASH
  Source section: Section 2 — In scope
  Declaration: Compute a content hash for each discovered file.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.GROUP_BY_HASH
  Source section: Section 2 — In scope
  Declaration: Group files that share an identical content hash.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.CALCULATE_RECOVERABLE_SPACE
  Source section: Section 2 — In scope
  Declaration: Calculate the total recoverable space represented by
               duplicate files.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.GENERATE_REPORT
  Source section: Section 2 — In scope
  Declaration: Generate a report containing duplicate groups, file paths
               per group, and total recoverable space.
  Status: DECLARED
```

### Out of Scope

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.NO_DELETION
  Source section: Section 2 — Out of scope
  Declaration: Deletion or modification of any file is out of scope.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.NO_DEDUPLICATION
  Source section: Section 2 — Out of scope
  Declaration: Deduplication or any destructive action on the filesystem
               is out of scope.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.NO_REMOTE_PATHS
  Source section: Section 2 — Out of scope
  Declaration: Scanning remote or network-mounted paths unless explicitly
               declared is out of scope.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.NO_UNDECLARED_BEHAVIOR
  Source section: Section 2 — Out of scope
  Declaration: Any behavior not directly implied by scan, detect, and
               report is out of scope.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.NO_SYMLINK_HARDLINK
  Source section: Section 2 — Out of scope
  Declaration: Resolution of symbolic links, hard links, or special files
               unless explicitly declared is out of scope.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC2.BOUNDARY.NO_SCHEDULING
  Source section: Section 2 — Out of scope
  Declaration: Any scheduling, automation, or background execution is
               out of scope.
  Status: DECLARED
```

---

## SECTION 3 — INPUTS AND OUTPUTS

### Inputs

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.INPUT.TARGET_DIR_PATH
  Source section: Section 3 — Inputs
  Declaration: A single target directory path provided as a CLI argument.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.INPUT.RECURSIVE_FILES
  Source section: Section 3 — Inputs
  Declaration: All files reachable by recursive traversal of that
               directory.
  Status: DECLARED
```

### Outputs

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.OUTPUT.REPORT_ARTIFACT
  Source section: Section 3 — Outputs
  Declaration: A report artifact containing one or more duplicate groups,
               for each group the list of file paths that share the same
               content hash, and the total recoverable disk space across
               all duplicate groups.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.OUTPUT.DUPLICATE_GROUPS
  Source section: Section 3 — Outputs
  Declaration: One or more duplicate groups included in the report.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.OUTPUT.FILE_PATHS_PER_GROUP
  Source section: Section 3 — Outputs
  Declaration: For each group: the list of file paths that share the
               same content hash.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC3.OUTPUT.TOTAL_RECOVERABLE_SPACE
  Source section: Section 3 — Outputs
  Declaration: The total recoverable disk space across all duplicate
               groups.
  Status: DECLARED
```

---

## SECTION 4 — CORE UNIT OF PROCESSING

### Fields

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.FIELD.FILE_PATH
  Source section: Section 4
  Declaration: The absolute or relative path of the file within the
               scanned directory tree. Required for processing as
               explicitly stated.
  Traceability note: Must be preserved from discovery through reporting
                     without modification.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.FIELD.CONTENT_HASH
  Source section: Section 4
  Declaration: The hash value computed from the full content of the
               file, used as the grouping key for duplicate detection.
  Traceability note: Must be bound to the exact file_path from which
                     it was computed and must not be reassigned.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.FIELD.FILE_SIZE
  Source section: Section 4
  Declaration: The size of the file in bytes, required to compute
               recoverable space per duplicate group.
  Status: DECLARED
```

### Open Questions on Core Unit

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.OQ.OQ-1
  Source section: Section 4
  Declaration: The hashing algorithm (e.g., MD5, SHA-1, SHA-256, BLAKE2)
               is not declared.
  OQ reference: OQ-1
  Status: OPEN

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.OQ.OQ-2
  Source section: Section 4
  Declaration: Whether a pre-filter by file size before hashing is
               implied is not declared.
  OQ reference: OQ-2
  Status: OPEN

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.OQ.OQ-3
  Source section: Section 4
  Declaration: Whether zero-byte files are included or excluded is
               not declared.
  OQ reference: OQ-3
  Status: OPEN

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC4.OQ.OQ-4
  Source section: Section 4
  Declaration: Whether symbolic links are followed during traversal
               is not declared.
  OQ reference: OQ-4
  Status: OPEN
```

---

## SECTION 5 — GLOBAL INVARIANTS (BETO RULES)

### Invariants

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.NO_INVENTION
  Source section: Section 5
  Declaration: No invention of information. Must never be violated
               during system evolution.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.NON_DESTRUCTIVE
  Source section: Section 5
  Declaration: Non-destructive processing. Must never be violated
               during system evolution.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.ABSOLUTE_TRACEABILITY
  Source section: Section 5
  Declaration: Absolute traceability across all phases. Must never be
               violated during system evolution.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.EXPLICIT_CONTRACTS
  Source section: Section 5
  Declaration: Clear and explicit contracts between phases. Must never
               be violated during system evolution.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.SEMANTIC_CONSISTENCY
  Source section: Section 5
  Declaration: Semantic and epistemic consistency. Must never be
               violated during system evolution.
  Status: DECLARED
```

### Epistemic States

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.EPISTEMIC.DECLARED
  Source section: Section 5
  Declaration: DECLARED — información explícitamente presente en
               IDEA_RAW, templates del framework, o respuesta explícita
               del operador.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.EPISTEMIC.NOT_STATED
  Source section: Section 5
  Declaration: NOT_STATED — información ausente; bloquea ejecución,
               reportar.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.EPISTEMIC.INFERRED
  Source section: Section 5
  Declaration: INFERRED — prohibido a partir del cierre del Paso 1.
               Autorizado exclusivamente en el PROMPT_CANONICO (Pasos
               0 y 1 combinados como frontera de expansión controlada).
  Status: DECLARED
```

### Controlled Initiative Invariant

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.CONTROLLED_INITIATIVE
  Source section: Section 5
  Declaration: La iniciativa del ejecutor para expandir el universo de
               la solución existe exclusivamente durante el Paso 0 y el
               Paso 1 combinados como frontera de expansión controlada.
               La frontera se cierra cuando el operador aprueba el
               BETO_CORE_DRAFT. A partir de ese cierre, ningún componente
               puede existir sin una decisión DECLARED que autorice su
               existencia.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.BETO_GAP_RULE
  Source section: Section 5
  Declaration: Los gaps detectados durante la ejecución se registran
               como BETO_GAP y se resuelven según la REGLA BETO_GAP
               del INSTRUCTIVO.
  Status: DECLARED
```

### Semantic Traceability Invariant

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC5.INVARIANT.TRACE_REGISTRY_BINDING
  Source section: Section 5
  Declaration: Toda declaración DECLARED en las Secciones 1 a 8 de este
               BETO_CORE, y toda OQ resuelta en Sección 9, genera
               exactamente un ID de trazabilidad autorizado que debe
               registrarse en TRACE_REGISTRY. Ningún código generado en
               el Paso 8 puede usar un ID que no exista en este registro.
  Status: DECLARED
```

---

## SECTION 6 — CONCEPTUAL MODEL

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.SCANNER
  Source section: Section 6
  Declaration: A Scanner traverses the directory tree and produces a
               flat collection of File Entries. Each File Entry carries
               a path and a content hash.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.FILE_ENTRY
  Source section: Section 6
  Declaration: The unit produced by the Scanner. Carries a path and a
               content hash.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.DUPLICATE_DETECTOR
  Source section: Section 6
  Declaration: A Duplicate Detector groups File Entries by content hash;
               any group containing more than one entry represents a set
               of duplicate files.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.SPACE_CALCULATOR
  Source section: Section 6
  Declaration: A Space Calculator derives the recoverable space for each
               duplicate group by multiplying the file size by the count
               of redundant copies (total copies minus one).
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.REPORT_COMPOSER
  Source section: Section 6
  Declaration: A Report Composer receives the collection of duplicate
               groups and the space calculation and produces the final
               output artifact.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.LOCAL_FILESYSTEM
  Source section: Section 6
  Declaration: The system operates on a local filesystem rooted at a
               user-supplied directory.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC6.COMPONENT.REPORT_SIDE_EFFECT
  Source section: Section 6
  Declaration: The only persistent side effect of the system is the
               report; the scanned filesystem is never modified.
  Status: DECLARED
```

---

## SECTION 7 — PHASE ARCHITECTURE

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.DISCOVERY
  Source section: Section 7 — Phase 1
  Declaration: Phase 1 — Discovery. Recursively traverse the target
               directory and produce the complete set of File Entries
               with path and size.
  Input:  Target directory path (CLI argument)
  Output: Collection of File Entries (path, size)
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.HASHING
  Source section: Section 7 — Phase 2
  Declaration: Phase 2 — Hashing. Compute the content hash for each
               File Entry.
  Input:  Collection of File Entries (path, size)
  Output: Collection of File Entries (path, size, content_hash)
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.GROUPING
  Source section: Section 7 — Phase 3
  Declaration: Phase 3 — Grouping. Group File Entries by content hash;
               retain only groups with more than one member.
  Input:  Collection of File Entries (path, size, content_hash)
  Output: Collection of Duplicate Groups (content_hash, [file_paths],
          group_size)
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.SPACE_CALCULATION
  Source section: Section 7 — Phase 4
  Declaration: Phase 4 — Space Calculation. Compute recoverable space
               per group and total recoverable space across all groups.
  Input:  Collection of Duplicate Groups
  Output: Duplicate Groups annotated with recoverable_bytes;
          total_recoverable_bytes
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC7.PHASE.REPORT_GENERATION
  Source section: Section 7 — Phase 5
  Declaration: Phase 5 — Report Generation. Compose and emit the final
               report from the annotated duplicate groups.
  Input:  Annotated Duplicate Groups; total_recoverable_bytes
  Output: Report artifact
  Status: DECLARED
```

---

## SECTION 8 — STABLE TECHNICAL DECISIONS

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC8.DECISION.LANGUAGE_RUNTIME
  Source section: Section 8
  Declaration: Language or runtime — NOT DECLARED. No programming
               language or runtime is specified in IDEA_RAW.
  OQ reference: OQ-5
  Status: NOT_STATED — OPEN (pending operator declaration)

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC8.DECISION.HASHING_ALGORITHM
  Source section: Section 8
  Declaration: Hashing algorithm — NOT DECLARED. The algorithm used
               to compute content_hash is not specified.
  OQ reference: OQ-1
  Status: NOT_STATED — OPEN (pending operator declaration)

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC8.DECISION.REPORT_OUTPUT_FORMAT
  Source section: Section 8
  Declaration: Report output format — NOT DECLARED. Whether the report
               is emitted to stdout, written to a file, or both, and in
               what structure, is not specified.
  OQ reference: OQ-6
  Status: NOT_STATED — OPEN (pending operator declaration)

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC8.DECISION.CLI_ARGUMENT_INTERFACE
  Source section: Section 8
  Declaration: CLI argument interface — Confirmed. The system exposes
               a command-line interface that accepts at minimum a target
               directory path as an argument, as explicitly stated in
               IDEA_RAW.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC8.DECISION.NON_DESTRUCTIVE_EXECUTION
  Source section: Section 8
  Declaration: Non-destructive execution — Confirmed. The system must
               never modify, delete, or move any file during execution,
               as implied by the scan-and-report intent of IDEA_RAW.
  Status: DECLARED
```

---

## SECTION 9 — CURRENT SYSTEM STATE (OPEN QUESTIONS)

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-1
  Source section: Section 9
  OQ ID: OQ-1
  Declaration: Which hashing algorithm must be used to compute the
               content hash of each file (e.g., MD5, SHA-1, SHA-256,
               BLAKE2b)?
  oq_type: OQ_CONFIG
  critical: SÍ
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-2
  Source section: Section 9
  OQ ID: OQ-2
  Declaration: Should files be pre-filtered by size before hashing
               (i.e., skip hashing for files whose size is unique
               across the tree) to optimize performance?
  oq_type: OQ_POLICY
  critical: NO
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: NOT_EVALUATED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-3
  Source section: Section 9
  OQ ID: OQ-3
  Declaration: Should zero-byte files be included in the duplicate
               detection process or excluded?
  oq_type: OQ_POLICY
  critical: NO
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: NOT_EVALUATED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-4
  Source section: Section 9
  OQ ID: OQ-4
  Declaration: Should the scanner follow symbolic links during recursive
               traversal, or skip them?
  oq_type: OQ_POLICY
  critical: SÍ
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-5
  Source section: Section 9
  OQ ID: OQ-5
  Declaration: In which programming language or runtime must the CLI
               tool be implemented?
  oq_type: OQ_CONFIG
  critical: SÍ
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-6
  Source section: Section 9
  OQ ID: OQ-6
  Declaration: What is the required output format and delivery channel
               for the report (e.g., plain text to stdout, JSON file,
               CSV file, human-readable file)? Must the report include
               a summary section separate from the group listing?
  oq_type: OQ_INTERFACE
  critical: SÍ
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-7
  Source section: Section 9
  OQ ID: OQ-7
  Declaration: Should the tool support additional CLI options beyond the
               target directory path (e.g., --output file path,
               --min-size threshold, --exclude patterns, --verbose)?
  oq_type: OQ_INTERFACE
  critical: NO
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: NOT_EVALUATED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-8
  Source section: Section 9
  OQ ID: OQ-8
  Declaration: How should the tool behave when it encounters files it
               cannot read due to permission errors during traversal or
               hashing (skip silently, skip with warning, abort)?
  oq_type: OQ_EXCEPTION
  critical: SÍ
  execution_state: PENDING
  status: OPEN
  execution_readiness_check: FAIL_EXECUTIONAL_GAP
```

---

## SECTION 10 — RISKS AND CONSTRAINTS

### Risks

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R1_PERMISSION_ERRORS
  Source section: Section 10
  Declaration: Risk R-1 — Permission errors during traversal. The tool
               operates on a user-supplied directory that may contain
               files or subdirectories with restricted read permissions.
               If unhandled, this will cause incomplete scan results or
               tool crashes. Behavior on permission errors is not
               declared (see OQ-8).
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R2_HASH_COLLISION
  Source section: Section 10
  Declaration: Risk R-2 — Hash collision. Any hashing algorithm carries
               a theoretical risk of collision, meaning two files with
               different content could produce the same hash and be
               incorrectly grouped as duplicates. Severity depends on
               OQ-1 resolution.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.RISK.R3_LARGE_DIRECTORY_TREES
  Source section: Section 10
  Declaration: Risk R-3 — Large directory trees. Recursively scanning a
               very large directory tree and computing content hashes for
               all files may result in high memory usage and long
               execution times. No performance requirements or limits are
               declared in IDEA_RAW.
  Status: DECLARED
```

### Constraints

```
ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C1_NON_DESTRUCTIVE
  Source section: Section 10
  Declaration: Constraint C-1 — Non-destructive execution. The system
               must never modify, delete, or move any file. This is a
               hard constraint directly implied by the scan-and-report
               intent.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C2_RECURSIVE_SCOPE
  Source section: Section 10
  Declaration: Constraint C-2 — Recursive traversal scope. The system
               must scan the entire subtree rooted at the target
               directory. Partial traversal is not a valid execution.
  Status: DECLARED

ID: BETO_DUPLICATE_FILE_FINDER_CLI.SEC10.CONSTRAINT.C3_REPORT_COMPLETENESS
  Source section: Section 10
  Declaration: Constraint C-3 — Report completeness. The report must
               include all three declared output elements: duplicate
               groups, file paths per group, and total recoverable space.
               Omitting any of these elements constitutes an incomplete
               output.
  Status: DECLARED
```

---

## SUMMARY INDEX

```
Total IDs registered: 66

By section:
  SEC1  — INTENT:       2
  SEC2  — BOUNDARY:    12
  SEC3  — INPUT/OUTPUT: 6
  SEC4  — FIELD/OQ:     7
  SEC5  — INVARIANT/EPISTEMIC: 11
  SEC6  — COMPONENT:    7
  SEC7  — PHASE:        5
  SEC8  — DECISION:     5
  SEC9  — OQ:           8
  SEC10 — RISK/CONSTRAINT: 6

By type:
  INTENT:      2
  BOUNDARY:   12
  INPUT:       2
  OUTPUT:      4
  FIELD:       3
  OQ:         12  (4 in SEC4 + 8 in SEC9)
  INVARIANT:   7
  EPISTEMIC:   3
  COMPONENT:   7
  PHASE:       5
  DECISION:    5
  RISK:        3
  CONSTRAINT:  3

OQs with FAIL_EXECUTIONAL_GAP (critical, execution-blocking):
  OQ-1  BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-1
  OQ-4  BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-4
  OQ-5  BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-5
  OQ-6  BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-6
  OQ-8  BETO_DUPLICATE_FILE_FINDER_CLI.SEC9.OQ.OQ-8
```

---

## CHANGELOG

```
2025-01-31T00:00:00Z  Registry created from BETO_CORE_DUPLICATE_FINDER.md
2025-01-31T00:00:00Z  Section 1 IDs registered (2)
2025-01-31T00:00:00Z  Section 2 IDs registered (12)
2025-01-31T00:00:00Z  Section 3 IDs registered (6)
2025-01-31T00:00:00Z  Section 4 IDs registered (7)
2025-01-31T00:00:00Z  Section 5 IDs registered (11)
2025-01-31T00:00:00Z  Section 6 IDs registered (7)
2025-01-31T00:00:00Z  Section 7 IDs registered (5)
2025-01-31T00:00:00Z  Section 8 IDs registered (5)
2025-01-31T00:00:00Z  Section 9 IDs registered (8)
2025-01-31T00:00:00Z  Section 10 IDs registered (6)
2025-01-31T00:00:00Z  Summary index compiled: 66 total IDs
2025-01-31T00:00:00Z  Registry status: DRAFT
```