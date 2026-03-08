import time

from ltb.system.logger import logger


class RiskWorker:

    def __init__(self, bus):
        self.bus = bus

    def run(self):

        logger.info("[RISK WORKER STARTED]")

        while True:

            logger.info("[RISK] monitoring")

            time.sleep(3)


def run_risk_worker(bus):

    worker = RiskWorker(bus)
    worker.run()
