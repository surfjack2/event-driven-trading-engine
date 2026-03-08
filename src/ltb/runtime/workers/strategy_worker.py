import time

from ltb.system.logger import logger


class StrategyWorker:

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe("market.price", self.on_price)

    def run(self):

        logger.info("[STRATEGY WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_price(self, data):

        price = data["price"]

        logger.info("[STRATEGY] received %s", price)

        if price > 60000:

            signal = {
                "symbol": data["symbol"],
                "action": "BUY",
                "price": price
            }

            self.bus.publish("strategy.signal", signal)

            logger.info("[STRATEGY] signal generated")


def run_strategy_worker(bus):

    worker = StrategyWorker(bus)
    worker.run()
