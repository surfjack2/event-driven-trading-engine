import time

from ltb.system.logger import logger


class RiskWorker:

    DAILY_LOSS_LIMIT = -50000

    def __init__(self, bus):

        self.bus = bus

        self.halted = False

        self.daily_pnl = 0

        self.bus.subscribe("POSITION_CLOSED", self.on_trade)

        self.bus.subscribe("system.halt", self.on_system_halt)


    def on_trade(self, trade):

        pnl = trade.get("pnl", 0)

        self.daily_pnl += pnl

        logger.info(
            "[RISK] daily pnl update %s",
            self.daily_pnl
        )

        if self.daily_pnl <= self.DAILY_LOSS_LIMIT:

            logger.error(
                "[RISK] DAILY LOSS LIMIT HIT %s",
                self.daily_pnl
            )

            self.bus.publish(
                "system.halt",
                {
                    "reason": "daily_loss_limit"
                }
            )


    def on_system_halt(self, data):

        reason = data.get("reason")

        logger.error(
            "[KILL SWITCH] system halt triggered reason=%s",
            reason
        )

        self.halted = True

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
