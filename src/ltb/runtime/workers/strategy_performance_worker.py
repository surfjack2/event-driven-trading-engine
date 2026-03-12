import time
from collections import defaultdict

from ltb.system.logger import logger


class StrategyPerformanceWorker:

    def __init__(self, bus):

        self.bus = bus

        # 전략별 거래 기록
        self.trades = defaultdict(list)

        # 전략별 통계
        self.stats = {}

        # 이벤트 수정
        self.bus.subscribe("POSITION_CLOSED", self.on_trade_closed)

    def run(self):

        logger.info("[STRATEGY PERFORMANCE WORKER STARTED]")

        while True:

            self.compute_stats()

            time.sleep(10)

    def on_trade_closed(self, trade):

        strategy = trade.get("strategy")

        if not strategy:
            return

        self.trades[strategy].append(trade)

    def compute_stats(self):

        for strategy, trades in self.trades.items():

            if not trades:
                continue

            pnl_list = [t["pnl"] for t in trades]

            total = sum(pnl_list)

            wins = len([p for p in pnl_list if p > 0])
            losses = len([p for p in pnl_list if p <= 0])

            win_rate = wins / len(pnl_list) if pnl_list else 0

            profit = sum([p for p in pnl_list if p > 0])
            loss = abs(sum([p for p in pnl_list if p < 0]))

            profit_factor = profit / loss if loss > 0 else 0

            self.stats[strategy] = {
                "trades": len(pnl_list),
                "pnl": total,
                "win_rate": win_rate,
                "profit_factor": profit_factor,
            }

            logger.info(
                f"[STRATEGY PERF] {strategy} trades={len(pnl_list)} pnl={total} win_rate={win_rate:.2f} pf={profit_factor:.2f}"
            )

            self.bus.publish(
                "strategy.performance",
                {
                    "strategy": strategy,
                    "stats": self.stats[strategy]
                }
            )
