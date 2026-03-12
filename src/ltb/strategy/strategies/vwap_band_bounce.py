from ltb.system.logger import logger


class VWAPBandBounceStrategy:

    def __init__(self, config=None):

        self.config = config or {}

        self.last_touch = {}

    def evaluate(self, event):

        symbol = event.get("symbol")

        price = event.get("price")
        prev_price = event.get("prev_price")

        vwap = event.get("vwap")
        upper = event.get("vwap_upper")
        lower = event.get("vwap_lower")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        if not all([price, lower]):
            return []

        # ------------------------
        # Lower band touch
        # ------------------------

        if price <= lower:

            self.last_touch[symbol] = True

            logger.info(
                f"[VWAP_BOUNCE] lower band touched {symbol}"
            )

            return []

        # ------------------------
        # Bounce detection
        # ------------------------

        if not self.last_touch.get(symbol):
            return []

        if prev_price and price > prev_price:

            logger.info(
                f"[VWAP_BOUNCE] bounce detected {symbol}"
            )

        else:
            return []

        # ------------------------
        # Volume confirmation
        # ------------------------

        if volume and volume_ma:

            if volume < volume_ma:
                return []

        signal = {

            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "strategy": "vwap_band_bounce"

        }

        logger.info(
            f"[VWAP_BOUNCE] BUY signal {symbol} price={price}"
        )

        return [signal]
