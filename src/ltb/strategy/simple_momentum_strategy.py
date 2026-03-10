import time

from ltb.system.logger import logger


class SimpleMomentumStrategy:

    def __init__(self, config):

        indicators = config.get("indicators", {})
        risk = config.get("risk", {})
        trailing = config.get("trailing_stop", {})

        self.rsi_threshold = indicators.get("rsi_threshold", 50)
        self.stoch_threshold = indicators.get("stochastic_threshold", 20)

        self.position_size = risk.get("position_size", 1)

        self.trailing_percent = trailing.get("percent", 5)

        self.cooldown = config.get("cooldown_seconds", 10)

        self.last_trade_time = {}

        self.prev_stoch = {}

        logger.info("[STRATEGY] simple_momentum v3 initialized")

    def evaluate(self, event):

        symbol = event.get("symbol")
        price = event.get("price")

        rsi = event.get("rsi")
        stoch = event.get("stoch")
        state = event.get("market_state")

        now = time.time()

        if rsi is None or stoch is None:
            return []

        last = self.last_trade_time.get(symbol)

        if last:

            elapsed = now - last

            if elapsed < self.cooldown:

                return []

        prev_stoch = self.prev_stoch.get(symbol)

        self.prev_stoch[symbol] = stoch

        if prev_stoch is None:
            return []

        # -------------------------
        # reversal signal
        # -------------------------

        reversal = prev_stoch < 20 and stoch > 20

        # -------------------------
        # trend continuation
        # -------------------------

        trend_follow = (
            state == "trend_up"
            and rsi > 60
            and stoch > 60
        )

        if reversal or trend_follow:

            self.last_trade_time[symbol] = now

            logger.info(
                "[STRATEGY] BUY signal %s price=%s rsi=%.2f stoch=%.2f state=%s",
                symbol,
                price,
                rsi,
                stoch,
                state
            )

            signal = {

                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "qty": self.position_size,
                "strategy": "simple_momentum"

            }

            return [signal]

        # -------------------------
        # SELL signal
        # -------------------------

        if state == "trend_down":

            self.last_trade_time[symbol] = now

            logger.info(
                "[STRATEGY] SELL signal %s price=%s rsi=%.2f stoch=%.2f",
                symbol,
                price,
                rsi,
                stoch
            )

            signal = {

                "symbol": symbol,
                "action": "SELL",
                "price": price,
                "qty": self.position_size,
                "strategy": "simple_momentum"

            }

            return [signal]

        return []
