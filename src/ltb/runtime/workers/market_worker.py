import random
import time

from ltb.system.logger import logger


class MarketWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
        self.price = 55000

    def run(self):

        logger.info("[MARKET WORKER STARTED]")

        while True:

            move = random.uniform(-200, 200)
            self.price += move

            price = float(self.price)

            self.event_bus.publish(
                "market.price",
                {
                    "symbol": "TEST",
                    "price": price,
                },
            )

            self.event_bus.publish(
                "MARKET_TICK",
                {
                    "symbol": "TEST",
                    "price": price,
                },
            )

            logger.info(f"[MARKET] price={price}")

            time.sleep(0.2)
