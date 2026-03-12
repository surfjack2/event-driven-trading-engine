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
        volume = event.get("volume", 0)
        prev_price = event.get("prev_price")

        self.engine.add_price(symbol, price, volume)

        rsi = self.engine.rsi(symbol)
        stoch = self.engine.stochastic(symbol)
        ema = self.engine.ema(symbol)

        vwap = self.engine.vwap(symbol)
        vwap_upper, vwap_lower = self.engine.vwap_bands(symbol)

        volume_ma = self.engine.volume_ma(symbol)

        indicator_event = {

            "symbol": symbol,
            "price": price,
            "prev_price": prev_price,

            "rsi": rsi,
            "stoch": stoch,
            "ema": ema,

            "vwap": vwap,
            "vwap_upper": vwap_upper,
            "vwap_lower": vwap_lower,

            "volume": volume,
            "volume_ma": volume_ma,
        }

        logger.info(
            "[INDICATOR] %s rsi=%s stoch=%s ema=%s vwap=%s",
            symbol,
            rsi,
            stoch,
            ema,
            vwap
        )

        self.bus.publish(
            "market.indicator",
            indicator_event
        )
