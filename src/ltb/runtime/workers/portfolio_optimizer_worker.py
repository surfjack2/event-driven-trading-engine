import time
from collections import defaultdict

from ltb.system.logger import logger


class PortfolioOptimizerWorker:

    }

    def __init__(self, bus):

    def run(self):

        logger.info("[PORTFOLIO OPTIMIZER WORKER STARTED]")

        while True:

            now = time.time()

            if now - self.last_flush >= self.FLUSH_INTERVAL:

                self.optimize()

                self.last_flush = now

            time.sleep(0.2)

    def on_portfolio_update(self, data):

    def optimize(self):
