from ltb.system.logger import logger
import time


class TrailingStopWorker:

    def __init__(self, event_bus):

        self.event_bus = event_bus
        self.positions = {}

        self.trailing_pct = 0.03

        self.event_bus.subscribe("POSITION_OPENED", self.handle_position)
        self.event_bus.subscribe("POSITION_CLOSED", self.handle_close)
        self.event_bus.subscribe("MARKET_TICK", self.handle_price)

    def run(self):

        logger.info("[TRAILING STOP WORKER STARTED]")

        while True:
            time.sleep(1)

    def handle_position(self, position):

        symbol = position["symbol"]

        self.positions[symbol] = position

        logger.info(
            f"[TRAILING] tracking symbol={symbol} qty={position['qty']} entry={position['entry_price']}"
        )

    def handle_close(self, position):

        symbol = position["symbol"]

        if symbol in self.positions:

            del self.positions[symbol]

            logger.info(f"[TRAILING] stop tracking {symbol}")

    def handle_price(self, tick):

        symbol = tick["symbol"]
        price = tick["price"]

        if symbol not in self.positions:
            return

        pos = self.positions[symbol]

        if price > pos["highest_price"]:

            pos["highest_price"] = price

            logger.info(f"[TRAILING] new high {price}")

        stop_price = pos["highest_price"] * (1 - self.trailing_pct)

        logger.info(
            f"[TRAILING] price={price} high={pos['highest_price']} stop={stop_price}"
        )

        if price <= stop_price:

            logger.info(f"[TRAILING] STOP TRIGGERED {price}")

            order = {
                "symbol": symbol,
                "side": "SELL",
                "price": price,
                "qty": pos["qty"]
            }

            self.event_bus.publish("order.request", order)
