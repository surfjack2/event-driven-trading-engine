from ltb.system.logger import logger
from ltb.execution.executor_router import ExecutorRouter
from collections import deque
import time
import threading


class OrderExecutorWorker:

    def __init__(self, event_bus, context):

        self.event_bus = event_bus
        self.context = context

        self.router = ExecutorRouter(context)

        # thread-safe queue
        self.queue = deque()

        self.lock = threading.Lock()

        self.event_bus.subscribe(
            "order.request",
            self.enqueue
        )

    def enqueue(self, order):

        with self.lock:

            self.queue.append(order)

        logger.info(
            "[ORDER EXECUTOR] queued order %s",
            order
        )

    def run(self):

        logger.info("[ORDER EXECUTOR WORKER STARTED]")

        while True:

            with self.lock:

                if not self.queue:
                    order = None
                else:
                    order = self.queue.popleft()

            if order is None:

                time.sleep(0.05)
                continue

            logger.info(
                "[ORDER EXECUTOR] executing order %s",
                order
            )

            filled = self.router.execute(order)

            if filled:

                self.event_bus.publish(
                    "ORDER_FILLED",
                    filled
                )

                logger.info(
                    "[ORDER EXECUTOR] ORDER_FILLED published"
                )
