# duplicate_file_finder

CLI tool that scans a directory recursively, detects duplicate files by content hash (SHA-256), and generates a report showing duplicate groups, file paths, and total recoverable space.

**BETO cycle:** `14210d80-17ee-404b-a58e-3709ede76d78`
**Executor version:** BETO v4.5.0
**Models:** Reasoning — claude-sonnet-4-6 · Code — qwen-coder (vLLM)
**Result:** 6 source files — 72 BETO-TRACE IDs — 100% TRACE_VERIFIED — 0 silent completions

---

## Requirements

- Python 3.11+
- No external dependencies — stdlib only (`hashlib`, `os`, `argparse`, `json`)

---

## Installation

```bash
git clone https://github.com/aramirez-maza/beto-framework.git
cd beto-framework/examples/duplicate_file_finder/materialized/src
```

No `pip install` required.

---

## Usage

```bash
python3 duplicate_finder/main.py <target_directory>
```

**Example:**

```bash
python3 duplicate_finder/main.py /home/user/Documents
```

**Output:**

```
Duplicate Groups Report:
Content Hash: a3f1c2d...
File Paths:
  /home/user/Documents/report.pdf
  /home/user/Documents/backup/report.pdf
Recoverable Bytes: 204800

Total Recoverable Bytes: 204800
```

---

## System Structure

| Module | Responsibility |
|--------|---------------|
| `duplicate_finder/main.py` | CLI entry point — orchestrates the full pipeline |
| `scanner/scanner.py` | Recursive directory scan, SHA-256 hash per file |
| `hasher/hasher.py` | Hash computation (chunked reads, 4096 bytes) |
| `duplicate_detector/duplicate_detector.py` | Groups files by content hash, filters singletons |
| `space_calculator/space_calculator.py` | Calculates recoverable bytes per group and total |
| `report_composer/report_composer.py` | Generates JSON or plain text report |

---

## Running the Tests

```bash
cd examples/duplicate_file_finder
python3 -m pytest tests/test_duplicate_finder.py -v
```

Expected result: **26/26 passed**

---

## BETO Traceability

Every function and class in this system is annotated with a `BETO-TRACE` ID that maps back to an operator-authorized specification decision. The full trace chain:

```
Source code line
  → BETO-TRACE annotation
  → TRACE_REGISTRY_DUPLICATE_FILE_FINDER_CLI.md
  → MANIFEST_PROYECTO.md (approved at G-3)
  → BETO_SYSTEM_GRAPH.md (approved at G-2)
  → BETO_CORE_DRAFT.md (approved at G-1)
```

BETO specification artifacts are in the parent directory (`examples/duplicate_file_finder/`).
