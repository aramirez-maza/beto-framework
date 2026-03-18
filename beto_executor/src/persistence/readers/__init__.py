"""
BETO-TRACE: BETO_V45.SEC1.INTENT.SQLITE_PERSISTENCE
BETO-TRACE: BETO_V45.SEC7.PHASE.PHASE_2_STATE_READER

Read-side of BETO persistence — renders canonical state from SQLite.
"""

from .state_reader import build_state_payload

__all__ = ["build_state_payload"]
