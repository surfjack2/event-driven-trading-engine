import time
from ltb.system.logger import logger


class StrategyAllocationWorker:

    MIN_WEIGHT = 0.05
    MAX_WEIGHT = 0.6

    def __init__(self, bus):

        self.bus = bus

        # 기본 weight
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

        # market regime event
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

        logger.info(
            "[ALLOCATION] strategy pnl update %s pnl=%s",
            strategy,
            self.strategy_pnl[strategy]
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

        logger.info(
            "[ALLOCATION] performance update %s %s",
            strategy,
            stats
        )

        self.rebalance()

    def apply_regime_modifier(self, weights):

        if self.market_regime == "bull":

            if "simple_momentum" in weights:
                weights["simple_momentum"] *= 1.3

            if "vwap_reclaim" in weights:
                weights["vwap_reclaim"] *= 0.8

        elif self.market_regime == "sideways":

            if "vwap_reclaim" in weights:
                weights["vwap_reclaim"] *= 1.4

            if "simple_momentum" in weights:
                weights["simple_momentum"] *= 0.7

        elif self.market_regime == "bear":

            for k in weights:
                weights[k] *= 0.5

        return weights

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

        new_allocations = {}

        for strategy, score in scores.items():

            w = score / total

            w = max(self.MIN_WEIGHT, min(self.MAX_WEIGHT, w))

            new_allocations[strategy] = w

        new_allocations = self.apply_regime_modifier(new_allocations)

        for k in new_allocations:
            new_allocations[k] = round(new_allocations[k], 2)

        self.allocations.update(new_allocations)

        logger.info(
            "[ALLOCATION] normalized weights %s regime=%s",
            self.allocations,
            self.market_regime
        )
