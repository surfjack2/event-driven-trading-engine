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

        # -----------------------------
        # BACKTEST / PAPER 초기화
        # -----------------------------

        if context.is_backtest() or context.is_paper():

            for symbol in self.universe:

                base_price = 55000 + random.uniform(-1000, 1000)

                self.prices[symbol] = base_price
                self.prev_prices[symbol] = None

        # -----------------------------
        # LIVE 초기화
        # -----------------------------

        if context.is_live():

            logger.info("[MARKET WORKER] live market mode")

            for symbol in self.universe:

                self.prices[symbol] = None
                self.prev_prices[symbol] = None

    # ---------------------------------
    # BACKTEST / PAPER market generator
    # ---------------------------------

    def _mock_market_tick(self):

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

        self.prev_prices[symbol] = price

        return event

    # ---------------------------------
    # LIVE market placeholder
    # ---------------------------------

    def _live_market_tick(self):

        # 실제 구현은
        # KIS / Upbit websocket 연결 예정

        time.sleep(1)

        return None

    # ---------------------------------
    # main loop
    # ---------------------------------

    def run(self):

        logger.info("[MARKET WORKER STARTED]")

        while True:

            if self.context.is_backtest() or self.context.is_paper():

                event = self._mock_market_tick()

            elif self.context.is_live():

                event = self._live_market_tick()

            else:

                event = None

            if event:

                self.event_bus.publish("market.price", event)
                self.event_bus.publish("MARKET_TICK", event)

                logger.debug(
                    f"[MARKET] {event['symbol']} price={event['price']} volume={event['volume']}"
                )

            time.sleep(0.02)
