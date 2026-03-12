from ltb.system.logger import logger


class VWAPReclaimBandStrategy:

    def __init__(self, config=None):

        self.config = config or {}

        # Lower band 터치 상태 기록
        self.last_lower_touch = {}

    def evaluate(self, event):

        symbol = event.get("symbol")

        price = event.get("price")
        vwap = event.get("vwap")
        upper = event.get("vwap_upper")
        lower = event.get("vwap_lower")

        volume = event.get("volume")
        volume_ma = event.get("volume_ma")

        prev_price = event.get("prev_price")

        # 필수 데이터 부족 시 무시
        if not all([price, vwap, upper, lower]):
            return []

        # ------------------------
        # 1️⃣ Lower Band Touch
        # ------------------------

        if price <= lower:

            self.last_lower_touch[symbol] = True

            logger.info(
                f"[VWAP] lower band touched {symbol}"
            )

            return []

        # ------------------------
        # 2️⃣ VWAP Reclaim
        # ------------------------

        if prev_price is not None and prev_price < vwap and price > vwap:

            if not self.last_lower_touch.get(symbol):
                return []

            logger.info(
                f"[VWAP] reclaim detected {symbol}"
            )

        else:
            return []

        # ------------------------
        # 3️⃣ Volume Confirmation
        # ------------------------

        if volume_ma is not None:

            if volume < volume_ma:
                logger.info(
                    f"[VWAP] volume filter failed {symbol}"
                )
                return []

        # ------------------------
        # 4️⃣ Signal 생성
        # ------------------------

        signal = {

            "symbol": symbol,
            "action": "BUY",
            "price": price,
            "strategy": "vwap_reclaim_band"

        }

        logger.info(
            f"[VWAP] BUY signal {symbol} price={price}"
        )

        # 상태 초기화 (중요)
        self.last_lower_touch[symbol] = False

        return [signal]
