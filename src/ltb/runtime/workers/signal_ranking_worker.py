import time
import math
from collections import deque
from ltb.system.logger import logger


class SignalRankingWorker:

    MAX_SIGNALS = 5
    RANK_INTERVAL = 1
    BUFFER_SIZE = 200

    def __init__(self, bus):

        self.bus = bus

        self.buffer = deque(maxlen=self.BUFFER_SIZE)

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
                signal = data["signal"]

                symbol = signal.get("symbol")
                strategy = signal.get("strategy")

                if score <= 0:

                    self.bus.publish(
                        "ranking.reject",
                        {
                            "symbol": symbol,
                            "strategy": strategy,
                            "score": score,
                            "reason": "score<=0"
                        }
                    )

                    continue

                if published >= self.MAX_SIGNALS:

                    self.bus.publish(
                        "ranking.reject",
                        {
                            "symbol": symbol,
                            "strategy": strategy,
                            "score": score,
                            "reason": "topN_limit"
                        }
                    )

                    continue

                logger.info(
                    "[RANKING PASS] %s score=%.3f",
                    symbol,
                    score
                )

                self.bus.publish(
                    "ranking.pass",
                    {
                        "symbol": symbol,
                        "strategy": strategy,
                        "score": score
                    }
                )

                self.bus.publish(
                    "ranked.signal",
                    signal
                )

                published += 1

            self.buffer.clear()

            time.sleep(self.RANK_INTERVAL)

    def on_strategy_perf(self, data):

        strategy = data["strategy"]
        stats = data["stats"]

        score = stats.get("score", 1.0)

        self.strategy_scores[strategy] = score

    def on_signal(self, signal):

        raw_alpha = self.alpha_score(signal)

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
        atr = signal.get("atr")

        features = signal.get("features", {})

        volume_ratio = features.get("volume_ratio", 0)
        price_change = features.get("price_change", 0)
        vwap_distance = features.get("vwap_distance", 0)

        if not price:
            return 0

        trend_score = vwap_distance * 600
        momentum_score = price_change * 1000
        liquidity_score = volume_ratio * 80

        volatility_penalty = 0

        if atr and price:

            vol = atr / price
            volatility_penalty = vol * 80

        raw = (
            trend_score
            + momentum_score
            + liquidity_score
            - volatility_penalty
        )

        return raw

    def normalize_alpha(self, alpha):

        # 🔴 scale 확장 (기관형 방식)
        scale = 80

        norm = math.tanh(alpha / scale)

        # 🔴 extreme alpha soft clipping
        if norm > 0.9:
            norm = 0.9 + (norm - 0.9) * 0.2

        if norm < -0.9:
            norm = -0.9 + (norm + 0.9) * 0.2

        return norm
