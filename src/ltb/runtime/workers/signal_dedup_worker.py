import time
from ltb.system.logger import logger


class SignalDedupWorker:

    DUP_TTL = 20.0

    def __init__(self, bus):

        self.bus = bus
        self.last_signal = {}

        self.bus.subscribe(
            "strategy.signal",
            self.on_signal
        )

    def run(self):

        logger.info("[SIGNAL DEDUP WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_signal(self, signal):

        symbol = signal["symbol"]
        now = time.time()

        last = self.last_signal.get(symbol)

        if last and now - last < self.DUP_TTL:

            logger.debug(
                "[DEDUP] filtered duplicate %s",
                symbol
            )

            return

        self.last_signal[symbol] = now

        logger.info(
            "[DEDUP] passed %s strategy=%s",
            symbol,
            signal.get("strategy")
        )

        self.bus.publish(
            "dedup.signal",
            signal
        )
