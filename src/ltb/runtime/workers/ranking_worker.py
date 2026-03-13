import time
from collections import defaultdict

from ltb.system.logger import logger


class RankingWorker:

    def __init__(self, bus):

        self.bus = bus

        self.scores = defaultdict(float)

        self.bus.subscribe(
            "market.indicator",
            self.on_market
        )

    def run(self):

        logger.info("[RANKING WORKER STARTED]")

        while True:

            self.publish_top()

            time.sleep(5)

    def on_market(self, data):

        symbol = data.get("symbol")

        price = data.get("price")
        prev = data.get("prev_price")

        volume = data.get("volume")
        volume_ma = data.get("volume_ma")

        vwap = data.get("vwap")

        if not symbol or not price or not prev:
            return

        score = 0

        # momentum
        change = (price - prev) / prev
        score += change * 40

        # volume spike
        if volume and volume_ma and volume_ma > 0:

            ratio = volume / volume_ma
            score += min(25, ratio * 10)

        # VWAP proximity
        if vwap:

            distance = abs(price - vwap) / vwap
            proximity = max(0, 20 - distance * 200)

            score += proximity

        # breakout
        high = data.get("high")

        if high and price > high:
            score += 15

        self.scores[symbol] = score

    def publish_top(self):

        ranked = sorted(
            self.scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top = [s for s, _ in ranked[:15]]

        logger.info("[RANKING] top symbols=%s", top)

        self.bus.publish(
            "market.ranking",
            {
                "symbols": top
            }
        )
