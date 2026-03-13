import time
from ltb.system.logger import logger


class KillSwitchWorker:

    def __init__(self, bus):

        self.bus = bus

        self.halted = False

        self.bus.subscribe(
            "system.halt",
            self.on_halt
        )

    def run(self):

        logger.info("[KILL SWITCH WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_halt(self, data):

        if self.halted:
            return

        self.halted = True

        reason = data.get("reason", "unknown")

        logger.error(
            f"[KILL SWITCH ACTIVATED] reason={reason}"
        )

        # 모든 포지션 청산 요청
        self.bus.publish(
            "risk.close_all",
            {
                "reason": reason
            }
        )

        # 신규 주문 차단
        self.bus.publish(
            "system.trading_halt",
            {
                "reason": reason
            }
        )
