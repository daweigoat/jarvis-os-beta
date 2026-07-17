import os
import subprocess
import threading
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class AutomationPlugin(Plugin):
    def __init__(self):
        super().__init__("AutomationPlugin")
        self.app_paths = {
            "chrome": "start chrome",
            "edge": "start msedge",
            "youtube": "start chrome https://www.youtube.com",
            "spotify": "start spotify",
            "discord": "start discord", 
            "visual studio code": "code",
            "steam": "start steam",
            "obs": "start obs64", 
            "windows explorer": "explorer"
        }
        
    def start(self):
        print("[AUTOMATION] Automation Plugin started.")
        bus.subscribe("voice_command", self.on_voice_command)

    def on_voice_command(self, command: str):
        cmd = command.lower()
        
        # 1. Open Applications
        if "buka" in cmd or "open" in cmd:
            for app, path in self.app_paths.items():
                if app in cmd:
                    bus.publish("jarvis_state", "Processing")
                    bus.publish("tts_speak", f"Membuka {app}.")
                    self._run_command(path)
                    # We assume it completes quickly enough, return state to listening
                    bus.publish("jarvis_state", "Listening")
                    return
                    
        # 2. Sensitive Actions (Shutdown)
        if "matikan komputer" in cmd or "shutdown windows" in cmd or "matikan windows" in cmd:
            bus.publish("detect_sensitive_action", {
                "name": "Mematikan Windows",
                "callback": self._shutdown_windows
            })

    def _run_command(self, path: str):
        def task():
            try:
                subprocess.run(path, shell=True, check=True)
            except Exception as e:
                print(f"[AUTOMATION] Error running {path}: {e}")
                bus.publish("tts_speak", "Maaf, aplikasi gagal dibuka. Pastikan sudah terinstal.")
        threading.Thread(target=task, daemon=True).start()

    def _shutdown_windows(self):
        bus.publish("tts_speak", "Windows akan dimatikan dalam 10 detik.")
        print("[AUTOMATION] Executing: shutdown /s /t 10")
        try:
            subprocess.run("shutdown /s /t 10", shell=True)
        except Exception as e:
            print(f"[AUTOMATION] Error shutting down: {e}")
