import time

from ltb.system.logger import logger


class ExecutionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe("strategy.signal", self.on_signal)

    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_signal(self, signal):

        logger.info("[EXECUTION] processing signal %s", signal)

        order = {
            "symbol": signal["symbol"],
            "side": signal["action"],
            "price": signal["price"],
            "qty": 1
        }

        self.bus.publish("order.request", order)

        logger.info("[EXECUTION] order request published")
