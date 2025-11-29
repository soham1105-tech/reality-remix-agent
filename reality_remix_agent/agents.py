# reality_remix_agent/agents.py
"""Multi-agent nodes: Sequential + parallel loops (*Intro to Agents* p.30-35)."""

import os
from typing import Dict

from dotenv import load_dotenv
import google.generativeai as genai

from .tools import surreal_fact_injector, branch_generator
from .memory import DreamMemoryBank

# Load environment variables (for local dev)
load_dotenv(dotenv_path=".env")

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 2.5-flash everywhere
model = genai.GenerativeModel("gemini-2.5-flash")


def ideator_node(state: Dict) -> Dict:
    """Initial think: create a core surreal short story."""

    # Per-user memory instance (not global)
    memory = DreamMemoryBank(user_id=state["user_id"])

    # Inject memory context into state
    state = memory.inject_context(state)

    # Get surreal facts (for flavor only)
    facts = surreal_fact_injector(state["prompt"], state["style"], state)
    surreal_facts_text = "\n".join(facts.get("surreal_facts", []))

    prompt_text = f"""
You are a skilled fiction writer.

Write a surreal short story based on this prompt:

"{state['prompt']}"

Use the following strange facts as inspiration (you can twist or reinterpret them):
{surreal_facts_text}

Match this tone: {state['memory'].get('tone', 'neutral')}
Match this style: {state.get('style', 'whimsical')}

Requirements:
- 4–7 paragraphs.
- Narrative, story-like prose (clear beginning, middle, and end).
- Use normal paragraphs with line breaks, NOT bullet points or lists.
- No headings like "Chapter 1" unless really needed.
"""

    response = model.generate_content(prompt_text)

    # This is your main “core story”
    state["core_idea"] = response.text
    return state


def brancher_node(state: Dict) -> Dict:
    """Generate alternate story versions (branches) in full story format."""
    # Conceptual branch ideas (sci-fi twist, myth twist, etc.)
    branches_raw = branch_generator(state["core_idea"], 2)

    refined = []
    for b in branches_raw["branches"]:
        twist_prompt = f"""
You are rewriting a surreal short story.

Original story (for reference):
{state['core_idea']}

Now write an ALTERNATE VERSION of this story with the following twist:
"{b}"

Requirements:
- It should be a complete standalone story (do not just list options).
- 4–7 paragraphs.
- Narrative, story-like prose with line breaks between paragraphs.
- No lists, no bullet points, no "Branch" labels in the text.
"""
        resp = model.generate_content(twist_prompt)
        refined.append(resp.text)

    # The list of full story variants
    state["branches"] = refined
    return state


def evaluator_node(state: Dict) -> Dict:
    """Refine branches if emotional resonance seems low (very rough heuristic)."""
    for i, branch in enumerate(state["branches"]):
        score_prompt = f"""
Score the following story on emotional resonance from 1 to 5.

Story:
{branch}

First line MUST be exactly: "Score: <number between 1 and 5>"
Then give 2–3 sentences of explanation.
"""
        score_text = model.generate_content(score_prompt).text.lower()

        # Very naive check: if model says score <3, refine
        if "score: 1" in score_text or "score: 2" in score_text:
            refine_prompt = f"""
This story was judged as low emotional resonance.

Please rewrite it to be more emotionally engaging, but keep the surreal style.

Story:
{branch}

Requirements:
- 4–7 paragraphs.
- Narrative, story-like prose.
- No lists or bullet points.
"""
            refined = model.generate_content(refine_prompt)
            state["branches"][i] = refined.text

    return state
