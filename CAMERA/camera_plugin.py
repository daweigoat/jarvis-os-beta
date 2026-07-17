import cv2
import threading
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class CameraPlugin(Plugin):
    def __init__(self):
        super().__init__("CameraPlugin")
        self.cap = None
        self.capture_thread = None

    def start(self):
        print("[CAMERA] Initializing Camera...")
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not self.cap.isOpened():
            print("[CAMERA] Error: Could not open webcam.")
            bus.publish("tts_speak", "Kamera gagal diaktifkan. Modul akan dimatikan.")
            raise Exception("Webcam tidak ditemukan atau error")
            
        bus.publish("tts_speak", "Kamera aktif.")
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()

    def stop(self):
        self.is_active = False
        if self.cap:
            self.cap.release()
        print("[CAMERA] Camera Stopped.")
        bus.publish("tts_speak", "Kamera dinonaktifkan.")

    def _capture_loop(self):
        while self.is_active:
            ret, frame = self.cap.read()
            if ret:
                # Flip horizontally for selfie view
                frame = cv2.flip(frame, 1)
                bus.publish("camera_frame", frame)
            else:
                print("[CAMERA] Frame capture failed.")
                break
