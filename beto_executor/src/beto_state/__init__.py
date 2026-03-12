"""
BETO_STATE — Live epistemic context layer for BETO_EXECUTOR.

Decouples project size from LLM context size by maintaining a structured,
queryable summary of the cycle's epistemic state. Updated after each paso.
context_builder.py injects BETO_STATE as first message (parallel to full
artifacts — does NOT replace them until validated).
"""
