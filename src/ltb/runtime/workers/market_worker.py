import random
import time

from ltb.system.logger import logger
from ltb.data.universe_builder import UniverseBuilder


class MarketWorker:

    def __init__(self, event_bus, context):

        self.event_bus = event_bus
        self.context = context

        logger.info(
            f"[MARKET WORKER INIT] mode={context.mode} market={context.market}"
        )

        self.universe = UniverseBuilder().build()

        self.prices = {}
        self.prev_prices = {}

        for symbol in self.universe:

            base_price = 55000 + random.uniform(-1000, 1000)

            self.prices[symbol] = base_price
            self.prev_prices[symbol] = None

    def run(self):

        logger.info("[MARKET WORKER STARTED]")

        while True:

            symbol = random.choice(self.universe)

            move = random.uniform(-200, 200)

            self.prices[symbol] += move

            price = float(self.prices[symbol])

            volume = random.randint(1000, 10000)

            event = {
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "prev_price": self.prev_prices[symbol],
            }

            self.event_bus.publish("market.price", event)
            self.event_bus.publish("MARKET_TICK", event)

            logger.debug(
                f"[MARKET] {symbol} price={price} volume={volume}"
            )

            self.prev_prices[symbol] = price

            time.sleep(0.02)
