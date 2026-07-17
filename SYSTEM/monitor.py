from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin
import psutil
import time

class SystemMonitor(Plugin):
    def __init__(self):
        super().__init__("SystemMonitor")
        self.last_update = 0
        self.update_interval = 1.0 # 1 second
        self.stats = {
            "cpu": 0,
            "ram": 0
        }
        
    def start(self):
        print("[MONITOR] System Monitor started.")
        
    def update(self):
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.stats["cpu"] = psutil.cpu_percent()
            self.stats["ram"] = psutil.virtual_memory().percent
            
            # Publish stats for HUD
            bus.publish("system_stats_update", self.stats)
            self.last_update = current_time
