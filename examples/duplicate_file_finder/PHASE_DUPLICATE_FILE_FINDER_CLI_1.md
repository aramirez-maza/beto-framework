# PHASE 1 - Discovery

## 1. PURPOSE

Derived from BETO_CORE Section 7 (Phase Architecture, Phase 1).

Phase 1 performs the complete recursive traversal of the target directory supplied as a CLI argument, discovering every file reachable within the directory tree and producing the authoritative collection of File Entries that serves as the sole input to Phase 2. Each File Entry carries exactly the fields required for downstream processing: the file path and the file size in bytes. The phase produces no analysis, no grouping, and no modification of any file. Its only responsibility is discovery and enumeration. This phase is the origin point of the traceability chain; every file path produced here must be preserved without modification through all subsequent phases.

---

## 2. INPUT CONTRACT

Derived from BETO_CORE Section 7 (Phase 1 Input column) and BETO_CORE Sections 3–5.

**Input source:** External source — command-line argument provided by the user at invocation time.

**Input artifact:** A single target directory path.

**Mandatory properties:**
- The path must designate a directory (not a file, device, or other non-directory filesystem object), as directly implied by BETO_CORE Section 1 (System Intent) and Section 3 (Inputs).
- The path must be provided as a CLI argument, as explicitly declared in BETO_CORE Section 3 (Inputs) and Section 8 (CLI argument interface: Confirmed).

**Format expectations:** BETO_CORE does not declare a specific format (absolute vs. relative path, quoting conventions, or encoding). No format assumption is introduced here.

**Traceability requirements:** The target directory path is the root anchor of the entire traceability chain. It must be recorded as the traversal root against which all discovered file paths are produced. No lineage requirement beyond this is declared in BETO_CORE for Phase 1 inputs.

**Unresolved dependencies:**

- `Unresolved: OQ-4 — Whether symbolic links encountered during traversal must be followed or skipped is not declared. BETO_CORE Section 9 records this as OQ-4 (critical, FAIL_EXECUTIONAL_GAP). This phase cannot define traversal behavior for symbolic links without OQ-4 resolution. Behavior toward symbolic links is declared undefined for this phase until OQ-4 is closed.`
- `Unresolved: OQ-8 — How the tool must behave when a file or subdirectory cannot be accessed due to permission errors (skip silently, skip with warning, or abort) is not declared. BETO_CORE Section 9 records this as OQ-8 (critical, FAIL_EXECUTIONAL_GAP). This phase cannot define error handling behavior without OQ-8 resolution.`
- `Unresolved: OQ-3 — Whether zero-byte files must be included in or excluded from the File Entry collection is not declared. BETO_CORE Section 9 records this as OQ-3 (non-critical, PENDING). This phase cannot declare inclusion or exclusion of zero-byte files without OQ-3 resolution.`
- `Unresolved: OQ-5 — The programming language or runtime is not declared. BETO_CORE Section 9 records this as OQ-5 (critical, FAIL_EXECUTIONAL_GAP). This phase cannot produce executable code until OQ-5 is closed.`

---

## 3. OUTPUT CONTRACT

Derived from BETO_CORE Section 7 (Phase 1 Output column) and BETO_CORE Sections 3–5.

**Output artifact:** A collection of File Entries representing every file discovered during recursive traversal of the target directory.

**Mandatory fields per File Entry** (explicitly declared in BETO_CORE Section 4, Core Unit of Processing):
- `file_path`: the path of the discovered file, preserved without modification from discovery, bound to this specific file entry and not reassigned.
- `file_size`: the size of the file in bytes.

**Output guarantees required by global invariants:**

- The collection must be complete: every file reachable by recursive traversal of the target directory must appear in the output (BETO_CORE Section 2, Constraint C-2: partial traversal is not valid execution).
- Every `file_path` in the output must be unique within the collection: a single filesystem entry must not produce multiple File Entries.
- The `file_path` field must be preserved exactly as produced during traversal; it must not be normalized, modified, or rewritten (BETO_CORE Section 4, Traceability fields).
- The `file_size` field must reflect the actual byte size of the file at the moment of discovery.
- No file in the filesystem is modified, deleted, or moved during this phase (BETO_CORE Section 5, Non-destructive processing; Section 8, Non-destructive execution: Confirmed; Section 2, Constraint C-1).

