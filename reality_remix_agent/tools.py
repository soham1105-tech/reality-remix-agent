# reality_remix_agent/tools.py
"""Custom tools with MCP-style docstrings (*Agent Tools* p.10-13)."""

import os
from typing import Dict, Any, List, Optional

from serpapi import GoogleSearch  # Built-in search


def surreal_fact_injector(
    query: str,
    style: str,
    context: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Injects surreal, fact-blended elements into narratives via search.

    Args:
        query: Base prompt (e.g., 'lost keys').
        style: Tone (e.g., 'whimsical', 'dark', 'epic').
        context: Session state (e.g., {'user_dreams': ['flight themes']}).

    Returns:
        Dict with twisted facts/sources. Pause/resume via context flag.
        Example:
        {
            "surreal_facts": [...],
            "sources": [...],
            "status": "ok" | "paused" | "no_api_key" | "error"
        }
    """
    # Pause/resume via context flag
    pause = context.get("pause", False) if isinstance(context, dict) else False
    if pause:
        return {"status": "paused", "resume_key": query}

    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        # Graceful fallback if SerpAPI key is missing
        return {
            "status": "no_api_key",
            "surreal_facts": [
                f"Imagined twist for '{query}' in {style} style (no SERPAPI_KEY set)."
            ],
            "sources": [],
        }

    params = {
        "engine": "google",
        "q": f"{query} {style} facts",
        "api_key": api_key,
        "num": 3,
    }

    search = GoogleSearch(params)
    try:
        results = search.get_dict().get("organic_results", [])
    except Exception as e:
        # Never let tools crash the agent
        return {
            "status": "error",
            "error": str(e),
            "surreal_facts": [
                f"Imagined twist for '{query}' in {style} style (search error)."
            ],
            "sources": [],
        }

    twisted: List[str] = []
    sources: List[str] = []

    for r in results:
        title: str = r.get("title", "Untitled result")
        snippet: str = r.get("snippet", "")
        link: Optional[str] = r.get("link")

        twisted.append(f"Twist: {title} → {snippet} in {style} veil.")
        if link:
            sources.append(link)

    return {
        "status": "ok",
        "surreal_facts": twisted,
        "sources": sources,
    }


def branch_generator(prompt: str, num_branches: int = 2) -> Dict[str, List[str]]:
    """Generates parallel branch ideas; resume from partial."""
    # Placeholder: In prod, this could be async / queued
    branches = [
        f"Branch {i + 1}: {prompt} as {['sci-fi', 'myth'][i % 2]} twist."
        for i in range(num_branches)
    ]
    return {"branches": branches}
