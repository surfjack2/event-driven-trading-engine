from ltb.system.logger import logger


class VWAPReclaimBandStrategy:

    name = "vwap_reclaim"

    def evaluate(self, event):

        symbol = event["symbol"]

        price = event["price"]
        prev = event.get("prev_price")

        vwap = event.get("vwap")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        if not vwap or not prev:
            return []

        reclaim = prev < vwap and price >= vwap

        volume_spike = False
        if volume and volume_ma and volume_ma > 0:
            volume_spike = volume > volume_ma * 1.3

        momentum = price > prev

        score = sum([
            bool(reclaim),
            bool(volume_spike),
            bool(momentum)
        ])

        if reclaim:
            logger.info("[VWAP] reclaim detected %s", symbol)

        if score >= 2:

            logger.info(
                "[VWAP] signal confirmed %s score=%s",
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
