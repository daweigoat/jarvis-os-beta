import requests
import threading
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin
from SYSTEM.memory import memory

class AIPlugin(Plugin):
    def __init__(self):
        super().__init__("AIPlugin")
        self.ollama_url = "http://localhost:11434/api/chat"
        self.system_prompt = (
            "Kamu adalah JARVIS, asisten AI canggih. "
            "Jawab dengan singkat, profesional, dan dalam bahasa Indonesia."
        )

    def start(self):
        bus.subscribe("voice_command", self.on_voice_command)
        print("[AI] AI Plugin started.")

    def on_voice_command(self, command: str):
        system_commands = ["status sistem", "laporan sistem", "matikan komputer", "cuaca", "mode kamera", "aktifkan mode kamera", "matikan mode kamera"]
        if any(cmd in command for cmd in system_commands):
            return
            
        bus.publish("jarvis_state", "Processing")
        threading.Thread(target=self._ask_ollama, args=(command,), daemon=True).start()

    def _ask_ollama(self, prompt: str):
        bus.publish("jarvis_state", "Thinking")
        model = memory.get("preferences").get("ai_model", "qwen")
        
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(memory.get_context())
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        try:
            bus.publish("jarvis_state", "Generating Response")
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                answer = response.json().get("message", {}).get("content", "")
                
                memory.add_context("user", prompt)
                memory.add_context("assistant", answer)
                
                bus.publish("tts_speak", answer)
            else:
                print(f"[AI] API Error: {response.text}")
                bus.publish("tts_speak", "Maaf, terjadi kesalahan pada server AI lokal.")
        except Exception as e:
            print(f"[AI] Exception: {e}")
            bus.publish("tts_speak", "Maaf, koneksi ke Ollama gagal. Pastikan Ollama berjalan.")
        finally:
            bus.publish("ai_thinking", False)
