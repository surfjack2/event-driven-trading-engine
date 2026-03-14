import time
from collections import defaultdict, deque
from ltb.system.logger import logger


class SignalPersistenceWorker:

    PERSIST_TICKS = 2
    WINDOW = 10

    def __init__(self, bus):

        self.bus = bus

        self.buffers = defaultdict(
            lambda: deque(maxlen=self.WINDOW)
        )

        self.bus.subscribe(
            "dedup.signal",
            self.on_signal
        )

    def run(self):

        logger.info("[SIGNAL PERSISTENCE WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_signal(self, signal):

        symbol = signal["symbol"]

        buffer = self.buffers[symbol]

        buffer.append(signal)

        if len(buffer) < self.PERSIST_TICKS:
            return

        valid = True

        base_price = buffer[0]["price"]

        for s in buffer:

            if s["price"] < base_price:
                valid = False
                break

        if not valid:
            return

        logger.info(
            "[PERSISTENCE] confirmed %s ticks=%s",
            symbol,
            len(buffer)
        )

        self.bus.publish(
            "persistent.signal",
            signal
        )

        buffer.clear()
