from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class PermissionSystem(Plugin):
    def __init__(self):
        super().__init__("PermissionSystem")
        self.pending_action = None
        self.pending_callback = None
        self.waiting_for_confirmation = False
        
    def start(self):
        bus.subscribe("voice_command", self.on_voice_command)
        bus.subscribe("request_permission", self.on_request_permission)

    def on_request_permission(self, data):
        """data: {'action_name': 'Deskripsi', 'callback': func}"""
        self.pending_action = data.get("action_name")
        self.pending_callback = data.get("callback")
        self.waiting_for_confirmation = True
        
        bus.publish("tts_speak", f"Apakah anda yakin ingin {self.pending_action}?")
        
    def on_voice_command(self, command: str):
        if self.waiting_for_confirmation:
            cmd = command.lower()
            if any(word in cmd for word in ["ya", "yakin", "tentu", "lanjut", "setuju"]):
                bus.publish("tts_speak", "Baik. Melaksanakan.")
                if self.pending_callback:
                    self.pending_callback()
            else:
                bus.publish("tts_speak", "Dibatalkan.")
                
            self.pending_action = None
            self.pending_callback = None
            self.waiting_for_confirmation = False
