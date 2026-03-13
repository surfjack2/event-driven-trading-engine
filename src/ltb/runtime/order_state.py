from threading import Lock


class OrderStateManager:

    def __init__(self):

        self.pending = set()
        self.lock = Lock()

    def is_pending(self, symbol):

        with self.lock:
            return symbol in self.pending

    def set_pending(self, symbol):

        with self.lock:
            self.pending.add(symbol)

    def clear(self, symbol):

        with self.lock:
            self.pending.discard(symbol)
