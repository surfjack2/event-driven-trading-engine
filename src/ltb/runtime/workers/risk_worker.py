import time

from ltb.system.logger import logger


class RiskWorker:

    def __init__(self, bus):

        self.bus = bus
        self.halted = False

        # KillSwitch 이벤트 구독
        self.bus.subscribe("system.halt", self.on_system_halt)


    def on_system_halt(self, data):

        reason = data.get("reason")

        logger.error(f"[KILL SWITCH] system halt triggered reason={reason}")

        self.halted = True

        # 모든 포지션 청산 요청
        self.bus.publish(
            "risk.close_all",
            {
                "reason": reason
            }
        )


    def run(self):

        logger.info("[RISK WORKER STARTED]")

        while True:

            if self.halted:

                logger.error("[RISK] trading halted")

            else:

                logger.info("[RISK] monitoring")

            time.sleep(3)


def run_risk_worker(bus):

    worker = RiskWorker(bus)
    worker.run()
