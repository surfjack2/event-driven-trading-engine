from ltb.system.logger import logger
from ltb.indicator.indicator_engine import IndicatorEngine


class IndicatorWorker:

    def __init__(self, bus):

        self.bus = bus
        self.engine = IndicatorEngine()

        self.bus.subscribe(
            "market.price",
            self.on_price
        )

    def run(self):

        logger.info("[INDICATOR WORKER STARTED]")

    def on_price(self, event):

        symbol = event["symbol"]
        price = event["price"]

        self.engine.add_price(symbol, price)

        rsi = self.engine.rsi(symbol)
        stoch = self.engine.stochastic(symbol)
        ema = self.engine.ema(symbol)

        indicator_event = {

            "symbol": symbol,
            "price": price,
            "rsi": rsi,
            "stoch": stoch,
            "ema": ema
        }

        logger.info(
            "[INDICATOR] %s rsi=%s stoch=%s ema=%s",
            symbol,
            rsi,
            stoch,
            ema
        )

        self.bus.publish(
            "market.indicator",
            indicator_event
        )


def run_indicator_worker(bus):

    worker = IndicatorWorker(bus)

    worker.run()
