import requests
import threading
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class WeatherPlugin(Plugin):
    def __init__(self):
        super().__init__("WeatherPlugin")
        self.weather_info = "Tidak tersedia"
        
    def start(self):
        bus.subscribe("voice_command", self.on_voice_command)
        self._fetch_weather()

    def _fetch_weather(self):
        def fetch():
            try:
                url = "https://api.open-meteo.com/v1/forecast?latitude=-6.2146&longitude=106.8451&current=temperature_2m,weather_code&timezone=Asia%2FJakarta"
                res = requests.get(url, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    temp = data["current"]["temperature_2m"]
                    self.weather_info = f"{temp} derajat celcius"
                    bus.publish("weather_update", self.weather_info)
            except Exception as e:
                print(f"[WEATHER] Fetch Error: {e}")
        threading.Thread(target=fetch, daemon=True).start()

    def on_voice_command(self, command: str):
        if "cuaca" in command:
            bus.publish("tts_speak", f"Cuaca saat ini di Jakarta adalah {self.weather_info}.")
