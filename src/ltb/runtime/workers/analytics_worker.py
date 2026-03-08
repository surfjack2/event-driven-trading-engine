import time

from ltb.system.logger import logger


class AnalyticsWorker:

    def __init__(self, bus):
        self.bus = bus

    def run(self):

        logger.info("[ANALYTICS WORKER STARTED]")

        while True:

            logger.info("[ANALYTICS] updating stats")

            time.sleep(5)


def run_analytics_worker(bus):

    worker = AnalyticsWorker(bus)
    worker.run()
