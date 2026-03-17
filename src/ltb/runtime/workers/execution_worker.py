import time
import threading

from ltb.system.logger import logger
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    MAX_NEW_POSITIONS = 1
    MAX_TOTAL_POSITIONS = 3
    MAX_STRATEGY_POSITIONS = 2

    ATR_MULTIPLIER = 2
    GLOBAL_ORDER_INTERVAL = 0.3

    MAX_PORTFOLIO_HEAT = 0.06

    # 🔴 Signal decay guard
    SIGNAL_MAX_AGE = 3.0

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.positions = {}
        self.strategy_positions = {}

        self.pending_orders = set()

        self.disabled_strategies = set()

        self.strategy_scores = {}

        self.trading_halted = False

        self.risk = context.risk_engine

        self.sizer = PositionSizer(self.risk)

        self.lock = threading.Lock()

        self.position_risk = {}

        self.last_order_time = 0

        self.bus.subscribe("optimized.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)
        self.bus.subscribe("ORDER_FILLED", self.on_order_filled)
        self.bus.subscribe("system.halt", self.on_system_halt)

        self.bus.subscribe(
            "strategy.performance",
            self.on_strategy_performance
        )

    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)

    def publish_block(self, symbol, reason):

        self.bus.publish(
            "execution.block",
            {
                "symbol": symbol,
                "reason": reason
            }
        )

    def publish_sizing(self, symbol, qty, price, alpha, weight):

        self.bus.publish(
            "execution.sizing",
            {
                "symbol": symbol,
                "qty": qty,
                "price": price,
                "alpha": alpha,
                "weight": weight
            }
        )

    def on_strategy_performance(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        score = stats.get("score", 1.0)

        self.strategy_scores[strategy] = score

    def on_system_halt(self, data):

        reason = data.get("reason")

        logger.error("[EXECUTION] trading halted reason=%s", reason)

        self.trading_halted = True

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]
        strategy = data.get("strategy")
        price = data.get("price", 0)

        if position <= 0:

            self.positions.pop(symbol, None)
            self.position_risk.pop(symbol, None)

            self.risk.update_position(symbol, 0, 0)

            if strategy and strategy in self.strategy_positions:

                self.strategy_positions[strategy] -= 1

                if self.strategy_positions[strategy] <= 0:
                    del self.strategy_positions[strategy]

        else:

            self.positions[symbol] = position

            self.risk.update_position(symbol, position, price)

            if strategy:

                self.strategy_positions[strategy] = \
                    self.strategy_positions.get(strategy, 0) + 1

    def on_order_filled(self, order):

        symbol = order["symbol"]

        with self.lock:
            self.pending_orders.discard(symbol)

    def calculate_stop_price(self, signal):

        price = signal["price"]
        atr = signal.get("atr")

        if not atr:
            atr = price * 0.01

        return price - atr * self.ATR_MULTIPLIER

    def calculate_portfolio_heat(self):

        capital = self.risk.get_capital()

        total_risk = sum(self.position_risk.values())

        if capital <= 0:
            return 0

        return total_risk / capital

    def get_strategy_multiplier(self, strategy):

        score = self.strategy_scores.get(strategy, 1.0)

        if score >= 2.0:
            return 1.4
        elif score >= 1.5:
            return 1.2
        elif score >= 1.0:
            return 1.0
        elif score >= 0.5:
            return 0.7
        else:
            return 0.4

    def on_signal(self, signal):

        if self.trading_halted:
            return

        now = time.time()

        # 🔴 Signal decay guard
        signal_ts = signal.get("timestamp", now)

        if now - signal_ts > self.SIGNAL_MAX_AGE:

            logger.info(
                "[EXECUTION BLOCK] stale signal %s age=%.2f",
                signal.get("symbol"),
                now - signal_ts
            )

            self.publish_block(signal.get("symbol"), "stale_signal")

            return

        if now - self.last_order_time < self.GLOBAL_ORDER_INTERVAL:
            return

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")

        if symbol in self.positions:
            self.publish_block(symbol, "already_position")
            return

        if symbol in self.pending_orders:
            self.publish_block(symbol, "pending_order")
            return

        if len(self.positions) >= self.MAX_TOTAL_POSITIONS:

            logger.info("[EXECUTION BLOCK] max positions reached")

            self.publish_block(symbol, "max_positions")

            return

        strategy_count = self.strategy_positions.get(strategy, 0)

        if strategy_count >= self.MAX_STRATEGY_POSITIONS:

            logger.info(
                "[EXECUTION BLOCK] strategy limit reached %s",
                strategy
            )

            self.publish_block(symbol, "strategy_limit")

            return

        stop_price = self.calculate_stop_price(signal)

        alpha = signal.get("alpha_score", 0)
        weight = signal.get("allocation_weight", 1.0)

        multiplier = self.get_strategy_multiplier(strategy)

        qty = self.sizer.calculate(
            entry_price=price,
            stop_price=stop_price,
            weight=weight,
            multiplier=multiplier,
            alpha=alpha
        )

        self.publish_sizing(symbol, qty, price, alpha, weight)

        if qty <= 0:
            self.publish_block(symbol, "position_size_zero")
            return

        position_risk = abs(price - stop_price) * qty

        capital = self.risk.get_capital()

        portfolio_heat = self.calculate_portfolio_heat()

        if portfolio_heat + (position_risk / capital) > self.MAX_PORTFOLIO_HEAT:

            logger.warning(
                "[EXECUTION BLOCK] portfolio heat exceeded heat=%s",
                portfolio_heat
            )

            self.publish_block(symbol, "portfolio_heat")

            return

        if not self.risk.check(symbol, qty, price):
            self.publish_block(symbol, "risk_engine")
            return

        order = {
            "symbol": symbol,
            "side": "BUY",
            "price": price,
            "qty": qty,
            "strategy": strategy
        }

        with self.lock:
            self.pending_orders.add(symbol)

        self.position_risk[symbol] = position_risk

        self.bus.publish("order.request", order)

        self.last_order_time = now

        logger.info(
            "[EXECUTION] order request symbol=%s qty=%s heat=%s multiplier=%s",
            symbol,
            qty,
            portfolio_heat,
            multiplier
        )
