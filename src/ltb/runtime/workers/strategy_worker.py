from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader


class StrategyWorker:

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        loader = StrategyLoader()
        strategies = loader.load()

        for strategy in strategies:
            self.engine.register(strategy)

        self.bus.subscribe("market.indicator", self.on_market)

    def run(self):

        logger.info("[STRATEGY WORKER STARTED]")

    def on_market(self, event):

        price = event.get("price")
        symbol = event.get("symbol")

        logger.info("[STRATEGY] received %s", price)

        signals = self.engine.evaluate(event)

        for signal in signals:

            logger.info("[STRATEGY] signal generated")

            self.bus.publish(
                "strategy.signal",
                signal
            )
