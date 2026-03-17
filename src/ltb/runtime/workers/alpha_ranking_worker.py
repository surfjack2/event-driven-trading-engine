import time
from collections import defaultdict

from ltb.system.logger import logger


class AlphaRankingWorker:

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe(
            self.on_signal
        )

    def run(self):

        logger.info("[ALPHA RANKING WORKER STARTED]")

        while True:

            if not self.scores:
                continue

            ranked = sorted(
                self.scores.items(),
            )

            )

            self.scores.clear()

            time.sleep(self.RANK_INTERVAL)

    def on_signal(self, data):

        symbol = data.get("symbol")

        if not symbol:
            return
