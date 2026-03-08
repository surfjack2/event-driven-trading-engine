import threading
from collections import defaultdict


class QueueBus:

    def __init__(self):

        self.subscribers = defaultdict(list)
        self.lock = threading.Lock()

    def subscribe(self, topic, handler):

        with self.lock:
            self.subscribers[topic].append(handler)

    def publish(self, topic, data):

        handlers = []

        with self.lock:
            handlers = list(self.subscribers.get(topic, []))

        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                print(f"[BUS ERROR] {topic} -> {e}")
