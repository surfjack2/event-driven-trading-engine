import time
import logging

from ltb.data.universe_builder import UniverseBuilder
from ltb.data.market_manager import MarketManager
from ltb.strategy.strategy_scanner import StrategyScanner
from ltb.execution.execution_engine import ExecutionEngine
from ltb.risk.position_size_manager import PositionSizeManager
from ltb.risk.portfolio_risk_manager import PortfolioRiskManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/engine.log"),
        logging.StreamHandler()
    ]
)


class TradingEngine:

    def __init__(self):

        self.logger = logging.getLogger("engine")

        self.universe_builder = UniverseBuilder()
        self.universe = self.universe_builder.build()

        self.market = MarketManager(self.universe)

        self.scanner = StrategyScanner(self.market)

        self.execution = ExecutionEngine(self)

        self.position_sizer = PositionSizeManager(self)
        self.portfolio_risk = PortfolioRiskManager(self)

        self.positions = {}

        self.max_positions = 5

        self.cooldown = {}
        self.cooldown_seconds = 60

        self.last_universe_update = time.time()

        self.logger.info("=== KIS TRADER ENGINE STARTED ===")

    def tick(self):

        now = time.time()

        if now - self.last_universe_update > 30:

            self.universe = self.universe_builder.build()

            self.market.set_universe(self.universe)

            self.last_universe_update = now

        self.monitor_positions()

        candidates = self.scanner.scan(self.universe)

        self.logger.info(f"Scanner found {len(candidates)} candidates")

        for symbol in candidates:

            if len(self.positions) >= self.max_positions:
                return

            if symbol in self.positions:
                continue

            if symbol in self.cooldown:
                if now - self.cooldown[symbol] < self.cooldown_seconds:
                    continue

            price = self.market.get_price(symbol)

            if price is None:
                continue

            stop = price * 0.92

            qty = self.position_sizer.calculate_qty(price)

            risk = abs(price - stop) * qty

            if not self.portfolio_risk.can_open_position(risk):
                continue

            self.execution.enter(symbol, qty, price, stop)

    def monitor_positions(self):

        for symbol, position in list(self.positions.items()):

            price = self.market.get_price(symbol)

            if price is None:
                continue

            stop = position["stop"]
            entry = position["entry"]

            self.logger.info(f"[MONITOR] {symbol} price={price} stop={stop}")

            if price > entry:

                new_stop = price * 0.95

                if new_stop > stop:
                    position["stop"] = new_stop

            if price < position["stop"]:

                self.logger.info(f"ATR STOP {symbol} entry={entry} price={price}")

                self.execution.exit(symbol)

                self.cooldown[symbol] = time.time()
