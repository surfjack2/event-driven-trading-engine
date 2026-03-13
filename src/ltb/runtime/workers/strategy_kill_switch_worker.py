import time

from ltb.system.logger import logger


class StrategyKillSwitchWorker:

    MIN_TRADES = 20
    MIN_PROFIT_FACTOR = 0.8
    MIN_WIN_RATE = 0.35

    COOLDOWN_SECONDS = 1800

    def __init__(self, bus):

        self.bus = bus

        self.strategy_stats = {}
        self.disabled_strategies = {}

        self.bus.subscribe(
            "strategy.performance",
            self.on_strategy_performance
        )

    def run(self):

        logger.info("[STRATEGY KILL SWITCH WORKER STARTED]")

        while True:

            self._recover_strategies()

            time.sleep(5)

    def on_strategy_performance(self, data):

        strategy = data["strategy"]

        trades = data.get("trades", 0)
        win_rate = data.get("win_rate", 0)
        profit_factor = data.get("profit_factor", 0)

        self.strategy_stats[strategy] = data

        if trades < self.MIN_TRADES:
            return

        if profit_factor < self.MIN_PROFIT_FACTOR or win_rate < self.MIN_WIN_RATE:

            if strategy not in self.disabled_strategies:

                self.disabled_strategies[strategy] = time.time()

                logger.warning(
                    "[STRATEGY KILL] %s disabled trades=%s win_rate=%.2f pf=%.2f",
                    strategy,
                    trades,
                    win_rate,
                    profit_factor
                )

                self.bus.publish(
                    "strategy.disabled",
                    {
                        "strategy": strategy
                    }
                )

    def _recover_strategies(self):

        now = time.time()

        for strategy, disabled_time in list(self.disabled_strategies.items()):

            if now - disabled_time > self.COOLDOWN_SECONDS:

                logger.info(
                    "[STRATEGY RECOVER] %s re-enabled",
                    strategy
                )

                del self.disabled_strategies[strategy]

                self.bus.publish(
                    "strategy.enabled",
                    {
                        "strategy": strategy
                    }
                )
