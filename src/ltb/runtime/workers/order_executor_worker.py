from ltb.system.logger import logger
from ltb.execution.executor_router import ExecutorRouter
import time


class OrderExecutorWorker:

    def __init__(self, event_bus, context):

        self.event_bus = event_bus
        self.context = context

        self.router = ExecutorRouter(context)

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

            filled = self.router.execute(order)

            if filled:

                self.event_bus.publish("ORDER_FILLED", filled)

                logger.info("[ORDER EXECUTOR] ORDER_FILLED published")
