from datetime import datetime, timezone

from database import EVENTS


class EventDispatcher:

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, handler):

        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(handler)

    def publish(self, event_name, payload):

        event = {
            "type": event_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }

        EVENTS.append(event)

        handlers = self.listeners.get(event_name, [])

        for handler in handlers:
            handler(event)