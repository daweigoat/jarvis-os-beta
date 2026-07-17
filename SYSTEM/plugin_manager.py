import threading
import time
import logging
from typing import Dict, Any
from SYSTEM.events import bus

logging.basicConfig(
    filename='jarvis.log', 
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class Plugin:
    def __init__(self, name: str):
        self.name = name
        self.is_active = False
        self.status = "INITIALIZING"

    def start(self):
        pass

    def stop(self):
        pass

    def update(self):
        pass
        
    def set_status(self, status: str):
        if self.status != status:
            self.status = status
            bus.publish("plugin_status_change", {"name": self.name, "status": self.status})

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self._lock = threading.Lock()
        
        bus.subscribe("enable_plugin", self._on_enable)
        bus.subscribe("disable_plugin", self._on_disable)

    def register(self, plugin: Plugin):
        with self._lock:
            plugin.set_status("DISABLED")
            self.plugins[plugin.name] = plugin
            msg = f"Plugin Registered: {plugin.name}"
            print(f"[SYSTEM] {msg}")
            logging.info(msg)
            bus.publish("plugin_status_change", {"name": plugin.name, "status": plugin.status})

    def _on_enable(self, name: str):
        self.start_plugin(name)
        
    def _on_disable(self, name: str):
        self.stop_plugin(name)

    def start_plugin(self, name: str):
        with self._lock:
            plugin = self.plugins.get(name)
            if plugin and not plugin.is_active:
                plugin.set_status("INITIALIZING")
                plugin.is_active = True
                try:
                    plugin.start()
                    plugin.set_status("ACTIVE")
                    msg = f"Plugin Started: {name}"
                    print(f"[SYSTEM] {msg}")
                    logging.info(msg)
                except Exception as e:
                    msg = f"Failed to start plugin {name}: {e}"
                    print(f"[SYSTEM] {msg}")
                    logging.error(msg)
                    plugin.is_active = False
                    plugin.set_status("FAILED")

    def stop_plugin(self, name: str):
        with self._lock:
            plugin = self.plugins.get(name)
            if plugin and plugin.is_active:
                try:
                    plugin.stop()
                    msg = f"Plugin Stopped: {name}"
                    print(f"[SYSTEM] {msg}")
                    logging.info(msg)
                except Exception as e:
                    msg = f"Error stopping plugin {name}: {e}"
                    print(f"[SYSTEM] {msg}")
                    logging.error(msg)
                finally:
                    plugin.is_active = False
                    plugin.set_status("DISABLED")

    def get_plugin(self, name: str) -> Plugin:
        with self._lock:
            return self.plugins.get(name)

    def update_all(self):
        with self._lock:
            active_plugins = [p for p in self.plugins.values() if p.is_active and p.status != "FAILED"]
            
        for plugin in active_plugins:
            try:
                plugin.update()
            except Exception as e:
                msg = f"Error updating plugin {plugin.name}: {e}"
                print(f"[SYSTEM] {msg}")
                logging.error(msg)
                plugin.is_active = False
                plugin.set_status("FAILED")
                bus.publish("show_notification", f"{plugin.name} failed and was disabled.")

    def stop_all(self):
        with self._lock:
            active_names = [name for name, p in self.plugins.items() if p.is_active]
            
        for name in active_names:
            self.stop_plugin(name)
