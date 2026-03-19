# PHASE 2 - Hashing

## 1. PURPOSE

Derived strictly from BETO_CORE Section 7.

Phase 2 receives the complete collection of File Entries produced by Phase 1 (Discovery) and computes a content hash for each entry. Each File Entry is enriched with a `content_hash` value derived from the full content of the file referenced by its `file_path`. The enriched collection is the sole output of this phase and constitutes the input required by Phase 3 (Grouping). This phase is the exclusive point in the pipeline where file content is read and converted into a hash value. No grouping, filtering by duplication, or space calculation is performed here. The filesystem is never modified.

---

## 2. INPUT CONTRACT

Derived strictly from BETO_CORE Section 7 and BETO_CORE Sections 3–5.

**Input source:** Phase 1 (Discovery) — via the declared pipeline dependency EDGE.DEP-SCANNER-HASHER (BETO_SYSTEM_GRAPH.md, Section 8).

**Input artifact:** Collection of File Entries produced by Phase 1.

**Mandatory fields per File Entry** (declared in BETO_CORE Section 4):
- `file_path`: the absolute or relative path of the file within the scanned directory tree. Must be preserved without modification from Phase 1.
- `file_size`: the size of the file in bytes. Must be preserved without modification from Phase 1.

**Format expectations:** Not explicitly stated in BETO_CORE. Format remains abstract.

**Traceability requirements:**
- Each File Entry must carry the `file_path` as bound at discovery time. This binding must not be altered or reassigned by this phase.
- The `file_size` value must remain identical to the value recorded in Phase 1.

**Unresolved dependencies:**

- `Unresolved: OQ-1` — The hashing algorithm (e.g., MD5, SHA-1, SHA-256, BLAKE2b) is not declared in BETO_CORE. Captured as OQ-1 (BETO_CORE Section 9, critical, execution_readiness_check = FAIL_EXECUTIONAL_GAP). This phase cannot execute hashing until OQ-1 is resolved. Referenced explicitly: BETO_CORE Section 8, Section 9 OQ-1.
- `Unresolved: OQ-2` — Whether a pre-filter by file size before hashing is applied is not declared. Captured as OQ-2 (BETO_CORE Section 9, non-critical). If OQ-2 remains unresolved at execution time, no size pre-filtering may be assumed or applied.
- `Unresolved: OQ-5` — The programming language or runtime is not declared (BETO_CORE Section 9, critical). This phase cannot be materialized until OQ-5 is resolved.
- `Unresolved: OQ-8` — Behavior on unreadable files (permission errors) during hashing is not declared (BETO_CORE Section 9, critical). If a file cannot be read during hashing, the required behavior (skip silently, skip with warning, abort) is undefined until OQ-8 is resolved.

---

## 3. OUTPUT CONTRACT

Derived strictly from BETO_CORE Section 7 and BETO_CORE Sections 3–5.

**Output artifact:** Collection of File Entries enriched with `content_hash`.

**Mandatory fields per File Entry in output** (declared in BETO_CORE Section 4 and Section 7):
- `file_path`: preserved from input without modification.
- `file_size`: preserved from input without modification.
- `content_hash`: the hash value computed from the full content of the file referenced by `file_path`, using the algorithm resolved by OQ-1.

**Output guarantees required by global invariants:**
- Every File Entry present in the input collection must appear in the output collection. No File Entry may be silently dropped unless explicitly authorized by the resolution of OQ-8.
- The `content_hash` of each File Entry must be bound exclusively to the `file_path` from which it was computed. A `content_hash` value must never be assigned to a `file_path` other than the one whose content was read.
- The `file_path` and `file_size` values must be identical to those received from Phase 1. This phase must not alter, normalize, or reinterpret either field.
- The output collection is consumed exclusively by Phase 3 (Grouping).

**Format expectations:** Not explicitly stated in BETO_CORE. Output format remains abstract.

**Unresolved output definitions:**
- The concrete representation and serialization format of the enriched File Entry collection are not declared. They remain abstract pending OQ-5 resolution.

---

## 4. PHASE RULES

**RULE-2.1 — Exclusive hash authority:**
The `content_hash` field may only be set by this phase. No other phase may compute, assign, or modify a `content_hash` value. A File Entry carrying a `content_hash` that was not computed in this phase is not a valid input to Phase 3.

**RULE-2.2 — Full content reading:**
The content hash must be computed from the complete content of the file. Partial reads, sampling, or approximations are not authorized. Hash computation over anything other than the full file content is a violation of this phase's purpose.

