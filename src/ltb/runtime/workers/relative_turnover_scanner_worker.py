from ltb.system.logger import logger


class RelativeTurnoverScannerWorker:

    MIN_RTV = 1.8

    def __init__(self, bus):

        self.bus = bus

        self.bus.subscribe(
            "market.indicator",
            self.on_indicator
        )

    def run(self):
        logger.info("[RELATIVE TURNOVER SCANNER STARTED]")

    def on_indicator(self, data):

        symbol = data.get("symbol")

        turnover = data.get("turnover")
        turnover_ma = data.get("turnover_ma")

        if not turnover or not turnover_ma:
            return

        rtv = turnover / turnover_ma

        if rtv < self.MIN_RTV:
            return

        logger.info(
            "[RTV SCANNER] %s rtv=%.2f",
            symbol,
            rtv
        )

        self.bus.publish(
            "scanner.rtv",
            data
        )
