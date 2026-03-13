from ltb.system.logger import logger
import time


class LiquidityFilterWorker:

    MIN_VOLUME = 5000
    MIN_PRICE = 2000
    MAX_SPREAD_RATIO = 0.002

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe(
            "ranked.signal",
            self.on_signal
        )

    def run(self):

        logger.info("[LIQUIDITY FILTER WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_signal(self, signal):

        symbol = signal["symbol"]

        volume = signal.get("volume")
        price = signal.get("price")
        bid = signal.get("bid")
        ask = signal.get("ask")

        if volume is None:
            logger.debug("[LIQUIDITY] volume missing %s", symbol)
            return

        if volume < self.MIN_VOLUME:
            logger.debug("[LIQUIDITY] volume filtered %s", symbol)
            return

        if price is None or price < self.MIN_PRICE:
            logger.debug("[LIQUIDITY] price filtered %s", symbol)
            return

        if bid and ask:

            spread = ask - bid
            spread_ratio = spread / price

            if spread_ratio > self.MAX_SPREAD_RATIO:
                logger.debug("[LIQUIDITY] spread filtered %s", symbol)
                return

        logger.info("[LIQUIDITY] passed %s", symbol)

        self.bus.publish(
            "liquidity.signal",
            signal
        )
