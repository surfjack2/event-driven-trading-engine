import time
from collections import deque
from ltb.system.logger import logger


class SignalRankingWorker:

    MAX_SIGNALS = 5
    RANK_INTERVAL = 1
    BUFFER_SIZE = 200

    def __init__(self, bus):

        self.bus = bus

        self.buffer = deque(maxlen=self.BUFFER_SIZE)

        self.bus.subscribe(
            "dedup.signal",
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
                    "[RANKING] passed %s score=%.2f",
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

        strategy = signal.get("strategy")

        if strategy == "simple_momentum":
            score = self.score_momentum(signal)

        elif strategy == "vwap_reclaim":
            score = self.score_vwap_reclaim(signal)

        elif strategy == "vwap_bounce":
            score = self.score_vwap_bounce(signal)

        else:
            score = 0

        self.buffer.append({
            "score": score,
            "signal": signal
        })

    def score_momentum(self, signal):

        price = signal.get("price")
        ema = signal.get("ema")
        volume = signal.get("volume")
        volume_ma = signal.get("volume_ma")
        rsi = signal.get("rsi")

        score = 0

        if ema and price:
            disparity = (price - ema) / ema
            score += disparity * 120

        if volume and volume_ma:
            score += (volume / volume_ma) * 10

        if rsi:
            score += rsi / 10

        return score

    def score_vwap_reclaim(self, signal):

        price = signal.get("price")
        vwap = signal.get("vwap")
        volume = signal.get("volume")
        volume_ma = signal.get("volume_ma")
        atr = signal.get("atr")

        score = 0

        if vwap and price:
            score += ((price - vwap) / vwap) * 150

        if volume and volume_ma:
            score += (volume / volume_ma) * 15

        if atr and price:
            score += (atr / price) * 200

        return score

    def score_vwap_bounce(self, signal):

        price = signal.get("price")
        vwap = signal.get("vwap")
        volume = signal.get("volume")
        volume_ma = signal.get("volume_ma")

        score = 0

        if vwap and price:
            score += abs(price - vwap) / vwap * 120

        if volume and volume_ma:
            score += (volume / volume_ma) * 10

        return score
