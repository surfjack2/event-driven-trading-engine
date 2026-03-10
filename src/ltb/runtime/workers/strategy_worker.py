from ltb.system.logger import logger

from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader


class StrategyWorker:

    def __init__(self, bus):

        self.bus = bus

        # Strategy Engine 생성
        self.engine = StrategyEngine()

        # Strategy Loader로 전략 로딩
        loader = StrategyLoader()
        strategies = loader.load()

        # Strategy Engine에 등록
        for strategy in strategies:
            self.engine.register(strategy)

        # Market Event 구독
        self.bus.subscribe(
            "market.price",
            self.on_market
        )

    def run(self):

        logger.info("[STRATEGY WORKER STARTED]")

    def on_market(self, event):

        price = event.get("price")
        symbol = event.get("symbol")

        logger.info("[STRATEGY] received %s", price)

        # 전략 평가
        signals = self.engine.evaluate(event)

        # 시그널 처리
        for signal in signals:

            logger.info("[STRATEGY] signal generated")

            self.bus.publish(
                "strategy.signal",
                signal
            )
