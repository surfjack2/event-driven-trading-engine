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

        price = fill["price"]

        if symbol not in self.positions:
            self.positions[symbol] = 0

        if fill["side"] == "BUY":
            self.positions[symbol] += qty
        else:
            self.positions[symbol] -= qty

        position = self.positions[symbol]

        logger.info("[PORTFOLIO] updated position %s = %s", symbol, position)

        event = {
            "symbol": symbol,
            "position": position,
            "price": price
        }

        self.bus.publish("portfolio.update", event)
