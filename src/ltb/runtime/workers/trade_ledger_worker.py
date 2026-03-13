import time
from collections import defaultdict

from ltb.system.logger import logger


class TradeLedgerWorker:

    def __init__(self, bus):

        self.bus = bus

        # 전체 거래 기록
        self.trades = []

        # 전략별 pnl
        self.strategy_pnl = defaultdict(float)

        # 일일 pnl
        self.daily_pnl = 0

        # 열린 포지션 저장
        self.open_positions = {}

        self.bus.subscribe("POSITION_OPENED", self.on_position_open)
        self.bus.subscribe("POSITION_CLOSED", self.on_trade_closed)

    def run(self):

        logger.info("[TRADE LEDGER WORKER STARTED]")

        while True:
            time.sleep(5)

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

            # 실제 시스템에서는 exit_price 받아야 한다
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

        if strategy:
            self.strategy_pnl[strategy] += pnl

        logger.info(
            f"[TRADE LEDGER] trade recorded symbol={symbol} strategy={strategy} pnl={pnl} daily={self.daily_pnl}"
        )

        # 전략 성과 시스템 전달
        self.bus.publish("trade.closed", trade_record)

        if symbol in self.open_positions:
            del self.open_positions[symbol]
