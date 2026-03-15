import time
from collections import deque
import statistics
from ltb.system.logger import logger


class SignalRankingWorker:

    MAX_SIGNALS = 5
    RANK_INTERVAL = 1
    BUFFER_SIZE = 200
    NORMALIZE_WINDOW = 200

    def __init__(self, bus):

        self.bus = bus

        self.buffer = deque(maxlen=self.BUFFER_SIZE)
        self.alpha_history = deque(maxlen=self.NORMALIZE_WINDOW)

        self.strategy_scores = {}

        self.bus.subscribe(
            "persistent.signal",
            self.on_signal
        )

        self.bus.subscribe(
            "strategy.performance",
            self.on_strategy_perf
        )

    def run(self):

        logger.info("[SIGNAL RANKING WORKER STARTED]")

        while True:

            if not self.buffer:
                time.sleep(self.RANK_INTERVAL)
                continue

            ranked = sorted(
                self.buffer,
                key=lambda x: x["score"],
                reverse=True
            )

            published = 0

            for data in ranked:

                score = data["score"]

                if score <= 0:
                    continue

                signal = data["signal"]

                logger.info(
                    "[RANKING] passed %s score=%.3f",
                    signal["symbol"],
                    score
                )

                self.bus.publish(
                    "ranked.signal",
                    signal
                )

                published += 1

                if published >= self.MAX_SIGNALS:
                    break

            self.buffer.clear()

            time.sleep(self.RANK_INTERVAL)

    def on_strategy_perf(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        score = stats.get("score", 1.0)

        self.strategy_scores[strategy] = score

    def on_signal(self, signal):

        raw_alpha = self.alpha_score(signal)

        self.alpha_history.append(raw_alpha)

        norm_alpha = self.normalize_alpha(raw_alpha)

        strategy = signal.get("strategy")

        perf_score = self.strategy_scores.get(strategy, 1.0)

        final_score = norm_alpha * perf_score

        signal["alpha_score"] = norm_alpha
        signal["final_score"] = final_score

        self.buffer.append({
            "score": final_score,
            "signal": signal
        })

    def alpha_score(self, signal):

        price = signal.get("price")
        ema = signal.get("ema")
        vwap = signal.get("vwap")

        volume_ratio = signal.get("volume_ratio", 0)
        price_change = signal.get("price_change", 0)

        atr = signal.get("atr")

        if not price:
            return 0

        trend = 0

        if ema:
            trend += (price - ema) / ema

        if vwap:
            trend += (price - vwap) / vwap

        trend_score = trend * 200

        momentum_score = price_change * 300

        liquidity_score = volume_ratio * 30

        volatility_penalty = 0

        if atr and price:

            vol = atr / price
            volatility_penalty = vol * 150

        score = (
            trend_score
            + momentum_score
            + liquidity_score
            - volatility_penalty
        )

        return score

    def normalize_alpha(self, alpha):

        if len(self.alpha_history) < 20:
            return alpha

        mean = statistics.mean(self.alpha_history)
        stdev = statistics.stdev(self.alpha_history)

        if stdev == 0:
            return alpha

        z = (alpha - mean) / stdev

        z = max(-3, min(3, z))

        return z
