import time

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.risk = RiskEngine()

        self.sizer = PositionSizer()

        # 현재 포지션 저장
        self.positions = {}

        self.bus.subscribe("strategy.signal", self.on_signal)

        self.bus.subscribe("portfolio.update", self.on_portfolio_update)


    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]
        price = data["price"]

        # 포지션 상태 업데이트
        self.positions[symbol] = position

        self.risk.update_position(symbol, position, price)


    def on_signal(self, signal):

        logger.info("[EXECUTION] processing signal %s", signal)

        symbol = signal["symbol"]
        entry_price = signal["price"]

        # 1️⃣ Position Gate
        position = self.positions.get(symbol, 0)

        if position > 0:

            logger.info("[POSITION GATE] already holding %s position=%s", symbol, position)

            return

        # stop price (임시 5%)
        stop_price = entry_price * 0.95

        # 2️⃣ position sizing
        qty = self.sizer.calculate(entry_price, stop_price)

        # 3️⃣ risk check
        if not self.risk.check(symbol, qty, entry_price):

            logger.warning("[EXECUTION] order blocked by risk")

            return

        order = {
            "symbol": symbol,
            "side": signal["action"],
            "price": entry_price,
            "qty": qty
        }

        self.bus.publish("order.request", order)

        logger.info("[EXECUTION] order request published")
