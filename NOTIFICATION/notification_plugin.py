from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin
import time

class NotificationPlugin(Plugin):
    def __init__(self):
        super().__init__("NotificationPlugin")
        self.active_notifications = []
        
    def start(self):
        bus.subscribe("show_notification", self.on_new_notification)
        
    def on_new_notification(self, message: str):
        self.active_notifications.append({
            "message": message,
            "time": time.time()
        })
        print(f"[NOTIFICATION] {message}")
        
    def update(self):
        current = time.time()
        # Keep notifications for 5 seconds
        self.active_notifications = [n for n in self.active_notifications if current - n["time"] < 5.0]
