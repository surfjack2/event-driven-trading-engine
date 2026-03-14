import time
from collections import deque
import statistics
from ltb.system.logger import logger


class SignalRankingWorker:

    MAX_SIGNALS = 5
    RANK_INTERVAL = 1
    BUFFER_SIZE = 200

    # 🔴 normalization window
    NORMALIZE_WINDOW = 100

    def __init__(self, bus):

        self.bus = bus

        self.buffer = deque(maxlen=self.BUFFER_SIZE)

        # 🔴 alpha history
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

        # 🔴 history 저장
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

        score = 0

        if price and ema:
            momentum = (price - ema) / ema
            score += momentum * 200

        if price and vwap:
            vwap_gap = (price - vwap) / vwap
            score += vwap_gap * 150

        score += volume_ratio * 25

        score += price_change * 300

        if atr and price:
            vol_factor = atr / price
            score -= vol_factor * 120

        return score

    # 🔴 alpha normalization
    def normalize_alpha(self, alpha):

        if len(self.alpha_history) < 10:
            return alpha

        mean = statistics.mean(self.alpha_history)
        stdev = statistics.stdev(self.alpha_history)

        if stdev == 0:
            return alpha

        z = (alpha - mean) / stdev

        # clamp extreme values
        z = max(-3, min(3, z))

        return z
