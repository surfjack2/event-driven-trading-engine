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

        symbol = fill.get("symbol")
        qty = fill.get("qty", 0)
        side = fill.get("side")

        if symbol is None:
            return

        current = self.positions.get(symbol, 0)

        if side == "BUY":
            current += qty
        else:
            current -= qty

        self.positions[symbol] = current

        logger.info(
            "[PORTFOLIO] updated position %s = %s",
            symbol,
            current
        )

        event = {
            "symbol": symbol,
            "position": current,
            "price": fill.get("price")
        }

        self.bus.publish("portfolio.update", event)
