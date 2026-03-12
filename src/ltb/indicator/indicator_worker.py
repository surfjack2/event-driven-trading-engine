from ltb.system.logger import logger
from ltb.indicator.indicator_engine import IndicatorEngine


class IndicatorWorker:

    def __init__(self, bus):

        self.bus = bus
        self.engine = IndicatorEngine()

        self.bus.subscribe(
            "market.price",
            self.on_price
        )

    def run(self):

        logger.info("[INDICATOR WORKER STARTED]")

    def on_price(self, event):

        symbol = event["symbol"]
        price = event["price"]
        volume = event.get("volume")
        prev_price = event.get("prev_price")

        # indicator engine 업데이트
        self.engine.add_price(symbol, price, volume)

        rsi = self.engine.rsi(symbol)
        ema = self.engine.ema(symbol)

        vwap = self.engine.vwap(symbol)
        upper, lower = self.engine.vwap_bands(symbol)

        volume_ma = self.engine.volume_ma(symbol)

        indicator_event = {

            "symbol": symbol,
            "price": price,
            "prev_price": prev_price,

            "volume": volume,
            "volume_ma": volume_ma,

            "rsi": rsi,
            "ema": ema,

            "vwap": vwap,
            "vwap_upper": upper,
            "vwap_lower": lower
        }

        logger.info(
            "[INDICATOR] %s price=%s vwap=%s volume=%s",
            symbol,
            price,
            vwap,
            volume
        )

        self.bus.publish(
            "market.indicator",
            indicator_event
        )


def run_indicator_worker(bus):

    worker = IndicatorWorker(bus)

    worker.run()
