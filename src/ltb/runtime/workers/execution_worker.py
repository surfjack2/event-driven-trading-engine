import time

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        self.risk = RiskEngine()
        self.sizer = PositionSizer()

        self.bus.subscribe("strategy.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)


    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        if position <= 0:

            self.positions.pop(symbol, None)

        else:

            self.positions[symbol] = position

        self.risk.update_position(symbol, position, 0)


    def on_signal(self, signal):

        symbol = signal["symbol"]
        price = signal["price"]

        logger.info("[EXECUTION] processing signal %s", signal)

        position = self.positions.get(symbol)

        if position:

            logger.info(
                "[POSITION GATE] already holding %s position=%s",
                symbol,
                position
            )

            return

        stop_price = price * 0.92

        qty = self.sizer.calculate(price, stop_price)

        if not self.risk.check(symbol, qty, price):

            logger.warning("[EXECUTION] risk engine blocked order")

            return

        order = {
            "symbol": symbol,
            "side": "BUY",
            "price": price,
            "qty": qty
        }

        self.bus.publish("order.request", order)

        logger.info("[EXECUTION] order request published")
