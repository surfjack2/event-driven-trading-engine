import time
from ltb.system.logger import logger


class StrategyAllocationWorker:

    MIN_WEIGHT = 0.05
    MAX_WEIGHT = 0.6

    def __init__(self, bus):

        self.bus = bus

        self.allocations = {
            "simple_momentum": 0.4,
            "vwap_reclaim": 0.3,
            "vwap_bounce": 0.3
        }

        self.strategy_enabled = {}

        self.strategy_pnl = {}
        self.strategy_stats = {}

        self.market_regime = "neutral"

        self.bus.subscribe("liquidity.signal", self.on_signal)
        self.bus.subscribe("POSITION_CLOSED", self.on_trade_closed)
        self.bus.subscribe("strategy.performance", self.on_performance)
        self.bus.subscribe("market.regime", self.on_market_regime)

    def run(self):

        logger.info("[STRATEGY ALLOCATION WORKER STARTED]")

        while True:
            time.sleep(5)

    def on_market_regime(self, data):

        regime = data.get("regime")

        if not regime:
            return

        self.market_regime = regime

        logger.info(
            "[ALLOCATION] market regime update %s",
            regime
        )

        self.rebalance()

    def on_signal(self, signal):

        strategy = signal.get("strategy")

        if not self.strategy_enabled.get(strategy, True):

            logger.info(
                "[ALLOCATION] strategy disabled %s",
                strategy
            )
            return

        weight = self.allocations.get(strategy, 0.1)

        signal["allocation_weight"] = weight

        logger.info(
            "[ALLOCATION] passing signal strategy=%s weight=%s regime=%s",
            strategy,
            weight,
            self.market_regime
        )

        self.bus.publish("allocation.signal", signal)

    def on_trade_closed(self, trade):

        strategy = trade.get("strategy")

        if not strategy:
            return

        pnl = trade.get("pnl", 0)

        self.strategy_pnl[strategy] = (
            self.strategy_pnl.get(strategy, 0) + pnl
        )

        if self.strategy_pnl[strategy] < -100000:

            logger.error(
                "[ALLOCATION] disabling strategy %s",
                strategy
            )

            self.strategy_enabled[strategy] = False

            self.bus.publish(
                "strategy.disabled",
                {"strategy": strategy}
            )

    def on_performance(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        self.strategy_stats[strategy] = stats

        self.strategy_enabled.setdefault(strategy, True)

        self.rebalance()

    def rebalance(self):

        scores = {}

        for strategy, stat in self.strategy_stats.items():

            if not self.strategy_enabled.get(strategy, True):
                continue

            score = stat.get("score", 0)

            if score <= 0:
                score = 0.1

            scores[strategy] = score

        if not scores:
            return

        total = sum(scores.values())

        weights = {}

        for strategy, score in scores.items():

            w = score / total

            w = max(self.MIN_WEIGHT, min(self.MAX_WEIGHT, w))

            weights[strategy] = w

        # normalization 재수행
        norm = sum(weights.values())

        for k in weights:

            weights[k] = round(weights[k] / norm, 2)

        self.allocations.update(weights)

        logger.info(
            "[ALLOCATION] normalized weights %s regime=%s",
            self.allocations,
            self.market_regime
        )
