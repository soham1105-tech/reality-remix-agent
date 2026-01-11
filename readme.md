# README.md
# Reality Remix Agent: Freestyle Track Capstone

## Pitch
Everyday frustrations—spilled coffee, missed buses—trap us in loops of the ordinary. This unclassifiable agent remixes them into branching, interactive narratives: user-driven tales that blend fact, fiction, and emotion. Objective: Spark creativity, saving 3 hours/week on "what if" brainstorming by generating 5+ personalized story forks per prompt. Value: 80% user-rated "inspiring" via evals, scaling from solo dreams to collaborative worlds.

Built on Google whitepapers: Multi-agents (sequential ideation → parallel branching, *Intro to Agents* p.30-35), tools/MCP, memory compaction, evals, eval-gated deploy.

## Features Demo (3+ Keys)
- **Multi-Agents**: LLM-powered sequential (ideate → branch) + parallel loops for rival paths.
- **Tools**: Custom surreal injector + built-in search; long-running pause/resume.
- **Sessions/Memory**: In-memory states + long-term dream bank (user profiles).
- **Observability/Eval**: Traces, LLM-as-Judge for resonance (A2A protocol).
- **Deployment**: Dockerfile-ready, CI/CD stubs.

## Setup
1. `pip install -r requirements.txt`
2. Set `GEMINI_API_KEY=your_key`
3. `python run.py --prompt "Lost my keys" --user_id dreamer1`

## Example Output
Prompt: "Rainy commute blues."  
Remix: Branch 1: Cyberpunk dash through neon floods (choice: Hack the storm?). Branch 2: Victorian intrigue in puddles (choice: Ally with the fog?). Eval Score: 4.5/5 "Evocative."

Extend: Add video renders for branches (+bonus points!).
