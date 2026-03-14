from ltb.system.logger import logger


class VWAPBandBounceStrategy:

    name = "vwap_bounce"

    def __init__(self, config=None):

        self.config = config or {}

        self.volume_ratio = self.config.get("volume_ratio", 1.2)
        self.reversal_threshold = self.config.get("reversal_threshold", 0.001)

    def evaluate(self, event):

        symbol = event["symbol"]

        price = event["price"]
        prev = event.get("prev_price")

        vwap = event.get("vwap")
        vwap_lower = event.get("vwap_lower")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        if not vwap or not vwap_lower or not prev:
            return []

        # -----------------------
        # 1️⃣ lower band 위치
        # -----------------------

        if price > vwap_lower:
            return []

        logger.info("[VWAP_BOUNCE] lower band touched %s", symbol)

        # -----------------------
        # 2️⃣ 반전 확인
        # -----------------------

        reversal = (price - prev) / prev

        if reversal < self.reversal_threshold:
            return []

        # -----------------------
        # 3️⃣ volume 확인
        # -----------------------

        if volume and volume_ma and volume_ma > 0:

            ratio = volume / volume_ma

            if ratio < self.volume_ratio:
                return []

        logger.info(
            "[VWAP_BOUNCE] signal confirmed %s",
            symbol
        )

        return [{
            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "qty": 1,
            "strategy": self.name
        }]
