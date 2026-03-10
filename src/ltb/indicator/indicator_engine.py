from collections import deque


class IndicatorEngine:

    def __init__(self):

        self.prices = {}

        self.rsi_period = 14
        self.stoch_period = 14
        self.ema_period = 20

    def add_price(self, symbol, price):

        if symbol not in self.prices:
            self.prices[symbol] = deque(maxlen=100)

        self.prices[symbol].append(price)

    def get_prices(self, symbol):

        return list(self.prices.get(symbol, []))

    # ==========================
    # EMA
    # ==========================

    def ema(self, symbol):

        prices = self.get_prices(symbol)

        if len(prices) < self.ema_period:
            return None

        k = 2 / (self.ema_period + 1)

        ema = prices[0]

        for p in prices[1:]:
            ema = p * k + ema * (1 - k)

        return ema

    # ==========================
    # RSI
    # ==========================

    def rsi(self, symbol):

        prices = self.get_prices(symbol)

        if len(prices) < self.rsi_period + 1:
            return None

        gains = []
        losses = []

        for i in range(1, len(prices)):

            diff = prices[i] - prices[i - 1]

            if diff > 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))

        avg_gain = sum(gains[-self.rsi_period:]) / self.rsi_period
        avg_loss = sum(losses[-self.rsi_period:]) / self.rsi_period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

    # ==========================
    # STOCH
    # ==========================

    def stochastic(self, symbol):

        prices = self.get_prices(symbol)

        if len(prices) < self.stoch_period:
            return None

        period = prices[-self.stoch_period:]

        low = min(period)
        high = max(period)

        if high == low:
            return 50

        close = prices[-1]

        k = (close - low) / (high - low) * 100

        return k
