import sys
import time
from SYSTEM.plugin_manager import PluginManager
from SYSTEM.security_core import SecurityCore
from SYSTEM.power import PowerManagement
from SYSTEM.monitor import SystemMonitor
from SYSTEM.command_center import CommandCenter
from VOICE.voice_plugin import VoicePlugin
from AI.ai_plugin import AIPlugin
from WEATHER.weather_plugin import WeatherPlugin
from NOTIFICATION.notification_plugin import NotificationPlugin
from CAMERA.camera_plugin import CameraPlugin
from FACE.face_plugin import FaceTrackingPlugin
from HAND.hand_plugin import HandTrackingPlugin
from GESTURE.gesture_plugin import GesturePlugin
from UTILS.automation_plugin import AutomationPlugin
from RENDERER.hud_plugin import HUDPlugin
from SYSTEM.events import bus

def main():
    print("[JARVIS] Initializing JARVIS OS 4.0...")
    
    manager = PluginManager()
    
    # Register Core Plugins
    manager.register(SecurityCore())
    manager.register(PowerManagement())
    manager.register(SystemMonitor())
    manager.register(CommandCenter())
    manager.register(NotificationPlugin())
    manager.register(WeatherPlugin())
    manager.register(AIPlugin())
    manager.register(VoicePlugin())
    manager.register(AutomationPlugin())
    manager.register(CameraPlugin())
    manager.register(FaceTrackingPlugin())
    manager.register(HandTrackingPlugin())
    manager.register(GesturePlugin())
    manager.register(HUDPlugin())
    
    # We can handle lazy loading requests via EventBus
    def on_enable_plugin(name):
        manager.start_plugin(name)
        
    def on_disable_plugin(name):
        manager.stop_plugin(name)
        
    bus.subscribe("enable_plugin", on_enable_plugin)
    bus.subscribe("disable_plugin", on_disable_plugin)
    
    # Start Phase 1 Core Plugins
    manager.start_plugin("SecurityCore")
    manager.start_plugin("PowerManagement")
    manager.start_plugin("SystemMonitor")
    manager.start_plugin("CommandCenter")
    manager.start_plugin("NotificationPlugin")
    manager.start_plugin("WeatherPlugin")
    manager.start_plugin("AIPlugin")
    manager.start_plugin("AutomationPlugin")
    manager.start_plugin("VoicePlugin")
    manager.start_plugin("HUDPlugin")

    print("[JARVIS] System fully operational. Listening for 'HALO JARVIS'...")
    bus.publish("tts_speak", "Halo Ray. Sistem berhasil diinisialisasi. JARVIS OS siap digunakan.")
    
    try:
        while True:
            manager.update_all()
            time.sleep(0.016) # ~60 FPS logic loop
    except KeyboardInterrupt:
        print("[JARVIS] Shutting down...")
        bus.publish("tts_speak", "Mematikan sistem.")
        manager.stop_all()
        sys.exit(0)

if __name__ == "__main__":
    main()