**Unresolved output definitions:**

- Output format (in-memory structure, intermediate file, serialization format) is not declared in BETO_CORE. This remains abstract; no format is introduced here.
- The disposition of symbolic links in the output collection is not declared pending OQ-4 resolution.
- The disposition of zero-byte files in the output collection is not declared pending OQ-3 resolution.
- The disposition of entries that could not be accessed due to permission errors is not declared pending OQ-8 resolution.

---

## 4. PHASE RULES

**RULE 1 — Traversal completeness.**
The traversal must visit every node in the directory tree rooted at the target directory. No subdirectory may be skipped unless its omission is explicitly authorized by a resolved OQ (OQ-4 for symbolic links, OQ-8 for permission errors). An unvisited subdirectory that has no authorizing resolution constitutes a violation of Constraint C-2 (BETO_CORE Section 2 and Section 10).

**RULE 2 — File-only emission.**
Only filesystem entries that are regular files may produce a File Entry in the output collection. Directories, devices, pipes, sockets, and other non-file objects must not produce File Entries. The phase collects files, not filesystem nodes in general. (Derived from BETO_CORE Section 4: the atomic unit is a discovered file entry.)

**RULE 3 — Immutability of file_path.**
The `file_path` value assigned to a File Entry during discovery must not be modified, normalized, abbreviated, or rewritten at any point during this phase. The value recorded in the output must be identical to the value produced at the moment of discovery. (BETO_CORE Section 4, Traceability fields; Section 5, Absolute traceability.)

**RULE 4 — Single-entry uniqueness.**
Each distinct filesystem file discovered during traversal must produce exactly one File Entry in the output collection. No file may be represented more than once in the output of this phase, regardless of traversal path or directory structure.

**RULE 5 — file_size accuracy.**
The `file_size` value recorded for each File Entry must reflect the actual byte size of the file at the moment of its discovery during traversal. No estimated, cached, or derived size value is permitted.

**RULE 6 — Non-destructive execution.**
This phase must not modify, write to, delete, rename, or move any file or directory encountered during traversal. The filesystem state after Phase 1 completes must be identical to the filesystem state before Phase 1 began. (BETO_CORE Section 5 global invariant; Section 8 Confirmed decision; Section 10 Constraint C-1.)

**RULE 7 — Symbolic link handling deferred.**
Until OQ-4 is resolved, this phase must not define, assume, or implement any traversal behavior specific to symbolic links. If symbolic links are encountered and OQ-4 is unresolved, the phase must record this as a blocking dependency and must not proceed to Phase 2 output production. (BETO_CORE Section 9, OQ-4, critical, FAIL_EXECUTIONAL_GAP.)

**RULE 8 — Permission error handling deferred.**
Until OQ-8 is resolved, this phase must not define, assume, or implement any behavior for files or subdirectories that cannot be accessed due to permission restrictions. (BETO_CORE Section 9, OQ-8, critical, FAIL_EXECUTIONAL_GAP.)

**RULE 9 — Zero-byte file inclusion deferred.**
Until OQ-3 is resolved, this phase must not define, assume, or implement any inclusion or exclusion rule for zero-byte files. (BETO_CORE Section 9, OQ-3, non-critical, PENDING.)

**RULE 10 — No content inspection.**
This phase must not read or inspect the content of any file. The only file properties accessed during this phase are those required to populate `file_path` and `file_size`. Content reading is exclusively the responsibility of Phase 2 (Hashing). (BETO_CORE Section 7, Phase Architecture: Phase 1 output does not include content_hash.)

**RULE 11 — No hashing, grouping, or analysis.**
This phase must not compute any hash, perform any grouping, calculate any recoverable space, or produce any artifact beyond the File Entry collection declared in Section 3. (BETO_CORE Section 7, Phase Architecture.)

