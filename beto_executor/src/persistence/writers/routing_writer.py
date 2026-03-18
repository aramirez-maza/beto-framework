"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC6.MODEL.ROUTING_WRITER

Dual-write for routing decisions and route promotions.
Called from ExecutionRouter._persist_decision() and _persist_promotion()
alongside the existing JSON writes.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from persistence.connection import get_connection


class RoutingWriter:
    """Writes routing decisions and route promotions to SQLite."""

    @staticmethod
    def write_decision(beto_dir: Path, decision) -> None:
        """
        Persist a RouteDecision to the routing_decisions table.
        decision is a RouteDecision dataclass from execution_router.path_registry.
        """
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO routing_decisions (
                        decision_id, cycle_id, route_selected, raw_score,
                        complexity_breakdown, context_layers, justification,
                        executor_assigned, trace_anchor, step_context,
                        subproblem_desc, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        decision.decision_id,
                        decision.cycle_id,
                        decision.route_selected.value,
                        decision.raw_score,
                        json.dumps(decision.complexity_breakdown, ensure_ascii=False),
                        json.dumps(
                            {
                                "layer_a": decision.context_layers.layer_a,
                                "layer_b": decision.context_layers.layer_b,
                                "layer_b_scope": decision.context_layers.layer_b_scope,
                                "layer_c": decision.context_layers.layer_c,
                            },
                            ensure_ascii=False,
                        ),
                        decision.justification,
                        decision.executor_assigned,
                        decision.trace_anchor,
                        decision.step_context,
                        decision.subproblem_description,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
        finally:
            conn.close()

    @staticmethod
    def write_promotion(beto_dir: Path, promotion) -> None:
        """
        Persist a RoutePromotion to the route_promotions table.
        promotion is a RoutePromotion dataclass from execution_router.path_registry.
        """
        conn = get_connection(beto_dir)
        try:
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO route_promotions (
                        promotion_id, cycle_id, original_decision_id,
                        promotion_transition, new_route, triggers,
                        trigger_description, operator_notification,
                        operator_notification_text, trace_anchor, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        promotion.promotion_id,
                        promotion.cycle_id,
                        promotion.original_decision_id,
                        promotion.promotion_transition.value,
                        promotion.new_route.value,
                        json.dumps(
                            {
                                "graph_required": promotion.triggers.graph_required,
                                "scope_became_multiunit": promotion.triggers.scope_became_multiunit,
                                "structural_authority_required": promotion.triggers.structural_authority_required,
                                "manifest_new_required": promotion.triggers.manifest_new_required,
                            },
                            ensure_ascii=False,
                        ),
                        promotion.trigger_description,
                        1 if promotion.operator_notification_required else 0,
                        promotion.operator_notification_text,
                        promotion.trace_anchor,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
        finally:
            conn.close()
