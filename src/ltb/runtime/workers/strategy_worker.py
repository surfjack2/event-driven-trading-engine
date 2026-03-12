from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader


class StrategyWorker:

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        self.universe = set()
        self.rankings = set()

        loader = StrategyLoader()
        strategies = loader.load()

        for strategy in strategies:
            self.engine.register(strategy)

        self.bus.subscribe(
            "market.indicator",
            self.on_market
        )

        self.bus.subscribe(
            "market.universe",
            self.on_universe
        )

        self.bus.subscribe(
            "market.ranking",
            self.on_ranking
        )

    def run(self):

        logger.info("[STRATEGY WORKER STARTED]")

    def on_universe(self, data):

        symbols = data.get("symbols", [])

        new_universe = set(symbols)

        if new_universe != self.universe:

            self.universe = new_universe

            logger.info(
                f"[STRATEGY] universe updated size={len(self.universe)}"
            )

    def on_ranking(self, data):

        symbols = data.get("symbols", [])

        new_rank = set(symbols)

        if new_rank != self.rankings:

            self.rankings = new_rank

            logger.info(
                f"[STRATEGY] ranking updated size={len(self.rankings)}"
            )

    def on_market(self, event):

        symbol = event.get("symbol")
        price = event.get("price")

        if symbol is None or price is None:
            return

        # ranking 아직 없으면 거래 금지
        if not self.rankings:
            return

        if symbol not in self.rankings:
            return

        # universe 필터
        if self.universe and symbol not in self.universe:
            return

        signals = self.engine.evaluate(event)

        if not signals:
            return

        for signal in signals:

            logger.info(
                f"[STRATEGY] signal generated {signal}"
            )

            self.bus.publish(
                "strategy.signal",
                signal
            )
