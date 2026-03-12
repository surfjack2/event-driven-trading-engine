from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader


class StrategyWorker:

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        # 현재 거래 가능 종목
        self.universe = set()

        loader = StrategyLoader()
        strategies = loader.load()

        for strategy in strategies:
            self.engine.register(strategy)

        # indicator 이벤트 구독
        self.bus.subscribe(
            "market.indicator",
            self.on_market
        )

        # universe 업데이트
        self.bus.subscribe(
            "market.universe",
            self.on_universe
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

    def on_market(self, event):

        symbol = event.get("symbol")
        price = event.get("price")

        # 데이터 검증
        if symbol is None or price is None:
            return

        # universe 필터
        if self.universe and symbol not in self.universe:
            return

        logger.debug(
            f"[STRATEGY] evaluating symbol={symbol} price={price}"
        )

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
