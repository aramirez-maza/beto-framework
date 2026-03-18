"""
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

ProjectIndexWriter — generates .beto/project_index.json.

Conforms to framework/PROJECT_INDEX_SCHEMA.json (v4.4.0).
Indexes all cycle artifacts: markdown docs, routing decisions, snapshots.

NOT a semantic authority — localization only.
Semantic authority remains in BETO_CORE, graph, manifests, contracts.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


# ─── Classification helpers ───────────────────────────────────────────────────

# Maps filename prefix → file_type enum value (from PROJECT_INDEX_SCHEMA.json)
_FILE_TYPE_PREFIXES: list[tuple[str, str]] = [
    ("BETO_CORE_DRAFT", "BETO_CORE"),
    ("BETO_CORE_", "BETO_CORE"),
    ("BETO_SYSTEM_GRAPH", "SYSTEM_GRAPH"),
    ("MANIFEST_PROYECTO", "MANIFEST_PROYECTO"),
    ("MANIFEST_BETO", "MANIFEST_BETO"),
    ("TRACE_REGISTRY", "TRACE_REGISTRY"),
    ("PHASE_", "PHASE_DOC"),
    ("STRUCTURAL_CLASSIFICATION", "OTHER"),
    ("PASO_0", "OTHER"),
    ("CIERRE_ASISTIDO", "OTHER"),
    ("EXECUTIONAL_GAP_REGISTRY", "OTHER"),
    ("EXECUTION_INTENT_MAP", "OTHER"),
]

_ROLE_PREFIXES: list[tuple[str, str]] = [
    ("BETO_CORE", "authority"),
    ("BETO_SYSTEM_GRAPH", "authority"),
    ("MANIFEST", "authority"),
    ("TRACE_REGISTRY", "authority"),
    ("PHASE_", "authority"),
]

_ROUTE_RELEVANCE_PREFIXES: list[tuple[str, str]] = [
    ("BETO_SYSTEM_GRAPH", "FULL_ONLY"),
    ("BETO_CORE", "PARTIAL_AND_FULL"),
    ("MANIFEST", "PARTIAL_AND_FULL"),
    ("TRACE_REGISTRY", "PARTIAL_AND_FULL"),
    ("PHASE_", "PARTIAL_AND_FULL"),
]


def _classify(name: str, table: list[tuple[str, str]], default: str) -> str:
    stem = name.replace(".md", "").replace(".json", "")
    for prefix, value in table:
        if stem.startswith(prefix):
            return value
    return default


def _file_type(name: str) -> str:
    return _classify(name, _FILE_TYPE_PREFIXES, "OTHER")


def _role(name: str) -> str:
    return _classify(name, _ROLE_PREFIXES, "documentation")


def _route_relevance(name: str) -> str:
    return _classify(name, _ROUTE_RELEVANCE_PREFIXES, "ALL_ROUTES")


# ─── Writer ───────────────────────────────────────────────────────────────────

class ProjectIndexWriter:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS
    BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG

    Generates .beto/project_index.json from cycle artifacts.
    Indexes: cycle markdown docs, routing decisions, snapshots.
    """

    def __init__(self, beto_dir: Path, ciclo_id: str) -> None:
        # BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG (storage path OQ-2)
        self.beto_dir = beto_dir
        self.ciclo_id = ciclo_id

    def write(
        self,
        cycle_dir: Path,
        updated_by: str = "materialization_executor",
        routing_config: dict | None = None,
    ) -> Path:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_3_OPERATIONAL_ARTIFACTS

        Index all artifacts in cycle_dir and write project_index.json.
        Returns path to the written index file.

        Indexes:
          1. Markdown artifacts in cycle_dir
          2. ROUTING_DECISION_RECORD files in .beto/routing/decisions/
          3. ROUTE_PROMOTION_RECORD files in .beto/routing/promotions/
          4. Snapshot files in .beto/snapshots/
        """
        now = datetime.now(timezone.utc).isoformat()
        entries: list[dict] = []

        # — Markdown artifacts in cycle_dir —
        for f in sorted(cycle_dir.glob("*.md")):
            entries.append({
                "file": f.name,
                "file_type": _file_type(f.name),
                "role": _role(f.name),
                "phase_associated": None,
                "unit_id": None,
                "dependencies": [],
                "trace_ids_authorized": [],
                "manifest_associated": None,
                "contract_associated": None,
                "materialization_status": "COMPLETE",
                "last_updated": now,
                "route_relevance": _route_relevance(f.name),
                "execution_locality": "GLOBAL",
                "snapshot_dependencies": [],
                "v43_compatibility": "COMPATIBLE",
            })

        # — ROUTING_DECISION_RECORD files —
        decisions_dir = self.beto_dir / "routing" / "decisions"
        if decisions_dir.exists():
            for f in sorted(decisions_dir.glob("*.json")):
                rel = str(f.relative_to(cycle_dir.parent))
                entries.append({
                    "file": rel,
                    "file_type": "ROUTING_DECISION_RECORD",
                    "role": "routing",
                    "phase_associated": None,
                    "unit_id": None,
                    "dependencies": [],
                    "trace_ids_authorized": ["BETO_V44.SEC9.ROUTING_DECISION.RECORD"],
                    "manifest_associated": None,
                    "contract_associated": None,
                    "materialization_status": "COMPLETE",
                    "last_updated": now,
                    "route_relevance": "ALL_ROUTES",
                    "execution_locality": "GLOBAL",
                    "snapshot_dependencies": [],
                    "v43_compatibility": "NEW_IN_V44",
                })

        # — ROUTE_PROMOTION_RECORD files —
        promotions_dir = self.beto_dir / "routing" / "promotions"
        if promotions_dir.exists():
            for f in sorted(promotions_dir.glob("*.json")):
                rel = str(f.relative_to(cycle_dir.parent))
                entries.append({
                    "file": rel,
                    "file_type": "ROUTE_PROMOTION_RECORD",
                    "role": "routing",
                    "phase_associated": None,
                    "unit_id": None,
                    "dependencies": [],
                    "trace_ids_authorized": ["BETO_V44.SEC9.ROUTE_PROMOTION.RECORD"],
                    "manifest_associated": None,
                    "contract_associated": None,
                    "materialization_status": "COMPLETE",
                    "last_updated": now,
                    "route_relevance": "ALL_ROUTES",
                    "execution_locality": "GLOBAL",
                    "snapshot_dependencies": [],
                    "v43_compatibility": "NEW_IN_V44",
                })

        # — Snapshot files —
        snapshots_dir = self.beto_dir / "snapshots"
        if snapshots_dir.exists():
            for f in sorted(snapshots_dir.glob("*.json")):
                rel = str(f.relative_to(cycle_dir.parent))
                # Determine snapshot type from prefix
                prefix = f.stem.split("-")[0]  # LC, CS, AQ, MS
                snap_type_map = {
                    "LC": "LOCAL_EXECUTION_CONTEXT",
                    "CS": "CYCLE_CONTEXT_SNAPSHOT",
                    "AQ": "ACTIVE_OQ_SET",
                    "MS": "MATERIALIZATION_SCOPE",
                }
                snap_file_type = snap_type_map.get(prefix, "CYCLE_CONTEXT_SNAPSHOT")
                entries.append({
                    "file": rel,
                    "file_type": snap_file_type,
                    "role": "snapshot",
                    "phase_associated": None,
                    "unit_id": None,
                    "dependencies": [],
                    "trace_ids_authorized": [
                        "BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT"
                    ],
                    "manifest_associated": None,
                    "contract_associated": None,
                    "materialization_status": "COMPLETE",
                    "last_updated": now,
                    "route_relevance": "PARTIAL_AND_FULL" if prefix != "LC" else "ALL_ROUTES",
                    "execution_locality": "SUBPROBLEM_LOCAL",
                    "snapshot_dependencies": [],
                    "v43_compatibility": "NEW_IN_V44",
                })

        config = routing_config or {
            "light_max": 5,
            "partial_max": 12,
            "full_min": 13,
            "weights": {
                "w1": 1, "w2": 1, "w3": 1, "w4": 2,
                "w5": 3, "w6": 2, "w7": 2, "w8": 2,
            },
            "weights_version": "v4.4_defaults",
        }

        index = {
            "index_metadata": {
                "cycle_id": self.ciclo_id,
                "version": "4.4.0",
                "last_updated": now,
                "last_updated_by": updated_by,
                "total_entries": len(entries),
                "routing_config": config,
            },
            "entries": entries,
        }

        self.beto_dir.mkdir(parents=True, exist_ok=True)
        path = self.beto_dir / "project_index.json"
        path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
