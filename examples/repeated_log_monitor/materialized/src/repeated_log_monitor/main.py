from __future__ import annotations

import sys
import time

from .alerts import append_alert, render_console_alert
from .config import parse_config
from .detector import RepetitionDetector
from .monitor import DirectoryLogMonitor


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_MAIN_PY
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.PYTHON_STANDARD_LIBRARY_ONLY_IMPLEMENTATION
def run(argv: list[str] | None = None) -> int:
    config = parse_config(argv)
    monitor = DirectoryLogMonitor(config.log_dir)
    detector = RepetitionDetector(
        threshold=config.threshold,
        window_seconds=config.window_seconds,
    )

    try:
        while True:
            for event in monitor.poll():
                alert = detector.process(event)
                if alert is None:
                    continue
                print(render_console_alert(alert), flush=True)
                append_alert(alert, config.alerts_file)
            time.sleep(config.poll_interval)
    except KeyboardInterrupt:
        return 0
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC1.INTENT.LIGHTWEIGHT_LOG_MONITORING_TOOL
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_MAIN_PY
def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
