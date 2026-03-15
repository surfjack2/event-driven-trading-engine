import time
from collections import deque, defaultdict
import numpy as np

from ltb.system.logger import logger


class CorrelationFilterWorker:

    CORR_WINDOW = 20
    CORR_THRESHOLD = 0.85

    MAX_SYMBOL_CORR = 1

    def __init__(self, bus):

        self.bus = bus

        self.price_history = defaultdict(
            lambda: deque(maxlen=self.CORR_WINDOW)
        )

        self.positions = set()

        # 🔴 FIX: intent.signal을 받아야 한다
        self.bus.subscribe("intent.signal", self.on_intent)

        self.bus.subscribe("market.indicator", self.on_price)
        self.bus.subscribe("portfolio.update", self.on_portfolio_update)

    def run(self):

        logger.info("[CORRELATION FILTER WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_portfolio_update(self, data):

        symbol = data["symbol"]
        position = data["position"]

        if position > 0:
            self.positions.add(symbol)
        else:
            self.positions.discard(symbol)

    def on_price(self, data):

        symbol = data.get("symbol")
        price = data.get("price")

        if not symbol or not price:
            return

        self.price_history[symbol].append(price)

    def on_intent(self, signal):

        symbol = signal["symbol"]

        # 포지션 없으면 통과
        if not self.positions:

            self.bus.publish(
                "filtered.intent",
                signal
            )
            return

        history = self.price_history.get(symbol)

        if not history or len(history) < self.CORR_WINDOW:

            self.bus.publish(
                "filtered.intent",
                signal
            )
            return

        new_series = np.array(history)

        for pos_symbol in self.positions:

            pos_hist = self.price_history.get(pos_symbol)

            if not pos_hist or len(pos_hist) < self.CORR_WINDOW:
                continue

            pos_series = np.array(pos_hist)

            corr = np.corrcoef(new_series, pos_series)[0, 1]

            if corr >= self.CORR_THRESHOLD:

                logger.info(
                    "[CORRELATION FILTER] blocked %s vs %s corr=%.2f",
                    symbol,
                    pos_symbol,
                    corr
                )

                return

        logger.info(
            "[CORRELATION FILTER] passed %s",
            symbol
        )

        self.bus.publish(
            "filtered.intent",
            signal
        )
