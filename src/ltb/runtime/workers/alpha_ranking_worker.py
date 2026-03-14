import time
from collections import defaultdict

from ltb.system.logger import logger


class AlphaRankingWorker:

    MAX_SYMBOLS = 20
    RANK_INTERVAL = 3

    def __init__(self, bus):

        self.bus = bus

        self.scores = defaultdict(float)

        self.bus.subscribe(
            "scanner.rtv",
            self.on_signal
        )

    def run(self):

        logger.info("[ALPHA RANKING WORKER STARTED]")

        while True:

            if not self.scores:
                time.sleep(self.RANK_INTERVAL)
                continue

            ranked = sorted(
                self.scores.items(),
                key=lambda x: x[1],
                reverse=True
            )

            symbols = [
                s[0] for s in ranked[:self.MAX_SYMBOLS]
            ]

            logger.info(
                "[ALPHA] selected symbols=%s",
                symbols
            )

            self.bus.publish(
                "alpha.symbols",
                {
                    "symbols": symbols
                }
            )

            self.scores.clear()

            time.sleep(self.RANK_INTERVAL)

    def on_signal(self, data):

        symbol = data.get("symbol")

        if not symbol:
            return

        price = data.get("price")
        turnover = data.get("turnover")
        atr = data.get("atr", 0)

        if not price or not turnover:
            return

        volatility = atr / price if atr else 0.001

        score = turnover * volatility

        self.scores[symbol] += score
