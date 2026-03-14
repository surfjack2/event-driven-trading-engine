import time

from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader


class StrategyWorker:

    SIGNAL_COOLDOWN = 3.0
    EXIT_COOLDOWN = 30.0

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        self.universe = set()
        self.rankings = set()

        self.last_signal_time = {}
        self.last_exit_time = {}

        self.positions = {}
        self.pending_orders = set()

        loader = StrategyLoader()
        strategies = loader.load()

        for strategy in strategies:
            self.engine.register(strategy)

        self.bus.subscribe("market.indicator", self.on_market)
        self.bus.subscribe("market.ranking", self.on_ranking)
        self.bus.subscribe("market.universe", self.on_universe)

        self.bus.subscribe("portfolio.update", self.on_portfolio_update)
        self.bus.subscribe("order.request", self.on_order_request)
        self.bus.subscribe("ORDER_FILLED", self.on_order_filled)

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

            self.last_exit_time[symbol] = time.time()

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

        if not self.rankings or symbol not in self.rankings:
            return

        if self.universe and symbol not in self.universe:
            return

        if symbol in self.positions:
            return

        if symbol in self.pending_orders:
            return

        now = time.time()

        last_exit = self.last_exit_time.get(symbol, 0)

        if now - last_exit < self.EXIT_COOLDOWN:
            return

        last = self.last_signal_time.get(symbol, 0)

        if now - last < self.SIGNAL_COOLDOWN:
            return

        signals = self.engine.evaluate(event)

        if not signals:
            return

        for signal in signals:

            signal["rsi"] = event.get("rsi")
            signal["volume"] = event.get("volume")
            signal["volume_ma"] = event.get("volume_ma")

            signal["vwap"] = event.get("vwap")
            signal["ema"] = event.get("ema")

            signal["atr"] = event.get("atr")

            signal["price_change"] = event.get("price_change")
            signal["volatility"] = event.get("volatility")

            logger.info(
                "[STRATEGY] signal generated %s",
                signal
            )

            self.bus.publish(
                "strategy.signal",
                signal
            )

        self.last_signal_time[symbol] = now
