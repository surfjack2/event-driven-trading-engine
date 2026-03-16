import time

from ltb.system.logger import logger
from ltb.strategy.strategy_engine import StrategyEngine
from ltb.strategy.strategy_loader import StrategyLoader


class StrategyWorker:

    SIGNAL_COOLDOWN = 3.0
    EXIT_COOLDOWN = 30.0

    MIN_VOLUME_RATIO = 0.3
    MIN_PRICE_MOVE = 0.0005

    def __init__(self, bus):

        self.bus = bus

        self.engine = StrategyEngine()

        self.universe = set()
        self.rankings = set()

        self.last_signal_time = {}
        self.last_exit_time = {}

        self.positions = {}
        self.pending_orders = set()

        # 🔴 Meta strategy control
        self.disabled_strategies = set()

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

        # 🔴 meta strategy events
        self.bus.subscribe("strategy.disabled", self.on_strategy_disabled)
        self.bus.subscribe("strategy.enabled", self.on_strategy_enabled)

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

            self.positions.pop(symbol, None)

            self.last_exit_time[symbol] = time.time()

        else:

            self.positions[symbol] = position

    def on_order_request(self, order):

        self.pending_orders.add(order["symbol"])

    def on_order_filled(self, order):

        self.pending_orders.discard(order["symbol"])

    # 🔴 Meta strategy disable
    def on_strategy_disabled(self, data):

        strategy = data.get("strategy")

        if strategy:
            self.disabled_strategies.add(strategy)

            logger.warning(
                "[STRATEGY] disabled %s",
                strategy
            )

    # 🔴 Meta strategy enable
    def on_strategy_enabled(self, data):

        strategy = data.get("strategy")

        if strategy and strategy in self.disabled_strategies:

            self.disabled_strategies.remove(strategy)

            logger.info(
                "[STRATEGY] enabled %s",
                strategy
            )

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

        volume_ratio = event.get("volume_ratio", 0)
        price_change = abs(event.get("price_change", 0))

        if volume_ratio < self.MIN_VOLUME_RATIO:
            return

        if price_change < self.MIN_PRICE_MOVE:
            return

        now = time.time()

        if now - self.last_exit_time.get(symbol, 0) < self.EXIT_COOLDOWN:
            return

        if now - self.last_signal_time.get(symbol, 0) < self.SIGNAL_COOLDOWN:
            return

        signals = self.engine.evaluate(event)

        if not signals:
            return

        for signal in signals:

            strategy_name = signal.get("strategy")

            # 🔴 Meta strategy filter
            if strategy_name in self.disabled_strategies:
                continue

            # -----------------------------
            # feature metadata
            # -----------------------------

            price = event.get("price")
            vwap = event.get("vwap")

            vwap_distance = None

            if price and vwap:
                vwap_distance = (price - vwap) / vwap

            signal["features"] = {

                "rsi": event.get("rsi"),

                "volume": event.get("volume"),
                "volume_ma": event.get("volume_ma"),
                "volume_ratio": volume_ratio,

                "vwap": vwap,
                "vwap_distance": vwap_distance,

                "ema": event.get("ema"),

                "atr": event.get("atr"),

                "price_change": event.get("price_change"),

                "volatility": event.get("volatility")
            }

            # -----------------------------
            # reason tag
            # -----------------------------

            signal["reason"] = strategy_name

            logger.info(
                "[STRATEGY] signal generated symbol=%s reason=%s",
                signal.get("symbol"),
                strategy_name
            )

            self.bus.publish("strategy.signal", signal)

        self.last_signal_time[symbol] = now
