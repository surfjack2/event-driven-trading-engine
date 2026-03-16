import time
from ltb.system.logger import logger


class StrategyAllocationWorker:

    MIN_WEIGHT = 0.05
    MAX_WEIGHT = 0.6

    # 🔴 안정화 파라미터
    REBALANCE_INTERVAL = 10
    MIN_CHANGE = 0.03

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
        self.liquidity_regime = "NORMAL"

        self.last_rebalance = 0

        # 🔴 pipeline 연결
        self.bus.subscribe("ranked.signal", self.on_signal)

        self.bus.subscribe("POSITION_CLOSED", self.on_trade_closed)
        self.bus.subscribe("strategy.performance", self.on_performance)

        self.bus.subscribe("market.regime", self.on_market_regime)
        self.bus.subscribe("market.liquidity_regime", self.on_liquidity_regime)

    def run(self):

        logger.info("[STRATEGY ALLOCATION WORKER STARTED]")

        while True:
            time.sleep(5)

    def on_market_regime(self, data):

        regime = data.get("regime")

        if not regime:
            return

        self.market_regime = regime

        logger.info("[ALLOCATION] market regime update %s", regime)

        self.rebalance()

    def on_liquidity_regime(self, data):

        regime = data.get("regime")

        if not regime:
            return

        self.liquidity_regime = regime

        logger.info("[ALLOCATION] liquidity regime update %s", regime)

        self.rebalance()

    def on_signal(self, signal):

        strategy = signal.get("strategy")

        if not self.strategy_enabled.get(strategy, True):
            return

        weight = self.allocations.get(strategy, 0.1)

        signal["allocation_weight"] = weight

        logger.info(
            "[ALLOCATION] signal strategy=%s weight=%s regime=%s liquidity=%s",
            strategy,
            weight,
            self.market_regime,
            self.liquidity_regime
        )

        # 🔴 optimizer pipeline
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

            logger.error("[ALLOCATION] disabling strategy %s", strategy)

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

        now = time.time()

        # 🔴 throttle
        if now - self.last_rebalance < self.REBALANCE_INTERVAL:
            return

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

        new_weights = {}

        for strategy, score in scores.items():

            w = score / total

            w = max(self.MIN_WEIGHT, min(self.MAX_WEIGHT, w))

            new_weights[strategy] = w

        norm = sum(new_weights.values())

        for k in new_weights:
            new_weights[k] = round(new_weights[k] / norm, 2)

        # 🔴 변화량 체크
        changed = False

        for k, v in new_weights.items():

            old = self.allocations.get(k, 0)

            if abs(old - v) > self.MIN_CHANGE:
                changed = True
                break

        if not changed:
            return

        self.allocations.update(new_weights)

        self.last_rebalance = now

        logger.info(
            "[ALLOCATION] normalized weights %s trend=%s liquidity=%s",
            self.allocations,
            self.market_regime,
            self.liquidity_regime
        )
