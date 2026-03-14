import time
from collections import deque
import statistics

from ltb.system.logger import logger


class MarketRegimeWorker:

    WINDOW = 50
    SHORT_EMA = 10
    LONG_EMA = 30

    def __init__(self, bus):

        self.bus = bus

        self.prices = deque(maxlen=self.WINDOW)

        self.current_regime = "unknown"

        # FIX: event name
        self.bus.subscribe("MARKET_TICK", self.on_tick)

    def run(self):

        logger.info("[MARKET REGIME WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_tick(self, tick):

        price = tick.get("price")

        if not price:
            return

        self.prices.append(price)

        if len(self.prices) < self.LONG_EMA:
            return

        self.evaluate_regime()

    def ema(self, data, period):

        if len(data) < period:
            return None

        k = 2 / (period + 1)

        ema = data[0]

        for p in data[1:]:
            ema = p * k + ema * (1 - k)

        return ema

    def evaluate_regime(self):

        prices = list(self.prices)

        ema_short = self.ema(prices, self.SHORT_EMA)
        ema_long = self.ema(prices, self.LONG_EMA)

        if ema_short is None or ema_long is None:
            return

        volatility = statistics.pstdev(prices) / prices[-1]

        diff = (ema_short - ema_long) / ema_long

        if diff > 0.002:

            regime = "bull"

        elif diff < -0.002:

            regime = "bear"

        else:

            regime = "sideways"

        if regime != self.current_regime:

            self.current_regime = regime

            logger.info(
                "[MARKET REGIME] regime=%s diff=%.4f vol=%.4f",
                regime,
                diff,
                volatility
            )

            self.bus.publish(
                "market.regime",
                {
                    "regime": regime,
                    "volatility": volatility
                }
            )
