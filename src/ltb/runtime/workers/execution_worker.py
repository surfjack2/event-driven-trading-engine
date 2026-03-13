import time
import threading

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    MAX_GLOBAL_POSITIONS = 5

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}
        self.pending_orders = set()

        self.risk = RiskEngine()
        self.sizer = PositionSizer()

        self.last_signal_time = {}

        # race condition protection
        self.lock = threading.Lock()

        self.bus.subscribe("allocation.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)

    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        with self.lock:

            if position <= 0:
                self.positions.pop(symbol, None)
            else:
                self.positions[symbol] = position

            # 주문 완료 시 pending 제거
            self.pending_orders.discard(symbol)

    def on_signal(self, signal):

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")

        now = time.time()

        # cooldown filter
        last = self.last_signal_time.get(symbol, 0)

        if now - last < 5:

            logger.debug("[EXECUTION] cooldown active %s", symbol)

            return

        with self.lock:

            self.last_signal_time[symbol] = now

            if symbol in self.positions or symbol in self.pending_orders:

                logger.info(
                    "[POSITION GATE] already holding or pending %s",
                    symbol
                )

                return

            if len(self.positions) >= self.MAX_GLOBAL_POSITIONS:

                logger.warning(
                    "[EXECUTION] global position limit reached"
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
                "qty": qty,
                "strategy": strategy
            }

            # pending 등록 (race protection)
            self.pending_orders.add(symbol)

        # lock 밖에서 publish
        self.bus.publish("order.request", order)

        logger.info("[EXECUTION] order request published")
