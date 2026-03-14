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

    # 🔴 portfolio heat control
    MAX_PORTFOLIO_HEAT = 0.06  # 6% risk

    # 🔴 slippage control
    MAX_SPREAD_RATIO = 0.003
    LIMIT_OFFSET_RATIO = 0.001

    def __init__(self, bus):

        self.bus = bus

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

        # 🔴 portfolio heat tracking
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

    def get_multiplier(self, strategy):

        score = self.strategy_scores.get(strategy, 1)

        if score > 1.5:
            return 1.3

        if score > 1.0:
            return 1.1

        if score > 0.7:
            return 1.0

        if score > 0.4:
            return 0.8

        return 0.6

    # 🔴 slippage control
    def calculate_limit_price(self, price, bid, ask):

        if not bid or not ask:
            return price

        spread = ask - bid
        spread_ratio = spread / price

        if spread_ratio > self.MAX_SPREAD_RATIO:

            logger.info(
                "[EXECUTION] spread too large %.4f",
                spread_ratio
            )

            return None

        limit_price = bid + spread * 0.5

        limit_price = min(
            limit_price,
            price * (1 + self.LIMIT_OFFSET_RATIO)
        )

        return limit_price

    # 🔴 portfolio heat 계산
    def calculate_portfolio_heat(self):

        total_risk = sum(self.position_risk.values())

        capital = self.risk.get_capital()

        if capital <= 0:
            return 0

        return total_risk / capital

    def on_signal(self, signal):

        if self.trading_halted:
            return

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")
        atr = signal.get("atr", 0)

        bid = signal.get("bid")
        ask = signal.get("ask")

        weight = signal.get("allocation_weight", 1.0)

        alpha = signal.get("alpha_score", 1.0)

        now = time.time()

        if strategy in self.disabled_strategies:
            return

        limit_price = self.calculate_limit_price(price, bid, ask)

        if limit_price is None:
            return

        with self.lock:

            if symbol in self.positions:
                return

            if symbol in self.pending_orders:
                return

            if len(self.positions) >= self.MAX_TOTAL_POSITIONS:
                return

            if len(self.pending_orders) >= self.MAX_NEW_POSITIONS:
                return

            strategy_pos = self.strategy_positions.get(strategy, 0)

            if strategy_pos >= self.MAX_STRATEGY_POSITIONS:
                return

            if now - self.last_global_order_time < self.GLOBAL_ORDER_INTERVAL:
                return

            multiplier = self.get_multiplier(strategy)

            if atr > 0:
                stop_price = limit_price - atr * self.ATR_MULTIPLIER
            else:
                stop_price = limit_price * 0.92

            qty = self.sizer.calculate(
                limit_price,
                stop_price,
                weight,
                multiplier,
                alpha
            )

            if qty <= 0:
                return

            if not self.risk.check(symbol, qty, limit_price):
                return

            # 🔴 예상 리스크 계산
            risk_per_share = limit_price - stop_price
            position_risk = risk_per_share * qty

            capital = self.risk.get_capital()

            new_heat = (
                sum(self.position_risk.values()) + position_risk
            ) / capital

            if new_heat > self.MAX_PORTFOLIO_HEAT:

                logger.warning(
                    "[EXECUTION] portfolio heat limit reached %.3f",
                    new_heat
                )

                return

            if symbol in self.pending_orders:
                return

            order = {
                "symbol": symbol,
                "side": "BUY",
                "price": limit_price,
                "qty": qty,
                "strategy": strategy
            }

            self.pending_orders.add(symbol)

            # 🔴 risk 기록
            self.position_risk[symbol] = position_risk

            self.last_global_order_time = now

        self.bus.publish("order.request", order)

        logger.info(
            "[EXECUTION] order request symbol=%s qty=%s heat=%.3f",
            symbol,
            qty,
            self.calculate_portfolio_heat()
        )
