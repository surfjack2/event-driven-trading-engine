import time
import threading

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    MAX_NEW_POSITIONS = 1
    MAX_TOTAL_POSITIONS = 3
    MAX_STRATEGY_POSITIONS = 2

    ATR_MULTIPLIER = 2
    GLOBAL_ORDER_INTERVAL = 0.3

    MAX_PORTFOLIO_HEAT = 0.06

    MAX_SPREAD_RATIO = 0.003
    LIMIT_OFFSET_RATIO = 0.001

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.positions = {}
        self.strategy_positions = {}

        self.pending_orders = set()

        self.disabled_strategies = set()

        self.exposure_limit = 1.0

        self.strategy_scores = {}

        self.trading_halted = False

        self.risk = RiskEngine()
        self.sizer = PositionSizer()

        self.last_signal_time = {}
        self.last_global_order_time = 0

        self.lock = threading.Lock()

        self.position_risk = {}

        self.bus.subscribe("optimized.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)
        self.bus.subscribe("ORDER_FILLED", self.on_order_filled)

        self.bus.subscribe("strategy.disabled", self.on_strategy_disabled)
        self.bus.subscribe("strategy.enabled", self.on_strategy_enabled)

        self.bus.subscribe("portfolio.exposure", self.on_exposure_update)
        self.bus.subscribe("strategy.performance", self.on_strategy_performance)

        self.bus.subscribe("system.halt", self.on_system_halt)

    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_system_halt(self, data):

        reason = data.get("reason")

        logger.error("[EXECUTION] trading halted reason=%s", reason)

        self.trading_halted = True

    def on_strategy_performance(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        self.strategy_scores[strategy] = stats.get("score", 1)

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
                self.position_risk.pop(symbol, None)

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

        if self.trading_halted:
            return

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")

        order = {
            "symbol": symbol,
            "side": "BUY",
            "price": price,
            "qty": 1,
            "strategy": strategy
        }

        self.bus.publish("order.request", order)

        logger.info(
            "[EXECUTION] order request symbol=%s",
            symbol
        )
