import time
from collections import defaultdict

from ltb.system.logger import logger
from ltb.indicator.indicator_engine import IndicatorEngine


class IndicatorWorker:

    def __init__(self, bus):

        self.bus = bus
        self.engine = IndicatorEngine()

        # ATR 계산용
        self.atr = defaultdict(float)
        self.atr_period = 14

        self.bus.subscribe(
            "market.price",
            self.on_price
        )

    def run(self):

        logger.info("[INDICATOR WORKER STARTED]")

        while True:
            time.sleep(1)

    def calculate_atr(self, symbol, price, prev_price):

        if prev_price is None:
            return 0

        tr = abs(price - prev_price)

        prev_atr = self.atr.get(symbol, tr)

        atr = (prev_atr * (self.atr_period - 1) + tr) / self.atr_period

        self.atr[symbol] = atr

        return atr

    def on_price(self, event):

        symbol = event["symbol"]
        price = event["price"]
        volume = event.get("volume")
        prev_price = event.get("prev_price")

        self.engine.add_price(symbol, price, volume)

        rsi = self.engine.rsi(symbol)
        ema = self.engine.ema(symbol)

        vwap = self.engine.vwap(symbol)
        upper, lower = self.engine.vwap_bands(symbol)

        volume_ma = self.engine.volume_ma(symbol)

        # ATR 계산
        atr = self.calculate_atr(symbol, price, prev_price)

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
            "vwap_lower": lower,

            "atr": atr
        }

        logger.debug(
            "[INDICATOR] %s price=%s vwap=%s atr=%s volume=%s",
            symbol,
            price,
            vwap,
            atr,
            volume
        )

        self.bus.publish(
            "market.indicator",
            indicator_event
        )


def run_indicator_worker(bus):

    worker = IndicatorWorker(bus)

    worker.run()
