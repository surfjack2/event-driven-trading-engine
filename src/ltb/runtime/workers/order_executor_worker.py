import time

from ltb.system.logger import logger
from ltb.execution.kis_executor import KISExecutor


class OrderExecutorWorker:

    def __init__(self, bus):

        self.bus = bus

        self.executor = KISExecutor()

        self.bus.subscribe("order.request", self.execute)


    def run(self):

        logger.info("[ORDER EXECUTOR WORKER STARTED]")

        while True:
            time.sleep(1)


    def execute(self, order):

        logger.info("[ORDER EXECUTOR] executing order %s", order)

        fill = self.executor.place_order(
            symbol=order["symbol"],
            side=order["side"],
            qty=order["qty"],
            price=order["price"]
        )

        self.bus.publish("order.fill", fill)

        logger.info("[ORDER EXECUTOR] fill published")
