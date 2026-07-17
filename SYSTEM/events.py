from typing import Callable, Dict, List, Any
import threading

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, callback: Callable):
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if callback not in self._subscribers[event_type]:
                self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any = None):
        with self._lock:
            subs = self._subscribers.get(event_type, []).copy()
            
        for callback in subs:
            try:
                callback(data)
            except Exception as e:
                print(f"[EventBus] Error in event '{event_type}' subscriber: {e}")

# Global event bus instance
bus = EventBus()
