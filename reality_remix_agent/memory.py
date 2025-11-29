# reality_remix_agent/memory.py
"""Long-term memory bank with compaction (*Context Engineering* p.27-38)."""

from typing import Dict, Any
import json
from datetime import datetime
import os


class DreamMemoryBank:
    def __init__(self, user_id: str):
        self.user_id = user_id

        # You could optionally store memories in a subfolder, e.g. "memory"
        self.filename = f"{self.user_id}_dreams.json"

        self.bank = self._load_bank()      # Persistent file-backed memory
        self.session_state: Dict[str, Any] = {}  # In-memory for current session

    def _default_bank(self) -> Dict[str, Any]:
        return {
            "profile": {
                "themes": [],
                "tone": "neutral",
            },
            "summaries": [],
        }

    def _load_bank(self) -> Dict[str, Any]:
        if not os.path.exists(self.filename):
            return self._default_bank()

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupt or unreadable file → reset to default
            return self._default_bank()

        # Ensure required keys exist
        if "profile" not in data or "summaries" not in data:
            data = self._default_bank()

        # Ensure profile has tone/themes
        data["profile"].setdefault("themes", [])
        data["profile"].setdefault("tone", "neutral")

        return data

    def _save_bank(self) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.bank, f, ensure_ascii=False, indent=2)
        except OSError:
            # In a real app you’d log this; for now we just avoid crashing
            pass

    def inject_context(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Inject declarative memory; compact to <5k tokens (conceptually)."""

        # Attach profile (themes, tone, etc.) to agent state
        state["memory"] = self.bank.get("profile", self._default_bank()["profile"])

        # Rolling summary compaction (simple version)
        summaries = self.bank.get("summaries", [])
        recent = summaries[-3:] if isinstance(summaries, list) else []

        state["context_summary"] = " | ".join(recent)
        return state

    def extract_and_store(self, narrative: str, user_feedback: str = "") -> None:
        """
        Extract procedural/declarative memory from a narrative and feedback.

        In a real system, this would call Gemini (e.g., gemini-2.5-flash)
        to summarize preferences, recurring themes, etc., then parse and store.
        """
        # Very simple stub: just stuff a truncated summary + timestamp
        summary = f"Extract key: {narrative} + feedback: {user_feedback}"
        new_sum = f"{datetime.now().isoformat(timespec='seconds')}: {summary[:100]}..."

        self.bank.setdefault("summaries", []).append(new_sum)

        # Compaction: keep only the last 5 summaries if list gets too long
        if len(self.bank["summaries"]) > 10:
            self.bank["summaries"] = self.bank["summaries"][-5:]

        self._save_bank()
