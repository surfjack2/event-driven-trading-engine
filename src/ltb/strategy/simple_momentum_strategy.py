from ltb.system.logger import logger


class SimpleMomentumStrategy:

    name = "simple_momentum"

    def __init__(self, config=None):

        self.config = config or {}

        self.rsi_threshold = self.config.get("rsi_threshold", 55)
        self.volume_ratio = self.config.get("volume_ratio", 1.2)
        self.price_change_threshold = self.config.get("price_change", 0.001)

        self.vwap_distance = self.config.get("vwap_distance", 0.001)

        self.min_volatility = self.config.get("min_volatility", 0.0005)
        self.max_volatility = self.config.get("max_volatility", 0.03)

    def evaluate(self, event):

        symbol = event.get("symbol")

        price = event.get("price")
        prev = event.get("prev_price")

        ema = event.get("ema")
        vwap = event.get("vwap")

        rsi = event.get("rsi")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        price_change = event.get("price_change")

        atr = event.get("atr")

        if not price or not prev:
            return []

        if atr:
            volatility = atr / price

            if volatility < self.min_volatility:
                return []

            if volatility > self.max_volatility:
                return []

        if ema and price < ema:
            return []

        if vwap:

            if price < vwap:
                return []

            dist = (price - vwap) / vwap

            if dist < self.vwap_distance:
                return []

        if rsi and rsi < self.rsi_threshold:
            return []

        if price_change and price_change < self.price_change_threshold:
            return []

        if volume and volume_ma and volume_ma > 0:

            ratio = volume / volume_ma

            if ratio < self.volume_ratio:
                return []

        logger.info("[MOMENTUM] signal confirmed %s", symbol)

        return [{
            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "qty": 1,
            "strategy": self.name
        }]
