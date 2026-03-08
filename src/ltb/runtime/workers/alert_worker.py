import time

from ltb.system.logger import logger


class AlertWorker:

    def __init__(self, bus):
        self.bus = bus

    def run(self):

        logger.info("[ALERT WORKER STARTED]")

        while True:

            logger.info("[ALERT] monitoring events")

            time.sleep(4)


def run_alert_worker(bus):

    worker = AlertWorker(bus)
    worker.run()
