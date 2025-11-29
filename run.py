# run.py
"""Demo entry (*Prototype to Production* p.11-15: Gated run)."""

import argparse
import os
import json
from dotenv import load_dotenv

# Load env vars
load_dotenv(".env")

from reality_remix_agent.main import build_graph
from reality_remix_agent.eval import agent_as_judge


def trace_step(name: str, payload: dict) -> None:
    """Simple tracing helper used during development to log steps."""
    try:
        print(f"[TRACE] {name}: {payload}")
    except Exception:
        pass  # tracing should never interrupt execution


def main(prompt: str, user_id: str, style: str = "whimsical"):
    # Require Gemini API key
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("Set GEMINI_API_KEY in your .env file")

    # Build LangGraph workflow
    graph = build_graph()

    # Initial state passed to graph
    initial = {"prompt": prompt, "user_id": user_id, "style": style}
    trace_step("Start", initial)

    # Execute graph
    result = graph.invoke(initial)
    trace_step("End", result)

    # Judge / critique output
    critique = agent_as_judge(result)
    critique_text = critique.get("critique", str(critique))

    branches = result.get("branches", [])
    print(f"Remixed Branches:\n{branches}\nCritique: {critique_text}")

    # Save result JSON
    with open(f"{user_id}_remix.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
            # Save plain text output (Notepad friendly)
    text_output = "=== Remixed Branches ===\n\n"
    for i, b in enumerate(branches, start=1):
        text_output += f"Branch {i}:\n{b}\n\n"

    text_output += "=== Critique ===\n"
    text_output += critique_text

    with open(f"{user_id}_remix.txt", "w", encoding="utf-8") as f:
        f.write(text_output)


    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--user_id", required=True)
    parser.add_argument("--style", default="whimsical")

    args = parser.parse_args()
    main(args.prompt, args.user_id, args.style)
