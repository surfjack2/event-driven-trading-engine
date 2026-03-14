import time
from collections import defaultdict

from ltb.system.logger import logger


class PortfolioOptimizerWorker:

    MAX_TOTAL_POSITIONS = 8
    OPTIMIZER_MAX_SELECTION = 2
    FLUSH_INTERVAL = 1.0

    STRATEGY_QUOTA = {
        "simple_momentum": 0.4,
        "vwap_reclaim": 0.4,
        "vwap_bounce": 0.4
    }

    def __init__(self, bus):

        self.bus = bus

        self.intent_buffer = defaultdict(list)

        self.positions = set()

        self.last_flush = time.time()

        self.bus.subscribe("filtered.intent", self.on_intent)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)

    def run(self):

        logger.info("[PORTFOLIO OPTIMIZER WORKER STARTED]")

        while True:

            now = time.time()

            if now - self.last_flush >= self.FLUSH_INTERVAL:

                self.optimize()

                self.last_flush = now

            time.sleep(0.2)

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        if position > 0:
            self.positions.add(symbol)
        else:
            self.positions.discard(symbol)

    def on_intent(self, signal):

        symbol = signal["symbol"]

        if symbol in self.positions:
            return

        self.intent_buffer[symbol].append(signal)

    def optimize(self):

        if not self.intent_buffer:
            return

        if len(self.positions) >= self.MAX_TOTAL_POSITIONS:
            self.intent_buffer.clear()
            return

        candidates = []

        for symbol, signals in self.intent_buffer.items():

            best = None
            best_score = -999

            for s in signals:

                alpha = s.get("alpha_score", 0)
                weight = s.get("allocation_weight", 0)

                atr = s.get("atr", 0.001)
                price = s.get("price", 1)

                volume = s.get("volume", 0)
                volume_ma = s.get("volume_ma", 1)

                volatility = atr / price
                if volatility <= 0:
                    volatility = 0.001

                liquidity = volume / volume_ma if volume_ma else 1

                momentum = s.get("price_change", 0)

                score = (
                    alpha * 0.6
                    + weight * 0.4
                    + momentum * 80
                    + liquidity * 5
                    - volatility * 120
                )

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

        remaining_slots = self.MAX_TOTAL_POSITIONS - len(self.positions)

        for signal in candidates:

            if remaining_slots <= 0:
                break

            if len(selected) >= self.OPTIMIZER_MAX_SELECTION:
                break

            strategy = signal.get("strategy")

            quota_ratio = self.STRATEGY_QUOTA.get(strategy, 0.5)

            quota = max(
                1,
                int(self.MAX_TOTAL_POSITIONS * quota_ratio)
            )

            if strategy_counts[strategy] >= quota:
                continue

            selected.append(signal)

            strategy_counts[strategy] += 1

            remaining_slots -= 1

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
