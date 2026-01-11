# Reality Remix Agent

**Modular AI storytelling that flips your reality into wild narratives — powered by Gemini 2.5-Flash & LangGraph.**

This isn’t your typical prompt-response bot. Think of it as your creative warp engine: you feed it a seed idea and it builds *branching, surreal story worlds*, complete with memory, tools, and eval loops to keep it smart and weird.

---

## 🚀 What It *Actually* Does

Reality Remix Agent takes your prompts and churns out **multi-paragraph, multi-branch stories** with:

* **Memory layers** — stays consistent and remembers user vibes.
* **Custom tools** — built-in SerpAPI search + surreal injectors.
* **Eval loops** — LLM judges its own outputs and improves them.
* **Branching narratives** — multiple story forks to pick your own adventure.

It’s like storytelling with training wheels taken off.

---

## ⚙️ Features

* **Multi-agent orchestration** — ideation → branching → parallel loops.
* **Long-term session memory** — keeps context across prompts/visits.
* **Custom tools integrated** — search, injectors, dynamic helpers.
* **Observability / evaluation** — traceable performance & resonance scores.
* **Deployment-ready** — Dockerfile included, CI/CD starter stubs.

---

## 📦 Quick Setup

1. Clone the repo

   ```bash
   git clone https://github.com/soham1105-tech/reality-remix-agent.git
   cd reality-remix-agent
   ```
2. Install deps

   ```bash
   pip install -r requirements.txt
   ```
3. Set your **Gemini API key**

   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```
4. Run the agent

   ```bash
   python run.py --prompt "Tell a weird bedtime story" --user_id dreamer1
   ```

---

## 🧪 Example Output

🗣 Prompt: `"Rainy commute blues."`
✨ Output:

* **Branch 1:** Cyberpunk dash through neon floods (chooses: Hack the storm?)
* **Branch 2:** Victorian intrigue in puddles (chooses: Ally with the fog?)

> *Eval Score: 4.5/5 “Evocative.”*

---

## 💡 How It Works (Under the Hood)

1. **Prompt intake**: user prompt enters the system.
2. **Agent orchestration**: sequential ideation followed by parallel branching.
3. **Tool integration**: runs search + surreal injection tools as needed.
4. **Evaluation loop**: LLM self-evaluates to keep stories on point.
5. **Output**: staged, branching narrative delivered back to you.

---

## 🛠️ Tools & Integrations

* **SerpAPI** for real-time grounded search.
* **Long-term memory** engines for consistent character/world retention.
* Modular tool architecture for easy expansion.

---

## 🐳 Deployment

Go big or go home. Use the included **Dockerfile** to containerize your agent, plug into CI/CD pipelines, or host it as a microservice with REST/webhook endpoints.

---

## 📌 Notes

* Currently Python-only.
* Designed for storytelling & creative remixing.
* Awesome for bots, games, narrative apps, IRL interactive experiences.

---

## 🤝 Contributing

Want to add tools, improve branching logic, or make the stories even wilder? Pull requests are welcome — let’s remix reality together.

---

## 📜 License

MIT Licensed — do whatever, just give love back.

---
