import time
from collections import defaultdict

from ltb.system.logger import logger


class TradeLedgerWorker:

    SNAPSHOT_INTERVAL = 3

    def __init__(self, bus, context):

        self.bus = bus
        self.context = context

        self.risk = context.risk_engine

        self.trades = []

        self.strategy_pnl = defaultdict(float)

        self.daily_pnl = 0
        self.weekly_pnl = 0
        self.monthly_pnl = 0

        self.open_positions = {}

        self.last_snapshot = 0

        self.bus.subscribe("POSITION_OPENED", self.on_position_open)
        self.bus.subscribe("POSITION_CLOSED", self.on_trade_closed)

    def run(self):

        logger.info("[TRADE LEDGER WORKER STARTED]")

        while True:

            now = time.time()

            if now - self.last_snapshot > self.SNAPSHOT_INTERVAL:

                self.publish_account_snapshot()

                self.last_snapshot = now

            time.sleep(1)

    def publish_account_snapshot(self):

        capital = self.risk.get_capital()

        equity = capital + self.daily_pnl

        snapshot = {
            "capital": capital,
            "equity": equity,
            "daily_pnl": self.daily_pnl,
            "weekly_pnl": self.weekly_pnl,
            "monthly_pnl": self.monthly_pnl,
            "open_positions": len(self.open_positions),
        }

        self.bus.publish("account.snapshot", snapshot)

    def on_position_open(self, position):

        symbol = position["symbol"]

        self.open_positions[symbol] = position

    def on_trade_closed(self, trade):

        symbol = trade["symbol"]

        entry_price = trade.get("entry_price", 0)
        qty = trade.get("qty", 0)

        open_position = self.open_positions.get(symbol)

        if open_position:

            entry_price = open_position.get("entry_price", entry_price)
            strategy = open_position.get("strategy")

            exit_price = trade.get("exit_price", entry_price)

            pnl = (exit_price - entry_price) * qty

        else:

            strategy = trade.get("strategy")
            pnl = trade.get("pnl", 0)

        trade_record = {
            "symbol": symbol,
            "strategy": strategy,
            "entry_price": entry_price,
            "exit_price": trade.get("exit_price", entry_price),
            "qty": qty,
            "pnl": pnl,
        }

        self.trades.append(trade_record)

        self.daily_pnl += pnl
        self.weekly_pnl += pnl
        self.monthly_pnl += pnl

        self.risk.record_trade(pnl)

        if strategy:
            self.strategy_pnl[strategy] += pnl

        logger.info(
            f"[TRADE LEDGER] trade recorded symbol={symbol} strategy={strategy} pnl={pnl} daily={self.daily_pnl}"
        )

        self.bus.publish("trade.closed", trade_record)

        if symbol in self.open_positions:
            del self.open_positions[symbol]
