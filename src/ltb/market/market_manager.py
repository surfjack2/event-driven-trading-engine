import time
from collections import defaultdict
from ltb.market.indicator_engine import IndicatorEngine

class MarketManager:

    def __init__(self, executor):

        self.executor = executor

        # 1초 캐시
        self.cache_ttl = 1

        # symbol → price
        self.price_cache = {}

        # symbol → timestamp
        self.last_update = {}

        # symbol → price history
        self.price_history = defaultdict(list)

        self.history_limit = 200

    # ==========================
    # PRICE 조회
    # ==========================

    def get_price(self, symbol):

        now = time.time()

        if symbol in self.last_update:

            if now - self.last_update[symbol] < self.cache_ttl:
                return self.price_cache[symbol]

        # API 호출
        price = self.executor.get_price()

        self.price_cache[symbol] = price
        self.last_update[symbol] = now

        self._update_history(symbol, price)

        return price

    # ==========================
    # price history 업데이트
    # ==========================

    def _update_history(self, symbol, price):

        history = self.price_history[symbol]

        history.append(price)

        if len(history) > self.history_limit:
            history.pop(0)

    # ==========================
    # history 조회
    # ==========================

    def get_history(self, symbol):

        return self.price_history[symbol]

    # ==========================
    # RSI 조회
    # ==========================

    def get_rsi(self, symbol):

        history = self.price_history[symbol]

        return IndicatorEngine.rsi(history)


    # ==========================
    # MACD 조회
    # ==========================

    def get_macd(self, symbol):

        history = self.price_history[symbol]

        return IndicatorEngine.macd(history)


    # ==========================
    # Stochastic 조회
    # ==========================

    def get_stochastic(self, symbol):

        history = self.price_history[symbol]

        return IndicatorEngine.stochastic(history)