**REGLA DE FASE — NO-INICIATIVA:**
Esta fase no puede producir outputs no declarados en la Sección 3 (Output Contract) de este documento. La iniciativa del ejecutor para proponer o expandir outputs fue válida únicamente en el Paso 0 (PROMPT_CANONICO). Si durante la ejecución de esta fase emerge la necesidad de un output no declarado → registrar como BETO_GAP y aplicar la REGLA BETO_GAP del BETO_INSTRUCTIVO. No producir. No asumir autorización implícita. Lo no declarado en el Output Contract no existe para esta fase.

**REGLA DE FASE — TRACE_REGISTRY:**
Cada construct de código producido por esta fase debe tener una anotación BETO-TRACE inmediatamente anterior que declare un ID registrado en el TRACE_REGISTRY del BETO_CORE que define esta fase. El ID debe referenciar la sección y el elemento específico del BETO_CORE que autoriza la existencia de ese construct. No es válido referenciar el ID de otra fase o de otro BETO_CORE como autorización para un construct de esta fase. Un construct sin ID registrado es un construct no autorizado.

---

## 5. VALIDATIONS

### Input Validation Checks

- **IV-1:** Verify that exactly one target directory path has been supplied as a CLI argument. If zero arguments are supplied, the phase must not proceed. If more than one argument is supplied, the phase must not proceed unless additional CLI options are resolved by OQ-7; in the absence of OQ-7 resolution, only the single target directory argument declared in BETO_CORE Section 3 is authoritative.
- **IV-2:** Verify that the supplied path designates an existing filesystem object. If the path does not exist, the phase must not proceed. (Derived from BETO_CORE Section 3: the input is "a single target directory path.")
- **IV-3:** Verify that the filesystem object at the supplied path is a directory. If it is not a directory (e.g., it is a regular file or device), the phase must not proceed. (Derived from BETO_CORE Section 1 and Section 3.)
- **IV-4:** Verify that OQ-4 has been resolved before traversal begins. If OQ-4 is unresolved and the directory tree contains or may contain symbolic links, the phase must not proceed to output production. (BETO_CORE Section 9, OQ-4, critical.)
- **IV-5:** Verify that OQ-8 has been resolved before traversal begins. If OQ-8 is unresolved and the directory tree contains or may contain permission-restricted entries, the phase must not proceed to output production. (BETO_CORE Section 9, OQ-8, critical.)

### Output Validation Checks

- **OV-1:** Verify that every File Entry in the output collection contains a non-null, non-empty `file_path` value. An entry with a null or empty `file_path` must be rejected. (BETO_CORE Section 4, mandatory fields.)
- **OV-2:** Verify that every File Entry in the output collection contains a non-negative numeric `file_size` value. An entry with a null or non-numeric `file_size` must be rejected. (BETO_CORE Section 4, mandatory fields.)
- **OV-3:** Verify that all `file_path` values in the output collection are unique. Duplicate `file_path` values in the output constitute a violation of Phase Rule 4.
- **OV-4:** Verify that no File Entry in the output collection represents a directory, device, or non-regular-file filesystem object. (Phase Rule 2.)
- **OV-5:** Verify that the output collection does not contain a `content_hash` field or any other field not declared in the Output Contract of Section 3. (Phase Rule 11; REGLA DE FASE — NO-INICIATIVA.)
- **OV-6:** TRACE_REGISTRY CHECK — For each construct in the output, verify that its BETO-TRACE ID exists in the TRACE_REGISTRY of this BETO_CORE. If the ID does not exist → BETO_GAP [ESCALADO] obligatorio. If the ID exists but corresponds to another section → BETO_WARNING emitted, construct marked as WARNED. If all IDs are verified → artifact marked as TRACE_VERIFIED.

### Failure Handling Policy

