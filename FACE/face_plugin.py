import cv2
import mediapipe as mp
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class FaceTrackingPlugin(Plugin):
    def __init__(self):
        super().__init__("FaceTrackingPlugin")
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = None

    def start(self):
        print("[FACE] Initializing Face Tracking...")
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        bus.subscribe("camera_frame", self.on_camera_frame)
        bus.publish("tts_speak", "Pelacakan wajah aktif.")

    def stop(self):
        self.is_active = False
        if self.face_mesh:
            self.face_mesh.close()
        print("[FACE] Face Tracking Stopped.")
        bus.publish("tts_speak", "Pelacakan wajah dinonaktifkan.")

    def on_camera_frame(self, frame):
        if not self.is_active:
            return
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        results = self.face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            bus.publish("face_data", results.multi_face_landmarks[0])
