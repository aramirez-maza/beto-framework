from __future__ import annotations

from collections import defaultdict, deque

from .models import AlertEvent, LogEvent


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC7.PHASE.REPETITION_DETECTION
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC6.CONCEPT.REPEATED_ERROR_PATTERN
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_DETECTOR_PY
class RepetitionDetector:
    def __init__(self, threshold: int, window_seconds: int) -> None:
        self.threshold = threshold
        self.window_seconds = window_seconds
        self._events_by_pattern: dict[str, deque[LogEvent]] = defaultdict(deque)
        self._active_patterns: set[str] = set()

    def process(self, event: LogEvent) -> AlertEvent | None:
        bucket = self._events_by_pattern[event.pattern]
        bucket.append(event)
        cutoff = event.detection_timestamp - self.window_seconds

        while bucket and bucket[0].detection_timestamp < cutoff:
            bucket.popleft()

        count = len(bucket)
        if count >= self.threshold and event.pattern not in self._active_patterns:
            self._active_patterns.add(event.pattern)
            return AlertEvent(
                pattern=event.pattern,
                count=count,
                window_seconds=self.window_seconds,
                first_seen_timestamp=bucket[0].detection_timestamp,
                last_seen_timestamp=bucket[-1].detection_timestamp,
            )

        if count < self.threshold:
            self._active_patterns.discard(event.pattern)

        return None
