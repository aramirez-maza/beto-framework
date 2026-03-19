# PHASE 3 - Grouping

## 1. PURPOSE

This phase receives the complete collection of File Entries enriched with content hashes and produces the collection of Duplicate Groups. Its sole responsibility is to group File Entries by identical content hash value and retain only those groups whose membership cardinality is greater than or equal to two. A group with exactly one member is not a duplicate group and must be discarded. This phase does not compute recoverable space, does not compose any report element, and does not modify any file. Its output is the authoritative input for Phase 4 (Space Calculation), as declared in BETO_CORE Section 7.

---

## 2. INPUT CONTRACT

**Input source:** Phase 2 (Hashing) output, delivered via the declared pipeline dependency EDGE.DEP-HASHER-DUPLICATE_DETECTOR (BETO_SYSTEM_GRAPH Section 8).

**Input artifact:** Collection of File Entries with content hash, as declared in BETO_CORE Section 7, Phase 2 output column.

**Mandatory fields per File Entry** (BETO_CORE Section 4):

- `file_path` — absolute or relative path of the file within the scanned directory tree; must have been preserved without modification from Phase 1 through Phase 2
- `file_size` — size of the file in bytes; must be present and bound to the same `file_path` from which it was originally derived
- `content_hash` — hash value computed from the full content of the file; must be bound to the exact `file_path` from which it was computed; must not have been reassigned or modified between Phase 2 and this phase

**Traceability requirements** (BETO_CORE Section 4 — Invariante de Trazabilidad Semántica):

- The binding `file_path → content_hash` established in Phase 2 must arrive intact and must not be broken, rebound, or inferred within this phase.
- The binding `file_path → file_size` established in Phase 1 must arrive intact.
- No traceability field may be dropped, inferred, or reconstructed within this phase.

**Unresolved dependencies:**

- The hashing algorithm that produced `content_hash` values is governed by OQ-1 (BETO_CORE Section 9), which is to be closed within GRAPH.HASHER's own BETO_CORE child. This phase treats `content_hash` as an opaque string value and does not depend on OQ-1's resolution to execute its grouping logic.
- `Unresolved: OQ-5 (programming language/runtime, BETO_CORE Section 8/9)` — this phase does not depend on OQ-5 for its logical specification, but materialization is blocked until OQ-5 is closed at the root BETO_CORE level, per BETO_SYSTEM_GRAPH Section 11.

---

## 3. OUTPUT CONTRACT

**Output artifact:** Collection of Duplicate Groups, as declared in BETO_CORE Section 7, Phase 3 output column.

**Mandatory fields per Duplicate Group** (BETO_CORE Section 7, Phase 3):

