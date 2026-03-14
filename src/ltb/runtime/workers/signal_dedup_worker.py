import time
from ltb.system.logger import logger


class SignalDedupWorker:

    DUP_TTL = 20.0

    def __init__(self, bus):

        self.bus = bus

        # symbol → (timestamp, alpha_score)
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

        alpha = signal.get("alpha_score", 0)

        last = self.last_signal.get(symbol)

        if last:

            last_time, last_alpha = last

            # TTL 내 duplicate 처리
            if now - last_time < self.DUP_TTL:

                # alpha가 더 강하면 교체
                if alpha <= last_alpha:

                    logger.debug(
                        "[DEDUP] filtered weaker signal %s alpha=%.3f",
                        symbol,
                        alpha
                    )

                    return

                logger.info(
                    "[DEDUP] replaced weaker signal %s old=%.3f new=%.3f",
                    symbol,
                    last_alpha,
                    alpha
                )

        self.last_signal[symbol] = (now, alpha)

        logger.info(
            "[DEDUP] passed %s strategy=%s alpha=%.3f",
            symbol,
            signal.get("strategy"),
            alpha
        )

        self.bus.publish(
            "dedup.signal",
            signal
        )
