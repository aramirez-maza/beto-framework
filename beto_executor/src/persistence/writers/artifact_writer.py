"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.ARTIFACT_WRITER

Writes artifact records to SQLite during REGISTRAR_ARTEFACTO events.
Reuses the same classification logic used by ProjectIndexWriter.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection

# File type classification (mirrors ProjectIndexWriter._file_type)
_FILE_TYPE_MAP = {
    "BETO_CORE": "BETO_CORE",
    "BETO_SYSTEM_GRAPH": "SYSTEM_GRAPH",
    "MANIFEST_PROYECTO": "MANIFEST_PROYECTO",
    "MANIFEST_BETO": "MANIFEST_BETO",
    "PHASE_": "PHASE_DOC",
    "CIERRE_ASISTIDO": "CIERRE_ASISTIDO",
    "PASO_": "PASO_DOC",
    "FRAMEWORK_FEEDBACK": "FRAMEWORK_FEEDBACK",
    "OPERATIONAL_LESSONS": "OPERATIONAL_LESSONS",
    "TRACE_REGISTRY": "TRACE_REGISTRY",
}

_ROLE_MAP = {
    "MANIFEST_PROYECTO": "authority",
    "BETO_SYSTEM_GRAPH": "authority",
    "BETO_CORE": "authority",
    "TRACE_REGISTRY": "authority",
}


def _classify_file(file_name: str) -> tuple[str, str, str]:
    """Returns (file_type, role, route_relevance)."""
    name_upper = file_name.upper()

    file_type = "OTHER"
    for prefix, ftype in _FILE_TYPE_MAP.items():
        if name_upper.startswith(prefix):
            file_type = ftype
            break

    role = _ROLE_MAP.get(file_type, "documentation")

    route_relevance = "ALL_ROUTES"

    return file_type, role, route_relevance


class ArtifactDBWriter:
    """
    Writes artifact records to SQLite.

    Artifact semantics — "current" vs "previous version":

    BETO artifacts are files on disk. When a step is re-run (after gate
    rejection or retroceso), the file is overwritten. There is no notion
    of "previous version" in the DB — the ON CONFLICT UPDATE strategy means
    the latest write wins, mirroring what happens on disk.

    "Vigente" (current) = present in the artifacts table with the latest
    updated_at. Every row in this table represents the most recent
    materialization of that (cycle_id, file_path) pair.

    Version history is not tracked here — that is the responsibility of
    the VCS (git). This keeps the schema simple and Phase 2 rendering
    deterministic: all artifacts rows are implicitly current.

    If explicit version tracking is needed in the future, add a `generation`
    INTEGER column (default 1, incremented on each upsert) as a Phase 3 task.
    """

    def __init__(self, beto_dir: Path, cycle_id: str) -> None:
        self.beto_dir = beto_dir
        self.cycle_id = cycle_id

    def write(
        self,
        file_path: str,
        paso: int,
        trace_ids: list[str] | None = None,
    ) -> None:
        """
        Upsert an artifact record.
        file_path: relative or absolute path to the artifact file.
        """
        file_name = Path(file_path).name
        file_type, role, route_relevance = _classify_file(file_name)

        conn = get_connection(self.beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT INTO artifacts (
                        cycle_id, file_path, file_name, file_type, role,
                        route_relevance, paso_generado, v43_compatible,
                        trace_ids, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                    ON CONFLICT(cycle_id, file_path) DO UPDATE SET
                        file_type       = excluded.file_type,
                        paso_generado   = excluded.paso_generado,
                        trace_ids       = excluded.trace_ids,
                        updated_at      = excluded.updated_at
                    """,
                    (
                        self.cycle_id,
                        file_path,
                        file_name,
                        file_type,
                        role,
                        route_relevance,
                        paso,
                        json.dumps(trace_ids or [], ensure_ascii=False),
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
        finally:
            conn.close()
