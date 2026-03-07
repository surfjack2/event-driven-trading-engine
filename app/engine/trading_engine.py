import json
import time
from app.execution.order_executor import OrderExecutor
from app.portfolio.position import Position
from app.core.scheduler import EventScheduler
from app.market.market_manager import MarketManager
from app.strategy.strategy_engine import StrategyEngine

class TradingEngine:
    def __init__(self):
        with open("config/settings.json") as f:
            self.settings = json.load(f)

        self.executor = OrderExecutor(self.settings)

        self.market = MarketManager(self.executor)
        self.strategy = StrategyEngine(self.market)

        self.positions = {}

        self.scheduler = EventScheduler()
        self.scheduler.setup(self)

        self.last_monitor_log = 0
        self.last_exit_time = 0
        self.reentry_cooldown = 5

        # 📦 Box 설정
        self.price_history = []
        self.box_period = 60  # POC면 20으로 줄여도 됨

    # ==========================
    # 진입
    # ==========================
    def enter_position(self, symbol, qty):
        buy = self.executor.market_buy(symbol, qty)
        entry_price = buy["price"]
        stop_price = entry_price * 0.975

        pos = Position(symbol, qty, entry_price, stop_price)
        self.positions[symbol] = pos

        print(f"Entered {symbol} at {entry_price}, stop at {stop_price}")

    # ==========================
    # PANIC (최상단 방어)
    # ==========================
    def panic_guard(self, symbol, pos, current_price):
        panic_threshold = pos.entry_price * 0.97

        if current_price <= panic_threshold:
            print("🚨 PANIC TRIGGERED")
            self.exit_position(symbol, pos.qty, reason="PANIC")
            return True

        return False

    # ==========================
    # BOX 계산
    # ==========================
    def calculate_box(self):
        if len(self.price_history) < self.box_period:
            return None, None

        upper = max(self.price_history)
        lower = min(self.price_history)

        return upper, lower

    # ==========================
    # BOX 붕괴
    # ==========================
    def box_guard(self, symbol, pos, current_price):
        upper, lower = self.calculate_box()

        if lower is None:
            return False

        if current_price < lower:
            print("🧱 BOX BREAKDOWN")
            self.exit_position(symbol, pos.qty, reason="BOX_BREAK")
            return True

        return False

    # ==========================
    # 청산
    # ==========================
    def exit_position(self, symbol, qty, reason="STOP"):
        sell = self.executor.market_sell(symbol, qty)
        print(f"EXIT ({reason}):", sell)

        del self.positions[symbol]
        self.last_exit_time = time.time()

    # ==========================
    # 포지션 체크
    # ==========================
    def check_positions(self, current_price):
        for symbol, pos in list(self.positions.items()):

            now = time.time()

            if now - self.last_monitor_log > 5:
                upper, lower = self.calculate_box()
                print(f"[MONITOR]{symbol}|Price:{current_price}|BoxL:{lower}|Stop:{pos.stop_price}")
                self.last_monitor_log = now

            # 1st Panic
            if self.panic_guard(symbol, pos, current_price):
                continue

            # 2nd Box
            if self.box_guard(symbol, pos, current_price):
                continue

            # 3rd Stop
            if current_price <= pos.stop_price:
                self.exit_position(symbol, pos.qty)

    # ==========================
    # TICK
    # ==========================
    def tick(self):

        # scheduler 실행
        self.scheduler.run()

        current_price = self.market.get_price("005930")

        rsi = self.market.get_rsi("005930")
        macd = self.market.get_macd("005930")
        stoch = self.market.get_stochastic("005930")

        print(f"[IND] RSI:{rsi} MACD:{macd} STOCH:{stoch}")

        # 🔥 먼저 체크 (현재값은 박스에 아직 포함 안 됨)
        self.check_positions(current_price)

        # 📦 그 다음 history 저장
        self.price_history.append(current_price)
        if len(self.price_history) > self.box_period:
            self.price_history.pop(0)

        # 진입 로직
        now = time.time()

        symbol = "005930"

        if not self.positions:
            if now - self.last_exit_time > self.reentry_cooldown:

                if self.strategy.check_entry(symbol):
                    self.enter_position(symbol, 1)

    # ==========================
    # Scheduler Events (placeholder)
    # ==========================

    def market_tick(self):
        pass

    def session_check(self):
        pass

    def scanner_update(self):
        pass

    def overnight_eval(self):
        pass