**RULE-2.3 — Strict path binding:**
The `content_hash` produced for a given file must be bound to the exact `file_path` from which the content was read. Reassigning a hash to a different `file_path` is prohibited and constitutes a traceability violation.

**RULE-2.4 — Field preservation:**
The `file_path` and `file_size` fields received from Phase 1 must be preserved in the output without any modification, normalization, or reinterpretation by this phase.

**RULE-2.5 — No filtering without authorization:**
This phase must not drop, exclude, or filter any File Entry from the input collection unless explicitly authorized by a resolved OQ. Specifically: size-based pre-filtering requires OQ-2 resolution; behavior on unreadable files requires OQ-8 resolution.

**RULE-2.6 — Algorithm consistency:**
A single hashing algorithm, as resolved by OQ-1, must be applied uniformly to all File Entries in the collection. Mixing algorithms across entries in the same execution is prohibited.

**RULE-2.7 — Non-destructive execution:**
This phase must not modify, delete, move, or write to any file in the scanned filesystem during content reading or hash computation. File access is read-only.

**RULE-2.8 — No grouping or duplicate detection:**
This phase must not evaluate whether two or more File Entries share the same `content_hash`. Grouping logic is the exclusive responsibility of Phase 3.

**RULE-2.9 — No output beyond the declared contract:**
This phase must not produce any artifact, annotation, side effect, or output not declared in Section 3. If a need for an undeclared output emerges during execution, it must be registered as a BETO_GAP. No undeclared output may be produced.

**RULE-2.10 — TRACE_REGISTRY compliance:**
Every construct produced by this phase must carry a BETO-TRACE annotation referencing an ID registered in the TRACE_REGISTRY of this BETO_CORE. A construct without a registered ID is not authorized.

---

## 5. VALIDATIONS

### Input validation checks

- **IV-2.1:** Verify that the input collection is present and non-empty before initiating any hash computation. An absent or null collection is a blocking failure.
- **IV-2.2:** Verify that every File Entry in the input collection contains a non-null, non-empty `file_path` field. A missing `file_path` is a blocking failure for that entry.
- **IV-2.3:** Verify that every File Entry in the input collection contains a `file_size` field with a non-negative integer value. A missing or invalid `file_size` is a blocking failure for that entry.
- **IV-2.4:** Verify that OQ-1 has been resolved and that a specific hashing algorithm is declared before any hash computation begins. An unresolved OQ-1 is a phase-level blocking failure.
- **IV-2.5:** Verify that OQ-8 has been resolved before any file read is attempted. An unresolved OQ-8 is a phase-level blocking failure because the behavior on unreadable files is undefined.
- **IV-2.6:** Verify that each `file_path` in the input collection references a file that exists and is accessible as a regular file at the time of hash computation. Behavior on inaccessible files is governed by OQ-8 resolution.

### Output validation checks

- **OV-2.1:** Verify that the output collection contains exactly as many File Entries as the input collection, unless entries were explicitly excluded by the policy resolved in OQ-8. Any count discrepancy not authorized by OQ-8 is a blocking failure.
- **OV-2.2:** Verify that every File Entry in the output collection contains a non-null, non-empty `content_hash` field.
- **OV-2.3:** Verify that every `content_hash` value in the output collection was produced by the algorithm declared in OQ-1. Mixed-algorithm outputs are a blocking failure.
- **OV-2.4:** Verify that the `file_path` field of every output File Entry is identical to the corresponding field in the input. Any modification is a blocking failure.
- **OV-2.5:** Verify that the `file_size` field of every output File Entry is identical to the corresponding field in the input. Any modification is a blocking failure.
- **OV-2.6:** Verify that each `content_hash` is bound to the `file_path` whose content was actually read to produce it. A hash-path mismatch is a traceability violation and a blocking failure.
- **OV-2.7:** TRACE_REGISTRY CHECK — For each construct in the output, verify that its BETO-TRACE ID exists in the TRACE_REGISTRY of this BETO_CORE. If the ID does not exist → BETO_GAP [ESCALADO] obligatorio. If the ID exists but corresponds to another section → BETO_WARNING emitted, construct marked as WARNED. If all IDs are verified → artifact status set to TRACE_VERIFIED.

### Failure handling policy