- **Default behavior for this phase: STOP.** If any input validation check (IV-1 through IV-5) fails, the phase must stop immediately and must not produce any output. No partial output is valid.
- **OQ-blocking failures:** If OQ-4 or OQ-8 are unresolved at the time of traversal, the phase must stop and report the blocking unresolved dependency. This is consistent with BETO_CORE Section 9 execution_readiness_check = FAIL_EXECUTIONAL_GAP for both OQs.
- **Output validation failures (OV-1 through OV-5):** Any File Entry that fails an output validation check must be excluded from the output collection and must be recorded as a failed entry with the specific check that caused rejection. The phase must not silently discard failed entries.
- **TRACE_REGISTRY failures (OV-6):** If a construct's BETO-TRACE ID is absent from the TRACE_REGISTRY → BETO_GAP [ESCALADO] must be raised; the construct must not be emitted. If the ID is present but mismatched → BETO_WARNING emitted, construct marked WARNED.
- **No silent continuation:** No failure condition in this phase may be silently ignored. Every failure must be surfaced to the caller or recorded as a declared gap.

---

## 6. EDGE CASES

- **EC-1 — Empty target directory:** The target directory exists but contains no files and no subdirectories. The output collection must be an empty collection. This is a valid terminal state; Phase 2 receives an empty collection and must handle it accordingly.
- **EC-2 — Target directory contains only subdirectories, no files:** Recursive traversal visits all subdirectories but discovers zero regular files. The output collection is empty. Same handling as EC-1.
- **EC-3 — Target directory contains only zero-byte files:** All discovered files have `file_size` = 0. Disposition depends on OQ-3 resolution. Until OQ-3 is resolved, this case is blocked. If OQ-3 resolves to inclusion, all zero-byte files produce File Entries with `file_size` = 0.
- **EC-4 — Target directory is deeply nested (very large tree depth):** Recursive traversal must reach files at any depth without enforcing a maximum depth limit. No depth constraint is declared in BETO_CORE. Stack overflow risk during traversal is an implementation concern outside this phase's scope.
- **EC-5 — Target directory contains a very large number of files:** No upper bound on the number of File Entries is declared in BETO_CORE. The output collection must include all discovered files regardless of count. Performance characteristics are not declared (BETO_CORE Section 10, Risk R-3).
- **EC-6 — Target directory contains symbolic links to files:** Disposition depends on OQ-4 resolution (critical, FAIL_EXECUTIONAL_GAP). Until OQ-4 is resolved, this case is blocked. If OQ-4 resolves to follow, the target file produces a File Entry. If OQ-4 resolves to skip, the symbolic link produces no File Entry.
- **EC-7 — Target directory contains symbolic links to directories:** Same dependency on OQ-4. If OQ-4 resolves to follow, the subtree rooted at the link target must be traversed. If OQ-4 resolves to skip, the subtree is not traversed.
- **EC-8 — Symbolic link creates a traversal cycle:** If OQ-4 resolves to follow symbolic links and a symbolic link points to an ancestor directory, traversal could loop infinitely. This edge case is only reachable after OQ-4 resolution and must be handled by the OQ-4 resolution policy or flagged as a BETO_GAP at that time.
- **EC-9 — Permission denied on a subdirectory:** The traversal cannot descend into a subdirectory due to permission restrictions. Disposition depends on OQ-8 resolution (critical, FAIL_EXECUTIONAL_GAP). Files within that subdirectory cannot be discovered. Until OQ-8 is resolved, this case is blocked.
- **EC-10 — Permission denied on a specific file:** The traversal can discover the file's name but cannot read its metadata (including `file_size`). Disposition depends on OQ-8 resolution. Until OQ-8 is resolved, this case is blocked.
- **EC-11 — Target path exists but is a regular file, not a directory:** Input validation check IV-3 must catch this and stop the phase before traversal begins.
- **EC-12 — Target path does not exist:** Input validation check IV-2 must catch this and stop the phase before traversal begins.
- **EC-13 — Target directory is provided with a trailing separator or alternative path representation:** The path's syntactic form may vary. The phase must resolve the path to its canonical filesystem target before beginning traversal without modifying or reassigning the `file_path` values of discovered files. No normalization of discovered `file_path` values is permitted by Phase Rule 3.
- **EC-14 — Two distinct paths within the directory tree resolve to the same physical file (hard links):** BETO_CORE Section 2 (Out of scope) does not declare hard link handling. Whether a hard-linked file should produce one or two File Entries is not declared. This case is marked as:
  `Unresolved: Hard link behavior — two traversal paths resolve to the same inode. Neither inclusion nor deduplication is declared in BETO_CORE.`
