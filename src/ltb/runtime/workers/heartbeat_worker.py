import time

from ltb.system.logger import logger


class HeartbeatWorker:

    def __init__(self, bus):

        self.bus = bus

        self.last_market_tick = time.time()

        self.bus.subscribe("MARKET_TICK", self.on_market_tick)


    def on_market_tick(self, data):

        self.last_market_tick = time.time()


    def run(self):

        logger.info("[HEARTBEAT WORKER STARTED]")

        while True:

            now = time.time()

            if now - self.last_market_tick > 5:

                logger.error("[KILL SWITCH] market data timeout")

                self.bus.publish(
                    "system.halt",
                    {
                        "reason": "market_data_timeout"
                    }
                )

            time.sleep(1)
