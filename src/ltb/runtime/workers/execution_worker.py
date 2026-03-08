import time

from ltb.system.logger import logger
from ltb.runtime.position_sizer import PositionSizer
from ltb.runtime.risk_engine import RiskEngine


class ExecutionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        self.sizer = PositionSizer()

        self.risk = RiskEngine()

        self.bus.subscribe("strategy.signal", self.on_signal)

        self.bus.subscribe("portfolio.update", self.on_portfolio_update)


    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_portfolio_update(self, data):

        symbol = data.get("symbol")
        position = data.get("position", 0)

        if symbol is None:
            return

        self.positions[symbol] = position


    def on_signal(self, signal):

        logger.info("[EXECUTION] processing signal %s", signal)

        symbol = signal.get("symbol")
        price = signal.get("price")

        if symbol is None or price is None:
            return

        position = self.positions.get(symbol, 0)

        if position > 0:

            logger.info(
                "[POSITION GATE] already holding %s position=%s",
                symbol,
                position
            )

            return

        qty = self.sizer.size(price)

        allowed = self.risk.check(symbol, qty, price)

        if not allowed:

            logger.warning("[EXECUTION] order blocked by risk")

            return

        order = {
            "symbol": symbol,
            "side": "BUY",
            "price": price,
            "qty": qty
        }

        self.bus.publish("order.request", order)

        logger.info("[EXECUTION] order request published")
