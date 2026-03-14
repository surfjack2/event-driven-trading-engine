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
        prev_price = data.get("prev_price")

        turnover = data.get("turnover")
        turnover_ma = data.get("turnover_ma")

        volume = data.get("volume")
        volume_ma = data.get("volume_ma")

        vwap = data.get("vwap")
        atr = data.get("atr", 0)

        if not price or not turnover:
            return

        score = 0

        # price momentum
        if prev_price:
            momentum = (price - prev_price) / prev_price
            score += momentum * 400

        # vwap displacement
        if vwap:
            vwap_gap = (price - vwap) / vwap
            score += vwap_gap * 250

        # volume impulse
        if volume and volume_ma:
            vol_ratio = volume / volume_ma
            score += vol_ratio * 30

        # turnover impulse
        if turnover_ma:
            turnover_ratio = turnover / turnover_ma
            score += turnover_ratio * 40

        # volatility penalty
        if atr and price:
            volatility = atr / price
            score -= volatility * 180

        self.scores[symbol] += score
