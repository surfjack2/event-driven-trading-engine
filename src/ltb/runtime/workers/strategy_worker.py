from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader

import time


class StrategyWorker:

    SIGNAL_COOLDOWN = 3.0

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        self.universe = set()
        self.rankings = set()

        # signal 중복 방지
        self.last_signal_time = {}

        # 현재 보유 포지션
        self.positions = {}

        # pending orders
        self.pending_orders = set()

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

        self.bus.subscribe(
            "portfolio.update",
            self.on_portfolio_update
        )

        self.bus.subscribe(
            "order.request",
            self.on_order_request
        )

        self.bus.subscribe(
            "ORDER_FILLED",
            self.on_order_filled
        )

    def run(self):

        logger.info("[STRATEGY WORKER STARTED]")

        while True:
            time.sleep(1)

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

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        if position <= 0:

            if symbol in self.positions:
                del self.positions[symbol]

        else:

            self.positions[symbol] = position

    def on_order_request(self, order):

        symbol = order["symbol"]

        self.pending_orders.add(symbol)

    def on_order_filled(self, order):

        symbol = order["symbol"]

        if symbol in self.pending_orders:
            self.pending_orders.remove(symbol)

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

        # 이미 보유한 종목이면 차단
        if symbol in self.positions:

            logger.debug(
                "[STRATEGY] holding filtered %s",
                symbol
            )

            return

        # pending 주문 있으면 차단
        if symbol in self.pending_orders:

            logger.debug(
                "[STRATEGY] pending order filtered %s",
                symbol
            )

            return

        now = time.time()

        last = self.last_signal_time.get(symbol, 0)

        if now - last < self.SIGNAL_COOLDOWN:

            logger.debug(
                "[STRATEGY] cooldown filtered %s",
                symbol
            )

            return

        signals = self.engine.evaluate(event)

        if not signals:
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
