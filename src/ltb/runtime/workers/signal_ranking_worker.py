import time
import math
from collections import deque
from ltb.system.logger import logger


class SignalRankingWorker:

    def __init__(self, bus):

        self.bus = bus

        self.strategy_scores = {}

        self.bus.subscribe(
            self.on_signal
        )

        self.bus.subscribe(
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
                reverse=True
            )

            published = 0

            for data in ranked:

                if score <= 0:

                    continue

                if published >= self.MAX_SIGNALS:

                    continue

                logger.info(
                    symbol,
                    score
                )

                self.bus.publish(
                )

            self.buffer.clear()

            time.sleep(self.RANK_INTERVAL)

    def on_strategy_perf(self, data):

    def on_signal(self, signal):

    def alpha_score(self, signal):
