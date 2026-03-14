import time
from ltb.system.logger import logger


class TrailingStopWorker:

    ATR_MULTIPLIER = 2
    MIN_HOLD_SECONDS = 20

    def __init__(self, event_bus):

        self.event_bus = event_bus

        self.positions = {}
        self.entry_time = {}

        self.atr = {}

        self.pending_orders = set()

        self.event_bus.subscribe("POSITION_OPENED", self.handle_position)
        self.event_bus.subscribe("POSITION_CLOSED", self.handle_close)

        self.event_bus.subscribe("market.indicator", self.handle_indicator)
        self.event_bus.subscribe("MARKET_TICK", self.handle_price)

        self.event_bus.subscribe("ORDER_FILLED", self.handle_filled)

    def run(self):

        logger.info("[TRAILING STOP WORKER STARTED]")

        while True:
            time.sleep(1)

    def handle_position(self, position):

        symbol = position["symbol"]

        self.positions[symbol] = {
            "qty": position["qty"],
            "entry_price": position["entry_price"],
            "highest_price": position["entry_price"]
        }

        self.entry_time[symbol] = time.time()

        logger.info(
            "[TRAILING] tracking symbol=%s qty=%s entry=%s",
            symbol,
            position["qty"],
            position["entry_price"]
        )

    def handle_close(self, position):

        symbol = position["symbol"]

        self.positions.pop(symbol, None)
        self.entry_time.pop(symbol, None)

        logger.info("[TRAILING] stop tracking %s", symbol)

    def handle_indicator(self, event):

        symbol = event["symbol"]
        atr = event.get("atr")

        if atr is None:
            return

        self.atr[symbol] = atr

    def handle_filled(self, order):

        symbol = order["symbol"]

        self.pending_orders.discard(symbol)

    def handle_price(self, tick):

        symbol = tick["symbol"]
        price = tick["price"]

        if symbol not in self.positions:
            return

        if symbol in self.pending_orders:
            return

        entry_time = self.entry_time.get(symbol, 0)

        if time.time() - entry_time < self.MIN_HOLD_SECONDS:
            return

        pos = self.positions[symbol]

        if price > pos["highest_price"]:
            pos["highest_price"] = price

        atr = self.atr.get(symbol)

        if atr is None:
            return

        stop_price = pos["highest_price"] - atr * self.ATR_MULTIPLIER

        if price <= stop_price:

            logger.info(
                "[ATR STOP TRIGGERED] %s price=%s stop=%s",
                symbol,
                price,
                stop_price
            )

            order = {
                "symbol": symbol,
                "side": "SELL",
                "price": price,
                "qty": pos["qty"]
            }

            self.pending_orders.add(symbol)

            self.event_bus.publish("order.request", order)
