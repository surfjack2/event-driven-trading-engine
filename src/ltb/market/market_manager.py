import random

from ltb.market.indicator_engine import IndicatorEngine


class MarketManager:

    def __init__(self, executor):

        self.executor = executor

        self.indicator = IndicatorEngine()

        # symbol별 price history 저장
        self.price_history = {}

    # ==========================
    # PRICE
    # ==========================

    def get_price(self, symbol):

        price = self.executor.get_price(symbol)

        if symbol not in self.price_history:
            self.price_history[symbol] = []

        self.price_history[symbol].append(price)

        # history 길이 제한
        if len(self.price_history[symbol]) > 500:
            self.price_history[symbol].pop(0)

        return price

    # ==========================
    # HISTORY
    # ==========================

    def get_history(self, symbol):

        return self.price_history.get(symbol, [])

    # ==========================
    # RSI
    # ==========================

    def get_rsi(self, symbol, period=14):

        prices = self.get_history(symbol)

        if len(prices) < period + 1:
            return None

        return self.indicator.rsi(prices, period)

    # ==========================
    # MACD
    # ==========================

    def get_macd(self, symbol):

        prices = self.get_history(symbol)

        if len(prices) < 35:
            return (None, None)

        return self.indicator.macd(prices)

    # ==========================
    # STOCHASTIC
    # ==========================

    def get_stochastic(self, symbol, period=14):

        prices = self.get_history(symbol)

        if len(prices) < period:
            return None

        return self.indicator.stochastic(prices, period)

    # ==========================
    # ATR
    # ==========================

    def get_atr(self, symbol, period=14):

        history = self.get_history(symbol)

        if history is None or len(history) < period + 1:
            return None

        trs = []

        for i in range(1, len(history)):

            high = history[i]
            low = history[i]
            prev_close = history[i - 1]

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )

            trs.append(tr)

        atr = sum(trs[-period:]) / period

        return atr
