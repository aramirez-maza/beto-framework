from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .models import AlertEvent


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC7.PHASE.ALERT_EMISSION
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC3.OUTPUT.LOCAL_CONSOLE_ALERT
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_ALERTS_PY
def render_console_alert(alert: AlertEvent) -> str:
    return "\n".join(
        [
            "ALERT: repeated error detected",
            f'pattern: "{alert.pattern}"',
            f"count: {alert.count}",
            f"time_window: {alert.window_seconds} seconds",
        ]
    )


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC3.OUTPUT.PERSISTED_ALERT_EVENT
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.APPEND_ONLY_PLAIN_TEXT_ALERTS_FILE
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_ALERTS_PY
def append_alert(alert: AlertEvent, alerts_file: Path) -> None:
    alerts_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    line = (
        f"{timestamp}\tpattern={alert.pattern}\tcount={alert.count}"
        f"\twindow_seconds={alert.window_seconds}\n"
    )
    with alerts_file.open("a", encoding="utf-8") as handle:
        handle.write(line)
