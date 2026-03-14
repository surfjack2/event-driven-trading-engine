import time
import threading

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    MAX_NEW_POSITIONS = 3
    MAX_TOTAL_POSITIONS = 8
    MAX_STRATEGY_POSITIONS = 2

    ATR_MULTIPLIER = 2

    GLOBAL_ORDER_INTERVAL = 0.3

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}
        self.strategy_positions = {}

        self.pending_orders = set()

        self.disabled_strategies = set()

        self.exposure_limit = 1.0

        self.risk = RiskEngine()
        self.sizer = PositionSizer()

        self.last_signal_time = {}
        self.last_global_order_time = 0

        self.lock = threading.Lock()

        self.bus.subscribe("optimized.signal", self.on_signal)

        self.bus.subscribe("portfolio.update", self.on_portfolio_update)
        self.bus.subscribe("ORDER_FILLED", self.on_order_filled)

        self.bus.subscribe("strategy.disabled", self.on_strategy_disabled)
        self.bus.subscribe("strategy.enabled", self.on_strategy_enabled)

        self.bus.subscribe("portfolio.exposure", self.on_exposure_update)

    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_exposure_update(self, data):

        exposure = data.get("exposure")

        if exposure is None:
            return

        self.exposure_limit = exposure

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]
        strategy = data.get("strategy")

        with self.lock:

            if position <= 0:

                self.positions.pop(symbol, None)

                if strategy:
                    self.strategy_positions[strategy] = max(
                        0,
                        self.strategy_positions.get(strategy, 1) - 1
                    )

            else:

                self.positions[symbol] = position

                if strategy:
                    self.strategy_positions[strategy] = (
                        self.strategy_positions.get(strategy, 0) + 1
                    )

    def on_order_filled(self, order):

        symbol = order["symbol"]

        with self.lock:
            self.pending_orders.discard(symbol)

    def on_strategy_disabled(self, data):

        strategy = data["strategy"]

        self.disabled_strategies.add(strategy)

    def on_strategy_enabled(self, data):

        strategy = data["strategy"]

        self.disabled_strategies.discard(strategy)

    def on_signal(self, signal):

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")
        atr = signal.get("atr", 0)

        weight = signal.get("allocation_weight", 1.0)

        now = time.time()

        if strategy in self.disabled_strategies:
            return

        with self.lock:

            last = self.last_signal_time.get(symbol, 0)

            if now - last < 5:
                return

            if now - self.last_global_order_time < self.GLOBAL_ORDER_INTERVAL:
                return

            if symbol in self.positions or symbol in self.pending_orders:
                return

            # 전체 포지션 제한
            if len(self.positions) >= self.MAX_TOTAL_POSITIONS:
                return

            # 신규 진입 슬롯 제한
            active_new_orders = len(self.pending_orders)

            if active_new_orders >= self.MAX_NEW_POSITIONS:
                return

            strategy_pos = self.strategy_positions.get(strategy, 0)

            if strategy_pos >= self.MAX_STRATEGY_POSITIONS:
                return

            self.last_signal_time[symbol] = now

            if atr > 0:
                stop_price = price - atr * self.ATR_MULTIPLIER
            else:
                stop_price = price * 0.92

            qty = self.sizer.calculate(price, stop_price, weight)

            if qty <= 0:
                return

            if not self.risk.check(symbol, qty, price):
                return

            order = {
                "symbol": symbol,
                "side": "BUY",
                "price": price,
                "qty": qty,
                "strategy": strategy
            }

            self.pending_orders.add(symbol)

            self.last_global_order_time = now

        self.bus.publish("order.request", order)

        logger.info(
            "[EXECUTION] order request published symbol=%s price=%s qty=%s weight=%s",
            symbol,
            price,
            qty,
            weight
        )
