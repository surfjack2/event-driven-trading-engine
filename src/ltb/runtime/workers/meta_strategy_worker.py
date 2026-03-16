import time
from ltb.system.logger import logger


class MetaStrategyWorker:

    DISABLE_SCORE = -0.05
    ENABLE_SCORE = 0.15

    def __init__(self, bus):

        self.bus = bus

        self.strategy_stats = {}
        self.strategy_enabled = {}

        self.market_regime = "neutral"
        self.liquidity_regime = "NORMAL"

        self.bus.subscribe("strategy.performance", self.on_performance)
        self.bus.subscribe("market.regime", self.on_market_regime)
        self.bus.subscribe("market.liquidity_regime", self.on_liquidity_regime)

    def run(self):

        logger.info("[META STRATEGY WORKER STARTED]")

        while True:

            self.evaluate()

            time.sleep(10)

    def on_performance(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        self.strategy_stats[strategy] = stats

        self.strategy_enabled.setdefault(strategy, True)

    def on_market_regime(self, data):

        regime = data.get("regime")

        if regime:
            self.market_regime = regime

    def on_liquidity_regime(self, data):

        regime = data.get("regime")

        if regime:
            self.liquidity_regime = regime

    def evaluate(self):

        if not self.strategy_stats:
            return

        for strategy, stats in self.strategy_stats.items():

            score = stats.get("score", 0)
            enabled = self.strategy_enabled.get(strategy, True)

            # 전략 비활성 조건
            if enabled and score < self.DISABLE_SCORE:

                logger.warning(
                    "[META STRATEGY] disabling %s score=%.3f",
                    strategy,
                    score
                )

                self.strategy_enabled[strategy] = False

                self.bus.publish(
                    "strategy.disabled",
                    {"strategy": strategy}
                )

            # 전략 재활성 조건
            elif not enabled and score > self.ENABLE_SCORE:

                logger.info(
                    "[META STRATEGY] enabling %s score=%.3f",
                    strategy,
                    score
                )

                self.strategy_enabled[strategy] = True

                self.bus.publish(
                    "strategy.enabled",
                    {"strategy": strategy}
                )