- **EC-15 — File is deleted or moved between discovery and metadata read:** A file may be enumerated during directory listing but cease to exist before `file_size` can be read. Disposition for this race condition is not declared in BETO_CORE. This case is marked as:
  `Unresolved: Filesystem race condition — file disappears after enumeration but before size retrieval.`

---

## 7. PROCESS STEPS (NO CODE)

**Step 1 — Receive and record the target directory path.**
Accept the single target directory path from the CLI argument. Record it as the traversal root. This value anchors all subsequent file path production.
[→ Collection of File Entries: establishes the root from which all file_path values are derived]

**Step 2 — Validate the target directory path (input checks IV-1 through IV-3).**
Confirm that exactly one path argument has been supplied, that the path designates an existing filesystem object, and that the object is a directory. If any of these checks fail, stop the phase and report the failure. Do not proceed to traversal.
[→ Collection of File Entries: prevents invalid traversal from producing invalid output]

**Step 3 — Verify resolution status of blocking OQs.**
Confirm that OQ-4 (symbolic link policy) and OQ-8 (permission error policy) have been resolved before traversal begins. If either is unresolved, stop the phase and report the blocking dependency. Do not proceed to traversal.
[→ Collection of File Entries: ensures traversal behavior is fully defined before output is produced]

**Step 4 — Initialize the traversal.**
Establish the traversal starting point at the target directory. Initialize an empty collection to accumulate File Entries. No files have been discovered yet.
[→ Collection of File Entries: initializes the output artifact]

**Step 5 — Visit the current directory node.**
For each entry in the current directory, determine whether the entry is a regular file, a directory, a symbolic link, or another filesystem object type.
[→ Collection of File Entries: enumerates candidates for File Entry production]

**Step 6 — Apply symbolic link policy.**
For each entry identified as a symbolic link, apply the policy declared by the resolution of OQ-4. If OQ-4 is unresolved at this step, stop and report the blocking dependency (this check is redundant with Step 3 but guards against runtime state changes).
[→ Collection of File Entries: determines whether symbolic link targets contribute entries]

**Step 7 — Apply zero-byte file policy.**
For each entry identified as a regular file with `file_size` = 0, apply the policy declared by the resolution of OQ-3. If OQ-3 is unresolved, the disposition of zero-byte files is deferred; record these files as pending OQ-3 resolution without including or excluding them from the output collection until the policy is declared.
[→ Collection of File Entries: determines whether zero-byte files are included in the output]

**Step 8 — Read file metadata for regular files.**
For each entry confirmed as a regular file that passes the zero-byte policy check, read the `file_size` value from filesystem metadata. Do not read file content. If the metadata read fails due to a permission error or other access failure, apply the policy declared by the resolution of OQ-8.
[→ Collection of File Entries: populates the file_size field for each File Entry]

**Step 9 — Construct the File Entry.**
For each regular file that has passed all applicable policy checks and whose metadata has been successfully read, construct a File Entry containing exactly two fields: `file_path` (the path as produced by traversal, unmodified) and `file_size` (the value read from filesystem metadata in Step 8). No other fields are added.
[→ Collection of File Entries: produces the declared output artifact entries]

**Step 10 — Add the File Entry to the output collection.**
Append the constructed File Entry to the accumulating output collection. Verify that the `file_path` value is not already present in the collection (uniqueness check per Phase Rule 4). If a duplicate `file_path` is detected, record it as a failure per the failure handling policy and do not add the duplicate entry.
[→ Collection of File Entries: enforces uniqueness guarantee on the output artifact]

