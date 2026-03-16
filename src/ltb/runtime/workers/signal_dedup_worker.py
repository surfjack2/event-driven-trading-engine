import time
from ltb.system.logger import logger


class SignalDedupWorker:

    DUP_TTL = 20.0

    def __init__(self, bus):

        self.bus = bus

        # (symbol, strategy) → (timestamp, alpha_score)
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
        strategy = signal.get("strategy")

        key = (symbol, strategy)

        now = time.time()

        alpha = signal.get("alpha_score")

        if alpha is None:
            alpha = 0

        last = self.last_signal.get(key)

        if last:

            last_time, last_alpha = last

            # TTL duplicate filtering
            if now - last_time < self.DUP_TTL:

                if alpha <= last_alpha:

                    logger.debug(
                        "[DEDUP] filtered weaker signal %s %s alpha=%.3f",
                        symbol,
                        strategy,
                        alpha
                    )

                    return

                logger.info(
                    "[DEDUP] replaced weaker signal %s %s old=%.3f new=%.3f",
                    symbol,
                    strategy,
                    last_alpha,
                    alpha
                )

        self.last_signal[key] = (now, alpha)

        logger.info(
            "[DEDUP] passed %s strategy=%s alpha=%.3f",
            symbol,
            strategy,
            alpha
        )

        self.bus.publish(
            "dedup.signal",
            signal
        )
