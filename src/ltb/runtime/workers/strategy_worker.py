from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader

import time


class StrategyWorker:

    SIGNAL_COOLDOWN = 1.0

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        self.universe = set()
        self.rankings = set()

        # duplicate signal 방지
        self.last_signal_time = {}

        # 현재 보유 포지션
        self.positions = {}

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

        # portfolio 상태 구독
        self.bus.subscribe(
            "portfolio.update",
            self.on_portfolio_update
        )

    def run(self):

        logger.info("[STRATEGY WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_portfolio_update(self, data):

        symbol = data.get("symbol")
        position = data.get("position", 0)

        if symbol is None:
            return

        if position <= 0:

            if symbol in self.positions:
                del self.positions[symbol]

        else:

            self.positions[symbol] = position

    def on_universe(self, data):

        symbols = data.get("symbols", [])

        new_universe = set(symbols)

        if new_universe != self.universe:

            self.universe = new_universe

            logger.info(
                "[STRATEGY] universe updated size=%s",
                len(self.universe)
            )

    def on_ranking(self, data):

        symbols = data.get("symbols", [])

        new_rank = set(symbols)

        if new_rank != self.rankings:

            self.rankings = new_rank

            logger.info(
                "[STRATEGY] ranking updated size=%s",
                len(self.rankings)
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

        # 이미 보유한 종목이면 전략 차단
        if symbol in self.positions:

            logger.debug(
                "[STRATEGY] holding filtered %s",
                symbol
            )

            return

        signals = self.engine.evaluate(event)

        if not signals:
            return

        now = time.time()

        last = self.last_signal_time.get(symbol, 0)

        # duplicate signal filter
        if now - last < self.SIGNAL_COOLDOWN:

            logger.debug(
                "[STRATEGY] duplicate filtered %s",
                symbol
            )

            return

        for signal in signals:

            signal["rsi"] = event.get("rsi")
            signal["volume"] = event.get("volume")
            signal["volume_ma"] = event.get("volume_ma")
            signal["vwap"] = event.get("vwap")
            signal["atr"] = event.get("atr")

            logger.info(
                "[STRATEGY] signal generated %s",
                signal
            )

            self.bus.publish(
                "strategy.signal",
                signal
            )

        self.last_signal_time[symbol] = now
