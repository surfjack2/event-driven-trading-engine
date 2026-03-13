import time
from collections import deque

from ltb.system.logger import logger


class MarketRegimeWorker:

    WINDOW = 50

    def __init__(self, bus):

        self.bus = bus

        self.prices = deque(maxlen=self.WINDOW)

        self.current_regime = "unknown"

        self.bus.subscribe("market.tick", self.on_tick)

    def run(self):

        logger.info("[MARKET REGIME WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_tick(self, tick):

        price = tick.get("price")

        if not price:
            return

        self.prices.append(price)

        if len(self.prices) < self.WINDOW:
            return

        self.evaluate_regime()

    def evaluate_regime(self):

        first = self.prices[0]
        last = self.prices[-1]

        change = (last - first) / first

        high = max(self.prices)
        low = min(self.prices)

        volatility = (high - low) / first

        if change > 0.01:
            regime = "bull"

        elif change < -0.01:
            regime = "bear"

        else:
            regime = "sideways"

        if regime != self.current_regime:

            self.current_regime = regime

            logger.info(
                "[MARKET REGIME] regime=%s volatility=%.4f change=%.4f",
                regime,
                volatility,
                change
            )

            self.bus.publish(
                "market.regime",
                {
                    "regime": regime,
                    "volatility": volatility
                }
            )
