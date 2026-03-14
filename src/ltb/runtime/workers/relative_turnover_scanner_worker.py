from ltb.system.logger import logger
import time


class RelativeTurnoverScannerWorker:

    SESSION_RTV = {
        "PREMARKET": 1.5,
        "OPEN": 1.8,
        "MIDDAY": 999,
        "POWERHOUR": 1.6
    }

    def __init__(self, bus):

        self.bus = bus
        self.session = "CLOSED"

        self.bus.subscribe(
            "market.indicator",
            self.on_indicator
        )

        self.bus.subscribe(
            "market.session",
            self.on_session
        )

    def run(self):

        logger.info("[RELATIVE TURNOVER SCANNER STARTED]")

        # watchdog restart 방지
        while True:
            time.sleep(60)

    def on_session(self, data):

        self.session = data.get("session", "CLOSED")

    def on_indicator(self, data):

        if self.session == "CLOSED":
            return

        symbol = data.get("symbol")

        turnover = data.get("turnover")
        turnover_ma = data.get("turnover_ma")

        if not turnover or not turnover_ma:
            return

        rtv = turnover / turnover_ma

        threshold = self.SESSION_RTV.get(self.session, 2.0)

        if rtv < threshold:
            return

        logger.info(
            "[RTV SCANNER] %s rtv=%.2f session=%s",
            symbol,
            rtv,
            self.session
        )

        self.bus.publish(
            "scanner.rtv",
            data
        )
