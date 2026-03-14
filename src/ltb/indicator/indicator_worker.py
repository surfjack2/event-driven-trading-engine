import time
from collections import defaultdict

from ltb.system.logger import logger
from ltb.indicator.indicator_engine import IndicatorEngine


class IndicatorWorker:

    def __init__(self, bus):

        self.bus = bus
        self.engine = IndicatorEngine()

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
        turnover_ma = self.engine.turnover_ma(symbol)

        atr = self.calculate_atr(symbol, price, prev_price)

        price_change = 0
        if prev_price:
            price_change = (price - prev_price) / prev_price

        vwap_gap = 0
        if vwap:
            vwap_gap = (price - vwap) / vwap

        volume_ratio = 0
        if volume and volume_ma:
            volume_ratio = volume / volume_ma

        indicator_event = {

            "symbol": symbol,
            "price": price,
            "prev_price": prev_price,

            "price_change": price_change,
            "vwap_gap": vwap_gap,
            "volume_ratio": volume_ratio,

            "volume": volume,
            "volume_ma": volume_ma,

            "turnover": price * volume if volume else 0,
            "turnover_ma": turnover_ma,

            "rsi": rsi,
            "ema": ema,

            "vwap": vwap,
            "vwap_upper": upper,
            "vwap_lower": lower,

            "atr": atr
        }

        logger.debug(
            "[INDICATOR] %s price=%s vwap=%s atr=%s",
            symbol,
            price,
            vwap,
            atr
        )

        self.bus.publish(
            "market.indicator",
            indicator_event
        )
