from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin
import time

class PowerManagement(Plugin):
    def __init__(self):
        super().__init__("PowerManagement")
        self.last_activity = time.time()
        # Modes: 'normal', 'active', 'sleep'
        self.power_mode = "normal" 
        self.sleep_timeout = 300 # 5 minutes to sleep
        
    def start(self):
        bus.subscribe("user_activity", self.on_user_activity)
        bus.subscribe("voice_command", self.on_user_activity)
        bus.subscribe("gesture_detected", self.on_user_activity)
        bus.subscribe("set_power_mode", self.set_power_mode)
        print("[POWER] Power Management started in NORMAL mode.")

    def on_user_activity(self, data=None):
        self.last_activity = time.time()
        if self.power_mode == "sleep":
            self.set_power_mode("normal")

    def set_power_mode(self, mode: str):
        if mode == self.power_mode:
            return
            
        self.power_mode = mode
        print(f"[POWER] Switching to {mode.upper()} mode")
        bus.publish("power_state_changed", mode)
        
        if mode == "sleep":
            bus.publish("jarvis_state", "Sleeping")
            bus.publish("tts_speak", "Sistem memasuki mode hemat daya.")
            # Disable intensive modules
            bus.publish("disable_plugin", "CameraPlugin")
            bus.publish("disable_plugin", "FaceTrackingPlugin")
            bus.publish("disable_plugin", "HandTrackingPlugin")
            bus.publish("disable_plugin", "GesturePlugin")
            
        elif mode == "normal":
            bus.publish("jarvis_state", "Listening")
            bus.publish("tts_speak", "Sistem kembali ke mode normal.")
            # Ensure heavy vision modules are off in normal mode
            bus.publish("disable_plugin", "CameraPlugin")
            bus.publish("disable_plugin", "FaceTrackingPlugin")
            bus.publish("disable_plugin", "HandTrackingPlugin")
            bus.publish("disable_plugin", "GesturePlugin")
            
        elif mode == "active":
            bus.publish("tts_speak", "Mode aktif. Semua sensor dinyalakan.")
            # Active mode can manually enable vision plugins, but usually we let specific commands do it.

    def update(self):
        if self.power_mode != "sleep":
            if time.time() - self.last_activity > self.sleep_timeout:
                self.set_power_mode("sleep")
