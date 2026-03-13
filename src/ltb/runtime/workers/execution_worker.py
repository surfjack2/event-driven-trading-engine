import time
import threading

from ltb.system.logger import logger
from ltb.risk.risk_engine import RiskEngine
from ltb.risk.position_sizer import PositionSizer


class ExecutionWorker:

    MAX_GLOBAL_POSITIONS = 5
    ATR_MULTIPLIER = 2

    GLOBAL_ORDER_INTERVAL = 0.3

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}
        self.pending_orders = set()

        self.risk = RiskEngine()
        self.sizer = PositionSizer()

        self.last_signal_time = {}
        self.last_global_order_time = 0

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

            # pending order 해제
            self.pending_orders.discard(symbol)


    def on_signal(self, signal):

        symbol = signal["symbol"]
        price = signal["price"]
        strategy = signal.get("strategy")
        atr = signal.get("atr", 0)

        # allocation weight (StrategyAllocationWorker에서 전달)
        weight = signal.get("allocation_weight", 1.0)

        now = time.time()

        with self.lock:

            # symbol cooldown
            last = self.last_signal_time.get(symbol, 0)

            if now - last < 5:
                logger.debug("[EXECUTION] cooldown active %s", symbol)
                return

            # global rate limit
            if now - self.last_global_order_time < self.GLOBAL_ORDER_INTERVAL:
                logger.debug("[EXECUTION] global rate limit active")
                return

            self.last_signal_time[symbol] = now

            # 이미 보유 / pending 차단
            if symbol in self.positions or symbol in self.pending_orders:

                logger.info(
                    "[POSITION GATE] already holding or pending %s",
                    symbol
                )

                return

            # 글로벌 포지션 제한
            if len(self.positions) >= self.MAX_GLOBAL_POSITIONS:

                logger.warning(
                    "[EXECUTION] global position limit reached"
                )

                return

            # stop price 계산
            if atr > 0:
                stop_price = price - atr * self.ATR_MULTIPLIER
            else:
                stop_price = price * 0.92

            # position sizing (weight 반영)
            qty = self.sizer.calculate(price, stop_price, weight)

            if qty <= 0:
                logger.warning("[EXECUTION] qty calculated as 0")
                return

            # risk engine
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

            # pending 등록
            self.pending_orders.add(symbol)

            # 글로벌 주문 시간 업데이트
            self.last_global_order_time = now

        # lock 밖에서 publish
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
