import time
import threading

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    MAX_GLOBAL_POSITIONS = 5
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

        # Position Intent Engine output
        self.bus.subscribe("intent.signal", self.on_signal)

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

        logger.info(
            "[EXECUTION] exposure limit updated %.2f",
            exposure
        )

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

        logger.warning(
            "[EXECUTION] strategy disabled %s",
            strategy
        )

    def on_strategy_enabled(self, data):

        strategy = data["strategy"]

        if strategy in self.disabled_strategies:
            self.disabled_strategies.remove(strategy)

        logger.info(
            "[EXECUTION] strategy re-enabled %s",
            strategy
        )

    def on_signal(self, signal):

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")
        atr = signal.get("atr", 0)

        weight = signal.get("allocation_weight", 1.0)

        now = time.time()

        if strategy in self.disabled_strategies:

            logger.warning(
                "[EXECUTION] blocked disabled strategy %s",
                strategy
            )

            return

        with self.lock:

            last = self.last_signal_time.get(symbol, 0)

            if now - last < 5:
                logger.debug("[EXECUTION] cooldown active %s", symbol)
                return

            if now - self.last_global_order_time < self.GLOBAL_ORDER_INTERVAL:
                logger.debug("[EXECUTION] global rate limit active")
                return

            if symbol in self.positions or symbol in self.pending_orders:

                logger.info(
                    "[POSITION GATE] already holding or pending %s",
                    symbol
                )

                return

            max_allowed = int(self.MAX_GLOBAL_POSITIONS * self.exposure_limit)

            if len(self.positions) >= max_allowed:

                logger.warning(
                    "[EXECUTION] exposure limit reached current=%s max=%s",
                    len(self.positions),
                    max_allowed
                )

                return

            strategy_pos = self.strategy_positions.get(strategy, 0)

            if strategy_pos >= self.MAX_STRATEGY_POSITIONS:

                logger.warning(
                    "[EXECUTION] strategy position limit reached %s",
                    strategy
                )

                return

            self.last_signal_time[symbol] = now

            if atr > 0:
                stop_price = price - atr * self.ATR_MULTIPLIER
            else:
                stop_price = price * 0.92

            qty = self.sizer.calculate(price, stop_price, weight)

            if qty <= 0:
                logger.warning("[EXECUTION] qty calculated as 0")
                return

            if not self.risk.check(symbol, qty, price):

                logger.warning(
                    "[EXECUTION] risk engine blocked order"
                )

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
            "[EXECUTION] order request published symbol=%s price=%s atr=%s stop=%s qty=%s weight=%s",
            symbol,
            price,
            atr,
            stop_price,
            qty,
            weight
        )
