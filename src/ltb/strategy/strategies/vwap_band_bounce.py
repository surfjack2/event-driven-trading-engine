from ltb.system.logger import logger


class VWAPBandBounceStrategy:

    name = "vwap_bounce"

    def evaluate(self, event):

        symbol = event["symbol"]

        price = event["price"]
        prev = event.get("prev_price")

        vwap = event.get("vwap")
        vwap_lower = event.get("vwap_lower")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        if not vwap or not vwap_lower:
            return []

        touch = price <= vwap_lower
        bounce = prev and price > prev

        volume_spike = False
        if volume and volume_ma and volume_ma > 0:
            volume_spike = volume > volume_ma * 1.2

        reclaim = price >= vwap

        score = sum([
            bool(touch),
            bool(bounce),
            bool(volume_spike),
            bool(reclaim)
        ])

        if touch:
            logger.info("[VWAP_BOUNCE] lower band touched %s", symbol)

        if score >= 3:

            logger.info(
                "[VWAP_BOUNCE] signal confirmed %s score=%s",
                symbol,
                score
            )

            return [{
                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "qty": 1,
                "strategy": self.name
            }]

        return []
