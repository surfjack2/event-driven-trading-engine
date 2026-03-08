import time

from ltb.system.logger import logger


class OrderExecutorWorker:

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe("order.request", self.execute)

    def run(self):

        logger.info("[ORDER EXECUTOR STARTED]")

        while True:
            time.sleep(1)

    def execute(self, order):

        logger.info("[ORDER EXECUTOR] executing order %s", order)

        fill = {
            "symbol": order["symbol"],
            "side": order["side"],
            "price": order["price"],
            "qty": order["qty"]
        }

        self.bus.publish("order.fill", fill)

        logger.info("[ORDER EXECUTOR] order filled")
