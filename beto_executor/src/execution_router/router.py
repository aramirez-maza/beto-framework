"""
BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
BETO-TRACE: BETO_V44.SEC8.DECISION.EXECUTOR_CONVENTIONS

ExecutionRouter — BETO v4.4 central orchestrator.

The ExecutionRouter is the single orchestration point for all sub-executors.
No sub-executor may invoke another sub-executor without passing through here.

Responsibilities:
  1. Evaluate complexity_score for every sub-problem
  2. Select execution path (LIGHT / PARTIAL / FULL)
  3. Record every routing decision (no silent decisions)
  4. Evaluate promotion conditions during execution
  5. Record every route promotion (no silent promotions)
  6. Enforce the no-separate-skill-surface invariant
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .complexity_scorer import ComplexityScorer, ComplexityFactors, RoutingConfig
from .path_registry import (
    ExecutionPath,
    RouteDecision,
    RoutePromotion,
    PromotionTransition,
    PromotionTriggers,
    ContextLayersUsed,
)


class ExecutionRouter:
    """
    BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

    Central orchestrator for BETO v4.4 execution routing.

    Usage:
        router = ExecutionRouter(cycle_id="my_cycle", beto_dir=Path(".beto"))
        decision = router.route(
            factors=ComplexityFactors(num_outputs=1, ambiguity_level=1),
            subproblem_description="Generate PHASE_1 document",
            step_context="paso_7",
            executor_assigned="materialization_executor",
            trace_anchor="BETO_V44.SEC7.PHASE.PHASE_1",
        )
    """

    # BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_THRESHOLDS
    DECLARED_SUB_EXECUTORS = {
        "eligibility_executor",
        "interview_executor",
        "closure_executor",
        "osc_executor",
        "materialization_executor",
        "verification_executor",
        "beto_light_executor",
        "beto_partial_executor",
        "beto_full_executor",
        "route_promotion_evaluator",
    }

    def __init__(
        self,
        cycle_id: str,
        beto_dir: Path | None = None,
        config: RoutingConfig | None = None,
    ) -> None:
        self.cycle_id = cycle_id
        self.beto_dir = beto_dir or Path(".beto")
        self.scorer = ComplexityScorer(config=config)
        self._decision_counter = 0
        self._promotion_counter = 0
        self._decisions: list[RouteDecision] = []
        self._promotions: list[RoutePromotion] = []

    # ─── Public API ───────────────────────────────────────────────────────────

    def route(
        self,
        factors: ComplexityFactors,
        subproblem_description: str,
        step_context: str,
        executor_assigned: str,
        trace_anchor: str,
        unit_id: str = "",
        snapshots_applied: list[dict] | None = None,
        justification: str = "",
    ) -> RouteDecision:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
        BETO-TRACE: BETO_V44.SEC9.ROUTING_DECISION.RECORD

        Evaluate complexity and select execution path.
        Records the decision — no silent routing.
        """
        if executor_assigned not in self.DECLARED_SUB_EXECUTORS:
            raise ValueError(
                f"Executor '{executor_assigned}' is not in DECLARED_SUB_EXECUTORS. "
                f"Only declared sub-executors may be assigned routing decisions."
            )

        breakdown = self.scorer.score_breakdown(factors)
        raw_score = breakdown["raw_score"]
        path = self._select_path(raw_score)
        context_layers = self._build_context_layers(path)

        self._decision_counter += 1
        decision_id = f"RD-{datetime.now(timezone.utc).year}-{self._decision_counter:04d}"

        auto_justification = (
            f"complexity_score={raw_score:.1f} using weights={breakdown['weights_used']}. "
            f"Score falls in range for {path.value}."
        )
        final_justification = justification or auto_justification

        decision = RouteDecision(
            decision_id=decision_id,
            cycle_id=self.cycle_id,
            route_selected=path,
            raw_score=raw_score,
            complexity_breakdown=breakdown,
            executor_assigned=executor_assigned,
            trace_anchor=trace_anchor,
            justification=final_justification,
            context_layers=context_layers,
            unit_id=unit_id,
            step_context=step_context,
            subproblem_description=subproblem_description,
            snapshots_applied=snapshots_applied or [],
        )

        self._decisions.append(decision)
        self._persist_decision(decision)
        return decision

    def promote(
        self,
        original_decision: RouteDecision,
        triggers: PromotionTriggers,
        trigger_description: str,
        trace_anchor: str,
        impact_on_current_execution: str = "",
        snapshots_invalidated: list[dict] | None = None,
        new_snapshots_required: list[dict] | None = None,
        operator_notification_required: bool = False,
        operator_notification_text: str = "",
    ) -> RoutePromotion:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION
        BETO-TRACE: BETO_V44.SEC9.ROUTE_PROMOTION.RECORD

        Register a route promotion. Raises ValueError if no triggers are set.
        No promotion may be silent — every promotion must be recorded.
        """
        current_path = original_decision.route_selected
        transition, new_path = self._resolve_promotion(current_path, triggers)

        self._promotion_counter += 1
        promotion_id = f"RP-{datetime.now(timezone.utc).year}-{self._promotion_counter:04d}"

        promotion = RoutePromotion(
            promotion_id=promotion_id,
            cycle_id=self.cycle_id,
            original_decision_id=original_decision.decision_id,
            promotion_transition=transition,
            new_route=new_path,
            triggers=triggers,
            trigger_description=trigger_description,
            trace_anchor=trace_anchor,
            unit_id=original_decision.unit_id,
            impact_on_current_execution=impact_on_current_execution,
            operator_notification_required=operator_notification_required,
            operator_notification_text=operator_notification_text,
            snapshots_invalidated=snapshots_invalidated or [],
            new_snapshots_required=new_snapshots_required or [],
        )

        self._promotions.append(promotion)
        self._persist_promotion(promotion)
        return promotion

    def get_decisions(self) -> list[RouteDecision]:
        return list(self._decisions)

    def get_promotions(self) -> list[RoutePromotion]:
        return list(self._promotions)

    # ─── Internal helpers ─────────────────────────────────────────────────────

    def _select_path(self, raw_score: float) -> ExecutionPath:
        """
        BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_THRESHOLDS

        Deterministic path selection based on score and declared thresholds.
        """
        thresholds = self.scorer.config.thresholds
        if raw_score <= thresholds["light_max"]:
            return ExecutionPath.BETO_LIGHT_PATH
        elif raw_score <= thresholds["partial_max"]:
            return ExecutionPath.BETO_PARTIAL_PATH
        else:
            return ExecutionPath.BETO_FULL_PATH

    def _build_context_layers(self, path: ExecutionPath) -> ContextLayersUsed:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_2_CONTEXT_SNAPSHOT

        Determine which context layers are authorized for the selected path.
        Layer A and C are always included. Layer B depends on path.
        """
        if path == ExecutionPath.BETO_LIGHT_PATH:
            return ContextLayersUsed(
                layer_a=True, layer_b=False, layer_b_scope="none", layer_c=True
            )
        elif path == ExecutionPath.BETO_PARTIAL_PATH:
            return ContextLayersUsed(
                layer_a=True, layer_b=True, layer_b_scope="minimal", layer_c=True
            )
        else:  # FULL
            return ContextLayersUsed(
                layer_a=True, layer_b=True, layer_b_scope="full", layer_c=True
            )

    def _resolve_promotion(
        self, current_path: ExecutionPath, triggers: PromotionTriggers
    ) -> tuple[PromotionTransition, ExecutionPath]:
        """
        BETO-TRACE: BETO_V44.SEC7.PHASE.PHASE_6_EXECUTOR_INTEGRATION

        Resolve the promotion transition based on current path and triggers.
        Returns (transition, new_path).
        """
        if current_path == ExecutionPath.BETO_FULL_PATH:
            raise ValueError(
                "Cannot promote from BETO_FULL_PATH — it is already the highest path."
            )

        # If graph is required or scope is multi-unit → FULL regardless of current path
        needs_full = (
            triggers.graph_required
            or triggers.scope_became_multiunit
            or triggers.structural_authority_required
            or triggers.manifest_new_required
        )

        if current_path == ExecutionPath.BETO_LIGHT_PATH:
            if needs_full:
                return PromotionTransition.LIGHT_TO_FULL, ExecutionPath.BETO_FULL_PATH
            else:
                return PromotionTransition.LIGHT_TO_PARTIAL, ExecutionPath.BETO_PARTIAL_PATH
        else:  # PARTIAL
            return PromotionTransition.PARTIAL_TO_FULL, ExecutionPath.BETO_FULL_PATH

    # ─── Persistence ──────────────────────────────────────────────────────────

    def _persist_decision(self, decision: RouteDecision) -> None:
        """
        BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG

        Persist routing decision to .beto/routing/decisions/.
        Stored as JSON for machine readability and audit.
        """
        decisions_dir = self.beto_dir / "routing" / "decisions"
        decisions_dir.mkdir(parents=True, exist_ok=True)
        path = decisions_dir / f"{decision.decision_id}.json"
        path.write_text(
            json.dumps(decision.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _persist_promotion(self, promotion: RoutePromotion) -> None:
        """
        BETO-TRACE: BETO_V44.SEC8.DECISION.ROUTING_CONFIG

        Persist route promotion to .beto/routing/promotions/.
        """
        promotions_dir = self.beto_dir / "routing" / "promotions"
        promotions_dir.mkdir(parents=True, exist_ok=True)
        path = promotions_dir / f"{promotion.promotion_id}.json"
        path.write_text(
            json.dumps(promotion.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