- `content_hash` — the shared hash value that defines membership of the group; must be identical to the `content_hash` values of all File Entries that are members of this group
- `[file_paths]` — the ordered or unordered list of all `file_path` values belonging to File Entries whose `content_hash` equals the group's `content_hash`; must contain at least two entries; must preserve all `file_path` values exactly as received from Phase 2 without modification
- `group_size` — the file size in bytes shared by all members of the group; must be traceable to the `file_size` field of any member File Entry within the group (all members in a group share the same `content_hash` and therefore the same content; `group_size` represents the per-file size used in Phase 4's recoverable space formula)

**Output guarantees required by global invariants** (BETO_CORE Section 5):

- Every Duplicate Group in the output collection has cardinality ≥ 2; no singleton groups are emitted.
- No file path is silently dropped; every File Entry present in the input whose `content_hash` appears in at least one other File Entry must appear in the output collection.
- No file path is invented or modified; the output contains exactly the `file_path` values received from Phase 2.
- The output collection may be empty if no two File Entries in the input share an identical `content_hash`; an empty collection is a valid output.

**Unresolved output definitions:**

- The physical format or encoding of the Duplicate Group collection (in-memory structure, serialized format, intermediate file) is not declared in BETO_CORE and remains abstract at this phase specification level. Resolution is deferred to the materialization step governed by OQ-5.

---

## 4. PHASE RULES

**RULE-3.1 — Grouping key is exclusively content_hash.**
File Entries must be grouped solely by the value of their `content_hash` field. No other field (`file_path`, `file_size`, filename, extension, modification date) may participate in or override the grouping key. Source: BETO_CORE Section 4 (content_hash as grouping key), Section 6 (Duplicate Detector conceptual role).

**RULE-3.2 — Singleton groups must be discarded.**
Any group that would contain exactly one File Entry must be removed from the output collection before the output is emitted. A file with a unique `content_hash` is not a duplicate and must not appear in the output. Source: BETO_CORE Section 7, Phase 3 purpose ("retain only groups with more than one member").

**RULE-3.3 — All qualifying file paths must be included.**
Every File Entry whose `content_hash` appears in at least one other File Entry must be included in the corresponding Duplicate Group. Partial inclusion within a group is not permitted. Omitting a qualifying file path constitutes an incomplete output, violating BETO_CORE Section 10 Constraint C-3 (report completeness as applied to intermediate pipeline stages). Source: BETO_CORE Section 5 (no invention of information; absolute traceability).

**RULE-3.4 — File paths must not be modified.**
The `file_path` values in the output must be byte-for-byte identical to the values received in the input. This phase must not normalize, canonicalize, shorten, or reformat any `file_path`. Source: BETO_CORE Section 4 (file_path must be preserved without modification), Section 5 (absolute traceability).

**RULE-3.5 — content_hash binding must not be broken.**
The association between a `content_hash` value and each `file_path` assigned to that value must remain as established by Phase 2. This phase must not recompute, reassign, or infer any `content_hash` value. Source: BETO_CORE Section 4 (content_hash must be bound to the exact file_path from which it was computed and must not be reassigned), Section 5 (Invariante de Trazabilidad Semántica).

**RULE-3.6 — group_size must be derived from input file_size.**
The `group_size` field of each Duplicate Group must be populated from the `file_size` field of the File Entries that are members of the group. This phase must not compute file sizes independently, access the filesystem, or infer sizes from any source other than the input collection. Source: BETO_CORE Section 4 (file_size required for space computation), Section 7 Phase 3 output column.

**RULE-3.7 — An empty output collection is valid.**
If no two File Entries in the input share an identical `content_hash`, the output collection of Duplicate Groups must be empty. This is a valid terminal state for Phase 3. The phase must not treat an empty output as an error condition. Source: BETO_CORE Section 3 (output may legitimately contain no duplicate groups), Section 5 (no invention of information).

**RULE-3.8 — This phase must not access the filesystem.**
Phase 3 operates exclusively on the in-memory or serialized collection received from Phase 2. It must not open, read, stat, or otherwise access any file or directory on the filesystem. Source: BETO_CORE Section 2 (out of scope: any behavior not directly implied by scan, detect, and report), Section 5 (non-destructive processing; Invariante de Iniciativa Controlada).

**RULE-3.9 — No output not declared in Section 3 may be produced.**
REGLA DE FASE — NO-INICIATIVA: This phase produces exclusively the Collection of Duplicate Groups declared in Section 3. If any need for an additional output artifact emerges during execution, it must be registered as a BETO_GAP and must not be produced.

**RULE-3.10 — Every construct must carry a BETO-TRACE annotation.**
REGLA DE FASE — TRACE_REGISTRY: Every code construct produced during materialization of this phase must be preceded by a BETO-TRACE annotation referencing an ID registered in the TRACE_REGISTRY for this BETO_CORE. A construct without a registered ID is an unauthorized construct.

---

## 5. VALIDATIONS

### Input Validation Checks

- **IV-3.1** — Every File Entry in the input collection must contain all three mandatory fields: `file_path`, `file_size`, and `content_hash`. Any entry missing one or more of these fields constitutes a malformed input. Justification: Input Contract, Section 2; BETO_CORE Section 4.
- **IV-3.2** — No `file_path` value in the input collection may be null, empty, or blank. Justification: BETO_CORE Section 4 (file_path must be preserved); Section 5 (absolute traceability).
- **IV-3.3** — No `content_hash` value in the input collection may be null, empty, or blank. Justification: BETO_CORE Section 4 (content_hash is the grouping key); Section 5.
- **IV-3.4** — No `file_size` value in the input collection may be negative. A value of zero is conditionally permitted per the resolution of OQ-3 (BETO_CORE Section 9); until OQ-3 is resolved within GRAPH.SCANNER's BETO_CORE child and its effect propagated, Phase 3 must accept zero-byte entries without filtering them. Justification: Input Contract, Section 2; BETO_CORE Section 4.
- **IV-3.5** — The input collection itself may be empty (zero File Entries). An empty input collection is valid and must produce an empty output collection. Justification: RULE-3.7; BETO_CORE Section 5 (no invention of information).

### Output Validation Checks

- **OV-3.1** — Every Duplicate Group in the output collection must contain at least two `file_path` entries in its `[file_paths]` list. A group with fewer than two members must not appear in the output. Justification: RULE-3.2; BETO_CORE Section 7, Phase 3.
- **OV-3.2** — For every Duplicate Group, all `file_path` values in its `[file_paths]` list must correspond to File Entries in the input collection whose `content_hash` equals the group's `content_hash`. No `file_path` may appear in a group for a `content_hash` other than the one assigned to it in the input. Justification: RULE-3.5; BETO_CORE Section 4.
- **OV-3.3** — No `file_path` value may appear in more than one Duplicate Group in the output collection. A single `file_path` is associated with exactly one `content_hash` and therefore can belong to at most one group. Justification: RULE-3.5; BETO_CORE Section 4.
- **OV-3.4** — Every `file_path` value that was present in the input collection and whose `content_hash` appears in at least one other input File Entry must appear in exactly one Duplicate Group in the output. No qualifying file path may be silently omitted. Justification: RULE-3.3; BETO_CORE Section 5 (absolute traceability; no invention of information).
- **OV-3.5** — The `group_size` field of each Duplicate Group must be equal to the `file_size` value of the File Entries that are members of that group. If members present inconsistent `file_size` values for the same `content_hash`, this is an anomalous condition (see Edge Cases). Justification: RULE-3.6; BETO_CORE Section 7, Phase 3 output column.
- **OV-3.6** — TRACE_REGISTRY CHECK: For every code construct in the materialized output, its BETO-TRACE ID must exist in the TRACE_REGISTRY of this BETO_CORE. A missing ID requires a BETO_GAP [ESCALADO]. An ID present but referencing a different section requires a BETO_WARNING and the construct must be marked WARNED. All IDs verified → file status TRACE_VERIFIED.

### Failure Handling Policy

- **Default behavior:** If any input validation check (IV-3.1 through IV-3.5, excluding IV-3.5's empty-input case) detects a malformed or incomplete entry, the phase must stop and emit a failure signal. Partial execution producing an incomplete Duplicate Group collection is not permitted, as it would violate BETO_CORE Section 10 Constraint C-3 and the absolute traceability invariant.
- **Empty input exception:** An empty input collection (IV-3.5) is not a failure condition. The phase must proceed and produce an empty output collection without emitting a failure signal.
- **Output validation failures** (OV-3.1 through OV-3.5): If any output validation check fails after grouping is complete, the phase must stop. The malformed output must not be forwarded to Phase 4. Justification: BETO_CORE Section 5 (absolute traceability; clear and explicit contracts between phases).
- **BETO_GAP on unresolved output need:** If during execution a need for an output artifact not declared in Section 3 emerges, the phase must stop, register a BETO_GAP, and not produce the undeclared artifact.

---

## 6. EDGE CASES

- **EC-3.1 — Empty input collection.** Phase 2 emits zero File Entries (e.g., the target directory contained no readable files). Phase 3 must produce an empty Duplicate Group collection without error. This is a declared valid terminal state (RULE-3.7; IV-3.5).

- **EC-3.2 — All files have unique content hashes.** Every File Entry in the input has a `content_hash` that appears exactly once. All candidate groups are singletons and must be discarded. Output collection is empty. Valid terminal state. Source: RULE-3.2; BETO_CORE Section 3.

- **EC-3.3 — All files share a single content hash.** Every File Entry in the input has the same `content_hash`. Phase 3 must produce exactly one Duplicate Group containing all file paths. The group is valid since cardinality ≥ 2. Source: RULE-3.1; RULE-3.3.

- **EC-3.4 — A content_hash maps to exactly two file paths.** The minimum valid duplicate group. Must be retained in the output. Source: RULE-3.2 (cardinality ≥ 2 means two is included).

- **EC-3.5 — A content_hash maps to a very large number of file paths.** No upper bound on group cardinality is declared in BETO_CORE. All file paths must be included. Source: RULE-3.3; BETO_CORE Section 5.

- **EC-3.6 — Inconsistent file_size values within a single content_hash group.** Two or more File Entries share the same `content_hash` but carry different `file_size` values in the input. This indicates a corruption or inconsistency in the Phase 2 output. Phase 3 cannot resolve this condition without inventing information. This must be treated as a failure (OV-3.5 violated), the phase must stop, and the condition must be reported. `Unresolved: behavior when file_size inconsistency within a hash group is detected — not declared in BETO_CORE; registered as candidate BETO_GAP.`

- **EC-3.7 — Input collection contains duplicate file_path entries with the same content_hash.** The same `file_path` appears more than once in the input bound to the same `content_hash`. This indicates a Phase 2 output anomaly. Phase 3 must not silently deduplicate `file_path` entries, as doing so would modify traceability. This condition must be reported as a failure. Source: RULE-3.4; BETO_CORE Section 5.

- **EC-3.8 — Input collection contains duplicate file_path entries with different content_hash values.** The same `file_path` appears more than once in the input bound to different `content_hash` values. This is a broken traceability binding from Phase 2 and must be reported as a failure; the phase must stop. Source: RULE-3.5; BETO_CORE Section 4.

- **EC-3.9 — A file_path is an empty string or null.** Detected by IV-3.2. Phase must stop. Source: Input Contract, Section 2.

- **EC-3.10 — A content_hash is an empty string or null.** Detected by IV-3.3. The affected entry cannot be grouped. Phase must stop. Source: Input Contract, Section 2.

- **EC-3.11 — A file_size value is zero.** Conditionally permitted per OQ-3 resolution (deferred to GRAPH.SCANNER). Phase 3 must not filter zero-byte entries; if two File Entries with `file_size` = 0 share a `content_hash`, they form a valid Duplicate Group. Source: IV-3.4; BETO_CORE Section 4.

- **EC-3.12 — A file_size value is negative.** Detected by IV-3.4. Phase must stop. Source: Input Contract, Section 2; BETO_CORE Section 4.

- **EC-3.13 — The number of distinct content_hash values resulting in groups with cardinality ≥ 2 is very large.** No upper bound on the number of Duplicate Groups is declared. Phase 3 must produce all qualifying groups. Source: RULE-3.3; BETO_CORE Section 10 Risk R-3.

---

## 7. PROCESS STEPS (NO CODE)

**Step 1 — Receive input collection.**
Accept the collection of File Entries (each carrying `file_path`, `file_size`, and `content_hash`) as delivered by Phase 2 via the EDGE.DEP-HASHER-DUPLICATE_DETECTOR pipeline dependency.
[→ Collection of Duplicate Groups — precondition for grouping]

**Step 2 — Validate input collection structure.**
Apply input validation checks IV-3.1 through IV-3.4 to every File Entry in the collection. For IV-3.5, if the collection is empty, proceed directly to Step 10. If any validation check fails, stop and emit a failure signal; do not proceed.
[→ Collection of Duplicate Groups — ensures only valid, traceable entries enter the grouping process]

**Step 3 — Check for file_path uniqueness per content_hash.**
Verify that no `file_path` value appears more than once in the input collection bound to the same `content_hash` (EC-3.7). If a duplicate `file_path` binding is detected, stop and emit a failure signal.
[→ Collection of Duplicate Groups — enforces RULE-3.4 and RULE-3.5 before grouping begins]

**Step 4 — Check for file_path uniqueness across all content_hash values.**
Verify that no `file_path` value appears in the input collection bound to more than one distinct `content_hash` value (EC-3.8). If a conflicting binding is detected, stop and emit a failure signal.
[→ Collection of Duplicate Groups — enforces RULE-3.5; prevents broken traceability from entering output]

**Step 5 — Group File Entries by content_hash.**
Partition the validated File Entry collection into sub-collections, where each sub-collection contains all and only those File Entries whose `content_hash` value is identical. The grouping key is exclusively `content_hash`. No other field participates in the partitioning.
[→ Collection of Duplicate Groups — primary transformation step; enforces RULE-3.1]

**Step 6 — Discard singleton groups.**
Inspect each sub-collection produced in Step 5. Remove any sub-collection whose cardinality is exactly one. Retain only sub-collections with cardinality ≥ 2.
[→ Collection of Duplicate Groups — enforces RULE-3.2; ensures only genuine duplicate groups are emitted]

**Step 7 — Validate file_size consistency within each retained group.**
For each retained sub-collection, verify that all member File Entries carry the same `file_size` value. If inconsistent `file_size` values are detected within a group (EC-3.6), stop and emit a failure signal. Do not attempt to resolve the inconsistency.
[→ Collection of Duplicate Groups — enforces OV-3.5; prevents invalid group_size population]

**Step 8 — Construct Duplicate Group records.**
For each retained sub-collection, construct a Duplicate Group record containing:
- `content_hash`: the shared hash value of all members in the sub-collection
- `[file_paths]`: the list of `file_path` values from all member File Entries, preserved exactly as received from Phase 2
- `group_size`: the `file_size` value shared by all members of the group (validated as consistent in Step 7)
No field may be computed, inferred, or invented beyond what is stated here.
[→ Collection of Duplicate Groups — constructs the declared output artifact; enforces RULE-3.3, RULE-3.4, RULE-3.6]

**Step 9 — Apply output validation checks.**
Apply output validation checks OV-3.1 through OV-3.5 to the constructed collection of Duplicate Group records. If any check fails, stop and emit a failure signal. Do not forward an invalid collection to Phase 4.
[→ Collection of Duplicate Groups — ensures the output satisfies all declared guarantees before handoff]

**Step 10 — Emit output collection.**
Deliver the validated collection of Duplicate Group records (or an empty collection if no qualifying groups exist) to Phase 4 (Space Calculation) via the EDGE.DEP-DUPLICATE_DETECTOR-SPACE_CALCULATOR pipeline dependency.
[→ Collection of Duplicate Groups — completes the Output Contract declared in Section 3]

---

## 8. HANDOFF TO NEXT PHASE

- The collection of Duplicate Groups delivered to Phase 4 (Space Calculation) contains exclusively groups with cardinality ≥ 2; no singleton groups are present.
- Every `file_path` value in every Duplicate Group is byte-for-byte identical to the value received from Phase 2; no path has been normalized, modified, or invented.
- The `content_hash` field of each Duplicate Group is the unmodified hash value that defines the group's membership; it was not recomputed or reassigned by Phase 3.
- The `group_size` field of each Duplicate Group is derived from the `file_size` values of the group's member File Entries, validated as consistent across all members within the group.
- The `[file_paths]` list of each Duplicate Group is complete: every File Entry from Phase 2 whose `content_hash` qualified it for a group of cardinality ≥ 2 is represented exactly once in exactly one group.
- The output collection may be empty. Phase 4 must treat an empty collection as a valid input and must not assume the presence of at least one Duplicate Group.
- The traceability binding `file_path → content_hash` established in Phase 2 is preserved intact through Phase 3's output. Phase 4 may rely on this binding without re-verifying it.
- The traceability binding `file_path → file_size` established in Phase 1 is preserved intact through Phase 3's output, expressed as `group_size` per group. Phase 4 must use `group_size` as the per-file size operand in its recoverable space formula.
- **Unresolved — must not be assumed by Phase 4:** OQ-5 (programming language/runtime) remains open at the root BETO_CORE level. Phase 4's materialization is subject to the same blocking condition.
- **Unresolved — must not be assumed by Phase 4:** OQ-3 (zero-byte file policy) is governed by GRAPH.SCANNER's BETO_CORE child and has not been closed. Phase 4 may receive Duplicate Groups with `group_size` = 0 and must handle this without assuming it is an error.

---

## END OF DOCUMENT