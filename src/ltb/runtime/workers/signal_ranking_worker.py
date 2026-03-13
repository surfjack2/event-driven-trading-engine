import time
from ltb.system.logger import logger


class SignalRankingWorker:

    MAX_SIGNALS = 5
    RANK_INTERVAL = 1

    def __init__(self, bus):

        self.bus = bus
        self.buffer = {}

        self.bus.subscribe(
            "strategy.signal",
            self.on_signal
        )

    def run(self):

        logger.info("[SIGNAL RANKING WORKER STARTED]")

        while True:

            if not self.buffer:
                time.sleep(self.RANK_INTERVAL)
                continue

            ranked = sorted(
                self.buffer.items(),
                key=lambda x: x[1]["score"],
                reverse=True
            )

            published = 0

            for symbol, data in ranked:

                score = data["score"]

                if score <= 0:
                    continue

                logger.info(
                    "[RANKING] passed %s score=%.2f",
                    symbol,
                    score
                )

                self.bus.publish(
                    "ranked.signal",
                    data["signal"]
                )

                published += 1

                if published >= self.MAX_SIGNALS:
                    break

            self.buffer.clear()

            time.sleep(self.RANK_INTERVAL)

    def on_signal(self, signal):

        symbol = signal["symbol"]

        price = signal["price"]
        vwap = signal.get("vwap")
        volume = signal.get("volume")
        volume_ma = signal.get("volume_ma")
        atr = signal.get("atr")
        rsi = signal.get("rsi")
        ema = signal.get("ema")

        score = 0

        if vwap:
            score += ((price - vwap) / vwap) * 40

        if ema:
            score += ((price - ema) / ema) * 60

        if volume and volume_ma and volume_ma > 0:
            score += (volume / volume_ma) * 5

        if atr:
            score += (atr / price) * 100

        if rsi:
            score += rsi / 20

        self.buffer[symbol] = {
            "score": score,
            "signal": signal
        }
