from ltb.system.logger import logger
from ltb.risk.atr_stop import ATRStop


class RiskManager:

    def __init__(self, engine):

        self.engine = engine

        self.market = engine.market

        self.atr_stop = ATRStop(self.market)

        self.last_price = None

    def update_price(self, price):

        self.last_price = price

    def check_exit(self, symbol, pos, current_price):

        # ATR 기반 stop 계산
        atr_stop_price = self.atr_stop.calculate_stop(symbol, pos.entry_price)

        # Stop Loss
        if current_price <= atr_stop_price:

            logger.info(
                f"ATR STOP {symbol} entry={pos.entry_price} price={current_price}"
            )

            self.engine.exit_position(symbol, pos.qty, reason="ATR_STOP")

            return True

        return False