- **FH-2.1:** Default behavior for this phase is STOP. Any blocking failure detected during input validation or output validation halts phase execution immediately. No partial output is emitted to Phase 3.
- **FH-2.2:** Failures caused by unresolved OQs (OQ-1, OQ-5, OQ-8) are phase-level blocking failures. Execution must not proceed under any circumstance until the relevant OQ is resolved.
- **FH-2.3:** Failures caused by individual unreadable files during hashing are governed exclusively by the policy declared in OQ-8 resolution. Until OQ-8 is resolved, encountering an unreadable file is a phase-level STOP.
- **FH-2.4:** A TRACE_REGISTRY CHECK failure (OV-2.7) where an ID does not exist in the registry requires immediate BETO_GAP [ESCALADO] registration. The construct is not forwarded to Phase 3.
- **FH-2.5:** A BETO_WARNING (ID exists but belongs to another section) results in the construct being marked WARNED. A WARNED construct must not be forwarded to Phase 3 without explicit operator resolution.

---

## 6. EDGE CASES

- **EC-2.1:** Input collection contains zero File Entries. Phase must detect this condition before attempting any hash computation and treat it as a blocking failure per FH-2.1, since an empty input cannot produce a valid output collection for Phase 3.
- **EC-2.2:** OQ-1 is declared as resolved but the declared algorithm identifier does not correspond to a recognized or implementable algorithm. Phase must halt and report the inconsistency as a blocking failure.
- **EC-2.3:** A File Entry in the input has a `file_size` value of zero. Whether zero-byte files are included or excluded is governed by OQ-3. If OQ-3 is unresolved, this entry must not be silently skipped; its handling is unresolved and must be flagged.
- **EC-2.4:** A `file_path` in the input references a file that existed at Phase 1 time but has been deleted or moved before Phase 2 reads it. The file is inaccessible at hash-computation time. Behavior is governed by OQ-8.
- **EC-2.5:** A `file_path` in the input references a file that exists but cannot be opened due to permission restrictions at hash-computation time. Behavior is governed by OQ-8.
- **EC-2.6:** Two or more File Entries in the input collection carry identical `file_path` values. This is a traceability anomaly originating in Phase 1. This phase must not deduplicate or suppress entries; the duplicate paths must be forwarded as-is, and the anomaly must be flagged.
- **EC-2.7:** A file is readable but its content changes between the moment the file was discovered (Phase 1) and the moment its content is read for hashing (Phase 2). The hash produced reflects the content at read time, which may differ from the content at discovery time. This phase has no mechanism to detect this condition; it is recorded as an inherent boundary condition.
- **EC-2.8:** A `file_path` in the input references a symbolic link. Whether symbolic links are followed during traversal is governed by OQ-4 (Phase 1 responsibility). If a symbolic link reaches Phase 2 as a File Entry, this phase must hash the content reachable through the link if the link is valid and readable, without re-evaluating the OQ-4 policy.
- **EC-2.9:** Hash computation for a specific file fails mid-read (e.g., I/O error, disk error) after a partial read has been performed. A partial hash must never be recorded as a valid `content_hash`. The entry must be treated as unreadable and handled per OQ-8 resolution.
- **EC-2.10:** The input collection contains a File Entry where `file_size` does not match the actual file size at read time. The hash must be computed from the full actual content regardless of the declared `file_size`. The `file_size` field must be forwarded to Phase 3 as received from Phase 1, without correction by this phase. The discrepancy is a boundary condition inherited from Phase 1.

---

## 7. PROCESS STEPS (NO CODE)

**Step 1 — Receive input collection from Phase 1.**
Accept the collection of File Entries (file_path, file_size) as produced by Phase 1 (Discovery).
[→ Collection of File Entries enriched with content_hash]

**Step 2 — Validate phase preconditions.**
Confirm that OQ-1 (hashing algorithm) and OQ-8 (unreadable file policy) are resolved. If either is unresolved, halt immediately and report a phase-level blocking failure. Do not proceed to any subsequent step.
[→ Collection of File Entries enriched with content_hash — prerequisite gate]

**Step 3 — Validate input collection presence.**
Confirm that the received collection is non-null and non-empty. If the collection is absent or empty, halt and report a blocking failure per FH-2.1.
[→ Collection of File Entries enriched with content_hash — prerequisite gate]

**Step 4 — Validate structural integrity of each File Entry.**
For each File Entry in the collection, confirm that `file_path` is non-null and non-empty, and that `file_size` is a non-negative integer. Flag and handle any entry that fails this check as a blocking failure for that entry.
[→ Collection of File Entries enriched with content_hash — prerequisite gate]

**Step 5 — Select the declared hashing algorithm.**
Retrieve the algorithm identifier resolved by OQ-1. Confirm that this algorithm is consistently available for application to all File Entries in this execution. Do not proceed if the algorithm cannot be confirmed.
[→ Collection of File Entries enriched with content_hash — prerequisite gate]

