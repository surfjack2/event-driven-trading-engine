import time
from ltb.system.logger import logger


class StrategyAllocationWorker:

    def __init__(self, bus):

        self.bus = bus

    def run(self):

        logger.info("[STRATEGY ALLOCATION WORKER STARTED]")

        while True:
            time.sleep(5)
