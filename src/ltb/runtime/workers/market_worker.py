import time
import random

from ltb.system.logger import logger


class MarketWorker:

    def __init__(self, bus):
        self.bus = bus

    def run(self):

        logger.info("[MARKET WORKER STARTED]")

        while True:

            price = random.uniform(45000, 65000)

            event = {
                "symbol": "TEST",
                "price": price
            }

            self.bus.publish("market.price", event)

            logger.info("[MARKET] pushed price %s", price)

            time.sleep(1)


def run_market_worker(bus):

    worker = MarketWorker(bus)
    worker.run()
