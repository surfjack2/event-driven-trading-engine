import time

from ltb.system.logger import logger


class HeartbeatWorker:

    def __init__(self, bus):

        self.bus = bus

        # 마지막 market tick 시간
        self.last_market_tick = time.time()

        # heartbeat interval
        self.heartbeat_interval = 10

        # market data timeout
        self.market_timeout = 5

        # 마지막 heartbeat 로그
        self.last_heartbeat = time.time()

        self.bus.subscribe("MARKET_TICK", self.on_market_tick)

    def on_market_tick(self, data):

        self.last_market_tick = time.time()

    def run(self):

        logger.info("[HEARTBEAT WORKER STARTED]")

        while True:

            now = time.time()

            # -----------------------------
            # market data watchdog
            # -----------------------------

            if now - self.last_market_tick > self.market_timeout:

                logger.error("[KILL SWITCH] market data timeout")

                self.bus.publish(
                    "system.halt",
                    {
                        "reason": "market_data_timeout"
                    }
                )

            # -----------------------------
            # engine heartbeat
            # -----------------------------

            if now - self.last_heartbeat > self.heartbeat_interval:

                logger.info("[HEARTBEAT] engine alive")

                # system heartbeat
                self.bus.publish(
                    "system.heartbeat",
                    {
                        "timestamp": now
                    }
                )

                # 🔴 CLI worker health용 heartbeat
                self.bus.publish(
                    "worker.heartbeat",
                    {
                        "worker": "heartbeat_worker",
                        "timestamp": now
                    }
                )

                self.last_heartbeat = now

            time.sleep(1)
