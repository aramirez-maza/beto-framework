"""
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG

Path registry for BETO v4.4 routing.

Declares the three execution paths, route decision records, and route
promotion records. All data classes used in ROUTING_DECISION_RECORD
and ROUTE_PROMOTION_RECORD artifacts.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


# BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_THRESHOLDS
class ExecutionPath(str, Enum):
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

    The three declared execution paths of BETO v4.4.
    Score thresholds: LIGHT 0-5, PARTIAL 6-12, FULL 13+
    """
    BETO_LIGHT_PATH = "BETO_LIGHT_PATH"
    BETO_PARTIAL_PATH = "BETO_PARTIAL_PATH"
    BETO_FULL_PATH = "BETO_FULL_PATH"


class PromotionTransition(str, Enum):
    """Declared promotion transitions — no others are authorized."""
    LIGHT_TO_PARTIAL = "LIGHT_TO_PARTIAL"
    PARTIAL_TO_FULL = "PARTIAL_TO_FULL"
    LIGHT_TO_FULL = "LIGHT_TO_FULL"


@dataclass
class ContextLayersUsed:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

    Documents which context layers were included in the model call.
    Layer A is always true. Layer B and C are path-dependent.
    """
    layer_a: bool = True               # STABLE_CORE_CONTEXT — always required
    layer_b: bool = False              # CYCLE_CONTEXT — required for PARTIAL and FULL
    layer_b_scope: str = "none"        # "none" | "minimal" | "full" | "unit_only"
    layer_c: bool = True               # LOCAL_EXECUTION_CONTEXT — always required


@dataclass
class RouteDecision:
    """
    BETO-TRACE: BETO_V44.SEC9.ROUTING_DECISION.RECORD

    Serializable record of a routing decision.
    Maps to the ROUTING_DECISION_RECORD template.
    Every routing decision must produce one RouteDecision.
    No routing decision may be silent.
    """
    decision_id: str                    # RD-YYYY-NNNN
    cycle_id: str
    route_selected: ExecutionPath
    raw_score: float
    complexity_breakdown: dict          # output of ComplexityScorer.score_breakdown()
    executor_assigned: str
    trace_anchor: str
    justification: str
    context_layers: ContextLayersUsed = field(default_factory=ContextLayersUsed)
    unit_id: str = ""
    step_context: str = ""
    subproblem_description: str = ""
    snapshots_applied: list[dict] = field(default_factory=list)
    weights_used: str = "v4.4_defaults"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "decision_id": self.decision_id,
            "timestamp": self.timestamp,
            "cycle_id": self.cycle_id,
            "unit_id": self.unit_id or None,
            "step_context": self.step_context,
            "subproblem_description": self.subproblem_description,
            "complexity_evaluation": self.complexity_breakdown,
            "route_selected": self.route_selected.value,
            "context_layers_authorized": {
                "layer_a": self.context_layers.layer_a,
                "layer_b": self.context_layers.layer_b,
                "layer_b_scope": self.context_layers.layer_b_scope,
                "layer_c": self.context_layers.layer_c,
            },
            "snapshots_applied": self.snapshots_applied,
            "executor_assigned": self.executor_assigned,
            "trace_anchor": self.trace_anchor,
            "justification": self.justification,
        }


@dataclass
class PromotionTriggers:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

    All declared trigger conditions for a route promotion.
    At least one must be True for a promotion to be valid.
    """
    oq_critical_unabsorbable: bool = False
    graph_required: bool = False
    manifest_new_required: bool = False
    scope_became_multiunit: bool = False
    ambiguity_exceeded_threshold: bool = False
    structural_authority_required: bool = False

    def any_triggered(self) -> bool:
        return any([
            self.oq_critical_unabsorbable,
            self.graph_required,
            self.manifest_new_required,
            self.scope_became_multiunit,
            self.ambiguity_exceeded_threshold,
            self.structural_authority_required,
        ])

    def to_dict(self) -> dict:
        return {
            "oq_critical_unabsorbable": self.oq_critical_unabsorbable,
            "graph_required": self.graph_required,
            "manifest_new_required": self.manifest_new_required,
            "scope_became_multiunit": self.scope_became_multiunit,
            "ambiguity_exceeded_threshold": self.ambiguity_exceeded_threshold,
            "structural_authority_required": self.structural_authority_required,
        }


@dataclass
class RoutePromotion:
    """
    BETO-TRACE: BETO_V44.SEC9.ROUTE_PROMOTION.RECORD

    Serializable record of a route promotion.
    Maps to the ROUTE_PROMOTION_RECORD template.
    Every route promotion must produce one RoutePromotion.
    No route promotion may be silent.
    """
    promotion_id: str                          # RP-YYYY-NNNN
    cycle_id: str
    original_decision_id: str                  # RD-id that is being promoted
    promotion_transition: PromotionTransition
    new_route: ExecutionPath
    triggers: PromotionTriggers
    trigger_description: str
    trace_anchor: str
    unit_id: str = ""
    impact_on_current_execution: str = ""
    operator_notification_required: bool = False
    operator_notification_text: str = ""
    snapshots_invalidated: list[dict] = field(default_factory=list)
    new_snapshots_required: list[dict] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self) -> None:
        if not self.triggers.any_triggered():
            raise ValueError(
                f"RoutePromotion {self.promotion_id}: at least one trigger condition "
                f"must be True. A promotion without declared triggers is not authorized."
            )

    def to_dict(self) -> dict:
        return {
            "promotion_id": self.promotion_id,
            "timestamp": self.timestamp,
            "cycle_id": self.cycle_id,
            "unit_id": self.unit_id or None,
            "original_decision_id": self.original_decision_id,
            "promotion_transition": self.promotion_transition.value,
            "trigger_conditions": self.triggers.to_dict(),
            "trigger_description": self.trigger_description,
            "new_route": self.new_route.value,
            "impact_on_current_execution": self.impact_on_current_execution,
            "operator_notification_required": self.operator_notification_required,
            "operator_notification_text": self.operator_notification_text,
            "snapshots_invalidated": self.snapshots_invalidated,
            "new_snapshots_required": self.new_snapshots_required,
        }
