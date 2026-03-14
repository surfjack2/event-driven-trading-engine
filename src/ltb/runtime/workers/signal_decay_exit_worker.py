import time
from ltb.system.logger import logger


class SignalDecayExitWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        # 주문 충돌 방지
        self.pending_orders = set()

        self.bus.subscribe("POSITION_OPENED", self.on_open)
        self.bus.subscribe("POSITION_CLOSED", self.on_close)

        self.bus.subscribe("market.indicator", self.on_indicator)

        self.bus.subscribe("ORDER_FILLED", self.on_filled)

    def run(self):

        logger.info("[SIGNAL DECAY EXIT WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_open(self, position):

        symbol = position["symbol"]

        self.positions[symbol] = position

    def on_close(self, position):

        symbol = position["symbol"]

        if symbol in self.positions:
            del self.positions[symbol]

        self.pending_orders.discard(symbol)

    def on_filled(self, order):

        symbol = order["symbol"]

        self.pending_orders.discard(symbol)

    def on_indicator(self, data):

        symbol = data.get("symbol")

        if symbol not in self.positions:
            return

        # pending 주문 있으면 exit 금지
        if symbol in self.pending_orders:
            return

        price = data.get("price")
        vwap = data.get("vwap")

        volume = data.get("volume")
        volume_ma = data.get("volume_ma")

        if not price or not vwap:
            return

        decay = False

        if price < vwap:
            decay = True

        if volume and volume_ma and volume < volume_ma * 0.6:
            decay = True

        if not decay:
            return

        pos = self.positions[symbol]

        logger.info(
            "[SIGNAL DECAY EXIT] symbol=%s price=%s vwap=%s",
            symbol,
            price,
            vwap
        )

        order = {
            "symbol": symbol,
            "side": "SELL",
            "price": price,
            "qty": pos["qty"]
        }

        self.pending_orders.add(symbol)

        self.bus.publish("order.request", order)
