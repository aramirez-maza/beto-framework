"""
BETO persistence writers — Phase 1 dual-write layer.

Each writer is stateless: instantiate, call, done.
All writers follow the same pattern:
  - Accept beto_dir as the first argument
  - Obtain connection via get_connection(beto_dir)
  - Execute write inside a transaction
  - Close connection before returning
  - Silently log warnings on failure (never block the executor)
"""

from .cycle_writer import CycleWriter
from .routing_writer import RoutingWriter
from .snapshot_writer import SnapshotDBWriter
from .oq_writer import OQWriter
from .artifact_writer import ArtifactDBWriter
from .gate_writer import GateWriter
from .model_call_writer import ModelCallWriter

__all__ = [
    "CycleWriter",
    "RoutingWriter",
    "SnapshotDBWriter",
    "OQWriter",
    "ArtifactDBWriter",
    "GateWriter",
    "ModelCallWriter",
]
