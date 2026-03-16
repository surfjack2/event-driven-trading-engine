import time
from ltb.system.logger import logger


class PositionTimeStopWorker:

    MAX_HOLD_SECONDS = 3600
    MIN_HOLD_SECONDS = 30

    PROFIT_THRESHOLD = 0.002

    def __init__(self, bus, exit_manager):

        self.bus = bus
        self.exit_manager = exit_manager

        self.positions = {}
        self.entry_time = {}

        self.pending_orders = set()

        self.bus.subscribe("POSITION_OPENED", self.on_open)
        self.bus.subscribe("POSITION_CLOSED", self.on_close)

        self.bus.subscribe("market.indicator", self.on_indicator)

        self.bus.subscribe("ORDER_FILLED", self.on_filled)

    def run(self):

        logger.info("[POSITION TIME STOP WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_open(self, position):

        symbol = position["symbol"]

        self.positions[symbol] = position
        self.entry_time[symbol] = time.time()

        logger.info(
            "[TIME STOP] tracking %s entry=%s",
            symbol,
            position.get("entry_price")
        )

    def on_close(self, position):

        symbol = position["symbol"]

        self.positions.pop(symbol, None)
        self.entry_time.pop(symbol, None)

        self.pending_orders.discard(symbol)

    def on_filled(self, order):

        symbol = order["symbol"]

        self.pending_orders.discard(symbol)

    def on_indicator(self, data):

        symbol = data.get("symbol")

        if symbol not in self.positions:
            return

        if symbol in self.pending_orders:
            return

        entry_time = self.entry_time.get(symbol)

        if not entry_time:
            return

        hold_time = time.time() - entry_time

        if hold_time < self.MIN_HOLD_SECONDS:
            return

        if hold_time < self.MAX_HOLD_SECONDS:
            return

        pos = self.positions[symbol]

        price = data.get("price")

        if not price:
            return

        entry_price = pos.get("entry_price")

        if not entry_price:
            return

        pnl = (price - entry_price) / entry_price

        if pnl >= self.PROFIT_THRESHOLD:

            logger.info(
                "[TIME STOP HOLD] symbol=%s pnl=%.4f hold=%s",
                symbol,
                pnl,
                int(hold_time)
            )

            return

        # 🔴 ExitManager gate
        if not self.exit_manager.request_exit(symbol):
            return

        logger.info(
            "[TIME STOP EXIT] symbol=%s pnl=%.4f hold=%s",
            symbol,
            pnl,
            int(hold_time)
        )

        order = {
            "symbol": symbol,
            "side": "SELL",
            "price": price,
            "qty": pos["qty"]
        }

        self.pending_orders.add(symbol)

        self.bus.publish(
            "order.request",
            order
        )
