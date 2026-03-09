import time

from ltb.system.logger import logger


class ExecutionWorker:

    def __init__(self, bus):

        self.bus = bus

        self.positions = {}

        self.bus.subscribe("strategy.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)


    def run(self):

        logger.info("[EXECUTION WORKER STARTED]")

        while True:
            time.sleep(1)


    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        if position <= 0:

            self.positions.pop(symbol, None)

        else:

            self.positions[symbol] = position


    def on_signal(self, signal):

        symbol = signal["symbol"]
        price = signal["price"]

        logger.info("[EXECUTION] processing signal %s", signal)

        position = self.positions.get(symbol)

        if position:

            logger.info(
                "[POSITION GATE] already holding %s position=%s",
                symbol,
                position
            )

            return

        order = {
            "symbol": symbol,
            "side": "BUY",
            "price": price,
            "qty": 1
        }

        self.bus.publish("order.request", order)

        logger.info("[EXECUTION] order request published")
