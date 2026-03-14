import time
from collections import defaultdict
import statistics

from ltb.system.logger import logger


class ScannerWorker:

    def __init__(self, bus):

        self.bus = bus
        self.prices = defaultdict(list)

        self.bus.subscribe(
            "scanner.rtv",
            self.on_market
        )

    def run(self):

        logger.info("[SCANNER WORKER STARTED]")

        while True:
            time.sleep(10)

    def on_market(self, data):

        symbol = data.get("symbol")
        price = data.get("price")
        vwap = data.get("vwap")

        if not symbol or not price:
            return

        self.prices[symbol].append(price)

        if len(self.prices[symbol]) > 30:
            self.prices[symbol].pop(0)

        if len(self.prices[symbol]) < 15:
            return

        change = (
            price - self.prices[symbol][0]
        ) / self.prices[symbol][0]

        if change < 0.015:
            return

        if vwap:

            distance = abs(price - vwap) / vwap

            if distance > 0.03:
                return

        prices = self.prices[symbol]

        returns = []

        for i in range(1, len(prices)):

            r = abs(prices[i] - prices[i - 1]) / prices[i - 1]

            returns.append(r)

        atr = statistics.mean(returns)

        if atr < 0.003:
            return

        logger.info(
            f"[SCANNER] breakout {symbol} change={change:.2%} atr={atr:.4f}"
        )

        self.bus.publish(
            "market.scanner",
            {
                "symbol": symbol,
                "change": change,
                "atr": atr
            }
        )
