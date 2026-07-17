import cv2
import mediapipe as mp
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class HandTrackingPlugin(Plugin):
    def __init__(self):
        super().__init__("HandTrackingPlugin")
        self.mp_hands = mp.solutions.hands
        self.hands = None

    def start(self):
        print("[HAND] Initializing Hand Tracking...")
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        bus.subscribe("camera_frame", self.on_camera_frame)
        bus.publish("tts_speak", "Pelacakan tangan aktif.")

    def stop(self):
        self.is_active = False
        if self.hands:
            self.hands.close()
        print("[HAND] Hand Tracking Stopped.")
        bus.publish("tts_speak", "Pelacakan tangan dinonaktifkan.")

    def on_camera_frame(self, frame):
        if not self.is_active:
            return
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            bus.publish("hand_data", results.multi_hand_landmarks)
