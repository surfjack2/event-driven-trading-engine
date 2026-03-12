import time
from ltb.system.logger import logger


class StrategyAllocationWorker:

    def __init__(self, bus):

        self.bus = bus

        # 전략별 자본 배분
        self.allocations = {
            "simple_momentum": 0.3,
            "volume_breakout": 0.3,
            "turtle": 0.4,
        }

        # 전략 상태
        self.strategy_enabled = {
            "simple_momentum": True,
            "volume_breakout": True,
            "turtle": True,
        }

        # 전략 누적 pnl
        self.strategy_pnl = {}

        # 전략 성과 통계
        self.strategy_stats = {}

        self.bus.subscribe("strategy.signal", self.on_signal)
        self.bus.subscribe("POSITION_CLOSED", self.on_trade_closed)
        self.bus.subscribe("strategy.performance", self.on_performance)

    def run(self):

        logger.info("[STRATEGY ALLOCATION WORKER STARTED]")

        while True:
            time.sleep(5)

    def on_signal(self, signal):

        strategy = signal.get("strategy")

        if not self.strategy_enabled.get(strategy, True):

            logger.info(
                f"[ALLOCATION] strategy disabled {strategy}"
            )
            return

        weight = self.allocations.get(strategy, 0.1)

        signal["allocation_weight"] = weight

        logger.info(
            f"[ALLOCATION] passing signal strategy={strategy} weight={weight}"
        )

        self.bus.publish("allocation.signal", signal)

    def on_trade_closed(self, trade):

        strategy = trade.get("strategy")

        if not strategy:
            return

        pnl = trade.get("pnl", 0)

        current = self.strategy_pnl.get(strategy, 0)

        self.strategy_pnl[strategy] = current + pnl

        logger.info(
            f"[ALLOCATION] strategy pnl update {strategy} pnl={self.strategy_pnl[strategy]}"
        )

        # 손실 전략 자동 OFF
        if self.strategy_pnl[strategy] < -100000:

            logger.error(
                f"[ALLOCATION] disabling strategy {strategy}"
            )

            self.strategy_enabled[strategy] = False

    def on_performance(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        self.strategy_stats[strategy] = stats

        logger.info(
            f"[ALLOCATION] performance update {strategy} {stats}"
        )

        self.rebalance()

    def rebalance(self):

        if not self.strategy_stats:
            return

        scores = {}

        for strategy, stat in self.strategy_stats.items():

            if not self.strategy_enabled.get(strategy, True):
                continue

            pf = stat.get("profit_factor", 0)

            if pf <= 0:
                pf = 0.1

            scores[strategy] = pf

        total = sum(scores.values())

        if total == 0:
            return

        for strategy in scores:

            new_weight = scores[strategy] / total

            self.allocations[strategy] = round(new_weight, 2)

        logger.info(f"[ALLOCATION] new weights {self.allocations}")
