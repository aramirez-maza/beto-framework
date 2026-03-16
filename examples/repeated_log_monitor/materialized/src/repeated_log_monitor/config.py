from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC3.INPUT.CONFIGURABLE_DIRECTORY_PATH
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC3.INPUT.REPETITION_THRESHOLD_N
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC3.INPUT.REPETITION_TIME_WINDOW
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC3.INPUT.LOCAL_ALERTS_FILE_PATH
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_CONFIG_PY
@dataclass(frozen=True)
class MonitorConfig:
    log_dir: Path
    threshold: int
    window_seconds: int
    alerts_file: Path
    poll_interval: float


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_CONFIG_PY
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.PYTHON_STANDARD_LIBRARY_ONLY_IMPLEMENTATION
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Monitor a directory of log files and alert on repeated errors.",
    )
    parser.add_argument("log_dir", type=Path, help="Directory containing log files.")
    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Number of repeated occurrences required to emit an alert.",
    )
    parser.add_argument(
        "--window-seconds",
        type=int,
        default=60,
        help="Time window used to count repeated occurrences.",
    )
    parser.add_argument(
        "--alerts-file",
        type=Path,
        default=Path("alerts.log"),
        help="Append-only local alerts file.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="Seconds to wait between directory scans.",
    )
    return parser


# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC8.DECISION.OUTPUT_FILE_CONFIG_PY
# BETO-TRACE: BETO_REPEATED_LOG_MONITOR.SEC10.CONSTRAINT.LINUX_ONLY_ENVIRONMENT
def parse_config(argv: list[str] | None = None) -> MonitorConfig:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.threshold <= 0:
        parser.error("--threshold must be greater than zero")
    if args.window_seconds <= 0:
        parser.error("--window-seconds must be greater than zero")
    if args.poll_interval <= 0:
        parser.error("--poll-interval must be greater than zero")

    return MonitorConfig(
        log_dir=args.log_dir,
        threshold=args.threshold,
        window_seconds=args.window_seconds,
        alerts_file=args.alerts_file,
        poll_interval=args.poll_interval,
    )