**Step 11 — Recurse into subdirectories.**
For each entry in the current directory identified as a regular directory (not a symbolic link to a directory, unless OQ-4 resolves to follow), add it to the traversal queue. Proceed to visit each queued subdirectory by repeating Steps 5 through 10. Continue until no unvisited directories remain in the queue.
[→ Collection of File Entries: enforces completeness guarantee (Constraint C-2)]

**Step 12 — Apply permission error policy on inaccessible directories.**
For each directory entry that cannot be opened or read due to permission restrictions, apply the policy declared by the resolution of OQ-8. If OQ-8 is unresolved at this step, stop and report the blocking dependency.
[→ Collection of File Entries: ensures all traversal exceptions are handled per declared policy]

**Step 13 — Confirm traversal completion.**
After the traversal queue is empty, confirm that no reachable directory node was skipped without an authorizing policy resolution. The traversal is complete when the queue is empty and all access failures have been handled per the OQ-8 policy.
[→ Collection of File Entries: satisfies Constraint C-2 (complete traversal)]

**Step 14 — Validate the output collection.**
Apply output validation checks OV-1 through OV-5 to the completed File Entry collection. For each entry that fails a check, remove it from the collection and record the failure. Apply TRACE_REGISTRY CHECK (OV-6) to all constructs.
[→ Collection of File Entries: ensures the output artifact satisfies all declared guarantees]

**Step 15 — Emit the output collection.**
Deliver the validated File Entry collection to Phase 2 (Hashing) as its declared input. The collection is the complete and authoritative set of File Entries produced by this phase.
[→ Collection of File Entries: completes the output contract for this phase]

---

## 8. HANDOFF TO NEXT PHASE

The following properties are guaranteed by Phase 1 upon successful completion and may be safely assumed by Phase 2 (Hashing):

- **The output collection is complete:** Every regular file reachable by recursive traversal of the target directory, subject to the policies resolved by OQ-3, OQ-4, and OQ-8, is represented in the collection. Partial traversal has not occurred (Constraint C-2).
- **Every File Entry contains a non-null, non-empty `file_path`:** This value was assigned at the moment of discovery and has not been modified, normalized, or rewritten. It uniquely identifies the filesystem location of the file.
- **Every File Entry contains a non-negative numeric `file_size`:** This value reflects the actual byte size of the file as read from filesystem metadata during traversal.
- **All `file_path` values in the collection are unique:** No file is represented more than once.
- **No File Entry contains a `content_hash` or any field beyond `file_path` and `file_size`:** Phase 2 must compute `content_hash` independently for each entry; it cannot assume any hash value exists.
- **No file in the filesystem has been modified:** The filesystem state is identical to its state before Phase 1 began.
- **All input and output validation checks have passed:** Entries that failed validation have been excluded and recorded; they are not present in the collection delivered to Phase 2.

The following remain unresolved and must NOT be assumed by Phase 2:

- **OQ-3 (zero-byte files):** If OQ-3 was unresolved when Phase 1 executed, the disposition of zero-byte files is not settled. Phase 2 must not assume zero-byte files are present or absent in the collection.
- **OQ-4 (symbolic links):** The presence or absence of symbolic link targets in the collection depends on OQ-4 resolution. Phase 2 must not assume all symbolic links were followed or all were skipped.
- **OQ-8 (permission errors):** Files that could not be accessed are absent from the collection per the OQ-8 policy. Phase 2 must not assume the collection represents the complete filesystem state independent of permission restrictions.
- **OQ-5 (programming language):** No implementation has been produced. Phase 2 cannot assume any runtime or language-specific artifact from Phase 1.
- **Hard link behavior (EC-14):** Whether hard-linked files appear once or multiple times in the collection is unresolved. Phase 2 must not assume either behavior.
- **Filesystem race conditions (EC-15):** Files that disappeared between enumeration and metadata read may have produced incomplete entries or been excluded per the failure handling policy. Phase 2 must not assume the collection is immune to this condition.

---

## END OF DOCUMENT