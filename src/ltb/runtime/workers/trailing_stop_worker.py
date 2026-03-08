import time

from ltb.system.logger import logger


class TrailingStopWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        self.last_prices = {}

        self.trail_percent = 0.05

        self.bus.subscribe("portfolio.update", self.on_position_update)
        self.bus.subscribe("market.price", self.on_price)


    def run(self):

        logger.info("[TRAILING STOP WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_position_update(self, data):

        symbol = data.get("symbol")
        position = data.get("position", 0)

        if symbol is None:
            return

        if position <= 0:

            if symbol in self.positions:
                del self.positions[symbol]

            return

        price = data.get("price")

        if price is None:
            price = self.last_prices.get(symbol)

        if price is None:
            return

        if symbol not in self.positions:

            stop_price = price * (1 - self.trail_percent)

            self.positions[symbol] = {
                "entry": price,
                "stop": stop_price,
                "qty": position
            }

            logger.info(
                "[TRAIL INIT] %s entry=%s stop=%s",
                symbol,
                price,
                stop_price
            )


    def on_price(self, event):

        symbol = event.get("symbol")
        price = event.get("price")

        if symbol is None or price is None:
            return

        self.last_prices[symbol] = price

        pos = self.positions.get(symbol)

        if pos is None:
            return

        stop = pos["stop"]

        new_stop = price * (1 - self.trail_percent)

        if new_stop > stop:

            pos["stop"] = new_stop

            logger.info(
                "[TRAIL MOVE] %s new_stop=%s",
                symbol,
                new_stop
            )

        if price < pos["stop"]:

            logger.info(
                "[TRAIL STOP HIT] %s price=%s stop=%s",
                symbol,
                price,
                pos["stop"]
            )

            order = {
                "symbol": symbol,
                "side": "SELL",
                "price": price,
                "qty": pos["qty"]
            }

            self.bus.publish("order.request", order)

            del self.positions[symbol]
