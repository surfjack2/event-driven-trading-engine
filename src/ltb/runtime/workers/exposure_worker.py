import time
from ltb.system.logger import logger


class ExposureWorker:

    DEFAULT_EXPOSURE = 0.7

    REGIME_EXPOSURE = {
        "bull": 0.9,
        "sideways": 0.6,
        "bear": 0.3,
    }

    def __init__(self, bus):

        self.bus = bus
        self.current_exposure = self.DEFAULT_EXPOSURE

        self.bus.subscribe("market.regime", self.on_regime)

    def run(self):

        logger.info("[EXPOSURE WORKER STARTED]")

        while True:
            time.sleep(5)

    def on_regime(self, data):

        regime = data.get("regime")

        if not regime:
            return

        exposure = self.REGIME_EXPOSURE.get(regime, self.DEFAULT_EXPOSURE)

        self.current_exposure = exposure

        logger.info(
            "[EXPOSURE] regime=%s exposure=%.2f",
            regime,
            exposure
        )

        self.bus.publish(
            "portfolio.exposure",
            {
                "exposure": exposure
            }
        )
