from ltb.system.logger import logger


class RiskKillSwitch:

    def __init__(self):

        # 최대 동시 보유 종목 수
        self.max_open_positions = 5

        # 최대 거래 횟수
        self.max_trades = 20

        self.open_positions = set()

        self.trade_count = 0

        self.enabled = True

        logger.info("[RISK KILL SWITCH INITIALIZED]")


    def update_position(self, symbol, position):

        if position > 0:
            self.open_positions.add(symbol)
        else:
            if symbol in self.open_positions:
                self.open_positions.remove(symbol)


    def record_trade(self):

        self.trade_count += 1


    def check(self, symbol):

        if not self.enabled:
            return True

        if symbol not in self.open_positions:

            if len(self.open_positions) >= self.max_open_positions:

                logger.warning("[RISK BLOCK] max open positions reached")

                return False

        if self.trade_count >= self.max_trades:

            logger.warning("[RISK BLOCK] max trades reached")

            return False

        return True
