from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from .models import LogEvent


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC6.CONCEPT.LOG_SOURCE
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_MONITOR_PY
@dataclass
class _FileState:
    inode: int
    offset: int


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC7.PHASE.LOG_MONITORING
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC6.CONCEPT.CANDIDATE_ERROR_EVENT
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_MONITOR_PY
class DirectoryLogMonitor:
    def __init__(self, log_dir: Path) -> None:
        self.log_dir = log_dir
        self._states: dict[Path, _FileState] = {}

    def poll(self) -> list[LogEvent]:
        events: list[LogEvent] = []
        current_files = set(self._iter_files())

        for path in current_files:
            events.extend(self._read_new_events(path))

        # Drop state for files that no longer exist in the directory.
        for path in list(self._states):
            if path not in current_files:
                del self._states[path]

        return events

    def _iter_files(self) -> Iterator[Path]:
        if not self.log_dir.is_dir():
            raise FileNotFoundError(f"log directory does not exist: {self.log_dir}")

        for entry in sorted(self.log_dir.iterdir()):
            if entry.is_file():
                yield entry

    def _read_new_events(self, path: Path) -> list[LogEvent]:
        stat_result = path.stat()
        previous = self._states.get(path)
        offset = 0
        if previous and previous.inode == stat_result.st_ino and stat_result.st_size >= previous.offset:
            offset = previous.offset

        events: list[LogEvent] = []
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            handle.seek(offset)
            for line in handle:
                event = self._build_event(path, line)
                if event is not None:
                    events.append(event)
            new_offset = handle.tell()

        self._states[path] = _FileState(inode=stat_result.st_ino, offset=new_offset)
        return events

    def _build_event(self, path: Path, raw_line: str) -> LogEvent | None:
        if "ERROR" not in raw_line:
            return None

        _, tail = raw_line.split("ERROR", 1)
        pattern = tail.strip()
        return LogEvent(
            source_path=str(path),
            detection_timestamp=time.time(),
            raw_line=raw_line.rstrip("\n"),
            pattern=pattern,
        )
