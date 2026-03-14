from collections import deque
import statistics


class IndicatorEngine:

    def __init__(self):

        self.prices = {}
        self.volumes = {}
        self.turnovers = {}

        self.rsi_period = 14
        self.ema_period = 20
        self.volume_ma_period = 20
        self.turnover_ma_period = 20

        self.vwap_band_mult = 1.2

    def add_price(self, symbol, price, volume):

        if symbol not in self.prices:
            self.prices[symbol] = deque(maxlen=200)
            self.volumes[symbol] = deque(maxlen=200)
            self.turnovers[symbol] = deque(maxlen=200)

        turnover = price * volume if volume else 0

        self.prices[symbol].append(price)
        self.volumes[symbol].append(volume)
        self.turnovers[symbol].append(turnover)

    def get_prices(self, symbol):
        return list(self.prices.get(symbol, []))

    def get_volumes(self, symbol):
        return list(self.volumes.get(symbol, []))

    def get_turnovers(self, symbol):
        return list(self.turnovers.get(symbol, []))

    def ema(self, symbol):

        prices = self.get_prices(symbol)

        if len(prices) < self.ema_period:
            return None

        k = 2 / (self.ema_period + 1)

        ema = prices[0]

        for p in prices[1:]:
            ema = p * k + ema * (1 - k)

        return ema

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

    def vwap(self, symbol):

        prices = self.get_prices(symbol)
        volumes = self.get_volumes(symbol)

        if not prices or not volumes:
            return None

        pv = sum(p * v for p, v in zip(prices, volumes))
        total_volume = sum(volumes)

        if total_volume == 0:
            return None

        return pv / total_volume

    def vwap_bands(self, symbol):

        prices = self.get_prices(symbol)

        if len(prices) < 20:
            return None, None

        vwap = self.vwap(symbol)

        std = statistics.pstdev(prices)

        band = std * self.vwap_band_mult

        upper = vwap + band
        lower = vwap - band

        return upper, lower

    def volume_ma(self, symbol):

        volumes = self.get_volumes(symbol)

        if len(volumes) < self.volume_ma_period:
            return None

        return sum(volumes[-self.volume_ma_period:]) / self.volume_ma_period

    def turnover_ma(self, symbol):

        turnovers = self.get_turnovers(symbol)

        if len(turnovers) < self.turnover_ma_period:
            return None

        return sum(turnovers[-self.turnover_ma_period:]) / self.turnover_ma_period