**Step 6 — For each File Entry: verify file accessibility.**
For each File Entry, verify that the file referenced by `file_path` exists and is accessible as a regular file at hash-computation time. If a file is inaccessible, apply the policy resolved by OQ-8 (skip silently, skip with warning, or abort).
[→ Collection of File Entries enriched with content_hash]

**Step 7 — For each File Entry: read the full file content.**
Open and read the complete content of the file referenced by `file_path`. A partial read must not be used as input to hash computation. If a read failure occurs mid-operation, treat the entry as unreadable and apply OQ-8 policy.
[→ Collection of File Entries enriched with content_hash]

**Step 8 — For each File Entry: compute the content hash.**
Apply the algorithm declared in OQ-1 to the full content read in Step 7. Produce a single hash value for the entry.
[→ Collection of File Entries enriched with content_hash]

**Step 9 — For each File Entry: bind the hash to its file_path.**
Associate the computed `content_hash` value exclusively with the `file_path` from which the content was read. Record this binding so that traceability from hash to source path is preserved through Phase 3.
[→ Collection of File Entries enriched with content_hash — traceability guarantee]

**Step 10 — For each File Entry: construct the enriched File Entry.**
Combine the original `file_path`, the original `file_size` (unchanged), and the newly computed `content_hash` into a single enriched File Entry. The `file_path` and `file_size` must be identical to the values received from Phase 1.
[→ Collection of File Entries enriched with content_hash]

**Step 11 — Validate the output collection count.**
After processing all File Entries, confirm that the output collection count matches the input collection count, accounting only for entries explicitly excluded under OQ-8 policy. Any unexplained count discrepancy is a blocking failure.
[→ Collection of File Entries enriched with content_hash — output guarantee]

**Step 12 — Validate each output File Entry for completeness.**
For each entry in the output collection, confirm that `file_path`, `file_size`, and `content_hash` are all present and non-null. An entry missing any field must not be forwarded to Phase 3.
[→ Collection of File Entries enriched with content_hash — output guarantee]

**Step 13 — Apply TRACE_REGISTRY check.**
For each construct in the output, verify that its BETO-TRACE annotation ID exists in the TRACE_REGISTRY of this BETO_CORE. Apply the TRACE_REGISTRY CHECK policy declared in Section 5. Set artifact status to TRACE_VERIFIED if all IDs pass.
[→ Collection of File Entries enriched with content_hash — TRACE_VERIFIED guarantee]

**Step 14 — Emit the validated output collection to Phase 3.**
Forward the complete, validated, enriched File Entry collection to Phase 3 (Grouping) via the declared dependency EDGE.DEP-HASHER-DUPLICATE_DETECTOR.
[→ Collection of File Entries enriched with content_hash]

---

## 8. HANDOFF TO NEXT PHASE

- The output collection contains File Entries each carrying exactly three fields: `file_path`, `file_size`, and `content_hash`. All three fields are guaranteed to be present and non-null in every entry forwarded.
- The `file_path` and `file_size` values in each output entry are identical to the values received from Phase 1. They have not been modified, normalized, or reinterpreted by Phase 2.
- The `content_hash` in each output entry was computed from the full content of the file referenced by `file_path`, using the single algorithm resolved by OQ-1. Partial hashes are guaranteed not to be present in the output.
- Each `content_hash` is bound exclusively to the `file_path` from which it was computed. No hash-to-path reassignment has occurred.
- The algorithm used to produce all `content_hash` values is uniform across the entire collection. Phase 3 may treat all hash values as produced by the same algorithm and directly comparable.
- The output collection count equals the input collection count minus any entries explicitly excluded under the policy resolved by OQ-8. Phase 3 must not assume that the output collection is identical in count to the original filesystem traversal without accounting for OQ-8 exclusions.
- The output artifact has passed the TRACE_REGISTRY CHECK and carries TRACE_VERIFIED status.
- **What remains unresolved and must NOT be assumed:** OQ-2 (size pre-filtering) and OQ-3 (zero-byte file policy) may still be open. Phase 3 must not assume that zero-byte files have been excluded or that any size-based filtering was applied, unless the resolutions of OQ-2 and OQ-3 are explicitly forwarded as part of the handoff context. Phase 3 must not re-evaluate hashing algorithm choices; OQ-1 is closed for the purposes of this execution.
- The concrete format and serialization of the collection are not declared. Phase 3 must consume the collection in whatever form it is produced, consistent with the absence of a declared format in BETO_CORE.

---

## END OF DOCUMENT