# reality_remix_agent/eval.py
"""Observability & evals (*Agent Quality* p.18-25; A2A protocol)."""

import logging
import os
from typing import Dict, Any, List

from dotenv import load_dotenv
import google.generativeai as genai


# Load env so GEMINI_API_KEY is available here too (for direct use / tests)
load_dotenv(".env")

# Configure Gemini once for this module
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 2.5-flash for evals as well
_eval_model = genai.GenerativeModel("gemini-2.5-flash")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def trace_step(step: str, state: Dict[str, Any]) -> None:
    """Log trajectories (lightweight, non-breaking)."""
    try:
        logger.info("Trace: %s | State keys: %s", step, list(state.keys()))
    except Exception:
        # Never let tracing crash the run
        pass


def llm_as_judge(output: str, criteria: str = "resonance, originality") -> float:
    """LLM Judge: Score output on given criteria from 1–5."""
    prompt = (
        f"Judge the following content on {criteria}.\n"
        f"Return the first line strictly as 'Score: <number between 1 and 5>'.\n"
        f"Then give a short explanation.\n\n"
        f"Content:\n{output}"
    )

    try:
        resp = _eval_model.generate_content(prompt)
        text = resp.text or ""
    except Exception as e:
        logger.warning("Judge model error: %s", e)
        trace_step("EvalError", {"error": str(e)})
        return 3.0  # neutral fallback

    score_value = 3.0  # default

    # Try to parse "Score: 4.2" from the first line
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if "score" in first_line.lower():
        try:
            # Extract the part after "Score:"
            num_part = first_line.split(":", 1)[-1].strip()
            # Take first token that looks like a number
            token = num_part.split()[0]
            score_value = float(token)
        except Exception:
            pass

    # Clamp score between 1 and 5 just in case
    score_value = max(1.0, min(5.0, score_value))

    trace_step("Eval", {"score": score_value, "snippet": output[:80]})
    return score_value


def agent_as_judge(state: Dict[str, Any]) -> Dict[str, Any]:
    """A2A: Critic agent reviews full flow and returns critique + overall score."""

    # Critic prompt over the full trajectory/state
    critic_prompt = (
        "You are a critic agent reviewing an AI agent's trajectory.\n"
        "Assess the path for efficiency, coherence, and errors.\n"
        "Suggest concrete fixes and improvements.\n\n"
        f"Trajectory state:\n{state}"
    )

    try:
        critic_resp = _eval_model.generate_content(critic_prompt)
        critique_text = critic_resp.text or ""
    except Exception as e:
        logger.warning("Critic model error: %s", e)
        critique_text = f"Critic model error: {e}"

    # Overall coherence score based on combined branches (if present)
    branches: List[str] = state.get("branches", [])
    combined_output = "\n\n".join(branches) if isinstance(branches, list) else str(branches)

    overall_score = llm_as_judge(combined_output, criteria="coherence, resonance")

    return {
        "critique": critique_text,
        "overall": overall_score,
    }
