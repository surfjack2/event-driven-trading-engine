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

        self.bus.subscribe(
            "persistent.signal",
            self.on_signal
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

    def on_signal(self, signal):

        raw_alpha = self.alpha_score(signal)

        self.alpha_history.append(raw_alpha)

        norm_alpha = self.normalize_alpha(raw_alpha)

        signal["alpha_score"] = norm_alpha

        self.buffer.append({
            "score": norm_alpha,
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

        score = 0

        # -------------------------
        # Trend alignment
        # -------------------------

        trend = 0

        if ema:
            trend += (price - ema) / ema

        if vwap:
            trend += (price - vwap) / vwap

        trend_score = trend * 200

        # -------------------------
        # Momentum
        # -------------------------

        momentum_score = price_change * 300

        # -------------------------
        # Liquidity pressure
        # -------------------------

        liquidity_score = volume_ratio * 30

        # -------------------------
        # Volatility penalty
        # -------------------------

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
