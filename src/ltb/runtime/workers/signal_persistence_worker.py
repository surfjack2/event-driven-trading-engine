import time
from collections import defaultdict, deque
from ltb.system.logger import logger


class SignalPersistenceWorker:

    PERSIST_TICKS = 1
    WINDOW = 15

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
        strategy = signal.get("strategy")

        key = (symbol, strategy)

        buffer = self.buffers[key]

        buffer.append(signal)

        if len(buffer) < self.PERSIST_TICKS:
            return

        logger.info(
            "[PERSISTENCE] confirmed %s strategy=%s ticks=%s",
            symbol,
            strategy,
            len(buffer)
        )

        self.bus.publish(
            "persistent.signal",
            signal
        )

        buffer.clear()
