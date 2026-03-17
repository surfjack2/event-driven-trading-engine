import time
from collections import defaultdict

from ltb.system.logger import logger


class RankingWorker:

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe(
            self.on_market
        )

    def run(self):

        logger.info("[RANKING WORKER STARTED]")

        while True:

            self.publish_top()

    def on_market(self, data):

        if not symbol or not price or not prev:
            return

        score = 0
