"""Gated Rewrite Agent: one Gemini call masks the document, then a check
decides whether the returned text is accepted. Run with `python -m agent`.
"""
from pathlib import Path

SUBMISSION = Path(__file__).resolve().parent.parent
