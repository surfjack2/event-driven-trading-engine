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
        score += change * 50

        # volume expansion
        if volume and volume_ma and volume > volume_ma:
            score += 10

        # vwap proximity
        if vwap:
            distance = abs(price - vwap) / vwap
            score += max(0, 5 - distance * 10)

        self.scores[symbol] = score

    def publish_top(self):

        ranked = sorted(
            self.scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top = [s for s, _ in ranked[:30]]

        logger.info(f"[RANKING] top symbols={top}")

        self.bus.publish(
            "market.ranking",
            {
                "symbols": top
            }
        )
