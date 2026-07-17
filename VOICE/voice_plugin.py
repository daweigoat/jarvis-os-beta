import threading
import speech_recognition as sr
import sounddevice as sd
from kokoro_onnx import Kokoro
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin
import numpy as np

class VoicePlugin(Plugin):
    def __init__(self):
        super().__init__("VoicePlugin")
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.kokoro = None
        self.listen_thread = None

    def start(self):
        print("[VOICE] Initializing Voice Plugin...")
        try:
            self.kokoro = Kokoro("ASSETS/kokoro/kokoro-v1_0.onnx", "ASSETS/kokoro/voices.bin")
            print("[VOICE] Kokoro TTS Loaded.")
        except Exception as e:
            print(f"[VOICE] Kokoro TTS failed to load. Using console output instead. Error: {e}")
            self.kokoro = None

        bus.subscribe("tts_speak", self.speak)
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()

    def stop(self):
        self.is_listening = False
        print("[VOICE] Voice Plugin Stopped.")

    def _listen_loop(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("[VOICE] Listening for wake word...")
                while self.is_listening:
                    try:
                        bus.publish("jarvis_state", "Listening")
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        text = self.recognizer.recognize_google(audio, language="id-ID").lower()
                        print(f"[VOICE] Heard: {text}")
                        
                        if "halo jarvis" in text or "halo jervis" in text:
                            bus.publish("jarvis_state", "Understanding")
                            command = text.split("halo jarvis")[-1].strip()
                            if not command:
                                command = text.split("halo jervis")[-1].strip()
                            
                            if not command:
                                self.speak("Ada yang bisa saya bantu?")
                                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                                command = self.recognizer.recognize_google(audio, language="id-ID").lower()
                            
                            print(f"[VOICE] Command: {command}")
                            bus.publish("voice_command", command)
                            
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except Exception as e:
                        if self.is_listening:
                            print(f"[VOICE] Rec Error: {e}")
        except Exception as e:
            print(f"[VOICE] Microphone error: {e}")

    def speak(self, text):
        print(f"[JARVIS] {text}")
        bus.publish("jarvis_state", "Speaking")
        if self.kokoro:
            try:
                # We assume Kokoro is correctly configured for ID in the ONNX model
                samples, sample_rate = self.kokoro.create(text, voice="af_bella", speed=1.0, lang="id")
                sd.play(samples, sample_rate)
                sd.wait()
            except Exception as e:
                print(f"[VOICE] TTS Error: {e}")
        bus.publish("jarvis_state", "Completed")
