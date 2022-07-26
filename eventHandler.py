from dataclasses import dataclass
from weakref import WeakKeyDictionary

@dataclass
class Event:
    name : str

@dataclass
class RowClosedEvent(Event):
    color : str = ""
    name : str = "Row closed"


class EventHandler:

    def __init__(self):
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        """Register a listener for the event queue"""
        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        """Unregister a listener"""
        if listener in self.listeners:
            del self.listeners[listener]

    def post(self, event):
        """Post a new event to the message queue"""

        for listener in self.listeners:
            listener.notify(event)