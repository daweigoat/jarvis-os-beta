import time
from SYSTEM.events import bus
from SYSTEM.plugin_manager import Plugin

class GesturePlugin(Plugin):
    def __init__(self):
        super().__init__("GesturePlugin")
        self.last_gesture_time = 0
        self.gesture_cooldown = 2.0 
        
    def start(self):
        print("[GESTURE] Initializing Gesture Detection...")
        bus.subscribe("hand_data", self.on_hand_data)
        bus.publish("tts_speak", "Sistem gestur aktif.")

    def stop(self):
        self.is_active = False
        print("[GESTURE] Gesture Detection Stopped.")
        bus.publish("tts_speak", "Sistem gestur dinonaktifkan.")

    def on_hand_data(self, hand_landmarks_list):
        if not self.is_active:
            return
            
        if time.time() - self.last_gesture_time < self.gesture_cooldown:
            return

        hand = hand_landmarks_list[0]
        fingers = self._get_finger_states(hand)
        gesture = self._recognize_gesture(fingers, len(hand_landmarks_list))
        
        if gesture:
            print(f"[GESTURE] Detected: {gesture}")
            self.last_gesture_time = time.time()
            bus.publish("gesture_detected", gesture)
            self._handle_gesture_action(gesture)

    def _get_finger_states(self, hand):
        up = []
        if hand.landmark[4].x < hand.landmark[3].x:
            up.append(1) 
        else:
            up.append(0)
            
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]
        for t, p in zip(tips, pips):
            if hand.landmark[t].y < hand.landmark[p].y:
                up.append(1)
            else:
                up.append(0)
        return up

    def _recognize_gesture(self, fingers, num_hands):
        if num_hands == 2:
            return "TWO HANDS"
            
        if fingers == [0, 1, 1, 0, 0]:
            return "PEACE SIGN"
        elif sum(fingers[1:]) == 4:
            return "OPEN PALM"
        elif fingers == [1, 0, 0, 0, 0]:
            return "THUMBS UP"
        elif fingers == [0, 0, 0, 0, 0]:
            return "FIST"
            
        return None

    def _handle_gesture_action(self, gesture):
        if gesture == "OPEN PALM":
            bus.publish("tts_speak", "Mode Pemindaian Diaktifkan.")
        elif gesture == "PEACE SIGN":
            bus.publish("tts_speak", "Mengambil tangkapan layar.")
        elif gesture == "THUMBS UP":
            bus.publish("tts_speak", "Tindakan diterima.")
        elif gesture == "TWO HANDS":
            bus.publish("tts_speak", "Membuka Menu Sistem.")
