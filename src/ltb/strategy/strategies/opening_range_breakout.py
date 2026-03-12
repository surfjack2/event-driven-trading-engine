from ltb.system.logger import logger
import time


class OpeningRangeBreakoutStrategy:

    def __init__(self, config=None):

        self.config = config or {}

        self.range_high = {}
        self.range_low = {}

        self.range_complete = {}

        self.start_time = 9 * 60
        self.range_minutes = 5

    def evaluate(self, event):

        symbol = event.get("symbol")

        price = event.get("price")
        volume = event.get("volume")
        volume_ma = event.get("volume_ma")
        vwap = event.get("vwap")

        if not price:
            return []

        now = time.localtime()

        minutes = now.tm_hour * 60 + now.tm_min

        # ---------------------------
        # Opening range build
        # ---------------------------

        if minutes < self.start_time + self.range_minutes:

            high = self.range_high.get(symbol, price)
            low = self.range_low.get(symbol, price)

            self.range_high[symbol] = max(high, price)
            self.range_low[symbol] = min(low, price)

            return []

        # range 완성
        self.range_complete[symbol] = True

        high = self.range_high.get(symbol)

        if not high:
            return []

        # ---------------------------
        # Breakout detection
        # ---------------------------

        if price <= high:
            return []

        # volume confirmation
        if volume and volume_ma:

            if volume < volume_ma:
                return []

        # vwap filter
        if vwap and price < vwap:
            return []

        logger.info(
            f"[ORB] breakout detected {symbol} price={price}"
        )

        signal = {

            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "strategy": "opening_range_breakout"

        }

        return [signal]
