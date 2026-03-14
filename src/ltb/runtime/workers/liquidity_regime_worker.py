import time
from collections import deque
import statistics

from ltb.system.logger import logger


class LiquidityRegimeWorker:

    WINDOW = 200
    REGIME_CONFIRM = 5

    def __init__(self, bus):

        self.bus = bus

        self.turnovers = deque(maxlen=self.WINDOW)
        self.volatility = deque(maxlen=self.WINDOW)

        self.current_regime = "NORMAL"
        self.candidate_regime = None
        self.candidate_count = 0

        self.bus.subscribe(
            "market.indicator",
            self.on_indicator
        )

    def run(self):

        logger.info("[LIQUIDITY REGIME WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_indicator(self, data):

        turnover = data.get("turnover")
        atr = data.get("atr")
        price = data.get("price")

        if not turnover or not atr or not price:
            return

        vol = atr / price

        self.turnovers.append(turnover)
        self.volatility.append(vol)

        if len(self.turnovers) < 50:
            return

        self.evaluate()

    def evaluate(self):

        avg_turnover = statistics.mean(self.turnovers)
        avg_vol = statistics.mean(self.volatility)

        latest_turnover = self.turnovers[-1]
        latest_vol = self.volatility[-1]

        regime = "NORMAL"

        if latest_turnover < avg_turnover * 0.5:
            regime = "DEAD"

        elif latest_turnover > avg_turnover * 2 and latest_vol > avg_vol * 1.5:
            regime = "PANIC"

        elif latest_turnover > avg_turnover * 1.5:
            regime = "EXPANSION"

        if regime != self.candidate_regime:
            self.candidate_regime = regime
            self.candidate_count = 1
            return

        self.candidate_count += 1

        if self.candidate_count < self.REGIME_CONFIRM:
            return

        if regime == self.current_regime:
            return

        self.current_regime = regime

        logger.info(
            "[LIQUIDITY REGIME] regime=%s turnover=%.2f vol=%.4f",
            regime,
            latest_turnover,
            latest_vol
        )

        self.bus.publish(
            "market.liquidity_regime",
            {
                "regime": regime,
                "turnover": latest_turnover,
                "volatility": latest_vol
            }
        )
