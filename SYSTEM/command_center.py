from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin
from SYSTEM.memory import memory

class CommandCenter(Plugin):
    def __init__(self):
        super().__init__("CommandCenter")
        self.latest_stats = {"cpu": 0, "ram": 0}
        self.latest_weather = "Tidak tersedia"
        
    def start(self):
        bus.subscribe("voice_command", self.on_voice_command)
        bus.subscribe("system_stats_update", self.on_stats_update)
        bus.subscribe("weather_update", self.on_weather_update)
        
    def on_stats_update(self, stats):
        self.latest_stats = stats
        
    def on_weather_update(self, weather_info):
        self.latest_weather = weather_info

    def on_voice_command(self, command: str):
        cmd = command.lower()
        if "status sistem" in cmd or "laporan sistem" in cmd:
            report = (f"Sistem beroperasi normal. "
                      f"Penggunaan CPU {self.latest_stats['cpu']} persen, "
                      f"dan RAM {self.latest_stats['ram']} persen. "
                      f"Cuaca saat ini: {self.latest_weather}. "
                      f"Model AI yang aktif adalah {memory.get('preferences').get('ai_model')}.")
            bus.publish("tts_speak", report)
        elif "aktifkan mode kamera" in cmd:
            bus.publish("set_power_mode", "active")
            bus.publish("enable_plugin", "CameraPlugin")
            bus.publish("enable_plugin", "FaceTrackingPlugin")
            bus.publish("enable_plugin", "HandTrackingPlugin")
            bus.publish("enable_plugin", "GesturePlugin")
        elif "matikan mode kamera" in cmd:
            bus.publish("set_power_mode", "normal")
            # The power management also disables these in normal mode, but doing it here guarantees it.
            bus.publish("disable_plugin", "CameraPlugin")
            bus.publish("disable_plugin", "FaceTrackingPlugin")
            bus.publish("disable_plugin", "HandTrackingPlugin")
            bus.publish("disable_plugin", "GesturePlugin")
