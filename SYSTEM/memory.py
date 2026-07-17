import json
import os
import threading
from typing import Any

MEMORY_FILE = "memory.json"

class MemorySystem:
    def __init__(self):
        self.data = {}
        self._lock = threading.Lock()
        self.load()

    def load(self):
        with self._lock:
            if os.path.exists(MEMORY_FILE):
                try:
                    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
                except Exception as e:
                    print(f"[MEMORY] Failed to load memory: {e}")
                    self.data = {}
            else:
                self.data = {
                    "preferences": {
                        "ai_model": "qwen",
                        "voice": "kokoro",
                        "language": "id"
                    },
                    "context": []
                }
                self.save_unlocked()

    def save_unlocked(self):
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"[MEMORY] Failed to save memory: {e}")

    def save(self):
        with self._lock:
            self.save_unlocked()

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self.data.get(key, default)

    def set(self, key: str, value: Any):
        with self._lock:
            self.data[key] = value
            self.save_unlocked()

    def add_context(self, role: str, content: str, max_history: int = 10):
        with self._lock:
            if "context" not in self.data:
                self.data["context"] = []
            self.data["context"].append({"role": role, "content": content})
            if len(self.data["context"]) > max_history:
                self.data["context"] = self.data["context"][-max_history:]
            self.save_unlocked()

    def get_context(self) -> list:
        with self._lock:
            return self.data.get("context", []).copy()

memory = MemorySystem()
