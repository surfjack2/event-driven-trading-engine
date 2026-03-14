import time
import numpy as np
from collections import defaultdict, deque

from ltb.system.logger import logger


class CorrelationFilterWorker:

    WINDOW = 30
    MAX_CORR = 0.8

    def __init__(self, bus):

        self.bus = bus

        self.prices = defaultdict(lambda: deque(maxlen=self.WINDOW))

        self.pending_signals = []

        self.positions = set()

        self.bus.subscribe("market.price", self.on_price)
        self.bus.subscribe("intent.signal", self.on_signal)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)

    def run(self):

        logger.info("[CORRELATION FILTER WORKER STARTED]")

        while True:

            if self.pending_signals:

                self.process()

            time.sleep(0.5)

    def on_price(self, data):

        symbol = data["symbol"]
        price = data["price"]

        self.prices[symbol].append(price)

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        if position > 0:
            self.positions.add(symbol)
        else:
            self.positions.discard(symbol)

    def on_signal(self, signal):

        self.pending_signals.append(signal)

    def process(self):

        accepted = []

        for signal in self.pending_signals:

            symbol = signal["symbol"]

            if self.is_correlated(symbol, accepted):

                logger.info(
                    "[CORRELATION] filtered %s",
                    symbol
                )

                continue

            accepted.append(symbol)

            self.bus.publish(
                "filtered.intent",
                signal
            )

        self.pending_signals.clear()

    def is_correlated(self, symbol, selected):

        if symbol not in self.prices:
            return False

        p1 = list(self.prices[symbol])

        if len(p1) < self.WINDOW:
            return False

        r1 = np.diff(p1) / p1[:-1]

        compare_list = list(selected) + list(self.positions)

        for s in compare_list:

            if s not in self.prices:
                continue

            p2 = list(self.prices[s])

            if len(p2) < self.WINDOW:
                continue

            r2 = np.diff(p2) / p2[:-1]

            corr = np.corrcoef(r1, r2)[0, 1]

            if np.isnan(corr):
                continue

            if corr > self.MAX_CORR:

                return True

        return False
