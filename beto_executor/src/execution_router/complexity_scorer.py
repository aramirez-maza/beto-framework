"""
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG
BETO-TRACE: BETO_V44.SEC9.OQ.OQ1_WEIGHTS

Complexity scorer for BETO v4.4 internal routing.

Evaluates a sub-problem's complexity using the declared function:

  complexity_score =
    w1 * num_outputs +
    w2 * num_entities +
    w3 * num_dependencies +
    w4 * ambiguity_level +
    w5 * need_for_graph +
    w6 * oq_critical_count +
    w7 * cross_module_scope +
    w8 * lifecycle_scope

Default weights (v4.4 — OQ-1 DECLARED [BETO_ASSISTED]):
  w1=1, w2=1, w3=1, w4=2, w5=3, w6=2, w7=2, w8=2

Default thresholds:
  LIGHT  → 0–5
  PARTIAL → 6–12
  FULL   → 13+
"""

from __future__ import annotations
from dataclasses import dataclass, field


# BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG
# Default weights — declared in BETO_CORE_DRAFT OQ-1 [BETO_ASSISTED]
# These are the canonical defaults. Override via RoutingConfig.
DEFAULT_WEIGHTS = {
    "w1": 1.0,   # num_outputs
    "w2": 1.0,   # num_entities
    "w3": 1.0,   # num_dependencies
    "w4": 2.0,   # ambiguity_level — higher: ambiguity is a strong discriminant
    "w5": 3.0,   # need_for_graph — highest: graph requirement → FULL path
    "w6": 2.0,   # oq_critical_count — higher: critical OQs require more structure
    "w7": 2.0,   # cross_module_scope — higher: multi-module means more coordination
    "w8": 2.0,   # lifecycle_scope — higher: multi-step BETO processes require FULL
}

# BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG
DEFAULT_THRESHOLDS = {
    "light_max": 5,    # 0–5 → BETO_LIGHT_PATH
    "partial_max": 12,  # 6–12 → BETO_PARTIAL_PATH
    "full_min": 13,     # 13+ → BETO_FULL_PATH
}

WEIGHTS_VERSION = "v4.4_defaults"


@dataclass
class ComplexityFactors:
    """
    BETO-TRACE: BETO_V44.SEC4.FIELD.COMPLEXITY_FACTORS

    All eight declared factors of the complexity function.
    All factors must be declared explicitly — no silent defaults except zero.
    """
    num_outputs: int = 0
    num_entities: int = 0
    num_dependencies: int = 0
    ambiguity_level: int = 0        # 0, 1, 2, or 3
    need_for_graph: int = 0         # 0 or 1
    oq_critical_count: int = 0
    cross_module_scope: int = 0     # 0 or 1
    lifecycle_scope: int = 0        # 0 or 1

    def __post_init__(self) -> None:
        if self.ambiguity_level not in (0, 1, 2, 3):
            raise ValueError(
                f"ambiguity_level must be 0, 1, 2, or 3 — got {self.ambiguity_level}"
            )
        if self.need_for_graph not in (0, 1):
            raise ValueError(
                f"need_for_graph must be 0 or 1 — got {self.need_for_graph}"
            )
        if self.cross_module_scope not in (0, 1):
            raise ValueError(
                f"cross_module_scope must be 0 or 1 — got {self.cross_module_scope}"
            )
        if self.lifecycle_scope not in (0, 1):
            raise ValueError(
                f"lifecycle_scope must be 0 or 1 — got {self.lifecycle_scope}"
            )


@dataclass
class RoutingConfig:
    """
    BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG

    Configurable routing parameters. Defaults are the v4.4 canonical values.
    If not explicitly provided, defaults are used and must be logged as
    'v4.4_defaults' in every ROUTING_DECISION_RECORD.
    """
    weights: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))
    thresholds: dict[str, int] = field(default_factory=lambda: dict(DEFAULT_THRESHOLDS))
    weights_version: str = WEIGHTS_VERSION

    def validate(self) -> None:
        required_weights = {"w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8"}
        missing = required_weights - set(self.weights.keys())
        if missing:
            raise ValueError(f"Missing weights in RoutingConfig: {missing}")
        required_thresholds = {"light_max", "partial_max", "full_min"}
        missing_t = required_thresholds - set(self.thresholds.keys())
        if missing_t:
            raise ValueError(f"Missing thresholds in RoutingConfig: {missing_t}")


class ComplexityScorer:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
    BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG

    Deterministic complexity scorer for BETO v4.4 routing.

    Usage:
        scorer = ComplexityScorer()
        factors = ComplexityFactors(num_outputs=2, need_for_graph=1, ...)
        score = scorer.score(factors)
    """

    def __init__(self, config: RoutingConfig | None = None) -> None:
        self.config = config or RoutingConfig()
        self.config.validate()

    def score(self, factors: ComplexityFactors) -> float:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

        Compute complexity_score using the declared function.
        Returns the weighted sum of all eight factors.
        """
        w = self.config.weights
        return (
            w["w1"] * factors.num_outputs
            + w["w2"] * factors.num_entities
            + w["w3"] * factors.num_dependencies
            + w["w4"] * factors.ambiguity_level
            + w["w5"] * factors.need_for_graph
            + w["w6"] * factors.oq_critical_count
            + w["w7"] * factors.cross_module_scope
            + w["w8"] * factors.lifecycle_scope
        )

    def score_breakdown(self, factors: ComplexityFactors) -> dict:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

        Returns detailed breakdown for ROUTING_DECISION_RECORD logging.
        """
        w = self.config.weights
        raw_score = self.score(factors)
        return {
            "num_outputs": factors.num_outputs,
            "num_entities": factors.num_entities,
            "num_dependencies": factors.num_dependencies,
            "ambiguity_level": factors.ambiguity_level,
            "need_for_graph": factors.need_for_graph,
            "oq_critical_count": factors.oq_critical_count,
            "cross_module_scope": factors.cross_module_scope,
            "lifecycle_scope": factors.lifecycle_scope,
            "raw_score": raw_score,
            "weights_used": self.config.weights_version,
        }
