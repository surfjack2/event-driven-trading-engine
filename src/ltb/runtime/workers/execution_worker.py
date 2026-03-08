import time

from ltb.system.logger import logger
from ltb.risk.risk_kill_switch import RiskKillSwitch


class ExecutionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.risk = RiskKillSwitch()

        self.bus.subscribe("strategy.signal", self.on_signal)

        self.bus.subscribe("portfolio.update", self.on_portfolio_update)


    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_portfolio_update(self, data):

        position = data["position"]

        self.risk.update_position(position)


    def on_signal(self, signal):

        logger.info("[EXECUTION] processing signal %s", signal)

        if not self.risk.check():

            logger.warning("[EXECUTION] order blocked by risk")

            return

        order = {
            "symbol": signal["symbol"],
            "side": signal["action"],
            "price": signal["price"],
            "qty": 1
        }

        self.bus.publish("order.request", order)

        self.risk.record_trade()

        logger.info("[EXECUTION] order request published")
