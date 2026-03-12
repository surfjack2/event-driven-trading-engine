import time
from collections import defaultdict

from ltb.system.logger import logger


class ScannerWorker:

    def __init__(self, bus):

        self.bus = bus

        # 최근 가격 저장
        self.prices = defaultdict(list)

        self.bus.subscribe(
            "market.indicator",
            self.on_market
        )

    def run(self):

        logger.info("[SCANNER WORKER STARTED]")

        while True:
            time.sleep(10)

    def on_market(self, data):

        symbol = data["symbol"]
        price = data["price"]

        self.prices[symbol].append(price)

        if len(self.prices[symbol]) > 20:
            self.prices[symbol].pop(0)

        if len(self.prices[symbol]) < 10:
            return

        change = (
            price - self.prices[symbol][0]
        ) / self.prices[symbol][0]

        # 단순 breakout 조건
        if change > 0.02:

            logger.info(
                f"[SCANNER] breakout detected {symbol} change={change:.2%}"
            )

            self.bus.publish(
                "market.scanner",
                {
                    "symbol": symbol,
                    "change": change
                }
            )
