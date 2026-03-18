"""
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
BETO-TRACE: BETO_V44.SEC8.DECISION.EXECUTOR_CONVENTIONS

execution_router — BETO v4.4 internal routing module.

Provides deterministic complexity scoring and path selection for the
BETO executor. All sub-executors are orchestrated through this module.
No sub-executor may call another sub-executor without passing through
the ExecutionRouter.
"""

from .complexity_scorer import ComplexityScorer, ComplexityFactors
from .path_registry import ExecutionPath, RouteDecision, RoutePromotion
from .router import ExecutionRouter
from .snapshot_writer import SnapshotWriter
from .project_index_writer import ProjectIndexWriter

__all__ = [
    "ComplexityScorer",
    "ComplexityFactors",
    "ExecutionPath",
    "RouteDecision",
    "RoutePromotion",
    "ExecutionRouter",
    "SnapshotWriter",
    "ProjectIndexWriter",
]
