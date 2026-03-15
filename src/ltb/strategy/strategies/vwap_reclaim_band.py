from ltb.system.logger import logger


class VWAPReclaimBandStrategy:

    name = "vwap_reclaim"

    def __init__(self, config=None):

        self.config = config or {}

        self.volume_ratio = self.config.get("volume_ratio", 1.3)

        self.min_volatility = self.config.get("min_volatility", 0.0005)
        self.max_volatility = self.config.get("max_volatility", 0.03)

    def evaluate(self, event):

        symbol = event["symbol"]

        price = event["price"]
        prev = event.get("prev_price")

        vwap = event.get("vwap")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        atr = event.get("atr")

        if not vwap or not prev:
            return []

        if atr:
            volatility = atr / price

            if volatility < self.min_volatility:
                return []

            if volatility > self.max_volatility:
                return []

        reclaim = prev < vwap and price >= vwap

        if not reclaim:
            return []

        logger.info("[VWAP] reclaim detected %s", symbol)

        if volume and volume_ma and volume_ma > 0:

            ratio = volume / volume_ma

            if ratio < self.volume_ratio:
                return []

        if price <= prev:
            return []

        logger.info("[VWAP] signal confirmed %s", symbol)

        return [{
            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "qty": 1,
            "strategy": self.name
        }]
