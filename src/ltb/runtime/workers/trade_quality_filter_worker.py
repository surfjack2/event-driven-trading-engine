import time
from ltb.system.logger import logger


class TradeQualityFilterWorker:

    MIN_VOLUME_RATIO = 0.8
    MAX_VOLATILITY = 0.04
    MIN_MOMENTUM = 0.0003

    # VWAP reclaim 강화 파라미터
    VWAP_RECLAIM_MIN_DISTANCE = 0.001
    VWAP_RECLAIM_MIN_VOLUME = 1.0

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe(
            "allocation.signal",
            self.on_signal
        )

    def run(self):

        logger.info("[TRADE QUALITY FILTER WORKER STARTED]")

        while True:
            time.sleep(1)

    def on_signal(self, signal):

        features = signal.get("features", {})

        volume_ratio = features.get("volume_ratio", 0)
        price_change = features.get("price_change", 0)
        vwap_distance = features.get("vwap_distance")

        atr = features.get("atr")
        price = signal.get("price")

        if not price:
            return

        # -----------------------------
        # liquidity check
        # -----------------------------

        if volume_ratio < self.MIN_VOLUME_RATIO:

            logger.info(
                "[QUALITY FILTER] rejected %s reason=liquidity",
                signal.get("symbol")
            )

            return

        # -----------------------------
        # volatility check
        # -----------------------------

        if atr:

            volatility = atr / price

            if volatility > self.MAX_VOLATILITY:

                logger.info(
                    "[QUALITY FILTER] rejected %s reason=volatility",
                    signal.get("symbol")
                )

                return

        # -----------------------------
        # momentum quality
        # -----------------------------

        if abs(price_change) < self.MIN_MOMENTUM:

            logger.info(
                "[QUALITY FILTER] rejected %s reason=weak_momentum",
                signal.get("symbol")
            )

            return

        # -----------------------------
        # VWAP reclaim 강화 필터
        # -----------------------------

        if signal.get("strategy") == "vwap_reclaim":

            if vwap_distance is None:
                return

            # reclaim depth 확인
            if vwap_distance < self.VWAP_RECLAIM_MIN_DISTANCE:

                logger.info(
                    "[QUALITY FILTER] rejected %s reason=weak_reclaim",
                    signal.get("symbol")
                )

                return

            # reclaim liquidity 확인
            if volume_ratio < self.VWAP_RECLAIM_MIN_VOLUME:

                logger.info(
                    "[QUALITY FILTER] rejected %s reason=no_reclaim_liquidity",
                    signal.get("symbol")
                )

                return

        logger.info(
            "[QUALITY FILTER] passed %s",
            signal.get("symbol")
        )

        self.bus.publish(
            "quality.signal",
            signal
        )
