import time

from ltb.system.logger import logger


class PortfolioWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        self.bus.subscribe("order.fill", self.on_fill)

    def run(self):

        logger.info("[PORTFOLIO WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_fill(self, fill):

        symbol = fill["symbol"]
        qty = fill["qty"]

        self.positions[symbol] = self.positions.get(symbol, 0) + qty

        logger.info("[PORTFOLIO] updated position %s = %s", symbol, self.positions[symbol])
