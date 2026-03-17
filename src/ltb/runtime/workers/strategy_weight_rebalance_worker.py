import time
from ltb.system.logger import logger


class StrategyWeightRebalanceWorker:

    def __init__(self, bus):

        self.bus = bus

        )

    def run(self):

        logger.info("[STRATEGY WEIGHT REBALANCE WORKER STARTED]")

        while True:

            if self.performance:
                self.rebalance()

            time.sleep(30)

    def on_performance(self, data):
