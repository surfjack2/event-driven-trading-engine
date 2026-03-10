import logging
import time

log = logging.getLogger(__name__)


class OrderExecutorWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
        self.queue = []

        self.event_bus.subscribe("ORDER_REQUEST", self.enqueue)

    def enqueue(self, order):

        self.queue.append(order)

    def run(self):

        log.info("[ORDER EXECUTOR WORKER STARTED]")

        while True:

            if not self.queue:
                time.sleep(0.05)
                continue

            order = self.queue.pop(0)

            log.info(f"[ORDER EXECUTOR] executing order {order}")

            filled = {
                "symbol": order["symbol"],
                "action": order["action"],
                "price": order["price"],
                "qty": order.get("qty", 1),
            }

            self.event_bus.publish("ORDER_FILLED", filled)

            log.info("[ORDER EXECUTOR] ORDER_FILLED published")
