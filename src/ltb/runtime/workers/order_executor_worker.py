from ltb.system.logger import logger
import time


class OrderExecutorWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
        self.queue = []

        self.event_bus.subscribe("order.request", self.enqueue)

    def enqueue(self, order):

        self.queue.append(order)

        logger.info("[ORDER EXECUTOR] queued order %s", order)

    def run(self):

        logger.info("[ORDER EXECUTOR WORKER STARTED]")

        while True:

            if not self.queue:
                time.sleep(0.05)
                continue

            order = self.queue.pop(0)

            logger.info("[ORDER EXECUTOR] executing order %s", order)

            filled = {
                "symbol": order["symbol"],
                "action": order["side"],
                "price": order["price"],
                "qty": order.get("qty", 1),
                "strategy": order.get("strategy")
            }

            self.event_bus.publish("ORDER_FILLED", filled)

            logger.info("[ORDER EXECUTOR] ORDER_FILLED published")
