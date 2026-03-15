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

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.positions = {}
        self.strategy_positions = {}

        self.pending_orders = set()

        self.disabled_strategies = set()

        self.strategy_scores = {}

        self.trading_halted = False

        # shared risk engine
        self.risk = context.risk_engine

        self.sizer = PositionSizer(self.risk)

        self.lock = threading.Lock()

        self.position_risk = {}

        # 🔴 주문 rate control
        self.last_order_time = 0

        self.bus.subscribe("optimized.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)
        self.bus.subscribe("ORDER_FILLED", self.on_order_filled)

        self.bus.subscribe("system.halt", self.on_system_halt)

    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_system_halt(self, data):

        reason = data.get("reason")

        logger.error("[EXECUTION] trading halted reason=%s", reason)

        self.trading_halted = True

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]
        strategy = data.get("strategy")

        if position <= 0:

            self.positions.pop(symbol, None)
            self.position_risk.pop(symbol, None)

            if strategy and strategy in self.strategy_positions:

                self.strategy_positions[strategy] -= 1

                if self.strategy_positions[strategy] <= 0:
                    self.strategy_positions.pop(strategy, None)

        else:

            self.positions[symbol] = position

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
            return None

        return price - atr * self.ATR_MULTIPLIER

    def calculate_portfolio_heat(self):

        capital = self.risk.get_capital()

        total_risk = sum(self.position_risk.values())

        if capital <= 0:
            return 0

        return total_risk / capital

    def on_signal(self, signal):

        if self.trading_halted:
            return

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")

        # 이미 포지션 있는 종목 진입 금지
        if symbol in self.positions:
            return

        # 주문 대기 중
        if symbol in self.pending_orders:
            return

        # 총 포지션 제한
        if len(self.positions) >= self.MAX_TOTAL_POSITIONS:

            logger.info("[EXECUTION BLOCK] max positions reached")

            return

        # 전략 포지션 제한
        strategy_count = self.strategy_positions.get(strategy, 0)

        if strategy_count >= self.MAX_STRATEGY_POSITIONS:

            logger.info(
                "[EXECUTION BLOCK] strategy limit reached strategy=%s",
                strategy
            )

            return

        stop_price = self.calculate_stop_price(signal)

        if stop_price is None:
            return

        alpha = signal.get("alpha_score", 0)
        weight = signal.get("allocation_weight", 1.0)

        qty = self.sizer.calculate(
            entry_price=price,
            stop_price=stop_price,
            weight=weight,
            multiplier=1.0,
            alpha=alpha
        )

        if qty <= 0:
            return

        position_risk = abs(price - stop_price) * qty

        capital = self.risk.get_capital()

        portfolio_heat = self.calculate_portfolio_heat()

        if portfolio_heat + (position_risk / capital) > self.MAX_PORTFOLIO_HEAT:

            logger.warning(
                "[EXECUTION BLOCK] portfolio heat exceeded heat=%s",
                portfolio_heat
            )

            return

        if not self.risk.check(symbol, qty, price):
            return

        # 🔴 GLOBAL ORDER RATE CONTROL
        now = time.time()

        if now - self.last_order_time < self.GLOBAL_ORDER_INTERVAL:

            logger.info("[EXECUTION BLOCK] global order interval")

            return

        order = {
            "symbol": symbol,
            "side": "BUY",
            "price": price,
            "qty": qty,
            "strategy": strategy
        }

        self.pending_orders.add(symbol)

        self.position_risk[symbol] = position_risk

        self.bus.publish("order.request", order)

        self.last_order_time = now

        logger.info(
            "[EXECUTION] order request symbol=%s qty=%s heat=%s",
            symbol,
            qty,
            portfolio_heat
        )
