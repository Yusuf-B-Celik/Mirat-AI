"""MİRAT test paketi: testler hiçbir zaman canlı LLM API'sine istek atmaz."""
import os

os.environ["MIRAT_OFFLINE"] = "1"
