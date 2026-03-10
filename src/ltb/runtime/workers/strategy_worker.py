import time

from ltb.system.logger import logger


class StrategyWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus

        self.cooldown = 10
        self.last_trade = None

        self.last_price = None

        self.event_bus.subscribe("market.indicator", self.on_market)

    def run(self):

        logger.info("[STRATEGY WORKER RUNNING]")

        while True:
            time.sleep(1)

    def on_market(self, data):

        price = data["price"]

        now = time.time()

        if self.last_trade is not None:

            if now - self.last_trade < self.cooldown:

                logger.info("[STRATEGY] cooldown active")
                return

        if self.last_price is None:

            self.last_price = price
            return

        if price < 54500 and price > self.last_price:

            logger.info("[STRATEGY] BUY signal")

            self.event_bus.publish(
                "ORDER_REQUEST",
                {
                    "symbol": "TEST",
                    "action": "BUY",
                    "price": price,
                },
            )

            self.last_trade = now

        self.last_price = price
