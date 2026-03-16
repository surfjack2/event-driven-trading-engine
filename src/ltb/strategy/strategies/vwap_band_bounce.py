from ltb.system.logger import logger
import time


class VWAPBandBounceStrategy:

    name = "vwap_bounce"

    TOUCH_COOLDOWN = 30

    def __init__(self, config=None):

        self.config = config or {}

        self.volume_ratio = self.config.get("volume_ratio", 1.2)
        self.reversal_threshold = self.config.get("reversal_threshold", 0.001)

        self.min_volatility = self.config.get("min_volatility", 0.0005)
        self.max_volatility = self.config.get("max_volatility", 0.03)

        # 🔴 band touch state
        self.last_touch = {}

    def evaluate(self, event):

        symbol = event["symbol"]

        price = event.get("price")
        prev = event.get("prev_price")

        vwap = event.get("vwap")
        vwap_lower = event.get("vwap_lower")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        atr = event.get("atr")

        if not vwap or not vwap_lower or not prev or not price:
            return []

        # volatility filter
        if atr:

            volatility = atr / price

            if volatility < self.min_volatility:
                return []

            if volatility > self.max_volatility:
                return []

        # 🔴 band touch event detection
        touched = prev > vwap_lower and price <= vwap_lower

        if not touched:
            return []

        # 🔴 touch cooldown
        now = time.time()

        last = self.last_touch.get(symbol)

        if last and now - last < self.TOUCH_COOLDOWN:
            return []

        logger.info("[VWAP_BOUNCE] lower band touched %s", symbol)

        # reversal check
        reversal = (price - prev) / prev

        if reversal < self.reversal_threshold:
            return []

        # volume confirmation
        if volume and volume_ma and volume_ma > 0:

            ratio = volume / volume_ma

            if ratio < self.volume_ratio:
                return []

        logger.info("[VWAP_BOUNCE] signal confirmed %s", symbol)

        self.last_touch[symbol] = now

        return [{
            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "qty": 1,
            "strategy": self.name
        }]
