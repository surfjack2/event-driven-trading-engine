import time
from ltb.system.logger import logger


class StrategyWeightRebalanceWorker:

    def __init__(self, bus):

        self.bus = bus

        # 전략 성과 저장
        self.performance = {}

        self.bus.subscribe(
            "strategy.performance",
            self.on_performance
        )

    def run(self):

        logger.info("[STRATEGY WEIGHT REBALANCE WORKER STARTED]")

        while True:

            if self.performance:
                self.rebalance()

            time.sleep(30)

    def on_performance(self, data):

        strategy = data.get("strategy")
        stats = data.get("stats", {})

        if not strategy:
            return

        self.performance[strategy] = stats

    def rebalance(self):

        scores = {}

        for strategy, stats in self.performance.items():

            pnl = stats.get("pnl", 0)
            pf = stats.get("profit_factor", 0)
            win = stats.get("win_rate", 0)

            score = pnl * 0.5 + pf * 0.3 + win * 0.2

            scores[strategy] = max(score, 0)

        total = sum(scores.values())

        if total == 0:
            return

        allocations = {}

        for strategy, score in scores.items():

            weight = score / total

            allocations[strategy] = round(weight, 2)

        logger.info(
            f"[REBALANCE] new allocations {allocations}"
        )

        self.bus.publish(
            "strategy.allocation.update",
            allocations
        )
