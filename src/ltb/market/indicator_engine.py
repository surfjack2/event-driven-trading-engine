import math


class IndicatorEngine:

    # ==========================
    # RSI
    # ==========================
    @staticmethod
    def rsi(prices, period=14):

        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(1, period + 1):
            change = prices[-i] - prices[-i - 1]

            if change >= 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi

    # ==========================
    # EMA
    # ==========================
    @staticmethod
    def ema(prices, period):

        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)

        ema = sum(prices[:period]) / period

        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema

        return ema

    # ==========================
    # MACD
    # ==========================
    @staticmethod
    def macd(prices):

        if len(prices) < 26:
            return None, None

        ema12 = IndicatorEngine.ema(prices, 12)
        ema26 = IndicatorEngine.ema(prices, 26)

        macd_line = ema12 - ema26

        return macd_line

    # ==========================
    # Stochastic
    # ==========================
    @staticmethod
    def stochastic(prices, period=14):

        if len(prices) < period:
            return None

        window = prices[-period:]

        low = min(window)
        high = max(window)

        current = prices[-1]

        if high == low:
            return 50

        k = ((current - low) / (high - low)) * 100

        return k
