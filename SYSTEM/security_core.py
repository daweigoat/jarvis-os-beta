from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class SecurityCore(Plugin):
    def __init__(self):
        super().__init__("SecurityCore")
        self.pending_actions = {}
        self.waiting_for_confirmation = False
        
    def start(self):
        print("[SECURITY] Security Core initialized.")
        bus.subscribe("voice_command", self.on_voice_command)
        bus.subscribe("request_permission", self.on_request_permission)
        bus.subscribe("detect_sensitive_action", self.on_detect_sensitive_action)

    def on_detect_sensitive_action(self, action_data):
        action_name = action_data.get("name", "Tindakan Sensitif")
        callback = action_data.get("callback")
        
        bus.publish("show_notification", f"Tindakan Sensitif Terdeteksi: {action_name}")
        bus.publish("jarvis_state", "Processing")
        
        # Route to request_permission
        self.on_request_permission({
            "action_name": action_name,
            "callback": callback
        })

    def on_request_permission(self, data):
        self.pending_actions["current"] = data
        self.waiting_for_confirmation = True
        
        bus.publish("tts_speak", f"Membutuhkan izin keamanan. Apakah anda yakin ingin {data.get('action_name')}?")
        
    def on_voice_command(self, command: str):
        if self.waiting_for_confirmation and "current" in self.pending_actions:
            cmd = command.lower()
            if any(word in cmd for word in ["ya", "yakin", "tentu", "lanjut", "setuju"]):
                bus.publish("tts_speak", "Izin diberikan. Melaksanakan.")
                callback = self.pending_actions["current"].get("callback")
                if callback:
                    callback()
            else:
                bus.publish("tts_speak", "Tindakan dibatalkan demi keamanan.")
                
            self.pending_actions.pop("current", None)
            self.waiting_for_confirmation = False
