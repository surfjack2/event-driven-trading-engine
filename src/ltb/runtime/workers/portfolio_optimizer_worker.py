import time
from collections import defaultdict

from ltb.system.logger import logger


class PortfolioOptimizerWorker:

    MAX_PORTFOLIO_SIZE = 5
    FLUSH_INTERVAL = 1.0

    STRATEGY_QUOTA = {
        "simple_momentum": 0.4,
        "vwap_reclaim": 0.4,
        "vwap_bounce": 0.4
    }

    def __init__(self, bus):

        self.bus = bus

        self.intent_buffer = defaultdict(list)

        self.last_flush = time.time()

        self.bus.subscribe("filtered.intent", self.on_intent)

    def run(self):

        logger.info("[PORTFOLIO OPTIMIZER WORKER STARTED]")

        while True:

            now = time.time()

            if now - self.last_flush >= self.FLUSH_INTERVAL:

                self.optimize()

                self.last_flush = now

            time.sleep(0.2)

    def on_intent(self, signal):

        symbol = signal["symbol"]

        self.intent_buffer[symbol].append(signal)

    def optimize(self):

        if not self.intent_buffer:
            return

        candidates = []

        for symbol, signals in self.intent_buffer.items():

            best = None
            best_score = -999

            for s in signals:

                weight = s.get("allocation_weight", 0)
                atr = s.get("atr", 0.001)
                price = s.get("price", 1)

                volatility = atr / price

                if volatility <= 0:
                    volatility = 0.001

                signal_strength = weight

                score = signal_strength / volatility

                if score > best_score:

                    best = s
                    best_score = score

            if best:
                best["optimizer_score"] = best_score
                candidates.append(best)

        if not candidates:

            self.intent_buffer.clear()
            return

        candidates.sort(
            reverse=True,
            key=lambda s: s.get("optimizer_score", 0)
        )

        selected = []

        strategy_counts = defaultdict(int)

        for signal in candidates:

            strategy = signal.get("strategy")

            quota_ratio = self.STRATEGY_QUOTA.get(strategy, 0.5)

            quota = max(
                1,
                int(self.MAX_PORTFOLIO_SIZE * quota_ratio)
            )

            if strategy_counts[strategy] >= quota:
                continue

            selected.append(signal)

            strategy_counts[strategy] += 1

            if len(selected) >= self.MAX_PORTFOLIO_SIZE:
                break

        for signal in selected:

            logger.info(
                "[PORTFOLIO OPT] selected %s strategy=%s score=%.2f",
                signal["symbol"],
                signal.get("strategy"),
                signal.get("optimizer_score", 0)
            )

            self.bus.publish(
                "optimized.signal",
                signal
            )

        self.intent_buffer.clear()
