import time
from collections import defaultdict

from ltb.system.logger import logger


class PositionIntentWorker:

    FLUSH_INTERVAL = 1.0

    def __init__(self, bus):

        self.bus = bus

        self.intent_buffer = defaultdict(list)

        self.last_flush = time.time()

        self.bus.subscribe("quality.signal", self.on_signal)

    def run(self):

        logger.info("[POSITION INTENT WORKER STARTED]")

        while True:

            now = time.time()

            if now - self.last_flush >= self.FLUSH_INTERVAL:

                self.flush()

                self.last_flush = now

            time.sleep(0.2)

    def on_signal(self, signal):

        symbol = signal["symbol"]

        self.intent_buffer[symbol].append(signal)

    def flush(self):

        if not self.intent_buffer:
            return

        for symbol, signals in list(self.intent_buffer.items()):

            if not signals:
                continue

            best = self.select_best(signals)

            if best:

                logger.info(
                    "[INTENT] resolved symbol=%s strategy=%s weight=%s alpha=%.3f",
                    symbol,
                    best.get("strategy"),
                    best.get("allocation_weight"),
                    best.get("alpha_score", 0)
                )

                self.bus.publish("intent.signal", best)

        self.intent_buffer.clear()

    def select_best(self, signals):

        best = None
        best_score = -999

        for s in signals:

            weight = s.get("allocation_weight", 0)
            alpha = s.get("alpha_score", 0)

            score = alpha * weight

            if score > best_score:

                best = s
                best_score = score

        return best
